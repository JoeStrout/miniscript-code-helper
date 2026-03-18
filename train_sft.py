#!/usr/bin/env python3
"""QLoRA supervised fine-tuning of Qwen2.5-Coder-7B-Instruct.

Loads the base model in 4-bit (QLoRA), attaches a LoRA adapter to the
attention layers, and trains on the JSONL dataset produced by prepare_data.py.

Usage:
    python prepare_data.py                      # first, generate train_data.jsonl
    python train_sft.py                         # train on all data
    python train_sft.py --sample-size 64        # train on a random 64-example subset
    python train_sft.py --epochs 10 --lr 1e-4   # override defaults

Output is saved to ./sft_output/ with the final adapter in ./sft_output/final/.
"""

import argparse
import os
os.environ["USE_TF"] = "0"          # prevent transformers from loading TensorFlow

import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
DATA_FILE = "train_data.jsonl"
OUTPUT_DIR = "./sft_output"


def parse_args():
    parser = argparse.ArgumentParser(description="QLoRA SFT training")
    parser.add_argument("--sample-size", type=int, default=64,
                        help="Randomly sample N examples per epoch (default: 64)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for sampling and training (default: 42)")
    parser.add_argument("--epochs", type=int, default=20,
                        help="Number of training epochs (default: 20)")
    parser.add_argument("--lr", type=float, default=2e-4,
                        help="Learning rate (default: 2e-4)")
    parser.add_argument("--max-length", type=int, default=1024,
                        help="Max sequence length in tokens (default: 1024)")
    return parser.parse_args()


def main():
    args = parse_args()

    # -- QLoRA: load the base model in 4-bit to save VRAM --
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    # -- LoRA adapter settings --
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # -- Training hyperparameters --
    # When sampling, we run our own outer epoch loop (1 epoch per iteration,
    # fresh sample each time), so num_train_epochs is always 1 here.
    training_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        lr_scheduler_type="constant",
        warmup_ratio=0.0,
        bf16=True,
        logging_steps=1,
        save_strategy="no",
        max_length=args.max_length,
        gradient_checkpointing=True,
        seed=args.seed,
    )

    # -- Load model, tokenizer, and dataset --
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
    full_dataset = load_dataset("json", data_files=DATA_FILE, split="train")
    print(f"  {len(full_dataset)} total examples")

    sample_size = min(args.sample_size, len(full_dataset))
    sampling = sample_size < len(full_dataset)

    print(f"Training for {args.epochs} epochs, {sample_size} examples each ...")

    for epoch in range(args.epochs):
        epoch_seed = args.seed + epoch
        if sampling:
            dataset = full_dataset.shuffle(seed=epoch_seed).select(range(sample_size))
            print(f"\n--- Epoch {epoch+1}/{args.epochs} (sampled {sample_size}, seed={epoch_seed}) ---")
        else:
            dataset = full_dataset.shuffle(seed=epoch_seed)
            print(f"\n--- Epoch {epoch+1}/{args.epochs} ---")

        trainer = SFTTrainer(
            model=model,
            args=training_config,
            train_dataset=dataset,
            processing_class=tokenizer,
            peft_config=lora_config,
        )

        trainer.train()

    # Save the final adapter (small — just the LoRA weights)
    trainer.save_model(f"{OUTPUT_DIR}/final")
    tokenizer.save_pretrained(f"{OUTPUT_DIR}/final")
    print(f"\nDone! Adapter saved to {OUTPUT_DIR}/final/")


if __name__ == "__main__":
    main()
