---
date: 2026-09-25
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - topic/agents
  - topic/testing
  - resolveflow
description: "Index for the ResolveFlow engineering journal: build order, current progress, and learning log."
aliases:
  - ResolveFlow Learning Journal
  - Project ResolveFlow Notes
hubs:
  - "[[Agent Engineering MOC]]"
---

# 00 ResolveFlow Index

> [!abstract] Purpose
> This is my living engineering journal for ResolveFlow. I update it with what I build, what I learn, mistakes I uncover, and changes in how I think about the system. It complements [[ResolveFlow — Flagship Build Spec]] and [[ResolveFlow — AI Handoff Prompt]].

## Build order

The notes follow the order the system was built in.

1. [[01 Planning and Engineering Principles]]
2. [[02 Project Setup and Domain Models]]
3. [[03 Duplicate Detection]]
4. [[04 Mock Billing Gateway and Idempotency]]
5. [[05 RefundService]]
6. [[06 LangGraph Orchestration]]
7. [[07 Intent Routing and LLM Classifier]]
8. [[08 FastAPI Layer]]
9. [[09 API Testing]]

Across all steps: [[90 Mistakes and Checklist]]

## What the system is now

So what we have now is 
Detetc a duplicate charge -> collect evidence -> propose refund -> pause for human approval -> and execute the refund safely

Domain Models -> define the business data
Services -> implement deterministic business rules
Infrastrcutre -> stimulate the external billing provider

```
ResolveFlow/
├── src/resolveflow/
│   ├── domain/
│   │   ├── enums.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── duplicate_detection.py
│   │   └── refund_service.py
│   │
│   ├── infrastructure/
│   │   └── mock_billing.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── routes.py
│   │   └── builder.py
│   │
│   └── config.py
│
├── tests/
│   ├── test_domain_models.py
│   ├── test_duplicate_detection.py
│   ├── test_mock_billing.py
│   ├── test_refund_service.py
│   └── test_refund_graph.py
│
├── alembic/
├── main.py
├── pyproject.toml
└── README.md
```

## Current progress

- [x] Establish product invariants and the first vertical slice.
- [x] Create the `src/resolveflow` package layout.
- [x] Define domain enums and Pydantic models.
- [x] Add domain-model validation tests.
- [x] Build deterministic duplicate-charge detection.
- [x] Test the same idempotency key with the same parameters.
- [x] Reject the same idempotency key with different parameters.
- [~] Finish mock billing safety tests.
  - [x] Reject pending and failed transactions.
  - [x] Reject wrong-tenant access.
  - [x] Reject amount and currency mismatches.
  - [x] Reject a second refund using a different key.
- [ ] Build an approval-aware `RefundService`.
- [ ] Introduce LangGraph after the deterministic action boundary is safe.

## Next engineering step

Finish the mock billing gateway's negative cases. Then add a `RefundService` that:

1. Accepts a `ProposedAction` and `ApprovalDecision`.
2. Confirms that both reference the same action.
3. Requires an approved decision.
4. Derives a stable idempotency key.
5. Calls the mock billing gateway.

The LLM must never call the gateway's refund method directly.

## Learning log

### 2026-09-25 — Domain modeling, tests, and idempotency

- Learned why a `src` layout imports `resolveflow`, not `src.resolveflow`.
- Learned the difference between field validation and cross-field model validation.
- Learned that a negative test must have only one invalid condition.
- Learned that a test containing only `...` passes without proving anything.
- Learned how `pytest.mark.parametrize` runs one test body with several inputs.
- Built deterministic duplicate detection before introducing an LLM.
- Built a mock billing gateway and tested idempotent retries.
- Learned that reusing one idempotency key with different parameters must be rejected.
- Learned that `@property` exposes computed behavior through attribute syntax; it does not update state by itself.

### 2026-09-28 — FastAPI layer over the graph

- Learned that a returned `JSONResponse` skips `response_model` validation, and that `model_dump(mode="json")` is needed only when data goes over the wire.
- Learned that `__interrupt__` exists only in the `invoke()` return value; saved state uses `snapshot.next`.
- Derived API status and message from graph state; check handoff before errors.
- Learned that `async def` + sync `invoke()` blocks the event loop; switched to `def`.
- Added the approval endpoint with a `snapshot.next` guard and a structured resume that records the real reviewer.
- Learned that passing tests are not proof: a fix needs an assertion that would fail without it.
- Added `GET /tickets/{ticket_id}` (404 via `snapshot.values`, waiting via `snapshot.next`).
- Wrote the first API test: fake classifier + `monkeypatch` + `TestClient`, proving a ticket created in one request can be read in another.
