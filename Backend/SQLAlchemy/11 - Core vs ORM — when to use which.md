---
tags: [sqlalchemy, core, orm, architecture, decision]
aliases: [Core vs ORM, When to use Core, When to use ORM, Key takeaways]
---

# 11 — Core vs ORM: when to use which

> [!info] Back to [[00 - Index]] · Previous: [[10 - Async SQLAlchemy]]

## The two layers

```
+---------------------------+
|  ORM  (Session, models,   |   classes <-> rows, relationships, identity map
|        relationship)      |
+---------------------------+
|  Core (Engine, Table,     |   SQL expression language, connections, pooling
|        select/insert ...) |
+---------------------------+
|  DBAPI driver             |   psycopg2 / sqlite3 / asyncpg ...
+---------------------------+
```

The ORM is **built on** Core. Every ORM query becomes a Core statement. You can mix them freely in one app (`session.execute(select(...))` is literally Core inside the ORM).

## Side by side

| | Core | ORM |
|---|---|---|
| Define schema | `Table("users", metadata, Column(...))` | `class User(Base): __tablename__ = ...` |
| Handle | `Connection` via `engine.connect()` | `Session` via `SessionLocal()` |
| Insert | `conn.execute(insert(t).values(...)); conn.commit()` | `db.add(User(...)); db.commit()` |
| Read | `conn.execute(select(t).where(...)).fetchall()` → `Row`s | `db.query(User).filter(...).all()` → `User` objects |
| Update | `update(t).where(...).values(...)` | `user.email = x; db.commit()` |
| Relationships | manual joins | `user.products`, `product.owner` |
| Change tracking | none | automatic (dirty tracking, identity map) |
| Overhead | minimal | object construction per row |

## Pick Core when

- You need **exact control** over the SQL (reporting, analytics, window functions, CTEs).
- **Bulk** operations: inserting 100k rows, mass updates — ORM per-object overhead hurts.
- Working against a **legacy schema** that doesn't map cleanly to classes.
- You're writing a thin script, migration, or ETL job.

## Pick ORM when

- Building a **CRUD application** (FastAPI API, admin tools) — which is the common case.
- You want relationships navigated as attributes.
- You want Pydantic `from_attributes=True` to serialise rows straight from objects ([[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/06 - Request vs Response Models Explained|see the FastAPI integration]]).
- Domain logic lives on the model classes.

## Use both

Common pattern: ORM for the app, Core (`session.execute(text(...))` or `session.execute(update(...))`) for the handful of hot paths that need it.

## Key takeaways (whole folder)

- **Connection** — one `create_engine` per app; `engine.connect()` for short-lived connections; `text()` for raw SQL. → [[01 - Engine and Connections]]
- **Table creation** — `Table` + `MetaData` in Core, `Base` subclasses in ORM; `create_all` creates missing tables only. → [[02 - Core Tables with MetaData]], [[04 - ORM Models (declarative_base)]]
- **SQL queries** — `insert`, `select`, `update`, `delete`; always `commit()` writes. → [[03 - Core CRUD (insert, select, update, delete)]]
- **ORM** — classes via `declarative_base`; `Column` for data, `relationship` for navigation. → [[04 - ORM Models (declarative_base)]]
- **Sessions** — `sessionmaker` factory, one session per unit of work, `get_db` for FastAPI. → [[05 - Sessions and sessionmaker]]
- **CRUD** — `add` → `commit` → `refresh`. → [[06 - ORM CRUD]]
- **Relationships** — `ForeignKey` + `relationship(back_populates=...)`; watch for N+1. → [[07 - Relationships One-to-Many]]
- **Many-to-many** — `secondary=` for plain links, association object for links with data. → [[08 - Many-to-Many and Association Objects]]
- **Querying** — `filter`/`where`, `join`, `order_by`; prefer 2.0 `select()`. → [[09 - Querying Data]]
- **Async** — `sqlalchemy.ext.asyncio`, `await` every I/O call, `expire_on_commit=False`, eager-load relationships. → [[10 - Async SQLAlchemy]]
