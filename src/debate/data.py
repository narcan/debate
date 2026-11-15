"""Datasets, seeded sampling, side swap and answer-order shuffle.

QuALITY hard subset: dev split, questions with difficult==1 (<50% of speed annotators correct).
Binary task: gold answer vs the best distractor (majority of validators' untimed_best_distractor).
Note: QuALITY options are fetched from raw.githubusercontent.com (the github.com/raw path is blocked
by the agent proxy in this environment).
"""
import csv, json, os, random, re, zlib
from collections import Counter
from dataclasses import dataclass, field, asdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
CACHE = os.path.join(ROOT, "data", "cache")
QUALITY_URL = "https://raw.githubusercontent.com/nyu-mll/quality/main/data/v1.0.1/QuALITY.v1.0.1.htmlstripped.{split}"


@dataclass
class Question:
    qid: str
    dataset: str
    question: str
    choices: list
    gold: int            # 0-indexed into choices
    distractor: int      # 0-indexed, the wrong answer used as the opponent
    passage: str = ""
    meta: dict = field(default_factory=dict)


@dataclass
class Instance:
    """One debate setup. answers[0] is labelled A, answers[1] B. correct is 'A' or 'B'.
    assigned: the label a one-sided protocol (consultancy, critique-only) defends."""
    qid: str
    dataset: str
    variant: int         # 0 or 1; variant 1 is the side swap of variant 0
    question: str
    answers: list
    correct: str
    assigned: str
    passage: str = ""

    @property
    def iid(self):
        return f"{self.qid}#{self.variant}"


def _seed(*parts):
    return zlib.crc32("|".join(map(str, parts)).encode())


def fetch_quality(split="dev"):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"quality_{split}.jsonl")
    if not os.path.exists(path):
        import requests
        r = requests.get(QUALITY_URL.format(split=split), timeout=120)
        r.raise_for_status()
        text = r.text.replace(" ", "").replace(" ", "").replace("\xa0", " ")
        with open(path, "w") as f:
            f.write(text)
    return path


def parse_quality(path, hard_only=True, seed=0):
    out = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            art = json.loads(line)
            for qi, q in enumerate(art["questions"]):
                if hard_only and not q.get("difficult"):
                    continue
                gold = q["gold_label"] - 1
                votes = Counter(v["untimed_best_distractor"] - 1 for v in q.get("validation", [])
                                if v.get("untimed_best_distractor") and v["untimed_best_distractor"] - 1 != gold)
                if votes:
                    top = max(votes.values())
                    dist = min(k for k, v in votes.items() if v == top)
                else:
                    rng = random.Random(_seed(seed, art["set_unique_id"], qi))
                    dist = rng.choice([i for i in range(len(q["options"])) if i != gold])
                out.append(Question(qid=f"quality-{art['set_unique_id']}-{qi}", dataset="quality",
                                    question=q["question"], choices=q["options"], gold=gold,
                                    distractor=dist, passage=art["article"].strip(),
                                    meta={"title": art["title"], "article_id": art["article_id"]}))
    out.sort(key=lambda x: x.qid)
    return out


def load_quality(split="dev", hard_only=True, seed=0):
    return parse_quality(fetch_quality(split), hard_only, seed)


def load_gpqa(csv_path=None, seed=0):
    """Stub. GPQA is gated (HF Idavidrein/gpqa). Pass a local CSV of gpqa_diamond.csv you downloaded
    yourself with your own HF access. Never commit or post its contents. No passage, so no quotes."""
    csv_path = csv_path or os.environ.get("GPQA_CSV")
    if not csv_path or not os.path.exists(csv_path):
        raise NotImplementedError("GPQA not loaded: set GPQA_CSV or pass csv_path to a local gpqa_diamond.csv")
    out = []
    with open(csv_path, newline="") as f:
        for i, row in enumerate(csv.DictReader(f)):
            wrong = [row[f"Incorrect Answer {k}"] for k in (1, 2, 3)]
            rng = random.Random(_seed(seed, row.get("Record ID", i)))
            d = rng.randrange(3)
            out.append(Question(qid=f"gpqa-{row.get('Record ID', i)}", dataset="gpqa", question=row["Question"],
                                choices=[row["Correct Answer"]] + wrong, gold=0, distractor=1 + d))
    out.sort(key=lambda x: x.qid)
    return out


def sample_questions(questions, n, seed):
    """Fixed-seed sample without replacement, independent of input order."""
    qs = sorted(questions, key=lambda q: q.qid)
    rng = random.Random(seed)
    return rng.sample(qs, min(n, len(qs)))


def make_instances(q, seed, swap=True):
    """Two instances per question. Answer order (which answer is labelled A) is shuffled per question
    by seed; variant 1 flips it (side swap), so each answer is defended by both A and B across variants.
    One-sided protocols: variant 0 defends the correct answer, variant 1 the incorrect one,
    always at the same label."""
    rng = random.Random(_seed(seed, q.qid))
    c0 = rng.choice("AB")
    gold_t, dist_t = q.choices[q.gold], q.choices[q.distractor]
    insts = []
    for v in (0, 1) if swap else (0,):
        correct = c0 if v == 0 else ("B" if c0 == "A" else "A")
        answers = [gold_t, dist_t] if correct == "A" else [dist_t, gold_t]
        assigned = correct if v == 0 else ("B" if correct == "A" else "A")
        insts.append(Instance(q.qid, q.dataset, v, q.question, answers, correct, assigned, q.passage))
    return insts
