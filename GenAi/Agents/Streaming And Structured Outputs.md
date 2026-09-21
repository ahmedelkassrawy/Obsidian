---
description: "Two agent I/O concerns — streaming (tokens + step events for live UX, via LangGraph stream_mode) and structured outputs (schema-validated data via with_structured_output). When to use each, code, and the tension between them."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/agents
  - topic/langgraph
  - topic/structured-output
  - agents
  - streaming
  - structured-output
  - pydantic
hubs:
  - "[[Agents]]"
  - "[[LangGraph]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# Streaming & Structured Outputs

> Related: [[Agent Workflow Patterns (The Five)]] (structured output as a router) · [[LLM Gateways]] (must pass streaming through) · [[Agent Handoffs And Tool Design]] (field descriptions are prompts).

Two agent I/O concerns: **streaming** makes output *feel* fast; **structured output** makes it *machine-usable*.

## Streaming
Agents are slow (many LLM calls). Streaming shows progress instead of a frozen wait. Two things to stream:
```text
1. TOKENS       → the model's text, word by word (perceived latency ↓)
2. STEPS/EVENTS → which node ran, which tool was called (progress + debugging)
```

> [!definition] Streaming
> Emitting partial output as it's produced rather than one final blob. **Token streaming** = the answer appears live; **event streaming** = intermediate steps (tool calls, node transitions) surface as they occur.

LangGraph `stream_mode`:
```python
# stream the AGENT'S TOKENS as they generate
for chunk, meta in agent.stream({"messages": [("user", q)]}, stream_mode="messages"):
    print(chunk.content, end="", flush=True)     # live text

# stream PER-NODE updates (what each step produced)
for update in agent.stream({"messages": [("user", q)]}, stream_mode="updates"):
    print(update)     # {'model': {...}} then {'tools': {...}} — the loop running

# fine-grained events (tool start/end, token, etc.)
async for ev in agent.astream_events({"messages": [("user", q)]}, version="v2"):
    if ev["event"] == "on_tool_start":
        print("calling:", ev["name"])
```
| `stream_mode` | Emits |
|---|---|
| `"messages"` | LLM tokens (+ metadata) — live text |
| `"updates"` | each node's output as it finishes — step progress |
| `"values"` | the full state after each step |
| `"custom"` | your own `get_stream_writer()` events (e.g. "searching…") |

**Best practices**
- Stream to the UI over **SSE or WebSockets**.
- Show **tool-call status** ("searching docs…") from `updates`/events so the user knows *why* it's waiting.
- The **gateway must pass tokens through**, not buffer ([[LLM Gateways]]).
- Send a final "done" event so the client stops.

## Structured outputs
Sometimes you need **machine-usable data** — JSON matching a schema — not prose. For extraction, routing, form-filling, anything downstream code consumes.

> [!definition] Structured output
> Forcing the model to return data conforming to a schema (usually Pydantic), validated, instead of free text. Under the hood it uses tool-calling or JSON/constrained decoding so the shape is guaranteed.

The one-liner — `with_structured_output`:
```python
from pydantic import BaseModel, Field

class Post(BaseModel):
    caption: str = Field(description="the post caption, under 150 chars")
    hashtags: list[str] = Field(description="3-5 relevant hashtags")
    schedule_hint: str = Field(description="best time to post, e.g. 'evening'")

structured_llm = llm.with_structured_output(Post)      # returns a validated Post
post = structured_llm.invoke("Draft a launch post for our new feature.")
print(post.caption, post.hashtags)                      # typed object, no json.loads
```
- You get a **typed object back**, not a string to parse.
- **`Field(description=...)` is a prompt** — the model reads it to fill each field (same rule as tool args).
- Invalid output → LangChain re-asks/validates; add Pydantic validators for value rules.

**Structured output as a reliable router:**
```python
class Route(BaseModel):
    domain: str = Field(description="one of: publishing, analytics, ads")
route = llm.with_structured_output(Route).invoke(user_msg).domain   # never a stray string
```

**Best practices**
- Use **Pydantic** (validation + descriptions); **describe every field**.
- Keep schemas **flat** — deep nesting confuses models.
- **Handle failure** — retry on validation error (evaluator-optimizer).
- Don't force structure when you want *prose* — it can dull the writing.

> [!tip] The tension between them
> **Streaming** improves perceived speed + debuggability; **structured output** makes the result machine-usable. But you can't cleanly stream a strict JSON object token-by-token (it's only valid when complete) — **stream prose**, use **structured output for data the code consumes**. Pick per surface.

## Fits
- **Shutterabia:** stream the caption draft to the SMM live (streaming); return the schedule/hashtags as a validated `Post` object the scheduler consumes (structured).
- **Routing** (workflow patterns): use structured output for the classifier so the route is always a valid enum, never a stray string.
- raaaaag: stream the grounded answer's tokens; keep citations as structured data.
