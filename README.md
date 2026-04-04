# miniscript-code-helper
a project to fine-tune (via SFT and RL) and RAG-ify an LLM to help with the MiniScript programming language


## Quick Start (without RAG)

1. Run `prepare_data.py` to convert the Q&A data in `qa_corpus.md` into `train_data.jsonl`.
2. Run `train_sft.py` to train a QLoRA adapter.  It will be saved to `./sft_output/final/`.
3. Run inference using the adapter via `inference_sft.py`.

## Adding RAG

I find the fine-tuning helps, but only so much; the model does much better with the addition of RAG (retrieval-augmented generation).  For that these additional steps are needed:

1. Run `prepare_data.py` to prepare the Chroma vector DB.
2. Run inference with `inference_rag.py` (instead of `inference_sft`).

## Training Setup

Key details about the training setup:
```
  ┌────────────────────────┬───────────────────────────────┬───────────────────────────────────────────────────┐
  │        Setting         │             Value             │                        Why                        │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ Quantization           │ 4-bit NF4 (QLoRA)             │ Base model uses ~4 GB VRAM instead of ~14 GB      │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ LoRA rank              │ 16                            │ Good balance of capacity vs. efficiency           │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ LoRA targets           │ q/k/v/o attention projections │ Where most task-specific learning happens         │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ Effective batch size   │ 4 (1 × 4 accumulation)        │ Small dataset, don't need large batches           │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ Learning rate          │ 2e-4 with cosine decay        │ Standard for QLoRA                                │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ Epochs                 │ 3                             │ Conservative — increase if loss is still dropping │
  ├────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────┤
  │ Gradient checkpointing │ On                            │ Saves VRAM during training                        │
  └────────────────────────┴───────────────────────────────┴───────────────────────────────────────────────────┘
```
