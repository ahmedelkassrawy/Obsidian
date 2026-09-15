---
description: "Hub: every note about LlamaIndex"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/llamaindex
---
# LlamaIndex

> [!info] Agents, event-driven workflows and the RAG pipeline. Almost entirely pasted code with hardcoded API keys.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/llamaindex`.

## Concepts
- [[LlamaIndex Async Explained]] — Explains the asyncio basics LlamaIndex relies on: the single event loop per thread, asyncio.run, coroutines and awaiting tasks.

## How-tos & recipes
- [[LlamaIndex RAG Pipeline]] — The LlamaIndex RAG pipeline end to end: loading with readers, transformations and chunking, adding metadata and embeddings, and building the index.
- [[LlamaIndex Agents And Multi-Agent Workflows]] `raw` — Pasted LlamaIndex agent code: a basic FunctionAgent, running with a Context for state, setting Settings for LLM and embeddings, and defining a multi-agent workflow.
- [[LlamaIndex Agents And Workflows Notes]] `raw` — Scratch notes plus code on combining LlamaIndex agents, workflows and AgentWorkflows, and on specifying tool parameters and outputs.
- [[LlamaIndex Event-Driven Workflows]] `raw` — Pasted LlamaIndex Workflow code: steps and typed events, start/stop events, running a workflow, concurrent state changes, typed state, and collecting multiple event types.

## Related hubs
[[Concurrency & Async]], [[Agents]], [[Multi-Agent Systems]], [[RAG]], [[Vector Search]]

## Notes to self (from the audit)
- [[LlamaIndex Agents And Multi-Agent Workflows]]: Contains a hardcoded Google API key - rotate it.
- [[LlamaIndex Event-Driven Workflows]]: Contains a hardcoded API key - rotate it.
- [[LlamaIndex RAG Pipeline]]: Contains a hardcoded API key - rotate it.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
