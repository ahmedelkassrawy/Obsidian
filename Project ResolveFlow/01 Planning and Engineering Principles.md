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
description: "CEO brief, vertical slice, agent justification, authority boundaries, first state design, and engineering principles."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 01 Planning and Engineering Principles

> Part of [[00 ResolveFlow Index]]. Previous: — · Next: [[02 Project Setup and Domain Models]]

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
