import argparse
import json
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

LABELS = ["法律关系", "争议焦点", "风险点", "证据与程序注意", "处理建议"]

def load_kb(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def retrieve(kb, query, top_k=3):
    corpus = [x["title"] + " " + x["content"] for x in kb]
    vec = TfidfVectorizer(analyzer="char", ngram_range=(2,4), max_features=10000)
    X = vec.fit_transform(corpus)
    q = vec.transform([query])
    sims = cosine_similarity(q, X)[0]
    idxs = sims.argsort()[::-1][:top_k]
    out = []
    for i in idxs:
        it = dict(kb[i])
        it["score"] = float(sims[i])
        out.append(it)
    return out

def retrieve_by_labels(kb, query, labels=LABELS, top_k=2):
    res = {}
    for lab in labels:
        q = lab + " " + query
        res[lab] = retrieve(kb, q, top_k=top_k)
    return res

def build_kb_text_by_labels(label_articles):
    parts = []
    for lab, arts in label_articles.items():
        seg = []
        for a in arts:
            seg.append(f"{a['title']}：{a['content']}")
        parts.append(f"{lab}：\n" + "\n".join(seg))
    return "\n".join(parts)

def load_model(model_path, adapter_path=None):
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32)
    if adapter_path:
        model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()
    return tokenizer, model

def build_prompt(query, labels=LABELS, kb_text=None, strict_json=False):
    label_lines = "\n".join([f"{i+1}. {lab}" for i, lab in enumerate(labels)])
    kb_block = f"\n参考知识：\n{kb_text}\n" if kb_text else "\n"
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
            "你是一名资深律师。请严格按以下JSON格式输出，不得包含任何多余文本，"
            "不得输出题目、选项、问答、医学内容或与案情无关的内容：\n"
            f"{schema_text}\n"
            f"{kb_block}"
            "案情：\n"
            f"{query}\n"
            "仅输出JSON，不要解释。"
        )
    return f"你是一名资深律师，请根据以下案情，完成结构化法律判断：\n{label_lines}\n{kb_block}\n案情：\n{query}\n"

def generate(tokenizer, model, prompt, max_new_tokens=512, temperature=0.7, top_p=0.9, bad_words=None):
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

def enforce_structure(text, labels=LABELS):
    # 如果模型未严格分段，简单正则切分并补齐标签标题
    result = {}
    for lab in labels:
        m = re.search(lab + r"[：:]\s*(.*?)(?=\n[^\n]*：|$)", text, flags=re.S)
        if m:
            result[lab] = m.group(1).strip()
        else:
            # 退化：尝试按顺序近似分段
            result[lab] = ""
    return result, text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_path", type=str, default="")
    parser.add_argument("--kb_path", type=str, default="")
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--use_rag", action="store_true")
    parser.add_argument("--strict_json", action="store_true")
    parser.add_argument("--rag_by_label", action="store_true")
    args = parser.parse_args()
    kb_text = None
    if args.use_rag and args.kb_path:
        kb = load_kb(args.kb_path)
        if args.rag_by_label:
            la = retrieve_by_labels(kb, args.query, LABELS, top_k=2)
            kb_text = build_kb_text_by_labels(la)
        else:
            articles = retrieve(kb, args.query, top_k=3)
            kb_text = "\n".join([f"{a['title']}：{a['content']}" for a in articles])
    tokenizer, model = load_model(args.model_path, args.adapter_path or None)
    prompt = build_prompt(args.query, LABELS, kb_text, strict_json=args.strict_json)
    bad_words = ["Human:", "Assistant:", "A.", "B.", "C.", "D.", "问题：", "答案：", "解析："]
    text = generate(tokenizer, model, prompt, bad_words=bad_words)
    if args.strict_json:
        m = re.search(r"\{[\s\S]*\}", text)
        structured = {}
        raw = text
        if m:
            try:
                obj = json.loads(m.group(0))
                for lab in LABELS:
                    structured[lab] = obj.get(lab, "")
            except Exception:
                structured, raw = enforce_structure(text, LABELS)
        else:
            structured, raw = enforce_structure(text, LABELS)
        print("RAW_OUTPUT_BEGIN")
        print(raw)
        print("RAW_OUTPUT_END")
        print("STRUCTURED_JSON_BEGIN")
        print(json.dumps(structured, ensure_ascii=False, indent=2))
        print("STRUCTURED_JSON_END")
        return
    structured, raw = enforce_structure(text, LABELS)
    print("RAW_OUTPUT_BEGIN")
    print(raw)
    print("RAW_OUTPUT_END")
    print("STRUCTURED_JSON_BEGIN")
    print(json.dumps(structured, ensure_ascii=False, indent=2))
    print("STRUCTURED_JSON_END")

if __name__ == "__main__":
    main()
