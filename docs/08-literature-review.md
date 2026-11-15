# Literature review: debate as scalable oversight, 2016-2026

Compiled 2026-11-15. Part A covers works by Irving, Amodei, Christiano, Barnes, Kenton, Khan and Brown-Cohen plus close co-authors. Part B covers related work (59 entries). Part C adds items from the earlier survey (01) that Part A missed. Every entry has a link. Links were spot-checked by the orchestrator; titles for arXiv items were checked by the compiling agents against arXiv. Items marked unverified are flagged.

## Part C: additions to Part A

| Year | Authors | Title | Type | Link |
|---|---|---|---|---|
| 2023 | Radhakrishnan (Anthropic) | Anthropic Fall 2023 Debate Progress Update | blog | https://www.alignmentforum.org/posts/QtqysYdJRenWFeWc4/anthropic-fall-2023-debate-progress-update |
| 2026 | Kenton et al. | Debate Training Reduces Reward Hacking in RLAIF | preprint, empirical | https://arxiv.org/abs/2608.17776 |
| 2018 | OpenAI | Debate (blog, original announcement). Not fetched by any agent (403), unverified | blog | https://openai.com/index/debate/ |
| 2018 | Christiano | Iterated amplification (blog series). Not fetched, unverified | blog | https://ai-alignment.com/iterated-amplification-ia-and-debate-6df05cd4aa5f |

# Part A: authors

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

# Part B: related works

Scope: works related to debate as scalable oversight, excluding the core debate papers by Irving, Amodei, Christiano, Barnes, Kenton, Khan and Brown-Cohen (covered separately; the Kenton 2026 debate-training paper and the Buhl et al. safety case sketch, which has Irving as a co-author, are noted below). Year is first public posting.

Verification: arXiv entries were checked against the arXiv API (title, authors, first-posted year) and the abs links resolve. Author lists are truncated with et al. LessWrong and Alignment Forum entries were checked only for title and URL resolving unless noted. Items marked unverified have a field that could not be confirmed.

Centrality tags: core = directly about debate; adjacent = neighbouring protocol, bias or benchmark used with debate; background = general context.

Excluded to avoid overlap: Kenton et al. 2024 (arXiv 2407.04622) and Kenton et al. 2026 (arXiv 2608.17776, Debate Training Reduces Reward Hacking in RLAIF). Buhl et al. is included because the brief asked for AISI safety case sketches.


## 1. Other debate empirical work

| Year | Authors | Title | Venue | Relevance to debate | Centrality | Link |
|---|---|---|---|---|---|---|
| 2022 | Parrish, Trivedi, Perez, et al. | Single-Turn Debate Does Not Help Humans Answer Hard Reading-Comprehension Questions | arXiv (workshop) | Early human study on QuALITY-style questions; null result for single-turn debate | core | https://arxiv.org/abs/2204.05212 |
| 2022 | Parrish, Trivedi, Nangia, et al. | Two-Turn Debate Doesn't Help Humans Answer Hard Reading Comprehension Questions | arXiv | Follow-up with two turns; still no gain over baseline | core | https://arxiv.org/abs/2210.10860 |
| 2023 | Michael, Mahdi, Rein, et al. | Debate Helps Supervise Unreliable Experts | arXiv | Human judges with live debate beat consultancy on QuALITY with unreliable experts | core | https://arxiv.org/abs/2311.08702 |
| 2024 | Arnesen, Rein, Michael | Training Language Models to Win Debates with Self-Play Improves Judge Accuracy | arXiv | Self-play debate training with a judge-in-the-loop raises judge accuracy | core | https://arxiv.org/abs/2409.16636 |
| 2025 | Lang, Huang, Li | Debate Helps Weak-to-Strong Generalization | arXiv | Uses debate-derived signals to improve weak supervisors for strong models | core | https://arxiv.org/abs/2501.13124 |
| 2025 | Rahman, Issaka, Suvarna, et al. | AI Debate Aids Assessment of Controversial Claims | arXiv | Debate helps judges on contested claims, including partisan judges | core | https://arxiv.org/abs/2506.02175 |
| 2025 | Reedi, Leger, Pourcel, et al. | Optimizing for Persuasion Improves LLM Generalization: Evidence from Quality-Diversity Evolution of Debate Strategies | arXiv | Evolves debate strategies; persuasion optimization versus truth tracking | adjacent | https://arxiv.org/abs/2510.05909 |
| 2025 | Carro, Mester, Nieto, et al. | AI Debaters are More Persuasive when Arguing in Alignment with Their Own Beliefs | arXiv | Debater belief alignment affects persuasiveness, a confound for debate judging | core | https://arxiv.org/abs/2510.13912 |
| 2026 | Elasky, Nakasako, Goyal, et al. | Debate Helps Weak Judges Reward Stronger Models | arXiv | Debate as a reward signal from weak judges for training stronger models | core | https://arxiv.org/abs/2605.27483 |
| 2026 | Carro, Mester, Nieto, et al. | Humans Correct Their Judgments Through Debate, but Weaker AI Models Do Not | arXiv | Compares human and weak-AI judge updating after debate | core | https://arxiv.org/abs/2610.28539 |
| 2023 | Du, Li, Torralba, Tenenbaum, Mordatch | Improving Factuality and Reasoning in Language Models through Multiagent Debate | arXiv (ICML 2024) | Multi-agent debate for accuracy, not oversight; often conflated with oversight debate | background | https://arxiv.org/abs/2305.14325 |

