"""Run a protocol over sampled questions with side swap; append records to JSONL (resumable)."""
import json, os
from concurrent.futures import ThreadPoolExecutor
from .data import make_instances
from .protocols import PROTOCOLS


def done_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        return {json.loads(l)["iid"] for l in f if l.strip() and not json.loads(l).get("error")}


def run(questions, protocol, client, cfg, out_path, seed=0, workers=1, swap=True):
    fn = PROTOCOLS[protocol]
    insts = [i for q in questions for i in make_instances(q, seed, swap)]
    skip = done_ids(out_path)
    insts = [i for i in insts if i.iid not in skip]
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    def one(inst):
        try:
            return fn(inst, client, cfg)
        except RuntimeError as e:
            from .client import BudgetExceeded
            if isinstance(e, BudgetExceeded):
                raise
            return {"iid": inst.iid, "qid": inst.qid, "protocol": protocol, "error": str(e)[:300]}

    recs = []
    with ThreadPoolExecutor(max_workers=workers) as ex, open(out_path, "a") as f:
        futs = [ex.submit(one, i) for i in insts]
        try:
            for fu in futs:
                r = fu.result()
                f.write(json.dumps(r) + "\n")
                f.flush()
                recs.append(r)
        except BaseException:
            for fu in futs:
                fu.cancel()
            raise
    return recs
