---
description: "Hub: every note about LangGraph"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/langgraph
---
# LangGraph

> [!info] Fourteen notes, the most of any framework, but most are pasted code with numbered filenames. The map-reduce and agent-building notes are the ones worth rereading.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/langgraph`.

## Concepts
- [[LangGraph Nodes Edges And State]] — The core LangGraph mental model - break the agent into nodes, describe the transitions, share state - plus error handling, retry policies and compiling with a checkpointer.

## How-tos & recipes
- [[LangGraph Agents]] — Walks through building a real LangGraph agent by hand: the tool loop, memory across turns, human approval before a tool runs, tool selection with 100 tools, and idempotent retries.
- [[Langchain.Multi Agent Example]] — A worked multi-agent build: HITL middleware on the subgraphs, a checkpointer on the supervisor, and a three-layer tools/subagents/supervisor architecture with controlled information flow.
- [[Langgraph v1 - Map Reduce Pattern]] — How to fan work out in LangGraph v1 with a map-reduce pattern: a prepare-batches node, parallel worker nodes, and reducing their results back into state.
- [[DeepAgents]] `raw` — Notes and code for the deepagents library: built-in planning with write_todos, streaming, the default StateBackend, and why a checkpointer is required for human-in-the-loop.
- [[LangGraph Human In The Loop And Checkpointers]] `raw` — Pasted human-in-the-loop code: a graph that interrupts for approval, the resume path after approve or reject, and checkpointer setup.
- [[LangGraph Long-Term Memory With Trustcall]] `raw` — Pasted code for long-term memory in LangGraph: a Memory schema, Trustcall extractor, a store for across-thread memory alongside a checkpointer, and a spy to inspect the tool calls.
- [[LangGraph Memory]] `raw` — Pasted LangGraph memory code: compiling with InMemorySaver, using thread_id config, and reading conversation state back with get_state.
- [[LangGraph Routing And Path Maps]] `raw` — Scratch notes on the coordinator/router shape in LangGraph: keeping next_step in state and using add_conditional_edges with a path map or Literal.
- [[LangGraph Tool Node Basics]] `stub` — One short tip plus snippet: do not pass state into tools, use ToolNode and bind the tools to the model, with a should_continue router.
- [[LangSmith]] `stub` — The .env variables that turn LangSmith tracing on and the two lines of Python that load them.
- [[Langgraph Best Practices]] `raw` — Short pasted patterns for LangGraph: with_structured_output, bind_tools, and a conditional-edge gate function that routes between nodes.
- [[Langgraphics Graph Visualizer]] `stub` — A single snippet showing how to wrap a compiled LangGraph with langgraphics' watch() to visualize a run.
- [[Run Agent - Langchain & Langgraph]] `raw` — Two pasted REPL loops - one LangChain, one LangGraph - for chatting with an agent from the terminal with a per-conversation thread_id.

## References & cheat sheets
- [[LangGraph - Before v1]] `stale` — Older LangGraph reference: reducers and add_messages, routers, Command vs conditional edges, and binding tools to the model.
- [[LangGraph Tools Persistence And Streaming]] `raw` — Large pasted LangGraph reference: defining tools and schema, nodes/routers/edges, a ReAct agent, persistence with interruptions, streaming, and threads.

## Book notes
- [[Building Applications with Agents.Ch1 & 2]] — Ch1-2 notes: build a minimal 'cancel order' agent in a LangGraph StateGraph, why scoping matters, a minimal evaluation, and the core components of an agent system.
- [[Ch1 - From LLMs to Agents - The Foundational Blueprint]] — Book chapter showing how a static LLM becomes an agent through a reason-act-observe loop, modelled as finite and hierarchical state machines and mapped onto LangGraph.

## Course notes
- [[Agent Memory with Redis]] — Tutorial notes on building a memory-enabled travel agent with Redis and LangGraph: short-term vs long-term memory, data models, storage, and vector search over memories.

## Project notes
- [[Project Agent Arch]] — Architecture writeup for DataPilot AI, a LangGraph Text-to-SQL agent: the graph nodes from router through schema intelligence, memory, SQL generation, approval gate and retry loop.

## Related hubs
[[Agents]], [[Agent Memory]], [[LangChain]], [[Observability]], [[Context Engineering]], [[Redis]]

## Notes to self (from the audit)
- [[Langchain.Multi Agent Example]]: Contains a hardcoded API key - rotate it.
- [[LangGraph - Before v1]]: Explicitly pre-v1 LangGraph plus legacy LangChain imports - check every snippet against current docs before reuse.
- [[LangSmith]]: Contains a real LANGSMITH_API_KEY in plain text - revoke and rotate that key now.
- [[Project Agent Arch]]: Content is GenAI agent engineering - likely belongs in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
