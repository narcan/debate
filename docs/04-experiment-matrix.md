# 04 Experiment Matrix and Phased Plan (2026-11-12)

Revised 2026-11-12: sections 4 and 6 now assume no batch discount and add protocol knobs (section 6). Cell costs in section 3 are `--batch` figures, kept for the optional final-run saving only.
Sources: `01-literature-survey.md` (cited as S1 row names or section numbers), `02-cost-model.md`, `tools/cost_calc.py`.
Warning: all prices are unverified aggregator numbers (02 sec 1). Every dollar figure below is "raw" (calculator output). "x1.5" = raw times the 1.5 safety margin. Budget decisions use x1.5 only.
Items labeled "inference" are my reading, not a checked fact.

## 1. Matrix axes and levels

| Axis | Levels | Notes |
|---|---|---|
| Protocol | standard (sequential), simultaneous, consultancy, open consultancy, open debate, cross-examination, critique-only baseline (one answer + one critique, then judge), proposer-critic, collaborative disagreement resolution (S1 Jiang 2026), prover-estimator, recursive / doubly-efficient | Only the first 4 schedules exist in cost_calc. Others are costed as approximations (marked). |
| Model gap | Judge tier vs debater tier. Judges: GPT-5.4 nano (weakest), GPT-5.4 mini, Haiku 4.5. Debaters: Haiku 4.5, Sonnet 4.6 | Gap proxy = price tier (inference). Measure the real gap with blind-judge accuracy (judge sees question only, no transcript). Use a different provider for the judge to avoid self-preference (S1 sec 3, last bullet). |
| Gap type | Information asymmetry (debaters see passage, judge does not) vs capability / reasoning (same inputs, debaters stronger) | S1 sec 3: reasoning gaps only tested on verifiable math, code, logic. |
| Metric | (a) judge accuracy with side swap and answer-order shuffle; (b) calibration (Brier, ECE) if the judge emits a probability (unverified that llm_debate exposes it); (c) critique-only comparison (debate minus critique-only accuracy); (d) no-judge: planted-flaw detection rate, quote-verification rate (fabricated quotes per transcript), honest-side win rate / Elo; (e) other gold: GPQA expert labels, planted-flaw ground truth, code tests, llm_debate human-trial transcripts | S1 sec 3: no paper reports (b) or (d) for debate. |
| Task / dataset | QuALITY hard subset (info asymmetry; license unverified, S1 sec 4); GPQA Diamond 198 q (reasoning; gated, CC BY 4.0 per HF card, never paste examples in plain text); planted-flaw reasoning chains (self-built, gold by construction); optional verifiable math/code | TruthfulQA unchecked, dropped. |

## 2. Coverage: protocol x gap type

Legend: Covered = empirical LLM or human result exists in S1. Partial = tested only in a narrow setting. Open = no result found (absence in my search is not proof, S1 sec 2 note).

| Protocol | Information asymmetry | Capability / reasoning |
|---|---|---|
| Standard / sequential debate | Covered (S1: Michael+ 2023, Khan+ 2024, Parrish+ 2022) | Partial (S1: Kenton+ 2024 mixed tasks, Elasky+ 2026, Kenton+ 2026; verifiable tasks only) |
| Simultaneous debate | Partial (S1: Radhakrishnan 2023, one turn, RL-trained, 2 choice) | Open (inference; not listed in S1 Kenton row) |
| Consultancy | Covered (S1: Michael+, Khan+, Kenton+ 2024) | Covered for verifiable tasks (S1: Kenton+ 2024, Elasky+ 2026) |
| Open consultancy | Partial (S1: Kenton+ 2024 mixed tasks) | Partial (S1: Kenton+ 2024) |
| Open debate | Partial (S1: Kenton+ 2024) | Partial (S1: Kenton+ 2024) |
| Cross-examination | Open (S1 sec 1 note, sec 3) | Open (S1 sec 3) |
| Critique-only baseline | Open (inference) | Partial (S1: Elasky+ 2026, "one independent critique recovers most of the gain", code and logic) |
| Proposer-critic debate | Open (inference) | Partial (S1: Elasky+ 2026; Kenton+ 2026 as RL reward) |
| Collaborative disagreement resolution | Partial (S1: Jiang+ 2026, task unverified) | Partial (S1: Jiang+ 2026, task unverified) |
| Prover-estimator | Open (S1: Brown-Cohen+ 2025 is theory only; sec 3 bullet 1) | Open (same) |
| Recursive / doubly-efficient | Open (S1: Brown-Cohen+ 2023 theory only; sec 3 bullet 2) | Open (same) |
| Debate-trained debaters (self-play / RL) | Partial (S1: Arnesen+ 2024 long-context, Radhakrishnan 2023) | Partial (S1: Kenton+ 2026) |

