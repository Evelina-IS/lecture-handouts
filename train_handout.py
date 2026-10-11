import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model_id = "Qwen/Qwen2.5-3B-Instruct"
dataset_path = "handout_train_data.jsonl"
output_lora_dir = "./qwen_handout_3b_lora"

print("--> [1/4] 载入分词器与 4-bit 量化底模...")
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)
model.gradient_checkpointing_enable()

# LoRA 适配层：针对长文本结构逻辑注入微调参数
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

print("--> [2/4] 预处理长文本讲义语料...")
dataset = load_dataset("json", data_files=dataset_path, split="train")

def preprocess_function(examples):
    inputs = []
    targets = []
    for inst, out in zip(examples["instruction"], examples["output"]):
        prompt = f"""<|im_start|>system
你是一个顶级的大学学术讲义编纂专家与 LaTeX 排版专家，只输出格式合规的 ctexart 讲义代码。<|im_end|>
<|im_start|>user
{inst}<|im_end|>
<|im_start|>assistant
"""
        inputs.append(prompt)
        targets.append(out + "<|im_end|>")

    model_inputs = {"input_ids": [], "labels": [], "attention_mask": []}
    for p, t in zip(inputs, targets):
        p_ids = tokenizer.encode(p, add_special_tokens=False)
        t_ids = tokenizer.encode(t, add_special_tokens=False)
        input_ids = (p_ids + t_ids)[:2048]
        labels = ([-100] * len(p_ids) + t_ids)[:2048]
        mask = [1] * len(input_ids)

        model_inputs["input_ids"].append(input_ids)
        model_inputs["labels"].append(labels)
        model_inputs["attention_mask"].append(mask)

    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset.column_names)

training_args = TrainingArguments(
    output_dir="./outputs_handout",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_ratio=0.1,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=1,
    save_strategy="no",
    optim="paged_adamw_8bit"
)

print("--> [3/4] 启动原生 Trainer 学术讲义排版微调...")
trainer = Trainer(
    model=model,
    train_dataset=tokenized_dataset,
    args=training_args,
    data_collator=DataCollatorForSeq2Seq(tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True)
)

trainer.train()

print(f"--> [4/4] 保存微调权重至 {output_lora_dir}...")
model.save_pretrained(output_lora_dir)
tokenizer.save_pretrained(output_lora_dir)
print("=== 讲义专用模型微调完成！===")
