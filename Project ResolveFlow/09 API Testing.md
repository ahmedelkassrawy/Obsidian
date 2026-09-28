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
  - topic/api
description: "Testing the FastAPI layer: fake LLM classifier, pytest monkeypatch, and FastAPI TestClient."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 09 API Testing

> Part of [[00 ResolveFlow Index]]. Previous: [[08 FastAPI Layer]] · Next: [[90 Mistakes and Checklist]]

## Why test the HTTP layer at all

The 32 graph and service tests passed the whole time the API had bugs: `KeyError` on `__interrupt__`, `status=` instead of `status_code=`, the customer's message echoed back, `None` from the fallback. None of those live in the graph. They live between the HTTP request and the graph, so only a test that goes through HTTP catches them.

> [!tip] One idea for the whole note
> Fake only what is slow or unpredictable (the LLM). Keep everything else real (graph, routing, checkpointer, FastAPI validation, helpers).

```text
FakeIntentClassifier    -> a predictable "LLM answer"
build_refund_graph(...) -> a real graph using that fake
monkeypatch.setattr     -> the app uses that graph, for this test only
TestClient              -> real HTTP requests to the app, no server
assertions              -> check status codes and JSON, like a client would
```

## The fake intent classifier

The real `IntentClassifier` calls Gemini or OpenRouter. In a test that is a problem because it is:

- **Not deterministic.** The same message can come back with a different intent or confidence. A test that sometimes passes proves nothing.
- **Slow and paid.** Every run is a network call.
- **Dependent on a key and network.** It fails offline, in CI, or when the provider is down, and none of those are bugs in my code.
- **Not steerable.** To test low-confidence handoff I would have to find a message the LLM happens to be unsure about.

```python
class FakeIntentClassifier:
    def __init__(self, intent: TicketIntent):
        self.intent = intent

    def classify_intent(self, message: str) -> TicketIntent:
        return self.intent
```

The test now says "pretend the LLM decided this" and checks what **my code** does with that decision.

> [!note] Two different questions
> Is the LLM classifying correctly? → **evaluation** (a separate dataset and metrics).
> Does my system handle each classification correctly? → **unit tests** with a fake.

It needs no inheritance. The graph only calls `classifier.classify_intent(message)`, and Python only checks that the method exists (duck typing). Swapping works because `build_refund_graph(gateway, classifier)` **receives** the classifier instead of creating it (dependency injection).

## `monkeypatch`: replacing a global for one test

In the graph tests I built the graph myself and passed the fake in. The API is different: `app.py` builds its own graph at import time, with the real classifier, and the endpoints use that global:

```python
agent = build_refund_graph(gateway=gateway, classifier=classifier)  # real LLM inside
```

So the test replaces it:

```python
monkeypatch.setattr(app_module, "agent", fake_agent)
```

This means "for this test only, `app_module.agent` points to `fake_agent`." When the test ends, pytest **restores the original automatically**.

> [!warning] Why not just `app_module.agent = fake_agent`?
> A manual assignment is never undone. Every test that runs afterwards uses the fake too, and tests start depending on the order they run in. The automatic undo is the whole point of `monkeypatch`.

It works because the endpoint looks up `agent` **each time it is called**, not when the function is defined:

```python
def create_ticket(...):
    response = agent.invoke(...)   # looked up in app_module at request time
```

`monkeypatch` is a pytest **fixture**: I ask for it by naming it as a test parameter (`def test_x(monkeypatch)`) and pytest hands it in.

## `TestClient`: calling the API without a server

A normal request:

```text
curl / browser -> network -> uvicorn -> FastAPI app -> endpoint
```

With `TestClient`:

```text
test -> TestClient -> FastAPI app -> endpoint
```

Same interface as a real HTTP client (`client.post`, `client.get`, `.status_code`, `.json()`), but it calls the app in memory. No server to start, no port, fast.

It still runs the **whole FastAPI pipeline**, not just my function:

- JSON body → `TicketRequest` validation (a missing field really returns 422)
- path parameters like `{ticket_id}`
- `response_model` checking and serialization
- `HTTPException` → a real 404
- my `JSONResponse` with its 202

> [!important] Calling the endpoint function directly is not the same
> `create_ticket(TicketRequest(...))` skips all of the above. The `status=` bug and response-model mismatches would not show up.

### Why `client` is kept in a variable

`client = TestClient(app_module.app)` wraps the app once, then several requests go through it:

```python
created = client.post("/tickets", json={...})              # creates thread <id>
read = client.get(f"/tickets/{created.json()['ticket_id']}")  # reads thread <id>
```

Both requests hit the same `fake_agent` and therefore the same `InMemorySaver`. If the GET finds the ticket, that proves the API's main promise: a ticket created in one request can be read in another, through `ticket_id` = `thread_id`. One call alone cannot prove that.

## The first API test

```python
def test_billing_question_can_be_created_and_read(monkeypatch):
    intent = TicketIntent(
        intent=IntentType.BILLING_QUESTION,
        confidence=0.95,
        reasoning="General billing question",
    )
    fake_agent = build_refund_graph(
        gateway=MockBillingGateway(transactions=[]),
        classifier=FakeIntentClassifier(intent),
    )
    monkeypatch.setattr(app_module, "agent", fake_agent)
    client = TestClient(app_module.app)

    created = client.post(
        "/tickets",
        json={"tenant_id": "tenant-a", "customer_id": "customer-1", "message": "How do invoices work?"},
    )
    assert created.status_code == 200
    body = created.json()
    assert body["status"] == TicketStatus.COMPLETED

    read = client.get(f"/tickets/{body['ticket_id']}")
    assert read.status_code == 200
    assert read.json()["status"] == TicketStatus.COMPLETED
```

