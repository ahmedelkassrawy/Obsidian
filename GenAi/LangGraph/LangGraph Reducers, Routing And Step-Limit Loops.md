---
description: "How LangGraph merges state (reducers), decides the next node (conditional routing), branches many ways (multi-way routing), and caps the agent loop (step-limit guard) — with runnable code."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/langgraph
  - topic/agents
  - langgraph
  - reducers
  - routing
  - state
  - agent-loop
aliases:
  - "reducers"
  - "conditional routing"
  - "step limit"
  - "should_continue"
hubs:
  - "[[LangGraph]]"
  - "[[Agents]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# LangGraph Reducers, Routing & Step-Limit Loops

> Prereq: [[LangGraph Nodes Edges And State]]. Related: [[LangGraph Routing And Path Maps]]. Four pieces that turn a graph into a real agent — how state **merges**, how control **branches**, and how the loop is **capped**.

## 1. Reducers — how state updates get merged

State is shared, and multiple nodes write to it. When a node returns `{"messages": [new]}`, does it **replace** the list or **append**? A **reducer** decides.

> [!definition] Reducer
> A function on a state field that combines the **old** value with the **new** value a node returns. No reducer = **overwrite** (last write wins). An "add" reducer = **append/merge**. Attached with `Annotated[type, reducer_fn]`.

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
import operator

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]     # append new messages
    retrieved_docs: Annotated[list, operator.add]  # concatenate lists
    current_query: str                          # no reducer → overwrite
```

```text
state.messages = [A, B]
node returns {"messages": [C]}

with add_messages → [A, B, C]   (appended)
no reducer        → [C]         (overwritten)
```

The agent loop works **because** `messages` appends every turn — overwrite would lose the conversation each step. `add_messages` is like `operator.add` but also de-dupes by message id and allows in-place updates.

> [!tip] Rule of thumb
> **Accumulating** across the loop (messages, docs, a counter) → give it an **add** reducer. A field that's just "the latest value" (a flag, current step name) → **no reducer**.

## 2. Conditional routing — the agent decides where to go next

A normal edge always goes to the same node. A **conditional edge** picks the next node from the current state — this is what makes an agent a loop instead of a line.

> [!definition] Conditional edge
> An edge whose target is chosen by a **router function** you write: read state, return a string; that string maps to the next node. The router does **nothing else** — no state mutation, no work.

The classic `should_continue` (tools-vs-end):

```python
from langgraph.graph import StateGraph, START, END

def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else "end"

g.add_conditional_edges("model", should_continue,
                        {"tools": "tools", "end": END})
g.add_edge("tools", "model")   # plain back-edge → the loop
```

```text
START → model ──should_continue──▶ tools ──▶ model ──▶ ...
                     │
                     └─(no tool call)──▶ END
```

## 3. Runnable end-to-end agent

```bash
pip install langgraph langchain-openai langchain-core
```

```python
# agent.py
import os
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

@tool
def word_count(text: str) -> int:
    """Count the words in a piece of text."""
    return len(text.split())

TOOLS = {"word_count": word_count}

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
).bind_tools(list(TOOLS.values()))

def call_model(state: AgentState):
    resp = llm.invoke(state["messages"])
    print(f"  [model] tool_calls={[c['name'] for c in resp.tool_calls]}")
    return {"messages": [resp]}

def call_tools(state: AgentState):
    out = []
    for call in state["messages"][-1].tool_calls:
        result = TOOLS[call["name"]].invoke(call["args"])
        print(f"  [tool ] {call['name']}({call['args']}) -> {result}")
        out.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return {"messages": out}

def should_continue(state: AgentState) -> str:
    return "tools" if state["messages"][-1].tool_calls else "end"

g = StateGraph(AgentState)
g.add_node("model", call_model)
g.add_node("tools", call_tools)
g.add_edge(START, "model")
g.add_conditional_edges("model", should_continue, {"tools": "tools", "end": END})
g.add_edge("tools", "model")
agent = g.compile()

if __name__ == "__main__":
    final = agent.invoke({"messages": [
        HumanMessage(content="How many words are in 'the cat sat on the mat'?")
    ]})
    print("\nFINAL:", final["messages"][-1].content)
```

Output — loop + reducer both visible:
```text
  [model] tool_calls=['word_count']    ← turn 1: model asks for the tool
  [tool ] word_count({'text': 'the cat sat on the mat'}) -> 6
  [model] tool_calls=[]                 ← turn 2: model answers
