#### Memory Collection
```python
from pydantic import BaseModel, Field

class Memory(BaseModel):
    content: str = Field(description="The main content of the memory. For example: User expressed interest in learning about French.")
    
trustcall_extractor = create_extractor(
    llm,
    tools = [Memory],
    tool_choice = "Memory",
    enable_inserts = True,
)
```

```python
user_extractor = create_extractor(
    llm,
    tools = [
        {
            "type": "function", 
            "function": {
                "name": "UserScheme",
                "description": "Extract user preferences from conversation",
                "parameters": UserScheme.model_json_schema()
            }
        }
    ],
    tool_choice = "UserScheme",
    enable_inserts= True,
)
```

```python
# Chatbot instruction
MODEL_SYSTEM_MESSAGE = """You are a helpful chatbot. You are designed to be a companion to a user. 
You have a long term memory which keeps track of information you learn about the user over time.
Current Memory (may include updated memories from this conversation): 
{memory}"""

# Trustcall instruction
TRUSTCALL_INSTRUCTION = """Reflect on following interaction. 
Use the provided tools to retain any necessary memories about the user. 
Use parallel tool calling to handle updates and insertions simultaneously:"""
```

```python
def call_model(state:MessagesState,
               config: RunnableConfig,
               store: BaseStore):
  user_id = config["configurable"]["user_id"]

  #retrieve memory from the store
  namespace = ("memories",user_id)
  memories = store.search(namespace)

  #format memories for the sys prompt
  info = "\n".join(f"- {mem.value['content']}" for mem in memories)
  system_msg = MODEL_SYSTEM_MESSAGE.format(memory=info)

  #respond using memory as well as the chat history
  response = llm.invoke([SystemMessage(content = system_msg)] + state["messages"])

  return {"messages":response}
  
def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """Reflect on the chat history and update the memory collection."""
    
    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Define the namespace for the memories
    namespace = ("memories", user_id)

    # Retrieve the most recent memories for context
    existing_items = store.search(namespace)

    # Format the existing memories for the Trustcall extractor
    tool_name = "Memory"
    existing_memories = ([(existing_item.key, tool_name, existing_item.value)
                          for existing_item in existing_items]
                          if existing_items
                          else None
                        )

    # Merge the chat history and the instruction
    updated_messages=list(merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION)] + state["messages"]))

    # Invoke the extractor
    result = trustcall_extractor.invoke({"messages": updated_messages, 
                                        "existing": existing_memories})

    # Save the memories from Trustcall to the store
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace,
                  rmeta.get("json_doc_id", str(uuid.uuid4())),
                  r.model_dump(mode="json"),
            )

```

```python
builder = StateGraph(MessagesState)

builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
  
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)

# Store for long-term (across-thread) memory
across_thread_memory = InMemoryStore()

# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()

# Compile the graph with the checkpointer fir and store
graph = builder.compile(checkpointer=within_thread_memory, store=across_thread_memory)
```

```python
# User input 
input_messages = [HumanMessage(content="I also enjoy going to bakeries")]

# Run the graph
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
```