Result: 33 passed.

> [!note] Comparing JSON to an enum
> `body["status"]` is a plain string from JSON. `== TicketStatus.COMPLETED` works because `TicketStatus` is a `StrEnum`, and a `StrEnum` member equals its string value.

## The approval-path test: proving money moves once

The most important API test, because it covers the only path that moves money. It walks the whole journey through HTTP and counts the side effect at each step.

```python
def test_duplicate_charge_requires_approval_and_refunds_once(monkeypatch):
    tx1 = Transaction(
        transaction_id="tx-1", tenant_id="tenant-a", customer_id="customer-1",
        order_id="order-1", amount=Decimal("100.00"), currency="USD",
        status=TransactionStatus.COMPLETED, charged_at="2024-06-01T12:00:00Z",
    )
    tx2 = Transaction(..., transaction_id="tx-2", charged_at="2024-06-01T12:02:00Z")

    gateway = MockBillingGateway(transactions=[tx1, tx2])   # kept to count refunds
    fake_agent = build_refund_graph(gateway=gateway, classifier=FakeIntentClassifier(duplicate_intent))
    monkeypatch.setattr(app_module, "agent", fake_agent)
    client = TestClient(app_module.app)

    # 1. Create: pauses for approval, nothing refunded yet
    created = client.post("/tickets", json={...})
    assert created.status_code == 202
    assert created.json()["status"] == TicketStatus.AWAITING_APPROVAL
    assert created.json()["proposed_action"]["target_id"] == "tx-2"
    assert gateway.refund_count == 0

    # 2. Read while waiting
    waiting = client.get(f"/tickets/{ticket_id}")
    assert waiting.json()["status"] == TicketStatus.AWAITING_APPROVAL

    # 3. Approve: exactly one refund
    approval = {"reviewer_id": "agent-1", "approved": True, "comment": "Verified duplicate charge"}
    approved = client.post(f"/tickets/{ticket_id}/approval", json=approval)
    assert approved.status_code == 200
    assert approved.json()["status"] == TicketStatus.COMPLETED
    assert approved.json()["action_result"] is not None
    assert gateway.refund_count == 1

    # 4. Read after approval
    assert client.get(f"/tickets/{ticket_id}").json()["status"] == TicketStatus.COMPLETED

    # 5. Approve again: refused, still one refund
    again = client.post(f"/tickets/{ticket_id}/approval", json=approval)
    assert again.status_code == 404
    assert gateway.refund_count == 1
```

Result: 34 passed.

### What each part proves

| Step | Assertion | Proves |
|---|---|---|
| 1 | `202` + `refund_count == 0` | Nothing moves before a human approves. |
| 2 | GET shows `awaiting_approval` | The paused state is stored and readable in a separate request. |
| 3 | `refund_count == 1` | Approval actually executes the refund, once. |
| 4 | GET shows `completed` | The final state is stored too. |
| 5 | `404` + `refund_count` still `1` | The `snapshot.next` guard stops a repeated approval from moving money twice. |

> [!important] Count the side effect before **and** after
> `refund_count == 1` alone does not prove much. `== 0` before approval proves the approval gate; `== 1` after the second call proves the refund-once guarantee. The **pair** of numbers tells the story.

### What went wrong in my first two attempts

The first version **passed-looking but proved nothing**:

- It expected `200` / `COMPLETED` from the POST. A duplicate charge pauses, so the correct answer is `202` / `AWAITING_APPROVAL`. The failing test was right; my expectation was wrong.
- The approval call used `/approve` (the endpoint is `/approval`) and `approver_id`/`reason` (the schema is `reviewer_id`/`approved`). It would have returned 404 or 422.
- The approval response was never assigned or asserted, so that failure was **silent**.
- The final GET only checked `200`, which a **paused** ticket also returns. With the POST expectation fixed, the test would have passed with **no refund at all**.

The second version had the right idea but:

- **Two missing commas**, so the file could not load and pytest collected nothing from it.
- Still `/approve`.
- `status=TicketStatus.COMPLETED` on a `Transaction`. The right enum is `TransactionStatus`. It "worked" only because both enums use the string `"completed"`.
- `Decimal(100.0)` instead of `Decimal("100.00")`.
- An extra `ticket_id` in the approval body, which FastAPI silently ignored.
- No second-approval check, which is the reason the test exists.

> [!tip] Money in Python
> `Decimal(0.1)` → `0.1000000000000000055511151231257827…` because the float is already inexact before `Decimal` sees it. `Decimal("0.1")` → exactly `0.1`. Always build money from strings.

> [!note] Test data away from the edges
> The first version put the two charges exactly 5 minutes apart, on the boundary of the 5-minute window. If `<=` ever becomes `<`, the API test breaks for a reason unrelated to the API. Keep test data clearly inside the rule (2 minutes) unless the test is **about** the boundary.

## The limit of this approach

This test only runs because my real API key is in `.env`. Importing `app.py` still builds the **real** classifier first, and `create_llm` raises if the key is missing. On a machine without the key (CI, a teammate), the import fails before any test runs.

`monkeypatch` swaps the graph **after** the real one was already built. The clean fix is to stop building it at import time: an app factory or FastAPI lifespan that receives the graph. That is the next architectural step, and it will be safe to make because these API tests will protect it.
