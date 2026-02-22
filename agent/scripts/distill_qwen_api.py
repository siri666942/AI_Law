import os
import json
import time
import argparse
from http import HTTPStatus
from dashscope import Generation

PROMPT_TMPL = "你是一名资深律师，请根据以下案情，完成结构化法律判断：\n1. 法律关系\n2. 核心争议点\n3. 风险点\n4. 建议\n\n案情：\n{case}\n"

def read_jsonl(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items

def write_jsonl(items, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def call_api(case_text, model="qwen2.5-instruct"):
    prompt = PROMPT_TMPL.format(case=case_text)
    resp = Generation.call(model=model, prompt=prompt)
    if resp.status_code == HTTPStatus.OK:
        return resp.output_text
    else:
        raise RuntimeError(str(resp))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_jsonl", type=str, required=True)
    parser.add_argument("--output_jsonl", type=str, required=True)
    parser.add_argument("--sleep", type=float, default=0.5)
    args = parser.parse_args()
    seeds = read_jsonl(args.input_jsonl)
    out = []
    for i, s in enumerate(seeds):
        case = s.get("input") or s.get("content") or ""
        if not case:
            continue
        try:
            text = call_api(case)
            out.append({
                "instruction": "请对以下案情进行法律辅助判断",
                "input": case,
                "output": text
            })
            time.sleep(args.sleep)
        except Exception as e:
            out.append({
                "instruction": "请对以下案情进行法律辅助判断",
                "input": case,
                "output": ""
            })
    write_jsonl(out, args.output_jsonl)

if __name__ == "__main__":
    main()
