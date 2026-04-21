import argparse
import json
import re

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def clean_text(t):
    t = re.sub(r"\s+", " ", t or "")
    return t.strip()

def split_output(text):
    idx = text.find("判决")
    if idx == -1:
        idx = text.find("裁判")
    if idx == -1:
        return "", ""
    fact = clean_text(text[:idx])
    judgment = clean_text(text[idx:])
    return fact, judgment

def build(items):
    out = []
    for it in items:
        c = it.get("content", "")
        if not c:
            continue
        fact, judgment = split_output(c)
        if not fact or not judgment:
            continue
        out.append({
            "instruction": "请根据案情进行法律分析并给出结论",
            "input": fact,
            "output": judgment
        })
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    items = load_json(args.input)
    ds = build(items)
    save_json(ds, args.output)

if __name__ == "__main__":
    main()