Open metric cells (all inference, S1 sec 3): calibration and no-judge honesty metrics for any protocol; human judges on reasoning gaps; open-ended reasoning with no checker.

## 3. Top 5 open cells, ranked

Score = value (1-5, my judgement, inference) / (hours/10 + x1.5 cost/10). Cost counts only arms this cell adds; shared comparator arms (standard on QuALITY) are charged once, to cell 1.
Common setup: N=3 rounds, T=300, J=300, side-swap repeats=2, `--batch --cache`. P=6000 for QuALITY (my estimate of article + question + rules, inference; real P may be 2x, which raises cost about 1.6x, see section 5). P=800 for GPQA. Debater provider Anthropic, judge OpenAI.

| Rank | Cell | Value | Raw $ | x1.5 $ | Hours | Score |
|---|---|---|---|---|---|---|
| 1 | Critique-only vs debate x info asymmetry | 5 | 10.4 | 15.6 | 10 | 1.95 |
| 2 | Simultaneous vs sequential x reasoning gap | 2.5 | 4.8 | 7.2 | 8 | 1.64 |
| 3 | Cross-examination x info asymmetry | 4 | 8.1 | 12.1 | 14 | 1.53 |
| 4 | No-judge flaw detection x reasoning gap | 4 | 4.4 | 6.6 | 20 | 1.50 |
| 5 | Prover-estimator toy x reasoning gap | 5 | 6.2 | 9.3 | 40 | 1.01 |

### Cell 1: critique-only baseline vs debate, information asymmetry
- Hypothesis: with a weak judge, standard debate beats a single answer + one critique by under 5 points, i.e. most debate gain is critique (extends S1 Elasky+ 2026 to hidden-passage QuALITY).
- Design: (1) Same questions, same models, judge sees transcript only. (2) Arms: critique-only (one answer, one critique, verdict) vs standard N=3 vs consultancy N=3. (3) Side swap, answer-order shuffle, paired bootstrap on per-question differences.
- Dataset: QuALITY hard subset, 300 q. Models: Haiku 4.5 debaters, GPT-5.4 nano judge. Debates: 300 x 2 = 600 per arm, 1,200 for the two new arms (standard + critique-only), consultancy reuses cell 3 budget.
- Cost (raw 10.4, x1.5 15.6):
```
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol standard --rounds 3 --questions 300 --cells 1 --repeats 2 --prompt-tokens 6000 --batch --cache   # 6.57
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol standard --rounds 1 --questions 300 --cells 1 --repeats 2 --prompt-tokens 6000 --batch --cache   # 3.85, critique-only = standard N=1 (inference)
```
- Hours: 10 (critique-only is a prompt variant on llm_debate).

### Cell 2: simultaneous vs sequential, reasoning gap
- Hypothesis: simultaneous and sequential debate give judge accuracy within 3 points on GPQA; sequential only helps when the last speaker can rebut.
- Design: (1) Debaters get question + choices, judge gets the same, no hidden text. (2) Arms: simultaneous N=3 vs standard N=3, optional critique-only. (3) Judge-sweep by judge tier.
- Dataset: GPQA Diamond, 198 q (gated; keep transcripts private, no plaintext examples in public docs). Models: Haiku debaters, nano judge. Debates: 198 x 2 = 396 per arm, 792 total.
- Cost (raw 4.77, x1.5 7.2):
```
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol simultaneous --rounds 3 --questions 198 --cells 1 --repeats 2 --prompt-tokens 800 --batch --cache   # 2.44
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol standard --rounds 3 --questions 198 --cells 1 --repeats 2 --prompt-tokens 800 --batch --cache   # 2.33
```
- Hours: 8 (llm_debate has simultaneous; need a GPQA loader). Same commands with `--debater anthropic-sonnet` give 6.98 and 6.62 (raw) for a strong-debater check; run on half the questions.

