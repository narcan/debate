# Debate testbed: literature survey (checked 2026-11-12)

Method: each row was checked against an arXiv abstract page, a search snippet, or both. "unverified" means I could not confirm it. Papers you listed as already read (Irving 2018, Barnes 2020) were not re-checked.

## 1. Protocols and variants

| Paper | Protocol | Judge | Models | Task type | Metric | Headline result |
|---|---|---|---|---|---|---|
| Parrish+ 2022, arXiv 2204.05212 and 2210.10860 | Single-turn, then two-turn debate | Human | Human debaters (unverified) | Hard reading comprehension (QuALITY) | Judge accuracy | No accuracy gain from explanations; human-selected snippets did help |
| Michael+ 2023, arXiv 2311.08702 | Debate vs consultancy, hidden passage | Human, non-expert | Human debaters | Info asymmetry, QuALITY | Judge accuracy | About 84% debate vs 74% consultancy |
| Radhakrishnan 2023 (Anthropic update, AF post) | Simultaneous openings, one turn, RL-trained debaters and judge | Claude 2-based LLM, trained | Claude 2 fine-tunes | Hidden-passage QuALITY, 2 choice | Judge accuracy, Elo | Judge 73.1% to 77.7% over 50 RL steps; blind judge about 66-67%; honest debaters about 175-225 Elo above dishonest |
| Khan+ 2024, arXiv 2402.06782 | Sequential debate vs consultancy, best-of-N and critique-refine | LLM and human, non-expert | GPT-4-Turbo experts, best-of-16 (judge sizes unverified) | Info asymmetry, QuALITY | Judge accuracy, Elo | LLM judges 76% vs 48% naive; humans 88% vs 60%; consultancy falls as persuasiveness rises |
| Kenton+ 2024, arXiv 2407.04622 | Debate, consultancy, open debate, open consultancy, direct QA | Weak LLM | Gemini Pro 1.5 debaters; judge models unverified | Extractive QA plus math, code, logic, multimodal (mixed info and reasoning gaps) | Judge accuracy | Debate beats consultancy everywhere; beats direct QA only with info asymmetry; stronger debaters help modestly |
| Arnesen+ 2024, arXiv 2409.16636 | Debate self-play training (training method unverified) | LLM, not trained | Models unverified | Long-context reading | Judge accuracy | About +4 points absolute after debate training; no trend for consultancy |
| Brown-Cohen+ 2023, arXiv 2311.14125 | Doubly-efficient debate (theory) | Black-box human judgments | None | Complexity model | Proofs | Honest side needs polynomial simulation |
| Brown-Cohen+ 2025, arXiv 2506.13609 | Prover-estimator (theory) | Abstract | None | Complexity model | Proofs | Honest debater wins at cost comparable to opponent, under a stability assumption; no LLM experiments found |
| Engels+ 2025, arXiv 2504.18530 | Debate as one of 4 games, nested oversight | Elo-modelled | Models unverified | Debate plus Mafia, Backdoor Code, Wargames | Elo, NSO success rate | At 400 Elo gap, NSO success about 51.7% for debate |
| Elasky+ 2026, arXiv 2605.27483 | Proposer-critic debate vs consultancy | Weaker LLM | 5 pairings, names unverified | Verifiable code and logic | Judge accuracy | Beats consultancy in 3 of 5 pairings; 2 null; one independent critique recovers most of the gain |
| Kenton+ 2026, arXiv 2608.17776 | Generator-critic debate as RL reward | Frozen Gemini 2.5 Flash Lite | Policy Gemini 2.5 Flash-class | Verifiable math | Validation accuracy, reward hacking | Baseline RLAIF hacks the judge; debate recovers a "45% performance gap" |
| Jiang+ 2026, arXiv 2607.01251 | Collaborative disagreement resolution vs debate | Non-expert model | Unverified | Unverified | Judge accuracy | 62.1% vs 49.2% for standard debate |

Cross-examination: no empirical LLM paper found in this search (unverified whether one exists).

## 2. Other papers worth reading (max 15)

