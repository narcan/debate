# 09 Phase 0 Results (2026-11-15)

QuALITY dev hard subset, 100 questions (seed 0), binary task, 2 side-swap variants = 200 instances per arm. Debaters Haiku 4.5 (T=300, temp 0.7), judge GPT-5.4 nano (reasoning low, passage-blind). Analysis plan: `09-phase0-analysis-plan.md` (written before Stage 1, not changed). Raw transcripts were removed from the public repo (the passages are third-party text); 3-line samples are in `results/phase0/samples/` and `logs/phase0/samples/`. Scores `results/phase0/score_*.{json,md}`, .

## Status
Stages 0 and 1 complete. Stage 2: consultancy complete, mini-judge sweep complete, cross-exam INCOMPLETE (169 of 200 instances) because the OpenRouter key returned 402 Payment Required. I stopped at once and made no further calls. Harness ledger at stop: $20.19 total ($19.96 this task; the ledger started at $0.23). OpenRouter reports $20.00 total account credits and $20.19 usage, matching the harness ledger. The account's prepaid credit ran out; the key's $50 limit was not reached.

## Accuracy per arm (judge accuracy, per-question bootstrap 95% CI, 10,000 resamples)

| Arm | Instances | Questions | Accuracy | 95% CI | Invalid verdicts |
|---|---|---|---|---|---|
| Blind (no transcript), nano | 200 | 100 | 57.0% | [48.5, 65.5] | 0 |
| Critique-only, nano (primary) | 200 | 100 | 81.5% | [75.5, 87.5] | 1 |
| Standard N=3, nano (primary) | 200 | 100 | 77.5% | [70.5, 84.0] | 0 |
| Consultancy N=3, nano | 200 | 100 | 75.0% | [68.5, 81.0] | 0 |
| Cross-exam N=3, nano (INCOMPLETE) | 169 | 85 | 78.2% | [70.6, 85.3] | 1 |
| Standard N=3, mini judge (same transcripts re-judged) | 200 | 100 | 79.0% | [72.0, 85.5] | 2 |

## Paired comparisons (per-question differences, paired bootstrap)

| Comparison | Diff (pts) | 95% CI | Note |
|---|---|---|---|
| Critique-only minus standard (PRIMARY) | +4.0 | [-1.5, +9.5] | null per plan |
| Standard minus blind | +20.5 | [+10.0, +31.0] | |
| Critique-only minus blind | +24.5 | [+15.0, +34.0] | |
| Consultancy minus blind | +18.0 | [+8.5, +28.0] | |
| Consultancy minus critique-only | -6.5 | [-11.5, -1.5] | exploratory, no multiplicity correction |
| Consultancy minus standard | -2.5 | [-8.5, +4.0] | |
| Mini judge minus nano judge (standard) | +1.5 | [-5.0, +7.5] | |
| Cross-exam minus standard (84 fully complete questions) | +1.8 | [-5.4, +8.9] | partial arm |
| Cross-exam minus critique-only (same 84) | -3.6 | [-10.1, +3.0] | partial arm |

Outcome per the pre-registered rule: NULL. Primary CI includes 0 and |diff| < 8. Both primary arms beat blind with CIs excluding 0, but the primary difference (4.0) is below the 5 points the plan required for the second positive clause. Setup is valid by the plan's criteria (see failure modes). Point estimate favours critique-only; not distinguishable from zero at n=100 (CI half-width about 5.5 points, so MDE about 11 points here; the plan's 13 to 18 was conservative).

Cross-exam caveat: the 31 missing instances come from 402 errors in time order (the last debates), not a random subset, though the submission order is by qid so the missing questions are the tail of the sorted-qid sample; bias is probably small but unchecked.

## Quote verification (verified / total quotes, per arm)
Critique-only 92.0% (1179/1281); standard 90.7% (2840/3131); consultancy 92.5% (1718/1857); cross-exam 90.5% (partial). Haiku 4.5 invents or alters about 8 to 10% of quotes. Strict check (contiguous normalised substring), so spliced quotes count as unverified.

## Real cost
From `usage.cost` in the per-call logs (includes wasted calls from failed and retried debates).

| Arm | Calls | Real spend | Valid records | Cost per valid debate | Model (`extrapolate.py` or old cost model) |
|---|---|---|---|---|---|
| Blind | 200 | $0.033 | 200 | $0.0002 | 0.05 raw per 200 |
| Critique-only | 631 | $3.091 | 200 | $0.0137 (record cost), $0.0155 incl. waste | $0.0138 |
| Standard N=3 | 1400 | $5.909 | 200 | $0.0295 | $0.0301 extrapolate; $0.0219 old model (1.35x over) |
| Consultancy N=3 | 1200 | $3.554 | 200 | $0.0178 | none |
| Cross-exam N=3 | 1884 | $6.984 | 169 | $0.0406 | none (smoke test: $0.02 at N=2) |
| Mini judge re-judge | 200 | $0.387 | 200 | $0.0019 per judge call | |
| **Total (call logs)** | | **$19.96** | | | ledger $20.19 incl. $0.23 prior |

