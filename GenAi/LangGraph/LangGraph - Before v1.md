 If you don't specify  a reducer, every state update will overwrite the list of messages with the most recently provided value. If you wanted to simply append messages to the existing list, you could use `operator.add` as a reducer.
 
state["messages"][-1].content
`add_messages` --> it's reducer function.
`MessagesState` is defined with a single `messages` key which is a list of `AnyMessage` objects and uses the `add_messages` reducer.
- Conditional Edges: Call a function to determine which node(s) to go to next.
- - Entry Point: Which node to call first when user input arrives. (Inputttt)
- - Conditional Entry Point:<font color="#2DC26B"> Call a function</font> to determine which node(s) to call first when <font color="#2DC26B">user input</font> arrives.
```python
graph.add_conditional_edges("node_a", routing_function)

graph.add_conditional_edges("node_a", routing_function, {True: "node_b", False: "node_c"})
```
Similar to nodes, the `routing_function` accepts the current `state` of the graph and returns a value.

Control -> edge + node (control the flow ,update state)
```python
def my_node(state: State) -> Command[Literal["my_other_node"]]:
    return Command(
        # state update
        update={"foo": "bar"},
        # control flow
        goto="my_other_node"
    )

#or

def my_node(state: State) -> Command[Literal["my_other_node"]]:
    if state["foo"] == "bar":
        return Command(update={"foo": "baz"}, goto="my_other_node")
```

### When should I use Command instead of conditional edges?

Use `Command` when you need to **both** update the graph state **and** route to a different node.

```python
from typing import TypedDict

class State(TypedDict):
  graph_state : str
```


```python
def node1(state: State):
  print("Node1")
  return {"graph_state": state["graph_state"] + "I as"}

def node2(state: State):
  print("Node2")
  return {"graph_state": state["graph_state"] + " HAPPY"}

def node3(state: State):
  print("Node3")
  return {"graph_state": state["graph_state"] + " SAD"}
```

```python
import random
from typing import Literal

def decide_mood(state: State) -> Literal["node2","node3"]:
  if random.random() < 0.5:
    return "node2"
  else:
    return "node3" 
```

```python
from langgraph.graph import StateGraph,START,END
from IPython.display import display,Image

graph_builder = StateGraph(State)

graph_builder.add_node("node1", node1)
graph_builder.add_node("node2", node2)
graph_builder.add_node("node3", node3)

graph_builder.add_edge(START,"node1")
graph_builder.add_conditional_edges("node1",decide_mood)
graph_builder.add_edge("node2",END)
graph_builder.add_edge("node3",END)

graph = graph_builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
```

```python
#implements a runnable protocol 
#standard way to execute langchain components
# invoke is one of them

graph.invoke({"graph_state" : "Hi, this is Lance."})
```

#### Messages
`HumanMessage`, `AIMessage`, `SystemMessage`, and `ToolMessage`.

Each message can be supplied with a few things:

- `content` - content of the message
- `name` - optionally, a message author
- `response_metadata` - optionally, a dict of metadata (e.g., often populated by model provider for `AIMessages`)
```python
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

messages = [AIMessage(content=f"So you said you were researching ocean mammals?", name="Model")]
messages.append(HumanMessage(content=f"Yes, that's right.",name="Lance"))
messages.append(AIMessage(content=f"Great, what would you like to learn about.", name="Model"))
messages.append(HumanMessage(content=f"I want to learn about the best place to see Orcas in the US.", name="Lance"))

for m in messages:
    m.pretty_print()
```

```python
results = llm.invoke(messages)
results
results.response_metadata
```

#### Tools

Tools are useful whenever you want a model to interact with external systems.
External systems (e.g., APIs) often require a particular input schema or payload, rather than natural language.
When we bind an API, for example, as a tool we given the model awareness of the required input schema.
The model will choose to call a tool based upon the natural language input from the user.
And, it will return an output that adheres to the tool's schema.
```python
def multiply(a:int, b : int) -> int:
  """MUltiply a and b"""

  return a * b

# llm_with_tools = llm.bind_tools(multiply) llms 
llm_with_tools = llm.bind_tools([multiply]) #gemini

tool_call = llm_with_tools.invoke([HumanMessage(content="What is 2 times 3?",name = "lance")])

tool_call
```

