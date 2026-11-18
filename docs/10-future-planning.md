# 10 Notes for future planning (2026-11-16)

The project is paused at the Phase 0 pilot. This file records what a continuation would need. Results are in `09-phase0-results.md`; estimates below are inference from those results and are marked as such.

## What the pilot showed

- Critique-only beat standard 3-round debate by 4.0 points (95% CI -1.5 to +9.5), a null under the pre-registered rule. Debate cost about 2.15 times as much per instance ($0.0295 vs $0.0137).
- 100 questions detects only differences of about 13 points or more. The agent's estimate for detecting a 4-point difference is about 380 questions.
- A blind judge scored 57.0%, near the lower edge of the 55 to 90% validity gate.

## Problems to fix before another run

1. Truncation: 84% of standard debater turns hit the 300-token cap and many were cut mid-sentence. Results describe T=300, not argument quality. Raising the cap raises debater output cost.
2. Judge bias: the judge leaned toward rejecting the argued answer in critique-only and toward trusting the consultant in consultancy. Standard accuracy was 72% when the gold answer was A and 83% when it was B.
3. Quotes: about 8 to 10% of Haiku 4.5 quotes were invented or altered.
4. Rate limits: HTTP 429 at 8 workers and persistently at 3 to 4. Throughput was about 3 debates per minute.
5. Credit: OpenRouter's prepaid balance ($20.00) ran out during cross-exam, which stopped at 169 of 200 instances. Top up before any run.

## Rough size of a narrower Phase 1 (inference)

About 380 questions at 2 variants is 760 instances per arm. At the measured per-instance costs, critique-only plus standard at T=300 is about $33 raw. A larger token cap would raise that. Cross-exam ($0.0406 per instance) would add about $31. Against a $100 compute cap, two to three arms fit once margin is included.

## Open options

- Fix truncation first, rerun a small check, then decide whether the full sample is worth it.
- Test a cheaper debater (`anthropic/claude-haiku-5.5` is listed at about a tenth of the Haiku 4.5 price and is untested).
- Move to the planned questions: values-type questions and human judges.

## Added 2026-11-18: judge strength

The pilot's judge is passage-blind, which makes it weaker in information, but nothing in the repo shows it is weaker in capability than the debater (GPT-5.4 nano costs about a fifth of Haiku 4.5 per token, and price is only a rough proxy). Two additions for any continuation:

1. Capability check: give each model the passage and the question with no debate, and compare accuracy. This is about 400 calls, estimated well under $2.
2. Judge-strength sweep with an open-weight family served by a hosted provider (the Qwen family on OpenRouter lists several sizes). Report accuracy, position bias, susceptibility to persuasive wrong arguments and calibration. Which of the listed Qwen models have open weights is unchecked.
