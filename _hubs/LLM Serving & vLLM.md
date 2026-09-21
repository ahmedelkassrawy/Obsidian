---
description: "Hub: every note about LLM Serving & vLLM"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/llm-serving-and-vllm
---
# LLM Serving & vLLM

> [!info] One strong hands-on vLLM note with real measurements. Everything else here is an empty lesson file and a link dump.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/llm-serving-and-vllm`.

## Concepts
- [[LLM Inference Internals]] — prefill/decode, KV cache, paged attention, static vs continuous batching, vLLM tuning.
- [[LLMOps Observability And Production Stack]] — Notes on LLMOps in production: which LLM metrics to monitor, the observability layers, LLM routing, feedback loops, versioning strategy, and cost and privacy controls.
- [[Optimizing GenAI Services for Multiple Users]] — Why GenAI services block under load and how to fix it: concurrency vs parallelism, Python execution models, asyncio, and FastAPI concurrency choices.

## How-tos & recipes
- [[LiteLLM Prompt Caching]] — How LiteLLM injects prompt-caching checkpoints for you, what it saves, and how to turn it on in the proxy without touching application code.
- [[vLLM Serving]] — Hands-on notes from serving Qwen2.5-1.5B on a Colab T4 with vLLM: what serving means, KV cache, continuous batching, prefix caching, and latency vs throughput with real measurements.

## Course notes
- [[LLM Proxies]] — Course notes on running a LiteLLM proxy in front of several model providers: config file, starting the server, calling it with the OpenAI client, logging and load balancing.

## Clippings (raw)
- [[AI Engineering Reading Links]] `raw` — A bare list of URLs to vLLM, eval-harness, BMAD-method and LinkedIn/YouTube posts to read later.

## Related hubs
[[LLM Internals]], [[Observability]], [[Caching]], [[Concurrency & Async]], [[FastAPI]], [[Agents]]

## Notes to self (from the audit)
- [[AI Engineering Reading Links]]: Pure link dump with no annotations - note next to each link why it is worth reading.
- [[LLMOps Observability And Production Stack]]: Opens with a LinkedIn link and a personal roadmap TODO - move that to a task note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
