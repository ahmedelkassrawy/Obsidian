---
description: "Hub: every note about Temporal & Durable Workflows"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/temporal-and-durable-workflows
---
# Temporal & Durable Workflows

> [!info] Core concepts through a PDF pipeline, advanced patterns via contract review, and the durable-ingestion design calls for raaaaag. Well digested.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/temporal-and-durable-workflows`.

## Concepts
- [[1. Temporal Core Concepts]] — Temporal explained through a real PDF-extraction pipeline: server, client, task queue, worker, workflow vs activity, retries, timeouts and determinism.
- [[Workers Concept]] — How to make scheduled agent work survive crashes on Cloudflare Workers using a sync plus watchdog pattern, state projection, heartbeats and reconciliation.

## How-tos & recipes
- [[2. AI Contract Review — Advanced Temporal Patterns]] — Advanced Temporal patterns on an AI contract-review project: child workflows fanned out in parallel, LLM synthesis in the parent, and human-in-the-loop via signals, queries and updates.

## Project notes
- [[2. Durable Ingestion in raaaaag (M5 W2)]] — The design calls for making the raaaaag ingestion pipeline durable: what to wrap in a workflow, how coarse each activity should be, why durable is not idempotent on its own, and when to use Celery instead.

## Related hubs
[[Cloudflare Workers]], [[Agents]], [[Multi-Agent Systems]], [[RAG]], [[Celery & Message Queues]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