### Cell 3: cross-examination, information asymmetry
- Hypothesis: cross-exam raises weak-judge accuracy over standard debate by at least 5 points, because it exposes fabricated quotes.
- Design: (1) Standard N=3 plus a 4-turn block (each side asks one short question and answers one) after round 1, per the cost_calc schedule. (2) Compare to standard and critique-only on the same questions. (3) Also log quote-verification rate.
- Dataset: QuALITY hard, 300 q. Models: Haiku debaters, nano judge. Debates: 600 (standard comparator comes from cell 1).
- Cost (raw 8.05, x1.5 12.1):
```
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol cross-exam --rounds 3 --questions 300 --cells 1 --repeats 2 --prompt-tokens 6000 --batch --cache
```
- Hours: 14 (new turn logic in llm_debate, plus prompts and parsing).

### Cell 4: no-judge flaw detection, reasoning gap
- Hypothesis: a debater or critic finds a planted flaw in a reasoning chain more often under debate than under critique-only, and flaw-detection rate tracks judge accuracy.
- Design: (1) Strong model writes 200 short reasoning chains, half with one planted step error (gold by construction). (2) Debaters argue "has a flaw" vs "sound"; measure flaw-detection rate and false-alarm rate without any judge, then add judge verdict. (3) Arms: debate N=2 vs critique-only.
- Dataset: self-built, 200 chains (generation about 1.5 raw extra, inference). Models: Haiku debaters, nano judge. Debates: 400 per arm.
- Cost (raw 2.86 + 1.5 generation = 4.4, x1.5 6.6):
```
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol standard --rounds 2 --questions 200 --cells 1 --repeats 2 --prompt-tokens 1200 --batch --cache   # 1.78
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --protocol standard --rounds 1 --questions 200 --cells 1 --repeats 2 --prompt-tokens 1200 --batch --cache   # 1.08
```
- Hours: 20 (dataset construction and validation dominate).

### Cell 5: prover-estimator toy, reasoning gap
- Hypothesis: a prover-estimator loop on 4-step decomposable problems (exact arithmetic or logic chains) locates the wrong step more reliably than standard debate at similar cost.
- Design: (1) Prover decomposes a claim into subclaims; estimator gives probabilities for each; recurse on the subclaim with most disagreement. (2) Gold = verifiable answer. (3) Compare with standard debate N=4.
- Dataset: 150 synthetic decomposable problems. Models: Haiku (Sonnet prover optional). Debates: 300 per arm.
- Cost: modeled as standard N=4 with a 2x factor for estimator calls (both inference, protocol not in cost_calc). Raw 3.08 x 2 = 6.2, x1.5 9.3:
```
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge anthropic-haiku --protocol standard --rounds 4 --questions 150 --cells 1 --repeats 2 --prompt-tokens 1000 --batch --cache   # 3.08
```
- Hours: 40 (no reference implementation; theory is S1 Brown-Cohen+ 2025). Highest novelty, lowest ratio. Do last, cut first.

## 4. Phases (revised 2026-11-12: protocol knobs added, no batch)

Budget basis: NO batch discount (OpenRouter batch unverified); prompt cache ON (also unverified on OpenRouter, so Phase 0 step 1 measures it). All $ below are raw calculator output; x1.5 is the budget figure. The `--batch` costs in section 3 cells are now "optional final-run saving" figures only (see 6.5). Primary question is unchanged: critique-only vs debate (cell 1). Knobs (section 6) are secondary arms.
Judge: GPT-5.4 nano first. Floor check before any debate: blind-judge accuracy on 50 QuALITY q and 60 GPQA q; if under 55% on a binary task, switch to mini.

### Phase 0 pilot (cost and hours)

| Item | Basis | Raw $ | Hours |
|---|---|---|---|
| Primary: QuALITY standard N=3, 100 q x 2 sides | `--protocol standard --rounds 3 --questions 100 --prompt-tokens 6000 --cache` | 4.38 | 6 (clone llm_debate, OpenAI judge, scoring) |
| Primary: QuALITY critique-only (N=1), 100 q | `--rounds 1` | 2.56 | 3 |
| Blind-judge floor checks (QuALITY 200 x 6k in, GPQA) | hand calc, no batch | 0.27 | 1 |
| Knob screen, GPQA, 8 runs 2^(4-1), 60 q x 2 sides | section 6.3 | 14.33 | 16 (judge-interaction turns 3, position choice 2, concede prompts 2, GPQA loader 3, runner and analysis 6) |
| Knob screen centre run (N=3, all baseline) | `--rounds 3 --questions 60 --prompt-tokens 800` | 1.41 | in above |
| Knob screen critique-only on GPQA (N=1) | `--rounds 1` | 0.57 | in above |
| Dev and debugging (QuALITY 20 q standard + critique-only 1.4, GPQA 20 q all protocols 1.84) | no batch | 3.24 | 8 |
| Analysis, bootstrap, write-up | | | 9 |
| **Phase 0 raw** | | **26.76** | **43** |
| **Phase 0 x1.5** | | **40.1** | |