1. Kirchner+ 2024, Prover-Verifier Games improve legibility (OpenAI): https://arxiv.org/abs/2407.13692 (legibility tax found)
2. Kim and Lee 2026, Decoupled Prover-Verifier Games: https://arxiv.org/abs/2602.23248 (cuts legibility tax; I did not read results)
3. Buhl+ 2025, Alignment safety case sketch based on debate (UK AISI): https://arxiv.org/abs/2505.03989 (conceptual, no experiments)
4. Sudhir+ 2025, Benchmark for Scalable Oversight Protocols: https://arxiv.org/abs/2504.03731 (agent score difference metric; no results on page)
5. Engels+ 2025, Scaling Laws for Scalable Oversight: https://arxiv.org/abs/2504.18530
6. Elasky+ 2026, Debate Helps Weak Judges Reward Stronger Models: https://arxiv.org/abs/2605.27483
7. Kenton+ 2026, Debate Training Reduces Reward Hacking in RLAIF: https://arxiv.org/abs/2608.17776
8. Jiang+ 2026, Collaborative Disagreement Resolution (ICML 2026): https://arxiv.org/abs/2607.01251 (non-adversarial alternative)
9. Arnesen+ 2024, Training LMs to Win Debates with Self-Play: https://arxiv.org/abs/2409.16636
10. Michael+ 2023, Debate Helps Supervise Unreliable Experts: https://arxiv.org/abs/2311.08702
11. Parrish+ 2022, Single-Turn Debate Does Not Help Humans: https://arxiv.org/abs/2204.05212
12. Parrish+ 2022, Two-Turn Debate Doesn't Help Humans: https://arxiv.org/abs/2210.10860
13. Radhakrishnan 2023, Anthropic Fall 2023 Debate Progress Update: https://www.alignmentforum.org/posts/QtqysYdJRenWFeWc4/anthropic-fall-2023-debate-progress-update
14. Brown-Cohen+ 2024, Scalable AI Safety via Doubly-Efficient Debate (ICML 2024): https://arxiv.org/abs/2311.14125
15. Brown-Cohen+ 2025, Prover-Estimator Debate: https://arxiv.org/abs/2506.13609

Search limits: I found no 2025-2026 human-judge debate study and no 2025-2026 LLM obfuscated-argument experiments. Absence in my search is not proof that none exist.

## 3. Gaps (all inference from the table above)

- Inference: prover-estimator has no LLM implementation in anything I found. Obfuscation is untested empirically.
- Inference: recursive or doubly-efficient debate has no LLM experiments at all.
- Inference: cross-examination has no empirical LLM result in this set.
- Inference: reasoning-gap tasks have been tested with inference-only debate (Kenton 2024, Elasky 2026) and RL (2608.17776), but only on verifiable math, code and logic. Open-ended reasoning with no ground-truth checker is untested.
- Inference: human judges appear only in QuALITY-style info-asymmetry work (2022-2024). No human-judge study on reasoning-gap tasks, and none on current frontier debaters.
- Inference: judge-debater gap is rarely swept as a controlled variable. Engels 2025 models it as Elo; the others use a few fixed pairings.
- Inference: open consultancy and open debate (Kenton 2024) have not been combined with RL training of debaters against a weak judge.
- Inference: judge-side training (not just debater training) is only in the 2023 Anthropic update, with one-turn two-choice QuALITY.
- Inference: no paper in this set reports no-judge metrics for debate, such as transcript-level honesty measures or calibration. 2608.17776 and 2605.27483 measure reward hacking and verification rate, which are partial.
- Inference: self-preference effects (judge favors its own model family) were reported only in a secondary EA Forum replication.

## 4. Codebases and datasets

| Resource | What | License | Link |
|---|---|---|---|
| ucl-dark/llm_debate | Khan 2024 code: debate, consultancy, judge, Elo, async inference, web UI, human-trial transcripts | MIT (verified on repo page) | https://github.com/ucl-dark/llm_debate |
| samuelarnesen/nyu-debate-modeling | Arnesen 2024 training code | Unverified | https://github.com/samuelarnesen/nyu-debate-modeling |
| QuALITY (nyu-mll/quality) | Long-article multiple choice; standard info-asymmetry testbed | Repo page shows no license; per-article license field exists. Treat as unverified | https://github.com/nyu-mll/quality |
| GPQA (Rein+ 2023, arXiv 2311.12022) | Hard science MCQ; a reasoning-gap and expert-gap candidate | CC BY 4.0 per Hugging Face card; gated, do not post examples in plain text | https://huggingface.co/datasets/Idavidrein/gpqa |
| Kenton 2024 code | Not found in this search | Unverified | n/a |
| TruthfulQA | Not checked | Unverified | n/a |
| Sudhir 2025 benchmark | Says a Python package exists; no link on abstract page | Unverified | https://arxiv.org/abs/2504.03731 |
