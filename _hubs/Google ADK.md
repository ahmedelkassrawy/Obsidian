---
description: "Hub: every note about Google ADK"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/google-adk
---
# Google ADK

> [!info] Agent architecture, tools, sessions/memory, observability and A2A deployment. Large but raw, with a duplicated sessions note and pasted API keys.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/google-adk`.

## How-tos & recipes
- [[Google ADK Agent Tools]] — ADK tool best practices: what the ToolContext parameter gives you (approval requests and state), and how to process the event stream a tool run produces.
- [[Google ADK]] `raw` — Long compiled ADK tutorial: creating and running an agent project, building a multi-tool agent, agent teams, and adding memory.
- [[Google ADK Agent Arch]] `raw` — Pasted ADK code building a root coordinator that calls sub-agents as tools, then sequential ('assembly line') and parallel workflow agents.
- [[Google ADK Deployment And A2A]] `raw` — How ADK's to_a2a() wraps an agent in an A2A server with an auto-generated agent card, and how to serve and call it from another agent.
- [[Google ADK Observability And Eval]] `raw` — Short pasted snippet showing how to attach ADK's LoggingPlugin to an InMemoryRunner for agent observability.
- [[Google ADK Sessions And Memory]] `raw` — Pasted ADK code for persistent sessions, context compaction, session state, and custom tools that read and write that state.

## Related hubs
[[Agent Memory]], [[Multi-Agent Systems]], [[Cloud Deployment]], [[Observability]], [[AI Evaluation]], [[Tool Use & Function Calling]]

## Notes to self (from the audit)
- [[Google ADK Agent Arch]]: Contains a hardcoded Google API key - rotate it and use an env var.
- [[Google ADK Sessions And Memory]]: Has a hardcoded Google API key to rotate.
- [[Google ADK Observability And Eval]]: Barely started - add the eval half that the title promises.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
