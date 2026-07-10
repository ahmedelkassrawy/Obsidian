#### Using Webhook with MCP

Import Libraries
```python
import ngrok
import uvicorn
from fastapi import FastAPI,Request
from loguru import logger
from config import get_settings
from contextlib import asynccontextmanager
from host.host import MCPHost
import json
import logging

settings = get_settings()
client = MCPHost()
logger = logging.getLogger("webhook")
logging.basicConfig(level=logging.INFO)
```

Async Context Manager
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the MCP client
    logger.info("Initializing MCPHost...")
    await client.initialize()
    logger.info("MCPHost initialized successfully")
    yield

    # Shutdown: Cleanup
    logger.info("Cleaning up MCPHost...")
    await client.cleanup()
    logger.info("MCPHost cleaned up")

app = FastAPI(lifespan=lifespan)
```

Making Clients:
```python
import httpx
from config import get_settings
from loguru import logger

SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
SLACK_CHANNEL_HISTORY_URL = "https://slack.com/api/conversations.history"

class SlackClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers = {
                "Authorization": f"Bearer {settings.SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            }
        )

    async def send_message(self,channel:str,text:str) -> dict:
        logger.info(f"Sending message to Slack Channel '{channel}' : {text}")
        
        payload = {
            "channel":channel,
            "text":text,
        }

        response = await self.client.post(SLACK_POST_MESSAGE_URL,json = payload)
        response.raise_for_status()

        if response.json()["ok"]:
            logger.info(f"Message sent successfully: {response.json()}")
        else:
            logger.error(f"Failed to send message: {response.json()}")

        return response.json()
```

Making Slack Server:
```python
from clients.slack_client import SlackClient
from fastmcp import FastMCP

slack_client = SlackClient()
slack_mcp = FastMCP("slack_tools")

@slack_mcp.tool(
    description = "Gets last x messages from a Slack channel",
    tags = {"slack","channel","history"},
    annotations = {"title":"Get Channel History",
                   "readOnlyHint":True,
                   "openWorldHint": True,
                   },
)
async def get_channel_history(channel:str,limit:int = 10):
    """Get the last x messages from a Slack channel"""
    messages = await slack_client.get_last_message(channel,limit)

    if messages:
        return {
            "status":"success",
            "messages":messages
        }
    else:
        return {
            "status":"failure",
            "messages":[]
        }
```

Making tool registry
```python
import logging
from typing import Set
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

class MCPServerRegistry:
    def __init__(self):
        self.registry = FastMCP("tool_registry")
        self.all_tags: Set[str] = set()
        self.is_initialized = False
        
	async def initialize(self):
        if self.is_initialized:
            return

        logger.info("Initializing MCPServersRegistry")

        all_mcp_instances = [asana_mcp, github_mcp, slack_mcp, agent_scope_mcp]
        
        for inst in all_mcp_instances:
		    name = getattr(inst, "name", "unknown")
		    logger.info(f"Processing MCP instance: {name}")
		
		    # Tools
		    tool_mgr = getattr(inst, "_tool_manager", None)
		    if tool_mgr and hasattr(tool_mgr, "_tools"):
		        tools = tool_mgr._tools
		        logger.info(f"Found {len(tools)} tools in {name}")
		        self.registry._tool_manager._tools.update(tools)
		
		    # Prompts
		    prompt_mgr = getattr(inst, "_prompt_manager", None)
		    if prompt_mgr and hasattr(prompt_mgr, "_prompts"):
		        prompts = prompt_mgr._prompts
		        logger.info(f"Found {len(prompts)} prompts in {name}")
		        self.registry._prompt_manager._prompts.update(prompts)
		
		# Final counts
		tools_count = len(getattr(self.registry._tool_manager, "_tools", []))
		prompts_count = len(getattr(self.registry._prompt_manager, "_prompts", []))
		
		logger.info(f"Registry has {tools_count} tools and {prompts_count} prompts")
		logger.info("Registry Initialization complete")
		
		self.is_initialized = True

    def get_registry(self) -> FastMCP:
        """Returns the initialized tool registry."""
        return self.registry

    def get_all_tags(self) -> Set[str]:
        """Returns the pre-computed set of all tool tags"""
        return self.all_tags    
```

Creating the MCP Server
```python
import anyio
from servers.tool_registry import MCPServerRegistry
from config import get_settings

settings = get_settings()

def main():
    mcp_tool_manager = MCPServerRegistry()
    anyio.run(mcp_tool_manager.initialize)

    mcp_tool_manager.get_registry().run(
        transport = "streamable-http",
        host = "localhost",
        port = settings.REGISTRY_PORT,
    )

if __name__ == "__main__":
    main()
```

Making of Connection Manager
```python
from config import get_settings
from contextlib import AsyncExitStack
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client

