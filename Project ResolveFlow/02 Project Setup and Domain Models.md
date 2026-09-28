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
description: "uv/src layout, enums, immutable Pydantic domain models, validators, and domain-model tests."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 02 Project Setup and Domain Models

> Part of [[00 ResolveFlow Index]]. Previous: [[01 Planning and Engineering Principles]] · Next: [[03 Duplicate Detection]]

## Build notes

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

## Corrected lessons

### `extra="forbid"`

`extra="forbid"` makes Pydantic reject fields that the schema does not define. This is useful for structured LLM output, but it is a schema-validation rule rather than a complete LLM guardrail.

### `default_factory`

```python
missing_information: list[str] = Field(default_factory=list)
evidence_id: UUID = Field(default_factory=uuid4)
collected_at: datetime = Field(default_factory=utc_now)
```

`default_factory` calls the function for each new model instance. Each instance receives its own list, UUID, or timestamp.

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
