# Related works bibliography: debate as scalable oversight, 2016-2026

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
