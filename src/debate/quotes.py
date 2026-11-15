"""Quote extraction and verification against the passage.
Debaters wrap evidence in <quote>...</quote>. Each is checked as a normalised substring of the passage
and rewritten to <v_quote> (verified) or <u_quote> (unverified) before the judge and opponent see it.
Quote budget (word cap) is not enforced in Phase 0; see docs/07-harness-notes.md."""
import re

QUOTE_RE = re.compile(r"<quote>(.*?)</quote>", re.S | re.I)


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^a-z0-9']+", " ", s.lower())
    return " ".join(s.split())


def mark_quotes(text, passage):
    """Returns (rewritten_text, n_total, n_verified)."""
    if not passage:
        return text, 0, 0
    p = " " + norm(passage) + " "
    tot = ver = 0

    def sub(m):
        nonlocal tot, ver
        q = norm(m.group(1))
        tot += 1
        if q and (" " + q + " ") in p:
            ver += 1
            return f"<v_quote>{m.group(1).strip()}</v_quote>"
        return f"<u_quote>{m.group(1).strip()}</u_quote>"

    return QUOTE_RE.sub(sub, text), tot, ver
