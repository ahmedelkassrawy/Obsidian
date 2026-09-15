---
description: "Hub: every note about Multi-Agent Systems"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/multi-agent-systems
---
# Multi-Agent Systems

> [!info] Router, handoffs, skills and subagent architectures with both concept and implementation notes, plus deep agents. Missing: failure modes when agents talk to each other.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/multi-agent-systems`.

## Concepts
- [[Crews vs Flows]] — Explains how CrewAI Flows and Crews fit together - Flows hold state and control, Crews do collaborative work - and when to use each or both.
- [[Deep Agents]] — Short explanation of why shallow agents break on long tasks and the four things deep agents add: planning, orchestrator/sub-agents, agentic search, and verification.
- [[Deep Agents Best Practice]] — When to use the deep-agents pattern instead of one big agent, how to manage context and memory across sub-agents, and a tactical checklist of what works and what to avoid.
- [[Langchain.Multi Agent - Handoffs]] — The handoffs architecture explained: tools update a persisted state variable that decides which behaviour is active next, plus when to use it.
- [[Langchain.Multi Agent - Router]] — The router architecture: a classification step sends each input to the specialist agent for its vertical, and the router itself can be wrapped as a tool.
- [[Langchain.Multi Agent - Skills]] — The skills architecture: packaging prompt-driven specializations as invokable skills the agent calls on demand instead of stuffing them all in the system prompt.
- [[Langchain.Multi Agent - Subagents]] — The supervisor/subagent architecture: wrapping agents as tools, sync vs async execution, and why a single dispatch tool beats one tool per subagent.
- [[Langchain.Multi Agent Intro]] — Why multi-agent exists at all (context management and specialization) and a decision guide for choosing between the router, handoff, skills and subagent patterns.

## How-tos & recipes
- [[2. AI Contract Review — Advanced Temporal Patterns]] — Advanced Temporal patterns on an AI contract-review project: child workflows fanned out in parallel, LLM synthesis in the parent, and human-in-the-loop via signals, queries and updates.
- [[Langchain.Multi Agent - Handoffs Implementation]] — Implements the handoff/state-machine pattern: tools that set the current step, per-step prompts and tool sets, required state, and a way to go back a step.
- [[Langchain.Multi Agent - Skills Implementation]] — Implements the skills pattern with progressive disclosure - the agent loads only the skill it needs via a tool call - worked through a database schema and business-logic example.
- [[Langchain.Multi Agent Example]] — A worked multi-agent build: HITL middleware on the subgraphs, a checkpointer on the supervisor, and a three-layer tools/subagents/supervisor architecture with controlled information flow.
- [[Google ADK Agent Arch]] `raw` — Pasted ADK code building a root coordinator that calls sub-agents as tools, then sequential ('assembly line') and parallel workflow agents.
- [[Google ADK Deployment And A2A]] `raw` — How ADK's to_a2a() wraps an agent in an A2A server with an auto-generated agent card, and how to serve and call it from another agent.
- [[Langchain.Multi Agent - Router Implementation]] `empty` — Empty placeholder for the code version of the multi-agent router pattern.
- [[LlamaIndex Agents And Multi-Agent Workflows]] `raw` — Pasted LlamaIndex agent code: a basic FunctionAgent, running with a Context for state, setting Settings for LLM and embeddings, and defining a multi-agent workflow.

## Book notes
- [[Agent Orchestration And Tool Selection]] — Ch5 notes on orchestration: the common agent archetypes (reflex, ReAct, planner-executor, query-decomposition, reflection, deep research) and strategies for selecting tools.

## Clippings (raw)
- [[Clipping - Building Reliable Agentic AI Systems (Article)]] `raw` — Clipped case-study article on PRINCE, a production agentic RAG system for preclinical drug research: intent clarification, a planning step, researcher, reflection and writer agents, and how they built trust in it.

## Related hubs
[[LangChain]], [[Agents]], [[Context Engineering]], [[Google ADK]], [[Tool Use & Function Calling]], [[CrewAI]]

## Notes to self (from the audit)
- [[Google ADK Agent Arch]]: Contains a hardcoded Google API key - rotate it and use an env var.
- [[Langchain.Multi Agent - Router Implementation]]: Zero words - the concept note 'Langchain.Multi Agent - Router' exists; fill in the implementation or delete.
- [[Langchain.Multi Agent Example]]: Contains a hardcoded API key - rotate it.
- [[LlamaIndex Agents And Multi-Agent Workflows]]: Contains a hardcoded Google API key - rotate it.
- [[Clipping - Building Reliable Agentic AI Systems (Article)]]: Digest into AI-Eng/Agents - it is the only production multi-agent case study in the vault.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
