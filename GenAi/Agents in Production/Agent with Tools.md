# Multi-User Agent Arcade Tutorial Study Guide

> **Source**: `multiuser-agent-arcade.ipynb`  
> **Purpose**: Learn to build secure, multi-user agents with Arcade.dev and LangGraph, focusing on secure tool-calling, authentication, and human-in-the-loop (HITL) safety mechanisms.

---

## Overview

This tutorial bridges the gap between demo and production-grade AI agents by demonstrating **secure tool-calling** for multiple users. It uses **Arcade.dev** for unified tool execution and **LangGraph** for agent orchestration, integrating services like Gmail, Slack, and Notion with safety guardrails.

### Key Learning Objectives
- Build conversational agents with LangGraph.
- Integrate secure tools (Gmail, Slack, Notion) using Arcade.
- Implement human-in-the-loop (HITL) safety controls.
- Manage multi-user authentication and tool execution.

> **Callout: Why This Matters**  
> Scaling AI agents for multiple users requires secure authentication and safety mechanisms to prevent unauthorized access or unintended actions, making this tutorial critical for production-ready systems.

---

## 1. Environment Setup

### 1.1 Dependencies
Install required libraries for agent orchestration and tool integration.

```python
!pip install langgraph langchain-arcade "langchain[openai]"
```

**Key Points**:
- **LangGraph**: Orchestrates agent workflows.
- **LangChain-Arcade**: Integrates Arcade tools with LangChain.
- **LangChain[OpenAI]**: Provides OpenAI model support.

### 1.2 API Key Configuration
Set up API keys for OpenAI and Arcade.
```
```python
import getpass
import os

def _set_env(key: str, default: str | None):
    if key not in os.environ:
        os.environ[key] = default or getpass.getpass(f"{key}:")
_set_env("OPENAI_API_KEY")
_set_env("ARCADE_API_KEY")
```

**Key Points**:
- **OpenAI API Key**: Required for the GPT-5 model.
- **Arcade API Key**: Enables secure tool integration.
- Uses `getpass` to securely input keys without hardcoding.

### 1.3 User Identity
Configure a user ID (email) for Arcade to manage tool authorizations.

```python
_set_env("ARCADE_USER_ID")
```

**Key Points**:
- User ID links to the Arcade account email.
- Ensures secure, user-specific tool access.

> **Tip**: Always protect API keys and user IDs. Avoid hardcoding in production code.

---

## 2. Simple Conversational Agent

### 2.1 Core Implementation
Create a basic conversational agent using LangGraph with memory.

```python
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
import uuid

checkpointer = MemorySaver()
agent_a = create_react_agent(
    model="openai:gpt-5",
    prompt="You are a helpful assistant that can help with everyday tasks. If the user's request is confusing you must ask them to clarify their intent, and fulfill the instruction to the best of your ability. Be concise and friendly at all times.",
    tools=[],
    checkpointer=checkpointer
)
```

**Key Points**:
- **React Agent**: Uses a ReAct (Reasoning + Acting) framework.
- **MemorySaver**: Persists conversation state for context retention.
- **No Tools**: This agent is purely conversational.

### 2.2 Interaction Utility
A utility function to stream and display agent responses.

```python
from langgraph.graph.state import CompiledStateGraph
def run_graph(graph: CompiledStateGraph, config, input):
    for event in graph.stream(input, config=config, stream_mode="values"):
        if "messages" in event:
            event["messages"][-1].pretty_print()
```

**Key Points**:
- Streams agent output for real-time feedback.
- Displays the latest message in each interaction cycle.

### 2.3 Interactive Chat Interface
A loop for user interaction with the agent.

```python
config = {"configurable": {"thread_id": uuid.uuid4()}}
while True:
    user_input = input("👤: ")
    if user_input.lower() == "exit":
        break
    user_message = {"messages": [HumanMessage(content=user_input)]}
    run_graph(agent_a, config, user_message)
