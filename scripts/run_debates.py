#!/usr/bin/env python3
"""Run a protocol on sampled questions. Reads OPENROUTER_API_KEY from env (never printed).
Budget: --budget (this run, USD) and --global-cap (all runs, via logs/ledger.json, default env DEBATE_GLOBAL_CAP or 2.0).
Example (5-debate token check):
  run_debates.py --protocol standard --rounds 3 --questions 5 --no-swap --budget 0.6 --out results/tokencheck.jsonl
"""
import argparse, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from debate import data, protocols, runner
from debate.client import BudgetGuard, OpenRouterClient, BudgetExceeded, LEDGER_PATH

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", choices=list(protocols.PROTOCOLS), default="standard")
    ap.add_argument("--dataset", choices=["quality", "gpqa"], default="quality")
    ap.add_argument("--questions", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-swap", action="store_true", help="only variant 0 per question (no side swap)")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--debater", default="anthropic/claude-haiku-4.5")
    ap.add_argument("--judge", default="openai/gpt-5.4-nano")
    ap.add_argument("--max-tokens", type=int, default=300)
    ap.add_argument("--judge-reasoning", default="low", help="reasoning effort for the judge, or 'none' to omit")
    ap.add_argument("--judge-interaction", action="store_true")
    ap.add_argument("--concede", action="store_true")
    ap.add_argument("--budget", type=float, default=float(os.environ.get("DEBATE_RUN_BUDGET", 0.5)))
    ap.add_argument("--global-cap", type=float, default=float(os.environ.get("DEBATE_GLOBAL_CAP", 2.0)))
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--out", required=True)
    ap.add_argument("--call-log", default=os.path.join(ROOT, "logs", "calls.jsonl"))
    a = ap.parse_args()

    qs = data.load_quality(seed=a.seed) if a.dataset == "quality" else data.load_gpqa(seed=a.seed)
    qs = data.sample_questions(qs, a.questions, a.seed)
    cfg = protocols.Config(debater_model=a.debater, judge_model=a.judge, rounds=a.rounds, max_tokens=a.max_tokens,
                           judge_reasoning=None if a.judge_reasoning == "none" else {"effort": a.judge_reasoning},
                           judge_interaction=a.judge_interaction, concede=a.concede)
    guard = BudgetGuard(a.budget, a.global_cap, LEDGER_PATH)
    client = OpenRouterClient(guard, a.call_log, run_id=os.path.basename(a.out))
    try:
        recs = runner.run(qs, a.protocol, client, cfg, a.out, a.seed, a.workers, swap=not a.no_swap)
    except BudgetExceeded as e:
        print("ABORTED, budget guard:", e)
        sys.exit(2)
    print(f"{len(recs)} debates, spent ${guard.spent:.4f} this run (ledger total ${guard.prior + guard.spent:.4f})")

if __name__ == "__main__":
    main()
