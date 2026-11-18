#!/usr/bin/env python3
"""Capability check: each model answers the binary question directly, with the passage (full information)
or without it (blind). No debate. Same instances as Phase 0 (seed 0, 100 questions x 2 variants).
Usage: capability_check.py --model anthropic/claude-haiku-4.5 [--blind] --out results/capability/x.jsonl"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from debate import data
from debate.client import BudgetGuard, OpenRouterClient, LEDGER_PATH
from debate.judge import parse_verdict

SYS = ("Answer a multiple-choice question. Reply in exactly this format:\nVerdict: A or B\n"
       "Confidence: a number from 50 to 100 (your probability that the verdict is correct)")

def msgs(i, blind):
    body = f"Question: {i.question}\n\nAnswer A: {i.answers[0]}\nAnswer B: {i.answers[1]}\n"
    if blind:
        body += "\nNo passage is available. Decide using your own knowledge and reasoning."
    else:
        body = f"Passage:\n{i.passage}\n\n" + body + "\nUse the passage."
    return [{"role": "system", "content": SYS}, {"role": "user", "content": body}]

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--blind", action="store_true")
ap.add_argument("--questions", type=int, default=100)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--reasoning", default="none")
ap.add_argument("--max-tokens", type=int, default=600)
ap.add_argument("--workers", type=int, default=3)
ap.add_argument("--budget", type=float, default=2.0)
ap.add_argument("--global-cap", type=float, default=30.0)
ap.add_argument("--out", required=True)
a = ap.parse_args()
qs = data.sample_questions(data.load_quality(seed=a.seed), a.questions, a.seed)
insts = [i for q in qs for i in data.make_instances(q, a.seed)]
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
done = set()
if os.path.exists(a.out):
    done = {json.loads(l)["iid"] for l in open(a.out) if l.strip() and not json.loads(l).get("error")}
insts = [i for i in insts if i.iid not in done]
guard = BudgetGuard(a.budget, a.global_cap, LEDGER_PATH)
log = os.path.join(ROOT, "logs", "capability", os.path.basename(a.out).replace(".jsonl", "_calls.jsonl"))
os.makedirs(os.path.dirname(log), exist_ok=True)
client = OpenRouterClient(guard, log, run_id=os.path.basename(a.out))
reasoning = None if a.reasoning == "none" else {"effort": a.reasoning}

def one(i):
    try:
        rep = client.chat(a.model, msgs(i, a.blind), max_tokens=a.max_tokens, temperature=0.0, tag="capability", reasoning=reasoning)
    except RuntimeError as e:
        if "budget" in str(e).lower():
            raise
        return {"iid": i.iid, "qid": i.qid, "error": str(e)[:200]}
    v, c = parse_verdict(rep.text)
    return {"iid": i.iid, "qid": i.qid, "model": a.model, "blind": a.blind, "correct": i.correct, "verdict": v,
            "confidence": c, "judge_correct": v == i.correct if v else None, "cost": rep.cost}

with ThreadPoolExecutor(max_workers=a.workers) as ex, open(a.out, "a") as f:
    for r in ex.map(one, insts):
        f.write(json.dumps(r) + "\n"); f.flush()
recs = [json.loads(l) for l in open(a.out) if l.strip() and not json.loads(l).get("error")]
ok = [r for r in recs if r["judge_correct"] is not None]
print(f"{a.model} blind={a.blind}: n={len(recs)} valid={len(ok)} acc={sum(r['judge_correct'] for r in ok)/max(1,len(ok)):.3f} cost=${sum(r['cost'] or 0 for r in recs):.3f}")