settings = get_settings()

AVAILABLE_SERVERS = {
    "tool-registry": {
                        "type": "streamable-http", 
                        "url": settings.TOOL_REGISTRY_URL
                    }
}

class ConnectionManager:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.is_initialized = False
        
	async def connect_to_server(self, server_key: str):
        config = AVAILABLE_SERVERS[server_key]

        if config["type"] == "stdio":
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(StdioServerParameters(command="python", args=[config["path"]]))
            )
            self.session = await self.exit_stack.enter_async_context(ClientSession(*stdio_transport))

        elif config["type"] == "streamable-http":
            context = streamablehttp_client(url=config["url"], headers=config.get("headers"))
            print(f"Connecting to SSE server '{server_key}' with streamablehttp_client...")

            read_stream, write_stream, get_session_id = await self.exit_stack.enter_async_context(context)
            await self._run_session(read_stream, write_stream, get_session_id)

        await self.session.initialize()

        try:
            tools = await self.session.list_tools()
            print(f"🔧 Tools available for {server_key}:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
        except Exception as e:
            print(f"(No tools found or error fetching tools: {e})")

        try:
            prompts = await self.session.list_prompts()
            print(f"📝 Prompts available for {server_key}:")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}")
        except Exception as e:
            print(f"(No prompts found or error fetching prompts: {e})")

    async def _run_session(self, read_stream, write_stream, get_session_id):
        print("🤝 Initializing MCP session...")

        session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        self.session = session

        print("⚡ Starting session initialization...")

        await session.initialize()

        print("✨ Session initialization complete!")
        print(f"\n✅ Connected to MCP server")
        
        if get_session_id:
            session_id = get_session_id()
            if session_id:
                print(f"Session ID: {session_id}")
                
    async def get_mcp_tools(self):
        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, function_name, function_args):
        return await self.session.call_tool(
                function_name, arguments=dict(function_args)
            )

    async def get_prompt(self, name, args):
        return await self.session.get_prompt(name, args)

    async def cleanup_all(self):
        await self.exit_stack.aclose()

    async def initialize_all(self):
        await self.connect_to_server('tool-registry')
        self.is_initialized = True
```

Making MCP host

```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_host")

settings = get_settings()

SKIPPABLE_PROPS = ["additional_properties", "additionalProperties", "$schema"]
MAX_LLM_CALLS = 5
```
---
Helper: `strip_additional_properties`

```python
def strip_additional_properties(schema: dict) -> dict[Any, dict] | list[dict] | dict | list:
    if isinstance(schema, dict):
        return {
            k: strip_additional_properties(v)
            for k, v in schema.items()
            if k not in SKIPPABLE_PROPS
        }
    elif isinstance(schema, list):
        return [strip_additional_properties(item) for item in schema]
    else:
        return schema
```

- Recursively removes keys in `SKIPPABLE_PROPS` from nested dicts/lists.
- Used to clean up tool input schemas before sending them to the LLM / SDK (reduces noise / non-serializable fields).
- Returns the same structure but with unwanted keys pruned.
---
`MCPHost` class — constructor

```python
class MCPHost:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.connection_manager = ConnectionManager()
        self.thread_id = str(uuid.uuid4())
```

- Holds the model name and GenAI client instance (constructed from `GOOGLE_API_KEY`).
- Owns a `ConnectionManager` instance — central point to access MCP tools, prompts and to call tools.
- `thread_id` is a unique ID for this host instance (useful in logging/tracing).
---
Lifecycle helpers: `initialize` and `cleanup`

```python
    async def initialize(self):
        await self.connection_manager.initialize_all()
```

- Awaits initialization of all upstream connections (MCP instances, DBs, external services) managed by `ConnectionManager`.

```python
    async def cleanup(self):
        await self.connection_manager.cleanup_all()
```

- Clean shutdown / resource release (close sockets, clear pools, etc.).
---
Prompt / tools accessors

```python
    async def get_system_prompt(self, name, args) -> str:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        return await self.connection_manager.get_prompt(name, args)
```

- Retrieves a system prompt (delegates to `ConnectionManager`).
- Guards against calling it before `initialize()`.

```python
    async def get_mcp_tools(self) -> list[Tool]:
        tools = await self.connection_manager.get_mcp_tools()

        return [
            types.Tool(
                function_declarations=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": strip_additional_properties(
                            {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in SKIPPABLE_PROPS
                            }
                        ),
                    }
                ]
            )
            for tool in tools
        ]
