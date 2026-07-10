InMemorySaver:
```python
checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)
```

```python
config1 = {"configurable": {"thread_id": "1"}}

agent.invoke({"topic":"pizza"},config = config1)
agent.get_state(config1)
```
**Use `get_state(config)` to retrieve the current state of a thread**

**`get_state_history(config)` to view the full chronological history of checkpoints.**
```python
for snapshot in agent.get_state_history(config1):
    print(f"Checkpoint ID: {snapshot.config['configurable']['checkpoint_id']}")
    print(f"Values at this step: {snapshot.values}")
    print("---")
```

---
```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

@tool
def add(a:int,b:int) -> int:
	"""Perform a basic add"""
	return a * b
	
tools = [add]
llm_with_tools = llm.bind_tools(tools)

def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response]}

tool_node = ToolNode(tools)
```

```python
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")

agent = graph.compile()
```

```python
response = agent.invoke(
    {
        "messages": [HumanMessage(content = "Hello!")]
    }
)
response["messages"][-1].content
```
-----
```python
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

loader = PyPDFLoader("intro-to-ml.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':4})

@tool
def rag_tool(query):
  """
  Retrieve relevant information from the pdf document.
  Use this tool when the user asks factual / conceptual questions
  that might be answered from the stored documents.
  """
  result = retriever.invoke(query)

  context = [doc.page_content for doc in result]
  metadata = [doc.metadata for doc in result]

  return {
      'query': query,
      'context': context,
      'metadata': metadata
  }

tools = [rag_tool]
llm_with_tools = llm.bind_tools(tools)

def chat_node(state: ChatState):
  messages = state['messages']
  response = llm_with_tools.invoke(messages)

  return {'messages': [response]}

tool_node = ToolNode(tools)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')

agent = graph.compile()

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Using the pdf notes, explain how to find the ideal value of K in KNN"
                )
            )
        ]
    }
)
```
---
HITL 
```python
from langgraph.types import Command

def run_agent_with_approval(agent, input_data, config):
  response = agent.invoke(input_data, config = config)

  #check for interrupts in a loop
  while response.get("__interrupt__"):
    interrupt = response["__interrupt__"][0]
    details = interrupt.value

    #display prompt to the user
    print(f"\n[INTERRUPT]: {details.get('reason', 'Approval Required')}")
    print(f"Question: {details.get('question', '')}")

    user_input = input(f"{details.get('instruction', 'Approve? (yes/no): ')} ")


    #resume the graph
    response = agent.invoke(
        Command(resume = {"approved":user_input}),
        config = config
    )
    return response

config = {"configurable": {"thread_id": "1234"}}
initial_input = {"messages": [("user", "Explain gradient descent.")]}

response = run_agent_with_approval(agent, initial_input, config)
response["messages"][-1].content
```