"""Per-query comparison of BGE-M3 with a baseline: the queries where one system clearly beats the other.

Usage: python analysis.py                                   → SciFact and NFCorpus, BGE-M3 All vs RRF
       python analysis.py nfcorpus --against bge --n 10     → one dataset, another baseline, more examples
       python analysis.py --run-dir runs_dense              → another BGE-M3 mode
Writes analysis/<dataset>_vs_<baseline>.md next to this file.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))          # repo root, for testbed.py
import testbed

TOP = 5                                           # documents shown per system for each example
CLEAR = 0.1                                       # |Δ nDCG@10| above which a system "clearly" wins a query


def ranking(run, q, name):
    """Document ids of a run for one query, best first, as scored by the testbed."""
    ranked = sorted(run[q], key=run[q].get, reverse=True)
    if name == "arguana":                         # the query's own document is removed, as in testbed.score_run
        ranked = [d for d in ranked if d != q]
    return ranked[:testbed.K]


def first_relevant(ranked, rel):
    """Rank (1-based) of the first relevant document, or '>100' if none is retrieved."""
    return next((i for i, d in enumerate(ranked, 1) if d in rel), ">100")


def words(text):
    return {w for w in re.findall(r"\w+", text.lower()) if len(w) > 3}


def overlap(query, text):
    """Share of the query's words (> 3 letters) that appear in the text."""
    q = words(query)
    return len(q & words(text)) / len(q) if q else 0.0


def short(text, n=70):
    text = " ".join(text.split()).replace("|", "/")
    return text if len(text) <= n else text[:n - 1] + "…"


def example(i, ctx):
    """One query as markdown: scores, ranks of the first relevant document, top documents of both systems."""
    q, name, corpus, queries = ctx["qids"][i], ctx["name"], ctx["corpus"], ctx["queries"]
    rel = {d: g for d, g in ctx["qrels"][q].items() if g > 0}
    r_ours, r_base = ranking(ctx["ours"], q, name), ranking(ctx["base"], q, name)
    doc = lambda d: corpus[d]["title"] + " " + corpus[d]["text"]
    ov = max((overlap(queries[q], doc(d)) for d in rel if d in corpus), default=0.0)
    lines = [f"### Query {q}: Δ nDCG@10 {ctx['delta'][i]:+.2f} ({ctx['me']} {ctx['nd_ours'][i]:.2f}, "
             f"{ctx['label']} {ctx['nd_base'][i]:.2f})", "",
             f"> {queries[q]}", "",
             f"- Relevant documents: {len(rel)}. First relevant at rank {first_relevant(r_ours, rel)} ({ctx['me']}) "
             f"vs {first_relevant(r_base, rel)} ({ctx['label']})",
             f"- Lexical overlap: {ov:.0%} of the query words appear in the closest relevant document", "",
             f"| Rank | {ctx['me']} | Rel. | {ctx['label']} | Rel. |", "|:-:|---|:-:|---|:-:|"]
    title = lambda d: short(corpus[d]["title"] or corpus[d]["text"])
    for k in range(TOP):
        cells = []
        for r in (r_ours, r_base):
            d = r[k] if k < len(r) else None
            cells += [title(d) if d else "", str(rel[d]) if d in rel else ""]
        lines.append(f"| {k + 1} | " + " | ".join(cells) + " |")
    return lines + [""]


def analyse(name, run_dir, against, n):
    corpus, queries, qrels = testbed.load(name)
    ours = json.load(open(run_dir / f"{name}.json"))
    base = testbed.baseline_run(name, against)
    qids, nd_ours, _ = testbed.score_run(ours, name)
    _, nd_base, _ = testbed.score_run(base, name)
    delta = nd_ours - nd_base
    me = "BGE-M3 (All)" if run_dir.name == "runs" else f"BGE-M3 ({run_dir.name.removeprefix('runs_')})"
    label = testbed.LABELS[against]
    ctx = dict(name=name, qids=qids, corpus=corpus, queries=queries, qrels=qrels, ours=ours, base=base,
               nd_ours=nd_ours, nd_base=nd_base, delta=delta, me=me, label=label)

    order = np.argsort(-delta)
    ours_wins = [i for i in order if delta[i] > CLEAR]
    base_wins = [i for i in order[::-1] if delta[i] < -CLEAR]
    ties = len(qids) - len(ours_wins) - len(base_wins)

    def mean_overlap(idx):
        vals = [max((overlap(queries[qids[i]], corpus[d]["title"] + " " + corpus[d]["text"])
                     for d, g in qrels[qids[i]].items() if g > 0 and d in corpus), default=0.0) for i in idx]
        return f"{np.mean(vals):.0%}" if vals else "n/a"

    lines = [f"# {name}: {me} vs {label}", "",
             f"nDCG@10: {me} {nd_ours.mean():.3f}, {label} {nd_base.mean():.3f} ({len(qids)} queries).", "",
             f"| Per query (Δ beyond ±{CLEAR}) | Queries | Mean lexical overlap |", "|---|:-:|:-:|",
             f"| {me} clearly better | {len(ours_wins)} | {mean_overlap(ours_wins)} |",
             f"| No clear difference | {ties} | |",
             f"| {label} clearly better | {len(base_wins)} | {mean_overlap(base_wins)} |", "",
             "Lexical overlap = share of the query words (> 3 letters) found in the closest relevant document.", "",
             f"## {me} clearly better", ""]
    for i in ours_wins[:n]:
        lines += example(i, ctx)
    lines += [f"## {label} clearly better", ""]
    for i in base_wins[:n]:
        lines += example(i, ctx)

    out = HERE / "analysis" / f"{name}_vs_{against}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{name}: {me} better on {len(ours_wins)}, {label} better on {len(base_wins)}, "
          f"no clear difference on {ties} → {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datasets", nargs="*", default=["scifact", "nfcorpus"])
    parser.add_argument("--run-dir", default="runs", help="BGE-M3 runs, relative to this folder (default: runs = All)")
    parser.add_argument("--against", choices=testbed.SYSTEMS, default="rrf")
    parser.add_argument("--n", type=int, default=5, help="examples shown in each direction")
    args = parser.parse_args()
    for name in args.datasets:
        analyse(name, HERE / args.run_dir, args.against, args.n)