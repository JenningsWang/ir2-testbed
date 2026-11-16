"""BGE-M3 on the testbed, with the five retrieval modes of the paper (section 4.1).

Same setup as the paper: dense search with Faiss, sparse search with Lucene (Pyserini impact index).

Modes:
    dense          Faiss (exact inner product) over all docs, ranked by s_dense
    sparse         Lucene impact index over all docs, ranked by s_lex
    multi-vec      rerank the dense top-200 by s_mul
    dense+sparse   rerank the union of dense top-1000 (Faiss) and sparse top-1000 (Lucene) by 1·s_dense + 0.3·s_lex
    all (default)  rerank the dense top-200 by 1·s_dense + 0.3·s_lex + 1·s_mul

Usage: python method.py                          → all datasets, mode all   → runs/
       python method.py arguana --mode sparse    → one dataset, one mode    → runs_sparse/

Extra requirements: faiss-cpu (or faiss-gpu), pyserini (needs Java 21).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import faiss
import numpy as np
import torch

import os, shutil
if shutil.which("javac") is None and "JAVA_HOME" not in os.environ:
    import jdk
    java_dir = Path.home() / ".jdk"
    found = list(java_dir.glob("jdk-21*")) if java_dir.exists() else []
    home = str(found[0]) if found else jdk.install("21", path=str(java_dir))
    os.environ["JAVA_HOME"] = home
    os.environ["PATH"] = home + "/bin:" + os.environ["PATH"]

from pyserini.search.lucene import LuceneImpactSearcher
from tqdm import tqdm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))          # repo root, for testbed.py
import testbed
from FlagEmbedding import BGEM3FlagModel

MODES = ["dense", "sparse", "multi-vec", "dense+sparse", "all"]
W_DENSE, W_LEX, W_MUL = 1.0, 0.3, 1.0             # the paper's weights for MIRACL / MKQA
N_CAND = 200                                      # dense candidates reranked (multi-vec, all), as in the paper
N_HYBRID = 1000                                   # top-k from dense and from sparse (dense+sparse), as in the paper
MAX_LEN = 512                                     # 200 words fit; ArguAna queries are full arguments
CHUNK = 1000                                      # encode in chunks to keep RAM low
QUANT = 100                                       # Lucene stores integer impacts: weight -> round(weight * 100)
INDEX_DIR = HERE / "indexes"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)


def encode(texts, colbert=True):
    """Encode texts with the three BGE-M3 heads (multi-vectors only if colbert=True).

    Returns:
        dense: np.ndarray (n_texts, 1024), one normalized [CLS] vector per text
        lexical:   list of n_texts dicts {token id (str): weight}, only non-zero tokens
        mul_vec:   list of n_texts np.ndarray (n_tokens_i, 1024), one vector per token, fp16 (empty if colbert=False)
    """
    dense, lexical, mul_vec = [], [], []
    for i in range(0, len(texts), CHUNK):
        out = model.encode(texts[i:i + CHUNK], batch_size=32, max_length=MAX_LEN,
                           return_dense=True, return_sparse=True, return_colbert_vecs=colbert)
        dense.append(np.asarray(out["dense_vecs"], dtype=np.float32))
        lexical += out["lexical_weights"]
        if colbert:
            mul_vec += [np.asarray(v, dtype=np.float16) for v in out["colbert_vecs"]]
    return np.vstack(dense), lexical, mul_vec

def faiss_index(D_dense):
    """Exact inner-product index (vectors are normalized, so this is cosine)."""
    index = faiss.IndexFlatIP(D_dense.shape[1])
    index.add(D_dense)
    return index


# Sparse: Lucene (Pyserini impact index)
def quantize(weights):
    """{token id: float weight} -> {token id: int impact}, dropping tokens that round to 0."""
    return {tok: int(round(float(x) * QUANT)) for tok, x in weights.items() if round(float(x) * QUANT) > 0}


def lucene_index(name, ids, D_lex):
    """Write the doc weights as a JsonVectorCollection and build a Lucene impact index (once per dataset)."""
    index_path = INDEX_DIR / f"{name}_lucene"
    if index_path.exists():
        return index_path
    coll_dir = INDEX_DIR / f"{name}_collection"
    coll_dir.mkdir(parents=True, exist_ok=True)
    with open(coll_dir / "docs.jsonl", "w") as f:
        for doc_id, w in zip(ids, D_lex):
            f.write(json.dumps({"id": doc_id, "contents": "", "vector": quantize(w)}) + "\n")
    subprocess.run([sys.executable, "-m", "pyserini.index.lucene",
                    "--collection", "JsonVectorCollection",
                    "--input", str(coll_dir),
                    "--index", str(index_path),
                    "--generator", "DefaultLuceneDocumentGenerator",
                    "--threads", "8",
                    "--impact", "--pretokenized"], check=True)
    return index_path


def lex_score(q, d):
    """s_lex = sum over shared tokens of w_q,t * w_p,t (exact float weights, as in FlagEmbedding)."""
    return sum(float(x) * float(d[t]) for t, x in q.items() if t in d)


def colbert_batch(q, docs):
    """Late interaction for one query against all its candidates at once, on GPU:
    each query token takes its best document token, averaged over query tokens."""
    # Padding: docs have different token counts, so we pad them with zeros to the longest one (L)
    # to stack them in a single tensor D of shape (candidates, L, 1024).
    L = max(len(d) for d in docs)
    D = np.zeros((len(docs), L, q.shape[1]), dtype=np.float16)
    mask = np.zeros((len(docs), L), dtype=bool)
    for k, d in enumerate(docs):
        D[k, :len(d)] = d
        mask[k, :len(d)] = True
    q = torch.from_numpy(np.asarray(q, dtype=np.float16)).to(DEVICE)
    D, mask = torch.from_numpy(D).to(DEVICE), torch.from_numpy(mask).to(DEVICE)
    sim = torch.einsum("qh,kdh->kqd", q, D).float()
    sim = sim.masked_fill(~mask[:, None, :], float("-inf"))
    return sim.max(dim=2).values.mean(dim=1).cpu().numpy()


def search(name, mode="all", queries=None):
    corpus, test_queries, _ = testbed.load(name)
    queries = queries or test_queries                          
    ids, qids = list(corpus), list(queries)
    pos = {doc_id: j for j, doc_id in enumerate(ids)}
    colbert = mode in ("multi-vec", "all")                      # multi-vectors only when needed (RAM)
    D_dense, D_lex, D_mul = encode(testbed.doc_texts(corpus), colbert)   # same text as the baselines
    Q_dense, Q_lex, Q_mul = encode([queries[q] for q in qids], colbert)  # no query prefix for M3

    # Dense first stage: Faiss
    dense_k = {"dense": testbed.K + 1, "dense+sparse": N_HYBRID}.get(mode, N_CAND)
    if mode != "sparse":
        _, dense_hits = faiss_index(D_dense).search(Q_dense, dense_k)

    # Sparse first stage: Lucene
    if mode in ("sparse", "dense+sparse"):
        searcher = LuceneImpactSearcher(str(lucene_index(name, ids, D_lex)), query_encoder=None)
        sparse_k = testbed.K + 1 if mode == "sparse" else N_HYBRID

    run = {}
    for i, q in enumerate(tqdm(qids, desc=f"{name} {mode}")):
        if mode == "dense":
            cand = dense_hits[i][dense_hits[i] >= 0]
            s = Q_dense[i] @ D_dense[cand].T
        elif mode == "sparse":
            hits = searcher.search(quantize(Q_lex[i]), k=sparse_k)
            cand = np.array([pos[h.docid] for h in hits], dtype=int)
            s = np.array([h.score for h in hits], dtype=float)
        elif mode == "dense+sparse":
            hits = searcher.search(quantize(Q_lex[i]), k=sparse_k)
            sparse_cand = [pos[h.docid] for h in hits]
            cand = np.union1d(dense_hits[i][dense_hits[i] >= 0], sparse_cand).astype(int)
            s_dense = Q_dense[i] @ D_dense[cand].T
            s_lex = np.array([lex_score(Q_lex[i], D_lex[j]) for j in cand])
            s = W_DENSE * s_dense + W_LEX * s_lex
        else:                                                   # multi-vec and all: rerank the dense top-200
            cand = dense_hits[i][dense_hits[i] >= 0]
            s_mul = colbert_batch(Q_mul[i], [D_mul[j] for j in cand])
            if mode == "multi-vec":
                s = s_mul
            else:
                s_dense = Q_dense[i] @ D_dense[cand].T
                s_lex = np.array([lex_score(Q_lex[i], D_lex[j]) for j in cand])
                s = W_DENSE * s_dense + W_LEX * s_lex + W_MUL * s_mul
        order = np.argsort(-s)[:testbed.K + 1]                  # top 101 (ArguAna drops one)
        run[q] = {ids[cand[k]]: float(s[k]) for k in order}
    return run


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="*", default=testbed.DATASETS, help="default: all three")
    parser.add_argument("--mode", choices=MODES, default="all")
    args = parser.parse_args()

    out_dir = HERE / ("runs" if args.mode == "all" else "runs_" + args.mode.replace("+", "_"))
    for name in args.datasets:
        testbed.save_run(search(name, args.mode), out_dir / f"{name}.json")
        print(name, args.mode, "done", flush=True)