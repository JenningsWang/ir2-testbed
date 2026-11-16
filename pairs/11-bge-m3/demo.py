"""Live demo on SciFact: the spring pipeline (RRF of BM25 + MiniLM) next to BGE-M3, on precomputed indexes.

Usage: python pairs/11-bge-m3/demo.py --build      → encodes the corpus once into runs/demo_index/ (about 2 min on a Mac)
       python pairs/11-bge-m3/demo.py --web        → the demo page on http://127.0.0.1:8765 (what we show in class)
       python pairs/11-bge-m3/demo.py              → same in the terminal: type a query, #<qid> for a test query, #<qid> fr in French
"""
import json
import pickle
import re
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))          # repo root, for testbed.py
import testbed

INDEX = HERE.parents[1] / "runs" / "demo_index"   # runs/ is git-ignored
W_DENSE, W_LEX, W_MUL = 1.0, 0.3, 1.0             # the paper's weights, as in method.py
N_CAND, N_HYBRID, MAX_LEN, SHOW = 200, 1000, 512, 10
MODES = ["all", "dense", "sparse", "multi-vec", "dense+sparse"]
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

corpus, queries, qrels = testbed.load("scifact")
ids = list(corpus)
queries_fr = json.load(open(HERE / "queries_fr.json", encoding="utf-8"))
by_text = {t.strip(): q for q, t in queries.items()} | {t.strip(): q for q, t in queries_fr.items()}

PRESETS = [
    {"key": "1", "label": "Hero", "qid": "1221", "lang": "en", "note": "typo: “matasteses”"},
    {"key": "2", "label": "Hero, in French", "qid": "1221", "lang": "fr", "note": "same claim, English corpus"},
    {"key": "3", "label": "Failure", "qid": "659", "lang": "en", "note": "the drug name is not in the abstract"},
    {"key": "4", "label": "Wildcard backup", "text": "Le café réduit le risque de diabète de type 2.", "note": "no label: judge by eye"},
]


def bge():
    from FlagEmbedding import BGEM3FlagModel
    return BGEM3FlagModel("BAAI/bge-m3", use_fp16=True, devices=DEVICE)


def minilm():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")


def bm25():
    """The spring BM25 (same preprocessing as testbed.bm25_search), kept as an object to query live."""
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from rank_bm25 import BM25Okapi
    from sklearn.feature_extraction.text import CountVectorizer
    nltk.download("stopwords", quiet=True)
    sw, porter, analyze = set(stopwords.words("english")), PorterStemmer(), CountVectorizer().build_analyzer()
    prep = lambda t: [porter.stem(x) for x in analyze(t) if x not in sw]
    return BM25Okapi([prep(t) for t in testbed.doc_texts(corpus)], k1=1.2, b=0.75), prep


def build():
    INDEX.mkdir(parents=True, exist_ok=True)
    texts = testbed.doc_texts(corpus)
    out = bge().encode(texts, batch_size=16, max_length=MAX_LEN,
                       return_dense=True, return_sparse=True, return_colbert_vecs=True)
    np.save(INDEX / "dense.npy", np.asarray(out["dense_vecs"], dtype=np.float32))
    pickle.dump([{k: float(v) for k, v in w.items()} for w in out["lexical_weights"]], open(INDEX / "lex.pkl", "wb"))
    vecs = [np.asarray(v, dtype=np.float16) for v in out["colbert_vecs"]]
    np.save(INDEX / "colbert.npy", np.concatenate(vecs))                      # all doc tokens, one after the other
    np.save(INDEX / "colbert_offsets.npy", np.cumsum([0] + [len(v) for v in vecs]))
    np.save(INDEX / "minilm.npy", minilm().encode(texts, batch_size=64, normalize_embeddings=True, convert_to_numpy=True))
    print("index written to", INDEX)


def rank_of(order, j):
    """1-based rank of doc j in an ordering, or None if it is not there."""
    hit = np.flatnonzero(np.asarray(order) == j)
    return int(hit[0]) + 1 if len(hit) else None


