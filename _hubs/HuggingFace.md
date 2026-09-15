---
description: "Hub: every note about HuggingFace"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/huggingface
---
# HuggingFace

> [!info] Tokenizers, padding and truncation, and a couple of pipeline snippets. All raw code.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/huggingface`.

## How-tos & recipes
- [[Fine-Tuning Tutorial]] — A full fine-tuning tutorial on Rotten Tomatoes sentiment: loading data, BERT setup, freezing layers to save compute, few-shot SetFit, and masked-language-model pretraining.
- [[Modern Tokenization]] — Shows modern subword tokenization with the BERT tokenizer and how to run text through BERT to get contextual embeddings.
- [[Fine-Tuning BERT On MRPC With Trainer]] `raw` — Pasted walkthrough of fine-tuning a model on the GLUE MRPC paraphrase task: loading the dataset, tokenizing, the data collator, and training with the Trainer API.
- [[Hugging Face]] `raw` — Short pasted code for two HuggingFace tasks: text classification with DistilBERT and basic text generation.
- [[NLP Eval Code]] `raw` — Code for computing NLP metrics with the HuggingFace evaluate library: BLEU for translation, ROUGE for summarization and seqeval for NER, wired into a training loop.
- [[PEFT]] `raw` — Pasted PEFT code fine-tuning flan-t5-base on a summarization dataset: tokenize function across splits, device handling, and the training setup.
- [[Sorting - Sort Three Numbers]] `raw` — Pasted tokenizer code covering encoding text, every padding option, truncation to model max length, and what input_ids and attention masks look like.
- [[Summarization]] `raw` — A minimal HuggingFace summarization pipeline call with bart-large-cnn on a sample passage.

## References & cheat sheets
- [[Fine-Tuning Quick Reference]] — A condensed fine-tuning recipe: add a classification head to a pretrained transformer, tokenize, define metrics, and run the HuggingFace Trainer, plus tricks to improve results.

## Book notes
- [[Ch3. Serving GenAI Models with FastAPI]] — Ch3 notes: how transformers, tokenization, embeddings and positional encoding work, then how to serve text, image, audio and 3D models from a FastAPI app.

## Clippings (raw)
- [[Clipping - LLM Fine-Tuning Crash Course (YouTube)]] `raw` — Raw YouTube transcript of a one-hour end-to-end fine-tuning walkthrough: preparing a custom dataset and fine-tuning an LLM on it.

## Related hubs
[[Transformers]], [[Fine-tuning]], [[NLP Preprocessing]], [[FastAPI]], [[LLM Internals]], [[Classification]]

## Notes to self (from the audit)
- [[Clipping - LLM Fine-Tuning Crash Course (YouTube)]]: Digest into AI-Eng/Fine-tuning. Vault has almost no hands-on fine-tuning note, so this one is worth the time.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
