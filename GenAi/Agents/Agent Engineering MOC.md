---
description: "Map of content for agent engineering — the coherent set of notes on building production LLM agents: mechanics, state, control, safety, scale, infra, and evaluation. Most notes carry runnable code."
domain: ai-eng
type: moc
status: digested
tags:
  - domain/ai-eng
  - type/moc
  - topic/agents
  - agents
  - agent-engineering
  - moc
hubs:
  - "[[Agents]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Agent Engineering MOC

The full set of agent-engineering notes, built as one cluster. Each links to the others; most carry runnable LangGraph code. Grouped by concern, then a suggested learning order.

## Core mechanics — how an agent runs
- [[LangGraph Reducers, Routing And Step-Limit Loops]] — state merging (reducers), conditional routing, the loop, and the step-limit guard. *The foundation the rest builds on.*
- [[Agent Reasoning Patterns]] — CoT · ReAct · Reflection · Plan-and-Execute · Tree-of-Thoughts. How the agent *thinks*.
- [[Agent Workflow Patterns (The Five)]] — chaining · parallelization · routing · orchestrator-workers · evaluator-optimizer. Fixed paths (workflow) vs dynamic (agent).

## State — what the agent remembers & sees
- [[LangGraph Short-Term & Long-Term Memory]] — checkpointer/thread (short-term) vs the namespaced Store (long-term).
- [[Context Engineering]] — curating the window: Write / Select / Compress / Isolate; context rot; ordering.

## I/O — how results come out
- [[Streaming And Structured Outputs]] — stream tokens/steps for live UX; `with_structured_output` for machine-usable data.

## Control & safety
- [[Agent Guardrails]] — input/output checks; block/regenerate/rewrite; fail-open vs fail-closed.
- [[Human-in-the-Loop (Approval & Interrupts)]] — pause on a consequential boundary, resume with a human decision.

## Scale & multi-agent
- [[Agent Handoffs And Tool Design]] — supervisor/swarm handoffs; tool-design best practices; grouping tools by domain.

## Infra
- [[LLM Gateways]] — one door to many models: fallback, cost caps, keys, rate limits.
- [[LLM Caching]] — exact / semantic (Redis) / prompt-prefix / embedding caches.

## Observability & evaluation
- [[LangSmith]] — traces, datasets, feedback/scores (human · rule · LLM-judge).
- [[Agent Trajectory Evaluation]] — outcome vs trajectory vs single-step; `agentevals` + `client.evaluate`.

## The through-lines (how it all connects)
- **Reducers** power everything: memory (accumulate messages), step limits (counters), parallel workflows (safe concurrent writes).
- **The step-limit guard** recurs: ReAct loops, reflection, handoffs, guardrail regenerate — cap them all.
- **Three "reasoning" patterns ARE workflow patterns:** reflection = evaluator-optimizer, ToT = parallelization-voting, plan-execute ≈ orchestrator-workers.
- **Context engineering ties the state notes together:** memory = Write, RAG + tool grouping = Select, summarization = Compress, handoffs = Isolate, caching rewards good ordering.
- **Guardrails and HITL are the same idea:** a rule vs a human approving a risky/irreversible action; both fail-closed on harm.
- **Gateway + caching + observability** = the production layer around any agent.

## Suggested learning order
1. Reducers/Routing/Step-limit → 2. Reasoning patterns → 3. Workflow patterns → 4. Memory → 5. Context engineering → 6. Tools & handoffs → 7. Guardrails → 8. HITL → 9. Streaming & structured outputs → 10. Gateways → 11. Caching → 12. Observability → 13. Trajectory eval.

## Flagship build — put it all together
- [[ResolveFlow — Flagship Build Spec]] — one multi-tenant agentic support platform that demonstrates all 13 concepts in shipped code (merges the CV's Customer Support Agent + Multi-Tenant RAG entries). The portfolio proof.

## Anchored to real builds
Everything maps to **raaaaag** (ReAct agent, `search_docs`, refusal guardrail, eval harness, OpenRouter gateway, Redis cache, Temporal durability) and **Shutterabia** (MCP tool catalog, publish HITL approval, brand guardrails, D1 mirror). The patterns aren't abstract — each note names where it shows up in code Kassra shipped.
