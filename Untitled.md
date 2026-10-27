Customer
  → POST /tickets
  → API reads tenant_id, customer_id, message
  → API creates ticket_id
  → API starts workflow with initial state
  → Workflow validates required data
  → AI classifies the intent

FAQ / Billing Question
-> retrieve the tenants policy
-> prepare evidence

Duplicate Charge
-> request this tenant/customer's transaction from billing
-> determinstic check for a duplicate

-> if no duplciate:
	AI recieves that no duplciate was found and explain that to user
	 end workflow

-> if duplicate exists:
	retrieve the tenant's refund policy
	 evidence based on the transaction + policy

-> if policy missing 
	escalate to human

-> if evidence support a refund 
	propose refund
	 request human approval
-> if rejected 
	we inform the customer
-> if approved:
	the refund goes through the billing system 
	save the transaction 
	inform the customer

Customer asking for a return of item
-> ask billing system for the date of the transaction
-> read the policy of return 
-> (if its elligble) return to customer with the issue id and the policy and approval that will be handled
-> Add to DB returns as a new return with having the tenant_id, customer_id, ticket_id, return_id and the item returned

Asking for a specific item in the website or shop
-> API takes it at the question endpoint
-> endpoint validates the input question and the customer id and the tenant 
-> API tells the workflow to then query the DB , tenants values and start
-> The response from db then returned to the AI to be better explainable to the user 

Unkown or low confidence intent -> human suport or escalation


C1: 
Users
- End customer -> submits a support problem and recieves response
- Human Reviewer -> accept/reject the escalated tickets
- Tenant Adminstrator -> configure the tenant and provides company policies

External Dependencies
- Billing system
- COmpany Policies
- LLM provider

```text
                     Tenant Administrator
                      policies/configuration
                              │
                              ▼
End Customer ────────► [ ResolveFlow ] ◄──────► LLM Provider
 support request          │       │
 response/status          │       └───────────► Tenant Billing System
                          │                    transactions/refunds
                          ▼
                  Human Support Reviewer
                  evidence and approval

```

for the C2:
```text
                   ResolveFlow boundary
┌────────────────────────────────────────────────┐
│                                                │
│  ResolveFlow Backend  ◄────► PostgreSQL        │
│  FastAPI + LangGraph          + pgvector       │
│                                                │
└────────────────────────────────────────────────┘
          │             │              │
          ▼             ▼              ▼
      LLM API      Embedding API   Billing API

```


Ticket
- ticket_id
- tenant_id
- customer_id
- initial_message
- status
- reported_transaction_id: optional
- created_at
- updated_at

Evidence
- evidence id
- tenant id
- ticket id
- evidence type
- source sytem 
- source id
- summary 
- collected at

no cutosmer id becuase we already have the ticket id which points to the customer
evidence type : Transaction - policy evidence
source type -> either billing system - policy store
source id -> the id from the source we used
summary: preserves the evidence we got

example: 
```text
Transaction evidence
- evidence_type: TRANSACTION
- source_system: BILLING
- source_id: tx-2
- summary: "tx-1 and tx-2 charged $100 for order-1 within two minutes"

Policy evidence
- evidence_type: REFUND_POLICY
- source_system: POLICY_STORE
- source_id: chunk-42
- summary: "Confirmed duplicate charges are eligible for refund"
```


