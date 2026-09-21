---
description: "Human-in-the-loop for agents — pause on a consequential boundary via interrupt(), get a human decision, resume with Command(resume=...). The four patterns, best practices, and a runnable approve/reject demo."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/langgraph
  - topic/human-in-the-loop
  - agents
  - hitl
  - interrupt
  - approval
hubs:
  - "[[Agents]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Human-in-the-Loop (Approval & Interrupts)

> Builds on [[LangGraph Human In The Loop And Checkpointers]] (the checkpointer plumbing) and [[LangGraph Short-Term & Long-Term Memory]] (pause = snapshot). Related: [[Agent Guardrails]] (HITL = the human version of a guardrail).

HITL = **pause the agent, get a human decision, resume from exactly where it stopped**. It runs on the checkpointer — the pause *is* a saved snapshot.

## When you need it
```text
agent about to do something → is it safe to do unattended?
  irreversible (publish, send money, delete) → PAUSE, ask a human
  high-stakes / low-confidence / compliance   → PAUSE, ask a human
  cheap + reversible                          → just do it
```

> [!definition] Human-in-the-loop (HITL)
> The agent **interrupts** before a consequential step, surfaces the decision to a person, and **resumes** with their answer. Built on the checkpointer: `interrupt` saves the full state as a snapshot and returns control; resuming reloads that snapshot and continues.

## The four patterns
| Pattern | The human… | Example |
|---|---|---|
| Approve / reject | says yes/no before an action | publish this post? |
| Edit state | fixes the plan/draft | tweak the caption before it goes |
| Review a tool call | approves/edits args before the tool runs | check the SQL before it deletes |
| Ask for input | supplies missing info | which account? what budget? |

## How it works — `interrupt` + resume
Requires a checkpointer (no snapshot = nowhere to pause).
```python
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

def publish_node(state):
    decision = interrupt({"action": "publish", "draft": state["draft"]})  # ← PAUSE
    if decision == "approve":
        return {"messages": [AIMessage(f"Published: {publish_to_meta(state['draft'])}")]}
    return {"messages": [AIMessage("Publish cancelled.")]}

agent = g.compile(checkpointer=MemorySaver())      # HITL needs this
cfg = {"configurable": {"thread_id": "post-42"}}

out = agent.invoke({"draft": "New post..."}, cfg)  # runs until the interrupt
print(out["__interrupt__"])                        # {"action": "publish", ...} (waiting)
agent.invoke(Command(resume="approve"), cfg)       # resume with the human's answer
```
```text
run → publish_node hits interrupt → snapshot saved, control returns (nothing published)
   human decides → Command(resume="approve") → reload snapshot → publish → done
```

**Review-and-edit variant** — the human changes the value before resuming:
```python
def draft_node(state):
    edited = interrupt({"draft": state["draft"]})   # human may edit the caption
    return {"draft": edited}
# resume: agent.invoke(Command(resume="the corrected caption"), cfg)
```

## Runnable demo (no API key needed)
```bash
pip install langgraph
```
```python
# hitl_demo.py — watch the agent pause for approval and resume
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

class State(TypedDict):
    draft: str
    log: Annotated[list, operator.add]

def write_draft(state: State):
    return {"draft": f"[caption] {state['draft']}", "log": ["drafted"]}

def approve_and_publish(state: State):
    # PAUSE: surface the draft, wait for a human decision
    decision = interrupt({"question": "Publish this?", "draft": state["draft"]})
    if decision == "approve":
        print(f"  >> PUBLISHED: {state['draft']}")     # the irreversible action
        return {"log": ["published"]}
    if decision == "reject":
        print("  >> cancelled")
        return {"log": ["cancelled"]}
    # treat anything else as an edited caption, then publish it
    print(f"  >> PUBLISHED (edited): {decision}")
    return {"draft": decision, "log": ["published-edited"]}

g = StateGraph(State)
g.add_node("write_draft", write_draft)
g.add_node("approve_and_publish", approve_and_publish)
g.add_edge(START, "write_draft")
g.add_edge("write_draft", "approve_and_publish")
g.add_edge("approve_and_publish", END)
agent = g.compile(checkpointer=MemorySaver())     # required for interrupt/resume

if __name__ == "__main__":
    cfg = {"configurable": {"thread_id": "post-1"}}

    # 1. run until it pauses
    out = agent.invoke({"draft": "Launch day!", "log": []}, cfg)
    print("PAUSED, waiting on human:", out["__interrupt__"][0].value)

    # 2. a human answers — try "approve" / "reject" / an edited string
    final = agent.invoke(Command(resume="approve"), cfg)
    print("LOG:", final["log"])       # ['drafted', 'published']
```
Run it and you'll see it **stop** after drafting, print the pending question, then only publish after you resume with `"approve"`. Swap `resume="reject"` or `resume="Better caption!"` to see the other paths.

## Best practices
- **Interrupt *before* the irreversible step** — pause on the boundary (publish/delete/pay); let reversible work run free.
- **Show what they're approving** — pass the full action + args into `interrupt(...)`.
- **Combine with guardrails** — auto-check cheap cases, escalate only the *ambiguous* ones to a human; don't make people rubber-stamp everything.
- **Durable checkpointer in prod** — approvals may come hours later; use `SqliteSaver`/`PostgresSaver`, not `MemorySaver`, so the pause survives a restart.
- **Idempotent resume** — the resumed action runs once (your `chunk_uid`/idempotency habit); a double-resume must not double-publish.
- **Timeout / default** — if no one answers, default safely (auto-reject anything harmful = fail-closed).

> [!tip] The through-line
> HITL = **a deliberate pause on a consequential boundary**, powered by the checkpointer (pause = snapshot) and resumed with `Command(resume=...)`. The human version of a guardrail: instead of a rule blocking bad output, a person approves a risky action. Use it exactly where "wrong and irreversible" is expensive.

## Shutterabia fit
The **stage draft → SMM approves → publish** flow (ADR 0003/0005) *is* HITL: the agent pauses at the irreversible boundary (publishing to Meta), a human approves, then it resumes. A publish fails **closed** — no approval, no post.
