## CEO Brief

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

