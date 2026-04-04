#!/usr/bin/env python3
"""Interactive RAG-augmented chat using the fine-tuned LoRA adapter + ChromaDB.

On each query, retrieves relevant MiniScript documentation chunks and injects
them into the system prompt so the model can ground its answers.

Usage:
    python inference_rag.py
    python inference_rag.py --adapter ./sft_output/final --db ./chroma_db --top-k 5
    python inference_rag.py --verbose   # show retrieved chunks
"""

import argparse
import os
import readline

os.environ.setdefault("USE_TF", "0")  # avoid TensorFlow/Keras crash

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
DEFAULT_ADAPTER = "./sft_output/final"
DEFAULT_DB = "./chroma_db"
COLLECTION = "miniscript_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

BASE_SYSTEM_PROMPT = "You are a helpful assistant specializing in MiniScript programming."


def build_system_prompt(base_prompt: str, results: dict) -> str:
    """Build augmented system prompt with retrieved context chunks."""
    if not results or not results["documents"] or not results["documents"][0]:
        return base_prompt

    context_parts = []
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    for doc, meta in zip(docs, metas):
        header = f"[Source: {meta['source']}, Section: {meta['section']}]"
        context_parts.append(f"{header}\n{doc}")

    context_block = "\n\n".join(context_parts)

    return (
        f"{base_prompt}\n\n"
        f"Use the following reference material to help answer the user's question:\n\n"
        f"{context_block}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", default=DEFAULT_ADAPTER,
                        help="Path to the LoRA adapter directory")
    parser.add_argument("--db", default=DEFAULT_DB,
                        help="Path to ChromaDB persistent storage")
    parser.add_argument("--top-k", type=int, default=5,
                        help="Number of chunks to retrieve per query")
    parser.add_argument("--verbose", action="store_true",
                        help="Print retrieved chunks before answering")
    args = parser.parse_args()

    # Load ChromaDB
    print(f"Loading ChromaDB (RAG data) from {args.db} ...")
    embedding_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    db_client = chromadb.PersistentClient(path=args.db)
    collection = db_client.get_collection(name=COLLECTION, embedding_function=embedding_fn)
    print(f"  Collection '{COLLECTION}' has {collection.count()} chunks")

    # Load model
    print(f"Loading tokenizer from {MODEL_NAME} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print(f"Loading base model from {MODEL_NAME} ...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )

    print(f"Loading LoRA adapter (fine tuning) from {args.adapter} ...")
    model = PeftModel.from_pretrained(base_model, args.adapter)
    model.eval()
    print("Ready!")

    messages = [{"role": "system", "content": BASE_SYSTEM_PROMPT}]

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
            messages = [{"role": "system", "content": BASE_SYSTEM_PROMPT}]
            print("-- conversation history cleared --\n")
            continue

        # Retrieve relevant chunks
        results = collection.query(query_texts=[user_input], n_results=args.top_k)

        if args.verbose and results["documents"] and results["documents"][0]:
            print("\n--- Retrieved chunks ---")
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                print(f"  [{meta['source']} > {meta['section']}] (dist={dist:.4f})")
                # Show first 120 chars of each chunk
                preview = doc[:120].replace('\n', ' ')
                print(f"    {preview}...")
            print("------------------------\n")

        # Build augmented system prompt with retrieved context
        augmented_prompt = build_system_prompt(BASE_SYSTEM_PROMPT, results)

        # Replace system message with augmented version for this turn
        rag_messages = [{"role": "system", "content": augmented_prompt}]
        # Add conversation history (skip original system message)
        rag_messages.extend(messages[1:])
        rag_messages.append({"role": "user", "content": user_input})

        text = tokenizer.apply_chat_template(rag_messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text], return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=1024)
        response = tokenizer.decode(output[0][len(inputs.input_ids[0]):], skip_special_tokens=True)

        # Store in conversation history (without RAG context, to keep history clean)
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": response})

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
