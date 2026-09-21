---
description: "LangSmith observability for LLM apps — traces/spans, env-var setup, @traceable, datasets + evaluation, and feedback/scores (human, rule, LLM-judge). Plus LangSmith vs Langfuse."
domain: ai-eng
type: howto
status: digested
tags:
  - domain/ai-eng
  - type/howto
  - status/digested
  - topic/observability
  - topic/langgraph
  - topic/ai-evaluation
  - langsmith
  - tracing
  - feedback
  - evaluation
aliases:
  - "LangSmith tracing"
  - "LANGSMITH_TRACING"
  - "create_feedback"
  - "observability"
hubs:
  - "[[Observability]]"
  - "[[LangGraph]]"
  - "[[AI Evaluation]]"
---
# LangSmith & Observability

> [!danger] Rotate the leaked key
> The earlier version of this note pasted a **real** `LANGSMITH_API_KEY` (`lsv2_pt_8a9a…`) in plaintext. Rotate it in the LangSmith dashboard and keep keys in a gitignored `.env` only. Redacted below.

Observability = seeing **inside** a non-deterministic, multi-step LLM app after it runs. You can't debug an agent loop by reading the code — the model decides the path. Related: [[LangGraph Long-Term Memory With Trustcall]] context aside, this is the same job you did in raaaaag with Langfuse.

## Trace / span (run)
```text
one user request = one TRACE
  └─ agent (span)          2.1s, 1.4k tokens
     ├─ model call (span)  0.8s   ← the exact prompt + response
     ├─ search_docs (span) 0.5s   ← tool args + result
     └─ model call (span)  0.8s   ← the final answer
```

> [!definition] Trace / span (run)
> A **trace** = one full request end to end. A **span** (LangSmith: **run**) = one step inside it (model call, tool, retriever), nested into a tree with inputs, outputs, tokens, latency, cost, and errors on every node.

## Setup — mostly env vars
LangSmith auto-instruments any LangChain/LangGraph run; no code change, just env:

```dotenv
# .env  (gitignored — never commit real keys)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_***REDACTED***
LANGSMITH_PROJECT=raaaaag-agent   # groups traces
```

```python
from dotenv import load_dotenv
load_dotenv()

# existing agent now emits full traces, no other change
agent.invoke({"messages": [HumanMessage("...")]})
```

For non-LangChain code, wrap it so it shows as a span:
```python
from langsmith import traceable

@tool
@traceable
def rag_process_tool(query: str) -> str:
    """Process queries using RAG to get relevant info from documents."""
    logger.info("rag_process_tool entered")
    result = rag_process(query)
    logger.info("rag_process_tool exited")
    return result
```

## The four jobs of observability
| Job | What LangSmith shows |
|---|---|
| **Debug** | exact prompt/response/tool-args per step; where it errored |
| **Monitor** | latency, tokens, **cost per call**, error rate over time |
| **Evaluate** | run the app over a dataset, score outputs |
| **Improve** | compare two prompt/model versions on the same inputs |

## Datasets + evaluation
Save example inputs (often captured from real traces), run the app over them, **score** the outputs — the hosted version of your raaaaag eval harness.

```python
from langsmith import Client
client = Client()

ds = client.create_dataset("qa-eval")
client.create_examples(
    inputs=[{"q": "what is RRF?"}],
    outputs=[{"answer": "reciprocal rank fusion"}],   # reference
    dataset_id=ds.id,
)

def correct(run, example) -> dict:                    # deterministic or LLM-judge
    ok = example.outputs["answer"].lower() in run.outputs["answer"].lower()
    return {"key": "correct", "score": int(ok)}

client.evaluate(my_app, data="qa-eval", evaluators=[correct])
```

## Feedback / scores — attach a score to a run
Feedback = a score attached to a **specific run after it happened**, linked by **`run_id`**. It turns traces into a quality signal you can query and average. `create_feedback` does **not** run the app or judge anything — it just records a score against an existing run_id.

