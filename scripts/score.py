#!/usr/bin/env python3
"""Score runs. Usage: score.py --run standard=results/std.jsonl --run critique=results/crit.jsonl
   --compare standard critique --out results/score"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from debate import scoring

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", required=True, help="name=path.jsonl")
    ap.add_argument("--compare", nargs=2, action="append", default=[], metavar=("A", "B"))
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None, help="prefix; writes .json and .md")
    a = ap.parse_args()
    runs = {}
    for r in a.run:
        name, path = r.split("=", 1)
        runs[name] = scoring.load(path)
    res = scoring.score(runs, [tuple(c) for c in a.compare], a.boot, a.seed)
    md = scoring.markdown(res)
    print(md)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(res, open(a.out + ".json", "w"), indent=1)
        open(a.out + ".md", "w").write(md)

if __name__ == "__main__":
    main()
