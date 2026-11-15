#!/usr/bin/env python3
"""Re-extrapolate QuALITY Phase 0 cost from measured calls. Reads a tokencheck results JSONL plus the
QuALITY hard-subset passage length distribution. Per-debate model (Haiku 4.5 debater, Anthropic cache on the
passage block only, cache needs prefix >= 4096 tokens; judge is passage-blind). Usage: extrapolate.py results.jsonl"""
import json, os, sys
import numpy as np
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from debate import data

IN, OUT, CR, CW = 1.0, 5.0, 0.1, 1.25      # Haiku 4.5, USD per M
JIN, JOUT = 0.2, 1.25                       # GPT-5.4 nano
MIN_CACHE = 4096

def main():
    recs = [json.loads(l) for l in open(sys.argv[1])]
    qs = {q.qid: q for q in data.load_quality()}
    # calibrate tokens per passage char: avg debater prompt per call minus ~750 (avg transcript 750 incl. overhead guess)
    tok_per_char = np.mean([(r["debater_prompt_tokens"] / r["debater_calls"] - 300 - 700) / len(qs[r["qid"]].passage)
                            for r in recs if not r.get("error")])   # rough: transcript avg 750, overhead ~350
    L = np.array([len(q.passage) for q in qs.values()]) * tok_per_char
    def debate_cost(L, calls, out_tok=300, overhead=400):
        cost = 0.0
        cached = L >= MIN_CACHE
        for k in range(calls):
            tr = out_tok * k
            fresh = overhead + tr + (L * (CW if k == 0 else 1.0) if cached and k == 0 else (0 if cached else L))
            cr = L if (cached and k > 0) else 0
            if cached and k == 0:
                fresh = overhead + tr + L * CW
            cost += (fresh * IN + cr * CR + out_tok * OUT) / 1e6
        return cost
    jcost = (1900 * JIN + 175 * JOUT) / 1e6
    std = np.array([debate_cost(l, 6) + jcost for l in L])
    crit = np.array([debate_cost(l, 2) + jcost for l in L])
    print(f"tokens/char {tok_per_char:.3f}; hard-subset passage tokens mean {L.mean():.0f} median {np.median(L):.0f} "
          f"share >= {MIN_CACHE}: {(L >= MIN_CACHE).mean():.2f}")
    print(f"per-debate $: standard N=3 mean {std.mean():.4f}, critique-only mean {crit.mean():.4f}")
    meas = np.mean([r["cost"] for r in recs if not r.get("error")])
    print(f"measured standard mean (5 debates) {meas:.4f}")
    for name, per, n in (("standard 100q x2", std.mean(), 200), ("critique 100q x2", crit.mean(), 200)):
        print(f"{name}: raw ${per * n:.2f}, x1.5 ${1.5 * per * n:.2f}")

if __name__ == "__main__":
    main()
