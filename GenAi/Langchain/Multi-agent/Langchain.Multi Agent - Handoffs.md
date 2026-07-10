- In the **handoffs** architecture, behavior changes dynamically based on state.
- The core mechanism: [tools](https://docs.langchain.com/oss/python/langchain/tools) update a state variable (e.g., `current_step` or `active_agent`) that persists across turns, and the system reads this variable to adjust behavior—either applying different configuration (system prompt, tools) or routing to a different [agent](https://docs.langchain.com/oss/python/langchain/agents).
- This pattern supports both handoffs between distinct agents and dynamic configuration changes within a single agent.

![[Pasted image 20260217134901.png]]
## Key characteristics
- State-driven behavior: Behavior changes based on a state variable (e.g., `current_step` or `active_agent`)
- Tool-based transitions: Tools update the state variable to move between states
- Direct user interaction: Each state’s configuration handles user messages directly
- Persistent state: State survives across conversation turns

## When to use
- Use the handoffs pattern when you need to enforce sequential constraints (unlock capabilities only after preconditions are met)
- The agent needs to converse directly with the user across different states, or you’re building multi-stage conversational flows. 
- This pattern is particularly valuable for customer support scenarios where you need to collect information in a specific sequence — for example, collecting a warranty ID before processing a refund.
## Basic implementation
The core mechanism is a [tool](https://docs.langchain.com/oss/python/langchain/tools) that returns a [`Command`](https://docs.langchain.com/oss/python/langgraph/graph-api#command) to update state, triggering a transition to a new step or agent:
```python
from langchain.tools import tool
from langchain.messages import ToolMessage
from langgraph.types import Command

@tool
def transfer_to_specialist(runtime) -> Command:
    """Transfer to the specialist agent."""
    return Command(
        update={
            "messages": [
                ToolMessage(  
                    content="Transferred to specialist",
                    tool_call_id=runtime.tool_call_id  
                )
            ],
            "current_step": "specialist"  # Triggers behavior change
        }
    )
```

>[!tip]
>**Why include a `ToolMessage`?** When an LLM calls a tool, it expects a response. The `ToolMessage` with matching `tool_call_id` completes this request-response cycle—without it, the conversation history becomes malformed. 
>This is required whenever your handoff tool updates messages.


Impleemntation Approaches:
- Single Agent with middleware  (one agent with dynamic configuration)
- Multiple agent subgraphs (distinicyt agents as graph nodes)

Single agent with middleware
- A single agent changes its behavior based on state.
- Middleware intercepts each model call and dynamically adjusts the system prompt and available tools.
- Tools update the state variable to trigger transitions:

```python
from langchain.tools import ToolRuntime, tool 
from langchain.messages import ToolMessage 
from langgraph.types import Command

@tool
def record_warranty_status(status:str,runtime: ToolRuntime[None,SupportState]) -> Command:
	"""Record warranty status and transition to te next step"""
	return Command(
		update = {
			"messages": [
				ToolMessage(
					content = f"Warranty status recorded: {status}",
					tool_call_id = runtime.tool_call_id
				)
			],
			"warranty_status": status,
			"current_step": "specialist" # Update state to trigger transition
		}
	)
```

Multi agent Subggraphs
Multiple distinct agents exist as separate nodes in a graph. 
Handoff tools navigate between agent nodes using `Command.PARENT` to specify which node to execute next.

```python
from langchain.messages import AIMessage, ToolMessage 
from langchain.tools import tool, ToolRuntime 
from langgraph.types import Command

@tool
def transfer_to_state(runtime: ToolRuntime) -> Command:
	"""Transfer to the sales agent"""
	last_ai_message = next(msg for msg in reversed(runtime.state["messsages"]) 
	if isinstance(msg, AIMessage))
	
	transfer_message = ToolMessage(
		content = "Transfered to sales agent",
		tool_call_id = runtime.tool_call_id,
	)
	
	return Command(
		goto = "sales_agent",
		update = {
			"active_agent": "sales_agent",
			"messages": [last_ai_message,transfer_message],
		},
		graph = Command.PARENT
	)
```

>[!tip]
>Use **single agent with middleware** for most handoffs use cases—it’s simpler. Only use **multiple agent subgraphs** when you need bespoke agent implementations (e.g., a node that’s itself a complex graph with reflection or retrieval steps).

####  Context engineering
With subgraph handoffs, you control exactly what messages flow between agents. This precision is essential for maintaining valid conversation history and avoiding context bloat that could confuse downstream agents

**Handling context during handoffs**When handing off between agents, you need to ensure the conversation history remains valid.

LLMs expect tool calls to be paired with their responses, so when using `Command.PARENT` to hand off to another agent, you must include both:

1. **The `AIMessage` containing the tool call** (the message that triggered the handoff)
2. **A `ToolMessage` acknowledging the handoff** (the artificial response to that tool call)
Without this pairing, the receiving agent will see an incomplete conversation and may produce errors or unexpected behavior.

```python
@tool
def transfer_to_sales(runtime: ToolRuntime) -> Command:
    # Get the AI message that triggered this handoff
    last_ai_message = runtime.state["messages"][-1]

    # Create an artificial tool response to complete the pair
    transfer_message = ToolMessage(
        content="Transferred to sales agent",
        tool_call_id=runtime.tool_call_id,
    )

    return Command(
        goto="sales_agent",
        update={
            "active_agent": "sales_agent",
            # Pass only these two messages, not the full subagent history
            "messages": [last_ai_message, transfer_message],
        },
        graph=Command.PARENT,
    )
```

**Returning control to the user**
When returning control to the user (ending the agent’s turn), ensure the final message is an `AIMessage`.
This maintains valid conversation history and signals to the user interface that the agent has finished its work.

## Implementation considerations
As you design your multi-agent system, consider:

- **Context filtering strategy**: Will each agent receive full conversation history, filtered portions, or summaries? Different agents may need different context depending on their role.
- **Tool semantics**: Clarify whether handoff tools only update routing state or also perform side effects. For example, should `transfer_to_sales()` also create a support ticket, or should that be a separate action?
- **Token efficiency**: Balance context completeness against token costs. Summarization and selective context passing become more important as conversations grow longer.