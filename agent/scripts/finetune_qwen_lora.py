import os
import json
import argparse
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, PeftModel
from transformers import BitsAndBytesConfig

def read_json_list(path):
    if path.endswith(".jsonl"):
        items = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                items.append(json.loads(line))
        return items
    else:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

def build_examples(items):
    for x in items:
        ins = x.get("instruction", "")
        inp = x.get("input", "")
        outp = x.get("output", "")
        if ins and inp and outp:
            prompt = f"指令：{ins}\n输入：{inp}\n输出："
            yield {"prompt": prompt, "output": outp}

def tokenize_function(tokenizer, max_len):
    def fn(ex):
        prompt_ids = tokenizer(
            ex["prompt"],
            add_special_tokens=True,
            truncation=True,
            max_length=max_len,
        )
        full_text = ex["prompt"] + ex["output"]
        full_ids = tokenizer(
            full_text,
            add_special_tokens=True,
            truncation=True,
            max_length=max_len,
        )
        input_ids = full_ids["input_ids"]
        attn = full_ids["attention_mask"]
        labels = input_ids.copy()
        mask_len = min(len(prompt_ids["input_ids"]), len(labels))
        for i in range(mask_len):
            labels[i] = -100
        return {"input_ids": input_ids, "attention_mask": attn, "labels": labels}
    return fn

def create_model(base_model, use_qlora, device):
    tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=False)
    tokenizer.pad_token = tokenizer.eos_token
    if use_qlora:
        bnb_cfg = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float32 if device == "cpu" else torch.bfloat16,
        )
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            quantization_config=bnb_cfg,
            device_map="auto" if device != "cpu" else None,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(base_model)
    if device == "cpu":
        model.to("cpu")
    lcfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        target_modules=["q_proj","k_proj","v_proj","o_proj","up_proj","down_proj","gate_proj"],
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lcfg)
    return tokenizer, model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, default=os.path.join("data","processed","cleaned_cases.json"))
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--output_dir", type=str, default=os.path.join("data","finetune","qwen_lora"))
    parser.add_argument("--max_length", type=int, default=1024)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--grad_accum", type=int, default=8)
    parser.add_argument("--epochs", type=float, default=0.1)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--use_qlora", action="store_true")
    parser.add_argument("--save_steps", type=int, default=50)
    parser.add_argument("--logging_steps", type=int, default=10)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--max_steps", type=int, default=50)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    items = read_json_list(args.dataset_path)
    examples = list(build_examples(items))
    raw_ds = {"train": examples}
    ds = load_dataset("json", data_files={"train": args.dataset_path})
    tokenizer, model = create_model(args.base_model, args.use_qlora, args.device)
    tok_fn = tokenize_function(tokenizer, args.max_length)
    proc_ds = ds["train"].map(
        lambda x: tok_fn({"prompt": f"指令：{x['instruction']}\n输入：{x['input']}\n输出：", "output": x["output"]}),
        remove_columns=ds["train"].column_names,
        desc="tokenize",
    )
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        save_total_limit=2,
        fp16=False,
        bf16=False,
        optim="adamw_torch",
        report_to="none",
        dataloader_num_workers=0,
    )
    if args.max_steps and args.max_steps > 0:
        training_args.max_steps = args.max_steps
    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        train_dataset=proc_ds,
        data_collator=collator,
    )
    trainer.train()
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

if __name__ == "__main__":
    main()
