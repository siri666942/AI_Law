import argparse
import json
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def load_kb(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def retrieve(kb, query, top_k=3):
    corpus = [x["title"] + " " + x["content"] for x in kb]
    vec = TfidfVectorizer(max_features=5000)
    X = vec.fit_transform(corpus)
    q = vec.transform([query])
    sims = cosine_similarity(q, X)[0]
    idxs = sims.argsort()[::-1][:top_k]
    return [kb[i] for i in idxs]

def load_model(model_path, adapter_path=None):
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32)
    if adapter_path:
        model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()
    return tokenizer, model

def build_prompt(query, articles):
    kb_text = "\n".join([f"{a['title']}：{a['content']}" for a in articles])
    return f"指令：参考以下法律条文与知识进行分析，并给出结论\n知识：\n{kb_text}\n输入：{query}\n输出："

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
    return tokenizer.decode(out[0], skip_special_tokens=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_path", type=str, default="")
    parser.add_argument("--kb_path", type=str, default="data/knowledge/legal_articles.json")
    parser.add_argument("--query", type=str, default="被告人盗窃价值5000元手机，应如何定罪量刑？")
    args = parser.parse_args()
    kb = load_kb(args.kb_path)
    articles = retrieve(kb, args.query, top_k=3)
    tokenizer, model = load_model(args.model_path, args.adapter_path or None)
    prompt = build_prompt(args.query, articles)
    text = generate(tokenizer, model, prompt)
    print(text)

if __name__ == "__main__":
    main()
