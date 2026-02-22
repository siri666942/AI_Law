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

def generate(tokenizer, model, prompt, max_new_tokens=256, temperature=0.7, top_p=0.9):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            eos_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2-1.5B-Instruct")
    parser.add_argument("--adapter_path", type=str, default="")
    parser.add_argument("--query", type=str, default="被告人盗窃价值5000元手机，应如何定罪量刑？")
    args = parser.parse_args()
    tokenizer, model = load_model(args.model_path, args.adapter_path or None)
    prompt = f"指令：请进行法律分析并给出结论\n输入：{args.query}\n输出："
    text = generate(tokenizer, model, prompt)
    print(text)

if __name__ == "__main__":
    main()
