---
description: "Multi-agent handoffs (supervisor vs swarm, Command, handoff-as-a-tool) and tool design best practices (naming, docstrings, typed args, string errors, empty-result rule) — with LangGraph code."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/multi-agent
  - topic/tools
  - agents
  - handoffs
  - supervisor
  - tool-design
hubs:
  - "[[Agents]]"
  - "[[Multi-Agent Systems]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Agent Handoffs & Tool Design

> Related: [[Langchain.Multi Agent - Handoffs]] · [[Langchain.Multi Agent - Router]] · [[Agent Tool Schema Best Practices]] · [[Agent Workflow Patterns (The Five)]].

# Part 1 — Handoffs (multi-agent)

**Why:** one agent with 30+ tools degrades — it gets confused about which tool to use, prompts bloat, accuracy drops (the "100-tools problem"). Fix: **split into specialists** that **transfer control**.

> [!definition] Handoff
> One agent passing control (and context) to another, more specialized agent. The receiver takes over with the shared state.

## Two architectures
```text
SUPERVISOR (hub-and-spoke)          SWARM (peer-to-peer)
      supervisor                     billing ⇄ support
      /    |    \                        ⇅
 billing support refunds            each agent hands directly
 (router decides who)               to any other when needed
```
- **Supervisor** — a router picks which specialist runs; specialists return to it. Predictable, easy to debug. **Start here.**
- **Swarm** — agents hand directly to each other. More flexible, loop-prone.

## Supervisor in LangGraph
```python
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]
    next: str
    handoffs: Annotated[int, operator.add]      # loop guard

MAX_HANDOFFS = 4

def supervisor(state: State):
    decision = router_llm.invoke(
        f"Route to billing/support/refunds/DONE:\n{state['messages'][-1].content}"
    ).content.strip()
    return {"next": decision, "handoffs": 1}

def route(state: State) -> str:
    if state["handoffs"] >= MAX_HANDOFFS:  return "done"   # don't ping-pong forever
    return state["next"].lower() if state["next"] != "DONE" else "done"

def billing(state): return {"messages": [billing_agent.invoke(state)], "next": "supervisor"}
def support(state): return {"messages": [support_agent.invoke(state)], "next": "supervisor"}

g = StateGraph(State)
g.add_node("supervisor", supervisor)
g.add_node("billing", billing); g.add_node("support", support)
g.add_edge(START, "supervisor")
g.add_conditional_edges("supervisor", route,
    {"billing": "billing", "support": "support", "done": END})
g.add_edge("billing", "supervisor")     # specialists report back
g.add_edge("support", "supervisor")
```

## Peer handoff via `Command`
A specialist hands directly to another and updates state in one move:
```python
from langgraph.types import Command

def billing_agent(state) -> Command:
    if needs_refund(state):
        return Command(
            goto="refunds",                                     # jump to another agent
            update={"messages": [AIMessage("Handing to refunds.")]},  # pass context
        )
    return Command(goto=END, update={"messages": [answer]})
```

## Handoff-as-a-tool (common LangChain idiom)
```python
from langchain_core.tools import tool

@tool
def transfer_to_refunds(reason: str) -> str:
    """Transfer the conversation to the refunds specialist when the user wants money back."""
    return f"HANDOFF:refunds:{reason}"      # a router turns this into a goto
```

## Handoff best practices
- **Few tools per agent (~5–10).** The whole point of splitting — don't recreate the 100-tool mess inside a specialist.
- **Pass context on handoff** — the receiver needs *why* it was called; put a reason in the update.
- **Cap handoffs** (`MAX_HANDOFFS` + guard) — two agents can bounce forever. Same step-limit pattern.
- **Shared state, one schema** — all agents read/write the same state; reducers make concurrent writes safe.
- **Prefer supervisor over swarm** until you truly need peer-to-peer — far easier to debug.
- **Clear agent descriptions** — the supervisor routes on them; vague = misroutes.

---

# Part 2 — Tool design

The model picks and calls tools by **reading their name, description, and arg schema**. A tool is a prompt as much as a function — bad wording = misuse.

## A well-designed tool
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class SearchArgs(BaseModel):
    query: str = Field(description="The user's question, in natural language")
    top_k: int = Field(5, ge=1, le=20, description="How many results to return")

@tool(args_schema=SearchArgs)
def search_docs(query: str, top_k: int = 5) -> str:
    """Search the knowledge base for passages relevant to a question.

    Use this when the user asks something that needs facts from the docs.
    Do NOT use it for chit-chat or math.
    Returns the top passages as a numbered, citable string.
    """
    try:
        hits = retriever.search(query, k=top_k)
        if not hits:
            return "No relevant passages found. Tell the user you don't know."
        return "\n".join(f"[{i+1}] {h.text}" for i, h in enumerate(hits))
    except Exception as e:
        return f"Search failed: {e}. Ask the user to rephrase."   # error as a STRING
