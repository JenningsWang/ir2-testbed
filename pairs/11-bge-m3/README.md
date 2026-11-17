# M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation

Pair: Oliver Wakeford, Mathis Lesgourgues. Method: BGE-M3 (`BAAI/bge-m3`, 568M parameters), one encoder with three heads: dense, sparse (lexical weights) and multi-vector (ColBERT). As in the paper (§4.1), dense search uses Faiss, sparse search a Lucene impact index, Multi-vec and All rerank the dense top 200, Dense+Sparse reranks the union of both top 1000, with weights 1 · dense + 0.3 · sparse + 1 · multi-vec. Compared with `rrf`, the best spring baseline. `method.py` encodes each corpus once (cached in `runs/cache/`) and computes all five modes from it. Everything ran on a Mac with PyTorch MPS: about 3 min of encoding, then 2 min for the rest. Run from the repo root:

```
pip install -r pairs/11-bge-m3/requirements.txt     # pyserini needs Java 21+
python pairs/11-bge-m3/method.py                    # 3 datasets x 5 modes → runs*/, results*.json, results_per_query.json
python testbed.py score pairs/11-bge-m3/runs --method "BGE-M3 (All)" --pair 11-bge-m3 --against rrf   # the shared row, = results.json
python pairs/11-bge-m3/translate_scifact.py --report   # hand check of 30 translations (queries_fr.json is committed)
python pairs/11-bge-m3/crosslingual.py               # French vs English SciFact queries, each mode → results_crosslingual.json
python pairs/11-bge-m3/tune_weights.py               # fusion weights tuned on the SciFact train queries → results_weights.json
python pairs/11-bge-m3/analysis.py && python pairs/11-bge-m3/results_to_md.py   # analysis/, results_all_methods.md
jupyter nbconvert --to notebook --execute --inplace pairs/11-bge-m3/reproduce.ipynb
python pairs/11-bge-m3/demo.py --build && python pairs/11-bge-m3/demo.py --web   # live demo on :8765, see demo.md
```

## Results (mode All vs RRF, nDCG@10)

| Dataset | BGE-M3 All | RRF | Δ [95% CI] | p | Recall@100 (RRF) |
|---|:-:|:-:|:-:|:-:|:-:|
| SciFact | 0.692 | 0.718 | −0.026 [−0.054, +0.003] | 0.078 | 0.914 (0.948) |
| NFCorpus | 0.336 | 0.342 | −0.006 [−0.022, +0.010] | 0.47 | 0.289 (0.310) |
| ArguAna | 0.527 | 0.549 | −0.022 [−0.036, −0.008] | 0.002 | 0.980 (0.985) |

The five modes on the three datasets: `results_all_methods.md`. The paper's comparison, read critically: `reproduce.ipynb`. In short, the paper's ordering (Sparse < Dense < Multi-vec < All) holds on SciFact and NFCorpus but not on ArguAna, where Dense is best. All over Multi-vec is noise on both, so the fusion gain comes from the multi-vector head. With French queries, Recall@100 doesn't move for Dense, Multi-vec and All (All 0.914 → 0.915, p = 0.92), while Sparse drops from 0.894 to 0.758 (p < 10⁻⁷). Weights tuned on the 809 training queries give −0.002 (p = 0.53) against the paper's, so the paper's weights stay.

## Files

| File | What it is |
|---|---|
| `method.py` | the five retrieval modes, scored with `testbed.cmd_score` |
| `results.json`, `results_<mode>.json` | mode All (the shared row) and the other four modes |
| `results_per_query.json` | per-query nDCG@10 and Recall@100 of each mode, for the paired tests in the notebook |
| `reproduce.ipynb` | our numbers next to the paper's Tables 1 and 2, the ablation tests, the weights, the compute |
| `translate_scifact.py`, `queries_fr.json`, `check_30.csv` | NLLB-200 (600M) translation of the 300 test queries; 30 checked by hand, 26 correct |
| `crosslingual.py`, `results_crosslingual.json`, `error_analysis.md` | each mode with French and English queries, and the queries French loses most on |
| `tune_weights.py`, `results_weights.json` | the weight grid on the training queries, applied once to test |
| `analysis.py`, `analysis/` | per-query comparison with RRF on SciFact and NFCorpus: where each system clearly wins |
| `demo.py`, `demo_ui.html`, `demo.md` | the live demo, spring RRF next to BGE-M3 on precomputed SciFact indexes, and the three queries |

AI use: we used Claude Code as an assistant to write parts of the code, the notebook, the README and the slides. We ran and checked all results ourselves. Details in the report.
