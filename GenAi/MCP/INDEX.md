# MCP — reading order

My notes on the Model Context Protocol, ordered from concepts to building to advanced. Read top to bottom the first time.

1. [[00 - Concepts]] — what MCP is, the host/client/server split, the four capabilities (tools, resources, prompts, sampling), JSON-RPC message types, and the connection lifecycle. Start here.
2. [[01 - Build a server (SDK v2)]] — build a task server from scratch, step by step, on the official SDK v2. Includes a production-operations appendix for remote/hosted servers.
3. [[02 - Best practices & refactor]] — general best practices, prompts in v2, the ten patterns I use, and the before/after refactor of the task server.
4. [[03 - MCP host (client side)]] — the other end: a host/client that consumes servers and runs the tool-call loop.

## Which SDK version am I using?

The official server class was renamed between versions, keep them straight:

- **v2** — `from mcp.server import MCPServer`. This is what notes 01 and 02 use.
- **v1** — `from mcp.server.fastmcp import FastMCP`. Older; the minimal example in 00 uses it.

Check your version first: `python -c "import mcp; print(mcp.__version__)"`.