```

**Key Points**:
- Uses unique `thread_id` for conversation tracking.
- Exits on "exit" input.
- Maintains memory across interactions.

### 2.4 Testing Limitations
Test the agent’s inability to access external data or authenticated services.

```python
prompt = "what's today's date?"
user_message = {"messages": [HumanMessage(content=prompt)]}
run_graph(agent_a, config, user_message)

prompt = "summarize my latest 3 emails please"
user_message = {"messages": [HumanMessage(content=prompt)]}
run_graph(agent_a, config, user_message)
```

**Key Points**:
- Lacks real-time data access (e.g., current date).
- Cannot access private data (e.g., emails) without authentication.

> **Question to Study**: Why does the basic agent fail to summarize emails?  
> **Answer**: It lacks tools and authentication to access external services like Gmail.

---

## 3. Secure Tool Integration (Gmail)

### 3.1 Arcade Client Setup
Initialize Arcade for tool management.

```python
from langchain_arcade import ToolManager
from arcadepy import Arcade

arcade_client = Arcade(api_key=os.getenv("ARCADE_API_KEY"))
manager = ToolManager(client=arcade_client)
```

**Key Points**:
- **Arcade Client**: Handles authentication and tool execution.
- **ToolManager**: Manages tool initialization and authorization.

### 3.2 Gmail Tool Setup
Add Gmail email-listing capability.

```python
gmail_tool = manager.init_tools(tools=["Gmail_ListEmails"])[0]
```

**Key Points**:
- Initializes the `Gmail_ListEmails` tool.
- Requires user authorization for access.

### 3.3 Authorization Utility
A function to handle OAuth for tools.

```python
def authorize_tool(tool_name, user_id, manager):
    auth_response = manager.authorize(tool_name=tool_name, user_id=user_id)
    if auth_response.status != "completed":
        print(f"The app wants to use the {tool_name} tool.\nPlease click this url to authorize it {auth_response.url}")
        manager.wait_for_auth(auth_response.id)
```

**Key Points**:
- Checks authorization status.
- Provides OAuth URL if needed.
- Waits for user to complete authorization.

### 3.4 Gmail Authorization
Authorize Gmail access.

```python
authorize_tool(gmail_tool.name, os.getenv("ARCADE_USER_ID"), manager)
```

**Key Points**:
- Persists authorization for future sessions.
- Uses Arcade’s OAuth handling for security.

### 3.5 Enhanced Agent with Gmail
Create an agent with Gmail capabilities.

```python
agent_b = create_react_agent(
    model="openai:gpt-5",
    prompt="You are a helpful assistant... Use the Gmail tools that you have to address requests about emails.",
    tools=[gmail_tool],
    checkpointer=checkpointer
)
config = {
    "configurable": {
        "thread_id": uuid.uuid4(),
        "user_id": os.getenv("ARCADE_USER_ID")
    }
}
prompt = "summarize my latest 3 emails please"
user_message = {"messages": [HumanMessage(content=prompt)]}
run_graph(agent_b, config, user_message)
```

**Key Points**:
- Includes `user_id` in config for Arcade tool execution.
- Prompt explicitly mentions Gmail tool usage.
- Successfully summarizes emails post-authorization.

> **Callout: Arcade’s Role**  
> Arcade simplifies OAuth for external services, enabling secure, multi-user tool access without manual token management.

---

## 4. Multi-Service Integration

### 4.1 Batch Authorization
Authorize multiple tools efficiently.

```python
def authorize_tools(tools, user_id, client):
    provider_to_scopes = {}
    for tool in tools:
        provider = tool.requirements.authorization.provider_id
        if provider not in provider_to_scopes:
            provider_to_scopes[provider] = set()
        if tool.requirements.authorization.oauth2.scopes:
            provider_to_scopes[provider] |= set(tool.requirements.authorization.oauth2.scopes)
    for provider, scopes in provider_to_scopes.items():
        auth_response = client.auth.start(user_id=user_id, scopes=list(scopes), provider=provider)
        if auth_response.status != "completed":
            print(f"🔗 Please click here to authorize: {auth_response.url}")
            client.auth.wait_for_completion(auth_response)
