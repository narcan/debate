# 02 Cost Model for Debate Experiments

Date of price check: 2026-11-12. Tool: `tools/cost_calc.py` (stdlib only, writes `tools/prices.json` on first run).
Status: all prices come from third-party aggregators. Official pages (Anthropic, OpenAI, Google, Together) did not return usable content via search, so every row is **unverified**. Re-check before spending real money.

## 1. Prices (USD per 1M tokens)

| Key | Model | Input | Output | Cached in | Batch | Source | Status |
|---|---|---|---|---|---|---|---|
| anthropic-haiku | Haiku 4.5 | 1.00 | 5.00 | 0.10 (write 1.25x) | -50% | https://www.morphllm.com/anthropic-api-pricing | unverified |
| anthropic-sonnet | Sonnet 4.6 | 3.00 | 15.00 | 0.30 | -50% | same | unverified |
| anthropic-opus | Opus 4.6/4.7 | 5.00 | 25.00 | 0.50 | -50% | same | unverified |
| openai-small | GPT-5.4 nano | 0.20 | 1.25 | 0.02 | -50% | https://www.benchlm.ai/blog/posts/openai-api-pricing | unverified |
| openai-mid | GPT-5.4 mini | 0.75 | 4.50 | 0.075 | -50% | same | unverified |
| openai-frontier | GPT-5.6 Sol (promo, at least to 2026-11-21) | 5.00 | 30.00 | 0.50 | -50% | https://www.finout.io/blog/openai-pricing-in-2026 | unverified |
| gemini-flash | Gemini 3 Flash preview | 0.50 | 3.00 | 0.05 (derived, 90% off) | -50% | https://ai.google.dev/gemini-api/docs/pricing | unverified, sources conflict |
| gemini-pro | Gemini 3.1 Pro preview (<=200k ctx) | 2.00 | 12.00 | 0.20 (derived) | -50% | https://www.morphllm.com/gemini-api-pricing | unverified, sources conflict |
| together-8b | Llama 3.1 8B | 0.18 | 0.18 | none | assumed -50% | https://www.aipricing.guru/meta-llama-pricing/ | unverified |
| together-70b | Llama 3.3 70B | 0.88 | 0.88 | none | assumed -50% | https://pricingsaas.com/companies/together/diffs/2026W24 (reports rise to 1.04) | unverified |

Notes: newer Anthropic names (Sonnet 5, Haiku 5.5) appear on aggregators with conflicting prices. Not used. Gemini cache storage is billed hourly on top (not modeled).

### Self-hosting GPU rental (per GPU-hour, on-demand)

| GPU | Low | Median | Source | Status |
|---|---|---|---|---|
| H100 80GB | 2.29 | 4.20 (hyperscalers 6.88 to 12.29) | https://uvik.net/blog/gpu-price-index/ , https://gpuperhour.com/rent/h100-sxm-80gb | unverified |
| A100 80GB | 1.49 | 2.75 | https://akash.network/the-bid/h100-rental-price-2026-cost-per-hour/ , uvik (above) | unverified |

Self-host rule: USD per 1M output tokens = GPU $/hr x GPUs / (tokens per sec x 3600) x 1e6. Throughput for 70B on 2xH100 under batching is not sourced; measure it (unverified).

## 2. Debate unit

Symbols: N rounds, T tokens per debater turn, P prompt (question + passage + rules), J verdict tokens, Q = T/3 for judge questions and cross-exam turns. Every call re-reads P plus the transcript visible to it.

| Variant | Turn schedule | Calls | Input growth |
|---|---|---|---|
| standard | A, B per round, then verdict | 2N + 1 | each turn adds T to context |
| simultaneous | A, B in parallel per round, see only prior rounds | 2N + 1 | context grows 2T per round, same-round turns do not see each other |
| consultancy | 1 consultant turn (T), judge question (Q) per round, then verdict | 2N + 1 | adds T + Q per round |
| cross-exam | standard, plus 4 short turns (Q) after round N/2 | 2N + 5 | standard plus a mid-debate block |

Closed form, standard: input = (2N+1)P + T x (2N)(2N+1)/2 (sum over calls), output = 2NT + J. Input grows quadratically in N, so rounds are the main token driver.

Per-debate tokens (N=3, T=300, P=1500, J=300), from the script:

| Variant | Input | Output |
|---|---|---|
| standard | 16,800 | 2,100 |
| simultaneous | 15,900 | 2,100 |
| consultancy | 15,000 | 1,500 |
| cross-exam | 27,800 | 2,500 |

Cache model: a role's second and later calls hit cache on the prefix it already saw (minus new tokens). Anthropic cache writes bill at 1.25x on fresh input.

## 3. Scenarios

Assumptions: Standard defaults above (N=3 for Pilot and Mid, N=5 for Full), 2 repeats (side swap), cost in USD. Tiers: cheap = Haiku debaters + Haiku judge, mixed = Sonnet debaters + Haiku judge, frontier = Opus + Opus. "b+c" = batch and cache on.

| Scenario | Grid | Debates | Tokens | Cheap list | Cheap b+c | Mixed list | Mixed b+c | Frontier list | Frontier b+c |
|---|---|---|---|---|---|---|---|---|---|
| Pilot | 1 protocol x 2 model tiers x 200 q | 800 | 15.1M | 22 | 7 | 58 | 17 | 109 | 35 |
| Mid | 5 protocols x 3 model pairs x 2 gap types x 300 q | 18,000 | 369M | 518 | 160 | 1,323 | 372 | 2,588 | 798 |
| Full | 4 protocols x 6 model pairs x 4 gap types x 1000 q, N=5 | 192,000 | 7.3B | 9,730 | 2,523 | 25,454 | 6,084 | 48,648 | 12,617 |

Ranges (USD): Pilot 7 to 109, Mid 160 to 2,588, Full 2,523 to 48,648.
Mid note: the 5th protocol is modeled as a standard variant (different judge prompt) since only 4 schedules exist.
Pilot caveat: the 2 tiers are priced as if both ran the same tier column. Real Pilot is a mix of two columns, so it falls between them.
Reproduce: `python3 tools/cost_calc.py scenarios`.

## 4. Three biggest cost levers

| Rank | Lever | Effect | Note |
|---|---|---|---|
| 1 | Model tier of debaters and judge | Opus is 5x Haiku (list), 5x on Sonnet vs Haiku pair spread | Use a weak judge, strong debaters only where the gap type needs it |
| 2 | Batch + prompt cache | Cuts list cost by about 3x (Haiku 518 to 160, Full 48.6k to 12.6k) | Needs async runs and a stable shared prefix (P plus transcript) |
| 3 | Rounds N and tokens per turn T | Input is quadratic in N: N=3 to 5 raises tokens per debate about 2.4x | Pilot at N=3, only scale N on cells that need it |

## 5. Usage

```
python3 tools/cost_calc.py tiers
python3 tools/cost_calc.py cost --debater anthropic-sonnet --judge anthropic-haiku \
    --protocol all --rounds 3 --questions 300 --cells 30 --repeats 2 --batch --cache
python3 tools/cost_calc.py scenarios --tokens-per-turn 300
```

Edit `tools/prices.json` to update prices or add keys (fields: in, out, cached, cache_write_mult, batch).
