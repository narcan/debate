#!/usr/bin/env python3
"""Parametric cost model for LLM debate experiments. Stdlib only.

Examples:
  cost_calc.py cost --debater anthropic-haiku --judge anthropic-haiku \
      --protocol standard --rounds 3 --questions 200 --cells 2 --repeats 2 --batch --cache
  cost_calc.py scenarios
  cost_calc.py tiers
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRICES_PATH = os.path.join(HERE, "prices.json")
DATE = "2026-11-12"

# USD per 1M tokens. cached = cache-read price. cache_write_mult applies to uncached input when caching is on.
DEFAULT_PRICES = {
    "_meta": {"date": DATE, "note": "Aggregator-sourced, official pages not confirmed. Re-verify before budgeting.",
              "batch_discount": 0.5},
    "anthropic-haiku":  {"in": 1.00, "out": 5.00,  "cached": 0.10, "cache_write_mult": 1.25, "batch": 0.5,
                         "model": "Haiku 4.5", "source": "https://www.morphllm.com/anthropic-api-pricing", "verified": False},
    "anthropic-sonnet": {"in": 3.00, "out": 15.00, "cached": 0.30, "cache_write_mult": 1.25, "batch": 0.5,
                         "model": "Sonnet 4.6", "source": "https://www.morphllm.com/anthropic-api-pricing", "verified": False},
    "anthropic-opus":   {"in": 5.00, "out": 25.00, "cached": 0.50, "cache_write_mult": 1.25, "batch": 0.5,
                         "model": "Opus 4.6/4.7", "source": "https://www.morphllm.com/anthropic-api-pricing", "verified": False},
    "openai-small":     {"in": 0.20, "out": 1.25,  "cached": 0.02, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "GPT-5.4 nano", "source": "https://www.benchlm.ai/blog/posts/openai-api-pricing", "verified": False},
    "openai-mid":       {"in": 0.75, "out": 4.50,  "cached": 0.075, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "GPT-5.4 mini", "source": "https://www.benchlm.ai/blog/posts/openai-api-pricing", "verified": False},
    "openai-frontier":  {"in": 5.00, "out": 30.00, "cached": 0.50, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "GPT-5.6 Sol (promo pricing, at least to 2026-11-21)", "source": "https://www.finout.io/blog/openai-pricing-in-2026", "verified": False},
    "gemini-flash":     {"in": 0.50, "out": 3.00,  "cached": 0.05, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "Gemini 3 Flash preview (cache price derived as 90% off, storage fee extra)",
                         "source": "https://ai.google.dev/gemini-api/docs/pricing", "verified": False},
    "gemini-pro":       {"in": 2.00, "out": 12.00, "cached": 0.20, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "Gemini 3.1 Pro preview, <=200k ctx (sources conflict)",
                         "source": "https://www.morphllm.com/gemini-api-pricing", "verified": False},
    "together-8b":      {"in": 0.18, "out": 0.18,  "cached": 0.18, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "Llama 3.1 8B (no cache discount assumed)",
                         "source": "https://www.aipricing.guru/meta-llama-pricing/", "verified": False},
    "together-70b":     {"in": 0.88, "out": 0.88,  "cached": 0.88, "cache_write_mult": 1.0, "batch": 0.5,
                         "model": "Llama 3.3 70B (a June 2026 tracker reports a rise to 1.04)",
                         "source": "https://pricingsaas.com/companies/together/diffs/2026W24", "verified": False},
    "_gpu_hourly": {"h100_low": 2.29, "h100_median": 4.20, "a100_80gb_low": 1.49, "a100_80gb_median": 2.75,
                    "source": "https://uvik.net/blog/gpu-price-index/ ; https://gpuperhour.com/rent/h100-sxm-80gb",
                    "verified": False},
}

def load_prices():
    if not os.path.exists(PRICES_PATH):
        with open(PRICES_PATH, "w") as f:
            json.dump(DEFAULT_PRICES, f, indent=2)
    with open(PRICES_PATH) as f:
        return json.load(f)

# ---- protocol turn schedules ----
# Each turn: (role, out_tokens, in_transcript). Every call reads prompt P + transcript so far.
def schedule(protocol, rounds, T, J, Q=None):
    Q = Q or max(T // 3, 1)
    turns = []
    if protocol == "standard":          # alternating A, B each round
        for _ in range(rounds):
            turns += [("debater", T, True), ("debater", T, True)]
    elif protocol == "simultaneous":    # both see only prior rounds; parallel calls, same cost per call
        for _ in range(rounds):
            turns += [("debater", T, "round"), ("debater", T, "round")]
    elif protocol == "consultancy":     # one consultant, judge questions each round
        for _ in range(rounds):
            turns += [("debater", T, True), ("judge", Q, True)]
    elif protocol == "cross-exam":      # standard + cross-exam block after half the rounds
        half = max(rounds // 2, 1)
        for r in range(rounds):
            turns += [("debater", T, True), ("debater", T, True)]
            if r + 1 == half:
                turns += [("debater", Q, True), ("debater", Q, True),   # each asks
                          ("debater", Q, True), ("debater", Q, True)]   # each answers
    else:
        raise SystemExit("unknown protocol " + protocol)
    turns.append(("judge", J, False))   # verdict
    return turns

PROTOCOLS = ["standard", "simultaneous", "consultancy", "cross-exam"]

def tokens_per_debate(protocol, rounds, T, P, J):
    """Returns dict role -> dict(in, out, cached_in) per single debate."""
    res = {"debater": {"in": 0, "out": 0, "cached": 0, "calls": 0},
           "judge":   {"in": 0, "out": 0, "cached": 0, "calls": 0}}
    ctx = P
    last_ctx = {}   # per role: context size at its previous call (cache prefix)
    round_ctx = P
    pending = 0
    turns = schedule(protocol, rounds, T, J)
    for i, (role, out, vis) in enumerate(turns):
        if vis == "round":
            inp = round_ctx
        else:
            inp = ctx
        r = res[role]
        r["in"] += inp
        r["out"] += out
        r["calls"] += 1
        prev = last_ctx.get(role)
        if prev is not None:
            r["cached"] += min(prev, inp)   # prefix already seen by this role's previous call
        last_ctx[role] = inp + out          # prefix incl. its own output is cacheable next time
        if vis is True:
            ctx += out
        elif vis == "round":
            pending += out
            if (i + 1) % 2 == 0:            # round boundary
                ctx += pending; round_ctx = ctx; pending = 0
    return res

def cost_usd(tok, price, batch, cache, batch_disc):
    inp, out, cached = tok["in"], tok["out"], tok["cached"] if cache else 0
    fresh = inp - cached
    wm = price.get("cache_write_mult", 1.0) if cache else 1.0
    usd = (fresh * price["in"] * wm + cached * price["cached"] + out * price["out"]) / 1e6
    if batch:
        usd *= price.get("batch", batch_disc)
    return usd

def debate_cost(prices, deb, jud, protocol, rounds, T, P, J, batch, cache):
    tok = tokens_per_debate(protocol, rounds, T, P, J)
    bd = prices["_meta"]["batch_discount"]
    usd = (cost_usd(tok["debater"], prices[deb], batch, cache, bd) +
           cost_usd(tok["judge"], prices[jud], batch, cache, bd))
    tin = tok["debater"]["in"] + tok["judge"]["in"]
    tout = tok["debater"]["out"] + tok["judge"]["out"]
    return tin, tout, usd

def fmt_tok(n):
    return f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:.0f}k"

def cmd_cost(a):
    prices = load_prices()
    protos = PROTOCOLS if a.protocol == "all" else [a.protocol]
    n = a.questions * a.cells * a.repeats
    print(f"debates per protocol = questions {a.questions} x cells {a.cells} x repeats {a.repeats} = {n}")
    print(f"debater={a.debater} judge={a.judge} rounds={a.rounds} T={a.tokens_per_turn} P={a.prompt_tokens} "
          f"J={a.judge_tokens} batch={a.batch} cache={a.cache}")
    tot_in = tot_out = tot_usd = 0
    print(f"{'protocol':<14}{'in/debate':>11}{'out/debate':>12}{'$/debate':>10}{'total in':>11}{'total out':>11}{'total USD':>12}")
    for p in protos:
        i, o, u = debate_cost(prices, a.debater, a.judge, p, a.rounds, a.tokens_per_turn,
                              a.prompt_tokens, a.judge_tokens, a.batch, a.cache)
        print(f"{p:<14}{i:>11}{o:>12}{u:>10.4f}{fmt_tok(i*n):>11}{fmt_tok(o*n):>11}{u*n:>12.2f}")
        tot_in += i*n; tot_out += o*n; tot_usd += u*n
    print(f"TOTAL tokens in={fmt_tok(tot_in)} out={fmt_tok(tot_out)} all={fmt_tok(tot_in+tot_out)}  USD={tot_usd:,.2f}")

def cmd_tiers(a):
    for k, v in load_prices().items():
        if k.startswith("_"): continue
        print(f"{k:<18} in {v['in']:<6} out {v['out']:<6} cached {v['cached']:<6} {v['model']}")

# name -> (debater, judge)
TIERS = {"cheap": ("anthropic-haiku", "anthropic-haiku"),
         "mixed": ("anthropic-sonnet", "anthropic-haiku"),
         "frontier": ("anthropic-opus", "anthropic-opus")}
SCEN = {  # protocols, pairs, gaps, questions, rounds
    "Pilot": (["standard"], 2, 1, 200, 3),
    "Mid":   (["standard", "simultaneous", "consultancy", "cross-exam", "standard"], 3, 2, 300, 3),
    "Full":  (PROTOCOLS, 6, 4, 1000, 5),
}

def cmd_scenarios(a):
    prices = load_prices()
    rep = a.repeats
    print(f"T={a.tokens_per_turn} P={a.prompt_tokens} J={a.judge_tokens} repeats={rep} (Mid repeats 5th protocol = standard variant)")
    print(f"{'scenario':<8}{'debates':>10}{'tokens':>9}  " + "  ".join(f"{t+' list':>13}{t+' b+c':>13}" for t in TIERS))
    for name, (protos, pairs, gaps, q, rounds) in SCEN.items():
        debates = len(protos) * pairs * gaps * q * rep
        row = []; toks = 0
        for t, (d, j) in TIERS.items():
            for batch, cache in ((False, False), (True, True)):
                usd = 0; tk = 0
                for p in protos:
                    i, o, u = debate_cost(prices, d, j, p, rounds, a.tokens_per_turn, a.prompt_tokens,
                                          a.judge_tokens, batch, cache)
                    k = pairs * gaps * q * rep
                    usd += u * k; tk += (i + o) * k
                row.append(usd); toks = tk
        print(f"{name:<8}{debates:>10}{fmt_tok(toks):>9}  " + "  ".join(f"{x:>13,.0f}" for x in row))

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    def common(s):
        s.add_argument("--rounds", type=int, default=3)
        s.add_argument("--tokens-per-turn", type=int, default=300)
        s.add_argument("--prompt-tokens", type=int, default=1500, help="question + source passage + instructions")
        s.add_argument("--judge-tokens", type=int, default=300)
        s.add_argument("--repeats", type=int, default=2)
    c = sub.add_parser("cost"); common(c)
    c.add_argument("--debater", default="anthropic-haiku"); c.add_argument("--judge", default="anthropic-haiku")
    c.add_argument("--protocol", default="standard", choices=PROTOCOLS + ["all"])
    c.add_argument("--questions", type=int, default=200); c.add_argument("--cells", type=int, default=1)
    c.add_argument("--batch", action="store_true", help="apply batch discount")
    c.add_argument("--cache", action="store_true", help="apply prompt-cache pricing")
    c.set_defaults(f=cmd_cost)
    s = sub.add_parser("scenarios"); common(s); s.set_defaults(f=cmd_scenarios)
    t = sub.add_parser("tiers"); t.set_defaults(f=cmd_tiers)
    a = ap.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
