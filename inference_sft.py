#!/usr/bin/env python3
"""Interactive chat using the base model + fine-tuned LoRA adapter.

Usage:
    python inference_sft.py                         # default adapter path
    python inference_sft.py --adapter ./sft_output/final
"""

import argparse

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
DEFAULT_ADAPTER = "./sft_output/final"
SYSTEM_PROMPT = "You are a helpful assistant specializing in MiniScript programming."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", default=DEFAULT_ADAPTER,
                        help="Path to the LoRA adapter directory")
    args = parser.parse_args()

    print(f"Loading tokenizer from {MODEL_NAME} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print(f"Loading base model from {MODEL_NAME} ...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )

    print(f"Loading LoRA adapter from {args.adapter} ...")
    model = PeftModel.from_pretrained(base_model, args.adapter)
    model.eval()
    print("Ready!")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("\nType your query below. Type '/quit' to exit, '/clear' to clear history.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "/quit":
            print("Bye!")
            break
        if user_input.lower() == "/clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("-- conversation history cleared --\n")
            continue

        messages.append({"role": "user", "content": user_input})

        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text], return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=1024)
        response = tokenizer.decode(output[0][len(inputs.input_ids[0]):], skip_special_tokens=True)

        messages.append({"role": "assistant", "content": response})

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
