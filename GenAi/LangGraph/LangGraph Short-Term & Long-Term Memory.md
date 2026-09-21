---
description: "LangGraph memory end to end — short-term via checkpointer/thread_id/snapshots (with time-travel), long-term via the namespaced Store (put/get/search + semantic recall), and when to use which. Code for both."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/langgraph
  - topic/agents
  - topic/memory
  - langgraph
  - memory
  - checkpointer
  - store
  - snapshots
aliases:
  - "checkpointer"
  - "thread_id"
  - "snapshots"
  - "long-term memory"
  - "store"
hubs:
  - "[[LangGraph]]"
  - "[[Agent Memory]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# LangGraph Short-Term & Long-Term Memory

> Related: [[LangGraph Human In The Loop And Checkpointers]] · [[LangGraph Long-Term Memory With Trustcall]] · [[Mem0.Agents Memory]] · [[Agent Memory with Redis]].

Two different mechanisms, often confused:

```text
SHORT-TERM (checkpointer)          LONG-TERM (store)
 keyed by thread_id                 keyed by user_id (namespace)
 one conversation's state           facts that outlive every conversation
 auto-saved each step               YOU decide what to save
 "what did we just say?"            "what do I know about this user?"
```

---

# Short-term memory — checkpoints & snapshots

State normally vanishes when `.invoke()` returns. A **checkpointer** saves a **snapshot of the full state after every step**, keyed by a **`thread_id`**. Re-invoke with the same `thread_id` → it reloads the last snapshot and continues. That's short-term memory.

```text
thread "chat-42":
  invoke 1 → [step]→snap → [step]→snap → returns   (state saved)
  invoke 2 (same thread_id)      → loads last snap → continues with full history
  invoke 2 (different thread_id) → fresh, remembers nothing
```

> [!definition] Checkpointer / thread / snapshot
> **Checkpointer** = saves state. **Snapshot (checkpoint)** = one saved copy of the full state at a point in the run. **thread_id** = the key grouping snapshots into one conversation. Same thread_id = same memory; different = clean slate.

## Turning it on
```python
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

checkpointer = MemorySaver()
agent = g.compile(checkpointer=checkpointer)

cfg = {"configurable": {"thread_id": "chat-42"}}

agent.invoke({"messages": [HumanMessage("My name is Kassra.")]}, cfg)   # turn 1
agent.invoke({"messages": [HumanMessage("What's my name?")]}, cfg)      # turn 2
#   → "Your name is Kassra."   (turn 1 still in state, same thread_id)
```
The mechanism is just: **checkpointer + the `add_messages` reducer + thread_id**. Same thread reloads the accumulated messages, so the model sees the whole conversation.

## Snapshots: read & rewind
```python
# CURRENT snapshot
snap = agent.get_state(cfg)
print(snap.values["messages"])   # state right now
print(snap.next)                 # next node to run ("" = done)

# ALL snapshots, newest first
for s in agent.get_state_history(cfg):
    print(s.config["configurable"]["checkpoint_id"], len(s.values["messages"]))

# TIME-TRAVEL: resume from an older snapshot (fork the timeline)
old = list(agent.get_state_history(cfg))[3]
agent.invoke({"messages": [HumanMessage("actually, redo it this way")]}, old.config)
```
```text
snap0 → snap1 → snap2 → snap3 → snap4
                 └── resume here → new branch (retry / time-travel)
```

## HITL runs on this
`interrupt` pauses the graph, saves a snapshot, returns control to you; resuming reloads that snapshot and continues. No checkpointer → no pause/resume. See [[LangGraph Human In The Loop And Checkpointers]].

## Where snapshots live
| Backend | Survives | Use for |
|---|---|---|
| `MemorySaver` | RAM only — gone on restart | dev, tests, demos |
| `SqliteSaver` | a local file | single-box apps |
| `PostgresSaver` | a real DB | production, multi-instance |

Swapping is a one-line change; graph code is identical.

---

# Long-term memory — the Store

Checkpoints forget at the thread boundary. Long-term memory is a separate **Store**, **namespaced by user**, that persists across all threads — facts you *choose* to write and read back in any future conversation.

> [!definition] Store (long-term memory)
> A namespaced key-value store that outlives every thread. The checkpointer saves conversation state automatically; the store holds durable facts you deliberately write — "prefers dark mode", "is vegetarian", "works at Shutterabia".

## The Store API
Pass a `store` at compile (alongside the checkpointer); nodes get it injected.