class Demo:
    def __init__(self):
        self.enc, self.mini = bge(), minilm()
        self.bm25, self.prep = bm25()
        self.D = np.load(INDEX / "dense.npy")
        self.L = pickle.load(open(INDEX / "lex.pkl", "rb"))
        self.C = np.load(INDEX / "colbert.npy", mmap_mode="r")
        self.off = np.load(INDEX / "colbert_offsets.npy")
        self.M = np.load(INDEX / "minilm.npy")

    def spring(self, text):
        """RRF (k = 60) of the BM25 and MiniLM top-100, as testbed.rrf."""
        s_bm = self.bm25.get_scores(self.prep(text))
        s_mini = self.M @ self.mini.encode([text], normalize_embeddings=True)[0]
        o_bm, o_mini = np.argsort(-s_bm)[:testbed.K], np.argsort(-s_mini)[:testbed.K]
        fused = {}
        for o in (o_bm, o_mini):
            for rank, j in enumerate(o, 1):
                fused[j] = fused.get(j, 0.0) + 1.0 / (testbed.RRF_K + rank)
        return sorted(fused, key=fused.get, reverse=True), o_bm, o_mini

    def mul(self, qc, cand):
        """Late interaction (ColBERT MaxSim) of the query tokens against each candidate."""
        qt = torch.from_numpy(np.asarray(qc, dtype=np.float32))
        return np.array([(qt @ torch.from_numpy(np.asarray(self.C[self.off[j]:self.off[j + 1]], dtype=np.float32)).T)
                         .max(dim=1).values.mean().item() for j in cand])

    def m3_search(self, text, mode="all"):
        """The five modes of method.py, on the precomputed vectors (exact search, so the same as Faiss flat)."""
        q = self.enc.encode([text], max_length=MAX_LEN, return_dense=True, return_sparse=True, return_colbert_vecs=True)
        qd, ql, qc = q["dense_vecs"][0], q["lexical_weights"][0], q["colbert_vecs"][0]
        s_dense = self.D @ qd
        s_lex = np.array([sum(float(w) * L.get(t, 0.0) for t, w in ql.items()) for L in self.L])
        o_dense, o_lex = np.argsort(-s_dense), np.argsort(-s_lex)
        pool = o_dense[:N_CAND]
        s_mul_pool = self.mul(qc, pool)                                       # always computed, for the per-head ranks
        if mode == "dense":
            order = o_dense
        elif mode == "sparse":
            order = o_lex
        elif mode == "multi-vec":
            order = pool[np.argsort(-s_mul_pool)]
        elif mode == "dense+sparse":
            cand = np.union1d(o_dense[:N_HYBRID], o_lex[:N_HYBRID])
            order = cand[np.argsort(-(W_DENSE * s_dense[cand] + W_LEX * s_lex[cand]))]
        else:
            order = pool[np.argsort(-(W_DENSE * s_dense[pool] + W_LEX * s_lex[pool] + W_MUL * s_mul_pool))]
        heads = {"dense": o_dense, "sparse": o_lex, "multi-vec": pool[np.argsort(-s_mul_pool)]}
        tok = self.enc.tokenizer.convert_ids_to_tokens
        lex = sorted(((tok(int(t)), round(float(w), 3)) for t, w in ql.items()), key=lambda x: -x[1])
        return order, heads, lex

    def search(self, text, mode="all", rel=None):
        """Everything the page shows for one query, as JSON-ready data."""
        t0 = time.time()
        text = text.strip()
        qid = by_text.get(text)
        rel = rel if rel is not None else qrels.get(qid, {})
        spring, o_bm, o_mini = self.spring(text)
        order, heads, lex = self.m3_search(text, mode)
        stems = self.prep(text)

        def doc(j, rank):
            d = corpus[ids[j]]
            words = set(re.findall(r"\w+", (d["title"] + " " + d["text"][:400]).lower()))
            return {"id": ids[j], "rank": rank, "title": d["title"], "text": d["text"][:400],
                    "relevant": ids[j] in rel, "match": sorted(w for w in words if self.prep(w) and self.prep(w)[0] in stems)}

        labelled = []
        for d in rel:
            j = ids.index(d)
            labelled.append({"id": d, "title": corpus[d]["title"], "ranks": {
                "Spring (RRF)": rank_of(spring, j), "BM25": rank_of(o_bm, j), "MiniLM": rank_of(o_mini, j),
                "M3 dense": rank_of(heads["dense"], j), "M3 sparse": rank_of(heads["sparse"], j),
                "M3 multi-vec": rank_of(heads["multi-vec"], j), "M3 final": rank_of(order, j)}})
        idf = self.bm25.idf
        return {
            "query": text, "qid": qid, "mode": mode, "ms": int(1000 * (time.time() - t0)),
            "spring": [doc(j, i + 1) for i, j in enumerate(spring[:SHOW])],
            "m3": [doc(j, i + 1) for i, j in enumerate(order[:SHOW])],
            "labelled": labelled,
            "bm25_terms": [{"t": s, "idf": round(float(idf[s]), 2) if s in idf else None} for s in dict.fromkeys(stems)],
            "m3_terms": [{"t": t.replace("▁", "·"), "w": w} for t, w in lex[:12]],
        }

    def show(self, text, rel=None):
        r = self.search(text, "all", rel)
        print(f"\nQuery: {r['query']}   ({r['ms']} ms)")
        print("BGE-M3 lexical weights:", ", ".join(f"{x['t']}={x['w']}" for x in r["m3_terms"][:8]))
        print(f"\n{'#':>2}  {'Spring: RRF (BM25 + MiniLM)':<58}  BGE-M3 (All)")
        for a, b in zip(r["spring"][:5], r["m3"][:5]):
            m = lambda d: "*" if d["relevant"] else " "
            print(f"{a['rank']:>2} {m(a)}{a['title'][:56]:<57}  {m(b)}{b['title'][:56]}")
        for d in r["labelled"]:
            print(f"\n* {d['title'][:70]}\n  " + ", ".join(f"{k} {v or '-'}" for k, v in d["ranks"].items()))