Dropped from the old Phase 0: consultancy (moved to Phase 1), cross-exam (moved out, see 4.3), the two judge-sweep arms (mini judge moved to Phase 1; Haiku judge dropped, self-preference risk, S1 sec 3 last bullet).
Power: QuALITY arms at n=100 q detect only about 13 to 18 point differences; the knob screen at 60 q detects roughly 8 to 12 point main effects because each contrast pools 4 runs vs 4 (both inference). Phase 0 is feasibility and screening.
Gate before spending the screen: run 10 debates and read cache-hit tokens. If caching does not work (list price, about 1.6x), halve scale: QuALITY 50 q, screen 40 q (about 23 raw, 34 x1.5).

### Phase 1 (cost and hours)

| Item | Basis | Raw $ | Hours |
|---|---|---|---|
| Primary scale-up: QuALITY standard to 300 q (13.13 minus 4.38 done) | `--questions 300 --cache` | 8.75 | 5 |
| Primary scale-up: critique-only to 300 q (7.69 minus 2.56 done) | `--rounds 1 --questions 300` | 5.13 | in above |
| Consultancy N=3, QuALITY 100 q (harness sanity check vs S1 Khan+ 2024, Michael+ 2023) | `--protocol consultancy` | 3.22 | 2 |
| Judge sweep: standard N=3, mini judge, 100 q | `--judge openai-mid` | 5.43 | 2 |
| GPQA block, 100 fresh q x 2: baseline | `--prompt-tokens 800` | 2.35 | 8 (scratchpad and told-weak prompts, confirmation runner) |
| GPQA block: confirm top 2 screen knobs (about 1.3x baseline each, inference) | 2 x 3.1 | 6.2 | |
| GPQA block: scratchpad on (about 1.4x, inference) | | 3.29 | |
| GPQA block: told-judge-is-weak (1.0x) | | 2.35 | |
| Quote-verification rate logging in every arm | free metric | 0 | 3 |
| Analysis, write-up | | | 12 |
| **Phase 1 raw** | | **36.72** | **32** |
| **Phase 1 x1.5** | | **55.1** | |

### Cap check

| | Raw $ | x1.5 $ | Hours |
|---|---|---|---|
| Phase 0 | 26.76 | 40.1 | 43 |
| Phase 1 | 36.72 | 55.1 | 32 |
| **Total** | **63.48** | **95.2** | **75** |

Fits the $100 cap with only $4.8 contingency, and the 85 hour budget with 10 hours spare. The old plan (83.9 x1.5) assumed batch; without batch it no longer fits, so these were cut or deferred (cut order, first to last):
1. Prover-estimator toy (cell 5, 6.2 batch raw, about 12 no batch, 40 h). Cut.
2. Flaw-detection dataset (cell 4, 4.4 batch raw, 20 h). Cut.
3. GPQA Sonnet-debater check (6.8 batch raw). Cut; covered partly by S1 Kenton+ 2024 "stronger debaters help modestly".
4. Cross-exam at 300 q (16.09 raw cached, no batch). Deferred; run only if Phase 1 ends under 70% of budget, at 100 q (5.36 raw).
5. Simultaneous vs sequential (cell 2). Cut as a separate cell; value score was lowest (2.5).
6. Haiku judge arm and the 3-tier judge-gap trend. Reduced to 2 tiers (nano, mini).
Order inside Phase 1: primary scale-up, consultancy and judge sweep, GPQA knob block. If spend reaches 70% of the x1.5 budget (66.6), stop and write up.
Stretch, NOT funded: no-quote-requirement arm on QuALITY (4.38 raw, 6.6 x1.5) breaks the cap.

