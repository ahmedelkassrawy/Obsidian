---
description: "Hub: every note about Agent Memory"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/agent-memory
---
# Agent Memory

> [!info] Short vs long term memory with Redis, Mem0, LangGraph stores and ADK sessions. Mostly pasted code - the concepts are not written up anywhere.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/agent-memory`.

## Concepts
- [[Claude Code Memory System - Deep Dive]] — Full study reference on Claude Code's memory architecture from reading its source: the CLAUDE.md, MEMORY.md index, topic file, auto-extraction and consolidation layers, plus the failure modes of each.

## How-tos & recipes
- [[AWS Bedrock Agent Core]] `raw` — Pasted CLI and Python snippets for configuring, launching, and adding memory to an agent on AWS Bedrock AgentCore with LangGraph.
- [[DeepAgents]] `raw` — Notes and code for the deepagents library: built-in planning with write_todos, streaming, the default StateBackend, and why a checkpointer is required for human-in-the-loop.
- [[Google ADK]] `raw` — Long compiled ADK tutorial: creating and running an agent project, building a multi-tool agent, agent teams, and adding memory.
- [[Google ADK Sessions And Memory]] `raw` — Pasted ADK code for persistent sessions, context compaction, session state, and custom tools that read and write that state.
- [[LangGraph Long-Term Memory With Trustcall]] `raw` — Pasted code for long-term memory in LangGraph: a Memory schema, Trustcall extractor, a store for across-thread memory alongside a checkpointer, and a spy to inspect the tool calls.
- [[Mem0.Agents Memory]] `raw` — Pasted Mem0 code for giving an agent long-term memory with Gemini models: init, add, search, and use memories in a chat loop.

## References & cheat sheets
- [[LangGraph Tools Persistence And Streaming]] `raw` — Large pasted LangGraph reference: defining tools and schema, nodes/routers/edges, a ReAct agent, persistence with interruptions, streaming, and threads.

## Book notes
- [[Agents - Ai Engineering Book]] — Chip Huyen chapter notes on agents: what an environment and action set are, tool categories and function calling, planning vs execution, and agent memory.

## Course notes
- [[Agent Memory with Redis]] — Tutorial notes on building a memory-enabled travel agent with Redis and LangGraph: short-term vs long-term memory, data models, storage, and vector search over memories.

## Related hubs
[[Agents]], [[LangGraph]], [[Google ADK]], [[Tool Use & Function Calling]], [[Cloud Deployment]], [[Redis]]

## Notes to self (from the audit)
- [[AWS Bedrock Agent Core]]: Pasted commands with almost no prose - add a short explanation of what each agentcore step does.
- [[Mem0.Agents Memory]]: Code only, no headings or prose - add a paragraph on when Mem0 beats a plain vector store.
- [[Google ADK Sessions And Memory]]: Has a hardcoded Google API key to rotate.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
