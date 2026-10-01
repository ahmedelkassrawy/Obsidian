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
description: "Approval-aware refund service: authorization checks, idempotency key, and lessons to reuse."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 05 RefundService

> Part of [[00 ResolveFlow Index]]. Previous: [[04 Mock Billing Gateway and Idempotency]] · Next: [[06 LangGraph Orchestration]]

## Build notes

Refund-execution system
safety boundary between a proposed action and the billing provider.

Before executing anything, `RefundService.execute()` verifies:

- The action type is `REFUND`.
- The approval decision belongs to that action’s UUID.
- The decision is explicitly approved.
- The refund contains an amount and currency.

It then creates this idempotency identity:
```
tenant_id
+ ticket_id
+ action_id
+ "refund"
+ target_transaction_id
```

```python
idempotency_key = (
            f"{action.tenant_id}:"
            f"{action.ticket_id}:"
            f"{action.action_id}:"
            f"refund:{action.target_id}"
        )
```

This means retrying the same proposed action generates the same provider key.

The service then calls the billing gateway and converts the returned receipt into an `ActionResult`.

## RefundService — lessons to reuse

The earlier section describes *what* `RefundService` checks. These are the parts worth repeating in any service that performs a consequential action.

### Bind the approval to the exact action

```python
if decision.action_id != action.action_id:
    raise ValueError("Approval decision does not match the action")
```

This is the check that is easiest to forget. Without it, an approval given for action A could be passed in with action B, and B would execute as "approved." An approval is only meaningful for **one specific action**, so the service must verify the pairing, not just `status == APPROVED`.

> [!tip] General rule
> Authorization answers two questions: *is this approved?* and *is this approval for this exact thing?* Checking only the first is a classic replay hole.

### Guard-clause order

```text
1. Is this the right kind of action?      (REFUND)
2. Does the approval belong to it?        (action_id match)
3. Is it approved?                        (status)
4. Is the data complete?                  (amount, currency)
5. Only then: build key, call provider
```

Every check runs before anything with a side effect. A service that moves money should have a visible "nothing happens above this line" boundary.

### Idempotency keys come from stable IDs, never time or randomness

```python
f"{tenant_id}:{ticket_id}:{action_id}:refund:{target_id}"
```

A retry must rebuild the **same** key. Anything like `datetime.now()` or a fresh `uuid4()` inside `execute()` would make every retry look new.

> [!warning] Subtle: `action_id` is generated with `default_factory=uuid4`
> If the graph ever re-runs `propose_action`, the new `ProposedAction` gets a **new** `action_id`, so the key changes and key-based idempotency will not catch it. What saves us is the gateway's second check: "this transaction is already refunded." That is why there are two layers (defense in depth). Never rely on one idempotency mechanism for money.

### Raise vs. return a failed result

Right now every failure raises `ValueError` (from the service or the gateway), and `execute_action` does not catch it, so the graph run aborts. A useful split for later:

| Kind of failure | Handle it by |
|---|---|
| Programmer error / broken invariant (wrong action type, mismatched approval) | Raise. It should never happen and must be loud. |
| Expected business outcome (provider declines, already refunded) | Return `ActionResult(status=FAILED, ...)` so the graph and API can report it. |

Open decision: not changed yet.

### Depend on what you need, add abstractions when a second implementation exists

`RefundService` takes a `MockBillingGateway` directly. That is fine while there is one gateway. A `Protocol` becomes worth it at the moment a real provider client appears, because then two classes must satisfy the same contract. Not before.

### Test that the side effect did **not** happen

```python
with pytest.raises(ValueError, match="must be approved"):
    service.execute(action, rejected_decision)

assert gateway.refund_count == 0
```

For negative tests of actions, the exception alone is not enough. Assert the external effect is absent.

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[01 Planning and Engineering Principles]]
%% related:end %%