```

## Best practices
| Practice | Why |
|---|---|
| **Descriptive name** (`search_docs`, not `run`/`tool1`) | the model routes on the name |
| **Docstring says *when* to use + when NOT** | stops misuse ("do NOT use for math") |
| **Typed args + `Field(description=...)`** | the model fills args correctly; validation rejects junk |
| **Constrain args** (`ge=1, le=20`) | can't ask for 10,000 results |
| **One job per tool** | a "do everything" tool confuses the model |
| **Return errors as strings, don't raise** | a raised exception kills the run; a string lets the model recover |
| **Token-lean, useful output** | dumping 50KB of JSON blows the context; return what's needed, citable |
| **Deterministic + idempotent where possible** | safe to retry (ties to idempotency work) |

> [!warning] The empty-result rule
> Return a **clear message**, not `""`/`None`/`[]`. `"No passages found. Tell the user you don't know."` teaches the model what to do; an empty return leaves it guessing → it hallucinates. This is raaaaag's refusal guardrail, applied at the tool boundary.

## When you have many tools
Don't give one agent 40 tools — **route or hand off**. Group tools by domain, give each specialist its handful. Tool sprawl is *why* you split into multi-agent (back to Part 1).

### Grouping tools by domain — in code
**1. Define tools in domain buckets** — a dict of domain → its tools *is* the grouping:
```python
from langchain_core.tools import tool

@tool
def create_draft(text: str) -> str:
    """Create a draft post from caption text."""; ...
@tool
def schedule_post(draft_id: str, when: str) -> str:
    """Schedule an approved draft for a given time."""; ...
@tool
def get_post_insights(post_id: str) -> str:
    """Fetch reach/engagement for a published post."""; ...

TOOL_GROUPS = {
    "publishing": [create_draft, schedule_post],
    "analytics":  [get_post_insights, top_posts],
    "ads":        [create_campaign, set_budget],
}
```

**2. Each specialist gets only its group** (`bind_tools` with one bucket — it can't see the others):
```python
def make_specialist(domain: str):
    llm_with_tools = llm.bind_tools(TOOL_GROUPS[domain])   # ONLY this domain's tools
    def node(state):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    return node

publishing_agent = make_specialist("publishing")   # sees 2 tools, not 6
analytics_agent  = make_specialist("analytics")
```

**3. Supervisor routes to the domain** (a small, reliable decision — a name, not a tool):
```python
def route(state) -> str:
    d = router_llm.invoke(
        f"Which domain handles this? {list(TOOL_GROUPS)} or DONE:\n"
        f"{state['messages'][-1].content}").content.strip().lower()
    return d if d in TOOL_GROUPS else "done"

g.add_conditional_edges("supervisor", route, {
    "publishing": "publishing_agent",
    "analytics":  "analytics_agent",
    "ads":        "ads_agent",
    "done":       END,
})
```
```text
                 ┌ publishing_agent → [create_draft, schedule_post]
supervisor ─route─┼ analytics_agent  → [get_post_insights, top_posts]
(picks domain)   └ ads_agent        → [create_campaign, set_budget]
```

**File-structure version** (cleaner as it grows) — one module per domain exporting its `TOOLS`:
```python
# tools/publishing.py →  TOOLS = [create_draft, schedule_post]
# tools/analytics.py  →  TOOLS = [get_post_insights, top_posts]

# registry.py
from tools import publishing, analytics, ads
TOOL_GROUPS = {"publishing": publishing.TOOLS,
               "analytics":  analytics.TOOLS,
               "ads":        ads.TOOLS}
```

> [!tip] Two ways to use the grouping
> **Single agent, dynamic subset** (not full multi-agent yet): classify the request, then `llm.bind_tools(TOOL_GROUPS[domain])` for *that one call* — model sees few tools, no separate agent nodes.
> **Multi-agent**: a specialist node per group (above). Use once domains need their own prompts/memory.

> [!tip] The unifying idea
> **Tool descriptions and agent descriptions are prompts the model reads to make decisions.** The quality of your names, docstrings, and arg schemas *is* the routing quality. Write them for the model like instructions for a new hire: what it does, when to use it, when not to, what it returns.

## Shutterabia + raaaaag fits
- **Shutterabia MCP server = a tool catalog.** Each MCP tool's name + description is what a client model reads to decide when to publish/schedule/analyze. Same rules: one job per tool, tight schemas, string errors. As the catalog grows, group by surface (Ads / Analytics / Publishing) rather than one flat list — the multi-agent split.
- **raaaaag `search_docs`** already follows the empty-result rule (refusal on no context), and the eval harness gates on refusal rate — testing the tool's contract.