```

- Queries `ConnectionManager` for registered MCP tools.
- Converts each tool into a `types.Tool` instance (GenAI SDK) with `function_declarations`.
    
- The `parameters` field is sanitized (strip unwanted schema props) so the LLM sees a clean function schema.
- This is how runtime tools become visible to the model for tool-calls.

```python
    async def call_tool(self, function_name: str, function_args: dict):
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        return await self.connection_manager.call_tool(function_name, function_args)
```

- Simple wrapper delegating to `ConnectionManager.call_tool`.
---
Main orchestration: `process_query`

This is the most important function — it sends the user query to the LLM, handles tool calls the LLM requests, and continues until a final text response is produced or `MAX_LLM_CALLS` is reached.

Key parts:

```python
    async def process_query(self, query: str) -> str:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        
        tools = await self.get_mcp_tools()
        config = types.GenerateContentConfig(temperature=0, tools=tools)

        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )
        ]

        llm_calls = 0
```

- Guard for initialized connections.
- Fetches tools and builds a `GenerateContentConfig` including tools and deterministic `temperature=0`.
- Starts conversation `contents` with the user message packaged into `types.Content` / `types.Part`.

Loop & LLM call:

```python
        while llm_calls < MAX_LLM_CALLS:
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
            except Exception as e:
                logger.error(f"Error during LLM call: {e}")
                raise e
            
            llm_calls += 1
            contents.append(response.candidates[0].content)
```

- Calls the GenAI `generate_content` API synchronously (note: your method is `async` but `self.client.models.generate_content(...)` looks blocking — check the GenAI SDK for async clients; if it's sync you may need a thread executor).
- Appends the model response to `contents` so follow-up calls see the full conversation.

Function call handling:

```python
            function_call_found = False

            for part in response.candidates[0].content.parts:
                if getattr(part, "function_call", None):
                    function_call_found = True
                    function_call = part.function_call
                    try:
                        result = await self.connection_manager.call_tool(
                            function_call.name, dict(function_call.args)
                        )
                    except Exception as e:
                        logger.error(f"Error during tool call '{function_call.name}': {e}")
                        result = f"[Error during tool call: {e}]"
                    function_response_part = types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result},
                    )
                    contents.append(types.Content(role="user", parts=[function_response_part]))
```

- Iterates over `parts` of the candidate content searching for `function_call` objects.
- If found:
    - Calls the named function through `ConnectionManager` (awaitable).
    - Packages the tool output into a `Part` (via `from_function_response`) and appends it to `contents` as a new user content item — this feeds the result back to the LLM so it can continue reasoning.
- On tool errors, you log and synthesize an error-string so the LLM can see the failure (so it can decide to retry, fall back, or explain).

Final text extraction and return:

```python
            if not function_call_found:
                parts = response.candidates[0].content.parts
                text_result = "".join([p.text for p in parts if hasattr(p, 'text') and p.text])
                logger.info(f"Final response after {llm_calls} LLM calls: {text_result}")
                return text_result 
```

- If the model didn't request any function call in this response, the code assumes the model produced a final textual answer, extracts all `text` from parts and returns it.

End of loop guard:

```python
        logger.error("Maximum LLM call limit reached without a final answer.")
        return None
```

- If loop exhausts `MAX_LLM_CALLS`, logs error and returns `None`. (Return type says `-> str` but you may return `None` — consider typing `-> Optional[str]`.)
---
Notes, potential improvements & gotchas

- **Async vs sync:** Ensure `genai.Client` methods are async if you intend to `await` them. If `generate_content` is blocking, wrap it in `run_in_executor` or use the SDK's async client.
    
- **Typing:** `process_query` can return `None`; update return annotation to `Optional[str]`.
    
- **Retry/backoff:** On transient LLM errors, consider retry/backoff rather than raising immediately.
    
- **Tool schema sanitization:** You already clean `parameters`, good. Validate `tool.inputSchema` exists and is structured as expected.
    
- **Security:** Be careful serializing tool results back to the model if results contain secrets.
    
- **Logging:** You log the final text — consider redacting sensitive outputs in production.
    
- **Tool collisions:** If multiple tools share the same `name`, the SDK may confuse them. Ensure unique names.
    
- **Edge cases:** If `response.candidates` is empty or malformed, code will raise. Add guard checks.
---
## Notes & Recommendations

> [!warning] Potential Issues & Improvements
> 
> - generate_content may be **synchronous** — wrap in anyio.to_thread.run_sync if needed
> - Return type of process_query should be -> Optional[str]
> - Add retry logic for transient LLM/tool errors
> - Sanitize tool outputs before sending back to LLM (avoid leaking secrets)
> - Ensure all tool names are globally unique across MCPs
> - Add proper error handling for empty candidates

> [!tip] Best Practices Implemented
> 
> - Clean schema sanitization with strip_additional_properties
> - Proper async lifecycle management
> - Centralized connection & tool registry
> - Temperature=0 for deterministic tool use
> - Graceful tool error fallback