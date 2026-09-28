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

> Part of [[00 ResolveFlow Index]]. Previous: [[09 API Testing]]

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
- [ ] Saying "check" without running the tests first. Two missing commas meant the file could not even load.
- [ ] Writing a test expectation from memory instead of from the flow: expecting 200/`COMPLETED` on a path that pauses for approval (202).
- [ ] Guessing an API's URL and body (`/approve`, `approver_id`) instead of copying them from the endpoint and its schema.
- [ ] Making a request in a test without asserting its response. A call you do not check proves nothing.
- [ ] Using the wrong enum because the string value happens to match (`TicketStatus.COMPLETED` on a `Transaction`).
- [ ] `Decimal(100.0)` for money. Build `Decimal` from a string: `Decimal("100.00")`.
- [ ] Sending fields the server ignores (`ticket_id` in the body when it is already in the URL).

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
- Would this test fail if my fix were removed?
- Is every request's response asserted? Is the side effect counted before **and** after?
- For anything that moves money: does a test repeat the action and prove it happens once?
- Did I run the tests before asking for review?
