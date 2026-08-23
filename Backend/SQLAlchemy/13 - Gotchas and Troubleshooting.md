---
tags: [sqlalchemy, troubleshooting, errors, debugging]
aliases: [SQLAlchemy gotchas, SQLAlchemy errors, DetachedInstanceError, MissingGreenlet, PendingRollbackError, check_same_thread, IntegrityError]
---

# 13 — Gotchas and Troubleshooting

> [!info] Added note — not from the README. Search by error text. Back to [[00 - Index]].
> FastAPI-specific errors (422s, `Depends` misuse, Pydantic `from_attributes`) are in [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/08 - Gotchas and Troubleshooting|Integrating › 08 - Gotchas]].

---

## My insert/update didn't save

**Cause:** no `commit()`. In 2.x the connection/session is in a transaction that **rolls back** when the `with` block exits uncommitted.
**Fix:** `conn.commit()` / `db.commit()`, or use `engine.begin()` / `SessionLocal.begin()` which commit on success.

---

## `sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread`

**Cause:** SQLite's connection is thread-bound; FastAPI runs sync endpoints in a threadpool.
**Fix:** `create_engine(url, connect_args={"check_same_thread": False})`. SQLite only.

---

## `sqlalchemy.exc.IntegrityError: UNIQUE constraint failed` / `FOREIGN KEY constraint failed` / `NOT NULL constraint failed`

**Cause:** duplicate on a `unique=True` column, FK pointing at a missing row, or a `nullable=False` column left empty.
**Fix:** `db.rollback()`, then handle (return 409/400). Check the parent exists before inserting a child.

---

## `sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception`

**Cause:** a previous `commit()`/`flush()` raised and you kept using the session without `rollback()`.
**Fix:** always `db.rollback()` in your `except`.

---

## `sqlalchemy.orm.exc.DetachedInstanceError: Instance <User> is not bound to a Session`

**Cause:** accessing an **expired** or **lazy** attribute on an object after its session closed. Commonly: returned an object from a `with SessionLocal()` block and then touched `.products` or an attribute expired by `commit()`.
**Fix:** `db.refresh(obj)` before closing; eager-load relationships (`selectinload`); or `expire_on_commit=False` on the sessionmaker.

---

## `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here`

**Cause:** async session + implicit I/O — usually a lazy-loaded relationship (`user.products`) or an expired attribute after `commit()`.
**Fix:** `expire_on_commit=False`; `select(User).options(selectinload(User.products))`; or `await db.refresh(user, ["products"])`. See [[10 - Async SQLAlchemy]].

---

## `AttributeError: 'AsyncSession' object has no attribute 'query'`

**Cause:** legacy `db.query()` doesn't exist on async sessions.
**Fix:** `await db.execute(select(Model).where(...))`.

---

## `RuntimeWarning: coroutine 'AsyncSession.commit' was never awaited`

**Cause:** `db.commit()` without `await` in async code. Nothing was saved.
**Fix:** `await db.commit()`.

---

## `.all()` returns `[(User,), (User,)]` — tuples, not objects

**Cause:** `session.execute(select(User)).all()` returns `Row`s.
**Fix:** `.scalars().all()`.

---

## `MovedIn20Warning: The declarative_base() function is now available as sqlalchemy.orm.declarative_base()`

**Cause:** importing from `sqlalchemy.ext.declarative` on 2.x.
**Fix:** `from sqlalchemy.orm import declarative_base` (or subclass `DeclarativeBase`). Warning only.

---

## `sqlalchemy.exc.OperationalError: no such table: users`

**Cause:** `create_all` never ran, or ran against a different SQLite file (relative path + different working directory).
**Fix:** run `Base.metadata.create_all(engine)` once; use an absolute path or always run from the same directory.

---

## Added a column to the model, but the table didn't change

**Cause:** `create_all` only creates **missing tables**; it never `ALTER`s.
**Fix (dev):** delete the SQLite file. **Fix (real):** Alembic — see [[Advanced Topics and Best Practices]].

---

## `sqlalchemy.exc.InvalidRequestError: Mapper 'Mapper[User(users)]' has no property 'owner'` / `back_populates` name mismatch

**Cause:** `back_populates="owner"` but the other class's attribute is named something else (or missing).
**Fix:** the string in `back_populates` must equal the attribute name on the **other** class exactly.

---

## `sqlalchemy.exc.NoForeignKeysError: Could not determine join condition between parent/child tables`

**Cause:** `relationship()` declared but no `ForeignKey` column linking the two tables, or FK string uses the class name instead of the table name.
**Fix:** `ForeignKey("users.id")` — **table**.**column**, lowercase SQL names.

---

## `sqlalchemy.exc.AmbiguousForeignKeysError`

**Cause:** two FKs between the same pair of tables; SQLAlchemy can't pick one.
**Fix:** `relationship("User", foreign_keys=[owner_id])` and/or an explicit `join(Product, Product.owner_id == User.id)`.

---

## Deleting a parent leaves orphan children (SQLite) or raises (Postgres)

**Cause:** no cascade configured; SQLite doesn't enforce FKs by default.
**Fix:** `relationship(..., cascade="all, delete-orphan")` or `ForeignKey(..., ondelete="CASCADE")`. To make SQLite enforce FKs: `PRAGMA foreign_keys=ON` via an engine event.

---

## Slow list endpoint — hundreds of small queries in the log

**Cause:** N+1 lazy loading: `for u in users: u.products`.
**Fix:** `.options(selectinload(User.products))`. See [[07 - Relationships One-to-Many#Lazy loading and the N+1 problem]].

---

## `result.lastrowid` is `None` / wrong on Postgres

**Cause:** `lastrowid` is a cursor attribute that Postgres doesn't populate.
**Fix:** `result.inserted_primary_key[0]` or `.returning(t.c.id)`.

---

## `update(...)` / `delete(...)` touched every row

**Cause:** forgot `.where()`.
**Fix:** always add a `.where()`; consider running with `echo=True` while developing.

---

## `(psycopg2.OperationalError) server closed the connection unexpectedly` after idle

**Cause:** pooled connection went stale (DB restarted, firewall idle timeout).
**Fix:** `create_engine(url, pool_pre_ping=True)`.

---

## Quick diagnosis flow

```
Something's wrong
|- data not saved            -> missing commit()
|- IntegrityError            -> unique / FK / not-null -> rollback + handle
|- PendingRollbackError      -> rollback() after the earlier failure
|- DetachedInstanceError     -> refresh / eager-load / expire_on_commit=False
|- MissingGreenlet (async)   -> lazy load in async -> selectinload / expire_on_commit=False
|- tuples instead of objects -> add .scalars()
|- no such table             -> create_all not run / wrong file
|- thread error (SQLite)     -> check_same_thread=False
|- many tiny queries         -> N+1 -> selectinload
```
