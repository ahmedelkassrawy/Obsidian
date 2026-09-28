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
description: "In-memory billing gateway, refund idempotency, @property, model_copy, and parameterized safety tests."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 04 Mock Billing Gateway and Idempotency

> Part of [[00 ResolveFlow Index]]. Previous: [[03 Duplicate Detection]] · Next: [[05 RefundService]]

## Build notes

building the MockBilling Gateway

to build the idempotency keys 
```python
self._refunds: dict[str, RefundReceipt] = {}
```

the refund receipt is saved by the idemptonecy key and that is used as the key and the value is the RefundReceiprt

a @property is something that gets updated 
```python
@property
    def refund_count(self):
        return len(self._refunds)
```

model copy and updating a single param inside the model 
```python
def _mark_refunded(self,transaction: Transaction):
        updated = transaction.model_copy(
            update = { 
                "status": TransactionStatus.REFUNDED
                }
            )
        
        self.transactions = [
            updated if t.transaction_id == transaction.transaction_id
            else t for t in self.transactions
        ]
```

here the parameterized pytest uses the status to intercgangily use them without having to rewrite the whole thing again

## How the gateway works

Mock Billing Gateway 
simulates an external billing provider.

It stores:

- Transactions.
- Refund receipts indexed by idempotency key.

Its refund operation verifies:

- The transaction exists under the requested tenant.
- Its status is `COMPLETED`.
- It has not already been refunded.
- Amount and currency match exactly.
- An idempotency key is not being reused with different parameters.

Its retry behavior is important:
```
Same key + same request
→ return the existing receipt

Same key + different request
→ reject

Different key + already refunded transaction
→ reject
```

After a successful refund, it creates an immutable updated copy of the transaction with status `REFUNDED`.

This produces two separate safety boundaries:

```
RefundService
    authorization and command identity
            ↓
MockBillingGateway
    provider facts, eligibility and idempotency
```

## Idempotency mental model

The mock billing gateway stores refund receipts by idempotency key:

```python
self._refunds: dict[str, RefundReceipt] = {}
```

Required behavior:

```text
Same key + same parameters
    -> return the original receipt

Same key + different parameters
    -> reject the request

Different key + already-refunded transaction
    -> reject the request
```

Idempotency does not mean the function is called exactly once. It means repeated attempts produce one externally visible effect.

The idempotency lookup happens before checking whether the transaction is already refunded:

```text
refund succeeds
    -> receipt is stored
    -> network response is lost
    -> caller retries with the same key
    -> gateway returns the stored receipt
```

If the transaction-status check happened first, the legitimate retry would incorrectly fail as “already refunded.”

## Corrected lessons

### `@property`

```python
@property
def refund_count(self) -> int:
    return len(self._refunds)
```

`@property` does **not** update a value. It lets a method be read using attribute syntax:

```python
gateway.refund_count
```

Each access calculates the current length of `_refunds`.

### Frozen models and `model_copy`

Because `Transaction` is immutable, updating its status creates a new instance:

```python
updated = transaction.model_copy(
    update={"status": TransactionStatus.REFUNDED}
)
```

The stored transaction is then replaced by the updated copy.

### Parameterized tests

```python
@pytest.mark.parametrize(
    "status",
    [
        TransactionStatus.PENDING,
        TransactionStatus.FAILED,
    ],
)
def test_non_completed_transaction_cannot_be_refunded(
    status: TransactionStatus,
) -> None:
    ...
```

Pytest runs the same test body twice: once with `PENDING` and once with `FAILED`. Each case is still reported separately.
