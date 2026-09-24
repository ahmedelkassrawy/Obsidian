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

