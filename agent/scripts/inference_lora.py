import os
import json
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re

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

LABELS = ["【法律关系】", "【核心争议点】", "【风险点】", "【建议】"]

def has_all_labels(text):
    flags = {lab: (lab in text) for lab in LABELS}
    return flags, all(flags.values())

def read_jsonl(path, limit=None):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
            if limit is not None and len(items) >= limit:
                break
    return items

def gen_structured(tokenizer, model, case, max_new_tokens=512):
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
    gen_ids = out[0][input_len:]
    return tokenizer.decode(gen_ids, skip_special_tokens=True)

def clean_structured(text):
    # remove text after ---
    if "---" in text:
        text = text.split("---")[0]

    t = text.strip()
    
    # Define labels and their standard order
    labels = ["【法律关系】", "【核心争议点】", "【风险点】", "【建议】"]
    
    # Extract all occurrences of each section
    sections_found = {}
    for i, label in enumerate(labels):
        # Find all occurrences of this label
        matches = list(re.finditer(re.escape(label), t))
        if not matches:
            continue
            
        # For each occurrence, find where it ends (at the next label or end of string)
        for match in matches:
            start_pos = match.start()
            # Find the nearest next label (any label)
            next_label_pos = len(t)
            for other_label in labels:
                other_match = re.search(re.escape(other_label), t[match.end():])
                if other_match:
                    pos = match.end() + other_match.start()
                    if pos < next_label_pos:
                        next_label_pos = pos
            
            content = t[start_pos:next_label_pos].strip()
            # If it's just the label, skip
            if content.strip() == label.strip():
                continue
                
            # Keep the longest content for each label if duplicates found
            if label not in sections_found or len(content) > len(sections_found[label]):
                sections_found[label] = content

    # Construct the final text in standard order
    parts = []
    for label in labels:
        if label in sections_found:
            parts.append(sections_found[label])
    
    if parts:
        return "\n\n".join(parts)
    
    # Fallback to original if no structured sections found
    return t if len(t) > 20 else text.strip()

def load_model(base_model, adapter_dir, device="cpu"):
    tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(base_model)
    model = PeftModel.from_pretrained(model, adapter_dir)
    if device == "cpu":
        model.to("cpu")
        model.eval()
    return tokenizer, model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_dir", type=str, required=True)
    parser.add_argument("--input_text", type=str)
    parser.add_argument("--input_jsonl", type=str)
    parser.add_argument("--output_jsonl", type=str)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--max_new_tokens", type=int, default=512)
    args = parser.parse_args()

    tokenizer, model = load_model(args.base_model, args.adapter_dir, args.device)

    if args.input_text:
        pred = gen_structured(tokenizer, model, args.input_text, args.max_new_tokens)
        pred = clean_structured(pred)
        print(pred)
        return

    if args.input_jsonl and args.output_jsonl:
        items = read_jsonl(args.input_jsonl, limit=args.limit)
        os.makedirs(os.path.dirname(args.output_jsonl), exist_ok=True)
        with open(args.output_jsonl, "w", encoding="utf-8") as f:
            for i, it in enumerate(items):
                case = it.get("input") or it.get("content") or ""
                if not case:
                    continue
                pred = gen_structured(tokenizer, model, case, args.max_new_tokens)
                pred = clean_structured(pred)
                flags, ok = has_all_labels(pred)
                rec = {
                    "id": it.get("id", f"sample_{i}"),
                    "input": case,
                    "prediction": pred,
                    "labels_ok": ok,
                    "labels": flags
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                print(f"[inference] {i+1}/{len(items)} labels_ok={ok}", flush=True)
        print(f"已写入预测到: {args.output_jsonl}")
        return

    print("必须提供 --input_text 或 (--input_jsonl 与 --output_jsonl)")

if __name__ == "__main__":
    main()
