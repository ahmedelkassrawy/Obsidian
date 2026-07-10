The [state machine pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) describes workflows where an agent’s behavior changes as it moves through different states of a task

This tutorial shows how to implement a state machine by using tool calls to dynamically change a single agent’s configuration—updating its available tools and instructions based on the current state. 

The state can be determined from multiple sources: 
- the agent’s past actions (tool calls), 
- external state (such as API call results) 
- even initial user input (for example, by running a classifier to determine user intent).

Unlike the [subagents pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant) where sub-agents are called as tools
- The **state machine pattern** uses a single agent whose configuration changes based on workflow progress
- Each “step” is just a different configuration (system prompt + tools) of the same underlying agent, selected dynamically based on state.
---
#### Define Custom State
The `current_step` field is the core of the state machine pattern - it determines which configuration (prompt + tools) is loaded on each turn.
```python
from langchain.agents import AgentState
from typing_extensions import NotRequired
from typing import Literal

# Define the possible workflow steps
SupportStep = Literal["warranty_collector", "issue_classifier", "resolution_specialist"]  

class SupportState(AgentState):  
    """State for customer support workflow."""
    current_step: NotRequired[SupportStep]  
    warranty_status: NotRequired[Literal["in_warranty", "out_of_warranty"]]
    issue_type: NotRequired[Literal["hardware", "software"]]
```

The `current_step` field is the core of the state machine pattern - it determines which configuration (prompt + tools) is loaded on each turn.

![[Pasted image 20260217171552.png]]

#### Create tools that manage workflow state
Create tools that update the workflow state
These tools allow the agent to record information and transition to the next step.

The key is using `Command` to update state, including the `current_step` field:
```python
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command

@tool
def record_warranty_status(
    status: Literal["in_warranty", "out_of_warranty"],
    runtime: ToolRuntime[None, SupportState],
) -> Command:  
    """Record the customer's warranty status and transition to issue classification."""
    return Command(  
        update={  
            "messages": [
                ToolMessage(
                    content=f"Warranty status recorded as: {status}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "warranty_status": status,
            "current_step": "issue_classifier",  
        }
    )


@tool
def record_issue_type(
    issue_type: Literal["hardware", "software"],
    runtime: ToolRuntime[None, SupportState],
) -> Command:  
    """Record the type of issue and transition to resolution specialist."""
    return Command(  
        update={  
            "messages": [
                ToolMessage(
                    content=f"Issue type recorded as: {issue_type}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "issue_type": issue_type,
            "current_step": "resolution_specialist",  
        }
    )


@tool
def escalate_to_human(reason: str) -> str:
    """Escalate the case to a human support specialist."""
    # In a real system, this would create a ticket, notify staff, etc.
    return f"Escalating to human support. Reason: {reason}"


@tool
def provide_solution(solution: str) -> str:
    """Provide a solution to the customer's issue."""
    return f"Solution provided: {solution}"
```

Notice how `record_warranty_status` and `record_issue_type` return `Command` objects that update both the data (`warranty_status`, `issue_type`) AND the `current_step`.

This is how the state machine works - tools control workflow progression.

#### Define step configurations
Prompts:
```python
# Define prompts as constants for easy reference
WARRANTY_COLLECTOR_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Warranty verification

At this step, you need to:
1. Greet the customer warmly
2. Ask if their device is under warranty
3. Use record_warranty_status to record their response and move to the next step

Be conversational and friendly. Don't ask multiple questions at once."""

ISSUE_CLASSIFIER_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Issue classification
CUSTOMER INFO: Warranty status is {warranty_status}

At this step, you need to:
1. Ask the customer to describe their issue
2. Determine if it's a hardware issue (physical damage, broken parts) or software issue (app crashes, performance)
3. Use record_issue_type to record the classification and move to the next step

If unclear, ask clarifying questions before classifying."""

RESOLUTION_SPECIALIST_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Resolution
CUSTOMER INFO: Warranty status is {warranty_status}, issue type is {issue_type}

At this step, you need to:
1. For SOFTWARE issues: provide troubleshooting steps using provide_solution
2. For HARDWARE issues:
   - If IN WARRANTY: explain warranty repair process using provide_solution
   - If OUT OF WARRANTY: escalate_to_human for paid repair options

Be specific and helpful in your solutions."""
```

