---
date: 2026-09-28
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - resolveflow
  - topic/api
description: "FastAPI endpoints over the LangGraph workflow: status derivation, 202 approval flow, resume, and audit trail."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 08 FastAPI Layer

> Part of [[00 ResolveFlow Index]]. Previous: [[07 Intent Routing and LLM Classifier]] · Next: [[09 API Testing]]

## API layer (FastAPI over the graph)

The API is a thin layer: it turns HTTP requests into graph runs and turns graph state back into a `TicketResponse`. The gateway, classifier, and compiled graph are created once at module level, so every request shares the same `InMemorySaver` checkpoint.

```text
POST /tickets                    -> start a new thread (ticket_id = thread_id)
POST /tickets/{ticket_id}/approval -> resume the paused thread
GET  /tickets/{ticket_id}        -> read the latest checkpoint (next step)
```

### `ticket_id` is the `thread_id`

```python
ticket_id = str(uuid4())
config = {"configurable": {"thread_id": ticket_id}}
```

The same config always points at the same checkpoint. That is what lets a second HTTP request (the approval) continue the exact run that the first request paused.

### Use `.get("__interrupt__")`, not `["__interrupt__"]`

Only the approval path pauses. The billing-question and human-handoff paths finish without an `__interrupt__` key, so indexing it directly raises `KeyError`.

> [!note] Where `__interrupt__` lives
> `__interrupt__` only appears in the **return value of `invoke()`**. It is not stored in the checkpoint. When reading saved state later, a paused thread is recognised by `snapshot.next` being non-empty.

### A returned `JSONResponse` skips `response_model`

`response_model=TicketResponse` only validates values the endpoint returns as plain data. A `JSONResponse` is sent as-is, so a wrong shape goes out silently. The 202 branch builds a real `TicketResponse` first:

```python
ticket_response = TicketResponse(
    ticket_id=ticket_id,
    status=TicketStatus.AWAITING_APPROVAL,
    message="Refund proposal needs reviewer approval",
    proposed_action=response.get("proposed_action"),
)
return JSONResponse(
    status_code=status.HTTP_202_ACCEPTED,
    content=ticket_response.model_dump(mode="json"),
)
```

- The reviewer needs `ticket_id` to approve later, and `proposed_action` to see what they are approving.
- `mode="json"` converts `Decimal`, `UUID`, `datetime`, and enums into JSON-safe values. `JSONResponse` cannot serialize them otherwise.
- The keyword is `status_code`, not `status`. `status=` raises `TypeError`, and the 202 path becomes a 500.

> [!tip] When `mode="json"` matters
> Use `model_dump(mode="json")` when the result goes **over the wire** (HTTP, JSON). Plain `model_dump()` is fine for `Command(resume=approval_request.model_dump())`, because the checkpointer stores Python values and `ApprovalRequest` only holds plain `str`/`bool`.

### Deriving the API status from graph state

The graph has no `status` field, so the API derives it:

```python
def get_ticket_status(state) -> TicketStatus:
    if "human_handoff" in state.get("trajectory", []):
        return TicketStatus.ESCALATED
    if state.get("errors"):
        return TicketStatus.FAILED
    return TicketStatus.COMPLETED
```

