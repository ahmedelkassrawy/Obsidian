---
description: "async/await lets one thread juggle many tasks while they wait on I/O; it does nothing for CPU-heavy work, which blocks the event loop and needs processes or workers instead."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/concurrency-async
  - topic/python
hubs:
  - "[[Concurrency & Async]]"
created: 2026-10-01
---
# Async helps with waiting, not with computing

## The idea
In Python, `asyncio` runs one event loop on one thread. When a coroutine hits `await` on something slow (a network call, a DB query), it hands control back and the loop runs another task. That's concurrency: many things in progress, one at a time on the CPU. It's great when most of the time is spent waiting.

It doesn't make computation faster. If a coroutine does heavy CPU work (parsing a big file, running a model on CPU) or calls a blocking library without `await`, the whole loop freezes and every other request waits. For CPU work you need real parallelism: multiple processes, or a worker queue like Celery.

## Example
In FastAPI, an `async def` route that calls `requests.get()` (blocking) stalls the whole server. Either use an async client (`httpx`) or declare the route as plain `def`, which FastAPI runs in a thread pool.

## Connects to
- [[Locks trade concurrency for correctness]] — once tasks overlap, shared state needs protecting. That's true even in async code, at every `await` point.
- [[The context window is a budget, not a bucket]] — LLM calls are slow I/O, which is why GenAI services are a natural fit for async.

## Sources
- [[Concurrency and Async]]
- [[FastAPI Async and Routers]]
- [[Optimizing GenAI Services for Multiple Users]]
- [[LlamaIndex Async Explained]]
- [[Celery]]

## 30-second answer
> Async lets a single thread switch between tasks while they wait on I/O, so it's great for network and database-heavy services. It doesn't help CPU-bound work. That blocks the event loop, so you move it to processes or a task queue like Celery.
