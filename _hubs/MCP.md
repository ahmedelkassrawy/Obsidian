---
description: "Hub: every note about MCP"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/mcp
---
# MCP

> [!info] The most polished series in the vault: concepts, building a server on SDK v2, best practices, and the host/client side, with an index note giving the reading order.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/mcp`.

## Concepts
- [[00 - Concepts]] — The MCP architecture from the ground up: the host/client/server split, the four capabilities, and the JSON-RPC 2.0 request, response and notification message types.

## How-tos & recipes
- [[01 - Build a server (SDK v2)]] — Step-by-step build of an MCP task server on SDK v2: server object, data shape, logging, each tool, saving to a file and loading on startup.
- [[02 - Best practices & refactor]] — The practice side of MCP: transport selection, message handling, security, debugging, prompts in SDK v2, and a worked refactor to thin handlers over pure functions.
- [[03 - MCP host (client side)]] — Building the other end of MCP - a Gemini-backed host that connects to servers, manages connections, keeps a tool registry, and exposes a webhook.
- [[MCPs]] — Explains what MCP is, how transports and tool discovery work, and gives a 3-step playbook for adding a new tool to an MCP server.

## Meta
- [[MCP Reading Order]] — The reading order for the MCP notes, from concepts through building a server to the host side, plus how to tell which SDK version you are on.

## Related hubs
[[Tool Use & Function Calling]], [[Claude Code]], [[Agents]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
