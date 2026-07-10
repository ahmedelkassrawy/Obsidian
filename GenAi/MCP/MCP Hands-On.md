```python
pip install fastmcp
```

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

It may be easier to think of it as an API, but specifically designed for LLM interactions. MCP servers can:
- Expose data through `Resources` (think of these sort of like GET endpoints; they are used to load information into the LLM’s context)
- Provide functionality through `Tools` (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through `Prompts` (reusable templates for LLM interactions)
---
#### Create a FastMCP Server
A FastMCP server is a collection of tools, resources, and other MCP components. To create a server, start by instantiating the `FastMCP` class.
```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
```

---
#### Add a Tool
To add a tool that returns a simple greeting, write a function and decorate it with `@mcp.tool` to register it with the server:
```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
---
#### Tool Naming
FastAPI-MCP uses the `operation_id` from your FastAPI routes as the MCP tool names. When you don’t specify an `operation_id`, FastAPI auto-generates one, but these can be cryptic.
```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

mcp = FastApiMCP(app)
mcp.mount_http()

@app.get("/users/{user_id}",operation_id = "get_user_info")
async def read_user(user_id:int):
    return {"user_id":user_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
---
#### Run the Server
The simplest way to run your FastMCP server is to call its `run()` method. You can choose between different transports, like `stdio` for local servers, or `http` for remote access:

studio
```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

httpx:
```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```
---
#### Call Your Server
Once your server is running with HTTP transport, you can connect to it with a FastMCP client or any LLM client that supports the MCP protocol:
```python
import asyncio 
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name:str):
    async with client:
        result = await client.call_tool("greet",
                                        {"name": name})
        print(result)

asyncio.run(call_tool("Kassra"))
```
---
#### Server
###### Creating
```python
from fastmcp import FastMCP

mcp = FastMCP(name = "MCP-Server")

#optional: MCP with instructions
mcp_with_instructions = FastMCP(
    name = "MCP-Server-With-Instructions",
    instructions = "You are a helpful assistant that always greets the user warmly."
)
```

###### Components
- Tools
- Resources -> expose data sources that client can read
```python
@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}
```

or parametrized
```python
@mcp.resource("users://{userid}/profile")
def get_user_profile(user_id:int) -> dict:
	"""Retrieves a user's profile by ID"""
	return {
		"id":user_id,
		"name":f"User {user_id}",
		"status":"active"
	}
```

- Prompts -> reusable message templates for guiding the LLM
```python
@mcp.prompt
def analyze_data(data_points:list[float]) -> str:
	"""Creates a prompt asking for analysis of numerical data"""
	formatted_data = ", ".join(str(point) for point in data_points)
	return f"Please analyze these data points: {formatted_data}"
```

##### Tag Based Filtering
FastMCP supports tag-based filtering to selectively expose components based on configurable include/exclude tag sets. This is useful for creating different views of your server for different environments or users
```python
@mcp.tool(tags={"public", "utility"})
def public_tool() -> str:
    return "This tool is public"

@mcp.tool(tags={"internal", "admin"})
def admin_tool() -> str:
    return "This tool is for admins only"
```

```python
# Only expose components tagged with "public"
mcp = FastMCP(include_tags={"public"})

# Hide components tagged as "internal" or "deprecated"  
mcp = FastMCP(exclude_tags={"internal", "deprecated"})

# Combine both: show admin tools but hide deprecated ones
mcp = FastMCP(include_tags={"admin"}, exclude_tags={"deprecated"})
```

###### Custom Routes
Adding a simple endpoints like health check that need to be served
```python
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    mcp.run(transport="http",port = 8000)  # Health check at http://localhost:8000/health
```

##### FastAPI and OpenAPI integrations
FastMCP can automatically generate servers from OpenAPI specifications or existing FastAPI applications using `FastMCP.from_openapi()` and `FastMCP.from_fastapi()`. This allows you to instantly convert existing APIs into MCP servers without manual tool creation.
```python
import httpx
from fastmcp import FastMCP
from fastapi import FastAPI

