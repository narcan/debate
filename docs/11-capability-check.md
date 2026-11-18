# 11 Capability check (2026-11-18)

Question: is the Phase 0 judge (GPT-5.4 nano) actually weaker than the debater (Claude Haiku 4.5)? Each model answered the same 200 binary instances (QuALITY hard subset, 100 questions, seed 0, 2 variants) directly, with no debate, at temperature 0. Script: `scripts/capability_check.py`. Haiku used no reasoning; nano used reasoning effort low (as in Phase 0). Raw outputs are not published.

| Condition | n valid | Accuracy | Cost |
|---|---|---|---|
| Haiku 4.5, with passage | 200 | 89.0% | $1.74 |
| Nano, with passage | 200 | 78.5% | $0.13 |
| Haiku 4.5, blind | 151 of 200 | 60.9% (valid answers only) | $0.22 |
| Nano, blind (Phase 0 blind arm) | 200 | 57.0% | $0.03 |

Paired bootstrap over questions (10,000 resamples, seed 0): Haiku minus nano with the passage is +10.5 points (95% CI +4.0 to +17.5). Haiku with the passage minus Haiku blind is +28.5 points on the 151 valid pairs (CI +19.1 to +38.0).

## Reading

- The judge is weaker than the debater in capability as well as information: about 10 points on reading comprehension with the passage, with an interval that excludes zero.
- Haiku declined to guess on 49 of 200 blind items (it said it could not answer without the story). Its blind accuracy covers only the answered 151 and is not comparable to nano's 57.0% on all 200.
- Inference: nano with the full passage (78.5%) scores about the same as nano judging a 3-round debate (77.5%) and a critique (81.5%). In this setup debate and critique do not lift the judge above what it would reach reading the passage itself. Relative to the gap between nano blind (57.0%) and Haiku with the passage (89.0%), standard debate closes about 64% and critique-only about 77%. These ratios use point estimates only, with no intervals, and are exploratory.

## Open-weight sweep (2026-11-18, hosted via OpenRouter, with passage, no debate)

Model sizes are as named on OpenRouter. Which of these have open weights is unchecked. Differences are Haiku minus the model, paired bootstrap over questions.

| Model | Valid of 200 | Accuracy (valid only) | Haiku minus model (95% CI) | Cost |
|---|---|---|---|---|
| `qwen/qwen3.8-27b` | 182 | 91.8% | -2.2 (-7.1 to +2.6) | $0.45 |
| `qwen/qwen3.6-35b-a3b` | 199 | 88.9% | 0.0 (-5.5 to +5.6) | $0.26 |
| `qwen/qwen3.5-9b`, strict format, reasoning off | 200 | 76.5% | +12.5 (+5.0 to +20.0) | $0.15 |
| `qwen/qwen3.5-9b`, first try | 146 | 87.0% | not comparable | $0.20 |
| `openai/gpt-5.4-nano` (earlier) | 200 | 78.5% | +10.5 (+4.0 to +17.5) | $0.13 |

The first 9b run lost 54 answers because its reasoning hit the 3,000-token cap, not because of format. The 27b run lost 18 answers for the same likely reason and its accuracy covers only the answered items, so it may be inflated.

Reading: the two larger Qwen models read as well as Haiku 4.5 on this task. Only the 9b model shows a capability gap (about 12.5 points), the same size as nano's. No tested judge is more than about 13 points below the debater when given the passage. The much larger gap is information: a blind judge scores 57.0% against 89.0% for Haiku with the passage.
