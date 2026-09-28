---
date: 2026-09-28
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - resolveflow
  - topic/testing
description: "Mistakes I made while building ResolveFlow, and the checklist to run on every build."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 90 Mistakes and Checklist

> Part of [[00 ResolveFlow Index]]. Previous: [[08 FastAPI Layer]]

## Mistakes worth remembering

Short list of things I got wrong, so I check for them next time.

- [ ] Indexing a key that only some paths write (`response["__interrupt__"]`). Use `.get()`.
- [ ] Returning a `JSONResponse` and assuming `response_model` validates it.
- [ ] `JSONResponse(status=...)` instead of `status_code=`.
- [ ] Using `messages[-1]` as "the AI reply."
- [ ] Putting a fallback `return` inside the loop instead of after it.
- [ ] `async def` around a synchronous, slow call.
- [ ] 400 for "not found." 400 = malformed request, 404 = not found, 409 = wrong state.
- [ ] Hard-coding an identity (`"local-reviewer"`) in an audit record.
- [ ] Trusting green tests after a change, without an assertion that would fail if the fix were missing.
- [ ] Implementing the next two steps ahead while fixing the current one. Smaller diffs are easier to review.
- [ ] Assuming "fails safely" covers exceptions. Routes only see what nodes write.

---

## Every-build checklist

Run through this whenever I add a node, service, or endpoint.

**Behavior**
- What does each path end with: which status, which message?
- What is the safest place for the unknown case to go?

**State and data**
- Which keys can be missing on some paths? Use `.get()` for them.
- Accumulating field → reducer. Single current value → no reducer.

**Safety**
- Does anything move money or change identity/permissions? Then: human approval, approval bound to the exact action, stable idempotency key, a second defensive check.
- Is there any side effect before an `interrupt()`?
- What happens when a dependency **raises**, not just returns a bad value?

**API**
- Does every response (including 202 and errors) match the response model?
- Is a slow synchronous call inside `async def`?
- Right status code: 200/202/400/404/409?

**Tests**
- Fake the LLM; never call a real provider in unit tests.
- Assert the path (`trajectory`), not only the result.
- For negative action tests, assert the side effect did not happen.
