import json, os, random
import pytest
from debate import data, protocols, scoring
from debate.client import BudgetGuard, BudgetExceeded, MockClient, _norm_messages
from debate.judge import parse_verdict
from debate.quotes import mark_quotes
from debate import runner

PASSAGE = "The old man walked slowly to the harbor. He had not seen the sea in twenty years."


def mkq(i, passage=PASSAGE):
    return data.Question(f"q{i}", "quality", f"Question {i}?", ["gold", "wrong", "x", "y"], 0, 1, passage)


def fake(model, messages, tag):
    if "judge" in tag and tag != "judge_question":
        return "Verdict: A\nConfidence: 80"
    if tag == "judge_question":
        return "Why?"
    return 'My point: <quote>walked slowly to the harbor</quote> and <quote>invented text</quote>.'


def client(cost=0.0, cap=10, log=None):
    return MockClient(fake, BudgetGuard(cap), log_path=log, cost_per_call=cost)


def test_sampler_fixed_seed_and_order_independent():
    qs = [mkq(i) for i in range(50)]
    a = [q.qid for q in data.sample_questions(qs, 10, 7)]
    b = [q.qid for q in data.sample_questions(list(reversed(qs)), 10, 7)]
    c = [q.qid for q in data.sample_questions(qs, 10, 8)]
    assert a == b and a != c and len(set(a)) == 10


def test_side_swap_and_shuffle_balanced():
    firsts = []
    for i in range(200):
        q = mkq(i)
        i0, i1 = data.make_instances(q, 0)
        assert i0.correct != i1.correct                      # side swap
        assert i0.answers[0 if i0.correct == "A" else 1] == "gold"
        assert i1.answers[0 if i1.correct == "A" else 1] == "gold"
        assert i0.assigned == i0.correct and i1.assigned != i1.correct
        firsts.append(i0.correct)
        assert data.make_instances(q, 0)[0] == i0             # deterministic
    assert 70 < firsts.count("A") < 130                       # shuffled


def test_parse_quality_hard_subset(tmp_path):
    def qq(diff, best):
        return {"question": "q", "options": ["a", "b", "c", "d"], "gold_label": 2, "writer_label": 2,
                "difficult": diff, "validation": [{"untimed_best_distractor": best}] * 3, "speed_validation": []}
    art = {"article_id": "1", "set_unique_id": "s1", "title": "T", "article": "text", "questions": [qq(1, 4), qq(0, 1)]}
    p = tmp_path / "d.jsonl"
    p.write_text(json.dumps(art) + "\n")
    qs = data.parse_quality(str(p))
    assert len(qs) == 1 and qs[0].gold == 1 and qs[0].distractor == 3
    assert len(data.parse_quality(str(p), hard_only=False)) == 2


def test_gpqa_stub_raises():
    with pytest.raises(NotImplementedError):
        data.load_gpqa("/nonexistent.csv")


def test_quote_verification():
    t, n, v = mark_quotes("see <quote>Walked, slowly to the HARBOR</quote> and <quote>nope</quote>", PASSAGE)
    assert (n, v) == (2, 1)
    assert "<v_quote>" in t and "<u_quote>nope</u_quote>" in t
    assert mark_quotes("<quote>x</quote>", "") == ("<quote>x</quote>", 0, 0)


def test_parse_verdict():
    assert parse_verdict("Verdict: B\nConfidence: 72") == ("B", 0.72)
    assert parse_verdict("**Verdict:** A\n**Confidence:** 90%") == ("A", 0.9)
    assert parse_verdict("Verdict: A\nConfidence: 20")[1] == 0.5
    assert parse_verdict("no idea") == (None, None)


def test_cache_blocks_only_for_anthropic():
    m = [{"role": "user", "content": [{"text": "a", "cache": True}, {"text": "b"}]}]
    an = _norm_messages(m, True)[0]["content"]
    assert an[0]["cache_control"] == {"type": "ephemeral"} and "cache_control" not in an[1]
    assert _norm_messages(m, False)[0]["content"] == "ab"


@pytest.mark.parametrize("proto,calls", [("standard", 7), ("consultancy", 3 + 2 + 1), ("critique", 3),
                                         ("cross-exam", 6 + 4 + 1), ("blind", 1)])
def test_protocol_call_counts(proto, calls):
    c = client()
    inst = data.make_instances(mkq(0), 0)[0]
    rec = protocols.PROTOCOLS[proto](inst, c, protocols.Config(rounds=3 if proto != "critique" else 1))
    assert rec["n_calls"] == calls == len(c.calls)
    assert rec["verdict"] == "A" and rec["judge_correct"] == (inst.correct == "A")
    if proto == "blind":
        assert "Transcript" not in c.calls[0][2][1]["content"]