#### MemoryAgent
We can add a [listener](https://www.google.com/url?q=https%3A%2F%2Fpython.langchain.com%2Fdocs%2Fhow_to%2Flcel_cheatsheet%2F%23add-lifecycle-listeners) to the Trustcall extractor.
This will pass runs from the extractor's execution to a class, `Spy`, that we will define.
Our `Spy` class will extract information about what tool calls were made by Trustcall.
```python
class Spy:
  def __init__(self):
    self.called_tools = []

  def __call__(self,run):
    #collect info about tool calls made by extractor
    q = [run]

    while q:
      r = q.pop()

      if r.child_runs:
        q.extend(r.child_runs)
      if r.run_type == "chat_model":
        self.called_tools.append(
            r.outputs["generations"][0][0]["message"]["kwargs"]["tool_calls"]
        )

spy = Spy()

trustcall_extractor = create_extractor(
    llm,
    tools=[Memory],
    tool_choice="Memory",
    enable_inserts=True,
)

# Add the spy as a listener
trustcall_extractor_see_all_tool_calls = trustcall_extractor.with_listeners(on_end=spy)
```

```python
# Inspect the tool calls made by Trustcall
spy.called_tools

[[{'name': 'Memory',
   'args': {'content': 'User went to Tartine and ate a croissant.'},
   'id': 'cf2efb5c-2623-471c-9e3e-ac6bf7e466aa',
   'type': 'tool_call'},
  {'name': 'Memory',
   'args': {'content': 'User is thinking about Japan and going back this winter.'},
   'id': 'a6e5845d-072c-4ae8-9c6d-5a0271bd0b2b',
   'type': 'tool_call'}]]
```
#### Extracting tool

```python
def extract_user_info(state: AgentState, config: RunnableConfig, store: BaseStore):
    """Extract user information from conversation and store it in memory."""
    logger.info("extract_user_info function entered")
    
    user_id = config["configurable"].get("user_id", "default_user")
    namespace = ("memory", user_id)
    
    # Extract user profile
    system_msg = "Extract the user profile from the following conversation"
    result = user_extractor.invoke({"messages": [SystemMessage(content=system_msg)] + state["messages"]})
    scheme = result.get("responses", [])
    user_preferences = scheme[0].model_dump() if scheme else {}
    
    # Store user preferences
    key = "user_preferences"
    store.put(namespace, key, user_preferences)
    
    # Update the state with extracted user preferences
    if user_preferences:
        # Handle None values for boolean field
        if user_preferences.get('want_flight_links') is None:
            user_preferences['want_flight_links'] = False
        
        try:
            updated_user = UserScheme(**user_preferences)
            state["user"] = updated_user
            logger.info(f"Updated user preferences in state: {updated_user.model_dump()}")
        except Exception as e:
            logger.error(f"Error creating UserScheme: {e}")
            logger.warning("Keeping default user preferences")
    else:
        logger.warning("No user preferences extracted, keeping default")
    
    logger.info("extract_user_info function exited")
    return state
```

```python
def extract_tool_info(tool_calls, schema_name="Memory"):
    """Extract information from tool calls for both patches and new memories.
    
    Args:
        tool_calls: List of tool calls from the model
        schema_name: Name of the schema tool (e.g., "Memory", "ToDo", "Profile")
    """

    # Initialize list of changes
    changes = []
    
    for call_group in tool_calls:
        for call in call_group:
            if call['name'] == 'PatchDoc':
                changes.append({
                    'type': 'update',
                    'doc_id': call['args']['json_doc_id'],
                    'planned_edits': call['args']['planned_edits'],
                    'value': call['args']['patches'][0]['value']
                })
            elif call['name'] == schema_name:
                changes.append({
                    'type': 'new',
                    'value': call['args']
                })

    # Format results as a single string
    result_parts = []
    for change in changes:
        if change['type'] == 'update':
            result_parts.append(
                f"Document {change['doc_id']} updated:\n"
                f"Plan: {change['planned_edits']}\n"
                f"Added content: {change['value']}"
            )
        else:
            result_parts.append(
                f"New {schema_name} created:\n"
                f"Content: {change['value']}"
            )
    
    return "\n\n".join(result_parts)

# Inspect spy.called_tools to see exactly what happened during the extraction
schema_name = "Memory"
changes = extract_tool_info(spy.called_tools, schema_name)
print(changes)

New Memory created:
Content: {'content': 'User went to Tartine and ate a croissant.'}
New Memory created:
Content: {'content': 'User is thinking about Japan and going back this winter.'}
```

##### Memory Agent
```python
import uuid
from IPython.display import Image, display
from datetime import datetime
from trustcall import create_extractor
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import merge_message_runs, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from typing import Literal

class Profile(BaseModel):
  name: Optional[str] = Field(description="The user's name", default=None)
  location: Optional[str] = Field(description="The user's location", default=None)
  job: Optional[str] = Field(description="The user's job", default=None)
  connections: list[str] = Field(
      description="Personal connection of the user, such as family members, friends, or coworkers",
      default_factory=list
  )
  interests: list[str] = Field(
      description="Interests that the user has",
      default_factory=list
  )

class Todo(BaseModel):
  task:str = Field(description = "The task to be completed")
  time_to_complete: Optional[int] = Field(description="Estimated time to complete the task (minutes).")
  deadline: Optional[datetime] = Field(
      description="When the task needs to be completed by (if applicable)",
      default=None
  )
  solutions: list[str] = Field(
      description="List of specific, actionable solutions (e.g., specific ideas, service providers, or concrete options relevant to completing the task)",
      min_items=1,
      default_factory=list
  )
  status: Literal["not started", "in progress", "done", "archived"] = Field(
      description="Current status of the task",
      default="not started"
  )

profile_extractor = create_extractor(
    llm,
    tools=[Profile],
    tool_choice="Profile",
)
```

```python
MODEL_SYSTEM_MESSAGE = """You are a helpful chatbot.

You are designed to be a companion to a user, helping them keep track of their ToDo list.

You have a long term memory which keeps track of three things:
1. The user's profile (general information about them)
2. The user's ToDo list
3. General instructions for updating the ToDo list

Here is the current User Profile (may be empty if no information has been collected yet):
<user_profile>
{user_profile}
</user_profile>

Here is the current ToDo List (may be empty if no tasks have been added yet):
<todo>
{todo}
</todo>

Here are the current user-specified preferences for updating the ToDo list (may be empty if no preferences have been specified yet):
<instructions>
{instructions}
</instructions>

Here are your instructions for reasoning about the user's messages:

1. Reason carefully about the user's messages as presented below.

2. Decide whether any of the your long-term memory should be updated:
- If personal information was provided about the user, update the user's profile by calling UpdateMemory tool with type `user`
- If tasks are mentioned, update the ToDo list by calling UpdateMemory tool with type `todo`
- If the user has specified preferences for how to update the ToDo list, update the instructions by calling UpdateMemory tool with type `instructions`

3. Tell the user that you have updated your memory, if appropriate:
- Do not tell the user you have updated the user's profile
- Tell the user them when you update the todo list
- Do not tell the user that you have updated instructions

4. Err on the side of updating the todo list. No need to ask for explicit permission.

5. Respond naturally to user user after a tool call was made to save memories, or if no tool call was made."""

# Trustcall instruction
TRUSTCALL_INSTRUCTION = """Reflect on following interaction.

Use the provided tools to retain any necessary memories about the user.

Use parallel tool calling to handle updates and insertions simultaneously.

System Time: {time}"""

# Instructions for updating the ToDo list
CREATE_INSTRUCTIONS = """Reflect on the following interaction.

Based on this interaction, update your instructions for how to update ToDo list items.

Use any feedback from the user to update how they like to have items added, etc.

Your current instructions are:

<current_instructions>
{current_instructions}
</current_instructions>"""

```

```python
from typing import TypedDict, Literal

class UpdateMemory(TypedDict):
    """ Decision on what memory type to update """
    update_type: Literal['profile', 'todo', 'instructions']

def task_maistro(state:MessagesState,
                 config: RunnableConfig,
                 store: BaseStore):
  user_id = config["configurable"]["user_id"]

  namespace = ("profile",user_id)
  memories = store.search(namespace)

  if memories:
    user_profile = memories[0].value
  else:
    user_profile = None

  namespace = ("todo",user_id)
  memories = store.search(namespace)
  todo = "\n".join(f"{mem.value}" for mem in memories)

  namespace = ("instructions",user_id)
  memories = store.search(namespace)
  if memories:
      instructions = memories[0].value
  else:
      instructions = ""

  system_msg = MODEL_SYSTEM_MESSAGE.format(
      user_profile=user_profile,
      todo=todo,
      instructions=instructions,
  )

  response = llm.bind_tools([UpdateMemory],
                            parallel_tool_calls = False).invoke([SystemMessage(content = system_msg)] + state["messages"])

  return {"messages":[response]}
```

```python
def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """Reflect on the chat history and update the memory collection."""

    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Define the namespace for the memories
    namespace = ("profile", user_id)

    # Retrieve the most recent memories for context
    existing_items = store.search(namespace)

    # Format the existing memories for the Trustcall extractor
    tool_name = "Profile"
    existing_memories = ([(existing_item.key, tool_name, existing_item.value)
                          for existing_item in existing_items]
                          if existing_items
                          else None
                        )

    # Merge the chat history and the instruction
    TRUSTCALL_INSTRUCTION_FORMATTED=TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages=list(merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION_FORMATTED)] + state["messages"][:-1]))

    # Invoke the extractor
    result = profile_extractor.invoke({"messages": updated_messages,
                                         "existing": existing_memories})

    # Save the memories from Trustcall to the store
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace,
                  rmeta.get("json_doc_id", str(uuid.uuid4())),
                  r.model_dump(mode="json"),
            )
    tool_calls = state['messages'][-1].tool_calls
    return {"messages": [{"role": "tool", "content": "updated profile", "tool_call_id":tool_calls[0]['id']}]}
```

```python
def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """Reflect on the chat history and update the memory collection."""

    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Define the namespace for the memories
    namespace = ("todo", user_id)

    # Retrieve the most recent memories for context
    existing_items = store.search(namespace)

    # Format the existing memories for the Trustcall extractor
    tool_name = "Todo"
    existing_memories = ([(existing_item.key, tool_name, existing_item.value)
                          for existing_item in existing_items]
                          if existing_items
                          else None
                        )

    # Merge the chat history and the instruction
    TRUSTCALL_INSTRUCTION_FORMATTED=TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages=list(merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION_FORMATTED)] + state["messages"][:-1]))

    # Initialize the spy for visibility into the tool calls made by Trustcall
    spy = Spy()

    # Create the Trustcall extractor for updating the ToDo list
    todo_extractor = create_extractor(
    llm,
    tools=[Todo],
    tool_choice=tool_name,
    enable_inserts=True
    ).with_listeners(on_end=spy)

    # Invoke the extractor
    result = todo_extractor.invoke({"messages": updated_messages,
                                    "existing": existing_memories})

    # Save the memories from Trustcall to the store
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace,
                  rmeta.get("json_doc_id", str(uuid.uuid4())),
                  r.model_dump(mode="json"),
            )

    # Respond to the tool call made in task_mAIstro, confirming the update
    tool_calls = state['messages'][-1].tool_calls

    # Extract the changes made by Trustcall and add the the ToolMessage returned to task_mAIstro
    todo_update_msg = extract_tool_info(spy.called_tools, tool_name)
    return {"messages": [{"role": "tool", "content": todo_update_msg, "tool_call_id":tool_calls[0]['id']}]}
```

```python
def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):

    """Reflect on the chat history and update the memory collection."""

    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    namespace = ("instructions", user_id)

    existing_memory = store.get(namespace, "user_instructions")

    # Format the memory in the system prompt
    system_msg = CREATE_INSTRUCTIONS.format(current_instructions=existing_memory.value if existing_memory else None)
    new_memory = llm.invoke([SystemMessage(content=system_msg)]+state['messages'][:-1] + [HumanMessage(content="Please update the instructions based on the conversation")])

    # Overwrite the existing memory in the store
    key = "user_instructions"
    store.put(namespace, key, {"memory": new_memory.content})
    tool_calls = state['messages'][-1].tool_calls
    return {"messages": [{"role": "tool", "content": "updated instructions", "tool_call_id":tool_calls[0]['id']}]}

```

```python
# Conditional edge
def route_message(state: MessagesState, config: RunnableConfig, store: BaseStore) -> Literal[END, "update_todos", "update_instructions", "update_profile"]:

    """Reflect on the memories and chat history to decide whether to update the memory collection."""
    message = state['messages'][-1]
    if len(message.tool_calls) ==0:
        return END
    else:
        tool_call = message.tool_calls[0]
        if tool_call['args']['update_type'] == "user":
            return "update_profile"
        elif tool_call['args']['update_type'] == "todo":
            return "update_todos"
        elif tool_call['args']['update_type'] == "instructions":
            return "update_instructions"
        else:
            raise ValueError

builder = StateGraph(MessagesState)

# Define the flow of the memory extraction process
builder.add_node(task_maistro)
builder.add_node(update_todos)
builder.add_node(update_profile)
builder.add_node(update_instructions)

builder.add_edge(START, "task_maistro")
builder.add_conditional_edges("task_maistro", route_message)
builder.add_edge("update_todos", "task_maistro")
builder.add_edge("update_profile", "task_maistro")
builder.add_edge("update_instructions", "task_maistro")

# Store for long-term (across-thread) memory
across_thread_memory = InMemoryStore()

# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()

# We compile the graph with the checkpointer and store
graph = builder.compile(checkpointer=within_thread_memory, store=across_thread_memory)
```

```python
def should_summarize_conversation(
    state: PhilosopherState,
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"

    return END
```