FINAL: There are 6 words in "the cat sat on the mat".
```
`messages` grew 1 → 4 (human, AI+tool-call, tool-result, AI-answer) via the **reducer**; the loop ran twice via **should_continue**.

> [!note] Shortcut
> `call_tools` can be replaced by LangGraph's prebuilt `ToolNode(list(TOOLS.values()))`. Hand-written here so the mechanism is visible.

## 4. Multi-way routing — branch to different paths

Two ways to route beyond tools-vs-end.

**Pattern A — route on which tool the model picked:**
```python
def route_by_tool(state: AgentState) -> str:
    last = state["messages"][-1]
    if not last.tool_calls:
        return "end"
    return last.tool_calls[0]["name"]      # "word_count" | "web_search" | ...

g.add_conditional_edges("model", route_by_tool, {
    "word_count": "word_count_node",
    "web_search": "web_search_node",
    "end": END,
})
```

**Pattern B — a classifier node routes by intent (branch before any tool):**
```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    route: str                              # overwrite → holds latest decision

def classify(state: AgentState):
    q = state["messages"][-1].content.lower()
    if any(w in q for w in ("price", "cost", "$")): route = "billing"
    elif "error" in q or "broken" in q:             route = "support"
    else:                                           route = "chat"
    return {"route": route}

def route_by_intent(state: AgentState) -> str:
    return state["route"]

g.add_conditional_edges("classify", route_by_intent, {
    "billing": "billing", "support": "support", "chat": "chat",
})
```
```text
                 ┌─ "billing" → billing_node → END
START → classify ─┼─ "support" → support_node → END
                 └─ "chat"    → chat_node    → END
```

> [!tip] Same mechanism, more keys
> Two-way and N-way routing are identical — the router returns a string, the `{...}` map picks the node. **Pattern A** = an agent with several tools. **Pattern B** = branch before the LLM (triage, cost control, guardrails). Shutterabia fit: a `classify` node routing to publish / analytics / support.

## 5. Step-limit loop — don't spin forever

A confused model can loop calling tools endlessly. Cap it with a **counter in state** the router checks.

```python
# agent_with_limit.py (key parts)
import operator
from langchain_core.messages import AIMessage

MAX_STEPS = 5

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    steps: Annotated[int, operator.add]     # add reducer → each turn INCREMENTS

def call_model(state: AgentState):
    resp = llm.invoke(state["messages"])
    return {"messages": [resp], "steps": 1}  # +1 per model turn

def should_continue(state: AgentState) -> str:
    if state["steps"] >= MAX_STEPS:
        return "give_up"                     # hit the cap → bail out
    if state["messages"][-1].tool_calls:
        return "tools"
    return "end"

def give_up(state: AgentState):
    return {"messages": [AIMessage(
        content=f"Stopped after {MAX_STEPS} steps without finishing."
    )]}

g.add_node("give_up", give_up)
g.add_conditional_edges("model", should_continue, {
    "tools": "tools", "end": END, "give_up": "give_up",
})
g.add_edge("give_up", END)

# start the counter at 0:
# agent.invoke({"messages": [...], "steps": 0})
```

```text
  [route] step 1/5 → tools
  [route] step 2/5 → end        ← normal finish
  …or if it kept looping…
  [route] step 5/5 → give_up    ← graceful stop, no infinite loop
```

Two pieces do the work: the **counter** (`operator.add` reducer, so returning `{"steps": 1}` increments) and the **guard** in the router (checks the cap *first*, routes to a `give_up` node).

> [!warning] Graceful give_up beats routing straight to END
> Route straight to `END` at the cap and the last message is a dangling tool-call with no answer — the caller gets junk. The `give_up` node writes a real closing message, so "you always get an AIMessage back" holds even on the bad path.

> [!tip] Built-in backstop
> `agent.invoke(state, {"recursion_limit": 10})` raises `GraphRecursionError` after N node visits. Use the **explicit counter** for product behavior (a clean "I gave up" / "you've used your 5 tool calls"); use **recursion_limit** as the hard crash-guard against bugs. Best practice: both.

## The through-line
- **Reducers** manage *state over time* (accumulate vs overwrite).
- **Conditional routing** manages *control flow* (which node next).
- **Multi-way routing** = same routing mechanism, more destinations.
- **Step-limit** = a counter (reducer) + a guard (router) so the loop always terminates cleanly.

An agent needs all four: reducers to keep the conversation, routing to loop, and a cap so it stops. This is the production shape of [[raaaaag]]'s agent — `search_docs` can be called repeatedly, but a step cap stops a confused model from burning tokens, and the user still gets a coherent reply.
