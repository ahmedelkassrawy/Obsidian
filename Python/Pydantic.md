---
tags: [python, pydantic, validation, data-modeling]
source: Track A · postqueue · Lesson 1
updated: 2026-08-17
---

# Pydantic (v2)

> Mental model: a Pydantic model is a **gate, not a bag**. A plain class holds whatever you put in it. A `BaseModel` only lets data become an object if it passes validation — bad data raises `ValidationError` **at construction**, not three functions later.

Pairs with the idea note [[#When to use Pydantic]] and the modeling instinct: *make illegal states unrepresentable* + *parse, don't validate*.

---

## When to use Pydantic

Reach for it whenever **data crosses a boundary** into your program and you want to trust it afterwards:

| Use case | Why Pydantic |
|---|---|
| **API request/response** (FastAPI) | Parse the JSON body into a typed model once; every handler downstream trusts it. This is what you already used. |
| **Config / settings** | `BaseSettings` reads env vars / `.env`, validates types, fails fast on bad config at startup. |
| **Parsing external JSON** (files, webhooks, 3rd-party APIs) | Turn a messy dict into a validated object; reject junk at the door. |
| **Domain objects with rules** | A `Post` whose caption length depends on platform — the rule lives in one place. |
| **LLM / tool outputs** | Validate that a model's JSON output matches the shape you expect before using it. |

### When NOT to use it
- A single open value with no rules and no fixed set → a plain variable/`str`. A model here is ceremony.
- Hot inner loops where you fully control the data and it's already typed → the validation cost isn't worth it.

**One-line test:** is there a *rule*, a *fixed set*, or a *clump* of fields that travel together? Any → model it. None → don't.

---

## BaseModel basics

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Post(BaseModel):
    id: int
    platform: Platform            # an Enum
    caption: str
    scheduled_at: datetime
    status: Status = Status.pending   # default -> field is optional at call site
```

Two things happen **for free** at the gate:
- **Coercion:** `"7"` → `7`; an ISO string `"2027-01-01T10:00"` → a real `datetime`.
- **Rejection:** `"banana"` for `scheduled_at` raises `ValidationError` — never gets in.

```python
Post(id=1, platform="x", caption="hi", scheduled_at="2027-01-01T10:00")  # kwargs
Post.model_validate(raw_dict)          # from a dict — the "front door"
Post.model_validate_json(json_string)  # straight from a JSON string
post.model_dump()                      # -> dict
post.model_dump_json()                 # -> JSON string
```

---

## Enums — closing the set of legal values

Use an `Enum` when a field's valid values are a **small, fixed, closed list** (the "dropdown vs text box" test). `platform: str` accepts `"instgram"`, `"MySpace"`, `""` — infinite mostly-wrong values. `platform: Platform` accepts exactly the members.

```python
class Platform(str, Enum):        # note the `str` mix-in
    instagram = "instagram"
    x = "x"
    facebook = "facebook"

class Status(str, Enum):
    pending = "pending"
    scheduled = "scheduled"
    cancelled = "cancelled"
```

**Why `class Platform(str, Enum)` and not just `Enum`?** The `str` mix-in makes each member *be* a string, so:
- it serializes to `"instagram"` in JSON with no extra work, and
- `platform == "instagram"` still works.

Plain `Enum` serializes as the enum object and needs extra handling. (Py 3.11+ also has `StrEnum` which does the same thing.)

Enum buys you three things a `str` can't: wrong values become **impossible**, right values become **autocompleted**, and the set has **one source of truth**.

---

## Field validators — rules on ONE field

```python
from pydantic import field_validator

class Post(BaseModel):
    caption: str
    scheduled_at: datetime

    @field_validator("caption", mode="before")
    @classmethod
    def strip_caption(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v

    @field_validator("scheduled_at", mode="after")
    @classmethod
    def must_be_future(cls, v: datetime) -> datetime:
        if v <= datetime.now(tz=v.tzinfo):
            raise ValueError("scheduled_at must be in the future")
        return v
```

Rules to **say aloud** (this is the Build-Twice gate):

| Piece | Why |
|---|---|
| `mode="before"` | runs on the **raw** input, before parsing/coercion. Use to **reshape** (trim, zero-pad, rename). |
| `mode="after"` | runs **after** Pydantic produced the typed value. Use to **check** an already-valid value (here, a real `datetime`). |
| `@classmethod` | validators run on the class, before an instance exists — no `self`. The value comes in as `v`. |
| `return v` | must return the value (changed or not). **Forget it → the field becomes `None`.** (#1 Pydantic bug.) |
| reject via `raise ValueError(...)` | Pydantic catches it and wraps into a `ValidationError`. Never raise `ValidationError` yourself. |

One validator, many fields: `@field_validator("f1", "f2")`.

Mnemonic: **reshape → before, check → after.**

---

## Model validators — rules across TWO+ fields

The rule "**caption length depends on platform**" needs `caption` AND `platform` at once. A `field_validator` only sees one field, so it *can't* express this. That's the whole reason `model_validator` exists.

```python
from typing import Self
from pydantic import model_validator

class Post(BaseModel):
    caption: str
    platform: Platform

    @model_validator(mode="after")
    def caption_within_platform_limit(self) -> Self:
        limits = {Platform.instagram: 2200, Platform.x: 280, Platform.facebook: 63206}
        if len(self.caption) > limits[self.platform]:
            raise ValueError(f"caption too long for {self.platform.value}")
        return self
```

- `mode="after"`: **instance method**, all fields already validated, takes `self`, returns `self`. The common one.
- `mode="before"`: `@classmethod` that gets the **raw input dict** before any field parsing; return the (reshaped) data.

---

## field_validator vs model_validator — the decision

> **Does the rule read more than one field?**
> - **One field** → `@field_validator("name", mode=...)` — classmethod, takes `v`, returns `v`.
> - **Two+ fields** → `@model_validator(mode="after")` — instance method, takes `self`, returns `self`.

| | `@field_validator` | `@model_validator(mode="after")` |
|---|---|---|
| Sees | one field's value `v` | the whole object `self` |
| Is a | `@classmethod` (no instance yet) | instance method (all fields set) |
| Returns | the value `v` | `self` |
| Use when | rule needs **1** field | rule needs **≥2** fields |

---

## Gotchas
- **Forgot `return`** → field silently becomes `None`.
- **Never `raise ValidationError`** inside a validator — raise `ValueError`; Pydantic packages it (and collects *all* failures into one error).
- **Cross-field rule in a field validator** is impossible — it only sees one field. Use a model validator.
- **Defaults aren't validated by default.** Set `model_config = ConfigDict(validate_default=True)` if you need them checked.
- **`datetime.now()` in a validator** — mind timezones. Compare against `datetime.now(tz=v.tzinfo)` when the field may be tz-aware.

---

## Full worked example — the `postqueue` `Post`

```python
from datetime import datetime
from enum import Enum
from typing import Self
from pydantic import BaseModel, field_validator, model_validator

class Platform(str, Enum):
    instagram = "instagram"
    x = "x"
    facebook = "facebook"

class Status(str, Enum):
    pending = "pending"
    scheduled = "scheduled"
    cancelled = "cancelled"

class Post(BaseModel):
    id: int
    platform: Platform
    caption: str
    scheduled_at: datetime
    status: Status = Status.pending

    @field_validator("caption", mode="before")
    @classmethod
    def strip_caption(cls, v: str) -> str:
        return v.strip() if isinstance(v, str) else v

    @field_validator("scheduled_at", mode="after")
    @classmethod
    def must_be_future(cls, v: datetime) -> datetime:
        if v <= datetime.now(tz=v.tzinfo):
            raise ValueError("scheduled_at must be in the future")
        return v

    @model_validator(mode="after")
    def caption_within_platform_limit(self) -> Self:
        limits = {Platform.instagram: 2200, Platform.x: 280, Platform.facebook: 63206}
        if len(self.caption) > limits[self.platform]:
            raise ValueError(f"caption too long for {self.platform.value}")
        return self
```

---

## Quick reference

```
Model = gate: data becomes the object only if valid; else ValidationError at build time.
Enum         -> field is one of a small fixed closed set (dropdown).
str/int      -> open-ended value, no rule.
+ validator  -> open but constrained (range, non-empty, future).
nested model -> field is itself a compound thing.

field_validator  -> 1 field  | @classmethod | (cls, v) -> v   | before=reshape / after=check
model_validator  -> 2+ fields | instance     | (self)  -> self | usually mode="after"
reject -> raise ValueError   (Pydantic wraps into ValidationError)
always -> return the value / self
```

**Sources:** [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/) · [Models](https://docs.pydantic.dev/latest/concepts/models/) · [Parse, don't validate (King)](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) · Lesson HTML: `D:\me\teach\lessons\0003-pydantic-post-model.html`
