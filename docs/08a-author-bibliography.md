# Author bibliography: debate and scalable oversight, 2016-2026

Scope: works by Irving, Amodei, Christiano, Barnes, Kenton, Khan, Brown-Cohen, plus co-authored papers directly about debate, amplification, recursive reward modeling or scalable oversight protocols. Each entry was checked against its arXiv abs page, Alignment Forum page, Distill page, or proceedings page (title, authors, date). Venue is given only where a page stated it; otherwise "preprint". Nothing is marked unverified; the Type column marks blogs. Not found or not checked (omitted, not guessed): OpenAI's May 2018 debate blog (403), Christiano's own amplification blog posts, ARC's ELK report, Kirchner et al. prover-verifier games.

Each paper is listed once, under the group of its first matching author. Cross-listings are noted.

## Irving, Amodei, Christiano

| Year | Authors | Title | Type | Contribution | Link |
|---|---|---|---|---|---|
| 2016 | Amodei, Olah, Steinhardt, Christiano, Schulman, Mane | Concrete Problems in AI Safety | preprint, theory | Names "scalable supervision" as a core problem (peripheral to debate, background only) | https://arxiv.org/abs/1606.06565 |
| 2018 | Irving, Christiano, Amodei | AI safety via debate | preprint, theory | Proposes zero-sum debate judged by a human as a scalable oversight scheme | https://arxiv.org/abs/1805.00899 |
| 2018 | Christiano, Shlegeris, Amodei | Supervising strong learners by amplifying weak experts | preprint, theory | Iterated amplification: train on decomposed tasks to supervise beyond human ability | https://arxiv.org/abs/1810.08575 |
| 2019 | Irving, Askell | AI Safety Needs Social Scientists (Distill, 19 Feb 2019) | paper (essay) | Argues debate-style schemes need human-judgement experiments | https://distill.pub/2019/safety-needs-social-scientists/ |
| 2025 | Buhl, Pfau, Hilton, Irving | An alignment safety case sketch based on debate | preprint, theory | Sketches a safety case relying on debate; v3 23 May 2025 | https://arxiv.org/abs/2505.03989 |

## Barnes

| Year | Authors | Title | Type | Contribution | Link |
|---|---|---|---|---|---|
| 2020 | Barnes, Christiano | Writeup: Progress on AI Safety via Debate (AF, 5 Feb 2020) | blog | OpenAI Reflection-Humans 2019 work: structured recursion and cross-examination | https://www.alignmentforum.org/posts/Br4xDbYu4Frwrb64a/writeup-progress-on-ai-safety-via-debate-1 |
| 2020 | Barnes (with Christiano) | Debate update: Obfuscated arguments problem (AF, 23 Dec 2020) | blog | Dishonest debater can hide a fatal flaw in a long argument; also hits amplification | https://www.alignmentforum.org/posts/PJLABqQ962hZEqhdB/debate-update-obfuscated-arguments-problem |

## Kenton

| Year | Authors | Title | Type | Contribution | Link |
|---|---|---|---|---|---|
| 2024 | Kenton, Siegel, Kramar, Brown-Cohen, Albanie, Bulian, Agarwal, Lindner, Tang, Goodman, Shah | On scalable oversight with weak LLMs judging strong LLMs (NeurIPS 2024) | paper, empirical | Compares debate, consultancy, direct QA across task types; debate beats consultancy, mixed vs direct QA | https://arxiv.org/abs/2407.04622 |

## Khan

| Year | Authors | Title | Type | Contribution | Link |
|---|---|---|---|---|---|
| 2024 | Khan, Hughes, Valentine, Ruis, Sachan, Radhakrishnan, Grefenstette, Bowman, Rocktaschel, Perez | Debating with More Persuasive LLMs Leads to More Truthful Answers (ICML 2024, PMLR 235:23662-23733) | paper, empirical | Debate raises weak-judge accuracy (76% model, 88% human judges); persuasiveness optimisation helps | https://arxiv.org/abs/2402.06782 |

## Brown-Cohen

