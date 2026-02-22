import os
import json
import argparse
import re


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def clean_text(text):
    text = text.replace("\u3000", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_fact_section(text, max_len=800):
    t = text
    t = re.sub(r"\s+", " ", t)
    start_idx = 0
    m = re.search(r"(基本事实|案件事实|案件基本情况|事实如下)", t)
    if m:
        start_idx = m.start()
    end_idx = len(t)
    m2 = re.search(r"(本院认为|裁判理由|本院分析|综上所述)", t)
    if m2 and m2.start() > start_idx:
        end_idx = m2.start()
    seg = t[start_idx:end_idx].strip()
    if not seg:
        seg = t
    if len(seg) > max_len:
        seg = seg[:max_len]
    return seg.strip()


def build_seed_from_dir(src_dir, out_path, category="enterprise_loan"):
    items = []
    for name in os.listdir(src_dir):
        if not name.lower().endswith(".txt"):
            continue
        full = os.path.join(src_dir, name)
        raw = read_text(full)
        cleaned = clean_text(raw)
        fact = extract_fact_section(cleaned)
        if not fact:
            continue
        items.append({
            "id": os.path.splitext(name)[0],
            "category": category,
            "input": fact
        })
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_dir", type=str, required=True)
    parser.add_argument("--out_jsonl", type=str, required=True)
    parser.add_argument("--category", type=str, default="enterprise_loan")
    args = parser.parse_args()
    build_seed_from_dir(args.src_dir, args.out_jsonl, args.category)


if __name__ == "__main__":
    main()

