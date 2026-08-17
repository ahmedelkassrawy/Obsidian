---
tags: [python, testing, pytest, pydantic, validation]
source: Track A · postqueue · Day 1 (pytest for Pydantic models)
updated: 2026-08-17
---

# Testing with pytest (validation-focused)

> The habit that matters: **a model that *constructs* fine proves nothing.** You only know a validator works when you watch **bad data get rejected.** Test the rejections, not just the happy path.

Companion to [[Pydantic]] and [[Data Modeling]]. This note is the testing muscle for Track A.

---

## 1. pytest basics

- pytest auto-discovers files named `test_*.py` and functions named `test_*`.
- A test **passes if it does not raise.** Use `assert` to check values.
- Run: `uv run pytest -q`  (`-q` = quiet; `-v` = verbose per-test).

```python
def test_default_status_is_pending() -> None:   # -> None required under mypy --strict
    post = Post(id=1, platform=Platform.x, caption="hi", scheduled_at=FUTURE)
    assert post.status == Status.pending
```

Write `assert x == y`, **not** `assert(x == y)` — `assert` is a statement, not a function; the parens are misleading (and can hide a bug if you write `assert (x, y)`, which is always truthy).

---

## 2. Testing that BAD input is rejected — `pytest.raises`

The key move. Flip the assertion: the test passes **only if** the block raises.

```python
import pytest
from pydantic import ValidationError

def test_past_date_is_rejected() -> None:
    with pytest.raises(ValidationError, match="future"):
        Post(id=1, platform=Platform.x, caption="hi", scheduled_at=PAST)
```

- If the `Post(...)` does **not** raise, the test **fails** — this is what catches a silently-broken validator (exactly the decorator-order bug where validators stopped firing).
- `match="future"` asserts the **right rule** fired, not just any error. `match` is a **regex searched against the error string**. Match on a stable word that's actually in *your* message.
- **Trap:** the `Post(...)` call must be **inside** the `with` block. If you build it outside, the exception escapes and the test *errors* instead of passing.

---

## 3. Isolate the variable — the #1 test-design rule

A good test builds a **complete valid baseline** and breaks **exactly one thing**. If a test omits required fields, the error is about the *missing fields*, not the rule you meant to test.

```python
# BAD: missing id + platform -> error is "Field required", not the rule
with pytest.raises(ValidationError, match="future"):
    Post(scheduled_at=PAST)            # noise, not a real test of the future rule

# GOOD: everything valid, only scheduled_at is wrong
with pytest.raises(ValidationError, match="future"):
    Post(id=1, platform=Platform.x, caption="hi", scheduled_at=PAST)
```

A tiny factory keeps this clean when you have many tests:

```python
def valid_kwargs(**overrides):
    base = dict(id=1, platform=Platform.instagram, caption="hi", scheduled_at=FUTURE)
    return {**base, **overrides}

Post(**valid_kwargs(caption="  hi  "))               # test strip
Post(**valid_kwargs(scheduled_at=PAST))              # test future rule
Post(**valid_kwargs(platform=Platform.x, caption="a"*300))  # test caption limit
```

---

## 4. GOTCHA: `@model_validator(mode="after")` only runs if the fields are valid

An **after** model validator runs **after** every field has already validated. So if a required field is missing (or a field validator fails), the model validator **never runs** — its rule can't fire.

That's why a caption-limit test on an incomplete `Post` fails: field validation errors (missing `id`/`scheduled_at`) short-circuit, the caption-limit check never executes, and `match="too long"` finds nothing. **Fix:** make everything else valid; break only the caption.

---

## 5. GOTCHA: Pydantic runtime coercion vs mypy static types

At **runtime**, Pydantic coerces `"2020-01-01T10:00"` (str) into a `datetime`. At **type-check time**, `mypy --strict` sees the field is declared `datetime` and flags passing a `str`:

```
Argument "scheduled_at" to "Post" has incompatible type "str"; expected "datetime"
```

mypy doesn't know about Pydantic's coercion — two different truths. **Fix in tests:** pass real `datetime`s, not strings. Cleaner anyway, and it kills the error. (This exact tension shows up all over FastAPI code.)

---

## 6. Test hygiene checklist (mypy --strict + ruff clean)

- [ ] Every test function annotated `-> None` (strict requires a return type on all functions).
- [ ] Use real `datetime`s, not string literals (satisfies mypy + reads better).
- [ ] `datetime.now(tz=UTC)` — timezone-aware; ruff flags naive `datetime.now()`. (`from datetime import UTC` on 3.11+, else `timezone.utc`.)
- [ ] Dates that must stay future/past: `now ± timedelta(...)`, **not** a hardcoded date — a literal like `"2027-01-01"` silently starts passing wrong once that date arrives (**test rot**).
- [ ] The `Post(...)` under test sits **inside** the `pytest.raises` block.
- [ ] `assert x == y`, not `assert(x == y)`.

Run all three green:
```
uv run pytest -q
uv run mypy --strict models.py test_models.py
uv run ruff check models.py test_models.py
```

---

## Worked example (postqueue Day 1)

```python
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from models import Platform, Post, Status

_NOW = datetime.now(tz=UTC)
FUTURE = _NOW + timedelta(days=1)   # always valid, never rots
PAST = _NOW - timedelta(days=1)


def test_valid_post_constructs_and_strips() -> None:
    post = Post(id=3, platform=Platform.facebook, scheduled_at=FUTURE, caption="  hi  ")
    assert post.status == Status.pending   # default kicked in
    assert post.caption == "hi"            # before-validator stripped it


def test_past_date_is_rejected() -> None:
    with pytest.raises(ValidationError, match="future"):
        Post(id=4, platform=Platform.instagram, caption="loooong", scheduled_at=PAST)


def test_caption_too_long_for_x_is_rejected() -> None:
    with pytest.raises(ValidationError, match="too long"):
        Post(id=5, platform=Platform.x, scheduled_at=FUTURE, caption="a" * 300)
```

---

## Quick reference

```
discover : files test_*.py, functions test_*        run: uv run pytest -q
pass     : test does not raise; use assert for values
reject   : with pytest.raises(ExcType, match="regex"): <call under test inside>
isolate  : complete valid baseline, change ONE thing (a valid_kwargs factory helps)
gotcha 1 : model_validator(after) runs only if all fields already valid
gotcha 2 : Pydantic coerces str->datetime at runtime, but mypy wants the real type
hygiene  : -> None on tests | real datetimes | now(tz=UTC) | now±timedelta (no rot)
mantra   : a model that constructs proves nothing — test the rejections
```

**Sources:** [pytest docs](https://docs.pytest.org/en/stable/) · [pytest.raises](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions) · [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/) · Lesson context: `D:\me\teach\postqueue\test_models.py`
