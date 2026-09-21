---
description: "Hub: every note about Tool Use & Function Calling"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/tool-use-and-function-calling
---
# Tool Use & Function Calling

> [!info] Tool schemas, the action/observation loop and debugging bad tool calls. New hub - the material was scattered across Agents and the framework folders.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/tool-use-and-function-calling`.

## Concepts
- [[Function Calling]] — How function calling drives the agent loop - tool definitions, the action/observation cycle, debugging bad tool calls, and rules for writing tool schemas.

## How-tos & recipes
- [[01 - Build a server (SDK v2)]] — Step-by-step build of an MCP task server on SDK v2: server object, data shape, logging, each tool, saving to a file and loading on startup.
- [[02 - Best practices & refactor]] — The practice side of MCP: transport selection, message handling, security, debugging, prompts in SDK v2, and a worked refactor to thin handlers over pure functions.
- [[Agent with Tools]] — Tutorial notes on building a secure multi-user agent with Arcade.dev and LangGraph: per-user identity, authorized tool calls, and human-in-the-loop approval.
- [[Google ADK Agent Tools]] — ADK tool best practices: what the ToolContext parameter gives you (approval requests and state), and how to process the event stream a tool run produces.
- [[MCPs]] — Explains what MCP is, how transports and tool discovery work, and gives a 3-step playbook for adding a new tool to an MCP server.
- [[Pipecat.Function Calling]] — Function calling in a Pipecat voice pipeline: defining functions with the standard schema or as direct functions, building the tools schema, and registering the handler.

## References & cheat sheets
- [[Agent Tool Schema Best Practices]] — A do/don't table for tool schemas: describe every field, give examples, mark optional fields properly, and avoid over-strict constraints.

## Book notes
- [[Agent Orchestration And Tool Selection]] — Ch5 notes on orchestration: the common agent archetypes (reflex, ReAct, planner-executor, query-decomposition, reflection, deep research) and strategies for selecting tools.
- [[Agents - Ai Engineering Book]] — Chip Huyen chapter notes on agents: what an environment and action set are, tool categories and function calling, planning vs execution, and agent memory.

## Related hubs
[[Agents]], [[MCP]], [[Claude Code]], [[Agent Memory]], [[Auth & Security]], [[Multi-Agent Systems]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
