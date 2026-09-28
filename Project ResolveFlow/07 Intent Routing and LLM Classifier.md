---
date: 2026-09-28
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - resolveflow
  - topic/agents
  - topic/llm
description: "Structured-output intent classifier, routing, failure handling, and .env setup."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 07 Intent Routing and LLM Classifier

> Part of [[00 ResolveFlow Index]]. Previous: [[06 LangGraph Orchestration]] · Next: [[08 FastAPI Layer]]

## Build notes

Ticket intake and intent routing
message should be clasiifeied into 3 categouries
- Duplicate charges -> refund workflow
- Billing question -> billing path
- Human Support -> low confidnece or an supported intent

## Lessons to reuse

### An exception is not a route

Routes only see what nodes **write** to state. If a node raises, the run aborts: no route runs and no handoff happens.

```text
classify_intent raises (LLM timeout)
    -> run aborts
    -> API returns 500
    -> route_after_intent never sees it
```

So "unknown/low-confidence fails safely to human handoff" is only true for answers the classifier **returns**. To make LLM failures fail safely too, the node must catch and write the error:

```python
try:
    intent = classifier.classify_intent(last_message.content)
except Exception as exc:
    return {"errors": [f"Intent classification failed: {exc}"], ...}
```

`route_after_intent` already sends `errors` to handoff. Open item: not changed yet. The same applies to `execute_action`.

### Structured output is a parser, not a guarantee

`llm.with_structured_output(TicketIntent)` makes the model return data that validates against `TicketIntent`, and `model_validate` checks it again. It guarantees **shape**, not **truth**. The `confidence` value is the model's own guess and is not calibrated. That is why low confidence routes to a human and why tests use a fake classifier instead of the real LLM.

### `.env` format

One `KEY=value` per line. Lines starting with `#` are comments. Quote the value if it contains spaces or `#`. A line without `=` (or a pasted multi-line value) is what `python-dotenv` reports as malformed.
