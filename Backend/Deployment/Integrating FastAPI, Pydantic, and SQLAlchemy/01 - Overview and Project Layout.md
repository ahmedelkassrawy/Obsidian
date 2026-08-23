---
tags: [fastapi, pydantic, sqlalchemy, architecture, overview]
aliases: [Integration overview, Project layout, How the three libraries fit together]
source: https://github.com/h9-tec/AI_deployment#6-integrating-fastapi-pydantic-and-sqlalchemy
---

# 01 — Overview and Project Layout

> [!info] Source
> https://github.com/h9-tec/AI_deployment#6-integrating-fastapi-pydantic-and-sqlalchemy
> Back to [[00 - Index]].

## What the section is trying to show

The original text says:

> This section brings together FastAPI, Pydantic, and SQLAlchemy to build a complete, functional API. We will demonstrate how to manage database sessions using FastAPI's dependency injection system and how to use Pydantic models for both request validation and response serialization.

In plain English: you already know the three tools on their own. Now you build **one** small app where:

- **FastAPI** receives the HTTP request and sends back the HTTP response.
- **Pydantic** checks the JSON coming *in* and shapes the JSON going *out*.
- **SQLAlchemy** reads and writes the actual database rows.

## Who does what (responsibility map)

| Layer | Library | Job | Lives in |
|---|---|---|---|
| HTTP / routing | FastAPI | Match URL + method to a Python function, inject dependencies, return JSON | `main_integrated.py` |
| Validation / serialization | Pydantic | Define the *shape* of request bodies and responses, reject bad input, convert ORM objects → JSON | `main_integrated.py` (or a separate `schemas.py`) |
| Persistence | SQLAlchemy ORM | Define tables as classes, open sessions, run queries, commit transactions | `models_orm.py`, `database_orm.py` |

## The request lifecycle (one POST, start to finish)

```
client sends  POST /users/  {"username": "ada", "email": "ada@x.com"}
        |
        v
FastAPI matches the route -> sees `user: UserCreate` -> hands the JSON to Pydantic
        |
        v
Pydantic validates against UserCreate (both fields present? both strings?)
   |-- invalid -> FastAPI returns HTTP 422 with a clear error; your function never runs
   '-- valid   -> continues
        |
        v
FastAPI sees `db: Session = Depends(get_db)` -> calls get_db() -> gets a fresh SQLAlchemy Session
        |
        v
Your function runs: builds a User ORM object, db.add, db.commit, db.refresh, returns the ORM object
        |
        v
FastAPI sees `response_model=UserResponse` -> hands the ORM object to Pydantic
        |
        v
Pydantic (because from_attributes=True) reads .id, .username, .email off the object -> JSON
        |
        v
FastAPI returns  201 Created  {"id": 1, "username": "ada", "email": "ada@x.com"}
        |
        v
get_db's `finally: db.close()` runs -> session returned to the pool
```

Keep this picture in your head; every later note is just zooming in on one arrow.

## Files involved

The section assumes two files **already exist** from sections 4–5 of the README:

| File | Purpose | Defined in README section |
|---|---|---|
| `models_orm.py` | `engine`, `Base`, and the `User` / `Product` ORM classes | §5 "Defining ORM Models" |
| `database_orm.py` | `SessionLocal` factory and the `get_db` dependency | §5 "Session Management" |

And it creates one new file:

| File | Purpose |
|---|---|
| `main_integrated.py` | Pydantic schemas + FastAPI app + all endpoints |

> [!tip] The original note split the code into `schemas.py` and `main.py`
> The README keeps everything in `main_integrated.py`. The archived note in this folder labelled the two halves `schemas.py` and `main.py`. Both layouts work — just keep imports consistent. [[07 - Full Source Listing (copy-paste ready)]] shows both the single-file version and a clean multi-file split.

## Data model being built

Two tables, one relationship:

```
users                       products
-----                       --------
id        (PK)      <---+   id           (PK)
username  (unique)      |   name         (unique)
email     (unique)      |   description  (nullable)
                        |   price
                        +-- owner_id     (FK -> users.id)
```

- One **User** owns many **Products** (`User.products` ↔ `Product.owner`).
- A product **must** have an owner, so it's created through `POST /users/{user_id}/products/`.

## Endpoints that will exist when you're done

| Method | Path | Does |
|---|---|---|
| `POST` | `/users/` | Create a user |
| `GET` | `/users/` | List users (paginated) |
| `GET` | `/users/{user_id}` | Get one user or 404 |
| `POST` | `/users/{user_id}/products/` | Create a product owned by that user |
| `GET` | `/products/` | List products (paginated) |
| `GET` | `/products/{product_id}` | Get one product or 404 |

## Next

→ [[02 - Database Session Dependency (get_db)]]
