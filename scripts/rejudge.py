#!/usr/bin/env python3
"""Re-judge saved transcripts with another judge model (judge sweep). Same judge prompt, same transcript text
the original judge saw (turns hold the quote-marked text). Writes records like run_debates output.
Usage: rejudge.py --in results/x.jsonl --judge openai/gpt-5.4-mini --out results/y.jsonl --budget 1"""
import argparse, json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from debate.client import BudgetGuard, OpenRouterClient, LEDGER_PATH, BudgetExceeded
from debate.judge import run_judge
from debate.data import load_quality

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True)
ap.add_argument("--judge", default="openai/gpt-5.4-mini")
ap.add_argument("--out", required=True)
ap.add_argument("--budget", type=float, default=1.0)
ap.add_argument("--global-cap", type=float, default=30.0)
ap.add_argument("--reasoning", default="low")
ap.add_argument("--call-log", default=os.path.join(ROOT, "logs", "phase0", "rejudge_calls.jsonl"))
a = ap.parse_args()
qs = {q.qid: q for q in load_quality()}
guard = BudgetGuard(a.budget, a.global_cap, LEDGER_PATH)
client = OpenRouterClient(guard, a.call_log, run_id=os.path.basename(a.out))
recs = [json.loads(l) for l in open(a.inp) if l.strip()]
recs = [r for r in recs if not r.get("error")]
done = set()
if os.path.exists(a.out):
    done = {json.loads(l)["iid"] for l in open(a.out) if l.strip()}
note = {"standard": "", "cross-exam": ""}
with open(a.out, "a") as f:
    for r in recs:
        if r["iid"] in done:
            continue
        q = qs[r["qid"]]
        # recover answers order from the record: correct label and texts
        gold, dist = q.choices[q.gold], q.choices[q.distractor]
        answers = [gold, dist] if r["correct"] == "A" else [dist, gold]
        tr = "\n\n".join(f"[{t['speaker']}, {t['kind']}]\n{t['text']}" for t in r["turns"])
        try:
            v, c, rep = run_judge(client, a.judge, q.question, answers, tr, 400, {"effort": a.reasoning}, note=note.get(r["protocol"], ""))
        except BudgetExceeded as e:
            print("ABORTED", e); sys.exit(2)
        except RuntimeError as e:
            f.write(json.dumps({"iid": r["iid"], "error": str(e)[:200]}) + "\n"); continue
        n = dict(r); n.update({"verdict": v, "confidence": c, "judge_correct": (v == r["correct"]) if v else None,
                               "judge_text": rep.text, "cost": rep.cost, "judge_only": True,
                               "models": {"debater": r["models"]["debater"], "judge": a.judge},
                               "judge_prompt_tokens": rep.prompt_tokens, "judge_completion_tokens": rep.completion_tokens})
        f.write(json.dumps(n) + "\n"); f.flush()
print("done, spent", round(guard.spent, 4))
