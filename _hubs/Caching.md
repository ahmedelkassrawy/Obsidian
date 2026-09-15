---
description: "Hub: every note about Caching"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/caching
---
# Caching

> [!info] Two overlapping notes on strategies and invalidation plus Memcached internals. Missing: a real Redis note and cache stampede handling.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/caching`.

## Concepts
- [[AI Agent Prompt Caching and Context Management]] — Why agent cost and latency grow every turn, and how prompt caching plus context trimming fix it - with a turn-by-turn breakdown of cached vs uncached prefill.
- [[Anthropic RAG Cheatsheet]] — Anthropic's contextual-retrieval writeup: why embeddings miss exact matches, how prepending context to each chunk fixes it, using prompt caching to make it affordable, and reranking on top.
- [[Caching]] — Introduction to caching: why it matters, cache types, read and write strategies, hit/miss, and invalidation problems.
- [[Consistent Hashing]] — Explains the consistent hashing ring, the rebalancing problem it solves, and how to present it in a system design interview.
- [[Full Text Search using Elasticsearch for Blazingly Fast Search]] — Why LIKE queries stop scaling and how an inverted index plus Elasticsearch relevance scoring solves search at size.

## How-tos & recipes
- [[LiteLLM Prompt Caching]] — How LiteLLM injects prompt-caching checkpoints for you, what it saves, and how to turn it on in the proxy without touching application code.
- [[Semantic Caching - Redis]] `raw` — Pasted code for a Redis semantic cache: a cache-optimized embedding model, loading FAQ data into the cache, and a TTL policy to keep it fresh.

## Course notes
- [[Caching - Capacity Estimation and Strategies]] — System Design lecture on caching: capacity estimation for a growing e-commerce system, cache placement, strategies and invalidation.
- [[LLM Proxies]] — Course notes on running a LiteLLM proxy in front of several model providers: config file, starting the server, calling it with the OpenAI client, logging and load balancing.
- [[Memcached]] — Course notes on Memcached internals: slab allocation against fragmentation, listener/worker threading and LRU eviction.

## Meta
- [[Reading Input With Cin And Getline]] `empty` — Three scratch lines pairing a problem with a tool: semantic caching to Redis, handwriting to VLMs, printed text to OCR.

## Clippings (raw)
- [[Clipping - Caching Strategies (YouTube, Arabic)]] `raw` — Raw Arabic YouTube transcript on caching: what a cache buys you, the caching strategies and their trade-offs, eviction policies, and cache invalidation.

## Related hubs
[[System Design]], [[LLM Serving & vLLM]], [[Redis]], [[Context Engineering]], [[LLM Internals]], [[OCR]]

## Notes to self (from the audit)
- [[Reading Input With Cin And Getline]]: Eight words - fold these three lines into the OCR and caching notes, then delete.
- [[Caching - Capacity Estimation and Strategies]]: Overlaps 'Caching.md' in the same folder - consider merging or cross-linking.
- [[Clipping - Caching Strategies (YouTube, Arabic)]]: Digest into Backend/System Design/Caching.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
