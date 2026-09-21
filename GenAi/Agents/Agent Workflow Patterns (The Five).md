---
description: "The five agent-workflow patterns from Anthropic's Building Effective Agents — chaining, parallelization, routing, orchestrator-workers, evaluator-optimizer — with LangGraph code and when to use each."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/langgraph
  - topic/workflows
  - agents
  - workflows
  - prompt-chaining
  - parallelization
  - routing
  - orchestrator-workers
  - evaluator-optimizer
aliases:
  - "workflow patterns"
  - "prompt chaining"
  - "parallelization"
  - "orchestrator workers"
  - "evaluator optimizer"
hubs:
  - "[[Agents]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21; Anthropic 'Building Effective Agents'"
---
# Agent Workflow Patterns (the five)

> Related: [[AI Workflows VS AI Agent]], [[LangGraph Reducers, Routing And Step-Limit Loops]].

**Workflow vs agent:** a **workflow** runs a *fixed, wired path*; an **agent** *decides its own path* at runtime. These five are workflows — predictable, cheaper, faster. Reach for a workflow whenever the path is known; save the agent loop for when the model genuinely must choose its own steps.

## 1. Prompt chaining — ordered steps
Break a task into a **fixed sequence** of LLM calls, each output feeding the next. Optionally a **gate** between steps catches a bad result early.

```text
input → [LLM step 1] → [LLM step 2] → [LLM step 3] → output
                 │
            (optional gate: check step 1 before continuing)
```

**When:** the task is genuinely sequential and each step is easier alone (outline → draft → polish; extract → transform → format).

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    topic: str; outline: str; draft: str; final: str

def make_outline(s): return {"outline": llm.invoke(f"Outline: {s['topic']}").content}
def write_draft(s):  return {"draft":  llm.invoke(f"Draft from:\n{s['outline']}").content}
def polish(s):       return {"final":  llm.invoke(f"Tighten:\n{s['draft']}").content}

g = StateGraph(State)
g.add_node("outline", make_outline); g.add_node("draft", write_draft); g.add_node("polish", polish)
g.add_edge(START, "outline")
g.add_edge("outline", "draft")     # plain edges = fixed order
g.add_edge("draft", "polish")
g.add_edge("polish", END)
chain = g.compile()
```

Gate variant — stop early on a failed check:
```python
def gate(s) -> str:
    return "draft" if len(s["outline"]) > 50 else "fail"
g.add_conditional_edges("outline", gate, {"draft": "draft", "fail": END})
```

> [!tip] Trade-off
> More accurate + inspectable (gate between steps), but **slower** (sequential). Worth it when accuracy beats speed.

## 2. Parallelization — steps at the same time
Fire multiple LLM calls concurrently. Two flavors.

**Sectioning** — split into **independent** subtasks, run together, combine:
```text
              ┌─ [subtask 1] ─┐
input → split ┼─ [subtask 2] ─┼→ aggregate → output
              └─ [subtask 3] ─┘
```
**Voting** — run the **same** task N times, aggregate (majority / best):
```text
              ┌─ [attempt 1] ─┐
input → fanout┼─ [attempt 2] ─┼→ vote/pick → output
              └─ [attempt 3] ─┘
```

**When:** sectioning = parts don't depend on each other (review a post for tone + facts + brand at once). Voting = one shot is unreliable (safety check run 3×, block on any fail).

```python
from typing import Annotated
import operator

class State(TypedDict):
    text: str
    reviews: Annotated[list, operator.add]   # reducer collects parallel results

def check_tone(s):  return {"reviews": [f"tone: {llm.invoke(...).content}"]}
def check_facts(s): return {"reviews": [f"facts: {llm.invoke(...).content}"]}
def check_brand(s): return {"reviews": [f"brand: {llm.invoke(...).content}"]}
def aggregate(s):   return {"summary": combine(s["reviews"])}

for n, fn in [("tone",check_tone),("facts",check_facts),("brand",check_brand)]:
    g.add_node(n, fn)
g.add_node("aggregate", aggregate)
g.add_edge(START, "tone"); g.add_edge(START, "facts"); g.add_edge(START, "brand")  # parallel
g.add_edge("tone", "aggregate"); g.add_edge("facts", "aggregate"); g.add_edge("brand", "aggregate")
g.add_edge("aggregate", END)
```

> [!warning] The reducer makes parallel safe
> Three nodes write `reviews` at once — without the `operator.add` reducer they'd **overwrite each other**. LangGraph also waits for **all** parallel branches before running `aggregate` (fan-in).

## 3. Routing — classify, then specialize
Classify the input, send it to a **specialized handler**. A cheap classifier up front lets each branch stay simple.

```text
                 ┌─ "refund"    → refund_prompt
input → classify ─┼─ "technical" → tech_prompt
                 └─ "general"   → general_prompt → output
```

**When:** distinct input categories each deserve different handling (prompt / model / tools).

```python
class State(TypedDict):
    query: str; kind: str; answer: str