| Year | Authors | Title | Type | Contribution | Link |
|---|---|---|---|---|---|
| 2023 | Brown-Cohen, Irving, Piliouras | Scalable AI Safety via Doubly-Efficient Debate (ICML 2024, PMLR 235:4585-4602) | paper, theory | Complexity-theoretic debate with efficient honest debater and judge | https://arxiv.org/abs/2311.14125 |
| 2025 | Brown-Cohen, Irving | Prover-Estimator Debate: A New Scalable Oversight Protocol (AF, 17 Jun 2025) | blog | Informal account of protocol aimed at obfuscated arguments | https://www.alignmentforum.org/posts/8XHBaugB5S3r27MG9/prover-estimator-debate-a-new-scalable-oversight-protocol |
| 2025 | Brown-Cohen, Irving, Piliouras, Chen, Li, Xun | Avoiding Obfuscation with Prover-Estimator Debate | preprint, theory | Formal protocol; honest play at equilibrium under a stability assumption; v2 revised 21 Jul 2026 | https://arxiv.org/abs/2506.13609 |

## Co-authors (only where directly on debate, amplification, RRM or oversight protocols)

| Year | Authors | Title | Type | Contribution | Link |
|---|---|---|---|---|---|
| 2018 | Leike, Krueger, Everitt, Martic, Maini, Legg | Scalable agent alignment via reward modeling: a research direction | preprint, theory | Recursive reward modeling agenda | https://arxiv.org/abs/1811.07871 |
| 2021 | Wu, Ouyang, Ziegler, Stiennon, Lowe, Leike, Christiano | Recursively Summarizing Books with Human Feedback | preprint, empirical | Recursive task decomposition with human feedback as scalable oversight case study | https://arxiv.org/abs/2109.10862 |
| 2022 | Parrish, Trivedi, Perez, Chen, Nangia, Phang, Bowman | Single-Turn Debate Does Not Help Humans Answer Hard Reading-Comprehension Questions (ACL LNLS workshop 2022) | paper, empirical | Negative result for single-turn debate with humans | https://arxiv.org/abs/2204.05212 |
| 2022 | Saunders, Yeh, Wu, Bills, Ouyang, Ward, Leike | Self-critiquing models for assisting human evaluators | preprint, empirical | Model critiques help humans find flaws; assisted-evaluation oversight | https://arxiv.org/abs/2206.05802 |
| 2022 | Parrish, Trivedi, Nangia, Padmakumar, Phang, Saimbhi, Bowman | Two-Turn Debate Doesn't Help Humans Answer Hard Reading Comprehension Questions | preprint, empirical | Same negative result with two turns | https://arxiv.org/abs/2210.10860 |
| 2022 | Bowman et al. (46 authors) | Measuring Progress on Scalable Oversight for Large Language Models | preprint, empirical | Experimental design for studying oversight; human plus unreliable LLM beats either alone | https://arxiv.org/abs/2211.03540 |
| 2023 | Michael, Mahdi, Rein, Petty, Dirani, Padmakumar, Bowman | Debate Helps Supervise Unreliable Experts | preprint, empirical | Human debate with judges improves accuracy over consultancy | https://arxiv.org/abs/2311.08702 |
| 2024 | Arnesen, Rein, Michael | Training Language Models to Win Debates with Self-Play Improves Judge Accuracy | preprint, empirical | Self-play debate training raises judge accuracy | https://arxiv.org/abs/2409.16636 |

## Chronology: 10 most important works

1. 2018 Irving, Christiano, Amodei, AI safety via debate
2. 2018 Christiano, Shlegeris, Amodei, Supervising strong learners by amplifying weak experts
3. 2018 Leike et al., Scalable agent alignment via reward modeling
4. 2019 Irving and Askell, AI Safety Needs Social Scientists
5. 2020 Barnes and Christiano, Writeup: Progress on AI Safety via Debate
6. 2020 Barnes, Debate update: Obfuscated arguments problem
7. 2022 Bowman et al., Measuring Progress on Scalable Oversight
8. 2023 Brown-Cohen, Irving, Piliouras, Doubly-Efficient Debate
9. 2024 Khan et al., Debating with More Persuasive LLMs
10. 2025 Brown-Cohen et al., Avoiding Obfuscation with Prover-Estimator Debate

Also in 2024: Kenton et al. (weak LLM judges) and Michael et al. (Debate Helps Supervise Unreliable Experts).