app = FastAPI()
mcp = FastMCP.from_fastapi(app = app)
```

----
#### Tools
Tools in FastMCP transform regular Python functions into capabilities that LLMs can invoke during conversations. When an LLM decides to use a tool:
1. It sends a request with parameters based on the tool’s schema.
2. FastMCP validates these parameters against your function’s signature.
3. Your function executes with the validated inputs.
4. The result is returned to the LLM, which can use it in its response.
This allows LLMs to perform tasks like querying databases, calling APIs, making calculations, or accessing files—extending their capabilities beyond what’s in their training data.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b
```

When this tool is registered, FastMCP automatically:
- Uses the function name (`add`) as the tool name.
- Uses the function’s docstring (`Adds two integer numbers...`) as the tool description.
- Generates an input schema based on the function’s parameters and type annotations.
- Handles parameter validation and error reporting.

The way you define your Python function dictates how the tool appears and behaves for the LLM client.
###### Async support
 Use `anyio` (which FastMCP already uses internally) to wrap them as async functions, for example:

```python
import anyio
from fastmcp import FastMCP

mcp = FastMCP()

def cpu_intensive_task(data: str) -> str:
    # Some heavy computation that could block the event loop
    return processed_data

@mcp.tool
async def wrapped_cpu_task(data: str) -> str:
    """CPU-intensive task wrapped to prevent blocking."""
    return await anyio.to_thread.run_sync(cpu_intensive_task, data)
```

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
@make_async_background
def my_tool() -> None:
    time.sleep(5)
```

###### Type Annotations
MCP tools have typed arguments, and FastMCP uses type annotations to determine those types. Therefore, you should use standard Python type annotations for tool arguments:

```python
@mcp.tool
def analyze_text(
    text: str,
    max_tokens: int = 100,
    language: str | None = None
) -> dict:
    """Analyze the provided text."""
    # Implementation...
```

FastMCP supports a wide range of type annotations, including all Pydantic types:

| Type Annotation   | Example                                   | Description                                                  |
| ----------------- | ----------------------------------------- | ------------------------------------------------------------ |
| Basic types       | `int`, `float`, `str`, `bool`             | Simple scalar values                                         |
| Binary data       | `bytes`                                   | Binary content (raw strings, not auto-decoded base64)        |
| Date and Time     | `datetime`, `date`, `timedelta`           | Date and time objects (ISO format strings)                   |
| Collection types  | `list[str]`, `dict[str, int]`, `set[int]` | Collections of items                                         |
| Optional types    | `float \| None`, `Optional[float]`        | Parameters that may be null/omitted                          |
| Union types       | `str \| int`, `Union[str, int]`           | Parameters accepting multiple types                          |
| Constrained types | `Literal["A", "B"]`, `Enum`               | Parameters with specific allowed values                      |
| Paths             | `Path`                                    | File system paths (auto-converted from strings)              |
| UUIDs             | `UUID`                                    | Universally unique identifiers (auto-converted from strings) |
| Pydantic models   | `UserData`                                | Complex structured data with validation                      |
#### Strict Validation
```python
mcp = FastMCP("StrictServer",strict_input_validation = True)
```

#### Notifications
FastMCP automatically sends `notifications/tools/list_changed` notifications to connected clients when tools are added, removed, enabled, or disabled. This allows clients to stay up-to-date with the current tool set without manually polling for changes.
```python
@mcp.tool
def example_tool() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_tool(example_tool)     # Sends tools/list_changed notification
example_tool.disable()         # Sends tools/list_changed notification  
example_tool.enable()          # Sends tools/list_changed notification
mcp.remove_tool("example_tool") # Sends tools/list_changed notification
```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.
#### Remove Tools
```python
from fastmcp import FastMCP

mcp = FastMCP(name="DynamicToolServer")

@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

mcp.remove_tool("calculate_sum")
```

---
#### Resources
###### Accessing MCP Content
Resources and resource templates can access additional MCP information and features through the `Context` object. To access it, add a parameter to your resource function with a type annotation of `Context`:
```python
from fastmcp import FastMCP, Context

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://system-status")
async def get_system_status(ctx: Context) -> dict:
    """Provides system status information."""
    return {
        "status": "operational",
        "request_id": ctx.request_id
    }

@mcp.resource("resource://{name}/details")
async def get_details(name: str, ctx: Context) -> dict:
    """Get details for a specific name."""
    return {
        "name": name,
        "accessed_at": ctx.request_id
    }
