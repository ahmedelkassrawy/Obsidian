# Agent Memory with Redis Study Guide

This guide summarizes the "Agent Memory with Redis" tutorial, which demonstrates building a **memory-enabled travel agent** using **Redis** and **LangGraph**. It covers short-term and long-term memory management, vector-powered semantic search, and conversation summarization, with practical code snippets for study. Key concepts are linked to enterprise RAG system design principles for broader applicability.

## 📚 Introduction

AI agents without memory are limited, forgetting context after each interaction. This tutorial builds a **travel agent** that remembers user preferences and provides personalized recommendations using:

- **Short-term memory**: Manages conversation context via LangGraph's checkpointer.
- **Long-term memory**: Stores persistent knowledge (episodic and semantic) in Redis using RedisVL.
- **Tool-based memory management**: Allows the LLM to store/retrieve memories.
- **Conversation summarization**: Manages context window size.

> [!note]
> This is a **horizontal concept** applicable to any agent use case requiring state management (e.g., enterprise RAG systems for document retrieval).

---

## 🧠 Memory Architecture Overview

The agent uses a **dual-memory system**:

### Short-Term Memory
- **Purpose**: Tracks conversation history within a session.
- **Implementation**: Uses LangGraph's `RedisSaver` checkpointer to store state (e.g., messages, thread metadata) in Redis.
- **Diagram**:
  ![Short-term Memory Diagram](assets/short-term-memory.png)

> [!tip]
> Summarize conversations when they exceed a threshold to prevent context window overflow.

