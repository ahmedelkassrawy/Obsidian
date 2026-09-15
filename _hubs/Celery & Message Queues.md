---
description: "Hub: every note about Celery & Message Queues"
type: hub
domain: backend
tags:
  - type/hub
  - topic/celery-and-message-queues
---
# Celery & Message Queues

> [!info] A complete Celery guide, a RabbitMQ concept note and an idempotency code review. Missing: retries, dead-letter handling and worker monitoring.
> Part of [[MOC - Backend]]. Also try the tag `#topic/celery-and-message-queues`.

## Concepts
- [[Celery]] — What Celery is and when a web app needs it, how it works at a high level, the terminology, and how to choose between Redis and RabbitMQ as the broker.
- [[Message Queues  (RabbitMQ)]] — Why message queues exist beyond request/response, polling vs push delivery, queue vs pub-sub, and when a queue is actually warranted.
- [[RabbitMQ]] — What RabbitMQ does as a broker, when to use it with Celery vs on its own, plus memory management and TLS configuration notes.

## How-tos & recipes
- [[Celery - Complete Guide]] — End-to-end practical guide to Celery: whether you need it, broker choice, the four components, configuration, task patterns and production concerns.
- [[FastAPI - Scheduler]] `stub` — A three-line snippet adding APScheduler BackgroundScheduler interval jobs inside a FastAPI app file.

## Project notes
- [[2. Durable Ingestion in raaaaag (M5 W2)]] — The design calls for making the raaaaag ingestion pipeline durable: what to wrap in a workflow, how coarse each activity should be, why durable is not idempotent on its own, and when to use Celery instead.
- [[IdempotencyManager - Review & Fixes]] — Code review of a project's IdempotencyManager: the race condition, the celery_task_id coupling and the sync/async mismatch, with the fixes for each.

## Related hubs
[[Redis]], [[FastAPI]], [[Temporal & Durable Workflows]], [[RAG]], [[Concurrency & Async]], [[Transactions & Concurrency Control]]

## Notes to self (from the audit)
- [[FastAPI - Scheduler]]: Stub - explain scheduler lifecycle, shutdown and why not Celery.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