```

##### Async Resources
Use `async def` for resource functions that perform I/O operations (e.g., reading from a database or network) to avoid blocking the server.
```python
import aiofiles
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

@mcp.resource("file:///app/data/important_log.txt", mime_type="text/plain")
async def read_important_log() -> str:
    """Reads content from a specific log file asynchronously."""
    try:
        async with aiofiles.open("/app/data/important_log.txt", mode="r") as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        return "Log file not found."
```
##### Notifications
```python
@mcp.resource("data://example")
def example_resource() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_resource(example_resource)  # Sends resources/list_changed notification
example_resource.disable()          # Sends resources/list_changed notification  
example_resource.enable()           # Sends resources/list_changed notification
```

----
#### Client
###### Tools Access
```python
async def example():
    client = Client("my_mcp_server.py")
    
    # Connection established here
    async with client:
        print(f"Connected: {client.is_connected()}")
        
        # Make multiple calls within the same session
        tools = await client.list_tools()
        result = await client.call_tool("greet", {"name": "World"})
        
    # Connection closed automatically here
    print(f"Connected: {client.is_connected()}")
```

```python
async with client:
    # List available tools
    tools = await client.list_tools()
    
    # Execute a tool
    result = await client.call_tool("multiply", {"a": 5, "b": 3})
    print(result.data)  # 15
```

##### Resources
```python
async with client:
    # List available resources
    resources = await client.list_resources()
    
    # Read a resource
    content = await client.read_resource("file:///config/settings.json")
    print(content[0].text)
```

##### Prompts
```python
async with client:
    # List available prompts
    prompts = await client.list_prompts()
    
    # Get a rendered prompt
    messages = await client.get_prompt("analyze_data", {"data": [1, 2, 3]})
    print(messages.messages)
```

##### Server Connectivity
```python
async with client:
    await client.ping()
    print("Server is reachable")
```
---
#### FastAPI
FastAPI + MCP in one program
```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP
from fastapi import FastAPI

# 1. Generate MCP server from your API
mcp = FastMCP.from_fastapi(app=app, name="E-commerce MCP")

# 2. Create the MCP's ASGI app
mcp_app = mcp.http_app(path='/mcp')

# 3. Create a new FastAPI app that combines both sets of routes
combined_app = FastAPI(
    title="E-commerce API with MCP",
    routes=[
        *mcp_app.routes,  # MCP routes
        *app.routes,      # Original API routes
    ],
    lifespan=mcp_app.lifespan,
)

# Now you have:
# - Regular API: http://localhost:8000/products
# - LLM-friendly MCP: http://localhost:8000/mcp
# Both served from the same FastAPI application!
```

##### Adding MCP servers to existing FastAPI app
### Basic Mounting
To mount an MCP server, you can use the `http_app` method on your FastMCP instance. This will return an ASGI application that can be mounted to your FastAPI application.
```python
from fastmcp import FastMCP
from fastapi import FastAPI

# Create MCP server
mcp = FastMCP("Analytics Tools")

@mcp.tool
def analyze_pricing(category: str) -> dict:
    """Analyze pricing for a category."""
    products = [p for p in products_db.values() if p.category == category]
    if not products:
        return {"error": f"No products in {category}"}
    
    prices = [p.price for p in products]
    return {
        "category": category,
        "avg_price": round(sum(prices) / len(prices), 2),
        "min": min(prices),
        "max": max(prices),
    }

# Create ASGI app from MCP server
mcp_app = mcp.http_app(path='/mcp')

# Key: Pass lifespan to FastAPI
app = FastAPI(title="E-commerce API", lifespan=mcp_app.lifespan)

# Mount the MCP server
app.mount("/analytics", mcp_app)

# Now: API at /products/*, MCP at /analytics/mcp/
```

- Always pass the lifespan context
- Operations IDS
FastAPI operation IDs become MCP component names. Always specify meaningful operation IDs:
```python
# Good - explicit operation_id
@app.get("/users/{user_id}", operation_id="get_user_by_id")
def get_user(user_id: int):
    return {"id": user_id}

# Less ideal - auto-generated name
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```
---
#### Deployment Cloud
[FastMCP Cloud - FastMCP](https://gofastmcp.com/deployment/fastmcp-cloud)