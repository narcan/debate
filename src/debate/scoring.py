"""Scoring: judge accuracy, paired bootstrap CI on per-question differences, quote-verification rate."""
import json
import numpy as np


def load(path):
    with open(path) as f:
        return [r for r in (json.loads(l) for l in f if l.strip()) if not r.get("error")]


def per_question(recs):
    """qid -> mean judge accuracy over that question's instances (invalid verdicts count as wrong)."""
    d = {}
    for r in recs:
        d.setdefault(r["qid"], []).append(1.0 if r.get("judge_correct") else 0.0)
    return {k: float(np.mean(v)) for k, v in d.items()}


def paired_bootstrap(a, b, n=10000, seed=0, alpha=0.05):
    """a, b: dict qid -> accuracy. Paired on shared qids. Returns mean diff (a - b) and percentile CI."""
    ids = sorted(set(a) & set(b))
    if not ids:
        return {"n": 0, "diff": None, "lo": None, "hi": None}
    d = np.array([a[i] - b[i] for i in ids])
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(d), size=(n, len(d)))
    means = d[idx].mean(axis=1)
    lo, hi = np.percentile(means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"n": len(ids), "diff": float(d.mean()), "lo": float(lo), "hi": float(hi)}


def summarize(recs):
    n = len(recs)
    if n == 0:
        return {"n": 0}
    acc = float(np.mean([1.0 if r.get("judge_correct") else 0.0 for r in recs]))
    qt = sum(r.get("quotes_total", 0) for r in recs)
    qv = sum(r.get("quotes_verified", 0) for r in recs)
    pq = per_question(recs)
    se = float(np.std(list(pq.values()), ddof=1) / np.sqrt(len(pq))) if len(pq) > 1 else None
    by_variant = {}
    for v in (0, 1):
        x = [1.0 if r.get("judge_correct") else 0.0 for r in recs if r.get("variant") == v]
        by_variant[str(v)] = float(np.mean(x)) if x else None
    confs = [r["confidence"] for r in recs if r.get("confidence") is not None]
    return {"n": n, "n_questions": len(pq), "accuracy": acc, "accuracy_se": se,
            "accuracy_by_variant": by_variant, "n_invalid_verdict": sum(1 for r in recs if r.get("verdict") is None),
            "mean_confidence": float(np.mean(confs)) if confs else None,
            "quotes_total": qt, "quotes_verified": qv, "quote_verification_rate": (qv / qt) if qt else None,
            "mean_cost": float(np.mean([r.get("cost", 0) for r in recs])),
            "total_cost": float(sum(r.get("cost", 0) for r in recs))}


def score(runs, compare=(), n_boot=10000, seed=0):
    """runs: name -> list of records. compare: list of (name_a, name_b)."""
    out = {"runs": {k: summarize(v) for k, v in runs.items()}, "comparisons": []}
    pq = {k: per_question(v) for k, v in runs.items()}
    for a, b in compare:
        out["comparisons"].append({"a": a, "b": b, **paired_bootstrap(pq[a], pq[b], n_boot, seed)})
    return out


def markdown(res):
    f = lambda x, p=1: "n/a" if x is None else f"{100 * x:.{p}f}%"
    L = ["| run | n | questions | accuracy | invalid | mean conf | quote verif. | cost |", "|---|---|---|---|---|---|---|---|"]
    for k, s in res["runs"].items():
        if not s["n"]:
            L.append(f"| {k} | 0 | | | | | | |")
            continue
        L.append(f"| {k} | {s['n']} | {s['n_questions']} | {f(s['accuracy'])} | {s['n_invalid_verdict']} | "
                 f"{f(s['mean_confidence'], 0)} | {f(s['quote_verification_rate'])} ({s['quotes_verified']}/{s['quotes_total']}) | ${s['total_cost']:.4f} |")
    if res["comparisons"]:
        L += ["", "| a minus b | questions | diff (pts) | 95% CI (pts) |", "|---|---|---|---|"]
        for c in res["comparisons"]:
            if c["n"]:
                L.append(f"| {c['a']} - {c['b']} | {c['n']} | {100 * c['diff']:+.1f} | [{100 * c['lo']:+.1f}, {100 * c['hi']:+.1f}] |")
            else:
                L.append(f"| {c['a']} - {c['b']} | 0 | n/a | n/a |")
    return "\n".join(L) + "\n"