#### MessageState
```python
from typing import TypedDict, List, Dict, Any,Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState

# class MessageState(TypedDict):
#   messages : Annotated[list[AnyMessage], add_messages]

class State(MessageState):
  pass
```
```python
#Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)

graph_builder.add_node("tool_calling_llm", tool_calling_llm)
graph_builder.add_edge(START,"tool_calling_llm")
graph_builder.add_edge("tool_calling_llm",END)

graph = graph_builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
```

```python
messages = graph.invoke({"messages": HumanMessage(content="Hello!")})

for m in messages['messages']:
    m.pretty_print()
```

```python
messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})
for m in messages['messages']:
    m.pretty_print()
```

### Routers
 add new node that calls our tool
add a conditional edge that will look at the cat model output and route to our tool calling node or simply end if no tool call is performed

we use the ToolNode and simply pass a list of our tools
use tools_condition as our conditional edge
```python
def tool_calling_llm(state:MessageState):
  return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(MessageState)

graph_builder.add_node("tool_calling_llm",tool_calling_llm)
graph_builder.add_node("tools",ToolNode([multiply]))

graph_builder.add_edge(START,"tool_calling_llm")
graph_builder.add_conditional_edges("tool_calling_llm",tools_condition)
graph_builder.add_edge("tools",END)

graph = graph_builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
```

```python
messages = [HumanMessage(content = f"MUltiply 3 and 4")]
results = graph.invoke({"messages":messages})

for m in results['messages']:
    m.pretty_print()
    
# ================================ Human Message =================================

# MUltiply 3 and 4
# ================================== Ai Message ==================================
# Tool Calls:
#   multiply (9227c460-a10d-4734-b115-7e9501444108)
#  Call ID: 9227c460-a10d-4734-b115-7e9501444108
#   Args:
#     a: 3.0
#     b: 4.0
# ================================= Tool Message =================================
# Name: multiply

# 12
```

```python
messages = [HumanMessage(content = f"Mr robot")]
results = graph.invoke({"messages":messages})

for m in results['messages']:
    m.pretty_print()

# ================================ Human Message =================================

# Mr robot
# ================================== Ai Message ==================================

# I am here to help, how can I assist?
```

#### ReAct Agents
the above router, we invoked the model and, if it chose to call a tool, we returned a ToolMessage to the user.
But, what if we simply pass that ToolMessage back to the model?

We can let it either (1) call another tool or (2) respond directly.

This is the intuition behind ReAct, a general agent architecture.
act - let the model call specific tools
observe - pass the tool output back to the model
reason - let the model reason about the tool output to decide what to do next (e.g., call another tool or just respond directly)

```python
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [multiply,add,divide]
llm_with_tools = llm.bind_tools(tools)
```

```python
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def assistant(state : MessagesState):
  return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}
```

```python
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display

graph_builder = StateGraph(MessagesState)

graph_builder.add_node("assistant",assistant)
graph_builder.add_node("tools",ToolNode(tools))

graph_builder.add_edge(START,"assistant")
graph_builder.add_conditional_edges("assistant",tools_condition)
graph_builder.add_edge("tools","assistant")
react_graph = graph_builder.compile()

display(Image(react_graph.get_graph().draw_mermaid_png()))
```

```python
messages = [HumanMessage(content = "Add 3 and 4.Multiply the output by 2 and divide the output by 5")]

results = react_graph.invoke({"messages":messages})

for m in results['messages']:
    m.pretty_print()
```

##### Memory
We can use persistence to address this!
LangGraph can use a checkpointer to automatically save the graph state after each step.
This built-in persistence layer gives us memory, allowing LangGraph to pick up from the last state update.
One of the easiest checkpointers to use is the MemorySaver, an in-memory key-value store for Graph state.
All we need to do is simply compile the graph with a checkpointer, and our graph has memory!

```python
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
react_graph_memory = graph_builder.compile(checkpointer=memory)
```

When we use memory, we need to specify a thread_id.
This thread_id will store our collection of graph states.

Here is a cartoon:
The checkpointer write the state at every step of the graph
These checkpoints are saved in a thread
We can access that thread in the future using the thread_id
```python
config = {"configurable":{"thread_id" : "1"}}

messages = [HumanMessage(content = "Add 3 and 4")]

results = react_graph_memory.invoke({"messages":messages},config)

for m in results["messages"]:
  m.pretty_print()
```

