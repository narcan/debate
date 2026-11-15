# 07 Harness Notes (2026-11-12)

Phase 0 harness: standard debate, consultancy, critique-only, cross-exam, blind judge, on QuALITY hard subset. Measured 5-debate token check, then the Phase 0 pilot (see `README.md` and `results/phase0/`). Spend is tracked in `logs/ledger.json`.

## How to run

```
pip install -r requirements.txt
python3 -m pytest -q tests                       # mocked client, no network, 21 tests
python3 scripts/fetch_models.py                  # check IDs and record prices to data/model_prices.json
export OPENROUTER_API_KEY=...                    # env only; in this sandbox the proxy overwrites the header
python3 scripts/run_debates.py --protocol standard --rounds 3 --questions 5 --no-swap \
    --budget 0.6 --out results/tokencheck_standard_n3.jsonl --call-log logs/tokencheck_calls.jsonl
python3 scripts/score.py --run std=results/a.jsonl --run crit=results/b.jsonl --compare std crit --out results/score
python3 scripts/extrapolate.py results/tokencheck_standard_n3.jsonl
```

Protocols: `standard`, `consultancy`, `critique`, `cross-exam`, `blind`. Flags: `--rounds`, `--judge-interaction` (knob A), `--concede` (knob C, prompt only, `CONCEDE` ends the debate), `--judge-reasoning`, `--max-tokens` (T), `--no-swap`, `--workers`. Runs are resumable (done instance ids are skipped).

Budget guard: `--budget` per run (default $0.50, env `DEBATE_RUN_BUDGET`) and `--global-cap` across runs through `logs/ledger.json` (default $2, env `DEBATE_GLOBAL_CAP`). Before each call it checks spent + estimate (prompt chars/3 at list price + max_tokens at output price); it aborts with exit code 2 on breach. Cost is the `usage.cost` field from OpenRouter, with a price-table fallback.

## File map

| Path | What |
|---|---|
| `src/debate/client.py` | OpenRouter client, `BudgetGuard`, per-call JSONL log, `MockClient` |
| `src/debate/data.py` | QuALITY loader (hard = `difficult==1`), GPQA stub (local CSV only), seeded sampler, side swap, answer shuffle |
| `src/debate/protocols.py` | Protocols, `Config`, `Session` |
| `src/debate/judge.py` | Judge prompt, verdict and confidence parser, blind mode |
| `src/debate/quotes.py` | Quote marking to `<v_quote>` or `<u_quote>` |
| `src/debate/scoring.py` | Accuracy, paired bootstrap, quote rate, markdown |
| `src/debate/runner.py` | Instance loop, resume, thread pool |
| `scripts/` | `run_debates.py`, `score.py`, `fetch_models.py`, `extrapolate.py` |
| `tests/test_harness.py` | 21 tests, all pass |
| `data/model_prices.json`, `data/cache/quality_dev.jsonl` | Recorded prices; cached dataset (8.5 MB, consider gitignoring) |
| `logs/calls.jsonl` style files | Per call: model, prompt, completion, cached, cache-write, reasoning tokens, cost, latency |

Design choices: each question gives 2 instances. The task is binary, gold answer vs the validators' most-chosen best distractor. Variant 1 flips which label holds the correct answer (side swap plus answer-order shuffle, seeded per question). Debater A always speaks first and defends label A. One-sided protocols defend the correct answer in variant 0 and the wrong one in variant 1. The judge is always passage-blind (information asymmetry). Judge outputs `Verdict` and `Confidence` (50 to 100), both logged.

## Source notes

- llm_debate clone succeeded (MIT, in scratch outside the repo). Nothing imported; reused ideas only: QuALITY schema (`difficult`, `untimed_best_distractor`), html-stripped dev file with line-terminator cleanup, verified and unverified quote tags.
- QuALITY: the github.com `?raw=true` URL (as in llm_debate) is blocked by the proxy. One retry via `raw.githubusercontent.com` worked. Only the dev split was fetched (230 articles, 2086 questions, 1065 hard). Train split not fetched.
- GPQA: stub only (`load_gpqa(csv_path)` or env `GPQA_CSV`). It is gated; I did not try to download it.

## Models and prices (OpenRouter /models, 2026-11-12, USD per M tokens)

| Role | ID | in | out | cache read | cache write |
|---|---|---|---|---|---|
| Debater | `anthropic/claude-haiku-4.5` | 1.00 | 5.00 | 0.10 | 1.25 |
| Judge | `openai/gpt-5.4-nano` | 0.20 | 1.25 | 0.02 | none |
| Judge (mid, unused) | `openai/gpt-5.4-mini` | 0.75 | 4.50 | 0.075 | none |

