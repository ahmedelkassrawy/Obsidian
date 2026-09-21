---
description: "How agents think — CoT, ReAct, Reflection/Reflexion, Plan-and-Execute, Tree-of-Thoughts/self-consistency. When to use each, how they map to workflow patterns, and a runnable LangGraph reflection agent."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/reasoning
  - topic/langgraph
  - agents
  - react
  - reflection
  - plan-and-execute
  - tree-of-thoughts
hubs:
  - "[[Agents]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Agent Reasoning Patterns

> Related: [[Agent Agency Levels And Reflection Pattern]] · [[Agent Workflow Patterns (The Five)]] (three of these ARE workflow patterns).

How an agent **thinks** before/while acting. Most map onto workflow patterns you already know.

## 1. Chain-of-Thought (CoT) — think before answering
Make the model reason step by step instead of blurting an answer. Improves multi-step accuracy (math, logic). A prompting move, not an architecture; modern reasoning models do it internally.
```text
"...Let's think step by step." → reasoning → answer
```

## 2. ReAct (Reason + Act) — the default agent loop
Interleave **Thought → Action (tool) → Observation**, repeat. This is the agent loop you built.
```text
Thought: I need the doc count.
Action: search_docs("...")          ← tool call
Observation: "...6 words..."         ← result
Thought: I have it.  Answer: 6
```
```python
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(llm, tools=[search_docs])   # ReAct, batteries-included
```
- **When:** default for tool-using agents; reactive. **Cost:** many calls, can wander (needs a step-limit guard).

## 3. Reflection / Reflexion — critique your own output
Generate → **model critiques its own answer** → revise. Self-improvement loop.
```text
draft → self-critique → revise → (repeat, capped)
```
- **Is the evaluator-optimizer workflow** applied to reasoning. **When:** clear quality bar + iteration helps. **Cost:** 2–3×.
- **Reflexion** = reflection that *remembers* past mistakes across attempts (writes critiques to memory → the Write move from context engineering).

## 4. Plan-and-Execute — plan all steps first, then do them
Make the whole plan upfront, then execute — vs ReAct's one-step-at-a-time.
```text
PLAN (once, big model):  1. search X  2. search Y  3. compare  4. summarize
EXECUTE (per step, cheap model): run 1 → 2 → 3 → 4   (re-plan only on failure/new info)
```
- **When:** complex multi-step where wandering is costly. **Wins:** fewer big-model calls, less drift, cheaper (plan with GPT-4, execute with mini). **Cost:** a rigid plan breaks if reality changes → add re-planning. Cousin of orchestrator-workers.

## 5. Tree-of-Thoughts / self-consistency — explore several paths
Generate multiple reasoning paths, then **vote or pick the best**.
```text
          ┌─ path A → answer A ─┐
question ─┼─ path B → answer B ─┼→ vote / pick → final
          └─ path C → answer C ─┘
```
- **Self-consistency** = run the same CoT N times (temp>0), take the majority. **Is the parallelization/voting workflow** applied to reasoning. **When:** hard problems, accuracy worth N×. **Cost:** N× — sparingly.

## How to choose
| Pattern | Use when | Cost |
|---|---|---|
| CoT | any multi-step reasoning | ~free (one call) |
| ReAct | tool-using agent, reactive | many calls, can wander |
| Reflection | clear quality bar, iteration helps | 2–3× |
| Plan-and-Execute | complex, multi-step, wandering costly | cheaper than ReAct on big tasks |
| ToT / self-consistency | hard problems, accuracy worth N× | N× |

> [!tip] The through-line
> Three of these **are workflow patterns**: reflection = evaluator-optimizer, ToT/self-consistency = parallelization-voting, plan-and-execute ≈ orchestrator-workers with an explicit plan. ReAct = base agent loop; CoT = base prompting move. Pick by **task shape + budget**.

