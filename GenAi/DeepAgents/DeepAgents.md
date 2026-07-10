## How does it work?
Your deep agent automatically:
1. **Plans its approach** using the built-in [`write_todos`](https://docs.langchain.com/oss/python/deepagents/harness#to-do-list-tracking) tool to break down the research task.
2. **Conducts research** by calling the `internet_search` tool to gather information.
3. **Manages context** by using file system tools ([`write_file`](https://docs.langchain.com/oss/python/deepagents/harness#file-system-access), [`read_file`](https://docs.langchain.com/oss/python/deepagents/harness#file-system-access)) to offload large search results.
4. **Spawns subagents** as needed to delegate complex subtasks to specialized subagents.
5. **Synthesizes a report** to compile findings into a coherent response.

```python
print(result["messages"][-1].content)
```
## Streaming
Deep agents have built-in [streaming](https://docs.langchain.com/oss/python/langchain/streaming/overview) for real-time updates from agent execution using LangGraph. This allows you to observe output progressively and review and debug agent and subagent work, such as tool calls, tool results, and LLM responses.
#### Backends
- Deep agent tools can make use of virtual file systems to store, access, and edit files. 
- By default, deep agents use a `StateBackend`.
- If you are using [skills](https://docs.langchain.com/oss/python/deepagents/customization#skills) or [memory](https://docs.langchain.com/oss/python/deepagents/customization#memory), you must add the expected skill or memory files to the backend before creating the agent.

StateBackend
An ephemeral filesystem backend stored in `langgraph` state.
This filesystem only persists _for a single thread_.
```python
# By default we provide a StateBackend
agent = create_deep_agent()

# Under the hood, it looks like
from deepagents.backends import StateBackend

agent = create_deep_agent(
    backend=(lambda rt: StateBackend(rt))   # Note that the tools access State through the runtime.state
)
```

FileSystemBackend
The local machine’s filesystem.
```python
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir=".", 
    virtual_mode=True)
)
```

LocalShellBackend
A filesystem with shell execution directly on the host. 
Provides filesystem tools plus the `execute` tool for running commands.
```python
from deepagents.backends import LocalShellBackend

agent = create_deep_agent(
    backend=LocalShellBackend(root_dir=".", 
    env={"PATH": "/usr/bin:/bin"})
)
```

CompositeBackend
A flexible backend where you can specify different routes in the filesystem to point towards different backends.
```python
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

composite_backend = lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={
        "/memories/": StoreBackend(rt),
    }
)

agent = create_deep_agent(
    backend=composite_backend,
    store=InMemoryStore()  # Store passed to create_deep_agent, not backend
)
```

Sandboxes
- Sandboxes are specialized [backends](https://docs.langchain.com/oss/python/deepagents/backends) that run agent code in an isolated environment with their own filesystem and an `execute` tool for shell commands. 
- Use a sandbox backend when you want your deep agent to write files, install dependencies, and run commands without changing anything on your local machine.
```python
pip install langchain-modal

import modal
from langchain_anthropic import ChatAnthropic

from deepagents import create_deep_agent
from langchain_modal import ModalSandbox

app = modal.App.lookup("your-app")
modal_sandbox = modal.Sandbox.create(app=app)
backend = ModalSandbox(sandbox=modal_sandbox)

agent = create_deep_agent(
    model=ChatAnthropic(model="claude-sonnet-4-20250514"),
    system_prompt="You are a Python coding assistant with sandbox access.",
    backend=backend,
)
try:
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Create a small Python package and run pytest",
                }
            ]
        }
    )
finally:
    modal_sandbox.terminate()
```

#### HITL
```python
# Checkpointer is REQUIRED for human-in-the-loop 
checkpointer = MemorySaver() 

agent = create_deep_agent(model="claude-sonnet-4-6", 
	tools=[delete_file, read_file, send_email], 
	interrupt_on={ "delete_file": True, # Default: approve, edit, reject 
	"read_file": False, # No interrupts needed 
	"send_email": {"allowed_decisions": ["approve", "reject"]},# No editing }, 
	checkpointer=checkpointer # Required! 
)
```

#### SKILLS
- Skills can contain detailed instructions on how to complete tasks, reference info, and other assets, such as templates. 
- These files are only loaded by the agent when the agent has determined that the skill is useful for the current prompt. 
- This progressive disclosure reduces the amount of tokens and context the agent has to consider upon startup.

To add skills to your deep agent, pass them as an argument to `create_deep_agent`:

```python
from urllib.request import urlopen
from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

skill_url = "https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/libs/cli/examples/skills/langgraph-docs/SKILL.md"

with urlopen(skill_url) as response:
    skill_content = response.read().decode('utf-8')

skills_files = {
    "/skills/langgraph-docs/SKILL.md": create_file_data(skill_content)
}

agent = create_deep_agent(
    skills=["/skills/"],
    checkpointer=checkpointer,
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is langgraph?",
            }
        ],
        # Seed the default StateBackend's in-state filesystem (virtual paths must start with "/").
        "files": skills_files
    },
    config={"configurable": {"thread_id": "12345"}},
)
```

### Memory
Use [`AGENTS.md` files](https://agents.md/) to provide extra context to your deep agent.You can pass one or more file paths to the `memory` parameter when creating your deep agent:
```python
from urllib.request import urlopen

from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver

with urlopen("https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/examples/text-to-sql-agent/AGENTS.md") as response:
    agents_md = response.read().decode("utf-8")
checkpointer = MemorySaver()

agent = create_deep_agent(
    memory=[
        "/AGENTS.md"
    ],
    checkpointer=checkpointer,
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Please tell me what's in your memory files.",
            }
        ],
        # Seed the default StateBackend's in-state filesystem (virtual paths must start with "/").
        "files": {"/AGENTS.md": create_file_data(agents_md)},
    },
    config={"configurable": {"thread_id": "123456"}},
)
```

#### Structured Output
Deep agents support [structured ouput](https://docs.langchain.com/oss/python/langchain/structured-output). 
- You can set a desired structured output schema by passing it as the `response_format` argument to the call to `create_deep_agent()`. 
- When the model generates the structured data, it’s captured, validated, and returned in the ‘structured_response’ key of the deep agent’s state.
```python
class WeatherReport(BaseModel): 
"""A structured weather report with current conditions and forecast.""" 
	location: str = Field(description="The location for this weather report") 
	temperature: float = Field(description="Current temperature in Celsius") 
	condition: str = Field(description="Current weather condition (e.g., sunny, cloudy, rainy)") 
	humidity: int = Field(description="Humidity percentage")  
	wind_speed: float = Field(description="Wind speed in km/h") 
	forecast: str = Field(description="Brief forecast for the next 24 hours") 
	
agent = create_deep_agent(response_format=WeatherReport, 
						tools=[internet_search] )
```