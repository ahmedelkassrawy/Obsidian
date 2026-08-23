---
tags: [sqlalchemy, best-practices, checklist, review]
aliases: [SQLAlchemy best practices, SQLAlchemy checklist, SQLAlchemy code review checklist]
---

# 14 — Best Practices Checklist

> [!info] Use this as a review list for any file that touches SQLAlchemy. Each item links to the note that explains it. Back to [[00 - Index]].

## Project structure

- [ ] `database.py` holds `engine`, `SessionLocal`, `get_db`, `get_db_dep`. Nothing else. → [[05 - Sessions and sessionmaker]]
- [ ] `models.py` holds `Base` + models. **No engine, no `create_all` at import.** → [[04 - ORM Models (declarative_base)]]
- [ ] `crud.py` / repository functions take `db: Session` as first arg and **never commit**. → [[06 - ORM CRUD]]
- [ ] `DATABASE_URL` comes from config/env, never hard-coded.

## Engine

- [ ] Exactly **one** `create_engine` / `create_async_engine` per process, module-level.
- [ ] `pool_pre_ping=True` for anything that talks to a real server.
- [ ] SQLite under FastAPI/threads: `connect_args={"check_same_thread": False}`.
- [ ] `echo=True` only via a config flag, never committed on.

## Sessions

- [ ] `sessionmaker(..., expire_on_commit=False)` — mandatory for async, recommended for sync.
- [ ] Session scope = `with get_db() as db:` (commit-on-exit, rollback-on-error). → [[05 - Sessions and sessionmaker#The recommended database.py]]
- [ ] FastAPI uses the **undecorated generator** (`get_db_dep`), scripts use the `@contextmanager` one. Never `db = get_db()`. → [[05 - Sessions and sessionmaker#The FastAPI dependency is a different shape — don't mix them up]]
- [ ] One session per request / job / CLI command. No global session. Never shared across threads or asyncio tasks.
- [ ] Open the session **around** a loop, not inside it.

## Models

- [ ] 2.0 typed style: `class Base(DeclarativeBase)`, `Mapped[...]`, `mapped_column(...)`.
- [ ] `String(n)` lengths on columns that may hit MySQL.
- [ ] `index=True` on every FK and every column you filter/sort on.
- [ ] `unique=True` for business-unique columns; catch `IntegrityError`.
- [ ] FKs: `ForeignKey("table.col", ondelete="CASCADE")` **and** `relationship(..., cascade="all, delete-orphan")` so DB and ORM agree. → [[07 - Relationships One-to-Many#Cascade and orphan handling]]
- [ ] `back_populates` on both sides; no `backref`. → [[08 - Many-to-Many and Association Objects#back_populates vs backref]]
- [ ] Timestamps via `server_default=func.now()`; money via `Numeric`, not `Float`.
- [ ] Many-to-many with extra columns → association object; write through it, mark the `secondary` relationship `viewonly=True` or drop it. → [[08 - Many-to-Many and Association Objects]]

## Queries

- [ ] `select()` + `db.execute()`, not `db.query()` (legacy, and absent on `AsyncSession`). → [[09 - Querying Data]]
- [ ] `.scalars()` when selecting whole entities; `.scalar_one_or_none()` for one.
- [ ] `db.get(Model, pk)` for primary-key lookups.
- [ ] `order_by` on every paginated query.
- [ ] Loops over relationships → `selectinload` / `joinedload` in the query (no N+1). → [[07 - Relationships One-to-Many#Lazy loading and the N+1 problem]]
- [ ] No f-strings in `text()`; bind params with `:name`. → [[01 - Engine and Connections#text() — running raw SQL]]

## Writes

- [ ] Default: `db.add()` / `db.add_all()`; `db.flush()` when you need the id mid-transaction. → [[06 - ORM CRUD#The write dance]]
- [ ] Thousands of rows or upsert → Core `insert(Model)` with a list of dicts. → [[06 - ORM CRUD#db.add() vs Core insert() — which write path?]]
- [ ] Every `update()` / `delete()` statement has a `.where()`.
- [ ] External API calls (embeddings, HTTP) happen **before** opening the session, batched — don't hold a transaction open while waiting on the network. → [[10 - Async SQLAlchemy#Worked example — PDF ingestion]]

## Async

- [ ] Async driver in the URL (`+asyncpg`, `+aiosqlite`).
- [ ] `await` on `execute / get / flush / commit / rollback / refresh / delete`; none on `add` or result accessors. → [[10 - Async SQLAlchemy#What gets awaited and what doesn't]]
- [ ] No lazy loads: `expire_on_commit=False` + `selectinload`. → [[10 - Async SQLAlchemy#The big trap — lazy loading in async]]
- [ ] DDL via `await conn.run_sync(Base.metadata.create_all)` at startup (`lifespan`), not per request.
- [ ] `await engine.dispose()` on shutdown.

## Schema changes

- [ ] `create_all` for dev/tests only. Alembic for anything with data you care about. → [[Advanced Topics and Best Practices]]

## Errors

- [ ] `IntegrityError` caught and mapped to a user-facing error (409 in HTTP).
- [ ] After any failed flush/commit you keep using the session → `rollback()` first. → [[13 - Gotchas and Troubleshooting]]

## Review prompt (copy into a PR review)

> Check this file against `SQLAlchemy/14 - Best Practices Checklist`: session scope, commit ownership, 2.0 style, N+1, await coverage, FK/cascade agreement, `.where()` on bulk statements.
