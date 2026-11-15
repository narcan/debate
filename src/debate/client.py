"""OpenRouter chat client with a hard budget guard and per-call JSONL log.

Messages: {"role": ..., "content": str | [{"text": str, "cache": bool}, ...]}.
Parts with cache=True get an Anthropic cache_control breakpoint (Anthropic models only).
Key comes from env OPENROUTER_API_KEY only; it is never logged or written.
"""
import json, os, threading, time
from dataclasses import dataclass, field

BASE_URL = "https://openrouter.ai/api/v1"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PRICES_PATH = os.path.join(ROOT, "data", "model_prices.json")
LEDGER_PATH = os.path.join(ROOT, "logs", "ledger.json")


class BudgetExceeded(RuntimeError):
    pass


def load_prices(path=PRICES_PATH):
    try:
        with open(path) as f:
            return json.load(f)
    except OSError:
        return {}


class BudgetGuard:
    """Cumulative cost guard. run_cap: this run. global_cap: across runs via a ledger file."""

    def __init__(self, run_cap, global_cap=None, ledger_path=None):
        self.run_cap = float(run_cap)
        self.global_cap = None if global_cap is None else float(global_cap)
        self.ledger_path = ledger_path
        self.spent = 0.0
        self.prior = self._read_ledger()
        self._lock = threading.Lock()

    def _read_ledger(self):
        if not self.ledger_path:
            return 0.0
        try:
            with open(self.ledger_path) as f:
                return float(json.load(f).get("total_usd", 0.0))
        except (OSError, ValueError):
            return 0.0

    def check(self, est=0.0):
        with self._lock:
            if self.spent + est > self.run_cap:
                raise BudgetExceeded(f"run cap ${self.run_cap:.4f} would be exceeded "
                                     f"(spent ${self.spent:.4f}, next call est ${est:.4f})")
            if self.global_cap is not None and self.prior + self.spent + est > self.global_cap:
                raise BudgetExceeded(f"global cap ${self.global_cap:.2f} would be exceeded "
                                     f"(prior ${self.prior:.4f} + run ${self.spent:.4f} + est ${est:.4f})")

    def add(self, cost):
        with self._lock:
            self.spent += cost
            if self.ledger_path:
                os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
                with open(self.ledger_path, "w") as f:
                    json.dump({"total_usd": self.prior + self.spent}, f)


@dataclass
class Reply:
    text: str
    model: str
    tag: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    cache_write_tokens: int = 0
    reasoning_tokens: int = 0
    cost: float = 0.0
    latency: float = 0.0
    finish_reason: str = ""


def _norm_messages(messages, anthropic):
    out = []
    for m in messages:
        c = m["content"]
        if isinstance(c, str):
            out.append({"role": m["role"], "content": c})
            continue
        if not anthropic:
            out.append({"role": m["role"], "content": "".join(p["text"] for p in c)})
            continue
        parts = []
        for p in c:
            blk = {"type": "text", "text": p["text"]}
            if p.get("cache"):
                blk["cache_control"] = {"type": "ephemeral"}
            parts.append(blk)
        out.append({"role": m["role"], "content": parts})
    return out


def _flat_len(messages):
    n = 0
    for m in messages:
        c = m["content"]
        n += len(c) if isinstance(c, str) else sum(len(p["text"]) for p in c)
    return n