## Runnable reflection agent (LangGraph)
Generate → critique → revise, looped with a cap (the step-limit guard).
```bash
pip install langgraph langchain-openai
```
```python
# reflection_agent.py
import os, operator
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="openai/gpt-4o-mini",
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.environ["OPENROUTER_API_KEY"])

MAX_ROUNDS = 3

class State(TypedDict):
    task: str
    draft: str
    critique: str
    rounds: Annotated[int, operator.add]

def generate(state: State):
    if not state.get("draft"):
        draft = llm.invoke(f"Write a short answer to: {state['task']}").content
    else:  # revise using the last critique
        draft = llm.invoke(
            f"Task: {state['task']}\nYour draft:\n{state['draft']}\n"
            f"Critique to fix:\n{state['critique']}\nRewrite it better:").content
    print(f"  [generate] round {state.get('rounds', 0)}")
    return {"draft": draft, "rounds": 1}

def reflect(state: State):
    critique = llm.invoke(
        f"Critique this answer against the task. If it's already good, reply exactly PASS.\n"
        f"Task: {state['task']}\nAnswer:\n{state['draft']}").content
    print(f"  [reflect] {critique[:60]}...")
    return {"critique": critique}

def gate(state: State) -> str:
    if state["critique"].strip().upper().startswith("PASS"):
        return "done"
    if state["rounds"] >= MAX_ROUNDS:      # step-limit guard
        return "done"
    return "revise"

g = StateGraph(State)

g.add_node("generate", generate)
g.add_node("reflect", reflect)

g.add_edge(START, "generate")
g.add_edge("generate", "reflect")
g.add_conditional_edges("reflect", gate, {"revise": "generate", "done": END})

agent = g.compile()

if __name__ == "__main__":
    out = agent.invoke({"task": "Explain what a KV cache does, in 2 sentences.", "rounds": 0})
    print("\nFINAL:\n", out["draft"])
```
```text
[generate] round 0 → [reflect] "too vague, mention memory..." → revise
[generate] round 1 → [reflect] "PASS" → done
FINAL: <the improved answer>
```
This is the evaluator-optimizer loop: **generate → reflect (critique) → revise**, gated by PASS or the round cap. Swap the critique prompt for a concrete rubric to make reflection actually bite.

## Best practices
- **Start with ReAct or plain CoT** — don't reach for ToT/reflection until a simpler pattern fails ("climb the ladder", same as workflows).
- **Cap every loop** — ReAct and reflection both need the step-limit guard.
- **Match model to role** — big model plans/reflects, cheap model executes (gateway tier routing).
- **Reflection needs a real critic** — vague "is this good?" adds nothing; give concrete criteria, like a guardrail rubric.

## Fits
- raaaaag's agent is **ReAct** (model ↔ `search_docs`).
- Adding a **reflection** pass ("is this grounded? if not, retry") = the evaluator-optimizer/guardrail already sketched.
- A complex Shutterabia task (plan a week of posts) suits **plan-and-execute** (plan once, execute per-post cheaply).

---

## Classic agent architectures (reactive / deliberative / hybrid)

The patterns above are about *how the agent reasons*. There's an older, coarser taxonomy about *how the agent is wired* — merged in from the old `Agent Patterns` note.

### Reactive agents
Direct mapping from state → action. No internal memory or world model; they respond to the current input immediately.
- **Example:** a thermostat — if temp < 20°C, turn on the heater.
- **When:** low-latency tasks, predictable environment, where history doesn't change the immediate decision.

### Deliberative agents
Hold an internal model of the world and **plan** toward goals — they think through consequences before acting.
- **Example:** a chess AI simulating thousands of future board states to pick the winning move.
- **When:** complex, goal-oriented, multi-step tasks where the best move isn't obvious from the current state.

### Hybrid agents
Combine reactive speed with deliberative foresight — usually layered: a fast layer for emergencies, a slow layer for planning.
- **Example:** a self-driving car — reactive layer slams the brakes for a pedestrian, deliberative layer plans the route NY → DC.
- **When:** real-world robotics/autonomy that must balance immediate safety with planned efficiency.

### Summary table (all six)
| Pattern | Primary strength | Weakness |
|---|---|---|
| **Reactive** | Speed / simplicity | No long-term memory |
| **Deliberative** | Goal-oriented | High compute / slow |
| **ReAct** | Tool use / fact-checking | Can get stuck in infinite loops |
| **Plan-Execute** | Efficiency in long tasks | Brittle if the plan fails midway |
| **Tree of Thoughts** | Deep problem solving | Very high token cost |
