import json
import os
import re

def clean_text(text):
    """
    简单的文本清洗函数
    """
    # 去除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_cases(input_file, output_file):
    """
    读取原始案例数据，清洗并转换为初步的问答对格式
    """
    if not os.path.exists(input_file):
        print(f"文件不存在: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = []
    
    for item in data:
        content = item.get('content', '')
        if not content:
            continue
            
        # 简单规则：假设内容中包含"判决："，我们尝试分割案情和判决
        # 在实际项目中，这需要更复杂的NLP提取或人工标注
        if '判决：' in content:
            parts = content.split('判决：')
            fact = parts[0]
            judgment = '判决：' + parts[1]
            
            # 构造微调数据项
            # instruction: 指令，告诉模型要做什么
            # input: 输入内容（案情）
            # output: 期望输出（判决结果）
            processed_item = {
                "instruction": "请根据以下案情描述，模拟法官进行判决分析。",
                "input": clean_text(fact),
                "output": clean_text(judgment)
            }
            processed_data.append(processed_item)

    # 保存处理后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成，共生成 {len(processed_data)} 条数据，保存至 {output_file}")

if __name__ == "__main__":
    # 定义路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "raw", "sample_cases.json")
    output_path = os.path.join(base_dir, "data", "processed", "cleaned_cases.json")
    
    process_cases(input_path, output_path)
