---
description: "Evaluating agents at three levels — outcome, trajectory, single-step — with focus on trajectory (did it take the right steps). Matching modes, agentevals + LangSmith evaluate over a dataset, and a full runnable LangGraph example."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/ai-evaluation
  - topic/langgraph
  - agents
  - evaluation
  - trajectory
  - agentevals
  - langsmith
hubs:
  - "[[Agents]]"
  - "[[AI Evaluation]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Agent Trajectory Evaluation

> Complements [[Agent Evaluation]]. Related: [[LangSmith]] (hosts the eval + scores) · raaaaag eval harness (outcome eval).

Agent eval has **three levels** — the one people skip is trajectory. The raaaaag harness does level 1.

```text
1. FINAL RESPONSE (outcome)  → did it get the right answer?      (hit@k, refusal)
2. TRAJECTORY (the path)     → did it take the right STEPS?
3. SINGLE-STEP (one node)    → given this input, was this node's output right?  (unit test)
```

> [!definition] Trajectory
> The **sequence of steps an agent took** — which tools, with what args, in what order — to reach its answer. Trajectory eval scores the *path*, not just the destination.

**Why outcome-only isn't enough:** an agent can get the right answer via the **wrong path** (8 tools when 2 would do, or luck) — fragile + expensive. And a wrong answer needs the trajectory to show *where* it broke.
```text
Q: "how many words in the doc?"
outcome: "6" ✓        → looks fine
trajectory: web_search (wrong) → guessed → RIGHT answer, BROKEN path (fails next time)
```

## What trajectory eval measures
- **Tool selection** — right tools called? wrong ones avoided?
- **Order** — sensible sequence?
- **Efficiency** — step count; loops/detours?
- **Completion** — finished vs hit the step limit?

## Matching modes (how strict)
| Mode | Passes when | Use when |
|---|---|---|
| strict (exact) | actual == expected, same order | rigid pipelines |
| in-order / subset | expected appears in order (extras ok) | key steps must happen in sequence |
| unordered / any-order | all expected present, order-free | order doesn't matter |
| superset | actual covers expected | "did it at least do these" |

Exact is usually too brittle (agents have many valid paths). **In-order / unordered / superset** are the sweet spot.

## Full runnable example — LangGraph agent + agentevals + LangSmith
```bash
pip install langgraph langchain-openai agentevals langsmith
```
```bash
export OPENROUTER_API_KEY=...        # the model
export LANGSMITH_API_KEY=lsv2_...    # eval host
export LANGSMITH_TRACING=true
```
```python
# eval_agent.py — build a LangGraph agent, then trajectory-eval it on a dataset
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langsmith import Client
from agentevals.trajectory.match import create_trajectory_match_evaluator
from agentevals.trajectory.llm import (
    create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT)

# ---------- 1. a real LangGraph agent ----------
@tool
def search_docs(query: str) -> str:
    """Search the knowledge base for passages relevant to a question."""
    return "RRF (reciprocal rank fusion) merges multiple ranked lists into one."

llm = ChatOpenAI(model="openai/gpt-4o-mini",
                 base_url="https://openrouter.ai/api/v1",
                 api_key=os.environ["OPENROUTER_API_KEY"])
agent = create_react_agent(llm, tools=[search_docs])   # prebuilt ReAct loop

# ---------- 2. target: run the agent, RETURN THE MESSAGES (the trajectory) ----------
def run_agent(inputs: dict) -> dict:
    result = agent.invoke({"messages": [("user", inputs["question"])]})
    return {"messages": result["messages"]}            # full trajectory, not just the answer

# ---------- 3. evaluators (agentevals) ----------
matcher = create_trajectory_match_evaluator(trajectory_match_mode="superset")
judge   = create_trajectory_llm_as_judge(
    prompt=TRAJECTORY_ACCURACY_PROMPT, model="openai:gpt-4o-mini")

def trajectory_match(outputs: dict, reference_outputs: dict) -> dict:
    return matcher(outputs=outputs["messages"],
                   reference_outputs=reference_outputs["messages"])   # deterministic → gate

def trajectory_quality(outputs: dict) -> dict:
    return judge(outputs=outputs["messages"])                         # LLM-judge → report-only

# ---------- 4. dataset (create once, reuse by name) ----------
client = Client()
DATASET = "agent-traj"
if not client.has_dataset(dataset_name=DATASET):
    ds = client.create_dataset(DATASET)
    client.create_examples(
        dataset_id=ds.id,
        inputs=[{"question": "What does RRF do?"}],
        outputs=[{"messages": [                         # expected trajectory
            {"role": "user", "content": "What does RRF do?"},
            {"role": "assistant", "tool_calls": [
                {"function": {"name": "search_docs", "arguments": '{"query":"RRF"}'}}]},
            {"role": "assistant", "content": "RRF merges ranked lists."},
        ]}],
    )

# ---------- 5. run the eval over the dataset ----------
results = client.evaluate(
    run_agent, data=DATASET,
    evaluators=[trajectory_match, trajectory_quality],
    experiment_prefix="traj-eval",
)

# ---------- 6. gate CI on the deterministic metric (raaaaag philosophy) ----------
scores = [r["evaluation_results"]["results"][0].score for r in results]
pass_rate = sum(bool(s) for s in scores) / len(scores)
print(f"trajectory match pass-rate: {pass_rate:.0%}")
if pass_rate < 0.9:
    raise SystemExit("trajectory gate failed")   # non-zero exit → CI red
```

**What each block does:**
```text
1. create_react_agent → a real agent (model + search_docs tool, ReAct loop)
2. run_agent          → invokes it, returns the MESSAGES (the trajectory IS the messages)
3. matcher + judge    → agentevals: deterministic tool-path match + LLM path-quality
4. dataset            → question + expected trajectory, stored in LangSmith
5. client.evaluate    → runs the agent over every example, scores each, stores results
6. gate               → deterministic pass-rate fails the build; judge stays report-only
```

**Try the matcher standalone (no LangSmith):**
```python
out = run_agent({"question": "What does RRF do?"})
print(trajectory_match(out, {"messages": [
    {"role": "assistant", "tool_calls": [
        {"function": {"name": "search_docs", "arguments": "{}"}}]}]}))
# → {'key': 'trajectory_match', 'score': True}
```

## Best practices
- **Eval outcome AND trajectory** — a right answer with a broken path is luck; a wrong answer needs the trajectory to locate the break.
- **Build the dataset from real traces** (capture in LangSmith, label the good ones) — don't invent cases in a vacuum.
- **Gate deterministic, report flaky** — matcher gates CI (`SystemExit`), LLM-judge stays report-only (noisy). Same rule as the raaaaag eval gate.
- **Prefer in-order/unordered/superset over exact** — agents have many valid paths.
- **Add single-step tests** for critical nodes (router, a tool wrapper) — fast + deterministic.
- **Track efficiency** — step count + cost per task, not just correctness.

> [!tip] The two things that make it work
> **create_react_agent** gives the standard agent for free (you hand-built this loop in [[LangGraph Reducers, Routing And Step-Limit Loops]]). And **`run_agent` must return `result["messages"]`** — agentevals reads the *messages* to reconstruct the tool path; return only the final string and there's no trajectory to score.

## Fits
raaaaag's harness is **outcome** eval (hit@k, refusal) and already gates-deterministic/reports-flaky — the next step is a **trajectory** eval (did it call `search_docs` before answering, and not skip it?). [[LangSmith]] hosts both via the feedback/scores API.