```python
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver

store = InMemoryStore()
agent = g.compile(checkpointer=MemorySaver(), store=store)   # BOTH at once

def remember(state, *, store):            # store injected into the node
    uid = state["user_id"]
    ns = ("memories", uid)                # namespace = per user
    store.put(ns, "diet", {"fact": "vegetarian"})   # WRITE a fact
    hits = store.search(ns)                          # READ this user's facts
    return {"context": [h.value["fact"] for h in hits]}
```

Three operations:
```text
store.put(namespace, key, value)   → save / overwrite a fact
store.get(namespace, key)          → fetch one fact
store.search(namespace, query=...) → find relevant facts
```
Namespaced by `user_id` (not `thread_id`), so a fact from one chat is present in **every** future chat for that user.

## Semantic recall
Give the store an embedder → `search` does vector similarity, pulling only the *relevant* memories into the prompt (same idea as raaaaag retrieval, aimed at a user's memory).

```python
store = InMemoryStore(index={"embed": embeddings, "dims": 1536})
hits = store.search(("memories", uid), query="what should I cook?")
#   → returns the "vegetarian" memory (semantically close)
```

## The three kinds
| Type | Holds | Example |
|---|---|---|
| **Semantic** | facts about the user/world | "Kassra is vegetarian" |
| **Episodic** | past events/interactions | "last time they asked for a refund" |
| **Procedural** | how to behave | "always answer concisely" |

## The hard part: what to write, and when
Checkpoints are automatic; long-term memory is **your** decision — the whole difficulty.
- **When to write:** after a turn, extract durable facts (often a small LLM call: "any facts worth keeping?").
- **The trap:** "append every message" bloats the store with junk. **Trustcall** *updates a structured profile* instead of piling raw text — "vegetarian" gets corrected to "vegan", not duplicated. See [[LangGraph Long-Term Memory With Trustcall]].

```text
turn ends → extract facts → store.put(("memories", uid), ...)          [write path]
new turn  → store.search(("memories", uid), query=msg) → inject → LLM  [read path]
```

---

# Choosing + mental model

> [!warning] Don't use the wrong tool
> **Across sessions / per user → store** (long-term). **Within one session → checkpointer** (short-term). Checkpoints for cross-session memory fail silently (different thread = gone); a store for turn-by-turn state is overkill and loses ordering.

> [!tip] Mental model
> **Checkpointer = the save-file for one conversation. Store = the user's profile every conversation reads.** Short-term is automatic + thread-scoped + auto-loaded; long-term is deliberate + user-scoped + usually semantically searched. The skill in long-term is *curating what goes in*, not the API.

## Both together — the full compile
```python
agent = g.compile(
    checkpointer=MemorySaver(),   # short-term: this conversation's state
    store=InMemoryStore(),        # long-term: facts across all conversations
)
# short-term key comes from thread_id at invoke; long-term key is the namespace in nodes
cfg = {"configurable": {"thread_id": "chat-42"}}
agent.invoke({"messages": [...], "user_id": "kassra"}, cfg)
```

**In raaaaag (M5 W1):** the checkpointer made the answer loop **durable** (state saved each step → crash resumes mid-flow) — same short-term machinery, framed as durability. Long-term (a per-user store) would be the next layer if the agent needed to remember a user across sessions.

---

## Salvaged from LangGraph Memory (raw)

Raw code pasted from the old `LangGraph Memory` note. The checkpointer/`get_state`/`get_state_history` mechanics above already cover its memory bits; kept below are the graph examples it uniquely had.

Basic ReAct graph with `ToolNode` + `tools_condition`:
```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages

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

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")
agent = graph.compile()
```

Same wiring, but the tool is a RAG retriever:
```python
loader = PyPDFLoader("intro-to-ml.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':4})

@tool
def rag_tool(query):
  """Retrieve relevant information from the pdf document."""
  result = retriever.invoke(query)
  return {
      'query': query,
      'context': [doc.page_content for doc in result],
      'metadata': [doc.metadata for doc in result],
  }

tools = [rag_tool]
llm_with_tools = llm.bind_tools(tools)
# ... same StateGraph(chat_node + ToolNode) as above ...
```

HITL approval loop with `Command(resume=...)`:
```python
from langgraph.types import Command

def run_agent_with_approval(agent, input_data, config):
  response = agent.invoke(input_data, config = config)
  while response.get("__interrupt__"):
    interrupt = response["__interrupt__"][0]
    details = interrupt.value
    print(f"\n[INTERRUPT]: {details.get('reason', 'Approval Required')}")
    print(f"Question: {details.get('question', '')}")
    user_input = input(f"{details.get('instruction', 'Approve? (yes/no): ')} ")
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
