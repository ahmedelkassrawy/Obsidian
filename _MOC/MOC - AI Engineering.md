---
description: "Map of Content for the AI Engineering domain"
type: moc
domain: ai-eng
tags:
  - type/moc
  - domain/ai-eng
---
# MOC - AI Engineering

This is the biggest and most active area of the vault: 176 notes on LLMs, RAG, agents, agent frameworks and the infrastructure around them. The strongest parts are RAG (20 notes, from chunking strategies through hybrid search and reranking to a real production retriever), agent design (patterns, eval loops, system design, two production case studies), and voice agents (Pipecat covered framework-feature by framework-feature). Framework coverage is wide - LangChain, LangGraph, LlamaIndex, CrewAI, DSPy, Google ADK, deepagents, MCP, Temporal - but uneven: the MCP, Temporal and Claude Code notes are written in your own words, while most of the LangGraph, LlamaIndex, ADK and CrewAI notes are pasted code with no explanation. The biggest gaps are evaluation (the AI Engineering Ch4 note on evaluating AI systems is empty and there is no eval note of your own), fine-tuning past the tutorial level, and LLM serving (one good vLLM note, an empty vLLM lesson, and a link dump). Ten notes still carry pre-1.0 LangChain code that will not run today, and twelve notes have live API keys pasted into them.

**181 notes** — digested 109, raw 45, stub 11, stale 9, empty 7. Search tip: tag `#domain/ai-eng`.

## Hubs
- [[LLM Internals]] (14) — How models are built and how inference actually runs - prefill vs decode, KV cache, sampling. Missing: quantization and anything about attention variants.
- [[Prompting]] (10) — Prompt techniques from zero-shot to ReAct, plus prompt-injection defence. The main note's code half is pre-1.0 LangChain.
- [[Context Engineering]] (14) — Designing what goes into the window: layered context, compaction, prompt caching, progressive disclosure. The strongest cross-cutting topic here.
- [[AI Evaluation]] (10) — Why single-run eval is worthless and what a harness must collect. The weakest hub relative to its importance - the book chapter on evaluating AI systems is an empty file.
- [[Fine-tuning]] (11) — SFT vs RL, LoRA/QLoRA/PEFT, an Axolotl tutorial and two pasted training runs. Missing: a real end-to-end fine-tune you ran yourself and any eval of the result.
- [[LLM Serving & vLLM]] (9) — One strong hands-on vLLM note with real measurements. Everything else here is an empty lesson file and a link dump.
- [[RAG]] (25) — The deepest hub in the vault: chunking strategies, HyDE, sentence-window, parent-child, GraphRAG, hybrid search, reranking, and production trade-offs. Six of these notes run on pre-1.0 LangChain code.
- [[Vector Search]] (20) — Index types, ANN and HNSW, choosing a vector database, PGVector and Pinecone. Missing: a benchmark you ran yourself.
- [[Agents]] (41) — The largest agent collection in the vault: patterns, agency levels, workflows vs agents, production best practice, two case studies and a system-design note. Well digested.
- [[Multi-Agent Systems]] (18) — Router, handoffs, skills and subagent architectures with both concept and implementation notes, plus deep agents. Missing: failure modes when agents talk to each other.
- [[Agent Memory]] (12) — Short vs long term memory with Redis, Mem0, LangGraph stores and ADK sessions. Mostly pasted code - the concepts are not written up anywhere.
- [[Tool Use & Function Calling]] (11) — Tool schemas, the action/observation loop and debugging bad tool calls. New hub - the material was scattered across Agents and the framework folders.
- [[AI Security]] (3) — Guardrails, rate limiting, prompt attacks and agent sandboxing. Thin - the sandbox note is a stub.
- [[LangChain]] (19) — v1 create_agent and middleware plus the multi-agent pattern series. Two notes still use pre-1.0 APIs.
- [[LangGraph]] (20) — Fourteen notes, the most of any framework, but most are pasted code with numbered filenames. The map-reduce and agent-building notes are the ones worth rereading.
- [[LlamaIndex]] (5) — Agents, event-driven workflows and the RAG pipeline. Almost entirely pasted code with hardcoded API keys.
- [[CrewAI]] (4) — Agents, tasks, and crews vs flows. One duplicate note; no project built with it yet.
- [[DSPy]] (3) — Programming, evaluation and optimization including a MIPROv2 walkthrough. The optimization note is the good one.
- [[Google ADK]] (7) — Agent architecture, tools, sessions/memory, observability and A2A deployment. Large but raw, with a duplicated sessions note and pasted API keys.
- [[MCP]] (6) — The most polished series in the vault: concepts, building a server on SDK v2, best practices, and the host/client side, with an index note giving the reading order.
- [[Voice Agents]] (14) — The STT-LLM-TTS sandwich, latency, LiveKit and a LangChain voice agent. Missing: anything you shipped.
- [[Pipecat]] (11) — Eleven notes covering the framework feature by feature - pipeline and frames, VAD and turn detection, STT, TTS, function calling, context and termination. New hub.
- [[OCR]] (4) — OCR vs vision models with a confidence-threshold hybrid, and PaddleOCR basics. Practical and short.
- [[HuggingFace]] (11) — Tokenizers, padding and truncation, and a couple of pipeline snippets. All raw code.
- [[Claude Code]] (10) — Reverse-engineered architecture notes - the agent loop, bootstrap pipeline, memory system, LSP, skills and tool schemas. Some of the best-written notes here.
- [[Temporal & Durable Workflows]] (4) — Core concepts through a PDF pipeline, advanced patterns via contract review, and the durable-ingestion design calls for raaaaag. Well digested.
- [[Cloudflare Workers]] (2) — Fault-tolerant scheduled agent work with a sync plus watchdog pattern, and the camelAI Durable Object story.
- [[Observability]] (14) — Golden signals, three pillars, and MySQL profiling. Missing: an OpenTelemetry or Prometheus setup you actually ran.
- [[Caching]] (12) — Two overlapping notes on strategies and invalidation plus Memcached internals. Missing: a real Redis note and cache stampede handling.
- [[Redis]] (6) — Referenced as a Celery broker and a cache but has no note of its own. Empty hub - worth filling first.

Gaps: [[Knowledge Gaps Audit 2026-09-15]]. Back to [[00 Home]].
