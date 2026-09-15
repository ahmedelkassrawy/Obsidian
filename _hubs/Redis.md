---
description: "Hub: every note about Redis"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/redis
---
# Redis

> [!info] Referenced as a Celery broker and a cache but has no note of its own. Empty hub - worth filling first.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/redis`.

## Concepts
- [[Celery]] — What Celery is and when a web app needs it, how it works at a high level, the terminology, and how to choose between Redis and RabbitMQ as the broker.

## How-tos & recipes
- [[Celery - Complete Guide]] — End-to-end practical guide to Celery: whether you need it, broker choice, the four components, configuration, task patterns and production concerns.
- [[Semantic Caching - Redis]] `raw` — Pasted code for a Redis semantic cache: a cache-optimized embedding model, loading FAQ data into the cache, and a TTL policy to keep it fresh.

## References & cheat sheets
- [[Redis Env Config]] `empty` — A handful of Redis environment variables for persistence, memory limit, eviction policy and protected mode.

## Course notes
- [[Agent Memory with Redis]] — Tutorial notes on building a memory-enabled travel agent with Redis and LangGraph: short-term vs long-term memory, data models, storage, and vector search over memories.
- [[Caching - Capacity Estimation and Strategies]] — System Design lecture on caching: capacity estimation for a growing e-commerce system, cache placement, strategies and invalidation.

## Related hubs
[[Celery & Message Queues]], [[Caching]], [[Agent Memory]], [[LangGraph]], [[Concurrency & Async]], [[Embeddings & Semantic Search]]

## Notes to self (from the audit)
- [[Redis Env Config]]: Sixteen words - fold into the Mini-RAG deployment notes.
- [[Caching - Capacity Estimation and Strategies]]: Overlaps 'Caching.md' in the same folder - consider merging or cross-linking.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
