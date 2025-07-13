import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from transformers import BitsAndBytesConfig

# MODEL: Falcon-RW-1B (small, fits on low VRAM)
model_id = "tiiuae/falcon-rw-1b"

# Bitsandbytes 4-bit config with CPU offload allowed
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

# Load tokenizer & model
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
model.config.use_cache = False
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["query_key_value"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)

# Load dataset from both files
ds = load_dataset("json", data_files=["data/symptom_diagnosis.jsonl", "data/blood_reports.jsonl"], split="train")

# Format prompt
def format_prompt(example):
    prompt = f"<human>: {example['instruction']}\n<bot>: {example['output']}"
    encoding = tokenizer(prompt, truncation=True, padding="max_length", max_length=256)
    encoding["labels"] = encoding["input_ids"].copy()
    return encoding

ds = ds.map(format_prompt, remove_columns=["instruction", "output"])

# Training arguments
training_args = TrainingArguments(
    output_dir="models/falcon-rw1b-medbot",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=2,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=1,
    fp16=True,
    learning_rate=2e-4,
    report_to="none",
)

data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

# Train
print("Starting training...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=ds,
    tokenizer=tokenizer,
    data_collator=data_collator
)

trainer.train()