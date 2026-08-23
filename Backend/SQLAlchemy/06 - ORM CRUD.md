---
tags: [sqlalchemy, orm, crud, add, commit, flush, refresh, select, get, bulk-insert]
aliases: [ORM CRUD, crud.py, add commit refresh, db.get, db.add vs insert, bulk insert, update with ORM, delete with ORM, repository pattern]
source: https://github.com/h9-tec/AI_deployment#basic-crud-operations-with-orm
---

# 06 — ORM CRUD

> [!info] Source
> README §5 "Basic CRUD Operations with ORM", rewritten 2.0-style with commit-on-exit sessions from [[05 - Sessions and sessionmaker]].
> Back to [[00 - Index]] · Previous: [[05 - Sessions and sessionmaker]]

## The one-sentence version

**Create** = build object → `db.add()` (commit happens when the `get_db` block exits). **Read** = `db.get(Model, pk)` or `db.execute(select(...))`. **Update** = change attributes. **Delete** = `db.delete(obj)`. **Many rows at once** = `db.add_all()` or Core `insert()`.

## The recommended crud.py

Every function takes `db: Session` first and **never commits** — the caller's `with get_db()` block owns the transaction. That's what makes these functions composable (two creates in one transaction) and testable.

```python
# crud.py
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import User, Product


# ---------- Create ----------
def create_user(db: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    db.add(user)
    db.flush()            # sends INSERT now so user.id is populated; commit still belongs to the caller
    return user


def create_product_for_user(db: Session, user_id: int, name: str, price: float,
                            description: str | None = None) -> Product:
    product = Product(name=name, price=price, description=description, owner_id=user_id)
    db.add(product)
    db.flush()
    return product


# ---------- Read ----------
def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)                       # by primary key — uses the identity map, may skip SQL


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.execute(
        select(User).order_by(User.id).offset(skip).limit(limit)
    ).scalars().all()


def list_users_with_products(db: Session) -> list[User]:
    return db.execute(
        select(User).options(selectinload(User.products))     # avoids N+1
    ).scalars().all()


# ---------- Update ----------
def update_user_email(db: Session, user_id: int, new_email: str) -> User | None:
    user = db.get(User, user_id)
    if user is None:
        return None
    user.email = new_email        # session sees the change ("dirty"); UPDATE on flush/commit
    return user


# ---------- Delete ----------
def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if user is None:
        return False
    db.delete(user)               # cascade="all, delete-orphan" removes their products too
    return True
```

Using it:

```python
from database import get_db
import crud

with get_db() as db:                                   # one transaction for everything inside
    alice = crud.create_user(db, "alice", "alice@example.com")
    crud.create_product_for_user(db, alice.id, "Keyboard", 120.0)   # alice.id exists thanks to flush()
    crud.create_product_for_user(db, alice.id, "Mouse", 50.0)
# commit happened here, once

with get_db() as db:
    for u in crud.list_users_with_products(db):
        print(u.username, [p.name for p in u.products])
```

## The write dance

What `add` / `flush` / `commit` / `refresh` each do:

```
User(...)        Python object only                        id = None
db.add(obj)      session tracks it (pending)               id = None
db.flush()       INSERT sent, tx still open                id assigned — usable now
db.commit()      tx committed (get_db does this for you)
db.refresh(obj)  SELECT the row back — only needed for server-side defaults/triggers
```

- **`flush()`** = "send the SQL, keep the transaction open". Use it when you need the id mid-transaction.
- **`refresh()`** = re-read from DB. Needed for `server_default` columns (e.g. `created_at`) if you read them right after insert. Not needed just to get `id` — `flush()` already did that.
- With `expire_on_commit=False` (recommended), objects stay readable after commit without `refresh()`.

## db.add() vs Core insert() — which write path?

| Situation | Use | Why |
|---|---|---|
| 1 – a few hundred rows, you have model objects | `db.add(obj)` / `db.add_all([objs])` | Simplest; relationships, defaults, cascades all work; objects come back with ids |
| Thousands+ rows, no need for the objects afterwards | `db.execute(insert(Model), [dict, dict, ...])` | One statement (`executemany`); skips per-object ORM bookkeeping — several × faster |
| Need `ON CONFLICT DO NOTHING / UPDATE` (upsert) | Core `insert()` with dialect `.on_conflict_do_*` | ORM has no upsert |

Example of the bulk path:

```python
from sqlalchemy import insert

with get_db() as db:
    db.execute(
        insert(Product),
        [{"name": n, "price": p, "owner_id": uid} for n, p in rows],
    )
```

> [!tip] Rule: start with `db.add` / `db.add_all`. Switch to `insert()` only when you measure a problem or you're loading bulk data (ETL, embeddings ingestion). The async worked example in [[10 - Async SQLAlchemy#Worked example — PDF ingestion]] shows both.

## Read patterns (2.0)

| Want | Code |
|---|---|
| One by PK | `db.get(User, 1)` |
| One by condition or `None` | `db.execute(select(User).where(User.email == e)).scalar_one_or_none()` |
| Exactly one (raise otherwise) | `...scalar_one()` |
| Many | `db.execute(select(User)).scalars().all()` |
| Paged | `select(User).order_by(User.id).offset(skip).limit(limit)` — **always `order_by` when paging** or pages aren't stable |
| Count | `db.execute(select(func.count()).select_from(User)).scalar_one()` |
| Exists | `db.execute(select(User.id).where(...).limit(1)).first() is not None` |
| With relationship loaded | `select(User).options(selectinload(User.products))` |

Full operator list and legacy `query()` equivalents in [[09 - Querying Data]].

## Bulk update / delete without loading objects

```python
from sqlalchemy import update, delete

db.execute(update(Product).where(Product.price < 10).values(price=10))
db.execute(delete(Product).where(Product.owner_id == 42))
```

Faster than load-modify-commit for many rows; bypasses ORM cascades and in-session objects (call `db.expire_all()` after if you still hold objects).

## Handling unique-constraint violations

With commit-on-exit, the `IntegrityError` surfaces when the `with` block exits. Catch it **outside** the block (the session has already been rolled back by `get_db`):

```python
from sqlalchemy.exc import IntegrityError

try:
    with get_db() as db:
        crud.create_user(db, "alice", "alice@example.com")
except IntegrityError:
    print("username or email already taken")
```

If you need to detect it *inside* the block (e.g. to try a different value), `db.flush()` inside a `try` — the error fires at flush time:

```python
with get_db() as db:
    db.add(User(username="alice", email="alice@example.com"))
    try:
        db.flush()
    except IntegrityError:
        db.rollback()           # required before using the session again
        ...
```

## Legacy style (README) — recognise it

```python
db.query(User).filter(User.id == user_id).first()
db.query(User).offset(skip).limit(limit).all()
db.add(u); db.commit(); db.refresh(u)
```

Works, but `query()` is legacy, doesn't exist on `AsyncSession`, and commit-per-function makes composing operations into one transaction impossible.

## Next

→ [[07 - Relationships One-to-Many]]
