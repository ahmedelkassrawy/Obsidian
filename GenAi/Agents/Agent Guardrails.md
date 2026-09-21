---
description: "Guardrails for LLM/agent apps — input vs output, the categories, rule/LLM-judge/library levels, placement in a LangGraph agent, block/regenerate/rewrite, parallel checks, and fail-open vs fail-closed. Includes a runnable guardrail'd agent."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/guardrails
  - topic/safety
  - agents
  - guardrails
  - pii
  - moderation
  - grounding
hubs:
  - "[[Agents]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Agent Guardrails

> Related: [[Agent Workflow Patterns (The Five)]] (regenerate = evaluator-optimizer) · [[LangSmith]] (score blocked runs) · [[LangGraph Reducers, Routing And Step-Limit Loops]] (the retry cap).

Guardrails = checks **around** the LLM that stop bad input getting in and bad output getting out. The model is unpredictable; guardrails are the deterministic-ish fence around it.

## The two positions
```text
user input → [INPUT guardrails] → LLM/agent → [OUTPUT guardrails] → user
                  │                                   │
             block/sanitize                     block / rewrite / regenerate
             before it reaches the model         before it reaches the user
```

> [!definition] Guardrail
> A check on LLM input or output enforcing a rule the model can't be trusted to follow. **Input** guards protect the model (and your bill) from bad/malicious requests; **output** guards protect the user and brand from bad responses.

## What they check
| Guardrail | Catches | Side |
|---|---|---|
| Safety / moderation | hate, violence, self-harm, sexual | in + out |
| PII | emails, cards, SSNs in or out | in + out |
| Jailbreak / injection | "ignore your instructions…" | input |
| Topic / scope | off-topic requests | input |
| Hallucination / grounding | answer not supported by retrieved docs | output |
| Format | must be valid JSON / schema | output |
| Brand / tone | off-voice, competitor mentions, banned claims | output |

## Three levels of implementation
**1. Rule-based (cheap, deterministic — do first):**
```python
import re
def pii_check(text: str) -> bool:
    if re.search(r"\b\d{16}\b", text):     return False   # card number
    if re.search(r"[\w.]+@[\w.]+", text):  return False   # email
    return True
```

