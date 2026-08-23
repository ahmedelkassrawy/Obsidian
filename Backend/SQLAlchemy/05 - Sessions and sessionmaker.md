---
tags: [sqlalchemy, orm, session, sessionmaker, get_db, transaction, unit-of-work]
aliases: [Sessions, sessionmaker, SessionLocal, get_db, Session lifecycle, expire_on_commit]
source: https://github.com/h9-tec/AI_deployment#session-management
---

# 05 — Sessions and `sessionmaker`

> [!info] Source
> README §5 "Session Management". Back to [[00 - Index]] · Previous: [[04 - ORM Models (declarative_base)]]
> The FastAPI-specific angle (`Depends(get_db)`) is in [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/02 - Database Session Dependency (get_db)|Integrating › 02 - Database Session Dependency]].

## The one-sentence version

A `Session` is the ORM's **unit of work**: it tracks the objects you load/add/change and turns them into SQL at `flush`/`commit`. `sessionmaker` is the factory that makes sessions bound to your engine.

## The code

```python
# database_orm.py
from sqlalchemy.orm import sessionmaker
from models_orm import engine, Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base.metadata.create_all(engine)   # run once
```

## `sessionmaker(...)` arguments

| Arg | Value | Meaning |
|---|---|---|
| `bind=engine` | required | Which engine sessions connect through. |
| `autocommit=False` | default | Changes only persist on explicit `commit()`. (`autocommit=True` is removed in 2.x anyway.) |
| `autoflush=False` | README choice | Don't auto-`flush` pending changes before each query. Default is `True`. With `False` you control exactly when SQL is sent; with `True` a query after `db.add(x)` would see `x` in results. |
| `expire_on_commit=True` | default | After `commit()`, all loaded attributes are marked stale and reload on next access. Set `False` for async sessions (see [[10 - Async SQLAlchemy]]) or when you return objects after the session closes. |

## Session lifecycle

```
SessionLocal()            open (borrows a connection lazily on first use)
   |
   v
db.query / db.add / obj.x = y       objects tracked in the identity map
   |
   v
db.flush()                SQL sent, transaction still open   (implicit before commit)
   |
   v
db.commit()               transaction committed; attributes expired
   |        \
   |         db.rollback()  on error: undo everything since last commit
   v
db.close()                connection returned to pool; objects become "detached"
```

### Object states

| State | Meaning | How you get there |
|---|---|---|
| Transient | plain Python object, not in any session | `User(...)` |
| Pending | added, not yet flushed | `db.add(user)` |
| Persistent | has a DB row and a session | after `flush()`/`commit()` or loaded via query |
| Detached | has a row but no session | after `db.close()` or `db.expunge(obj)` |

Accessing an **expired** attribute on a **detached** object → `DetachedInstanceError` (see [[13 - Gotchas and Troubleshooting]]). That's why `db.refresh(obj)` before returning matters.

## Three ways to scope a session

```python
# 1. Manual (scripts)
db = SessionLocal()
try:
    ...
    db.commit()
finally:
    db.close()

# 2. Context manager (SQLAlchemy >= 1.4) — close is automatic
with SessionLocal() as db:
    ...
    db.commit()

# 3. begin() — commit on success, rollback on exception, close always
with SessionLocal.begin() as db:
    db.add(User(...))        # no explicit commit needed

# 4. Generator dependency (FastAPI) — what get_db is
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Rules of thumb

- **One session per request / per unit of work.** Never a global session shared across threads.
- **Sessions are cheap**, engines are not. Make one engine; make many sessions.
- **Commit once** at the end of the unit of work, not after every `add`.
- On exception: `db.rollback()` before reusing the session, otherwise every further call raises `PendingRollbackError`.

## Workflow diagram

```mermaid
graph TD
    A[Python Application] -->|SessionLocal()| B[Session]
    B -->|query / add / modify| C[(Database)]
    C -->|objects| B
    B -->|commit / rollback| C
    B -->|close| A
```

## Next

→ [[06 - ORM CRUD]]