def parse(line):
    """'#1221' → test query 1221 with its labels, '#1221 fr' → its French version, anything else → free text."""
    if line.startswith("#"):
        qid, *lang = line[1:].split()
        return (queries_fr[qid] if lang and lang[0] == "fr" else queries[qid]), qrels.get(qid, {})
    return line, None


def serve(demo, port=8765):
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import parse_qs, urlparse
    page = HERE / "demo_ui.html"

    class Handler(BaseHTTPRequestHandler):
        def send(self, body, ctype):
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            url = urlparse(self.path)
            args = {k: v[0] for k, v in parse_qs(url.query).items()}
            if url.path == "/":
                self.send(page.read_bytes(), "text/html; charset=utf-8")
            elif url.path == "/api/presets":
                presets = [dict(p, text=p.get("text") or (queries_fr if p["lang"] == "fr" else queries)[p["qid"]]) for p in PRESETS]
                self.send(json.dumps(presets).encode(), "application/json")
            elif url.path == "/api/search":
                text, rel = parse(args.get("q", "").strip())
                mode = args.get("mode", "all") if args.get("mode") in MODES else "all"
                self.send(json.dumps(demo.search(text, mode, rel)).encode(), "application/json")
            else:
                self.send_error(404)

        def log_message(self, *a):
            pass

    demo.search(queries["1221"])                                              # warm up, so the first query in class is fast
    print(f"demo on http://127.0.0.1:{port}  (Ctrl-C to stop)", flush=True)
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    if "--build" in sys.argv:
        build()
        sys.exit()
    demo = Demo()
    if "--web" in sys.argv:
        serve(demo)
    elif len(sys.argv) > 1:
        demo.show(*parse(" ".join(sys.argv[1:])))
    else:
        while True:
            try:
                line = input("\nquery> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if line:
                demo.show(*parse(line))