If we pass the same thread_id, then we can proceed from from the previously logged state checkpoint!

```python
messages = [HumanMessage(content = "Multiply that by 2")]
results = react_graph_memory.invoke({"messages":messages},config)

for m in results["messages"]:
  m.pretty_print()
```

**Short-term memory**, or [thread](https://langchain-ai.github.io/langgraph/concepts/persistence/#threads)-scoped memory, can be recalled at any time **from within** a single conversational thread with a user. LangGraph manages short-term memory as a part of your agent's [state](https://langchain-ai.github.io/langgraph/concepts/low_level/#state)

State is persisted to a database using a [checkpointer](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpoints) so the thread can be resumed at any time. Short-term memory updates when the graph is invoked or a step is completed, and the State is read at the start of each step.

**Long-term memory** is shared **across** conversational threads. It can be recalled _at any time_ and **in any thread**. Memories are scoped to any custom namespace, not just within a single thread ID. LangGraph provides [stores](https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store) ([reference doc](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)) to let you save and recall long-term memories.

Both are important to understand and implement for your application.

#### Short term memory
This state can normally include the conversation history along with other stateful data, such as uploaded files, retrieved documents, or generated artifacts. By storing these in the graph's state, the bot can access the full context for a given conversation while maintaining separation between different threads.

#### Long Term Memory
LangGraph stores long-term memories as JSON documents in a [store](https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store) ([reference doc](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.BaseStore)). Each memory is organized under a custom `namespace` (similar to a folder) and a distinct `key` (like a filename). Namespaces often include user or org IDs or other labels that makes it easier to organize information. This structure enables hierarchical organization of memories. Cross-namespace searching is then supported through content filters

```C++
from langchain_core.tools import tool

@tool 
def search_knowledge_base(query: str) -> str:
	"""" description:desc """
	return 
```

### ReAct Agent

```python
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END, MessagesState, START
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import os
class AgentState(MessagesState):
  pass

llm = ChatGroq(
    api_key = "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",
    model = "llama-3.3-70b-versatile"
)

def get_weather(location:str) -> str:
  """call to get weather of specific location"""

  if location.lower() in ["sf","san francisco"]:
    return "It's sunny in San Francisco, but you better look out if you're a Gemini 😈."
  else:
    return f"I am not sure what the weather is in {location}"

tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content ="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def assistant(state: MessagesState):
  return {"messages":[llm_with_tools.invoke([sys_msg] + state["messages"])]}

sys_msg = SystemMessage(content="""
You are a helpful assistant tasked with answering questions, including fetching weather information when requested.
Use the get_weather tool for weather queries. If the tool returns a message like 'I am not sure what the weather is in [location]', do not call the tool again. Instead, respond with:
'I cannot provide the current weather for [location]. Please check a weather website or app for up-to-date information.'
""")

# Assistant node function
def assistant(state: MessagesState):
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Build the graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
graph = builder.compile()

# Invoke the graph
messages = [HumanMessage(content="What is the weather in sf?")]
response = graph.invoke({"messages": messages})


# messages = [HumanMessage(content="What is the weather in new york?")]
# response = graph.invoke({"messages": messages})

# Print the response
for m in response["messages"]:
    m.pretty_print()
```

```python
================================ Human Message =================================

What is the weather in new york?
================================== Ai Message ==================================
Tool Calls:
  get_weather (call_0cm4)
 Call ID: call_0cm4
@ahmedelkassrawy ➜ /workspaces/CrewAi (main) $ /home/codespace/.python/current/bin/python /workspaces/CrewAi/src/agent/graph.py
================================ Human Message =================================

What is the weather in sf?
================================== Ai Message ==================================
Tool Calls:
  get_weather (call_cpts)
 Call ID: call_cpts
  Args:
    location: sf
================================= Tool Message =================================
Name: get_weather

It's sunny in San Francisco, but you better look out if you're a Gemini 😈.
================================== Ai Message ==================================

I cannot provide the current weather for sf. Please check a weather website or app for up-to-date information.
```

```python
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import MessagesState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq  # Using Groq for fast LLM inference
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END,START
from langgraph.prebuilt import ToolNode, tools_condition
import os

class AgentState(MessagesState):
  pass

search_tool = TavilySearchResults(max_results=2)  # Limit to 2 results for brevity
tools = [search_tool]


llm = ChatGroq(model = "llama-3.3-70b-versatile",
               api_key = os.environ.get("GROQ_API_KEY"))

llm_with_tools = llm.bind_tools(tools)
  
def conversation_node(state:AgentState):
  response = llm_with_tools.invoke(state["messages"])
  return {"messages":[response]}

builder = StateGraph(AgentState)

builder.add_node("conversation_node", conversation_node)
builder.add_node("tools", ToolNode(tools))  # Name the node "tools" to match tools_condition

# Define edges
builder.add_edge(START, "conversation_node")
builder.add_conditional_edges(
    "conversation_node",  # Changed from "search" to "conversation_node"
    tools_condition,      # tools_condition decides whether to call tools or end
)
builder.add_edge("tools", "conversation_node")  # After tools, go back to conversation

# Compile the graph
graph = builder.compile()
graph

messages = [HumanMessage(content="Who is Andrew Ng")]
result = graph.invoke({"messages": messages})

# Print the final response
for m in result["messages"]:
  m.pretty_print()
```

```python
================================ Human Message ================================= Who is Andrew Ng ================================== Ai Message ================================== Tool Calls: tavily_search_results_json (call_7cra) Call ID: call_7cra Args: query: Andrew Ng biography ================================= Tool Message ================================= Name: tavily_search_results_json [{"title": "Andrew Ng - Wikipedia", "url": "[https://en.wikipedia.org/wiki/Andrew_Ng](https://en.wikipedia.org/wiki/Andrew_Ng)", "content": "Andrew Yan-Tak Ng (Chinese: 吳恩達; born April 18, 1976[2]) is a British-American computer scientist and technology entrepreneur focusing on machine learning and artificial intelligence (AI).[3] Ng was a cofounder and head of Google Brain and was the former Chief Scientist at Baidu, building the company's Artificial Intelligence Group into a team of several thousand people.[4] [...] Appearance\nmove to sidebar hide\nFrom Wikipedia, the free encyclopedia\nAmerican artificial intelligence researcher\nFor the physicist, see Andrew Ng (physicist).\n| \nAndrew Ng\n|\n| --- |\n| \nNg in 2017\n|\n| Born | \nAndrew Yan-Tak Ng\n(1976-04-18) April 18, 1976 (age 48) \nLondon, United Kingdom\n|\n| Nationality | British |\n| Education | Carnegie Mellon University (BS)\nMassachusetts Institute of Technology (MS)\nUniversity of California, Berkeley (PhD) | [...] Ng was born in London, United Kingdom,[10] in 1976 to Ronald Paul Ng, a hematologist and lecturer at UCL Medical School and Tisa Ho, an arts administrator working at the London Film Festival.[11][12][13] His parents were both immigrants from Hong Kong. He has at least one brother.[12] Ng and his family moved back to Hong Kong and he spent his early years there. At the age of six he began learning the basics of programming through some books. In 1984 he and his family moved to Singapore.[10] Ng", "score": 0.8591094}, {"title": "Andrew Ng | Stanford HAI", "url": "[https://hai.stanford.edu/people/andrew-ng](https://hai.stanford.edu/people/andrew-ng)", "content": "Founder of DeepLearning.AI and Adjunct Professor at Stanford University\nAndrew Ng is Founder & CEO of Landing AI, Founder of deeplearning.ai, Co-Chairman and Co-Founder of Coursera, and is currently an Adjunct Professor at Stanford University. He was also Chief Scientist at Baidu Inc., and Founder & Lead for the Google Brain Project.", "score": 0.81595254}] ================================== Ai Message ================================== Andrew Ng is a British-American computer scientist and technology entrepreneur focusing on machine learning and artificial intelligence (AI). He was a cofounder and head of Google Brain and was the former Chief Scientist at Baidu, building the company's Artificial Intelligence Group into a team of several thousand people. Ng was born in London, United Kingdom, in 1976 and spent his early years in Hong Kong and Singapore. He has a background in programming and has founded several companies, including Landing AI and deeplearning.ai, and is an Adjunct Professor at Stanford University.
```

### Streaming

Streaming in LangGraph allows agents to send outputs (e.g., tokens, messages, or intermediate steps) to the user in real-time as they are generated, rather than waiting for the entire process to complete. This improves user experience by reducing perceived latency.
### Types of Streaming

- **Token Streaming**: Streams individual tokens of the LLM’s response (e.g., word-by-word).
- **Message Streaming**: Streams entire messages, such as tool call results or intermediate decisions.
- **Intermediate Step Streaming**: Streams the agent’s actions (e.g., “Calling search tool…”).
### Why Use Streaming?

- **Better UX**: Users see progress immediately, especially for long-running tasks.
- **Transparency**: Shows the agent’s reasoning and actions as they happen.
- **Debugging**: Helps developers monitor the agent’s workflow in real-time.

```python
messages = [HumanMessage(content="Who is Andrew Ng")]

for event in graph.stream({"messages":messages},stream_mode = "updates"):
  for node,state in event.items():
    print(f"Node: {node}")
    print(f"State: {state['messages'][-1].content}")
    print("---")
```

For token by token
```python
llm = ChatGroq(model = "llama-3.3-70b-versatile",
               api_key = os.environ.get("GROQ_API_KEY"),
               streaming = True)
```

## Human-in-the-Loop 
### What Is Human-in-the-Loop (HITL)?

Human-in-the-Loop allows humans to intervene in an agent’s workflow to review, edit, or approve actions before they’re executed. This is critical for:

- **Reliability**: Preventing errors or unintended actions (e.g., in sensitive tasks like finance or healthcare).
- **Debugging**: Inspecting the agent’s state to fix issues.
- **User Control**: Giving users the ability to steer the agent’s behavior.
### How It Works

LangGraph supports HITL through:

- **Checkpointers**: Save the state, allowing resumption after human input.
- **Breakpoints**: Pause the graph at specific nodes (e.g., before a tool call).
- **State Inspection**: Humans can view and modify the state (e.g., edit messages).

```python
graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["action"]  # Pause before tool calls
)
```

```python
config = {"configurable": {"thread_id": "3"}}
messages = [HumanMessage(content="What is the weather in Chicago?")]

# Run until interruption
for event in graph.stream({"messages": messages}, config=config, stream_mode="updates"):
    for node, state in event.items():
        print(f"Node: {node}")
        print(f"State: {state['messages'][-1].content}")
        print("---")

# Check if the graph is paused
state = graph.get_state(config)
if state.next:
    print("Paused for human input. Current state:")
    print(state.values["messages"][-1].tool_calls)  # Show the proposed tool call

    # Human reviews and approves (or modifies) the tool call
    approve = input("Approve tool call? (yes/no): ")
    if approve.lower() == "yes":
        # Resume the graph
        for event in graph.stream(None, config=config, stream_mode="updates"):
            for node, state in event.items():
                print(f"Node: {node}")
                print(f"State: {state['messages'][-1].content}")
                print("---")
    else:
        print("Tool call rejected. Stopping.")
```

#### What Happens?

1. The agent processes the query and proposes a search tool call (e.g., TavilySearchResults(query="Chicago weather")).
2. The graph pauses before the action node due to interrupt_before=["action"].
3. The human sees the proposed tool call and decides to approve or reject it.
4. If approved, the graph resumes, executes the search, and completes the response.
5. If rejected, the graph stops or can be modified (e.g., edit the query)

## RAG 

Use chains in RAGs and every thing related to tools or nodes that will take a prompt and make sure if there is a related input you should enter.

```python
builder.add_conditional_edges("agent", tools_condition, {
        "tools": "retrieve",
        "continue": "rewrite"
    })

builder.add_conditional_edges("retrieve", grade_docs, {
        "generate": "generate",
        "rewrite": "rewrite"
    })
```

**Example of RAG:**

```python
loader = WebBaseLoader(url)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=50)

chunks = splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(
	model="models/embedding-001",
	google_api_key=os.environ.get("GOOGLE_API_KEY"),
)

vectorstore = QdrantVectorStore.from_documents(
	documents=chunks,
	embedding=embeddings,
	collection_name="qdrant_db",
	url=os.environ.get("QDRANT_URL"),
	api_key=os.environ.get("QDRANT_API_KEY"),
	force_recreate=True
)

retriever = vectorstore.as_retriever(search_type="similarity", 
										search_kwargs={"k": 5})

retriever_tool = create_retriever_tool(
	retriever,
	"the_task",
	"task desc",
)

prompt = hub.pull("rlm/rag-prompt")
```