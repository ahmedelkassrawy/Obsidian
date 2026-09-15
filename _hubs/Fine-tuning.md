---
description: "Hub: every note about Fine-tuning"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/fine-tuning
---
# Fine-tuning

> [!info] SFT vs RL, LoRA/QLoRA/PEFT, an Axolotl tutorial and two pasted training runs. Missing: a real end-to-end fine-tune you ran yourself and any eval of the result.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/fine-tuning`.

## Concepts
- [[Fine-Tuning Use Cases And Hyperparameters]] — When fine-tuning is the right call: real-world uses, whether it adds new knowledge, how it compares to RAG, and the hyperparameters that matter during training.
- [[Fine-Tuning vs Reinforcement Learning]] — Lays out the LLM training stages and contrasts supervised fine-tuning (match a target) with reinforcement learning (score the result), including upsides and downsides of each.

## How-tos & recipes
- [[Fine-Tuning Tutorial]] — A full fine-tuning tutorial on Rotten Tomatoes sentiment: loading data, BERT setup, freezing layers to save compute, few-shot SetFit, and masked-language-model pretraining.
- [[Fine-Tuning BERT On MRPC With Trainer]] `raw` — Pasted walkthrough of fine-tuning a model on the GLUE MRPC paraphrase task: loading the dataset, tokenizing, the data collator, and training with the Trainer API.
- [[PEFT]] `raw` — Pasted PEFT code fine-tuning flan-t5-base on a summarization dataset: tokenize function across splits, device handling, and the training setup.

## References & cheat sheets
- [[Fine-Tuning Quick Reference]] — A condensed fine-tuning recipe: add a classification head to a pretrained transformer, tokenize, define metrics, and run the HuggingFace Trainer, plus tricks to improve results.
- [[LLM Terminology]] — Plain-English glossary of the fine-tuning and inference terms that keep coming up: PEFT, LoRA, QLoRA, adapters, instruction tuning, SFT and the KV cache.

## Book notes
- [[Ch2. Understanding Foundation Models]] — Chip Huyen Ch2: the four choices that make models differ - training data, transformer architecture and size, post-training alignment, and sampling (which is why models hallucinate).

## Course notes
- [[Fine-Tuning Fundamentals and Axolotl Tutorial]] — Video-course notes on the three ways to train an LLM (pre-training, fine-tuning, LoRA/QLoRA) plus a practical Axolotl-on-RunPod run and the key hyperparameters.

## Clippings (raw)
- [[Clipping - LLM Fine-Tuning Crash Course (YouTube)]] `raw` — Raw YouTube transcript of a one-hour end-to-end fine-tuning walkthrough: preparing a custom dataset and fine-tuning an LLM on it.
- [[LLM Finetuning & Deployment Notes]] `empty` — A bare Notion link with no content - the actual fine-tuning and deployment notes live outside the vault.

## Related hubs
[[HuggingFace]], [[Transformers]], [[LLM Internals]], [[RAG]], [[NLP Preprocessing]], [[Classification]]

## Notes to self (from the audit)
- [[LLM Finetuning & Deployment Notes]]: Nine words, just a Notion URL - pull the content in or delete.
- [[Clipping - LLM Fine-Tuning Crash Course (YouTube)]]: Digest into AI-Eng/Fine-tuning. Vault has almost no hands-on fine-tuning note, so this one is worth the time.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