### Results that would count as a finding
Any one of these, with 300 q x 2 sides, a paired bootstrap 95% CI excluding zero, and a harness sanity check (debate beats consultancy on QuALITY in the direction S1 Khan+ 2024 and Michael+ 2023 report):
- Debate minus critique-only judge accuracy of at least 7 points (the 300 q design can detect roughly 7 to 10 points, inference). Supports human-judge and trained-debater follow-ups.
- A tight null: debate within 2 points of critique-only across 3 judge tiers. A well-powered null against S1 Elasky+ 2026 is itself a useful result and cheap to defend.
- Cross-exam or flaw-detection effect of at least 5 points with the quote-verification rate moving in the same direction.
- A monotone judge-gap trend across nano and mini only (Haiku judge dropped for budget; two tiers give a direction, not a trend; S1 sec 3 "gap rarely swept").
Treat the result as invalid if blind-judge accuracy is at floor or ceiling, or if the pilot only reproduces the cost model.

## 5. Risks that waste money

| Risk | Effect | Mitigation |
|---|---|---|
| Judge variance (sampling, prompt wording) | Differences under 10 points are noise at n=100 to 300 | Temperature 0, 2 repeats, paired bootstrap, fix prompts after dev run |
| Position and side bias | Fake accuracy gains | Side swap and answer-order shuffle in every arm, report per-side accuracy |
| Floor or ceiling judge | Zero signal at full cost | Blind-judge check on 50 q before any debate (cost under $0.10) |
| Self-preference | Haiku judge scoring Haiku debaters inflates results | Use nano and mini (different provider) as primary judges; Haiku judge only as labeled comparison |
| Passage tokens underestimated | P=6000 is my guess; at P=12000 the Phase 0 QuALITY arms rise about 1.6x (3.12 at 6k to roughly 5 at 12k for standard, from the sanity runs), total x1.5 could pass $30 | Measure real P on 20 q first; truncate passages or cut to 60 q |
| Batch unavailable or latency | Debate rounds are sequential, so batching needs one batch per round (about 3 to 7 batch waits, each up to 24 h per provider terms, unverified). Without batch, cache-only costs about 2x: Phase 0 four protocol arms go from 7.8 to 15.5 raw | Test on 10 debates before the full run; if no batch, cut to 50 q or drop the cross-exam arm |
| Cache savings not realized | Savings model assumes stable prefixes and cache hits; Anthropic cache TTL and batch interplay unverified. List price without cache or batch: standard 10.29, cross-exam 16.42 per 200 debates | Log cache-hit tokens per run; abort if hit rate is far under model |
| Hidden reasoning tokens | GPT-5.x nano and mini may bill reasoning tokens as output; cost_calc does not model this (unverified) | Set minimal reasoning effort, log usage fields on first 20 calls |
| API price drift | All prices unverified; GPT-5.6 promo ends about 2026-11-21; Together 70B reported rising to 1.04; aggregator conflicts for Gemini | Re-check official pages before spending; edit `tools/prices.json`; the x1.5 margin is the buffer |
| Retries and parse failures | Silent doubling of spend | Hard per-run budget guard in the harness; billing caps on each provider console |
| Model deprecation mid-run | Arms not comparable | Pin model IDs, run all arms of a comparison in the same week |
| Dataset license and gating | QuALITY license unverified; GPQA gated | Keep data and transcripts private, do not publish examples; check QuALITY per-article license before any release |
| Underpowered pilot | Wrong go/no-go | Treat Phase 0 as feasibility only (section 4 power note) |
| Prompt iteration spend | Dev reruns eat budget | Dev budget fixed at $3.24 raw in Phase 0 (section 4); freeze prompts after |

Reuse note: llm_debate (MIT, S1 sec 4) already supplies debate, consultancy, judge, Elo, async inference. Its OpenAI and Anthropic backend support and judge probability output were not checked here (unverified); confirm in the repo before relying on cells 1 to 3.

## 6. Protocol knobs (secondary arms; added 2026-11-12)

Primary question stays critique-only vs debate (cell 1, section 4). Knobs test whether the answer depends on protocol details. "S1" rows are from `01-literature-survey.md`. Labels: Covered / Partial / Open are my reading (inference) unless a row is cited; "unverified" means the survey is silent and one quick web check (Khan+ 2024 setup details, 2026-11-12) did not settle it.

### 6.1 Baseline B

Sequential standard debate, N=3 rounds, T=300 tokens per turn, assigned positions, passive judge, forced choice (judge probability always logged), judge sees full transcript, same model (Haiku 4.5) for both debaters, no scratchpad, side swap and answer-order shuffle on, verified-quote tool on for QuALITY. Judge GPT-5.4 nano.

### 6.2 Knob table

