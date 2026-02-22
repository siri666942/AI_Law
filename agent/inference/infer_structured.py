import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def load_model(model_path, adapter_path=None):
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32)
    if adapter_path:
        model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()
    return tokenizer, model

def build_prompt(query, strict_json=False):
    if strict_json:
        schema = {
            "法律关系": "",
            "争议焦点": "",
            "风险点": "",
            "证据与程序注意": "",
            "处理建议": ""
        }
        schema_text = json.dumps(schema, ensure_ascii=False)
        return (
            "你是一名资深律师。请严格按以下JSON格式输出，不得包含任何多余文本：\n"
            f"{schema_text}\n"
            "案情：\n"
            f"{query}\n"
            "仅输出JSON。"
        )
    return f"你是一名资深律师，请根据以下案情，完成结构化法律判断：\n1. 法律关系\n2. 核心争议点\n3. 风险点\n4. 建议\n\n案情：\n{query}\n"

def generate(tokenizer, model, prompt, max_new_tokens=256, temperature=0.7, top_p=0.9, bad_words=None):
    inputs = tokenizer(prompt, return_tensors="pt")
    bad_words_ids = None
    if bad_words:
        bad_words_ids = [tokenizer(bw, add_special_tokens=False).input_ids for bw in bad_words]
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            eos_token_id=tokenizer.eos_token_id,
            bad_words_ids=bad_words_ids,
        )
    return tokenizer.decode(out[0], skip_special_tokens=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_path", type=str, default="")
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--strict_json", action="store_true")
    args = parser.parse_args()
    tokenizer, model = load_model(args.model_path, args.adapter_path or None)
    prompt = build_prompt(args.query, strict_json=args.strict_json)
    bad_words = ["Human:", "Assistant:", "A.", "B.", "C.", "D.", "问题：", "答案：", "解析："]
    text = generate(tokenizer, model, prompt, bad_words=bad_words)
    print(text)

if __name__ == "__main__":
    main()