Wasted spend: about $0.35 in critique-only (debater calls repeated after judge-call 429 failures), about $0.12 in cross-exam. Debate costs 2.15x critique-only per instance (0.0295 vs 0.0137) with no accuracy gain. Cache read share of debater prompt tokens: critique 46%, standard 69%, consultancy 59%, cross-exam 74%.
Projection check: after Stage 1 the ledger was $9.26; projected total (consultancy 3.6 + sweep 0.4 + cross-exam about 7.5 plus waste) about $21, under $30. The projection held; the stop came from the 402, not the cap.

## Failure modes
- Position bias: judge verdict "A" rate 46% blind, 51% critique, 45% standard, 51% consultancy, 48% cross-exam, 46% mini. No always-first collapse. Standard accuracy when gold is A 72%, gold is B 83% (judge mildly favours B, the last speaker).
- Judge asymmetry in one-sided arms (side swap exposes it): critique-only 70% when the defended answer is correct vs 93% when it is wrong, so the judge leans to reject the argued answer. Consultancy is reversed: 90% when the consultant is right vs 60% when wrong, so the judge leans to trust the consultant. Pooled accuracy hides this; the primary comparison pools both. Standard 80% / 75%.
- Truncation: 84% of debater turns in standard hit the 300-token cap (finish=length), 69% critique, 52% consultancy, 70% cross-exam. Turns are routinely cut mid-sentence and quotes lost. This is a large confound: results are for T=300, not for argument quality.
- Judge calibration: self-reported confidence vs accuracy: critique 81 vs 81.5, standard 79 vs 77.5, consultancy 85 vs 75, mini 90 vs 79 (overconfident). Not a logprob measure.
- Invalid verdicts: 1 critique, 2 mini, 1 cross-exam, 0 others. Refusals: 1 refusal-like opening in standard transcripts by regex, none material. No concessions (cross-exam had no concede flag).
- Rate limits: HTTP 429 at 8 workers (143 of 200 critique-only instances failed first pass) and persistently at 3 to 4 workers. Resumable runner retried them. Throughput about 3 debates per minute (standard), 2 per minute (cross-exam).
- Blind floor: 57.0% (CI 48.5 to 65.5) is barely above the 55% gate; the nano judge is near floor on this binary task. Passes the gate by 2 points so judge was not switched. Blind accuracy 61% on variant 0 vs 53% on variant 1 is noise at this n.
- The judge is passage-blind by design, so the +20 to 25 point gain over blind is information the debaters transmit from the passage. This is the information-asymmetry setup working, not evidence that debate beats critique.

## Deviations
1. `src/debate/client.py`: retries 3 to 6 and backoff `min(3*2**i, 40)` s (was 2**i s) after 429 storms. All 21 tests pass.
2. Added `scripts/rejudge.py` and `scripts/diag.py`. The mini-judge sweep re-judges the saved nano-run standard transcripts with GPT-5.4 mini instead of running fresh debates. Same transcript text the nano judge saw; paired and cheap; but debaters were never conditioned on the judge, and it tests judge capability only. Mini blind baseline not run.
3. Global cap passed as $30.00 on the ledger (which includes the $0.23 prior), stricter than $30 for this task.
4. Cross-exam stopped at 169/200 by the 402. Scored on all valid instances (85 questions, one with a single variant) in the table and on the 84 complete questions for paired comparisons. No result for it should be used as a primary finding.
5. Per-arm CIs added beyond the plan (descriptive only). Workers set to 8 then 3 to 4; no effect on results other than waste.
6. The analysis plan's example MDE (13 to 18 points) is conservative; observed SE of the primary difference was about 2.8 points.

## Recommendation on Phase 1
Not as specified. This pilot shows the transcript-giving protocols raise a weak passage-blind judge by 18 to 25 points over blind, and that debate offers no detectable benefit over the cheaper critique-only arm (point estimate -4 points for debate, CI [-9.5, +1.5]) at 2.15x the cost. Consultancy, cross-exam and a stronger judge all land within noise of standard debate (75 to 79%). With these data debate versus critique would need about 380 questions to detect a 4-point difference at 80% power (inference from per-question SD 0.28 of the paired differences), which is beyond a cheap Phase 1.

Phase 1 is worth running only if narrowed: fix the 84% truncation first (T of 600 or a stop-at-sentence rule, or word-limited prompts), counter the one-sided judge bias (critique and consultancy lean opposite ways), use at least 300 questions, and drop arms that did not differ (consultancy, mini judge). The grant case "debate beats critique-only for weak judges" is not supported here; "debate matches critique at higher cost" is what Phase 0 found. Cross-exam needs a rerun of the missing 31 instances (about $1.3) after credit is restored. Haiku 5.5 (10x cheaper, untested) would cut Phase 1 costs.