These match `tools/prices.json`. Note: `anthropic/claude-haiku-5.5` is listed at 0.10 in and 0.50 out (10x cheaper). I did not test it; the plan says Haiku 4.5, so it is a decision for you, not something I switched.

## Measured: 5 debates, QuALITY hard, standard N=3, T=300, Haiku 4.5 vs Haiku 4.5, nano judge (reasoning effort low)

| | Measured (mean per debate) | Cost model assumption |
|---|---|---|
| Debater prompt tokens, 6 calls | 41,546 (range 20.6k to 54.9k; passages 3.7k to 8k tokens) | 40,500 (P=6000) |
| Debater completion tokens | 1,786 (25 of 35 calls hit the 300 cap) | 1,800 |
| Judge prompt tokens | 1,823 (passage-blind) | 7,800 (model gives judge P + transcript) |
| Judge completion (incl. reasoning) | 173 (114 reasoning) | 300 |
| Cached debater tokens | 24,021 read, 4,804 written | most of the context |
| Cost per debate | $0.0306 (debater 0.0301, judge 0.0006) | $0.0219 (1.40x higher) |
| Latency per call | 3.3 s mean; about 23 s per debate | n/a |

Prompt caching works on OpenRouter for Anthropic when sent as `cache_control` blocks: first call writes (1.25x), later calls read (0.1x). I cache the passage block only (identical for both debaters). Finding: caching did not fire on the 2 of 5 debates whose passage was under about 4k tokens (Haiku 4.5 minimum cacheable prefix is 4096 tokens, inference from this pattern). 84% of hard-subset questions are above it by my estimate. Do not expect any caching on GPQA at P=800 (inference, not measured); the cost model assumed it.

Cost model gap, explained: the model also caches the growing transcript and applies the write premium to all uncached input; the harness caches the passage only, and the real passage mean is 6.5k tokens. `extrapolate.py` re-models the per-debate cost over the whole hard subset and reproduces the measured mean ($0.0301 modelled vs $0.0306 measured, n=5, so a low-n check).

## Phase 0 re-extrapolation (raw, no batch; x1.5 margin)

| Item | Old raw | New raw | Basis |
|---|---|---|---|
| QuALITY standard N=3, 100 q x 2 | 4.38 | 6.02 | `extrapolate.py`, 0.0301 per debate |
| QuALITY critique-only, 100 q x 2 | 2.56 | 2.76 | `extrapolate.py`, 0.0138 per debate |
| Blind floor, QuALITY 200 | 0.27 | 0.05 | judge sees no passage, about 300 tokens in |
| GPQA screen, 8 runs, 60 q x 2 | 14.33 | 24.03 | `cost_calc.py` without `--cache` (no caching at P=800), same 1.2x and 1.3x hand factors |
| Screen centre (N=3) | 1.41 | 2.30 | same |
| Screen critique-only | 0.57 | 0.67 | same |
| Dev and debugging | 3.24 | about 4.6 | hand scaling (QuALITY 20 q at measured cost 1.8, GPQA at list price 2.8) |
| **Phase 0 raw** | **26.76** | **about 40.4** | |
| **Phase 0 x1.5** | **40.1** | **about 60.6** | |

The rise is mostly GPQA losing the cache discount (inference). Phase 0 gate ("run 10 debates, read cache hits") is half answered: QuALITY caches, GPQA likely does not. Options: halve screen scale (40 q), or test `claude-haiku-5.5`, or pad the GPQA prefix (wasteful, not recommended). Phase 1 numbers will also rise; not recomputed here.

## Known gaps

- Position choice (knob B) not built (`Config.position_choice` raises). Simultaneous, scratchpad, told-weak-judge, best-of-N not built.
- Quote budget not enforced; quotes are only verified (contiguous normalised substring; a spliced quote counts as unverified, which is correct but strict). Debaters often use markdown headings, wasting tokens; 300-token turns are often truncated mid-sentence.
- Judge confidence is self-reported, not logprob based. Judge uses reasoning effort low (reasoning tokens bill as output). The floor check (blind accuracy on 50 QuALITY q) was not run; 2 blind items run only as a smoke test.
- n=5 token check: accuracy numbers are meaningless; only tokens, cost and caching are reported.
- Only the dev split of QuALITY; hard subset has 1065 questions, enough for 300 q. GPQA loader untested against the real CSV.
- Debaters sometimes agree with the opponent or switch sides; prompt was tightened after the first smoke run, but no compliance rate is measured.
- Consultancy, critique, cross-exam each ran once on 2 questions live (smoke only) to confirm the code paths; cross-exam cost $0.02 per debate at N=2.