> [!important] Order matters
> `route_after_intent` sends any state with `errors` to `human_handoff` (for example, `classify_intent` with no messages). Such a ticket has errors **and** was escalated. Checking errors first would report it as `FAILED`. Check handoff first.
>
> Correction: a classifier that **raises** (LLM timeout, bad output) does not add to `errors`. The exception aborts the run. See [[07 Intent Routing and LLM Classifier#An exception is not a route]].

It is a module-level function (not inline) for one concrete reason: `/tickets` and the approval endpoint both need it.

### Deriving the message: last `AIMessage`, not `messages[-1]`

On the validation-failure path no node adds an `AIMessage`, so `messages[-1]` is the customer's own text, and the API would echo it back.

```python
def get_last_ai_message(state) -> str:
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, AIMessage):
            return msg.content
    return "The request could not be processed."
```

- The fallback `return` sits **outside** the loop. Inside it, the function only ever looks at the last message, and an empty list returns `None`, which fails `TicketResponse` validation (500).
- The fallback does not include `errors` text. Some errors are internal (classifier exceptions) and should not reach a client.

### `async def` + synchronous `invoke()` blocks the server

`async def` endpoints share one event loop, which can only switch tasks at an `await`. `agent.invoke()` is synchronous and includes an LLM call, so it freezes every other request, `/health` included, for seconds.

| Option | When it is right |
|---|---|
| `def` endpoint | Sync graph and clients. FastAPI runs it in a thread pool. **Chosen.** |
| `async def` + `await agent.ainvoke()` | Only when the classifier and gateway are async all the way down. |

`/health` stays `async def` because it does no blocking work.

### Approval endpoint

```python
snapshot = agent.get_state(config)
if not snapshot.next:
    raise HTTPException(status_code=404, detail="No tickets found waiting for approval")

response = agent.invoke(Command(resume=approval_request.model_dump()), config)
```

- **The `snapshot.next` guard is required.** This endpoint moves money. It must never resume an unknown or already-finished thread.
- **404, not 400.** 400 means the request is malformed. Here the body is fine; the ticket is not waiting. Later: 404 for unknown, 409 for already finished.
- **Race to know about:** two simultaneous approvals can both pass the guard. The gateway's idempotency key still prevents a double refund.

### The decision node owns its reply

A rejected refund routed straight to `END` with no `AIMessage`, so the API returned the "could not be processed" fallback, which is untrue. The fix went in the graph, not the API: `request_approval` adds `"The refund was not approved by the reviewer."` when the status is `REJECTED`. The node that makes a decision should also produce its reply.

### Structured resume for a real audit trail

The node used to resume with `"yes"`/`"no"` and hard-code `reviewer_id="local-reviewer"`. Every refund would have looked approved by the same person. Now the node reads the real values:

```python
status = ApprovalStatus.APPROVED if response["approved"] else ApprovalStatus.REJECTED
decision = ApprovalDecision(
    action_id=proposed_action.action_id,
    reviewer_id=response["reviewer_id"],
    status=status,
    comment=response.get("comment"),
)
```

`ApprovalDecision.reviewer_id` has `min_length=1`, so an empty reviewer now fails loudly instead of being saved.

> [!warning] Tests must prove the fix
> After changing the resume shape, the tests passed, but they would also have passed with the hard-coded reviewer. The fix is only proven by asserting it:
> ```python
> assert final_state["approval_decision"].reviewer_id == "reviewer-1"
> ```

### `GET /tickets/{ticket_id}`: reading a ticket from the checkpoint

```python
@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str):
    config = {"configurable": {"thread_id": ticket_id}}
    snapshot = agent.get_state(config)

    if not snapshot.values:
        raise HTTPException(status_code=404, detail="Ticket not found")

    state = snapshot.values
    if snapshot.next:
        ticket_status = TicketStatus.AWAITING_APPROVAL
        message = "Refund proposal needs reviewer approval"
    else:
        ticket_status = get_ticket_status(state)
        message = get_last_ai_message(state)
    ...
```

Verified with a fake classifier: an unknown thread gives `values={}` and `next=()`, and a finished thread has values and `next=()`.

- 404 check uses `snapshot.values` (empty for unknown IDs). A finished ticket has values but no `next`, and it must return 200.
- Pause check uses `snapshot.next`, not `"__interrupt__"`.
- Returns 200 even while waiting. The 202 on POST meant "accepted, not finished." A GET succeeded at reading; the `status` field carries the waiting state.
- Security gap for later: anyone with a `ticket_id` can read the ticket. A real system checks the caller's tenant against `tenant_id`.

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[01 - Overview and Project Layout]]
- [[06 LangGraph Orchestration]]
- [[FastAPI - Asynchronous Code and Path Parameters]]
- [[04 - API Endpoints with Database Operations]]
- [[Human-in-the-Loop (Approval & Interrupts)]]
%% related:end %%
