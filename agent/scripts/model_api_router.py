import os
import json
import argparse
import re
from http import HTTPStatus
from dashscope import Generation
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import structured_pipeline as sp

def resolve_kb_path(kb):
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "knowledge")
    if kb == "civil":
        return os.path.join(base, "civil_code.json")
    if kb == "contract":
        return os.path.join(base, "legal_articles.json")
    if kb == "procedure":
        return os.path.join(base, "legal_articles.json")
    return os.path.join(base, "legal_articles.json")

def parse_structured(text):
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
        out = {}
        for lab in sp.LABELS:
            out[lab] = obj.get(lab, "")
        return out
    except Exception:
        return None

def call_api_fallback(case_text, kb_text, provider="dashscope", model="qwen2.5-instruct"):
    prompt = "你是一名资深律师。参考以下知识完成结构化法律判断，严格输出JSON。\n知识：\n" + kb_text + "\n案情：\n" + case_text + "\n仅输出JSON。"
    if provider == "dashscope":
        try:
            resp = Generation.call(model=model, prompt=prompt)
            if resp.status_code == HTTPStatus.OK:
                return resp.output_text
            else:
                return ""
        except Exception:
            return ""
    return ""

def route(query, task, kb, model_path, adapter_path, strict_json, fallback_api, threshold, dry_run=False):
    kb_path = resolve_kb_path(kb)
    kb_data = sp.load_kb(kb_path)
    label_articles = sp.retrieve_by_labels(kb_data, query, sp.LABELS, top_k=2)
    scores = []
    for lab, arts in label_articles.items():
        for a in arts:
            scores.append(a.get("score", 0.0))
    max_score = max(scores) if scores else 0.0
    kb_text = sp.build_kb_text_by_labels(label_articles)
    if dry_run:
        return {
            "route": "student" if max_score >= threshold else "api_fallback",
            "max_score": max_score,
            "kb_path": kb_path,
            "kb_text_len": len(kb_text)
        }
    tokenizer, model = sp.load_model(model_path, adapter_path or None)
    bad_words = ["Human:", "Assistant:", "A.", "B.", "C.", "D.", "问题：", "答案：", "解析："]
    prompt = sp.build_prompt(query, sp.LABELS, kb_text, strict_json=strict_json)
    text = sp.generate(tokenizer, model, prompt, bad_words=bad_words)
    if strict_json:
        obj = parse_structured(text)
        if obj and max_score >= threshold and any(obj.values()):
            return {
                "source": "student",
                "max_score": max_score,
                "structured": obj,
                "raw": text,
                "kb_path": kb_path
            }
    if fallback_api != "none":
        api_text = call_api_fallback(query, kb_text, provider=fallback_api)
        obj = parse_structured(api_text) if api_text else None
        return {
            "source": "api_fallback",
            "provider": fallback_api,
            "max_score": max_score,
            "structured": obj if obj else {},
            "raw": api_text if api_text else "",
            "kb_path": kb_path
        }
    structured, raw = sp.enforce_structure(text, sp.LABELS)
    return {
        "source": "student",
        "max_score": max_score,
        "structured": structured,
        "raw": raw,
        "kb_path": kb_path
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--task", type=str, default="legal_judgement")
    parser.add_argument("--kb", type=str, default="civil")
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_path", type=str, default="")
    parser.add_argument("--strict_json", action="store_true")
    parser.add_argument("--fallback_api", type=str, default="dashscope")
    parser.add_argument("--threshold", type=float, default=0.15)
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()
    res = route(
        args.query,
        args.task,
        args.kb,
        args.model_path,
        args.adapter_path,
        args.strict_json,
        args.fallback_api,
        args.threshold,
        dry_run=args.dry_run
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
