import json
import os
import argparse

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def to_instruction_format(items):
    out = []
    for x in items:
        ins = x.get("instruction") or "请根据案情进行法律分析并给出结论"
        inp = x.get("input") or x.get("facts") or ""
        outp = x.get("output") or x.get("judgment") or ""
        if inp and outp:
            out.append({"instruction": ins, "input": inp, "output": outp})
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    data = load_json(args.input)
    converted = to_instruction_format(data)
    save_json(converted, args.output)

if __name__ == "__main__":
    main()