def test_standard_quote_stats_and_marking_reach_judge():
    c = client()
    rec = protocols.standard(data.make_instances(mkq(0), 0)[0], c, protocols.Config(rounds=3))
    assert rec["quotes_total"] == 12 and rec["quotes_verified"] == 6
    judge_prompt = c.calls[-1][2][1]["content"]
    assert "<v_quote>" in judge_prompt and "<u_quote>" in judge_prompt


def test_judge_interaction_and_concede():
    c = client()
    cfg = protocols.Config(rounds=2, judge_interaction=True)
    rec = protocols.standard(data.make_instances(mkq(0), 0)[0], c, cfg)
    assert rec["n_calls"] == 4 + 4 + 1                        # 2 rounds x2 + (1 interaction: 2 q + 2 a) + verdict
    n = []
    def conc(model, messages, tag):
        n.append(tag)
        return "CONCEDE I was wrong" if tag == "debater_B" else fake(model, messages, tag)
    c2 = MockClient(conc, BudgetGuard(10))
    rec = protocols.standard(data.make_instances(mkq(0), 0)[0], c2, protocols.Config(rounds=3, concede=True))
    assert rec["conceded"] == "B" and rec["n_calls"] == 3


def test_cache_prefix_identical_across_sides():
    c = client()
    protocols.standard(data.make_instances(mkq(0), 0)[0], c, protocols.Config(rounds=1))
    a, b = c.calls[0][2], c.calls[1][2]
    assert a[0] == b[0] and a[1]["content"][0] == b[1]["content"][0]


def test_budget_guard_aborts(tmp_path):
    c = MockClient(fake, BudgetGuard(0.25), cost_per_call=0.1)
    with pytest.raises(BudgetExceeded):
        protocols.standard(data.make_instances(mkq(0), 0)[0], c, protocols.Config(rounds=3))
    assert len(c.calls) == 3 and c.guard.spent == pytest.approx(0.3)  # overshoot bounded by one call (est covers it for real models)


def test_global_cap_ledger(tmp_path):
    led = str(tmp_path / "l.json")
    g = BudgetGuard(5, 0.3, led)
    c = MockClient(fake, g, cost_per_call=0.1)
    for _ in range(3):
        c.chat("m", [{"role": "user", "content": "x"}])
    with pytest.raises(BudgetExceeded):
        c.chat("m", [{"role": "user", "content": "x"}])
    assert BudgetGuard(5, 0.3, led).prior == pytest.approx(0.3)     # persisted across runs
    with pytest.raises(BudgetExceeded):
        MockClient(fake, BudgetGuard(5, 0.3, led)).chat("m", [{"role": "user", "content": "x"}])


def test_pre_call_estimate_blocks():
    prices = {"m": {"prompt": 1e-6, "completion": 1e-3}}
    c = MockClient(fake, BudgetGuard(0.01), prices=prices)
    with pytest.raises(BudgetExceeded):
        c.chat("m", [{"role": "user", "content": "x"}], max_tokens=300)  # est 0.3 > 0.01
    assert not c.calls


def test_call_log_jsonl(tmp_path):
    log = str(tmp_path / "calls.jsonl")
    c = client(cost=0.01, log=log)
    protocols.critique_only(data.make_instances(mkq(0), 0)[0], c, protocols.Config(rounds=1))
    rows = [json.loads(l) for l in open(log)]
    assert len(rows) == 3
    for k in ("model", "prompt_tokens", "completion_tokens", "cached_tokens", "cost", "latency_s"):
        assert k in rows[0]


def test_runner_resume_and_scoring(tmp_path):
    out = str(tmp_path / "r.jsonl")
    qs = [mkq(i) for i in range(6)]
    recs = runner.run(qs, "standard", client(), protocols.Config(rounds=1), out, seed=1)
    assert len(recs) == 12
    assert runner.run(qs, "standard", client(), protocols.Config(rounds=1), out, seed=1) == []   # resume
    recs2 = runner.run(qs, "critique", client(), protocols.Config(rounds=1), str(tmp_path / "c.jsonl"), seed=1)
    res = scoring.score({"s": scoring.load(out), "c": recs2}, [("s", "c")], n_boot=500)
    assert res["runs"]["s"]["accuracy"] == pytest.approx(0.5)     # judge always says A, correct is A half the time
    assert res["runs"]["s"]["quote_verification_rate"] == pytest.approx(0.5)
    cmp = res["comparisons"][0]
    assert cmp["n"] == 6 and cmp["lo"] <= cmp["diff"] <= cmp["hi"]
    assert "95% CI" in scoring.markdown(res)


def test_paired_bootstrap_detects_shift():
    a = {f"q{i}": 1.0 for i in range(40)}
    b = {f"q{i}": 0.5 for i in range(40)}
    r = scoring.paired_bootstrap(a, b, n=1000)
    assert r["diff"] == pytest.approx(0.5) and r["lo"] > 0
