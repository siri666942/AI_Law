import json
import argparse
import re
from collections import Counter

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def tokenize(text):
    text = re.sub(r"\s+", " ", text.strip())
    return [t for t in re.split(r"[\\s，。；：、,.!?]", text) if t]

def f1_overlap(pred, ref):
    p = Counter(tokenize(pred))
    r = Counter(tokenize(ref))
    inter = sum((p & r).values())
    p_sum = sum(p.values())
    r_sum = sum(r.values())
    if p_sum == 0 or r_sum == 0:
        return 0.0, 0.0, 0.0
    precision = inter / p_sum
    recall = inter / r_sum
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1

def eval_items(pred_items, ref_items):
    ref_map = {x.get("id", i): x for i, x in enumerate(ref_items)}
    totals = {"precision": 0.0, "recall": 0.0, "f1": 0.0, "count": 0}
    for i, p in enumerate(pred_items):
        pid = p.get("id", i)
        ref = ref_map.get(pid)
        if not ref:
            continue
        pr, rc, f1 = f1_overlap(p.get("output", ""), ref.get("output", ""))
        totals["precision"] += pr
        totals["recall"] += rc
        totals["f1"] += f1
        totals["count"] += 1
    if totals["count"] == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "count": 0}
    return {
        "precision": totals["precision"] / totals["count"],
        "recall": totals["recall"] / totals["count"],
        "f1": totals["f1"] / totals["count"],
        "count": totals["count"],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", type=str, required=True)
    parser.add_argument("--ref", type=str, required=True)
    args = parser.parse_args()
    preds = load_json(args.pred)
    refs = load_json(args.ref)
    report = eval_items(preds, refs)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
