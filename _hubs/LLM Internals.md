---
description: "Hub: every note about LLM Internals"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/llm-internals
---
# LLM Internals

> [!info] How models are built and how inference actually runs - prefill vs decode, KV cache, sampling. Missing: quantization and anything about attention variants.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/llm-internals`.

## Concepts
- [[AI Agent Prompt Caching and Context Management]] — Why agent cost and latency grow every turn, and how prompt caching plus context trimming fix it - with a turn-by-turn breakdown of cached vs uncached prefill.
- [[Embeddings Representations And Latent Space]] — Answers what embeddings, representations and latent space have in common and how they differ, from the Machine Learning Q and AI book.
- [[Fine-Tuning vs Reinforcement Learning]] — Lays out the LLM training stages and contrasts supervised fine-tuning (match a target) with reinforcement learning (score the result), including upsides and downsides of each.
- [[How KV Cache speed up LLM Inference]] — Why a model that is fast for one user crawls for a hundred, and the two fixes: KV cache to stop redoing attention maths, and paged attention to stop wasting GPU memory.
- [[LLM Inference From Prefill To Batching]] — The two phases of inference - prefill reads the whole prompt, decode writes one token at a time - plus KV cache and static vs continuous batching.

## How-tos & recipes
- [[vLLM Serving]] — Hands-on notes from serving Qwen2.5-1.5B on a Colab T4 with vLLM: what serving means, KV cache, continuous batching, prefix caching, and latency vs throughput with real measurements.
- [[Anthropic Messages API Basics]] `raw` — Short pasted Anthropic SDK code: a single messages.create call and a helper pattern for multi-turn conversations that keeps history in a message list.
- [[LLM And Embedding Provider Interface]] `stub` — An abstract base class sketch for swapping LLM and embedding providers behind one interface.

## References & cheat sheets
- [[LLM Terminology]] — Plain-English glossary of the fine-tuning and inference terms that keep coming up: PEFT, LoRA, QLoRA, adapters, instruction tuning, SFT and the KV cache.

## Book notes
- [[Ch1. Introduction to Building AI Applications with Foundation Models]] — Chip Huyen Ch1: how self-supervision and scale produced foundation models, why the job is called AI engineering, what people build with it, and the layers of the stack.
- [[Ch2. Understanding Foundation Models]] — Chip Huyen Ch2: the four choices that make models differ - training data, transformer architecture and size, post-training alignment, and sampling (which is why models hallucinate).
- [[Ch3. Serving GenAI Models with FastAPI]] — Ch3 notes: how transformers, tokenization, embeddings and positional encoding work, then how to serve text, image, audio and 3D models from a FastAPI app.
- [[Encoder Vs Decoder Models]] `stub` — Short comparison of encoder models (representation, e.g. BERT) and decoder models (generation) by purpose, input and output.

## Clippings (raw)
- [[Sorting - Sort Three Numbers]] `raw` — Clipped handbook section on context-window pitfalls: the lost-in-the-middle effect and context compression with LLMLingua.

## Related hubs
[[LLM Serving & vLLM]], [[Transformers]], [[Fine-tuning]], [[Context Engineering]], [[Embeddings & Semantic Search]], [[Caching]]

## Notes to self (from the audit)
- [[Sorting - Sort Three Numbers]]: Verbatim clip from handbook.exemplar.dev (anchor links still in the headings) - rewrite in your own words to pull it back out of _inbox.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
