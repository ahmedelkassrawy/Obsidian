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
description: "Living engineering journal for ResolveFlow: architecture decisions, implementation lessons, tests, and progress."
aliases:
  - ResolveFlow Learning Journal
hubs:
  - "[[Agent Engineering MOC]]"
---

# Project ResolveFlow Notes

> [!abstract] Purpose
> This is my living engineering journal for ResolveFlow. I update it with what I build, what I learn, mistakes I uncover, and changes in how I think about the system. It complements [[ResolveFlow — Flagship Build Spec]] and [[ResolveFlow — AI Handoff Prompt]].

## Index

- [[#Original CEO brief]]
- [[#Refined engineering principles]]
- [[#Corrected implementation lessons]]
- [[#Duplicate-detection rule]]
- [[#Idempotency mental model]]
- [[#Current progress]]
- [[#Next engineering step]]
- [[#Learning log]]

## Original CEO brief

We run a multi-tenant SaaS platform. Our support team spends too much time investigating billing issues across documentation, account records, transactions, and refund policies.

I want you to build **ResolveFlow**, an AI support-operations system. Its first production scenario is:

> A customer reports a duplicate charge and requests a refund.

The system should investigate the case, collect evidence, propose a resolution, and help the support agent complete the case. It must never perform a consequential action—refund, cancellation, credit, or account change—without explicit human approval.

My non-negotiable requirements are:

- No data may leak between tenants.
- Every proposed conclusion must be supported by evidence.
- Consequential actions require human approval.
- Retried requests must never execute an action twice.
- Every model call, tool call, decision, failure, and approval must be auditable.
- Development must use synthetic data and mock external services.
- The first version should prove the core workflow, not integrate with Zendesk or build an elaborate frontend.
- We need objective evaluation—not a demo that merely “looks intelligent.”
- Model cost and latency must be measurable and controllable.

Your first assignment is to present an engineering plan before writing code.

Include:

1. Your understanding of the business problem and primary users.
2. Questions you need answered by me.
3. Assumptions you are making.
4. MVP scope and explicit non-goals.
5. The end-to-end user journey.
6. Proposed system architecture and component responsibilities.
7. Agent/workflow design and why an agent is justified.
8. State and data model.
9. Tenant-isolation and security approach.
10. Failure handling, retries, and idempotency strategy.
11. Evaluation plan and measurable success criteria.
12. Milestones and build order.
13. The largest technical risks and the alternatives you considered.

---
1. Buisness
Resolve a support case using **evidence** without allowing AI to cause an authorized or duplicated financial action 

Evidence -> Source from the RAG
Indempotency to stop the duplication effect
Authorization is required
Tenant data never crosses boundaries

---
2. Vertical Slice
Not begin with billing , techinical support , account support , general questions , RAG 

lets take a complete feature from end-to-end

```
Duplicate Charge ticket

1. check the customer and identify
2. get the transaction
3. detect if duplicated
4. get the policy for this situation
5. propose refund (for the person controlling the agent)
6. request approval (for the person controllling the agent)
7. execute mock refund once
8. report result
```

---
3. Agent Justification
agent is useful where the path depends on :
- interpreting the customer complaint
- deciding which evidence is needed
- choosing the correct tools
- ask for missing info
- making a explanation from the sources retrieved

not important for:
- checking whether 2 transaction share the id
- comparing refund amount against threshold
- prevent the same refund from being executed twice

---
4. Draw Authority Boundaries
```
Customer
   │ untrusted text
   ▼
API authentication ─────────────── deterministic
   │ trusted tenant/user identity
   ▼
Input guardrails
   ▼
Intent router ──────────────────── LLM, structured output
   ▼
Investigation planner ──────────── LLM, read-only tools only
   │
   ├── transaction lookup ──────── deterministic tool
   ├── duplicate detector ──────── deterministic function
   └── policy retrieval ────────── tenant-filtered retrieval
   ▼
Resolution proposal ────────────── LLM, cannot execute
   ▼
Grounding/policy validation ────── deterministic + model-assisted
   ▼
Risk and permission check ──────── deterministic
   ▼
Human approval
   ▼
Refund service ─────────────────── deterministic + idempotent
   ▼
Audit record and customer response
```

----
5. Design state before designing graph nodes
```python
class ResolveFlowState:
	#Identity
	tenant_id: str
	actor_id: str
	customer_id: str | None
	ticket_id: str
	thread_id: str
	
	#understanding
	intent: TicketIntent | None
	original_request: str
	missing_inforamtion: list[str]
	route_confidence: float | None
	
	#Investigation
	plan: Plan | None
	evidence: list[Evidence]
	transaction_ids: list[str]
	policy_ids: list[str]
	
	#Human Deciision 
	approval_status: ApprovalStatus
	approval_by: str | None
	approval_comment: str | None
	
	#Execution
	idempotency_key: str | None
	action_status: ActionStatus
	action_result: ActionResult | None
	
	# Proposed decision
    proposed_resolution: str | None
    proposed_action: ProposedAction | None
    risk_level: RiskLevel | None
    
	# Control
    step_count: int
    retry_count: int
    errors: list[RunError]
    messages: list[Message]
```

---
First we used the README.md and then used the uv project to declare that as the place for the , and then the src folder and have to have init and the config.py and then the domain folders with the enums.py and models.py 

the enums and the models are used for the domain (buisness rules) 
the enums use 
```python
from enum import StrEnum
```

for the models
we have the Domain Model as the default which everyother model inherits from 
```python
class DomainModel(BaseModel):
    """Base Configuration for all domain models."""
    model_config = ConfigDict(
        extra = "forbid",
        frozen = True,
        str_strip_whitespace = True,
    )
```

extra is to make the llm forbid the extra adding
frozen is to make it immutable 
str strip the whitespace 

any model that has a list of str should have the default factory of list
```python
missing_information: list[str] = Field(default_factory=list)
```

same for the uuid 
```python
evidence_id: UUID = Field(default_factory=uuid4)
```

```python
collected_at: datetime = Field(default_factory=utc_now)
```

the model validator of the mode its either before or after 
```python
@model_validator(mode = "after")
def final_decision(self) -> "ApprovalDecision":
	if self.status not in {
		ApprovalStatus.APPROVED,
		ApprovalStatus.REJECTED,
	}:
		raise ValueError(
			"An approval decision must be approved or rejected"
		)

	return self
```

currency is always min of 3 and the max of 3

Writiting the test for the domain models
assert is the same as if it returns true and false and checks for the infomartion you want to know 
```python
assert transaction.currrency == "USD"
```

with pytest is used when looking for a speicifc error that should arise from the wrong params or wrong runtime 

```python
with pytest.raises(ValidationError,match = "greater than 0"):
	Transaction(
            transaction_id="transaction-123",
            tenant_id="tenant-a",
            customer_id="customer-456",
            order_id="order-789",
            amount=Decimal("-50.00"),
            currency="USD",
            charged_at=datetime.now(UTC),
        )
```

---
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

---

## Refined engineering principles

> [!important] Core question
> How can ResolveFlow resolve a support case using evidence without allowing an AI model to perform an unauthorized or duplicated financial action?

### Start with behavior, not frameworks

```text
Written behavior
    -> typed domain model
    -> deterministic business core
    -> graph orchestration
    -> LLM decisions
    -> persistence and human approval
    -> API and streaming
    -> multi-tenancy and RAG
    -> evaluation and observability
    -> gateway, caching, and deployment
```

Before adding a feature, answer:

1. What user or system problem does this solve?
2. Why does it require an LLM?
3. What happens when it fails?
4. How will I test it?
5. What proves it is finished?

### Decision authority

| Authority | Responsibilities |
|---|---|
| LLM | Interpret language, classify intent, choose read-only evidence, ask for missing information, and propose an explanation |
| Deterministic code | Authentication, tenant filtering, transaction truth, duplicate detection, permissions, idempotency, and action execution |
| Human | Approve consequential actions and resolve uncertainty |

> [!tip] Rule of thumb
> If being wrong changes money, identity, permissions, or tenant boundaries, the LLM cannot be the final authority.

Related: [[Agent Guardrails]], [[Human-in-the-Loop (Approval & Interrupts)]], and [[Agent Handoffs And Tool Design]].

## Corrected implementation lessons

### `extra="forbid"`

`extra="forbid"` makes Pydantic reject fields that the schema does not define. This is useful for structured LLM output, but it is a schema-validation rule rather than a complete LLM guardrail.

### `default_factory`

```python
missing_information: list[str] = Field(default_factory=list)
evidence_id: UUID = Field(default_factory=uuid4)
collected_at: datetime = Field(default_factory=utc_now)
```

`default_factory` calls the function for each new model instance. Each instance receives its own list, UUID, or timestamp.

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

### Precise tests

A negative test should contain exactly one invalid condition. Every other field must be valid, or the test might pass because of the wrong error.

A valid-object test should construct the model normally:

```python
transaction = Transaction(...)
assert transaction.currency == "USD"
```

An exception test should name the expected error:

```python
with pytest.raises(ValidationError, match="greater than 0"):
    Transaction(...)
```

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

## Duplicate-detection rule

Two transactions are potential duplicates when they:

- Have different transaction IDs.
- Are both completed.
- Belong to the same tenant and customer.
- Have the same order ID, amount, and currency.
- Occur within the configured time window.

The detector sorts by `charged_at`, making the earlier transaction the original and the later transaction the duplicate. Normal non-matches return `None`; they are not exceptional failures.

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