```

**Key Points**:
- Groups tools by provider to minimize OAuth flows.
- Handles authorization for multiple services at once.

### 4.2 Tool Suite Setup
Add tools for Gmail, Slack, and Notion.

```python
manager.add_tool("Gmail.SendEmail")
manager.add_toolkit("Slack")
manager.add_toolkit("NotionToolkit")
authorize_tools(tools=manager.definitions, user_id=os.getenv("ARCADE_USER_ID"), client=arcade_client)
```

**Key Points**:
- Adds `Gmail.SendEmail` for sending emails.
- Adds `Slack` and `NotionToolkit` for comprehensive functionality.
- Authorizes all tools in a single flow.

### 4.3 Multi-Service Agent
Create an agent with access to all tools.

```python
agent_c = create_react_agent(
    model="openai:gpt-5",
    prompt="You are a helpful assistant... Use the Gmail tools to address requests about reading or sending emails. Use the Slack tools to address requests about interactions with users and channels in Slack. Use the Notion tools to address requests about managing content in Notion Pages...",
    tools=manager.to_langchain(),
    checkpointer=checkpointer
)
```

**Key Points**:
- Converts Arcade tools to LangChain-compatible format.
- Prompt specifies tool usage for clarity.

### 4.4 Complex Task Execution
Test the agent with a multi-service task.

```python
prompt = "summarize my latest 3 emails, then show me the latest 3 messages in the #general Slack channel, and tell me about the structure of my Notion Workspace"
user_message = {"messages": [HumanMessage(content=prompt)]}
run_graph(agent_c, config, user_message)
```

**Key Points**:
- Orchestrates tasks across Gmail, Slack, and Notion.
- Demonstrates tool selection and execution coordination.

> **Question to Study**: How does the multi-service agent handle complex tasks?  
> **Answer**: It uses the prompt to select the appropriate tool for each task component and coordinates execution via LangGraph.

---

## 5. Human-in-the-Loop (HITL) Safety

### 5.1 Identifying Sensitive Tools
List and classify tools requiring oversight.

```python
for tool_name, _ in manager:
    print(tool_name)

tools_to_protect = [
    "Gmail_SendEmail",
    "Slack_SendDmToUser",
    "Slack_SendMessage",
    "Slack_SendMessageToChannel",
    "NotionToolkit_AppendContentToEndOfPage",
    "NotionToolkit_CreatePage",
]
```

**Key Points**:
- Lists all available tools.
- Identifies tools with external effects (e.g., sending messages, creating content).

### 5.2 HITL Tool Wrapper
Wrap sensitive tools to require user approval.

```python
from typing import Callable, Any
from langchain_core.tools import tool, BaseTool
from langgraph.types import interrupt, Command
from langchain_core.runnables import RunnableConfig
import pprint

def add_human_in_the_loop(target_tool: Callable | BaseTool) -> BaseTool:
    if not isinstance(target_tool, BaseTool):
        target_tool = tool(target_tool)
    @tool(target_tool.name, description=target_tool.description, args_schema=target_tool.args_schema)
    def call_tool_with_interrupt(config: RunnableConfig, **tool_input):
        arguments = pprint.pformat(tool_input, indent=4)
        response = interrupt(f"Do you allow the call to {target_tool.name} with arguments:\n{arguments}")
        if response == "yes":
            tool_response = target_tool.invoke(tool_input, config)
        elif response == "no":
            tool_response = "The User did not allow the tool to run"
        else:
            raise ValueError(f"Unsupported interrupt response type: {response}")
        return tool_response
    return call_tool_with_interrupt