## 2. Adjacent scalable oversight protocols and ideas

| Year | Authors | Title | Venue | Relevance to debate | Centrality | Link |
|---|---|---|---|---|---|---|
| 2018 | Leike, Krueger, Everitt, et al. | Scalable agent alignment via reward modeling: a research direction | arXiv | Recursive reward modeling; the closest sibling framing to debate | adjacent | https://arxiv.org/abs/1811.07871 |
| 2021 | Wu, Ouyang, Ziegler, et al. | Recursively Summarizing Books with Human Feedback | arXiv | Empirical task decomposition for supervising hard-to-evaluate outputs | adjacent | https://arxiv.org/abs/2109.10862 |
| 2021 | Anil, Zhang, Wu, Grosse | Learning to Give Checkable Answers with Prover-Verifier Games | arXiv | Original prover-verifier game formulation | adjacent | https://arxiv.org/abs/2108.12099 |
| 2022 | Saunders, Yeh, Wu, et al. | Self-critiquing models for assisting human evaluators | arXiv | Critique assistance raises human evaluator flaw detection | adjacent | https://arxiv.org/abs/2206.05802 |
| 2022 | Bowman, Hyun, Perez, et al. | Measuring Progress on Scalable Oversight for Large Language Models | arXiv | Sandwiching-style experiments; assisted humans beat unassisted | adjacent | https://arxiv.org/abs/2211.03540 |
| 2023 | Burns, Izmailov, Kirchner, et al. | Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision | arXiv (ICML 2024) | Weak supervisor, strong student; debate can supply the weak signal | adjacent | https://arxiv.org/abs/2312.09390 |
| 2023 | Greenblatt, Shlegeris, Sachan, Roger | AI Control: Improving Safety Despite Intentional Subversion | arXiv (ICML 2024) | Oversight under adversarial models; complements debate with monitoring | background | https://arxiv.org/abs/2312.06942 |
| 2024 | McAleese, Pokorny, Ceron Uribe, et al. | LLM Critics Help Catch LLM Bugs | arXiv | CriticGPT; model critiques assist human code reviewers | adjacent | https://arxiv.org/abs/2407.00215 |
| 2024 | Kirchner, Chen, Edwards, Leike, et al. | Prover-Verifier Games improve legibility of LLM outputs | arXiv | Trains legible solutions against sneaky provers; debate-like adversarial training | adjacent | https://arxiv.org/abs/2407.13692 |
| 2024 | Hammond, Adam-Day | Neural Interactive Proofs | arXiv | Formal framework covering debate, PVGs and other interactive-proof protocols | adjacent | https://arxiv.org/abs/2412.08897 |
| 2025 | Engels, Baek, Kantamneni, Tegmark | Scaling Laws For Scalable Oversight | arXiv | Nested oversight, Elo scaling; includes debate among tested games | adjacent | https://arxiv.org/abs/2504.18530 |
| 2025 | Jain, Bridgers, Janzer, et al. | Human-AI Complementarity: A Goal for Amplified Oversight | arXiv | Frames amplified oversight goals; debate as one tool | adjacent | https://arxiv.org/abs/2510.26518 |
| 2026 | Young | Knowledge Divergence and the Value of Debate for Scalable Oversight | arXiv | Theory of when debate adds value over other oversight | core | https://arxiv.org/abs/2603.05293 |
| 2026 | Guan, Kalai, Rothblum | Efficient Scalable Oversight via Rewinding | arXiv | Interactive-proof style oversight protocol; relates to doubly-efficient debate | adjacent | https://arxiv.org/abs/2610.40535 |
| 2020 | Hubinger | AI safety via market making | LessWrong post | Market-making alternative to debate (author and date unverified) | adjacent | https://www.lesswrong.com/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making |
| 2021 | Cotra | The case for aligning narrowly superhuman models | AI Alignment Forum | Origin of the sandwiching evaluation setup | adjacent | https://www.alignmentforum.org/posts/PZtsoaoSLpKjjbMqM/the-case-for-aligning-narrowly-superhuman-models |
| 2021 | Christiano, Cotra, Xu (unverified byline) | ARC's first technical report: Eliciting Latent Knowledge | LessWrong post | ELK; connects to what honest debaters must elicit (byline unverified) | background | https://www.lesswrong.com/posts/qHCDysDnvhteW7kRd/arc-s-first-technical-report-eliciting-latent-knowledge |
| 2022 | Burns, Ye, Klein, Steinhardt | Discovering Latent Knowledge in Language Models Without Supervision | arXiv (ICLR 2023) | Unsupervised truth probing; alternative route to truthful signals | background | https://arxiv.org/abs/2212.03827 |

