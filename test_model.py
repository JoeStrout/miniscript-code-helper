#!/usr/bin/env python3
"""Interactive chat session with Qwen2.5-Coder-7B-Instruct."""

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
SYSTEM_PROMPT = "You are a helpful coding assistant."

print(f"Loading tokenizer from {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print(f"Loading model from {MODEL_NAME} (this will download ~15 GB on first run) ...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)
print(f"Model loaded on {model.device} | dtype {model.dtype}")

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("\nReady! Type your query below. Type '/quit' to exit, '/clear' to clear history.\n")

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