**2. LLM-as-judge (fuzzy rules rules can't catch):**
```python
def on_topic(text: str) -> bool:
    v = judge_llm.invoke(f"Is this about social publishing? YES/NO:\n{text}").content
    return v.strip().upper() == "YES"
```

**3. Dedicated libraries** — `Guardrails AI` (validators + auto-refix), `NeMo Guardrails` (rules DSL), provider moderation endpoints. Reach for these with many rules; hand-rolled is fine to start.

## Output guardrails have three responses
```text
BLOCK      → replace with a safe canned message ("I can't help with that")
REGENERATE → send back to the model with the failure as feedback (retry, capped)
REWRITE    → cheap fix (redact PII, strip banned phrase) and pass it
```
Regenerate = the **evaluator-optimizer** pattern used as a guardrail; the step-limit guard applies (don't regenerate forever).

## Run checks in parallel for speed
Guardrails add hot-path latency. Run several concurrently (sectioning) so cost = one check's time, not the sum:
```text
              ┌─ safety check ─┐
output → fan  ┼─ pii check   ─┼→ any fail? → block / fix
              └─ grounding    ─┘   (else pass)
```

## Fail-open vs fail-closed
> [!warning] Decide what happens when the guardrail itself errors
> **Fail-closed** — check crashes/times out → **block** (safe default for moderation, PII, anything harmful). **Fail-open** — non-critical check fails → **let it through** (a brand-tone check shouldn't take down the API). Match it to the cost of being wrong — same call as the Shutterabia rate limiter.

## Runnable guardrail'd agent (input PII block + output grounding + regenerate)
```python
# guarded_agent.py
import os, re, operator
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="openai/gpt-4o-mini",
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.environ["OPENROUTER_API_KEY"])

MAX_REGEN = 2

class State(TypedDict):
    messages: Annotated[list, operator.add]
    context: str          # the retrieved docs the answer must stick to
    answer: str
    blocked: bool
    regens: Annotated[int, operator.add]

# --- INPUT guardrail: block PII / injection before the model sees it ---
def input_guard(state: State):
    txt = state["messages"][-1].content
    pii = re.search(r"\b\d{16}\b", txt) or re.search(r"[\w.]+@[\w.]+", txt)
    inject = "ignore your instructions" in txt.lower()
    blocked = bool(pii or inject)
    print(f"  [in-guard] blocked={blocked}")
    return {"blocked": blocked}

def route_in(state: State) -> str:
    return "refuse" if state["blocked"] else "generate"

# --- the model ---
def generate(state: State):
    q = state["messages"][-1].content
    ans = llm.invoke(f"Answer ONLY from this context:\n{state['context']}\n\nQ: {q}").content
    print(f"  [model] regen #{state['regens']}")
    return {"answer": ans, "regens": 1}

# --- OUTPUT guardrail: is the answer grounded in the context? ---
def output_guard(state: State) -> str:
    v = llm.invoke(
        f"Is this answer fully supported by the context? PASS/FAIL.\n"
        f"Context:\n{state['context']}\nAnswer:\n{state['answer']}").content
    grounded = v.strip().upper().startswith("PASS")
    print(f"  [out-guard] grounded={grounded}")
    if grounded:                       return "ok"
    if state["regens"] >= MAX_REGEN:   return "give_up"   # step-limit
    return "regenerate"

def refuse(state: State):
    return {"messages": [AIMessage("I can't help with that request.")]}

def give_up(state: State):
    return {"messages": [AIMessage("I don't have enough grounded information to answer.")]}

def deliver(state: State):
    return {"messages": [AIMessage(state["answer"])]}

g = StateGraph(State)
g.add_node("input_guard", input_guard)
g.add_node("generate", generate)
g.add_node("refuse", refuse)
g.add_node("give_up", give_up)
g.add_node("deliver", deliver)

g.add_edge(START, "input_guard")
g.add_conditional_edges("input_guard", route_in, {"generate": "generate", "refuse": "refuse"})
g.add_conditional_edges("generate", output_guard,
    {"ok": "deliver", "regenerate": "generate", "give_up": "give_up"})
g.add_edge("deliver", END); g.add_edge("refuse", END); g.add_edge("give_up", END)
agent = g.compile()

if __name__ == "__main__":
    out = agent.invoke({
        "messages": [HumanMessage("What does RRF do?")],
        "context": "RRF (reciprocal rank fusion) merges ranked lists into one.",
        "regens": 0,
    })
    print("\nFINAL:", out["messages"][-1].content)
```

Trace shapes you'll see:
```text
happy:   [in-guard] blocked=False → [model] regen #0 → [out-guard] grounded=True → deliver
blocked: [in-guard] blocked=True  → refuse            ("I can't help with that.")
ungrounded: [model] #0 → grounded=False → [model] #1 → grounded=False → give_up
```

> [!tip] The through-line
> **Defense in depth**: cheap rules first (regex, schema), LLM-judge for fuzzy stuff, moderation API for safety. **Input** guards protect the model; **output** guards protect the user. Non-negotiable checks fail **closed**; nice-to-haves fail **open**. Regenerate is bounded by a step limit.

## Shutterabia + raaaaag fits
- **raaaaag already has one:** the **refusal** ("no relevant context → don't answer") is an output grounding guardrail, and the eval harness **gates on refusal rate** — that's testing the guardrail.
- **Shutterabia:** *input* = PII + injection on incoming messages; *output* = brand-voice + banned-claims + no-competitor before a caption publishes. A publish is **irreversible**, so that output guard fails **closed**.