## 3. Problems that threaten debate

| Year | Authors | Title | Venue | Relevance to debate | Centrality | Link |
|---|---|---|---|---|---|---|
| 2022 | Perez, Ringer, Lukosiute, et al. | Discovering Language Model Behaviors with Model-Written Evaluations | arXiv (ACL Findings 2023) | Documents sycophancy that can corrupt judges and debaters | background | https://arxiv.org/abs/2212.09251 |
| 2022 | Gao, Schulman, Hilton | Scaling Laws for Reward Model Overoptimization | arXiv (ICML 2023) | Overoptimizing a proxy judge degrades true quality | background | https://arxiv.org/abs/2210.10760 |
| 2022 | Skalse, Howe, Krasheninnikov, Krueger | Defining and Characterizing Reward Hacking | arXiv (NeurIPS 2022) | Formal basis for judge exploitation by debaters | background | https://arxiv.org/abs/2209.13085 |
| 2023 | Sharma, Tong, Korbak, et al. | Towards Understanding Sycophancy in Language Models | arXiv (ICLR 2024) | Human and model preferences reward agreement over truth | adjacent | https://arxiv.org/abs/2310.13548 |
| 2023 | Wang, Li, Chen, et al. | Large Language Models are not Fair Evaluators | arXiv | Position bias in LLM judges | adjacent | https://arxiv.org/abs/2305.17926 |
| 2023 | Zheng, Chiang, Sheng, et al. | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | arXiv (NeurIPS 2023) | Position, verbosity and self-preference bias in judges | adjacent | https://arxiv.org/abs/2306.05685 |
| 2024 | Wen, Zhong, Khan, et al. | Language Models Learn to Mislead Humans via RLHF | arXiv | RLHF makes models more convincing without being more correct, a judge-fooling case | adjacent | https://arxiv.org/abs/2409.12822 |
| 2024 | Shi, Ma, Liang, et al. | Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge | arXiv | Quantifies position bias across judge models | adjacent | https://arxiv.org/abs/2406.07791 |
| 2024 | Ye, Wang, Huang, et al. | Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge | arXiv | Catalogues twelve judge biases | adjacent | https://arxiv.org/abs/2410.02736 |
| 2024 | Salvi, Horta Ribeiro, Gallotti, West | On the Conversational Persuasiveness of Large Language Models: A Randomized Controlled Trial | arXiv | LLMs out-persuade humans when personalised; persuasion risk for judges | adjacent | https://arxiv.org/abs/2403.14380 |
| 2024 | Denison, MacDiarmid, Barez, et al. | Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models | arXiv | Reward tampering generalizes from sycophancy | background | https://arxiv.org/abs/2406.10162 |
| 2024 | van der Weij, Hofstatter, Jaffe, et al. | AI Sandbagging: Language Models can Strategically Underperform on Evaluations | arXiv | Sandbagging by a debater or judge would undermine oversight | background | https://arxiv.org/abs/2406.07358 |
| 2024 | Greenblatt, Roger, Krasheninnikov, Krueger | Stress-Testing Capability Elicitation With Password-Locked Models | arXiv | Whether fine-tuning can elicit hidden capability; relevant to sandbagged debaters | background | https://arxiv.org/abs/2405.19550 |
| 2024 | Greenblatt, Denison, Wright, et al. | Alignment faking in large language models | arXiv | Models behave differently when they infer they are trained or overseen | background | https://arxiv.org/abs/2412.14093 |
| 2025 | Baker, Huizinga, Gao, et al. | Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation | arXiv | Optimizing against a monitor induces obfuscated misbehavior | adjacent | https://arxiv.org/abs/2503.11926 |
| 2025 | Recchia, Mangat, Nyachhyon, et al. | Confirmation bias: A challenge for scalable oversight | arXiv | Human confirmation bias degrades oversight protocols | adjacent | https://arxiv.org/abs/2507.19486 |
| 2026 | Jang, Falck, Braun, et al. | Exploration Hacking: Can LLMs Learn to Resist RL Training? | arXiv | Models withholding exploration to evade RL, including debate training | adjacent | https://arxiv.org/abs/2604.28182 |

