#!/usr/bin/env python3
"""Check model IDs against OpenRouter /models and record per-token prices to data/model_prices.json.
No key needed for this endpoint. Usage: fetch_models.py [model_id ...]"""
import json, os, sys, time, requests

DEFAULT = ["anthropic/claude-haiku-4.5", "openai/gpt-5.4-nano", "openai/gpt-5.4-mini"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "model_prices.json")

def main():
    ids = sys.argv[1:] or DEFAULT
    r = requests.get("https://openrouter.ai/api/v1/models", timeout=60)
    r.raise_for_status()
    by_id = {m["id"]: m for m in r.json()["data"]}
    out = {"_meta": {"fetched": time.strftime("%Y-%m-%d"), "unit": "USD per token (as returned by OpenRouter)"}}
    for i in ids:
        if i not in by_id:
            sys.exit(f"model id not found on OpenRouter: {i}")
        m = by_id[i]
        p = m["pricing"]
        out[i] = {k: float(v) for k, v in p.items() if k in
                  ("prompt", "completion", "input_cache_read", "input_cache_write")}
        out[i]["context_length"] = m.get("context_length")
        print(i, {k: f"${v*1e6:.3f}/M" for k, v in out[i].items() if k != "context_length"})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=1)

if __name__ == "__main__":
    main()
