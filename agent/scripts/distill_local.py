import os
import json
import argparse
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

PROMPT_TMPL = """你是一名资深律师，请根据以下案情，完成结构化法律判断。
请严格按照以下格式输出：
【法律关系】
...
【核心争议点】
...
【风险点】
...
【建议】
...

案情：
{case}
"""

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

def gen_case(tokenizer, model, case, max_new_tokens=1024):
    prompt = PROMPT_TMPL.format(case=case)
    inputs = tokenizer(prompt, return_tensors="pt")
    input_len = inputs.input_ids.shape[1]
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id,
        )
    # Only decode the new tokens
    generated_ids = out[0][input_len:]
    return tokenizer.decode(generated_ids, skip_special_tokens=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_jsonl", type=str, required=True)
    parser.add_argument("--output_jsonl", type=str, required=True)
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--stream_write", action="store_true")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, use_fast=False)
    # Fix deprecated torch_dtype to dtype
    model = AutoModelForCausalLM.from_pretrained(args.model_path, dtype=torch.float32)
    model.eval()
    seeds = read_jsonl(args.input_jsonl)
    
    processed_count = 0
    if args.stream_write and os.path.exists(args.output_jsonl):
        with open(args.output_jsonl, "r", encoding="utf-8") as f:
            processed_count = sum(1 for _ in f)
    
    if processed_count > 0:
        print(f"Found {processed_count} existing entries. Skipping...")
        seeds = seeds[processed_count:]

    if args.stream_write:
        os.makedirs(os.path.dirname(args.output_jsonl), exist_ok=True)
        # Use tqdm for progress bar
        with open(args.output_jsonl, "a", encoding="utf-8") as f:
            for idx, s in enumerate(tqdm(seeds, desc="Distilling (Stream)")):
                case = s.get("input") or s.get("content") or ""
                if not case:
                    continue
                text = gen_case(tokenizer, model, case)
                rec = {
                    "instruction": "请对以下案情进行法律辅助判断",
                    "input": case,
                    "output": text
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
    else:
        out = []
        for idx, s in enumerate(tqdm(seeds, desc="Distilling")):
            case = s.get("input") or s.get("content") or ""
            if not case:
                continue
            text = gen_case(tokenizer, model, case)
            out.append({
                "instruction": "请对以下案情进行法律辅助判断",
                "input": case,
                "output": text
            })
        write_jsonl(out, args.output_jsonl)

if __name__ == "__main__":
    main()