## 4. Evaluation and datasets

| Year | Authors | Title | Venue | Relevance to debate | Centrality | Link |
|---|---|---|---|---|---|---|
| 2020 | Hendrycks, Burns, Basart, et al. | Measuring Massive Multitask Language Understanding | arXiv (ICLR 2021) | MMLU; used as oversight test bed in sandwiching studies | background | https://arxiv.org/abs/2009.03300 |
| 2021 | Lin, Hilton, Evans | TruthfulQA: Measuring How Models Mimic Human Falsehoods | arXiv (ACL 2022) | Truthfulness benchmark used in debate and oversight experiments | background | https://arxiv.org/abs/2109.07958 |
| 2021 | Pang, Parrish, Joshi, et al. | QuALITY: Question Answering with Long Input Texts, Yes! | arXiv (NAACL 2022) | Main dataset for human and LLM debate with information asymmetry | adjacent | https://arxiv.org/abs/2112.08608 |
| 2023 | Rein, Hou, Stickland, et al. | GPQA: A Graduate-Level Google-Proof Q&A Benchmark | arXiv (COLM 2024) | Hard expert questions used for scalable oversight tests | adjacent | https://arxiv.org/abs/2311.12022 |
| 2024 | Zheng, Zhang, Zhang, et al. | ProcessBench: Identifying Process Errors in Mathematical Reasoning | arXiv (ACL 2025) | Step-level error finding; a critique and verification benchmark | background | https://arxiv.org/abs/2412.06559 |
| 2025 | Sudhir, Kaunismaa, Panickssery | A Benchmark for Scalable Oversight Protocols | arXiv | Framework and benchmark comparing debate, consultancy and other protocols | adjacent | https://arxiv.org/abs/2504.03731 |

## 5. Safety cases, surveys, position papers

| Year | Authors | Title | Venue | Relevance to debate | Centrality | Link |
|---|---|---|---|---|---|---|
| 2022 | Ngo, Chan, Mindermann | The Alignment Problem from a Deep Learning Perspective | arXiv | Frames why oversight must scale beyond human evaluation | background | https://arxiv.org/abs/2209.00626 |
| 2023 | Casper, Davies, Shi, et al. | Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback | arXiv (TMLR) | Limits of human feedback that motivate scalable oversight | background | https://arxiv.org/abs/2307.15217 |
| 2024 | Anwar, Saparov, Rando, et al. | Foundational Challenges in Assuring Alignment and Safety of Large Language Models | arXiv | Agenda including scalable oversight open problems | background | https://arxiv.org/abs/2404.09932 |
| 2024 | Clymer, Gabrieli, Krueger, Larsen | Safety Cases: How to Justify the Safety of Advanced AI Systems | arXiv | Safety-case methodology that debate arguments would plug into | background | https://arxiv.org/abs/2403.10462 |
| 2025 | Buhl, Pfau, Hilton, Irving | An alignment safety case sketch based on debate | arXiv (UK AISI) | Safety case sketch using debate; lists open research problems | core | https://arxiv.org/abs/2505.03989 |
| 2025 | Shah, Irpan, Turner, et al. | An Approach to Technical AGI Safety and Security | arXiv (Google DeepMind) | Amplified oversight with debate as a central component | adjacent | https://arxiv.org/abs/2504.01849 |
| 2025 | Korbak, Balesni, Barnes, et al. | Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety | arXiv | Position paper on CoT monitoring, a complement to debate | background | https://arxiv.org/abs/2507.11473 |

## Notes

- Total entries: 59. Entries with an unverified field: 2.
- Obfuscated arguments and prover-estimator debate are by excluded authors and left to the core list.
- Not found or not checked: a dedicated long-context debate benchmark beyond QuALITY-based work.