Then map step names to their configurations using a dictionary:
```python
# Step configuration: maps step name to (prompt, tools, required_state)
STEP_CONFIG = {
    "warranty_collector": {
        "prompt": WARRANTY_COLLECTOR_PROMPT,
        "tools": [record_warranty_status],
        "requires": [],
    },
    "issue_classifier": {
        "prompt": ISSUE_CLASSIFIER_PROMPT,
        "tools": [record_issue_type],
        "requires": ["warranty_status"],
    },
    "resolution_specialist": {
        "prompt": RESOLUTION_SPECIALIST_PROMPT,
        "tools": [provide_solution, escalate_to_human],
        "requires": ["warranty_status", "issue_type"],
    },
}
```

This dictionary-based configuration makes it easy to:

- See all steps at a glance
- Add new steps (just add another entry)
- Understand the workflow dependencies (`requires` field)
- Use prompt templates with state variables (e.g., `{warranty_status}`)

#### Create a step based middleware
Create middleware that reads `current_step` from state and applies the appropriate configuration.

By using the `@wrap_model_call` decorator, this function intercepts every call the agent makes to the LLM.
It modifies the prompt and available tools on the fly before the model ever sees the request.

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable


@wrap_model_call
def apply_step_config(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Configure agent behavior based on the current step."""
    # Get current step (defaults to warranty_collector for first interaction)
    current_step = request.state.get("current_step", "warranty_collector")  

    # Look up step configuration
    stage_config = STEP_CONFIG[current_step]  

    # Validate required state exists
    for key in stage_config["requires"]:
        if request.state.get(key) is None:
            raise ValueError(f"{key} must be set before reaching {current_step}")

    # Format prompt with state values (supports {warranty_status}, {issue_type}, etc.)
    system_prompt = stage_config["prompt"].format(**request.state)

    # Inject system prompt and step-specific tools
    request = request.override(  
        system_prompt=system_prompt,  
        tools=stage_config["tools"],  
    )

    return handler(request)
```

Params:
- `request: ModelRequest`: An object containing the current state of the agent's execution.
	- This includes the `state` (message history and custom variables), 
	- the `system_prompt`, 
	- and the currently assigned `tools`.
	
-  `handler: Callable[[ModelRequest], ModelResponse]`: This is the "next" function in the execution chain (the actual LLM call). Your function must call this handler to proceed with the agent's turn.

#### What the code does
1. **Step Identification**: It looks at `request.state` to find the `current_step` (e.g., "warranty_collector"). If no step is found, it starts the user at the default `warranty_collector` step.
2. **Configuration Lookup**: It retrieves the specific prompt and toolset for that step from a global `STEP_CONFIG` dictionary.
3. **State Validation**: It checks the `requires` list from the config to ensure all necessary data (like `user_id` or `serial_number`) exists in the state before proceeding. If a key is missing, it raises an error.
4. **Prompt Templating**: It formats the system prompt by injecting current state values (e.g., "Hello {user_name}" becomes "Hello Alice").
5. **Request Overriding**: It uses `request.override()` to swap the generic agent settings for the step-specific `system_prompt` and `tools`.
6. **Execution**: It passes the modified request to the `handler`, which sends it to the LLM.

This middleware:
1. **Reads current step**: Gets `current_step` from state (defaults to “warranty_collector”).
2. **Looks up configuration**: Finds the matching entry in `STEP_CONFIG`.
3. **Validates dependencies**: Ensures required state fields exist.
4. **Formats prompt**: Injects state values into the prompt template.
5. **Applies configuration**: Overrides the system prompt and available tools.

The `request.override()` method is key - it allows us to dynamically change the agent’s behavior based on state without creating separate agent instances.

#### Create agent
```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Collect all tools from all step configurations
all_tools = [
    record_warranty_status,
    record_issue_type,
    provide_solution,
    escalate_to_human,
]

# Create the agent with step-based configuration
agent = create_agent(
    model,
    tools=all_tools,
    state_schema=SupportState,  
    middleware=[apply_step_config],  
    checkpointer=InMemorySaver(),  
)
```

>[!warning]
>**Why a checkpointer?** The checkpointer maintains state across conversation turns. Without it, the `current_step` state would be lost between user messages, breaking the workflow.

Expected flow:
1. **Warranty verification step**: Asks about warranty status
2. **Issue classification step**: Asks about the problem, determines it’s hardware
3. **Resolution step**: Provides warranty repair instructions

Understanding state transitions
Turn 1: Initial message
```python
{
    "messages": [HumanMessage("Hi, my phone screen is cracked")],
    "current_step": "warranty_collector"  # Default value
}
```

Middleware applies:
- System prompt: `WARRANTY_COLLECTOR_PROMPT`
- Tools: `[record_warranty_status]`

Turn 2: After warranty recorded
Tool call: `record_warranty_status("in_warranty")` returns:
```python
Command(update={
	    "warranty_status": "in_warranty",
	    "current_step": "issue_classifier"  # State transition!
	}
)
```

Next turn, middleware applies:
- System prompt: `ISSUE_CLASSIFIER_PROMPT` (formatted with `warranty_status="in_warranty"`)
- Tools: `[record_issue_type]`

Turn 3: After issue classified
Tool call: `record_issue_type("hardware")` returns:
```python
Command(update={
    "issue_type": "hardware",
    "current_step": "resolution_specialist"  # State transition!
})
```

Next turn, middleware applies:

- System prompt: `RESOLUTION_SPECIALIST_PROMPT` (formatted with `warranty_status` and `issue_type`)
- Tools: `[provide_solution, escalate_to_human]`

The key insight: **Tools drive the workflow** by updating `current_step`, and **middleware responds** by applying the appropriate configuration on the next turn.

---
Advanced Features:

Manage message history
- As the agent progresses through steps, message history grows
- Use [summarization middleware](https://docs.langchain.com/oss/python/langchain/short-term-memory#summarize-messages) to compress earlier messages while preserving conversational context:
```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware  
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools=all_tools,
    state_schema=SupportState,
    middleware=[
        apply_step_config,
        SummarizationMiddleware(  
            model="gpt-4.1-mini",
            trigger=("tokens", 4000),
            keep=("messages", 10)
        )
    ],
    checkpointer=InMemorySaver(),
)
```

### Add flexibility: Go back
- Some workflows need to allow users to return to previous steps to correct information (e.g., changing warranty status or issue classification).
- However, not all transitions make sense—for example, you typically can’t go back once a refund has been processed.
- For this support workflow, we’ll add tools to return to the warranty verification and issue classification steps.

>[!tip]
>If your workflow requires arbitrary transitions between most steps, consider whether you need a structured workflow at all.
>This pattern works best when steps follow a clear sequential progression with occasional backwards transitions for corrections.

```python
@tool
def go_back_to_warranty() -> Command:  
    """Go back to warranty verification step."""
    return Command(update={"current_step": "warranty_collector"})  


@tool
def go_back_to_classification() -> Command:  
    """Go back to issue classification step."""
    return Command(update={"current_step": "issue_classifier"})  


# Update the resolution_specialist configuration to include these tools
STEP_CONFIG["resolution_specialist"]["tools"].extend([
    go_back_to_warranty,
    go_back_to_classification
])
```

The prompt should be changed:
```python
RESOLUTION_SPECIALIST_PROMPT = """You are a customer support agent helping with device issues.

CURRENT STAGE: Resolution
CUSTOMER INFO: Warranty status is {warranty_status}, issue type is {issue_type}

At this step, you need to:
1. For SOFTWARE issues: provide troubleshooting steps using provide_solution
2. For HARDWARE issues:
   - If IN WARRANTY: explain warranty repair process using provide_solution
   - If OUT OF WARRANTY: escalate_to_human for paid repair options

If the customer indicates any information was wrong, use:
- go_back_to_warranty to correct warranty status
- go_back_to_classification to correct issue type

Be specific and helpful in your solutions."""
```

Now the agent can handle corrections:

```python
result = agent.invoke(
    {"messages": [HumanMessage("Actually, I made a mistake - my device is out of warranty")]},
    config
)
# Agent will call go_back_to_warranty and restart the warranty verification step
```