---
tags: [fastapi, sqlalchemy, dependency-injection, session, get_db]
aliases: [get_db, Database session dependency, Depends(get_db), Session per request]
source: https://github.com/h9-tec/AI_deployment#database-session-dependency
---

# 02 — Database Session Dependency (`get_db`)

> [!info] Source
> https://github.com/h9-tec/AI_deployment#database-session-dependency
> Back to [[00 - Index]] · Previous: [[01 - Overview and Project Layout]]
> Deeper SQLAlchemy background on sessions: [[Backend/SQLAlchemy/05 - Sessions and sessionmaker|SQLAlchemy › 05 - Sessions and sessionmaker]]

## The one-sentence version

`get_db` is a tiny generator function that **opens a SQLAlchemy session, hands it to your endpoint, and guarantees it gets closed afterwards** — and FastAPI's `Depends()` is what calls it for you on every request.

## What the README says

> FastAPI's dependency injection system is perfect for managing database sessions. We'll create a dependency that provides a database session for each request and ensures it's closed afterward.
>
> First, ensure you have your `database_orm.py` and `models_orm.py` set up as described in the previous sections. We'll use the `get_db` function from `database_orm.py` as a dependency.

## The code (from `database_orm.py`, README §5)

```python
# database_orm.py

from sqlalchemy.orm import sessionmaker
from models_orm import engine, Base

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables (run this once to set up your database)
# Base.metadata.create_all(engine)
```

## Line by line

### `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`

- `sessionmaker(...)` is a **factory**. It doesn't open a session; it builds a *class* that, when called, produces a session.
- `bind=engine` — every session made by this factory talks to the `engine` defined in `models_orm.py` (SQLite file `./test_orm.db` in the README).
- `autocommit=False` — nothing is written until **you** call `db.commit()`. This is what you want for a web API: either the whole endpoint's work lands, or none of it.
- `autoflush=False` — SQLAlchemy won't silently push pending `add()`s to the DB before every query. Makes behaviour more predictable; you flush/commit explicitly.
- Naming convention: `SessionLocal` (capital S) because it's a class-like factory, not an instance.

### `def get_db():` with `yield`

This is a **generator**, and FastAPI treats generator dependencies specially:

| Step | What runs | When |
|---|---|---|
| 1 | `db = SessionLocal()` — open a session | Before your endpoint function starts |
| 2 | `yield db` — hand the session to the endpoint | The endpoint runs with `db` as its parameter |
| 3 | `finally: db.close()` — release the connection | After the response is built, **even if the endpoint raised** |

The `try/finally` is the important part. Without it, an exception in the endpoint would leave a session (and a pooled DB connection) dangling. With SQLite it's mostly harmless; with Postgres in production, leaked connections eventually exhaust the pool and the app hangs.

### Why a session **per request**, not one global session?

- A `Session` is **not thread-safe** and holds transaction state. Sharing one across concurrent requests mixes up their transactions.
- Per-request sessions are cheap: `SessionLocal()` checks a connection out of the engine's pool, `close()` checks it back in. No new TCP connection each time.
- It also gives you a clean unit of work: one request = one transaction boundary.

## How it's used in `main_integrated.py`

```python
from sqlalchemy.orm import Session
from fastapi import Depends
from database_orm import get_db

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    ...
```

- `db: Session` — the type hint is just for your editor/IDE. FastAPI doesn't need it to work, but it makes autocomplete on `db.query`, `db.add` etc. work.
- `= Depends(get_db)` — tells FastAPI: "before calling `read_user`, call `get_db()`, take what it yields, and pass it as `db`."
- You **never** call `get_db()` yourself inside the endpoint. If you do, you'll get a generator object, not a session (see [[08 - Gotchas and Troubleshooting]]).

## Mental model: `Depends` is a plug socket

Think of `Depends(get_db)` as a socket on the wall. FastAPI plugs a fresh session in right before your function runs and unplugs it right after. The endpoint doesn't know or care *how* the session was made; it just uses it. That's why the same `get_db` can be:

- swapped for an in-memory SQLite session in tests (`app.dependency_overrides[get_db] = override_get_db`),
- swapped for an async version later (`get_async_db` in [[Advanced Topics and Best Practices]]),
- reused across dozens of endpoints with zero duplicated setup/teardown code.

## Common variations you'll see in the wild

| Variation | Looks like | Notes |
|---|---|---|
| Context-manager style | `with SessionLocal() as db: yield db` | SQLAlchemy ≥1.4. Same effect as try/finally. |
| Commit-on-success | `try: yield db; db.commit() except: db.rollback(); raise finally: db.close()` | Auto-commits if the endpoint didn't raise. Saves writing `db.commit()` everywhere but hides when writes happen. |
| Async | `async def get_async_db(): async with AsyncSessionLocal() as s: yield s` | Covered in §7 of the README. |
| Typed alias | `DB = Annotated[Session, Depends(get_db)]` then `db: DB` | FastAPI ≥0.95. Cleaner signatures. |

## Next

→ [[03 - Pydantic Schemas (Request and Response Models)]]