class BaseClient:
    """Shared guard, pricing, logging. Subclasses implement _complete()."""

    def __init__(self, guard, log_path=None, run_id="run", prices=None):
        self.guard = guard
        self.log_path = log_path
        self.run_id = run_id
        self.prices = load_prices() if prices is None else prices
        self._log_lock = threading.Lock()

    def estimate(self, model, messages, max_tokens):
        p = self.prices.get(model)
        if not p:
            return 0.0
        return (_flat_len(messages) / 3.0) * p["prompt"] + max_tokens * p["completion"]

    def chat(self, model, messages, max_tokens=300, temperature=None, tag="", reasoning=None):
        self.guard.check(self.estimate(model, messages, max_tokens))
        t0 = time.time()
        rep = self._complete(model, messages, max_tokens, temperature, tag, reasoning)
        rep.latency = time.time() - t0
        self.guard.add(rep.cost)
        self._log(rep)
        return rep

    def _cost_from_usage(self, model, usage):
        if usage.get("cost") is not None:
            return float(usage["cost"])
        p = self.prices.get(model)
        if not p:
            return 0.0
        det = usage.get("prompt_tokens_details") or {}
        cached = det.get("cached_tokens") or 0
        wr = det.get("cache_write_tokens") or 0
        fresh = max(usage.get("prompt_tokens", 0) - cached - wr, 0)
        return (fresh * p["prompt"] + cached * p.get("input_cache_read", p["prompt"])
                + wr * p.get("input_cache_write", p["prompt"])
                + usage.get("completion_tokens", 0) * p["completion"])

    def _reply_from_json(self, model, tag, j):
        usage = j.get("usage") or {}
        det = usage.get("prompt_tokens_details") or {}
        cdet = usage.get("completion_tokens_details") or {}
        ch = (j.get("choices") or [{}])[0]
        return Reply(text=(ch.get("message") or {}).get("content") or "", model=model, tag=tag,
                     prompt_tokens=usage.get("prompt_tokens", 0),
                     completion_tokens=usage.get("completion_tokens", 0),
                     cached_tokens=det.get("cached_tokens") or 0,
                     cache_write_tokens=det.get("cache_write_tokens") or 0,
                     reasoning_tokens=cdet.get("reasoning_tokens") or 0,
                     cost=self._cost_from_usage(model, usage),
                     finish_reason=ch.get("finish_reason") or "")

    def _log(self, r):
        if not self.log_path:
            return
        rec = {"ts": time.time(), "run": self.run_id, "tag": r.tag, "model": r.model,
               "prompt_tokens": r.prompt_tokens, "completion_tokens": r.completion_tokens,
               "cached_tokens": r.cached_tokens, "cache_write_tokens": r.cache_write_tokens,
               "reasoning_tokens": r.reasoning_tokens, "cost": r.cost,
               "latency_s": round(r.latency, 3), "finish": r.finish_reason}
        with self._log_lock:
            os.makedirs(os.path.dirname(os.path.abspath(self.log_path)), exist_ok=True)
            with open(self.log_path, "a") as f:
                f.write(json.dumps(rec) + "\n")

    def _complete(self, *a):
        raise NotImplementedError


class OpenRouterClient(BaseClient):
    def __init__(self, guard, log_path=None, run_id="run", prices=None, retries=6, timeout=180):
        super().__init__(guard, log_path, run_id, prices)
        self.key = os.environ.get("OPENROUTER_API_KEY")
        if not self.key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.retries, self.timeout = retries, timeout

    def _complete(self, model, messages, max_tokens, temperature, tag, reasoning):
        import requests
        body = {"model": model, "messages": _norm_messages(messages, model.startswith("anthropic/")),
                "max_tokens": max_tokens, "usage": {"include": True}}
        if temperature is not None and not model.startswith("openai/gpt-5"):
            body["temperature"] = temperature
        if reasoning is not None:
            body["reasoning"] = reasoning
        hdr = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        last = None
        for i in range(self.retries + 1):
            try:
                r = requests.post(f"{BASE_URL}/chat/completions", headers=hdr, json=body, timeout=self.timeout)
                if r.status_code in (429, 500, 502, 503, 504):
                    last = f"HTTP {r.status_code}"
                else:
                    r.raise_for_status()
                    j = r.json()
                    if "error" in j and not j.get("choices"):
                        last = f"api error: {str(j['error'])[:200]}"
                    else:
                        return self._reply_from_json(model, tag, j)
            except requests.RequestException as e:
                last = f"{type(e).__name__}: {str(e)[:200]}"
            time.sleep(min(3 * 2 ** i, 40))
        raise RuntimeError(f"OpenRouter call failed after retries: {last}")


class MockClient(BaseClient):
    """No network. fn(model, messages, tag) -> str. Fake usage from text length; optional price."""

    def __init__(self, fn, guard, log_path=None, run_id="mock", prices=None, cost_per_call=0.0):
        super().__init__(guard, log_path, run_id, prices if prices is not None else {})
        self.fn, self.cost_per_call = fn, cost_per_call
        self.calls = []

    def _complete(self, model, messages, max_tokens, temperature, tag, reasoning):
        text = self.fn(model, messages, tag)
        self.calls.append((model, tag, messages))
        pt = _flat_len(messages) // 4
        return Reply(text=text, model=model, tag=tag, prompt_tokens=pt,
                     completion_tokens=len(text) // 4, cost=self.cost_per_call, finish_reason="stop")
