# Agent Evaluation — Why Single-Run Eval Is Worthless

> *"If your Evaluation consists solely of Accuracy or LLM-as-a-Judge... then you haven't even started evaluating AI Agents yet."*

## The Core Problem

AI Agents are **Non-Deterministic Systems**. The same input can produce:

- A different trajectory
- Different tool calls
- Different context
- A different outcome

A single run — even if the result looks good — is **statistically worthless**.

## What True Evaluation Must Answer

| Question | What It Measures |
|---|---|
| Did the agent reach the goal with the lowest cost? | Efficiency |
| How many tool calls did it need? | Tool efficiency |
| How many retries happened? | Robustness |
| Did retrieval affect the decision? | Retrieval quality |
| Was the planning efficient? | Planning quality |
| Did the state change correctly? | State correctness |
| Are there hallucinated actions? | Groundedness |
| Did tool misuse occur? | Tool fidelity |
| Is the latency within SLA? | Performance |
| Did the context window affect decision quality? | Context utilization |

## What a Production Eval Harness Collects

For every run:

- **Task** — the input/instruction
- **Transcript** — full conversation log
- **Trajectory** — step-by-step path the agent took
- **Tool Invocations** — which tools, with what args, in what order
- **Intermediate States** — state snapshots at each step
- **Final Outcome** — the end result
- **Cost Metrics** — tokens, API calls, model tier usage
- **Latency Metrics** — per-step and total wall time
- **Failure Modes** — retries, errors, edge cases hit

## Real Metrics (not just accuracy)

| Metric | What It Captures |
|---|---|
| **Task Success Rate** | Did it complete the goal? |
| **Tool Success Rate** | Did tool calls succeed without errors? |
| **pass@k** | Out of k runs, how many succeeded? |
| **pass^k** | Out of k attempts on the SAME input, how many succeeded? |
| **Cost per Successful Task** | Economic efficiency |
| **Average Tool Calls** | How complex was the path? |
| **Planning Efficiency** | Optimal path vs actual path ratio |
| **Trajectory Length** | Number of steps taken |
| **Context Precision** | Retrieved docs useful vs total retrieved |
| **Groundedness** | Claims in output supported by retrieved context |
| **Faithfulness** | Output stays within retrieved context |
| **Retrieval Recall / Precision** | Standard IR metrics for each retrieval step |

## The Golden Rule

> **Don't evaluate the model. Evaluate the entire cognitive system.**

In most production incidents, the problem isn't the LLM. It lies in:

- Retrieval
- Context construction
- Tool selection
- Memory
- Planning
- State management
- Orchestration

## LLM Development vs AI Engineering

| LLM Development | AI Engineering |
|---|---|
| Evaluate the model | Evaluate the whole system |
| Accuracy / loss | Task success + cost + trajectory |
| Single run | pass^k, distribution of outcomes |
| Prompt tuning | Architecture + observability + eval harness |

> *"The LLM is just a component... while the Agent is a Distributed Cognitive System that requires Observability and Evaluation with the same seriousness as any Distributed Software System."*

## Related

- [[RAG Eval]] — retrieval-specific metrics
- [[LangFuse Observability]] — tracing & instrumentation
- `Google ADK. Agent Observability , Eval` — ADK-specific eval tooling