```

**Key Points**:
- Wraps tools to pause execution and request user approval.
- Uses LangGraph’s `interrupt` to halt and resume execution.

### 5.3 Apply Protection
Selectively apply HITL to sensitive tools.

```python
protected_tools = [
    add_human_in_the_loop(t) if t.name in tools_to_protect else t
    for t in manager.to_langchain()
]
```

**Key Points**:
- Protects only specified tools, leaving read-only tools unaffected.
- Balances safety and efficiency.

### 5.4 Interrupt Handling
Handle user decisions for interrupts.

```python
def yes_no_loop(prompt: str) -> str:
    print(prompt)
    user_input = input("Your response [y/n]: ")
    while user_input.lower() not in ["y", "n"]:
        user_input = input("Your response (must be 'y' or 'n'): ")
    return "yes" if user_input.lower() == "y" else "no"

def handle_interrupts(graph: CompiledStateGraph, config):
    for interr in graph.get_state(config).interrupts:
        approved = yes_no_loop(interr.value)
        run_graph(graph, config, Command(resume=approved))
```

**Key Points**:
- `yes_no_loop`: Ensures valid user input (y/n).
- `handle_interrupts`: Processes interrupts and resumes execution.

### 5.5 Protected Agent
Create an agent with HITL-protected tools.

```python
agent_hitl = create_react_agent(
    model="openai:gpt-5",
    prompt="You are a helpful assistant... Use the Gmail tools... Slack tools... Notion tools...",
    tools=protected_tools,
    checkpointer=checkpointer
)
```

**Key Points**:
- Incorporates all tools with selective HITL protection.
- Production-ready with safety controls.

### 5.6 Safety Demonstration
Test HITL with a sensitive action.

```python
prompt = 'send an email with subject "confidential data" and body "this is top secret information" to random-dude@example.com'
user_message = {"messages": [HumanMessage(content=prompt)]}
run_graph(agent_hitl, config, user_message)
handle_interrupts(agent_hitl, config)
```

**Key Points**:
- Interrupts execution to request approval.
- User reviews action details before proceeding.

### 5.7 Complete Interactive System
A full system with HITL controls.

```python
config = {"configurable": {"thread_id": uuid.uuid4()}}
while True:
    user_input = input("👤: ")
    if user_input.lower() == "exit":
        break
    user_message = {"messages": [HumanMessage(content=user_input)]}
    run_graph(agent_hitl, config, user_message)
    handle_interrupts(agent_hitl, config)
```

**Key Points**:
- Combines all features: multi-service tools, memory, and HITL safety.
- User-friendly interface with safety prompts.

> **Callout: HITL Importance**  
> HITL ensures users control sensitive actions (e.g., sending emails), preventing unintended consequences in production systems.

---

## Study Aids

### Key Concepts
- **Arcade.dev**: Simplifies OAuth for secure, multi-user tool access.
- **LangGraph**: Orchestrates agent workflows with memory and interrupts.
- **HITL**: Requires user approval for sensitive actions, enhancing safety.
- **ToolManager**: Manages tool initialization and authorization in Arcade.
- **MemorySaver**: Persists conversation state for context-aware interactions.

### Potential Exam Questions
1. **What problem does Arcade solve in multi-user agent systems?**  
   *Answer*: Arcade provides a unified platform for secure tool execution, handling OAuth flows for multiple users and services, eliminating the need for manual token management.

2. **How does the HITL wrapper ensure safety?**  
   *Answer*: It intercepts sensitive tool calls, pauses execution, and requires user approval via LangGraph interrupts, preventing unintended actions.

3. **Why is `user_id` required in the LangGraph config?**  
   *Answer*: It ensures Arcade executes tools with the correct user’s authorization, maintaining security boundaries.

### Tips for Mastery
- **Practice**: Set up a local environment and run the notebook cells to see the agent in action.
- **Review Code**: Focus on the `add_human_in_the_loop` function to understand interrupt handling.
- **Test Scenarios**: Try different prompts to test tool selection and HITL behavior.
- **Explore Arcade Docs**: Visit [Arcade.dev](https://docs.arcade.dev) for deeper tool integration insights.

---
## Additional Resources
- **Arcade Documentation**: [https://docs.arcade.dev](https://docs.arcade.dev)
- **LangGraph Documentation**: Explore LangChain’s LangGraph for agent orchestration.
- **OpenAI API**: [https://platform.openai.com](https://platform.openai.com) for model details.
---