def classify(s): return {"kind": llm.invoke(f"refund/technical/general: {s['query']}").content.strip()}
def route(s) -> str: return s["kind"] if s["kind"] in ("refund","technical","general") else "general"
def refund(s):    return {"answer": refund_llm.invoke(s["query"]).content}
def technical(s): return {"answer": tech_llm.invoke(s["query"]).content}
def general(s):   return {"answer": small_cheap_llm.invoke(s["query"]).content}

g.add_node("classify", classify)
for n, fn in [("refund",refund),("technical",technical),("general",general)]: g.add_node(n, fn)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route, {"refund":"refund","technical":"technical","general":"general"})
for n in ("refund","technical","general"): g.add_edge(n, END)
```

> [!tip] Cost + quality together
> Route easy queries to a small cheap model, hard ones to a big model — save money **and** keep each branch's prompt focused.

## 4. Orchestrator–workers — LLM plans subtasks, then synthesize
A lead LLM **decides the subtasks at runtime**, workers handle each, a synthesizer merges. Unlike sectioning, the subtasks **aren't known ahead of time**.

```text
                    ┌─ worker → result ─┐
input → orchestrator ┼─ worker → result ─┼→ synthesize → output
   (plans subtasks)  └─ worker → result ─┘
```

**When:** the number/shape of subtasks depends on the input (research question → N sub-questions; a code change touching an unknown set of files).

```python
class State(TypedDict):
    task: str; subtasks: list
    results: Annotated[list, operator.add]
    final: str

def orchestrate(s):
    plan = llm.invoke(f"Break into 2-5 subtasks (one per line): {s['task']}").content
    return {"subtasks": [l for l in plan.splitlines() if l.strip()]}

def workers(s):
    return {"results": [llm.invoke(f"Do: {st}").content for st in s["subtasks"]]}

def synthesize(s):
    return {"final": llm.invoke("Combine:\n" + "\n".join(s["results"])).content}

g.add_edge(START, "orchestrate"); g.add_edge("orchestrate", "workers")
g.add_edge("workers", "synthesize"); g.add_edge("synthesize", END)
```
*(For true parallel workers, LangGraph's `Send` API fans out one node per subtask dynamically.)*

> [!warning] vs parallel sectioning
> **Sectioning** = *you* fixed the subtasks in code. **Orchestrator-workers** = *the LLM* decides them at runtime. More powerful, but more expensive and less predictable — use only when the split can't be hard-coded.

## 5. Evaluator–optimizer — generate, critique, retry
One LLM **generates**, another **evaluates** against criteria; on fail, feedback loops back for another attempt (capped).

```text
input → [generate] → [evaluate] ──pass──▶ output
              ▲            │
              └──fail:─────┘  (feedback → retry, up to N times)
```

**When:** clear quality criteria + iteration measurably helps (translation with a tone bar, code that must pass tests, brand-voice copy).

```python
class State(TypedDict):
    task: str; draft: str; feedback: str
    attempts: Annotated[int, operator.add]
    done: bool

MAX = 3

def generate(s):
    prompt = s["task"] if not s.get("feedback") else \
             f"{s['task']}\nFix: {s['feedback']}\nPrevious: {s['draft']}"
    return {"draft": llm.invoke(prompt).content, "attempts": 1}

def evaluate(s):
    v = llm.invoke(f"Reply PASS or feedback:\n{s['draft']}").content
    return {"done": v.strip() == "PASS", "feedback": v}

def gate(s) -> str:
    if s["done"] or s["attempts"] >= MAX: return "accept"   # step-limit guard
    return "retry"

g.add_edge(START, "generate"); g.add_edge("generate", "evaluate")
g.add_conditional_edges("evaluate", gate, {"retry": "generate", "accept": END})
```

> [!tip] Reuses everything
> Evaluator-optimizer = a **loop** (conditional edge back) + a **step limit** (attempts counter + guard) + a **reducer** (accumulate attempts) — the agent-loop machinery applied to self-critique instead of tool-calling. See [[LangGraph Reducers, Routing And Step-Limit Loops]].

## All five + how to choose
| Pattern | Shape | Use when |
|---|---|---|
| Chaining | steps in order | task splits into sequential steps |
| Parallelization | steps at once | independent subtasks, or voting |
| Routing | classify → branch | distinct input categories |
| Orchestrator–workers | LLM plans subtasks → merge | subtasks unknown until runtime |
| Evaluator–optimizer | generate → critique → retry | clear quality bar + iteration helps |

> [!tip] The golden rule (Anthropic's "Building Effective Agents")
> **Start with the simplest thing that works.** A single LLM call beats a workflow; a workflow (fixed path) beats an agent (dynamic path) when the path is known. Add complexity only when a simpler pattern demonstrably falls short — every step up costs latency, tokens, and unpredictability.
>
> The ladder: **one call → chain → route/parallelize → orchestrator-workers / evaluator-optimizer → full agent.** Climb only as far as the task forces you.

## Shutterabia fits
- **Chain:** publish flow — draft caption → brand-check gate → schedule.
- **Sectioning:** the 3-way content review (tone / facts / brand at once).
- **Voting:** a safety gate — run the check a few times, block on any fail.
- **Routing:** triage an incoming message → publish / analytics / support.
- **Evaluator–optimizer:** caption generation held to the brand-voice bar.
