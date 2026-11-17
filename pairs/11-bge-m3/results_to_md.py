"""Gather the results*.json files of this pair into one Markdown file (results_all_methods.md).

Usage (from anywhere): python pairs/11-bge-m3/results_to_md.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# file name -> label, in the order of the table
MODES = [("results_dense.json", "Dense"), ("results_sparse.json", "Sparse"),
         ("results_multi-vec.json", "Multi-vec"), ("results_dense_sparse.json", "Dense+Sparse"),
         ("results.json", "All")]


def fmt_p(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def fmt_delta(d):
    """Δ [95 % CI], in bold when significant (p < 0.05 and CI excludes zero), like the shared table."""
    lo, hi = d["ci95"]
    text = f"{d['delta']:+.3f} [{lo:+.3f}, {hi:+.3f}]"
    significant = d["p"] < 0.05 and (lo > 0 or hi < 0)
    return f"**{text}**" if significant else text


def main():
    results = {}
    for filename, label in MODES:
        path = HERE / filename
        if path.exists():
            results[label] = json.loads(path.read_text())["datasets"]
        else:
            print(f"missing: {path.name} (skipped)")

    datasets = list(dict.fromkeys(ds for r in results.values() for ds in r))
    lines = ["# BGE-M3 results (pair 11)", "",
             "A difference is in bold only when its p-value is below 0.05 and its confidence interval excludes zero.", ""]

    for ds in datasets:
        lines += [f"## {ds}", "",
                  "| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |",
                  "|---|:-:|:-:|---|:-:|:-:|"]
        baseline = next(r[ds]["baseline"] for r in results.values() if ds in r)
        lines.append(f"| *{baseline['name'].upper()}* | {baseline['ndcg10']:.3f} | {baseline['recall100']:.3f} | | | |")
        for label, r in results.items():
            if ds not in r:
                continue
            d = r[ds]
            cmp = d["ndcg10_vs_baseline"]
            lines.append(f"| BGE-M3 ({label}) | {d['ndcg10']:.3f} | {d['recall100']:.3f} | "
                         f"{d['baseline']['name'].upper()} | {fmt_delta(cmp)} | {fmt_p(cmp['p'])} |")
        lines.append("")

    out = HERE / "results_all_methods.md"
    out.write_text("\n".join(lines))
    print(f"written: {out}")


if __name__ == "__main__":
    main()