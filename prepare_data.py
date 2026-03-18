#!/usr/bin/env python3
"""Parse qa_corpus.md into JSONL training data for SFT.

Each **User:** / **Assistant:** pair becomes one training example
in chat-message format:
    {"messages": [{"role":"system",...}, {"role":"user",...}, {"role":"assistant",...}]}

Usage:
    python prepare_data.py                  # write train_data.jsonl
    python prepare_data.py --preview        # print examples without writing
"""

import argparse
import json
import re

from transformers import AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
SYSTEM_PROMPT = "You are a helpful assistant specializing in MiniScript programming."
INPUT_FILE = "qa_corpus.md"
OUTPUT_FILE = "train_data.jsonl"


def parse_corpus(path):
    with open(path) as f:
        content = f.read()

    # Match each User/Assistant pair; assistant text runs until the next
    # **User:** marker or end-of-file.
    pattern = (
        r"\*\*User:\*\*\s*(.*?)"       # user content (lazy)
        r"\s*\*\*Assistant:\*\*\s*"     # delimiter
        r"(.*?)"                        # assistant content (lazy)
        r"(?=\*\*User:\*\*|\Z)"        # stop before next user or EOF
    )
    matches = re.findall(pattern, content, re.DOTALL)

    examples = []
    for user_text, assistant_text in matches:
        # Strip trailing markdown section headers that belong to the next entry
        assistant_text = re.sub(r"\n+(?:#+ [^\n]*\n*)+\s*$", "", assistant_text).strip()
        user_text = user_text.strip()

        if not user_text or not assistant_text:
            continue

        examples.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_text},
            ]
        })

    return examples


def report_token_stats(examples):
    """Tokenize every example with the real chat template and print stats."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    lengths = []
    for ex in examples:
        text = tokenizer.apply_chat_template(
            ex["messages"], tokenize=False, add_generation_prompt=False
        )
        token_count = len(tokenizer.encode(text))
        lengths.append(token_count)

    lengths.sort()
    print(f"\nToken stats ({MODEL_NAME} tokenizer):")
    print(f"  min:    {lengths[0]}")
    print(f"  median: {lengths[len(lengths)//2]}")
    print(f"  max:    {lengths[-1]}")
    print(f"  mean:   {sum(lengths)/len(lengths):.0f}")

    # Flag examples that might cause OOM
    long = [i for i, n in enumerate(lengths) if n > 1024]
    if long:
        print(f"  >1024 tokens: {len(long)} examples")


def main():
    parser = argparse.ArgumentParser(description="Convert qa_corpus.md to JSONL")
    parser.add_argument("--preview", action="store_true",
                        help="Print parsed examples instead of writing JSONL")
    args = parser.parse_args()

    examples = parse_corpus(INPUT_FILE)

    if args.preview:
        for i, ex in enumerate(examples):
            msgs = ex["messages"]
            print(f"{'='*60}")
            print(f"Example {i+1}")
            print(f"{'='*60}")
            print(f"USER:\n{msgs[1]['content'][:200]}...")
            print(f"\nASSISTANT:\n{msgs[2]['content'][:200]}...")
            print()
        print(f"Total: {len(examples)} examples")
        return

    with open(OUTPUT_FILE, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")

    print(f"Wrote {len(examples)} training examples to {OUTPUT_FILE}")
    report_token_stats(examples)


if __name__ == "__main__":
    main()