### Long-Term Memory
- **Purpose**: Stores persistent knowledge for future sessions.
- **Types** (aligned with [CoALA paper](https://arxiv.org/abs/2309.02427)):
  - **Episodic**: User-specific preferences/experiences (e.g., "User prefers Delta airlines").
  - **Semantic**: General knowledge (e.g., "Tokyo has excellent public transit").
- **Implementation**: Uses RedisVL for vector embeddings and semantic search.
- **Diagram**:
  ![Long-term Memory Diagram](assets/long-term-memory.png)

> [!important]
> Metadata (e.g., user_id, memory_type) is critical for filtering and retrieval, especially in enterprise RAG systems where context drives query accuracy.

---
## 🛠️ Environment Setup

### Dependencies
Install required Python libraries:

```python
pip install langchain-openai langgraph-checkpoint langgraph langgraph-checkpoint-redis langchain-redis
```

---
### API Keys
Set up an OpenAI API key:

```python
import getpass
import os

def _set_env(key: str):
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}:")
_set_env("OPENAI_API_KEY")
```

### Redis Setup
Options:
1. **Redis Cloud**: Use a free instance ([redis.io/try-free](https://redis.io/try-free)).
2. **Local Redis**: Install locally (e.g., on Colab):

```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update  > /dev/null 2>&1
sudo apt-get install redis-stack-server  > /dev/null 2>&1
redis-stack-server --daemonize yes
```

Test Redis connection:

```python
from redis import Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = Redis.from_url(REDIS_URL)
redis_client.ping()  # Returns True if successful
```

---

## 📦 Memory Data Models

Define type-safe data models using Pydantic for memory lifecycle management:

```python
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import ulid

class MemoryType(str, Enum):
    EPISODIC = "episodic"  # User preferences/experiences
    SEMANTIC = "semantic"  # General knowledge

class Memory(BaseModel):
    content: str
    memory_type: MemoryType
    metadata: str

class Memories(BaseModel):
    memories: List[Memory]

class StoredMemory(Memory):
    id: str
    memory_id: ulid.ULID = Field(default_factory=lambda: ulid.ULID())
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    thread_id: Optional[str] = None
```

> [!tip]
> Use structured metadata (e.g., user_id, thread_id) to filter memories, aligning with enterprise RAG metadata schemas for contextual retrieval.

---

## 🗄️ Memory Storage

### Short-Term Memory
- Handled by `RedisSaver` from `langgraph-checkpoint-redis`.
- Stores conversation state (messages, metadata) automatically.

### Long-Term Memory
- Stored in Redis using RedisVL with vector embeddings for semantic search.
- Schema for `agent_memories` index:

```python
from redisvl.index import SearchIndex
from redisvl.schema.schema import IndexSchema

memory_schema = IndexSchema.from_dict({
    "index": {
        "name": "agent_memories",
        "prefix": "memory",
        "key_separator": ":",
        "storage_type": "json"
    },
    "fields": [
        {"name": "content", "type": "text"},
        {"name": "memory_type", "type": "tag"},
        {"name": "metadata", "type": "text"},
        {"name": "created_at", "type": "text"},
        {"name": "user_id", "type": "tag"},
        {"name": "memory_id", "type": "tag"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "algorithm": "flat",
                "dims": 1536,  # OpenAI embedding dimension
                "distance_metric": "cosine",
                "datatype": "float32"
            }
        }
    ]
})

long_term_memory_index = SearchIndex(schema=memory_schema, redis_client=redis_client)
long_term_memory_index.create(overwrite=True)
```

Inspect index:

```bash
rvl index info -i agent_memories
```

---

## 🔧 Memory Management Functions

### 1. Check for Similar Memories
Prevent duplicates by checking for similar memories:

```python
from redisvl.query import VectorRangeQuery
from redisvl.query.filter import Tag

SYSTEM_USER_ID = "system"

def similar_memory_exists(content: str, memory_type: MemoryType, user_id: str = SYSTEM_USER_ID, thread_id: Optional[str] = None, distance_threshold: float = 0.1) -> bool:
    content_embedding = openai_embed.embed(content)
    filters = (Tag("user_id") == user_id) & (Tag("memory_type") == memory_type)
    if thread_id:
        filters &= Tag("thread_id") == thread_id
    vector_query = VectorRangeQuery(
        vector=content_embedding,
        num_results=1,
        vector_field_name="embedding",
        filter_expression=filters,
        distance_threshold=distance_threshold,
        return_fields=["id"]
    )
    results = long_term_memory_index.query(vector_query)
    return bool(results)
```

### 2. Store Long-Term Memories
Store memories with deduplication:

```python
def store_memory(content: str, memory_type: MemoryType, user_id: str = SYSTEM_USER_ID, thread_id: Optional[str] = None, metadata: Optional[str] = None):
    if metadata is None:
        metadata = "{}"
    if similar_memory_exists(content, memory_type, user_id, thread_id):
        return
    embedding = openai_embed.embed(content)
    memory_data = {
        "user_id": user_id or SYSTEM_USER_ID,
        "content": content,
        "memory_type": memory_type.value,
        "metadata": metadata,
        "created_at": datetime.now().isoformat(),
        "embedding": embedding,
        "memory_id": str(ulid.ULID()),
        "thread_id": thread_id
    }
    long_term_memory_index.load([memory_data])
```

### 3. Retrieve Long-Term Memories
Retrieve memories using vector similarity search:

```python
def retrieve_memories(query: str, memory_type: Optional[List[MemoryType]] = None, user_id: str = SYSTEM_USER_ID, thread_id: Optional[str] = None, distance_threshold: float = 0.1, limit: int = 5) -> List[StoredMemory]:
    vector_query = VectorRangeQuery(
        vector=openai_embed.embed(query),
        return_fields=["content", "memory_type", "metadata", "created_at", "memory_id", "thread_id", "user_id"],
        num_results=limit,
        vector_field_name="embedding",
        distance_threshold=distance_threshold
    )
    base_filters = [f"@user_id:{{{user_id or SYSTEM_USER_ID}}}"]
    if memory_type:
        if isinstance(memory_type, list):
            base_filters.append(f"@memory_type:{{{'|'.join(mt.value for mt in memory_type)}}}")
        else:
            base_filters.append(f"@memory_type:{{{memory_type.value}}}")
    if thread_id:
        base_filters.append(f"@thread_id:{{{thread_id}}}")
    vector_query.set_filter(" ".join(base_filters))
    results = long_term_memory_index.query(vector_query)
    return [StoredMemory(**doc) for doc in results]
```

> [!important]
> Deduplication prevents redundant storage, critical for enterprise RAG systems to maintain clean, efficient memory stores.

---

## 🛠️ Agent Tools

Expose memory operations as LLM-callable tools:

### Store Memory Tool
Saves user preferences or knowledge:

```python
from langchain_core.tools import tool

@tool
def store_memory_tool(content: str, memory_type: MemoryType, metadata: Optional[Dict[str, str]] = None, config: Optional[RunnableConfig] = None) -> str:
    config = config or RunnableConfig()
    user_id = config.get("user_id", SYSTEM_USER_ID)
    thread_id = config.get("thread_id")
    store_memory(content, memory_type, user_id, thread_id, str(metadata) if metadata else None)
    return f"Successfully stored {memory_type} memory: {content}"
```

Test:

```python
store_memory_tool.invoke({"content": "I like flying on Delta when possible", "memory_type": "episodic"})
```

### Retrieve Memories Tool
Retrieves relevant memories:

```python
@tool
def retrieve_memories_tool(query: str, memory_type: List[MemoryType], limit: int = 5, config: Optional[RunnableConfig] = None) -> str:
    config = config or RunnableConfig()
    user_id = config.get("user_id", SYSTEM_USER_ID)
    stored_memories = retrieve_memories(query, memory_type, user_id, limit=limit, distance_threshold=0.3)
    response = ["Long-term memories:"] if stored_memories else ["No relevant memories found."]
    for memory in stored_memories:
        response.append(f"- [{memory.memory_type}] {memory.content}")
    return "\n".join(response)
```

Test:

```python
retrieve_memories_tool.invoke({"query": "Airline preferences", "memory_type": ["episodic"]})
```

> [!tip]
> Tool-based memory management balances control and efficiency, but manual management may be preferred for enterprise RAG systems needing richer context.

---

## 🌎 Travel Agent Workflow

### Setup ReAct Agent
Uses LangGraph's `create_react_agent` with Redis checkpointer:

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langgraph.checkpoint.redis import RedisSaver

redis_saver = RedisSaver(redis_client=redis_client)
redis_saver.setup()
llm = ChatOpenAI(model="gpt-4o", temperature=0.7).bind_tools(tools)
travel_agent = create_react_agent(
    model=llm,
    tools=[store_memory_tool, retrieve_memories_tool],
    checkpointer=redis_saver,
    prompt=SystemMessage(content="You are a travel assistant...")  # See full prompt in notebook
)
```

### Workflow Nodes
1. **Respond to User**:
   - Handles user input, invokes the agent, and updates conversation state.
   - Code:

```python
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import MessagesState

class RuntimeState(MessagesState):
    pass

def respond_to_user(state: RuntimeState, config: RunnableConfig) -> RuntimeState:
    human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    if not human_messages:
        return state
    result = travel_agent.invoke({"messages": state["messages"]}, config=config)
    state["messages"].append(result["messages"][-1])
    return state
```

2. **Execute Tools**:
   - Processes tool calls (e.g., store/retrieve memories).
   - Code:

```python
from langchain_core.messages import ToolMessage

def execute_tools(state: RuntimeState, config: RunnableConfig) -> RuntimeState:
    messages = state["messages"]
    latest_ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage) and m.tool_calls), None)
    if not latest_ai_message:
        return state
    tool_messages = []
    for tool_call in latest_ai_message.tool_calls:
        tool = next((t for t in tools if t.name == tool_call["name"]), None)
        if tool:
            result = tool.invoke(tool_call["args"], config=config)
            tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"], name=tool_call["name"]))
    state["messages"].extend(tool_messages)
    return state
```

3. **Summarize Conversation**:
   - Summarizes history after 6 messages to manage context window.
   - Code:

```python
summarizer = ChatOpenAI(model="gpt-4o", temperature=0.3)
MESSAGE_SUMMARIZATION_THRESHOLD = 6

def summarize_conversation(state: RuntimeState, config: RunnableConfig) -> RuntimeState:
    messages = state["messages"]
    if len(messages) < MESSAGE_SUMMARIZATION_THRESHOLD:
        return state
    message_content = "\n".join([f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content}" for msg in messages])
    summary_response = summarizer.invoke([
        SystemMessage(content="You are a conversation summarizer..."),
        HumanMessage(content=f"Please summarize this conversation:\n\n{message_content}")
    ])
    summary_message = SystemMessage(content=f"Summary of the conversation so far:\n\n{summary_response.content}\n\nPlease continue...")
    state["messages"] = [RemoveMessage(id=msg.id) for msg in messages if msg.id] + [summary_message, messages[-1]]
    return state
```

### Assemble Graph
Define workflow with conditional edges:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(RuntimeState)
workflow.add_node("agent", respond_to_user)
workflow.add_node("execute_tools", execute_tools)
workflow.add_node("summarize_conversation", summarize_conversation)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    lambda state: "execute_tools" if any(isinstance(m, AIMessage) and m.tool_calls for m in reversed(state["messages"])) else "summarize_conversation",
    {"execute_tools": "execute_tools", "summarize_conversation": "summarize_conversation"}
)
workflow.add_edge("execute_tools", "agent")
workflow.add_edge("summarize_conversation", END)
graph = workflow.compile(checkpointer=redis_saver)
```

---

## 🚀 Testing the Agent

Run the main interaction loop:

```python
def main(thread_id: str = "book_flight", user_id: str = "demo_user"):
    config = RunnableConfig(configurable={"thread_id": thread_id, "user_id": user_id})
    state = RuntimeState(messages=[])
    while True:
        user_input = input("\nYou (type 'quit' to quit): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        state["messages"].append(HumanMessage(content=user_input))
        for result in graph.stream(state, config=config, stream_mode="values"):
            state = RuntimeState(**result)
        ai_message = next((m.content for m in reversed(state["messages"]) if isinstance(m, AIMessage)), "Error processing request.")
        print(f"\nAssistant: {ai_message}")
```

Example interaction:

- User: "I plan to go to Singapore... love outdoor activities and trying new foods."
- Agent: Stores episodic memory, suggests Gardens by the Bay, hawker centers.
- User: "Help booking flights... prefer Delta and first class."
- Agent: Stores preference, suggests ATL-SIN via Tokyo, mentions Delta One upgrades.
- User: "Wife is allergic to shellfish."
- Agent: Stores allergy, adjusts recommendations.

> [!note]
> The agent automatically stores key user preferences (e.g., Delta, shellfish allergy) and retrieves them for personalized responses, demonstrating memory persistence.

---

## 📊 Recap and Key Takeaways

### Achievements
- **Dual-Memory System**: Short-term (conversation state) and long-term (persistent knowledge) memory using Redis.
- **Vector Search**: Semantic retrieval with RedisVL for context-aware responses.
- **Deduplication**: Prevents redundant memory storage.
- **Summarization**: Manages context window with concise summaries.
- **Tools**: LLM-driven memory management for efficiency.

### Why Redis?
- **Performance**: Sub-millisecond retrieval.
- **Versatility**: Handles structured (checkpoints) and unstructured (vectors) data.
- **Production-Ready**: Persistence, clustering, high availability.
- **Developer-Friendly**: Integrates with AI frameworks like LangGraph.

### Integration with Enterprise RAG
- **Document Quality Detection**: Assess document quality before processing to tailor pipelines (e.g., clean PDFs vs. scanned notes), as emphasized in the enterprise RAG post.
- **Metadata Schemas**: Use domain-specific metadata (e.g., user_id, memory_type) for filtering, aligning with the post’s focus on metadata-driven retrieval.
- **Hybrid Retrieval**: Combine semantic search with rule-based filtering (e.g., for user_id) to address semantic failures in specialized domains.
- **Table Processing**: Extend memory system to handle tabular data (e.g., flight schedules) by treating tables as separate entities with structured metadata.

### Alternative Frameworks
- **LangMem**: For LangChain integration and rapid prototyping.
- **Mem0**: For multi-application memory sharing and enterprise features.

---

## 🔄 Next Steps
- **Enhance Metadata**: Add domain-specific schemas (e.g., travel preferences, dietary restrictions) for richer context, as suggested in the enterprise RAG post.
- **Improve Deduplication**: Fine-tune `distance_threshold` for better duplicate detection.
- **Handle Tables**: Implement table processing pipelines for structured data (e.g., flight schedules).
- **Optimize Infrastructure**: Use quantized models and semaphores for concurrent users, as recommended in the enterprise RAG post.
- **Explore Redis Cloud**: For production-grade scalability and persistence.
---