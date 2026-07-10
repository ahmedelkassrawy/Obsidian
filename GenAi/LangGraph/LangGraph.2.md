LangSmith -> Tracing and evalutation
LangGraph -> App control flow (Orchestration)
Langchain -> Integrations

## Tools
[Tools](https://python.langchain.com/docs/concepts/tools/) are utilities that can be called by a chat model. In LangChain, creating tools can be done using the `@tool` decorator, which transforms Python functions into callable tools
```python
from langchain.tools import tool

@tool
def write_email(to: str, subject: str, content: str) -> str:
    """Write and send an email."""
    # Placeholder response - in real app would send email
    return f"Email sent to {to} with subject '{subject}' and content: {content}"
```

#### Tool calling
```python
tools = [write_email]

llm_with_tools = llm.bind_tools(tools,
					tool_choice = "any",
					parallel_tool_calls = False)
					
res = llm_with_tools.invoke("")
```

## Schema
- TypeDict is fastest but doesn’t support defaults
- Dataclass is basically as fast, supports dot syntax `state.foo`, and has defaults.
- Pydantic is slower (especially with custom validators) but gives type validation.
- 
```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class StateSchema(TypedDict):
    request: str
    email: str

workflow = StateGraph(StateSchema)
```

## Nodes,Routers,Edge
Routing between nodes can be done [conditionally](https://langchain-ai.github.io/langgraph/concepts/low_level/#conditional-edges) using a simple function.

The return value of this function is used as the name of the node (or list of nodes) to send the state to next.
##### Nodes
```python
from typing import Literal
from langgraph.graph import MessagesState
from email_assistant.utils import show_graph

def call_llm(state: MessagesState) -> MessagesState:
    """Run LLM"""

    output = model_with_tools.invoke(state["messages"])
    return {"messages": [output]}
```

```python
def run_tool(state: MessagesState):
    """Performs the tool call"""

    result = []
    
    for tool_call in state["messages"][-1].tool_calls:
        observation = write_email.invoke(tool_call["args"])
        result.append({"role": "tool", 
        "content": observation, 
        "tool_call_id": tool_call["id"]})
        
    return {"messages": result}
```

The common is that the return is returning a {"messages":......} 
##### Route - Should Continue
```python
def should_continue(state: MessagesState) -> Literal["run_tool", "__end__"]:
    """Route to tool handler, or end if Done tool called"""
    
    # Get the last message
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the last message is a tool call, check if it's a Done tool call
    if last_message.tool_calls:
        return "run_tool"
    # Otherwise, we stop (reply to the user)
    return END
```

```python
def should_continue(state: AgentState) -> str:
    """Determine if the workflow should continue or end."""
    
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    return END
```

- Should specify the data type of the return in the function 
- Return of the func definition has to be a Literal 
- the Return at the end of the func has to be "THE NEXT NODE"
#### Workflow
```python
workflow = StateGraph(MessagesState)

worfklow.add_node("...",...)

worfklow.add_edges(START,"...")
workflow.add_conditional_edges("..",route_func,"...")
workflow.add_edges("...",END)

app = workflow.compile()
```

ex:
```python
overall_workflow.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "tool_handler": "tool_handler",
        END: END,
    },
)
```

#### Invoke
```python
result = app.invoke({"messages": [{"role": "user", "content": "Draft a response to my boss (boss@company.ai) confirming that I want to attend Interrupt!"}]})

for m in result["messages"]:
    m.pretty_print()
```

### ReAct Agent
```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=llm,
    tools=[write_email],
    prompt="Respond to the user's request using the tools provided."  
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", 
				"content": "Draft a response to my boss (boss@company.ai) confirming that I want to attend Interrupt!"}]}
)

for m in result["messages"]:
    m.pretty_print()
```

### Persistence
It can be very useful to allow agents to pause during long running tasks.
LangGraph has a built-in persistence layer, implemented through checkpointers, to enable this.
When you compile graph with a checkpointer, the checkpointer saves a [checkpoint](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpoints) of the graph state at every step.
```python

from langgraph.checkpoint.memory import InMemorySaver

agent = create_react_agent(
    model=llm,
    tools=[write_email],
    prompt="Respond to the user's request using the tools provided.",
    checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id": "1"}}

result = agent.invoke({"messages": [{"role": "user", 
									"content": "What are some good practices for writing emails?"}]}, config)
```

```python
# Set up memory
memory = InMemorySaver()

thread = {"configurable": {"thread_id": "1"}}
```

#### Interrupts
```python
from langgraph.types import Command, interrupt

def human_feedback(state):
    print("---human_feedback---")
    feedback = interrupt("Please provide feedback:")
    return {"user_feedback": feedback}
```

```python
# Run the graph until the first interruption
for event in graph.stream(initial_input,thread,stream_mode="updates"):
    print(event)
    print("\n")
```

To resume from an interrupt, we can use [the `Command` object](https://langchain-ai.github.io/langgraph/how-tos/command/).
We'll use it to resume the graph from the interrupted state, passing the value to return from the interrupt call to `resume`.

```python
# Continue the graph execution
for event in graph.stream(
    Command(resume="go to step 3!"),
    thread,
    stream_mode="updates",
):
    print(event)
    print("\n")
```

### Streaming
```python
# Create a thread
config = {"configurable": {"thread_id": "1"}}

# Start conversation
for chunk in graph.stream({"messages": [HumanMessage(content="hi! I'm Lance")]}, config, stream_mode="updates"):
    print(chunk)
```

### Breakpoints
```python
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a by b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine the control flow
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(interrupt_before=["tools"], checkpointer=memory)

# Show graph
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

# Example 1: Multiply 2 and 3 (Thread ID: "1")
initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}
thread = {"configurable": {"thread_id": "1"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()

# Check state
state = graph.get_state(thread)
print("Next node:", state.next)

# Continue from breakpoint
for event in graph.stream(None, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()

# Example 2: Multiply 2 and 3 with user approval (Thread ID: "2")
initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}
thread = {"configurable": {"thread_id": "2"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()

# Get user feedback
user_approval = input("Do you want to call the tool? (yes/no): ")

# Check approval
if user_approval.lower() == "yes":
    # If approved, continue the graph execution
    for event in graph.stream(None, thread, stream_mode="values"):
        event['messages'][-1].pretty_print()
else:
    print("Operation cancelled by user.")
```

### Should Continue
```python
def should_continue(state: AgentState) -> str:
    """Determine if the workflow should continue or end."""
    
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    return END
```

#### Stream Modes
|**Mode**|**Output**|**When to Use**|
|---|---|---|
|`updates`|Dictionary of state updates per node|Track incremental changes; efficient when you only need what changed.|
|`messages`|Tuples with message objects|Stream conversational outputs (e.g., AI responses) for real-time display.|
|`values`|Full state dictionary per node|Need the complete state context at each step (e.g., for debugging or processing).|

```python
# Start conversation, again
config = {"configurable": {"thread_id": "2"}}

# Start conversation
input_message = HumanMessage(content="hi! I'm Lance")
for chunk in graph.stream({"messages": [input_message]}, config, stream_mode="messages"):
  print(chunk[0].content)
```

```python
# Start conversation, again
config = {"configurable": {"thread_id": "2"}}

# Start conversation
input_message = HumanMessage(content="hi! I'm Lance")
for chunk in graph.stream({"messages": [input_message]}, config, stream_mode="updates"):
  print(chunk)
  print(chunk["conversation"]["messages"].content)
```

`values` (full state), 
`updates` (state deltas), 
`messages` (LLM tokens + metadata), 
`custom` (arbitrary user data), 
or `debug` (detailed traces).

```python
stream_mode = ["updates","messages","custom"]
```

#### Combining Tool Binding with Tool Node
Create a powerful workflow where the LLM generates tool calls and the Tool Node executes them as part of a stateful graph. This combination is a common pattern in LangGraph applications, allowing you to leverage the LLM’s ability to decide when to call tools (via tool binding) and the graph’s structure to execute those tools and manage the state.
### How Tool Binding and Tool Node Work Together
1. **Tool Binding with LLM (LangChain)**:
    - You bind tools to the LLM using .bind_tools(), which allows the LLM to generate structured tool_calls in its AIMessage responses.
    - The tool_calls field contains a list of dictionaries with the tool name, arguments, and a unique tool_call_id.
    - This prepares the LLM to decide when and how to invoke tools based on the input prompt.
2.  **Tool Node (LangGraph)**:
    - A ToolNode in LangGraph is designed to process tool_calls from an AIMessage and execute the corresponding tools.
    - It updates the graph’s state by appending ToolMessage objects with the tool execution results.
    - The Tool Node integrates seamlessly with the graph’s state management, ensuring tool results are stored (e.g., in the messages list).
3. **Combining Them**:
- The LLM node (with bound tools) generates an AIMessage with tool_calls.
- The Tool Node takes the state (containing the AIMessage) and executes the tools, updating the state with the results.
- You can use conditional edges in the graph to route execution to the Tool Node when tool_calls are present, or to other nodes (e.g., end the workflow) otherwise.

```python
llm_with_tools = llm.bind_tools([search])

def call_model(state:State):
	messages = state["messages"]
	response = llm_with_tools.invoke(messages)
	
	return {"messages":[response]}
	
def route_to_tools(state:State):
	if state["messages"][-1].tool_calls:
		return "tools"
	return END
	
graph = StateGraph(State)

graph.add_node("tools,ToolNode(tools = [search]))
graph.add_edge("llm","tools")

graph.add_conditional_edges("llm",route_to_tools)
```

#### Human Feedback in Loop
```python
graph = builder.compile(interrupt_before=["assistant"], checkpointer=memory)

initial_input = {"messages": "Multiply 2 and 3"}

# Thread
thread = {"configurable": {"thread_id": "1"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()
```

```python
================================ Human Message ================================= 
Multiply 2 and 3
```
the graph is interrupted before the chat model responds.
```python
graph.update_state(
    thread,
    {"messages": [HumanMessage(content="No, actually multiply 3 and 3!")]},
)

for event in graph.stream(None, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()
```

Another method:
```python
class State(TypedDict):
	feedback_needed: bool
	
def call_model(state:State):
	messages = state["messages"]
	response = llm_with_tools.invoke(messages)
	
	feedback_needed = "clarify" in messages[-1].content,lower() or response.tool_calls
	if feedback_needed:
		response = AIMessage(content="I need clarification. Please provide more details.")
		
		
def human_feedback_node(state: State):
    # In a real application, this could wait for input via a UI/API
    print("Waiting for human feedback...")
    user_input = input("Please provide feedback or clarification: ")
    return {
        "messages": [HumanMessage(content=user_input)],
        "feedback_needed": False  # Reset flag after feedback
    }
    
def route_to_feedback(state: State):
    if state["feedback_needed"]:
        return "human_feedback"
    elif state["messages"][-1].tool_calls:
        return "tools"
    return END
    
graph.add_node("human_feedback", human_feedback_node)
graph.add_conditional_edges("llm", route_to_feedback)
graph.add_edge("human_feedback", "llm")

state = {"messages": [input_message], "conversation": {}, "feedback_needed": False}
for chunk in compiled_graph.stream(state, config, stream_mode="messages"):
    print(chunk[0].content)
```

#### Extraction Prompt
You should use a extraction prompt to extract from the travel preferences from the user query and put the order you want in
example:
```python
extraction_prompt = f"""
    Extract travel preferences from this user query: "{query}"
    
    Please identify and return the following information if available:
    - user_location: Where is the user starting from (current location)
    - destination: Where does the user want to go
    - duration: How long is the trip (e.g., "6 days", "1 week")
    - interests: What activities or interests (e.g., culture, adventure, beaches)
    - budget: Budget range if mentioned
    - travel_style: Travel style preference (luxury, budget, adventure, etc.)
    
    Return the information in this exact format:
    user_location: [value or "Not specified"]
    destination: [value or "Not specified"]  
    duration: [value or "Not specified"]
    interests: [value or "Not specified"]
    budget: [value or "Not specified"]
    travel_style: [value or "Not specified"]
    """
    
    extraction_response = llm.invoke(extraction_prompt)
    preferences_text = extraction_response.content
```

#### Tool binding and Custom Tool Node
```python
tools = [rag_process_tool, suggest_trip_tool, search_tool]
llm_with_tools = llm.bind_tools(tools)

def call_model(state: State):
	messages = state["messages"]
	logger.info(f"Calling model with {len(messages)} messages")
	
	system_prompt = """
    You are a helpful travel assistant. You can assist users in planning their trips, finding relevant information, and providing recommendations.
    Tools Available:
    - rag_process_tool: Get relevant information from documents and guides provided
    - suggest_trip_tool: Suggest travel itineraries based on user preferences
    - search_tool: Perform searches to find specific information including any flight or real time information
    """
    
    response = llm_with_tools.invoke(
        [SystemMessage(content=system_prompt)] + messages
    )
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        logger.info(f"Model wants to use tools: {[tc['name'] for tc in response.tool_calls]}")
    else:
        logger.info("Model generated direct response without using tools")

    return {"messages": [response]}
```

```python
def route_to_tools(state: State):
    if state["messages"][-1].tool_calls:
        logger.info("Routing to tools execution")
        return "tools"

    logger.info("Routing to END - no tools needed")
    return END
```

```python
def update_rag_context(state: State):
    if isinstance(state["messages"][-1], ToolMessage):
        state["rag_context"] = state["messages"][-1].content

    return state
```

```python
workflow = StateGraph(State)

workflow.add_node("call_model", call_model)
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("update_rag_context", update_rag_context)

workflow.set_entry_point("call_model")

workflow.add_conditional_edges(
	"call_model",
	route_to_tools,
	{"tools": "tools", END: END}
)
workflow.add_edge("tools", "update_rag_context")
workflow.add_edge("update_rag_context", "call_model")
```

```python
 graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {
            "tools": "retrieve_philosopher_context",
            END: "connector_node"
        }
    )
```

Tools don't usually require the state as the function arg
#### Long Memory

|Memory Type|What is Stored|Human Example|Agent Example|
|---|---|---|---|
|[Semantic](https://langchain-ai.github.io/langgraph/concepts/memory/#semantic-memory)|Facts|Things I learned in school|Facts about a user|
|[Episodic](https://langchain-ai.github.io/langgraph/concepts/memory/#episodic-memory)|Experiences|Things I did|Past agent actions|
|[Procedural](https://langchain-ai.github.io/langgraph/concepts/memory/#procedural-memory)|Instructions|Instincts or motor skills|Agent system prompt|
When storing objects (e.g., memories) in the [Store](https://www.google.com/url?q=https%3A%2F%2Flangchain-ai.github.io%2Flanggraph%2Freference%2Fstore%2F%23langgraph.store.base.BaseStore), we provide:
- The `namespace` for the object, a tuple (similar to directories)
- the object `key` (similar to filenames)
- the object `value` (similar to file contents)

Langgraph Store Memory
```python
import uuid
from langgraph.store.memory import InMemoryStore

in_memory_store = InMemoryStore()

#namespace for memory to use
user_id = "1"
namespace_for_memory = (user_id,"memories")

#save a memroy to namespace as key and value
key = str(uuid.uuid4())

#the value to be in the dictionary
value = {"food_preference":"I like pizza"}

#save the memory
in_memory_store.put(namespace_for_memory,key,value)
```

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig

# Chatbot instruction
MODEL_SYSTEM_MESSAGE = """You are a helpful assistant with memory that provides information about the user. 
If you have memory for this user, use it to personalize your responses.
Here is the memory (it may be empty): {memory}"""

# Create new memory from the chat history and any existing memory
CREATE_MEMORY_INSTRUCTION = """"You are collecting information about the user to personalize your responses.

CURRENT USER INFORMATION:
{memory}

INSTRUCTIONS:
1. Review the chat history below carefully
2. Identify new information about the user, such as:
   - Personal details (name, location)
   - Preferences (likes, dislikes)
   - Interests and hobbies
   - Past experiences
   - Goals or future plans
3. Merge any new information with existing memory
4. Format the memory as a clear, bulleted list
5. If new information conflicts with existing memory, keep the most recent version

Remember: Only include factual information directly stated by the user. Do not make assumptions or inferences.

Based on the chat history below, please update the user information:"""

def call_model(state:MessagesState,
               config: RunnableConfig,
               store:BaseStore):
  """Load memory from the store and use it to personalize the chatbot's response."""

  #get user_id from the config
  user_id = config["configurable"]["user_id"]

  #retrieve memory from the store
  namespace = ("memory",user_id)
  key = "user_memory"
  existing_memory = store.get(namespace,key)

  #extract the actual memory content if it exists 
  if existing_memory:
    existing_memory_content = existing_memory.value.get("memory")
  else:
    existing_memory_content = "No existing memory found."

  system_msg = MODEL_SYSTEM_MESSAGE.format(memory = existing_memory_content)

  response = llm.invoke([SystemMessage(content = system_msg)] + state["messages"])

  return {"messages":response}
```

```python
def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and save a memory to the store."""
    
    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Retrieve existing memory from the store
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")
        
    # Extract the memory
    if existing_memory:
        existing_memory_content = existing_memory.value.get('memory')
    else:
        existing_memory_content = "No existing memory found."

    # Format the memory in the system prompt
    system_msg = CREATE_MEMORY_INSTRUCTION.format(memory=existing_memory_content)
    new_memory = llm.invoke([SystemMessage(content=system_msg)]+state['messages'])

    # Overwrite the existing memory in the store 
    key = "user_memory"

    # Write value as a dictionary with a memory key
    store.put(namespace, key, {"memory": new_memory.content})
```

```python
builder = StateGraph(MessagesState)

builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)

builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)
```

```python
# Store for long-term (across-thread) memory
across_thread_memory = InMemoryStore() 

# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()
```

```python
# Compile the graph with the checkpointer fir and store
graph = builder.compile(checkpointer=within_thread_memory,
                        store=across_thread_memory)
                        
#thread_id -> short term
#user_id -> long term
config = {"configurable":{"thread_id":"1",
                          "user_id":"1"}}

#user input
input_messages = [HumanMessage(content = "Hi,my name is Lance")]

for chunk in graph.stream({"messages":input_messages},
                          config,
                          stream_mode = "values"):
  chunk["messages"][-1].pretty_print()
```

[Add memory](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/)
#### MemorySchema - UserProfile Extracting

```python
from trustcall import create_extractor
from pydantic import BaseModel,Field

# Schema 
class UserProfile(BaseModel):
    """User profile schema with typed fields"""
    user_name: str = Field(description="The user's preferred name")
    interests: List[str] = Field(description="A list of the user's interests")
    location: str = Field(description="The user's location currently")


# Create the extractor
trustcall_extractor = create_extractor(
    llm,
    tools=[UserProfile],
    tool_choice="UserProfile"
)

# Instruction
system_msg = "Extract the user profile from the following conversation"

# Invoke the extractor
result = trustcall_extractor.invoke({"messages": [SystemMessage(content=system_msg)] + conversation})
```

```python
for m in result["messages"]:
    m.pretty_print()
    
schema = result["responses"]
schema

schema[0].model_dump()
# We can save the existing schema as a dict.
# We can use `model_dump()` to serialize a Pydantic model instance into a dict.
```

```python
# Update the conversation
updated_conversation = [HumanMessage(content="Hi, I'm Lance."), 
                        AIMessage(content="Nice to meet you, Lance."), 
                        HumanMessage(content="I really like biking around San Francisco."),
                        AIMessage(content="San Francisco is a great city! Where do you go after biking?"),
                        HumanMessage(content="I really like to go to a bakery after biking."),]

# Update the instruction
system_msg = f"""Update the memory (JSON doc) to incorporate new information from the following conversation"""

# Invoke the extractor with the updated instruction and existing profile with the corresponding tool name (UserProfile)
result = trustcall_extractor.invoke({"messages": [SystemMessage(content=system_msg)]+updated_conversation}, 
                                    {"existing": {"UserProfile": schema[0].model_dump()}})  
                                    
for m in result["messages"]:
    m.pretty_print()
    
updated_schema = result["responses"][0]
updated_schema.model_dump()
```

```python
# Chatbot instruction
MODEL_SYSTEM_MESSAGE = """You are a helpful assistant with memory that provides information about the user.
If you have memory for this user, use it to personalize your responses.
Here is the memory (it may be empty): {memory}"""

# Extraction instruction
TRUSTCALL_INSTRUCTION = """Create or update the memory (JSON doc) to incorporate information from the following conversation:"""


def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """Load memory from the store and use it to personalize the chatbot's response."""

    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Retrieve memory from the store
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")

    # Format the memories for the system prompt
    if existing_memory and existing_memory.value:
        memory_dict = existing_memory.value
        formatted_memory = (
            f"Name: {memory_dict.get('user_name', 'Unknown')}\n"
            f"Location: {memory_dict.get('user_location', 'Unknown')}\n"
            f"Interests: {', '.join(memory_dict.get('interests', []))}"
        )
    else:
        formatted_memory = None

    # Format the memory in the system prompt
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=formatted_memory)

    # Respond using memory as well as the chat history
    response = llm.invoke([SystemMessage(content=system_msg)]+state["messages"])

    return {"messages": response}


def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """Reflect on the chat history and save a memory to the store."""

    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Retrieve existing memory from the store
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")

    # Get the profile as the value from the list, and convert it to a JSON doc
    existing_profile = {"UserProfile": existing_memory.value} if existing_memory else None

    # Invoke the extractor
    result = trustcall_extractor.invoke({"messages": [SystemMessage(content=TRUSTCALL_INSTRUCTION)]+state["messages"], "existing": existing_profile})

    # Get the updated profile as a JSON object
    updated_profile = result["responses"][0].model_dump()

    # Save the updated profile
    key = "user_memory"
    store.put(namespace, key, updated_profile)
```