Cost multiplier is vs B at the cache-on, no-batch price, from `cost_calc.py` where marked "calc", else hand estimate marked "est" (inference).

| Knob | Levels | Hypothesis | Literature | Cost x |
|---|---|---|---|---|
| A. Judge interaction | passive vs judge asks each side a question between rounds | Questions expose weak arguments, raising weak-judge accuracy | Partial: consultancy with judge questions is in S1 (Michael+ 2023, Khan+ 2024, Kenton+ 2024); interactive judge in LLM debate not in S1 (inference) | 1.3 est |
| B. Position choice | assigned vs each debater picks its own answer first | Self-chosen sides make the honest side more sincere; if both pick the same answer the debate degenerates | Partial: "open debate" in S1 Kenton+ 2024 (that it means self-chosen sides is inference) | 1.2 est (2 extra calls reading P) |
| C. Concede or switch | not allowed vs may concede or switch sides mid-debate | Concession is a cheap honesty signal and shortens debates | Open (S1 silent, unverified) | 1.0 est (prompt only) |
| D. Rounds | 1 (= critique-only), 2, 3, 4, 5 | Accuracy gain over critique-only grows with rounds, then saturates | Partial: single vs two-turn only for humans (S1 Parrish+ 2022); LLM sweep not in S1 | 1 round 0.58, 2 rounds 0.79, 4 rounds about 1.3, 5 rounds 1.44 calc (QuALITY); GPQA 0.40, 0.70, 1.31 calc |
| E. Simultaneous vs sequential | sequential vs simultaneous | Sequential last speaker gets a rebuttal edge | Partial: S1 Radhakrishnan 2023 simultaneous; S1 matrix sec 2 says open on reasoning gap | 1.03 calc |
| F. Who speaks first | honest first vs dishonest first | First-speaker advantage | Open (S1 silent, unverified) | 1.0; already balanced by side swap, analyse as a free covariate |
| G. Turn length | T=150, 300, 600 tokens | Short turns cut padding; long turns help the persuasive side | Open (S1 silent, unverified) | 0.78, 1.0, 1.45 calc |
| H. Verified quotes | quotes required with budget vs unrestricted | Verified quotes cut fabricated evidence (needs passage, QuALITY only) | Partial: S1 Parrish+ 2022 "human-selected snippets did help"; quote ablation for LLM judges unverified | 1.0 est |
| I. Debater sees judge weakness | not told vs told judge is weak vs given its blind-accuracy | Telling debaters the judge is weak invites simpler, less truthful persuasion | Open (S1 silent, unverified) | 1.0 est |
| J. Judge output | forced choice vs probability | Calibration is usable without extra cost | Open: S1 sec 3 bullet 9 (no calibration metric reported) | 1.0; always elicit and log, do not make it an arm |
| K. Judge sees prior rounds | full transcript vs last round only | Cheaper judge; tests whether argument history matters | Open (S1 silent, unverified; low interest) | about 0.95 est |
| L. Best-of-N or critique-refine | none vs N=4 sampling with selection vs one refine pass | More persuasive debaters, as in S1 Khan+ 2024 | Covered: S1 Khan+ 2024 | N=4 about 4.5 est; refine about 2 est |
| M. Debater model gap | Haiku vs Haiku, Haiku vs Sonnet, Sonnet vs Sonnet | Stronger debaters help modestly | Partial: S1 Kenton+ 2024, Khan+ 2024 Elo, Elasky+ 2026 pairings | mixed 1.9 calc, both Sonnet 2.8 calc |
| N. Answer-order randomization | on vs off | Controls position bias | Hygiene; section 1 metric (a) already requires it | 1.0; always on, never an arm |
| O. Hidden scratchpad | none vs private reasoning before each turn | Planning improves argument quality | Open (S1 silent, unverified) | 1.4 est; also check reasoning-token billing (section 5) |

### 6.3 Design: fractional factorial screen, then one-factor-at-a-time confirmation

Phase 0 screen: 2^(4-1) fractional factorial, resolution IV, generator D = ABC, 8 runs plus a centre run (all baseline, N=3) plus critique-only. Main effects are clear of two-factor interactions; two-factor interactions are aliased in pairs (AB=CD, AC=BD, AD=BC), which is acceptable for a screen. Runs on GPQA Diamond (P=800), 60 q x 2 sides = 120 debates per run, Haiku vs Haiku, nano judge. GPQA, not QuALITY, because QuALITY at P=6000 costs about 1.9x more per debate (4.38 vs 2.35 raw per 100 q), and none of A to D needs a passage. Rounds D: "-" is 2, "+" is 4.

