### Subagents
- a central main [agent](https://docs.langchain.com/oss/python/langchain/agents) (often referred to as a **supervisor**) coordinates subagents by calling them as [tools](https://docs.langchain.com/oss/python/langchain/tools).
- The main agent decides which subagent to invoke, what input to provide, and how to combine results.
- Subagents are stateless—they don’t remember past interactions, with all conversation memory maintained by the main agent.
- This provides [context](https://docs.langchain.com/oss/python/langchain/context-engineering) isolation: each subagent invocation works in a clean context window, preventing context bloat in the main conversation.

![[Pasted image 20260217030956.png]]

Key characteristics:
- Centralized control: all routing passes through the main agent
- No direct user interaction: Subagents return results to the main agent, not the user (though you can use [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts#interrupt) within a subagent to allow user interaction)
- Subagents via tools: Subagents are invoked via tools
- Parallel execution: The main agent can invoke multiple subagents in a single turn

>[!warning]
**Subgraph state inspection may not be available with this pattern.** LangGraph can only inspect subgraph state for subgraphs it can [statically discover](https://docs.langchain.com/oss/python/langgraph/use-subgraphs#view-subgraph-state). Because subagents are called inside tool functions, they are not statically discoverable, so [`get_state` with `subgraphs`](https://docs.langchain.com/oss/python/langgraph/use-subgraphs#view-subgraph-state) will not return subagent state. If you need to read nested graph state (e.g., during an [interrupt](https://docs.langchain.com/oss/python/langgraph/interrupts#interrupt)), invoke the subagent from a [node function](https://docs.langchain.com/oss/python/langgraph/use-subgraphs#invoke-a-graph-from-a-node) in a custom graph instead.

>[!tip]
**Supervisor vs. Router**: A supervisor agent (this pattern) is different from a [router](https://docs.langchain.com/oss/python/langchain/multi-agent/router). 
The supervisor is a full agent that maintains conversation context and dynamically decides which subagents to call across multiple turns. 
A router is typically a single classification step that dispatches to agents without maintaining ongoing conversation state.

## When to use
Use the subagents pattern when you have multiple distinct domains (e.g., calendar, email, CRM, database), subagents don’t need to converse directly with users, or you want centralized workflow control

>[!tip]
>**Need user interaction within a subagent?** While subagents typically return results to the main agent rather than conversing directly with users, you can use [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts#interrupt) within a subagent to pause execution and gather user input. This is useful when a subagent needs clarification or approval before proceeding. The main agent remains the orchestrator, but the subagent can collect information from the user mid-task.

Example: [[Langchain.Multi Agent Example]]

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a subagent
subagent = create_agent(model="anthropic:claude-sonnet-4-20250514", tools=[...])

# Wrap it as a tool
@tool("research", description="Research a topic and return findings")
def call_research_agent(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool
main_agent = create_agent(model="anthropic:claude-sonnet-4-20250514", tools=[call_research_agent])
```
---
#### Design Decisions
When implementing the subagents pattern, you’ll make several key design choices.

| Decision                                                                                                       | Options                                                                                |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [**Sync vs. async**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#sync-vs-async)      | Sync (blocking) vs. async (background)                                                 |
| [**Tool patterns**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#tool-patterns)       | Tool per agent vs. single dispatch tool                                                |
| [**Subagent specs**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#subagent-specs)     | System prompt vs. enum constraint vs. tool-based discovery (single dispatch tool only) |
| [**Subagent inputs**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#subagent-inputs)   | Query only vs. full context                                                            |
| [**Subagent outputs**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#subagent-outputs) | Subagent result vs full conversation history                                           |

---
## Sync vs. async

Subagent execution can be **synchronous** (blocking) or **asynchronous**
(background). 
Your choice depends on whether the main agent needs the result to continue.

| Mode      | Main agent behavior                         | Best for                               | Tradeoff                            |
| --------- | ------------------------------------------- | -------------------------------------- | ----------------------------------- |
| **Sync**  | Waits for subagent to complete              | Main agent needs result to continue    | Simple, but blocks the conversation |
| **Async** | Continues while subagent runs in background | Independent tasks, user shouldn’t wait | Responsive, but more complex        |
>[!tip]
>Not to be confused with Python’s `async`/`await`. Here, “async” means the main agent kicks off a background job (typically in a separate process or service) and continues without blocking.

Sync (default)
- By default, subagent calls are **synchronous**—the main agent waits for each subagent to complete before continuing.
- Use sync when the main agent’s next action depends on the subagent’s result.
![[Pasted image 20260217031949.png]]

**When to use sync:**
- Main agent needs the subagent’s result to formulate its response
- Tasks have order dependencies (e.g., fetch data → analyze → respond)
- Subagent failures should block the main agent’s response

**Tradeoffs:**
- Simple implementation—just call and wait
- User sees no response until all subagents complete
- Long-running tasks freeze the conversation

Async
- Use **asynchronous execution** when the subagent’s work is independent—the main agent doesn’t need the result to continue conversing with the user.
- The main agent kicks off a background job and remains responsive.
![[Pasted image 20260217032142.png]]

**When to use async:**

- Subagent work is independent of the main conversation flow
- Users should be able to continue chatting while work happens
- You want to run multiple independent tasks in parallel

**Three-tool pattern:**

1. **Start job**: Kicks off the background task, returns a job ID
2. **Check status**: Returns current state (pending, running, completed, failed)
3. **Get result**: Retrieves the completed result

**Handling job completion:** When a job finishes, your application needs to notify the user. One approach: surface a notification that, when clicked, sends a `HumanMessage` like “Check job_123 and summarize the results.”

---
#### Tool Patterns
There are two main ways to expose subagents as tools:

|Pattern|Best for|Trade-off|
|---|---|---|
|[**Tool per agent**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#tool-per-agent)|Fine-grained control over each subagent’s input/output|More setup, but more customization|
|[**Single dispatch tool**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#single-dispatch-tool)|Many agents, distributed teams, convention over configuration|Simpler composition, less per-agent customization|

Tool per agent
![[Pasted image 20260217032401.png]]

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a sub-agent
subagent = create_agent(model="...", tools=[...])  

# Wrap it as a tool
@tool("subagent_name", description="subagent_description")  
def call_subagent(query: str):  
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool
main_agent = create_agent(model="...", tools=[call_subagent])
```


### Single Dispatch Tool
Think of the **Single Dispatch Tool** as a **"Universal Remote"** instead of having a separate remote for every device in your house.

Here is the simpler breakdown:
#### 1. The Old Way (Tool per Agent)
Imagine a manager (the Coordinator Agent) who has a desk full of specific "buttons":

- Button A: "Summon the Writer Agent"
- Button B: "Summon the Coder Agent"
- Button C: "Summon the Researcher Agent"

If you hire a new "Math Agent," you have to physically install a **new button** (write new code) on the manager's desk. This gets messy fast.

### 2. The New Way (Single Dispatch)
Now, imagine the manager has just **one phone** (the Single Dispatch Tool).

To get help, the manager just picks up the phone and says:

> _"Connect me to [Agent Name] and tell them [Instructions]."_

- **The Mechanism:** The manager doesn't need a special button for everyone. It just uses one generic tool—let's call it `delegate_task`.
    
- **The Input:** It passes two things:
    1. **Who** to call (e.g., "Research_Team").
    2. **What** to do (e.g., "Find the price of gold in 2022").
### Why is this better?
1. **Context Hygiene (The "Clean Desk" Policy):**
    When the sub-agent (e.g., the Researcher) picks up the phone, they **don't** see the manager's entire messy conversation history. They start fresh, do their one job, send back the answer, and hang up. This saves "tokens" and prevents confusion.
    
2. **Scalability (Plug-and-Play):**
    You can add 50 new specialized agents (a Math agent, a Translation agent, etc.) without ever touching the manager's code. As long as the manager knows their names, it can call them using the same phone.
    
3. **Teamwork:**
    Team A can build the "Coder Agent" and Team B can build the "Writer Agent" completely separately. The manager just calls them when needed.

![[Pasted image 20260217033113.png]]

**Key characteristics:**

- Single task tool: One parameterized tool that can invoke any registered sub-agent by name
- Convention-based invocation: Agent selected by name, task passed as human message, final message returned as tool result
- Team distribution: Different teams can develop and deploy agents independently
- Agent discovery: Sub-agents can be discovered via system prompt (listing available agents) or through [progressive disclosure](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant) (loading agent information on-demand via tools)

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Sub-agents developed by different teams
research_agent = create_agent(
    model="gpt-4.1",
    prompt="You are a research specialist..."
)

writer_agent = create_agent(
    model="gpt-4.1",
    prompt="You are a writing specialist..."
)

# Registry of available sub-agents
SUBAGENTS = {
    "research": research_agent,
    "writer": writer_agent,
}

@tool
def task(
    agent_name: str,
    description: str
) -> str:
    """Launch an ephemeral subagent for a task.

    Available agents:
    - research: Research and fact-finding
    - writer: Content creation and editing
    """
    agent = SUBAGENTS[agent_name]
    result = agent.invoke(
    {
        "messages": [
            {
	            "role": "user", 
	            "content": description
			}
        ]
    })
    return result["messages"][-1].content

# Main coordinator agent
main_agent = create_agent(
    model="gpt-4.1",
    tools=[task],
    system_prompt=(
        "You coordinate specialized sub-agents. "
        "Available: research (fact-finding), "
        "writer (content creation). "
        "Use the task tool to delegate work."
    ),
)
```

----
## Context engineering
Control how context flows between the main agent and its subagents:

|Category|Purpose|Impacts|
|---|---|---|
|[**Subagent specs**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#subagent-specs)|Ensure subagents are invoked when they should be|Main agent routing decisions|
|[**Subagent inputs**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#subagent-inputs)|Ensure subagents can execute well with optimized context|Subagent performance|
|[**Subagent outputs**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents#subagent-outputs)|Ensure the supervisor can act on subagent results|Main agent performance|

#### Subagent specs
- The **names** and **descriptions** associated with subagents are the primary way the main agent knows which subagents to invoke
- These are prompting levers—choose them carefully.

- **Name**: How the main agent refers to the sub-agent. Keep it clear and action-oriented (e.g., `research_agent`, `code_reviewer`).
- **Description**: What the main agent knows about the sub-agent’s capabilities. Be specific about what tasks it handles and when to use it.

>[!tip]
>For the single dispatch tool design, you must additionally provide the main agent with info about the subagents it can invoke. You can provide this info in diff ways based on the number of agents and whether your registry is static or dynamic:

| Method                        | Best for                                | Tradeoff                                                             |
| ----------------------------- | --------------------------------------- | -------------------------------------------------------------------- |
| **System prompt enumeration** | Small, static agent lists (< 10 agents) | Simple, but requires prompt updates when agents change               |
| **Enum constraint**           | Small, static agent lists (< 10 agents) | Type-safe and explicit, but requires code changes when agents change |
| **Tool-based discovery**      | Large or dynamic agent registries       | Flexible and scalable, but adds complexity                           |

#### System prompt enumeration
List available agents directly in the main agent’s system prompt. The main agent sees the list of agents and their descriptions as part of its instructions.

**When to use:**
- You have a small, fixed set of agents (< 10)
- Agent registry rarely changes
- You want the simplest implementation

```python
main_agent = create_agent(
    model="...",
    tools=[task],
    system_prompt=(
        "You coordinate specialized sub-agents. "
        "Available agents:\n"
        "- research: Research and fact-finding\n"
        "- writer: Content creation and editing\n"
        "- reviewer: Code and document review\n"
        "Use the task tool to delegate work."
    ),
)
```

#### Enum constraint on dispatch tool

Add an enum constraint to the `agent_name` parameter in your dispatch tool. This provides type safety and makes available agents explicit in the tool schema.

**When to use:**
- You have a small, fixed set of agents (< 10)
- You want type safety and explicit agent names
- You prefer schema-based validation over prompt-based guidance

```python
from enum import Enum

class AgentName(str, Enum):
    RESEARCH = "research"
    WRITER = "writer"
    REVIEWER = "reviewer"

@tool
def task(
    agent_name: AgentName,  # Enum constraint
    description: str
) -> str:
    """Launch an ephemeral subagent for a task."""
    # ...
```

#### Tool-based discovery
Provide a separate tool (e.g., `list_agents` or `search_agents`) that the main agent can call to discover available agents on-demand. 
This enables progressive disclosure and supports dynamic registries.

**When to use:**
- You have many agents (> 10) or a growing registry
- Agent registry changes frequently or is dynamic
- You want to reduce prompt size and token usage
- Different teams manage different agents independently

```python
@tool
def list_agents(query: str = "") -> str:
    """List available subagents, optionally filtered by query."""
    agents = search_agent_registry(query)
    return format_agent_list(agents)

@tool
def task(agent_name: str, description: str) -> str:
    """Launch an ephemeral subagent for a task."""
    # ...

main_agent = create_agent(
    model="...",
    tools=[task, list_agents],
    system_prompt="Use list_agents to discover available subagents, then use task to invoke them."
)
```

#### Subagent Inputs
- Customize what context the subagent receives to execute its task.
- Add input that isn’t practical to capture in a static prompt—full message history, prior results, or task metadata—by pulling from the agent’s state.

```python
from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime

class CustomState(AgentState):
    example_state_key: str

@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent1(query: str, runtime: ToolRuntime[None, CustomState]):
    # Apply any logic needed to transform the messages into a suitable input
    subagent_input = some_logic(query, runtime.state["messages"])
    result = subagent1.invoke({
        "messages": subagent_input,
        # You could also pass other state keys here as needed.
        # Make sure to define these in both the main and subagent's
        # state schemas.
        "example_state_key": runtime.state["example_state_key"]
    })
    return result["messages"][-1].content
```

#### Subagent Outputs
Customize what the main agent receives back so it can make good decisions. Two strategies:
1. **Prompt the sub-agent**: Specify exactly what should be returned. A common failure mode is that the sub-agent performs tool calls or reasoning but doesn’t include results in its final message—remind it that the supervisor only sees the final output.
2. **Format in code**: Adjust or enrich the response before returning it.  

For example, pass specific state keys back in addition to the final text using a [`Command`](https://docs.langchain.com/oss/python/langgraph/graph-api#command).

```python
from typing import Annotated
from langchain.agents import AgentState
from langchain.tools import InjectedToolCallId
from langgraph.types import Command


@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent1(
    query: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    result = subagent1.invoke(
	    {
	        "messages": [
		        {
			        "role": "user", 
			        "content": query
				}
			]
	    }
    )
    
    return Command(update = {
        # Pass back additional state from the subagent
        "example_state_key": result["example_state_key"],
        "messages": [
            ToolMessage(
                content = result["messages"][-1].content,
                tool_call_id = tool_call_id
	            )
	        ]
	    }
	)
```