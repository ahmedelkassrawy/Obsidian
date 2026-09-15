---
description: "Hub: every note about Concurrency & Async"
type: hub
domain: backend
tags:
  - type/hub
  - topic/concurrency-and-async
---
# Concurrency & Async

> [!info] asyncio, coroutines, and async in FastAPI and SQLAlchemy. Missing: thread pools, the GIL in detail and structured concurrency.
> Part of [[MOC - Backend]]. Also try the tag `#topic/concurrency-and-async`.

## Concepts
- [[Celery]] — What Celery is and when a web app needs it, how it works at a high level, the terminology, and how to choose between Redis and RabbitMQ as the broker.
- [[Concurrency]] — Shows a race condition in concurrent transactions and walks the fixes: single threading, locking and fine-grained locks, with common mistakes.
- [[Concurrency and Async]] — Walks through sync vs async execution in Python, async/await, coroutines, and how concurrency and parallelism play out in FastAPI path operations.
- [[FastAPI Async and Routers]] — Explains when to declare a FastAPI path function async vs sync, and what an APIRouter is for.
- [[LlamaIndex Async Explained]] — Explains the asyncio basics LlamaIndex relies on: the single event loop per thread, asyncio.run, coroutines and awaiting tasks.
- [[Optimizing GenAI Services for Multiple Users]] — Why GenAI services block under load and how to fix it: concurrency vs parallelism, Python execution models, asyncio, and FastAPI concurrency choices.

## How-tos & recipes
- [[10 - Async SQLAlchemy]] — The recommended async engine/session setup, what must be awaited, and a worked async ingest example.
- [[LlamaIndex Event-Driven Workflows]] `raw` — Pasted LlamaIndex Workflow code: steps and typed events, start/stop events, running a workflow, concurrent state changes, typed state, and collecting multiple event types.

## Book notes
- [[OSTEP - Virtualization, Concurrency and Persistence]] — OSTEP opening chapter: the OS as a virtualizer of CPU and memory, system calls, concurrency, persistence and the OS design goals.

## Course notes
- [[FastAPI - Asynchronous Code and Path Parameters]] — FastAPI course notes on async routes, HTTP methods, path and query parameters, Enum-constrained values and request bodies.

## Interviews
- [[InstaBug Assessment]] — The InstaBug written assessment with worked answers: ULID vs UUID as a primary key, race conditions and locks, webhooks, HTTP auth headers, statelessness, and page tables.

## Clippings (raw)
- [[Advanced Topics and Best Practices]] `raw` — Verbatim copy of section 7 of the h9-tec/AI_deployment README on async SQLAlchemy, dependency injection and other FastAPI best practices.

## Related hubs
[[FastAPI]], [[LlamaIndex]], [[API Design]], [[SQLAlchemy]], [[Operating Systems]], [[LLM Serving & vLLM]]

## Notes to self (from the audit)
- [[LlamaIndex Event-Driven Workflows]]: Contains a hardcoded API key - rotate it.
- [[Advanced Topics and Best Practices]]: Copied README section - overlaps the digested 'Integrating FastAPI, Pydantic, and SQLAlchemy' folder.
- [[InstaBug Assessment]]: Good interview material but the answers are generic; add one line per question on how you would say it out loud.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