| Run | A judge interacts | B self-chosen sides | C concede/switch | D rounds (=ABC) | Cost basis | Raw $ |
|---|---|---|---|---|---|---|
| 1 | - | - | - | 2 | 0.98 | 0.98 |
| 2 | + | - | - | 4 | 1.85 x 1.3 | 2.41 |
| 3 | - | + | - | 4 | 1.85 x 1.2 | 2.22 |
| 4 | + | + | - | 2 | 0.98 x 1.3 x 1.2 | 1.53 |
| 5 | - | - | + | 4 | 1.85 | 1.85 |
| 6 | + | - | + | 2 | 0.98 x 1.3 | 1.27 |
| 7 | - | + | + | 2 | 0.98 x 1.2 | 1.18 |
| 8 | + | + | + | 4 | 1.85 x 1.3 x 1.2 | 2.89 |
| Centre | baseline, N=3 | | | 3 | 1.41 | 1.41 |
| Critique-only | N=1 | | | 1 | 0.57 | 0.57 |
| **Total** | 1,200 debates | | | | | **16.31** |

Commands (no batch, cache on; the 1.3 and 1.2 factors are hand estimates, not calculator output):
```
C="python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --cells 1 --repeats 2 --questions 60 --prompt-tokens 800 --cache"
$C --protocol standard --rounds 1   # 0.57
$C --protocol standard --rounds 2   # 0.98
$C --protocol standard --rounds 3   # 1.41
$C --protocol standard --rounds 4   # 1.85
```
Reading the screen: a knob "moves" if its main effect is at least 8 points of judge accuracy with the same sign in both halves of the runs (inference, 60 q). Nothing here is confirmatory.

Phase 1 follow-up is one-factor-at-a-time around B on fresh questions (GPQA, 100 q x 2 sides): baseline 2.35, top 2 screen knobs about 3.1 each (est), scratchpad 3.29, told-weak 2.35. OFAT because confirmation tests only the winners, and a new factorial would cost more.
```
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --cells 1 --repeats 2 --questions 100 --prompt-tokens 800 --protocol standard --rounds 3 --cache   # 2.35
python3 tools/cost_calc.py cost --debater anthropic-haiku --judge openai-small --cells 1 --repeats 2 --questions 100 --prompt-tokens 6000 --protocol standard --rounds 3 --cache  # 4.38 (QuALITY reference)
```
If the researcher wants a QuALITY knob screen (info asymmetry), the same 8-run design at 60 q, P=6000 would cost about 1.9x the GPQA figures (about 30 raw, 46 x1.5), which does not fit alongside the primary arms.

### 6.4 Recommendation

| Where | Knobs | Why |
|---|---|---|
| Phase 0 screen (4) | A judge interaction, B position choice, C concede/switch, D rounds | The researcher's three, plus rounds because it is the dose-response of the primary question (1 round = critique-only). All prompt or schedule changes, cheap on GPQA. |
| Phase 1 (2 to 4) | The top 2 of A to D by screen effect (confirm), O scratchpad, I told-judge-weak | Both are prompt-only, GPQA-cheap, and open in S1. |
| Always logged, not arms | J judge probability, F first speaker, N answer-order shuffle, quote-verification rate | Zero marginal cost; gives calibration and fabricated-quote metrics that S1 sec 3 says nobody reports. |
| Not worth the money | L best-of-N and critique-refine (covered by S1 Khan+ 2024, 2 to 4.5x cost), M model gap (covered by S1 Kenton+ 2024, 2 to 2.8x), E simultaneous (low value, 1.03x but needs its own arm), G turn length (inference: effect confounded with padding), K judge sees prior rounds (low interest), H quote budget on QuALITY (4.38 raw per arm, breaks the cap; revisit only with batch or a larger budget) | |

### 6.5 Batch as optional final-run saving

Batch is not assumed anywhere in sections 4 and 6. If a provider with real batch is verified before a large final run, the saving at the section 3 settings is about 2x on the batched arms (cell 1: 15.6 x1.5 with batch vs about 31 x1.5 without, from 10.4 raw batch vs 13.13 + 7.69 = 20.8 raw cached no-batch for standard + critique-only at 300 q x 2). Do not plan around it.