### The full loop: run → capture run_id → collect feedback
```python
from langsmith import Client
from langsmith.run_helpers import get_current_run_tree
client = Client()

# 1. run the app, return the run_id so it can be scored later
def answer(question: str):
    resp = agent.invoke({"messages": [HumanMessage(question)]})
    run_id = get_current_run_tree().id
    return {"answer": resp["messages"][-1].content, "run_id": str(run_id)}
```

```python
# 2. user reacts → an endpoint attaches feedback to that run_id
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Feedback(BaseModel):
    run_id: str
    thumbs_up: bool
    note: str | None = None

@app.post("/feedback")
def submit_feedback(fb: Feedback):
    client.create_feedback(
        run_id=fb.run_id,                     # WHICH run this scores
        key="user_rating",                    # the metric name
        score=1.0 if fb.thumbs_up else 0.0,   # 👍 = 1.0, 👎 = 0.0
        comment=fb.note,                      # optional reason
    )
    return {"ok": True}
```

```text
user asks → agent runs (run_id=abc123) → answer shown with 👍/👎
   ↓ user clicks 👎 "cited the wrong post"
POST /feedback {run_id: abc123, thumbs_up: false, note: "..."}
   ↓
create_feedback(run_id=abc123, key="user_rating", score=0.0, comment="...")
   ↓
run abc123 now shows score 0.0 → filter "show all 👎 traces" → open → fix
```

### The fields
```python
client.create_feedback(
    run_id="abc123",        # REQUIRED — links the score to that exact trace
    key="user_rating",      # metric name; many keys allowed per run
    score=0.0,              # numeric 0–1 (👍/👎, ratings, pass/fail)
    value="thumbs_down",    # OR a categorical label instead of a number
    comment="wrong date",   # free-text reason
)
```
- **`key`** → track several signals on one run (`user_rating`, `hallucination`, `latency_ok`), each its own column.
- **`score`** = numeric (averages/graphs); **`value`** = categorical label. Use one or both.

### Three sources of feedback
```python
# 1. HUMAN — real user signal
client.create_feedback(run_id, key="user_rating", score=0.0)

# 2. AUTOMATED RULE — cheap deterministic check
if len(answer) < 10:
    client.create_feedback(run_id, key="too_short", score=0.0)

# 3. LLM-AS-JUDGE — a second model grades it
verdict = judge_llm.invoke(f"Is this grounded? PASS/FAIL:\n{answer}").content
client.create_feedback(run_id, key="grounded",
                       score=1.0 if verdict == "PASS" else 0.0)
```

> [!tip] Why feedback matters
> It's the loop from *production complaint* → *root cause* → *fix*: "show every trace where `user_rating`=0 last week" → open those exact traces → see the prompt/tool-args that caused it → fix. Same scoring idea as the raaaaag eval harness, but on **live** traffic instead of a test set.

## LangSmith vs Langfuse (you used Langfuse in raaaaag)
| | LangSmith | Langfuse |
|---|---|---|
| Made by | LangChain | independent, **open-source** |
| Hosting | SaaS (cloud) | self-host or cloud |
| Best fit | all-in on LangChain/LangGraph | want to self-host / avoid lock-in |
| Tracing | auto via env vars | SDK / `@observe` |

Same job (traces, datasets, evals, scores). raaaaag picked Langfuse (open-source, self-hostable, own key). LangSmith is the zero-config option if you're already in LangChain.

> [!tip] The through-line
> **Tracing** = one request's tree · **Monitoring** = traces in aggregate (latency/cost/errors) · **Evaluation** = score outputs over a dataset · **Feedback** = attach real-world scores by run_id. All four = observability. For agents it's not optional — you can't debug a non-deterministic loop from the source.

Ties to the parked **[[otel-langfuse-grafana]]** lesson: **OTel** = the vendor-neutral standard for emitting spans; **Langfuse / LangSmith / Grafana** = backends that receive and display them. LangSmith is the LangChain-flavored backend; the OTel lesson is the theory underneath all of them.
