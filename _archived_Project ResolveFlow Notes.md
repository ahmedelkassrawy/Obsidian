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
- [[#API layer (FastAPI over the graph)]]
- [[#RefundService — lessons to reuse]]
- [[#LangGraph — lessons to reuse]]
- [[#Mistakes worth remembering]]
- [[#Every-build checklist]]

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

- Rejects unexpected fields.
- Removes surrounding whitespace.
- Freezes objects after creation.
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


The models we introduced till now are 
- Transaction -> record a customer charge
- Evidence -> traceble fact supporting an action
- ProposedAction -> Something resolveflow wants to execute
- - ApprovalDecision ->  a reviewer’s final decision for one exact action.
- ActionResult -> he result of executing an action.
- RefundReceipt ->  the billing provider’s record of a refund.

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

### 2026-09-28 — FastAPI layer over the graph

- Learned that a returned `JSONResponse` skips `response_model` validation, and that `model_dump(mode="json")` is needed only when data goes over the wire.
- Learned that `__interrupt__` exists only in the `invoke()` return value; saved state uses `snapshot.next`.
- Derived API status and message from graph state; check handoff before errors.
- Learned that `async def` + sync `invoke()` blocks the event loop; switched to `def`.
- Added the approval endpoint with a `snapshot.next` guard and a structured resume that records the real reviewer.
- Learned that passing tests are not proof: a fix needs an assertion that would fail without it.

---
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

The duplicate detection system 
it recieves
- a sequence of transactions
- a time window supplied by the caller

it then:
1. Sort transactions chronologically 
2. compares each charge with later cahrges
3. requires matching tenant and customer and order and amount and currency
4. checks whether the charges occurred within the allowed window
5. returns the first mathcing pair as DuplicatedCHargedFinding
6. Returns `None` if no duplicate exists.

The graph currently supplies a five-minute window, meaning the general duplicate detector does not own that policy—the orchestration layer does.

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

Orchestration of Langgraph
```
state.py     What data moves through the workflow?
nodes.py     What work happens?
routes.py    Where does execution go next?
builder.py   How is the complete graph assembled?
```

Reducers
`errors` uses list addition
```python
errors: Annotated[list[str], operator.add]
```

```python
{
	"errors": [
		"There is soemthing wrong at"
	]
}
```

A workflow can accumulate many messages, evidence records and events, but it has one current proposal, decision and result.

The routes 
```
After validation
├── errors → END
└── valid → load_transactions

After detection
├── no duplicate → END
└── duplicate → create_evidence

After approval
├── approved → execute_action
└── rejected → END
```

```python
def route_after_validation(state:ResolveFlowState):
    if state.get("errors"):
        return "end"
        
    return "load_transactions"

def route_after_detection(state:ResolveFlowState):
    if state.get("duplicate_finding") is None:
        return "end"
        
    return "create_evidence"

def route_after_approval(state:ResolveFlowState):
    decision = state.get("approval_decision")

    if (decision is not None and decision.status == ApprovalStatus.APPROVED):
        return "execute_action"
        
    return "end"
```

Conditional edges
```python
graph.add_conditional_edges(
        "request_approval",
        route_after_approval,
        {
            "execute_action": "execute_action",
            "end" : END
      
```

Workflow Diagram
```
flowchart TD
    A[Initial ticket state] --> B[Validate request]

    B -->|missing fields| Z[END with errors]
    B -->|valid| C[Load tenant and customer transactions]

    C --> D[Detect duplicate within five minutes]

    D -->|not found| N[Add no-duplicate message]
    N --> Z

    D -->|found| E[Create evidence]
    E --> F[Create pending refund proposal]
    F --> G[Interrupt for human approval]

    G -->|rejected| Z
    G -->|approved| H[RefundService checks authorization]
    H --> I[Billing gateway checks provider rules]
    I --> J[Receipt and refunded transaction]
    J --> K[Successful ActionResult]
    K --> Z
```

---
Ticket intake and intent routing
message should be clasiifeied into 3 categouries
- Duplicate charges -> refund workflow
- Billing question -> billing path
- Human Support -> low confidnece or an supported intent

---

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
> Correction: a classifier that **raises** (LLM timeout, bad output) does not add to `errors`. The exception aborts the run. See [[#An exception is not a route]].

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

### Next: `GET /tickets/{ticket_id}`

- 404 check uses `snapshot.values` (empty for unknown IDs). A finished ticket has values but no `next`, and it must return 200.
- Pause check uses `snapshot.next`, not `"__interrupt__"`.
- Returns 200 even while waiting. The 202 on POST meant "accepted, not finished." A GET succeeded at reading; the `status` field carries the waiting state.
- Security gap for later: anyone with a `ticket_id` can read the ticket. A real system checks the caller's tenant against `tenant_id`.

---

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

---

## LangGraph — lessons to reuse

### Nodes return partial updates, reducers decide how they merge

A node returns only the keys it changes. The state's annotations decide what happens next:

| Field | Annotation | Returning `{"x": v}` does |
|---|---|---|
| `messages` | `add_messages` | Appends (and replaces by message ID) |
| `errors`, `evidence`, `trajectory` | `operator.add` | Appends the list |
| `step_count` | `operator.add` on `int` | Adds, so returning `1` is a counter |
| `proposed_action`, `action_result` | none | Overwrites |

> [!tip] Rule
> Accumulating things (messages, evidence, errors, events) get a reducer. Things that have "one current value" (proposal, decision, result) do not.

### Missing keys are normal

`TypedDict` does not create defaults. A key a node never wrote simply does not exist:

```python
assert "action_result" not in final_state   # rejected path
state.get("proposed_action")                 # not state["proposed_action"]
```

Use `.get()` for anything a path might skip. This is the same lesson as `__interrupt__` in the API.

### `trajectory` is a test tool

Every node appends its name. Asserting the exact list proves the **path**, not just the result:

```python
assert final_state["trajectory"] == ["validate_request", "classify_intent", ..., "request_approval"]
```

A test that only checks the final answer can pass while the graph took the wrong route.

### Injecting dependencies into nodes

A node is called with `state` only. Extra dependencies are bound in the builder:

```python
graph.add_node("classify_intent", partial(classify_intent, classifier=classifier))
graph.add_node("execute_action", lambda state: execute_action(state, refund_service))
```

Both work. `partial` is slightly better: it keeps the function's name and cannot capture the wrong variable later (lambdas in a loop bind late). The real win is `build_refund_graph(gateway, classifier)`: tests pass a fake, production passes the real one, and no node imports a global.

> [!note] Fakes do not need inheritance
> `FakeIntentClassifier` does not subclass `IntentClassifier`. It only has a `classify_intent(message)` method that returns a `TicketIntent`. Python only cares that the method exists (duck typing).

### Routes are pure functions that return labels

```python
def route_after_intent(state) -> str:
    ...
    return "human_handoff"   # the last line is the safe default
```

- A route reads state and returns a label. The `path_map` in `add_conditional_edges` maps labels to nodes, so labels like `"end"` stay stable even if node names change.
- Pure functions are unit-testable without building a graph.
- **The fall-through default goes to the safest path.** Anything unknown, missing, or below the threshold ends in human handoff.
- Policy numbers (confidence `0.75`, the five-minute window) live in the orchestration layer, not in the general-purpose service.

### `interrupt()`: how pausing really works

```python
answer = interrupt({"question": "...", "action": proposed_action.model_dump(mode="json")})
```

- Requires a **checkpointer** and a **`thread_id`**. Without them there is nothing to resume.
- The dict passed to `interrupt()` is what the reviewer sees. Make it JSON-safe.
- The value in `Command(resume=...)` becomes the **return value** of `interrupt()`.

> [!warning] On resume, the node runs again from its first line
> LangGraph does not continue from the middle of the function. It re-executes `request_approval` from the top, and this time `interrupt()` returns the resume value instead of pausing. So **never put a side effect before `interrupt()`** (no refund, no email, no DB write). Everything above it will run twice. Here it only reads state, so it is safe.

### `InMemorySaver` is for learning

Checkpoints live in process memory. A server restart loses every paused ticket, and two server processes do not share them. Production needs a persistent saver (for example Postgres). Keep this in mind before calling the approval flow "done."

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

---

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
- Would this test fail if my fix were removed?