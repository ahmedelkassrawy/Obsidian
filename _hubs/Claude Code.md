---
description: "Hub: every note about Claude Code"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/claude-code
---
# Claude Code

> [!info] Reverse-engineered architecture notes - the agent loop, bootstrap pipeline, memory system, LSP, skills and tool schemas. Some of the best-written notes here.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/claude-code`.

## Concepts
- [[Agentic System Best Practices]] — The patterns from Claude Code's architecture that transfer to any agentic system, starting with using an async generator as the agent loop instead of callbacks.
- [[BootStrap Pipeline Best Practices]] — What Claude Code's startup sequence teaches about system design: each phase narrows the space of possibilities, and slow work is loaded in parallel.
- [[Claude Code Core Architecture]] — Deep dive into Claude Code's architecture: what separates an agent from a chatbot, the tech stack and scale, the execution flow, core components and the key design patterns.
- [[Claude Code Memory System - Deep Dive]] — Full study reference on Claude Code's memory architecture from reading its source: the CLAUDE.md, MEMORY.md index, topic file, auto-extraction and consolidation layers, plus the failure modes of each.

## How-tos & recipes
- [[Claude Code With LSP]] — Why grep-based search makes a coding agent slow and inaccurate, and what enabling the Language Server Protocol gives Claude Code - self-correcting edits and on-demand code intelligence.
- [[Context-Compression Best Practices]] — The four context-compaction strategies a Claude Code style agent loop uses to stay under the token limit, with a Python implementation of each.
- [[MCPs]] — Explains what MCP is, how transports and tool discovery work, and gives a 3-step playbook for adding a new tool to an MCP server.
- [[Skill Creation]] — How to write an Agent Skill so it actually triggers: the name/description is the trigger, be precise about goals and loose about steps, and guard against skill rot.

## References & cheat sheets
- [[Agent Tool Schema Best Practices]] — A do/don't table for tool schemas: describe every field, give examples, mark optional fields properly, and avoid over-strict constraints.
- [[SKILLS Best Practice]] — The full Skills authoring guide: keep it concise, set the right degrees of freedom, skill structure and naming, writing descriptions that get discovered, and testing across models.

## Related hubs
[[Agents]], [[Context Engineering]], [[System Design]], [[Tool Use & Function Calling]], [[MCP]], [[Agent Memory]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
