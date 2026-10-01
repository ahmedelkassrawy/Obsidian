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

`route_after_intent` already sends `errors` to handoff.

### Fixed: an LLM failure now escalates instead of returning 500

```python
last_message = messages[-1]
try:
    intent = classifier.classify_intent(last_message.content)
except Exception as e:
    return {
        "errors": [f"Intent classification failed: {e}"],
        "trajectory": ["classify_intent"],
        "step_count": 1,
    }
```

```text
Before: LLM timeout -> exception -> run aborts -> 500
After:  LLM timeout -> errors written -> route_after_intent -> human_handoff -> 200 "escalated"
```

- **The `try` wraps only the classifier call.** A bug anywhere else in the node still raises loudly instead of being hidden as "escalated."
- **Catching every `Exception` is right here, and only here.** This is the boundary with an external service (timeouts, rate limits, malformed output, auth errors), and the policy at that boundary is one rule: whatever goes wrong, a human takes over. Do not copy a broad `except` into other nodes by reflex.
- `f"{e}"` already calls `str(e)`. Writing `{str(e)}` is redundant.

> [!important] "Fails safely" needs two parts
> 1. The node **catches** the failure and **writes** it to state.
> 2. A route **reads** that state and sends it somewhere safe.
> Before the fix only part 2 existed, so the safety rule looked implemented but was not.

Tested in [[09 API Testing#The LLM-failure test: a fake that raises]].

Still open: `execute_action` raises the same way when the refund service or gateway fails. That one needs its own decision because it happens **after** a human approved money.

### Structured output is a parser, not a guarantee

`llm.with_structured_output(TicketIntent)` makes the model return data that validates against `TicketIntent`, and `model_validate` checks it again. It guarantees **shape**, not **truth**. The `confidence` value is the model's own guess and is not calibrated. That is why low confidence routes to a human and why tests use a fake classifier instead of the real LLM.

### `.env` format

One `KEY=value` per line. Lines starting with `#` are comments. Quote the value if it contains spaces or `#`. A line without `=` (or a pasted multi-line value) is what `python-dotenv` reports as malformed.

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[LLM Gateways]]
- [[Agent Guardrails]]
%% related:end %%
