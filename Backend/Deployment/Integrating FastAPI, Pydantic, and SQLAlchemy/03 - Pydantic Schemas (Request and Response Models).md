---
tags: [pydantic, schemas, from_attributes, orm_mode, request-model, response-model]
aliases: [Pydantic schemas, UserCreate, UserResponse, ProductCreate, ProductResponse, from_attributes, orm_mode]
source: https://github.com/h9-tec/AI_deployment#database-session-dependency
---

# 03 — Pydantic Schemas (Request and Response Models)

> [!info] Source
> Code block under https://github.com/h9-tec/AI_deployment#database-session-dependency (the first half of `main_integrated.py`).
> Back to [[00 - Index]] · Previous: [[02 - Database Session Dependency (get_db)]]

## The one-sentence version

You write **four** small Pydantic classes — two describing what the client **sends** (`...Create`) and two describing what the API **returns** (`...Response`) — and the `Response` ones carry `from_attributes = True` so they can be built straight from SQLAlchemy objects.

## The code (top of `main_integrated.py`)

```python
# main_integrated.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import Pydantic models (from models.py or models_orm.py if you prefer)
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True # Pydantic V2: orm_mode = True in Pydantic V1

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    owner_id: int

    class Config:
        from_attributes = True # Pydantic V2: orm_mode = True in Pydantic V1

# Import SQLAlchemy ORM models and session setup
from models_orm import Base, User, Product, engine
from database_orm import get_db # This is our dependency

# Create all tables (run once)
Base.metadata.create_all(bind=engine)

app = FastAPI()
```

## The imports, one by one

| Import | Why it's there |
|---|---|
| `FastAPI` | The app object. |
| `Depends` | Wires `get_db` into endpoints ([[02 - Database Session Dependency (get_db)]]). |
| `HTTPException` | Raise it to return a 4xx/5xx with a JSON `{"detail": ...}` body. |
| `status` | Named constants like `status.HTTP_201_CREATED` instead of magic numbers. |
| `Session` (from `sqlalchemy.orm`) | Type hint for the `db` parameter. |
| `List` (from `typing`) | For `response_model=List[UserResponse]`. On Python ≥3.9 you can write `list[UserResponse]` instead. |
| `BaseModel` | Parent class for every Pydantic schema. |
| `Base, User, Product, engine` (from `models_orm`) | The SQLAlchemy side: table metadata, the two ORM classes, the DB engine. |
| `get_db` (from `database_orm`) | The session dependency. |

## The four schemas

### `UserCreate` — what the client sends to make a user

```python
class UserCreate(BaseModel):
    username: str
    email: str
```

- Both fields **required** (no default).
- No `id` — the database assigns it. If a client sends one, Pydantic ignores it by default.
- No `Config` needed: request bodies arrive as JSON dicts, which Pydantic reads natively.

### `UserResponse` — what the API sends back

```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
```

- Now **includes `id`**, because after insert we know it.
- `from_attributes = True` is the key line — see below.

### `ProductCreate` — what the client sends to make a product

```python
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
```

- `description: str | None = None` — optional. Client can omit it, send `null`, or send a string. (`str | None` is Python 3.10+ syntax; on 3.9 use `Optional[str]`.)
- **No `owner_id`** — it comes from the URL (`/users/{user_id}/products/`), not the body. This prevents a client from attaching a product to someone else's account by editing the JSON.

### `ProductResponse` — what the API sends back

```python
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    owner_id: int

    class Config:
        from_attributes = True
```

- Includes `id` **and** `owner_id` so the client can see which user owns it.

## `from_attributes = True` — the line everyone asks about

### The problem it solves

By default, Pydantic builds a model from a **dict**: `UserResponse(**{"id": 1, "username": "ada", ...})`.

But your endpoint returns a **SQLAlchemy `User` object**. It has `.id`, `.username`, `.email` as *attributes*, not dict keys. Pydantic would fail: "expected dict, got User".

### What the flag does

`from_attributes = True` tells Pydantic: *"If I'm handed an arbitrary object, read the fields off its attributes with `getattr()`."* So `UserResponse.model_validate(user_orm_obj)` works, and FastAPI does exactly that behind `response_model=`.

### Pydantic V1 vs V2 naming

| Pydantic version | Setting | Where |
|---|---|---|
| V1 | `orm_mode = True` | `class Config:` |
| V2 (current) | `from_attributes = True` | `class Config:` **or** `model_config = ConfigDict(from_attributes=True)` |

The README uses the `class Config:` form with the V2 name. Modern V2 style prefers:

```python
from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
```

Both work in V2; `class Config` emits a deprecation warning in newer V2 releases.

### Why only on `Response` models?

Because only responses are built from ORM objects. Request bodies come from JSON → dict, where the default works. Adding it to `Create` models does no harm, it's just unnecessary.

## `Base.metadata.create_all(bind=engine)`

- Looks at every class that inherited from `Base` (`User`, `Product`) and issues `CREATE TABLE IF NOT EXISTS` for each.
- Safe to run repeatedly — it **won't** alter existing tables (so it will **not** add a new column you added to a model later; that's what Alembic migrations are for, covered in §7/§9 of the README).
- Runs at import time here, which is fine for a demo. In a real app you'd do it in a startup/lifespan hook or leave it to migrations.

## Naming conventions worth copying

| Suffix | Direction | Contains `id`? | `from_attributes`? |
|---|---|---|---|
| `XCreate` | client → API | no | no |
| `XUpdate` (not in README) | client → API, all fields optional | no | no |
| `XResponse` / `XRead` / `XOut` | API → client | yes | **yes** |

## Next

→ [[04 - API Endpoints with Database Operations]]
