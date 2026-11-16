"""Live demo on SciFact: the spring pipeline (RRF of BM25 + MiniLM) next to BGE-M3 (All), on precomputed indexes.

Usage: python pairs/11-bge-m3/demo.py --build      → encodes the corpus once into runs/demo_index/ (about 4 min on a Mac)
       python pairs/11-bge-m3/demo.py              → prompt: type a query, or #<qid> for a test query, #<qid> fr for its French version
       python pairs/11-bge-m3/demo.py "aspirin reduces colorectal cancer"
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))          # repo root, for testbed.py
import testbed

INDEX = HERE.parents[1] / "runs" / "demo_index"   # runs/ is git-ignored
W_DENSE, W_LEX, W_MUL = 1.0, 0.3, 1.0             # the paper's weights, as in method.py
N_CAND, MAX_LEN, SHOW = 200, 512, 5
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

corpus, queries, qrels = testbed.load("scifact")
ids = list(corpus)
queries_fr = json.load(open(HERE / "queries_fr.json", encoding="utf-8"))


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


class Demo:
    def __init__(self):
        self.m3, self.mini = bge(), minilm()
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
        fused = {}
        for s in (s_bm, s_mini):
            for rank, j in enumerate(np.argsort(-s)[:testbed.K], 1):
                fused[j] = fused.get(j, 0.0) + 1.0 / (testbed.RRF_K + rank)
        return sorted(fused, key=fused.get, reverse=True), {"bm25": s_bm, "minilm": s_mini}

    def m3_all(self, text):
        """Dense top-200, reranked by 1·dense + 0.3·lexical + 1·multi-vector, as method.py --mode all."""
        q = self.m3.encode([text], max_length=MAX_LEN, return_dense=True, return_sparse=True, return_colbert_vecs=True)
        qd, ql, qc = q["dense_vecs"][0], q["lexical_weights"][0], q["colbert_vecs"][0]
        s_dense_all = self.D @ qd
        cand = np.argsort(-s_dense_all)[:N_CAND]
        s_lex = np.array([sum(float(w) * self.L[j].get(t, 0.0) for t, w in ql.items()) for j in cand])
        qt = torch.from_numpy(np.asarray(qc, dtype=np.float32))
        s_mul = np.array([(qt @ torch.from_numpy(np.asarray(self.C[self.off[j]:self.off[j + 1]], dtype=np.float32)).T)
                          .max(dim=1).values.mean().item() for j in cand])
        s = W_DENSE * s_dense_all[cand] + W_LEX * s_lex + W_MUL * s_mul
        order = np.argsort(-s)
        heads = {"dense": s_dense_all[cand], "sparse": s_lex, "multi-vec": s_mul}
        return list(cand[order]), heads, cand, {t: round(float(w), 2) for t, w in ql.items()}

    def show(self, text, rel=None):
        rel = rel or {}
        spring, _ = self.spring(text)
        m3, heads, cand, ql = self.m3_all(text)
        print(f"\nQuery: {text}")
        tok = self.m3.tokenizer.convert_ids_to_tokens
        top_lex = sorted(ql.items(), key=lambda x: -x[1])[:8]
        print("BGE-M3 lexical weights:", ", ".join(f"{tok(int(t))}={w}" for t, w in top_lex))
        print(f"\n{'#':>2}  {'Spring: RRF (BM25 + MiniLM)':<58}  BGE-M3 (All)")
        for i in range(SHOW):
            a, b = ids[spring[i]], ids[m3[i]]
            mark = lambda d: "*" if d in rel else " "
            print(f"{i + 1:>2} {mark(a)}{corpus[a]['title'][:56]:<57}  {mark(b)}{corpus[b]['title'][:56]}")
        for d in rel:
            j = ids.index(d)
            r_s = spring.index(j) + 1 if j in spring[:testbed.K] else ">100"
            r_m = m3.index(j) + 1 if j in m3 else ">200 (not in the dense pool)"
            line = f"\n* relevant: {corpus[d]['title'][:70]}\n  rank: spring {r_s}, BGE-M3 {r_m}"
            if j in cand:                          # where each head alone would put it among the 200 candidates
                k = list(cand).index(j)
                line += "  | among the 200 candidates, by head: " + ", ".join(
                    f"{h} {int((v > v[k]).sum()) + 1}" for h, v in heads.items())
            print(line)


def parse(line):
    """'#1221' → test query 1221 with its labels, '#1221 fr' → its French version, anything else → free text."""
    if line.startswith("#"):
        qid, *lang = line[1:].split()
        text = queries_fr[qid] if lang and lang[0] == "fr" else queries[qid]
        return text, qrels.get(qid, {})
    return line, {}


if __name__ == "__main__":
    if "--build" in sys.argv:
        build()
        sys.exit()
    demo = Demo()
    if len(sys.argv) > 1:
        demo.show(*parse(" ".join(sys.argv[1:])))
        sys.exit()
    while True:
        try:
            line = input("\nquery> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if line:
            demo.show(*parse(line))
