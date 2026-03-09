## Mar 6, 2026

I'm starting a project to fine-tune a local LLM to be a MiniScript code assistant.

I'm starting with the [Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) model.  It's 7B parameters, which should fit comfortably on my RTX-4090 (which has 24GB of VRAM), and it's already trained to follow instructions and understand code.  

I've got a conda environment set up with:
- torch 2.6.0 (CUDA 12.4)
- transformers 4.57.5
- datasets 4.4.1
- huggingface-hub 0.36.0

I had to also install:
- accelerate 1.13.0
- bitsadbytes 0.49.2
- peft 0.18.1
- trl 0.29.0

Then, I wrote (with help from Claude) [test_model.py](test_model.py), which downloads the LLM and provides a basic interactive session.

I was pleasantly surprised to find that out of the box, Qwen-Coder-7B knows about MiniScript:

>You: Have you heard of MiniScript?
>
>Assistant: Yes, I am aware of MiniScript. It is a simple programming language designed to be easy 
>for beginners to learn and use. MiniScript is often used as an introduction to programming 
>concepts and can be used for basic scripting tasks. It has a syntax that is similar to Python and 
>supports many of the same features, such as variables, loops, conditionals, and functions. 
>Additionally, MiniScript is open-source and can be downloaded and used on various platforms.

However, as expected, it doesn't really understand much about the language:

> You: How would I iterate over a map in MiniScript?
> 
> Assistant: In MiniScript, you can iterate over a map (also known as a dictionary or associative 
> array) using a `for` loop with the `each` keyword. The following example demonstrates how to 
> iterate over a map called `myMap`:
> ```
> myMap = {
>   "key1": "value1",
>   "key2": "value2",
>   "key3": "value3"
> }
> 
> for key, value in myMap.each():
>   print("Key: " + key)
>   print("Value: " + value)
> ```
> 
> This will output the keys and values of each entry in the map. The `each()` method returns an 
> iterator that yields the key-value pairs in the map. You can then use these pairs in your loop 
> body to perform any operations you need.
> It's important to note that MiniScript does not have built-in support for maps, so if you're 
> working with a different programming language that uses a different data structure for maps, you 
> may need to adapt this code accordingly.

It's answering in Python rather than MiniScript.  So, fine-tuning time!

Earlier this week, I had prepared a small [Q&A Corpus](qa_corpus.md) of 18 questions and responses.  I'm keeping these in Markdown format so they are easier to read and write (for us humans).  The standard training package (trl) works best with the "JSONL" (JSON Lines) format, wherein each line is a standalone, valid JSON object.  Script [prepare_data.py](prepare_data.py) parses my .md format, and writes out [train_data.jsonl](train_data.jsonl), which is then used by another script, [train_sft.py](train_sft.py), to train a QLoRA adapter.

Key details about the initial training setup:
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
The trained adapter will be tiny (~50-100 MB in ./sft_output/final/) compared to the 15 GB base model. The inference script loads the full-precision base model + adapter overlay, so you get the best quality at inference time even though training was done in 4-bit.

After the first training run, the loss only got to a little more than 1.0, and upon testing (using [inference_sft.py](inference_sft.py), which loads the adapter), it still failed the map-iteration question.  So I made the following changes:

- num_train_epochs = 20 (up from 3)
- per_device_train_batch_size = 2 (up from 1)
- gradient_accumulation_steps = 2 (down from 4)

Finished the second training run, this time with a final loss of 0.0646.  Let's try it again!

> You: How would I iterate over a map in MiniScript?
> 
> Assistant: In MiniScript, use `for kv in map` to iterate over entries as `[key: value]` maps.                                      >                                                               
> ```
> map = [a: 1, b: 2, c: 3]
> for kv in map
>     print kv.key + ": " + kv.value
> end for
> // prints:
> // a: 1
> // b: 2
> // c: 3
> ```

A much better answer!  That bit about "as `[key: value]` map" doesn't make a lot of sense to me, and its syntax for defining `map` in the code example is wrong, but the rest of it is correct.

So, this is progress, and proves that the LoRA adapter works.  I think the next step is probably to build out the QA corpus so we have a lot more training data.


## Mar 8, 2026

I used Claude to go through all 30 chapters of _Learn to Code in 30 Days_ and generate questions based on that material.  I instructed it to leave the answers blank (just "TODO").  I reviewed and modified/added myself, resulting in 70 new questions.  Then, separately, I instructed Claude to find the unanswered questions, and for each one, spawn a fresh sub-agent to activate the MiniScript skill and answer a single question.  My goal with all that was to produce a fresh answer not relying on or referring to any previous context.

We now have 100 questions and answers.  However, I need to go over and manually verify the answers -- a quick scan showed some errors or misunderstandings on Claude's part.

...That took a while!  But I believe all the answers are correct now.

