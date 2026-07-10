#### Tool
```python
@tool
@traceable
def search_query_tool(query: str) -> str:
    """Search for information using web search for flights, pre-made trips, or anything you don't have information about."""
    
    result = search_query(query)
    return result
```

#### Custom ToolNode
```python
def custom_tool_node(tools):
    base_tool_node = ToolNode(tools)

    def _normalize_user_arg(tool_call, state):
        """Fix or inject the 'user' argument in any tool call."""
        if "args" not in tool_call:
            tool_call["args"] = {}

        user_arg = tool_call["args"].get("user")

        # Case 1: Empty stringified dict → replace with state user
        if isinstance(user_arg, str) and user_arg.strip() in ["{}", "'{}'"]:
            user_data = state.get("user")
            tool_call["args"]["user"] = (
                user_data.model_dump() if hasattr(user_data, "model_dump") else {}
            )
            return

        # Case 2: JSON-like string → try parsing
        if isinstance(user_arg, str):
            try:
                tool_call["args"]["user"] = json.loads(user_arg.replace("'", '"'))
                return
            except json.JSONDecodeError:
                tool_call["args"]["user"] = {}

        # Case 3: Missing user arg → inject from state
        if not user_arg:
            user_data = state.get("user")
            tool_call["args"]["user"] = (
                user_data.model_dump() if hasattr(user_data, "model_dump") else {}
            )

    def _tool_node(state: AgentState) -> AgentState:
        last_message = state["messages"][-1]

        # Normalize all tool calls (generic)
        if getattr(last_message, "tool_calls", None):
            for tool_call in last_message.tool_calls:
                _normalize_user_arg(tool_call, state)

        # Run base ToolNode
        result = base_tool_node.invoke(state)

        # Preserve custom state
        return {
            "messages": result["messages"],
            "user": state.get("user"),
            "context": state.get("context", ""),
            "rag_context": state.get("rag_context", "")
        }

    return _tool_node
```
#### DB integration
```python
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)

```

#### HITL
#### Approve or reject with interrupt
```python
from typing import Literal, TypedDict
import uuid

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

# Define the shared graph state
class State(TypedDict):
    llm_output: str
    decision: str

# Simulate an LLM output node
def generate_llm_output(state: State) -> State:
    return {"llm_output": "This is the generated output."}

# Human approval node
def human_approval(state: State) -> Command[Literal["approved_path", "rejected_path"]]:
    decision = interrupt({
        "question": "Do you approve the following output?",
        "llm_output": state["llm_output"]
    })

    if decision == "approve":
        return Command(goto="approved_path", update={"decision": "approved"})
    else:
        return Command(goto="rejected_path", update={"decision": "rejected"})

# Next steps after approval
def approved_node(state: State) -> State:
    print("✅ Approved path taken.")
    return state

# Alternative path after rejection
def rejected_node(state: State) -> State:
    print("❌ Rejected path taken.")
    return state

# Build the graph
builder = StateGraph(State)
builder.add_node("generate_llm_output", generate_llm_output)
builder.add_node("human_approval", human_approval)
builder.add_node("approved_path", approved_node)
builder.add_node("rejected_path", rejected_node)

builder.set_entry_point("generate_llm_output")
builder.add_edge("generate_llm_output", "human_approval")
builder.add_edge("approved_path", END)
builder.add_edge("rejected_path", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Run until interrupt
config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({}, config=config)
print(result["__interrupt__"])
# Output:
# Interrupt(value={'question': 'Do you approve the following output?', 'llm_output': 'This is the generated output.'}, ...)

# Simulate resuming with human input
# To test rejection, replace resume="approve" with resume="reject"
final_result = graph.invoke(Command(resume="approve"), config=config)
print(final_result)
```

#### Review and edit state
```python
from typing import TypedDict
import uuid

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

# Define the graph state
class State(TypedDict):
    summary: str

# Simulate an LLM summary generation
def generate_summary(state: State) -> State:
    return {
        "summary": "The cat sat on the mat and looked at the stars."
    }

# Human editing node
def human_review_edit(state: State) -> State:
    result = interrupt({
        "task": "Please review and edit the generated summary if necessary.",
        "generated_summary": state["summary"]
    })
    return {
        "summary": result["edited_summary"]
    }

# Simulate downstream use of the edited summary
def downstream_use(state: State) -> State:
    print(f"✅ Using edited summary: {state['summary']}")
    return state

# Build the graph
builder = StateGraph(State)
builder.add_node("generate_summary", generate_summary)
builder.add_node("human_review_edit", human_review_edit)
builder.add_node("downstream_use", downstream_use)

builder.set_entry_point("generate_summary")
builder.add_edge("generate_summary", "human_review_edit")
builder.add_edge("human_review_edit", "downstream_use")
builder.add_edge("downstream_use", END)

# Set up in-memory checkpointing for interrupt support
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Invoke the graph until it hits the interrupt
config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({}, config=config)

# Output interrupt payload
print(result["__interrupt__"])
# Example output:
# > [
# >     Interrupt(
# >         value={
# >             'task': 'Please review and edit the generated summary if necessary.',
# >             'generated_summary': 'The cat sat on the mat and looked at the stars.'
# >         },
# >         id='...'
# >     )
# > ]

# Resume the graph with human-edited input
edited_summary = "The cat lay on the rug, gazing peacefully at the night sky."
resumed_result = graph.invoke(
    Command(resume={"edited_summary": edited_summary}),
    config=config
)
print(resumed_result)
```