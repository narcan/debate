"""Weak judge: verdict plus confidence. Blind mode shows no transcript."""
import re
from . import prompts


def parse_verdict(text):
    """Returns (verdict 'A'|'B'|None, confidence in [0.5, 1.0] or None)."""
    v = re.search(r"verdict\s*[:\-]?\s*\**\s*(?:answer\s*)?\(?([AB])\b", text, re.I)
    c = re.search(r"confidence\s*[:\-]?\s*\**\s*(\d+(?:\.\d+)?)\s*%?", text, re.I)
    conf = None
    if c:
        x = float(c.group(1))
        x = x / 100.0 if x > 1.0 else x
        conf = min(max(x, 0.5), 1.0)
    return (v.group(1).upper() if v else None), conf


def judge_messages(question, answers, transcript=None, note=""):
    body = f"Question: {question}\n\nAnswer A: {answers[0]}\nAnswer B: {answers[1]}\n"
    if transcript is None:
        body += "\nNo debate is available. Decide using your own knowledge and reasoning."
    else:
        body += f"\n{note}Transcript:\n{transcript}\n\nWhich answer is correct?"
    return [{"role": "system", "content": prompts.JUDGE_SYS}, {"role": "user", "content": body}]


def run_judge(client, model, question, answers, transcript, max_tokens, reasoning, tag="judge", note=""):
    """transcript None = blind judge. Returns (verdict, confidence, Reply)."""
    rep = client.chat(model, judge_messages(question, answers, transcript, note), max_tokens=max_tokens,
                      temperature=0.0, tag=tag, reasoning=reasoning)
    v, c = parse_verdict(rep.text)
    return v, c, rep
