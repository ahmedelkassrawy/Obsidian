---
description: "Hub: every note about Context Engineering"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/context-engineering
---
# Context Engineering

> [!info] Designing what goes into the window: layered context, compaction, prompt caching, progressive disclosure. The strongest cross-cutting topic here.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/context-engineering`.

## Concepts
- [[AI Agent Prompt Caching and Context Management]] — Why agent cost and latency grow every turn, and how prompt caching plus context trimming fix it - with a turn-by-turn breakdown of cached vs uncached prefill.
- [[Claude Code Memory System - Deep Dive]] — Full study reference on Claude Code's memory architecture from reading its source: the CLAUDE.md, MEMORY.md index, topic file, auto-extraction and consolidation layers, plus the failure modes of each.
- [[Context Engineering]] — What context engineering is and how to do it: a deep-research-agent case study, layered context architecture, dynamic adjustment, and validation techniques.
- [[Deep Agents Best Practice]] — When to use the deep-agents pattern instead of one big agent, how to manage context and memory across sub-agents, and a tactical checklist of what works and what to avoid.
- [[Langchain.Multi Agent Intro]] — Why multi-agent exists at all (context management and specialization) and a decision guide for choosing between the router, handoff, skills and subagent patterns.

## How-tos & recipes
- [[Context-Compression Best Practices]] — The four context-compaction strategies a Claude Code style agent loop uses to stay under the token limit, with a Python implementation of each.
- [[LangGraph Agents]] — Walks through building a real LangGraph agent by hand: the tool loop, memory across turns, human approval before a tool runs, tool selection with 100 tools, and idempotent retries.
- [[Langchain.Multi Agent - Skills Implementation]] — Implements the skills pattern with progressive disclosure - the agent loads only the skill it needs via a tool call - worked through a database schema and business-logic example.
- [[Pipecat.Context Management]] — What context means in Pipecat, how it updates during a conversation, and how to set up the context aggregator with initial messages and a tools schema.
- [[Skill Creation]] — How to write an Agent Skill so it actually triggers: the name/description is the trigger, be precise about goals and loose about steps, and guard against skill rot.
- [[CrewAI Agent Parameters And Context Window]] `raw` — Pasted CrewAI code showing every Agent parameter, attaching tools, how CrewAI manages the context window with RAG and knowledge sources, and calling an agent directly with kickoff().

## References & cheat sheets
- [[SKILLS Best Practice]] — The full Skills authoring guide: keep it concise, set the right degrees of freedom, skill structure and naming, writing descriptions that get discovered, and testing across models.
- [[Langchain v1]] `raw` — Very large pasted reference for LangChain v1's create_agent: middleware hooks (before and after model), dynamic prompts, runtime and thread_id, and structured response formats.

## Clippings (raw)
- [[Sorting - Sort Three Numbers]] `raw` — Clipped handbook section on context-window pitfalls: the lost-in-the-middle effect and context compression with LLMLingua.

## Related hubs
[[Agents]], [[Claude Code]], [[Multi-Agent Systems]], [[LangChain]], [[LLM Internals]], [[LangGraph]]

## Notes to self (from the audit)
- [[Sorting - Sort Three Numbers]]: Verbatim clip from handbook.exemplar.dev (anchor links still in the headings) - rewrite in your own words to pull it back out of _inbox.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
