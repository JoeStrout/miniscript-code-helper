#!/usr/bin/env python3
"""QLoRA supervised fine-tuning of Qwen2.5-Coder-7B-Instruct.

Loads the base model in 4-bit (QLoRA), attaches a LoRA adapter to the
attention layers, and trains on the JSONL dataset produced by prepare_data.py.


Usage:
    python prepare_data.py          # first, generate train_data.jsonl
    python train_sft.py             # then, run training

Output is saved to ./sft_output/ with the final adapter in ./sft_output/final/.
"""

import os
os.environ["USE_TF"] = "0"          # prevent transformers from loading TensorFlow

import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
DATA_FILE = "train_data.jsonl"
OUTPUT_DIR = "./sft_output"

# QLoRA: load the base model in 4-bit to save VRAM
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# LoRA adapter settings
lora_config = LoraConfig(
    r=16,                   # rank — higher = more capacity but more VRAM
    lora_alpha=32,          # scaling factor (alpha/r = effective LR multiplier)
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# Training hyperparameters
training_config = SFTConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=20,                # small dataset needs many passes
    per_device_train_batch_size=2,
    gradient_accumulation_steps=2,      # effective batch size = 4
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    bf16=True,
    logging_steps=1,
    save_strategy="epoch",
    max_length=2048,
    gradient_checkpointing=True,        # saves VRAM at cost of speed
)

# ---------------------------------------------------------------------------
# Load model, tokenizer, and dataset
# ---------------------------------------------------------------------------
print(f"Loading tokenizer from {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f"Loading model in 4-bit from {MODEL_NAME} ...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
)

print(f"Loading dataset from {DATA_FILE} ...")
dataset = load_dataset("json", data_files=DATA_FILE, split="train")
print(f"  {len(dataset)} training examples")

# ---------------------------------------------------------------------------
# Train
# ---------------------------------------------------------------------------
trainer = SFTTrainer(
    model=model,
    args=training_config,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=lora_config,
)

print("Starting training ...")
trainer.train()

# Save the final adapter (small — just the LoRA weights)
trainer.save_model(f"{OUTPUT_DIR}/final")
tokenizer.save_pretrained(f"{OUTPUT_DIR}/final")
print(f"\nDone! Adapter saved to {OUTPUT_DIR}/final/")
