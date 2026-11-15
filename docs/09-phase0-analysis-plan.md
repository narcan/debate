# 09 Phase 0 Analysis Plan (written before Stage 1, 2026-11-15)

Frozen before any critique-only or debate result is seen. Only the blind-judge result (Stage 0) was known: 57.0% on 200 instances (100 questions), passing the gate (55% to 90%). Deviations go in `09-phase0-results.md`.

## Setup
- Data: QuALITY dev, hard subset (difficult==1), 100 questions, seed 0, binary (gold vs best distractor), 2 side-swap variants per question = 200 instances per arm.
- Debaters: anthropic/claude-haiku-4.5, T=300, temperature 0.7. Judge: openai/gpt-5.4-nano (reasoning low), passage-blind, sees transcript with verified/unverified quote tags.
- Unit of analysis: question. Per-question accuracy = mean of its 2 instances (as in `scoring.per_question`). Invalid verdicts count as wrong.

## Primary comparison
Critique-only (N=1) vs standard debate (N=3), nano judge. Statistic: mean over questions of (critique acc minus standard acc), paired bootstrap, 10,000 resamples of questions, seed 0, 95% percentile CI.

## Secondary comparisons (all same paired bootstrap, no multiplicity correction, exploratory)
1. Each arm vs blind baseline (does any transcript help the judge at all).
2. Consultancy N=3 vs critique-only; consultancy vs standard.
3. Cross-exam N=3 vs standard (only if the arm runs cleanly).
4. Standard debate with GPT-5.4 mini judge vs nano judge, same transcripts (re-judged; see results doc), and mini vs blind mini is not run.
Descriptive: quote verification rate per arm, verdict-A rate (position bias), accuracy by variant (correct answer defended at A vs B), invalid verdict rate, truncation rate (finish=length), cost per debate vs cost model.

## Outcome classification (decided now)
- Failed setup (results not interpretable), any of: critique-only or standard accuracy not above blind accuracy by at least 3 points AND judge verdict-A rate outside 35% to 65% (judge mostly picks a position); invalid verdict rate over 10% in any primary arm; more than 10% of instances errored; blind accuracy outside 55 to 90% (already passed).
- Positive (feasibility signal for Phase 1): the primary CI excludes 0 in either direction with |diff| >= 8 points, OR both primary arms exceed blind by a CI excluding 0 and the point difference is >= 5 points. Direction is reported as found: critique > debate or debate > critique.
- Null: primary CI includes 0 and the setup is valid. Reported as "no detectable difference at n=100 (MDE about 13 to 18 points)", not as equivalence.
- Recommendation rule: Phase 1 worth running if setup valid and (positive, or null with point difference in the plausible direction and cost per debate within 1.5x model). A null with a flat or reversed point estimate and no arm beating blind is a recommendation not to proceed with this judge and protocol as specified.

## Spend rules
Hard cap $30 on the harness ledger (ledger started at $0.2305 from earlier work; global cap set to $30.00 total, which is stricter than $30 for this task). Stop on any 402 or credit error. After Stage 1, if projected total > $30, stop.
