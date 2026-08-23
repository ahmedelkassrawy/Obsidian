---
tags: [sqlalchemy, orm, database, python, moc, 2.0-style]
aliases: [SQLAlchemy, SQLAlchemy Study Notes, SQLAlchemy Index]
source: https://github.com/h9-tec/AI_deployment#4-sqlalchemy-core-database-interaction
---

# SQLAlchemy — Index

> [!abstract] What this folder is
> The old single-page `SQLAlchemy.md` split into focused notes, rewritten **SQLAlchemy-2.0-first** (typed `Mapped` models, `select()` not `query()`, commit-on-exit sessions), enriched with README §4–§5 from `h9-tec/AI_deployment` and your own additions (context managers, result-object table, many-to-many / association objects, async).
> The README's legacy 1.x style is kept in each note under a "Legacy style — recognise it" heading so you can still read older code.
> Archived single-page version: [[_archived_ Original single-page note]].
>
> FastAPI wiring (Depends, Pydantic schemas, endpoints): [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/00 - Index|Integrating FastAPI, Pydantic, and SQLAlchemy]].

## The recommended shape (what every note assumes)

```
db/
├── database.py   engine · SessionLocal(expire_on_commit=False) · get_db (commit-on-exit ctx manager) · get_db_dep (FastAPI)
├── models.py     class Base(DeclarativeBase) · Mapped[...] models · no engine, no create_all
└── crud.py       functions take db: Session first · never commit · caller owns the transaction
```

```python
with get_db() as db:                 # async: async with get_db() as db:
    db.add(User(username="ada", email="ada@x.com"))
    user = db.execute(select(User).where(User.email == "ada@x.com")).scalar_one_or_none()
# committed here
```

Full checklist: [[14 - Best Practices Checklist]].

## Reading order (first time)

**Part A — Core (SQL expression language, no classes)**
1. [[01 - Engine and Connections]] — `create_engine`, `engine.connect()`, `text()`, context managers, how to read results.
2. [[02 - Core Tables with MetaData]] — `Table`, `Column`, `MetaData`, `create_all`.
3. [[03 - Core CRUD (insert, select, update, delete)]] — statements, `commit()`, bulk inserts.

**Part B — ORM (classes mapped to tables)**
4. [[04 - ORM Models (declarative_base)]] — `DeclarativeBase`, `Mapped`, `mapped_column`, `relationship`, `ForeignKey`, cascades.
5. [[05 - Sessions and sessionmaker]] — `SessionLocal`, commit-on-exit `get_db`, `get_db_dep` for FastAPI, object states.
6. [[06 - ORM CRUD]] — `add` / `flush` / `get` / `select`, `db.add` vs bulk `insert()`, update, delete.
7. [[07 - Relationships One-to-Many]] — `back_populates`, navigating, N+1 and `selectinload`, cascade.
8. [[08 - Many-to-Many and Association Objects]] — `secondary=`, composite PKs, `back_populates` vs `backref`.
9. [[09 - Querying Data]] — operators, `join`, `order_by`, 2.0 `select()` vs legacy `query()`.

**Part C — Beyond the basics**
10. [[10 - Async SQLAlchemy]] — async engine/session/`get_db`, what to `await`, worked PDF-ingestion example, lazy-load trap.
11. [[11 - Core vs ORM — when to use which]] — decision guide + key takeaways.

## Look-up notes

- [[12 - Cheatsheet]] — one screen of the 2.0 patterns.
- [[13 - Gotchas and Troubleshooting]] — errors you'll hit and the fix.
- [[14 - Best Practices Checklist]] — tick-list for reviewing any SQLAlchemy file.

## "I want to find…" quick table

| I want to… | Go to |
|---|---|
| Run raw SQL once | [[01 - Engine and Connections#text() — running raw SQL]] |
| `scalar()` vs `first()` vs `fetchall()` vs `scalars().all()` | [[01 - Engine and Connections#Reading results — the full table]] |
| Understand `@contextmanager` / `with` | [[01 - Engine and Connections#Context managers — why with works]] |
| Define a table without classes | [[02 - Core Tables with MetaData]] |
| `insert(...).values(...)`, `select(...).where(...)` | [[03 - Core CRUD (insert, select, update, delete)]] |
| Get the new row's id after insert (Core) | [[03 - Core CRUD (insert, select, update, delete)#Getting the inserted id]] |
| Write a model class (2.0 typed) | [[04 - ORM Models (declarative_base)#The recommended way (2.0)]] |
| Type hint → column type | [[04 - ORM Models (declarative_base)#Type hint → column type mapping]] |
| The recommended `database.py` | [[05 - Sessions and sessionmaker#The recommended database.py]] |
| `expire_on_commit=False` — why | [[05 - Sessions and sessionmaker#sessionmaker(...) arguments]] |
| `get_db()` returned a context-manager object, not a session | [[05 - Sessions and sessionmaker#The FastAPI dependency is a different shape — don't mix them up]] |
| `add` / `flush` / `commit` / `refresh` — which does what | [[06 - ORM CRUD#The write dance]] |
| `db.add` or `insert()` for many rows? | [[06 - ORM CRUD#db.add() vs Core insert() — which write path?]] |
| The recommended `crud.py` | [[06 - ORM CRUD#The recommended crud.py]] |
| `relationship(..., back_populates=...)` | [[07 - Relationships One-to-Many]] |
| Delete parent → children go too (cascade) | [[07 - Relationships One-to-Many#Cascade and orphan handling]] |
| Many-to-many with extra columns on the link table | [[08 - Many-to-Many and Association Objects]] |
| `back_populates` vs `backref` | [[08 - Many-to-Many and Association Objects#back_populates vs backref]] |
| `startswith`, `>`, `in_`, `join`, `order_by` | [[09 - Querying Data]] |
| Translate legacy `query()` to `select()` | [[09 - Querying Data#Legacy query() vs 2.0 select()]] |
| Async `database.py` / `async with get_db()` | [[10 - Async SQLAlchemy#The recommended database.py (async)]] |
| What to `await` and what not | [[10 - Async SQLAlchemy#What gets awaited and what doesn't]] |
| Ingest chunks + embeddings into the DB (raaaaag) | [[10 - Async SQLAlchemy#Worked example — PDF ingestion]] |
| `MissingGreenlet` / lazy load in async | [[10 - Async SQLAlchemy#The big trap — lazy loading in async]] |
| Create tables in async / pgvector extension | [[10 - Async SQLAlchemy#Creating the tables (async)]] |
| Decide Core or ORM | [[11 - Core vs ORM — when to use which]] |
| Any error message | [[13 - Gotchas and Troubleshooting]] |
| Review a file against best practices | [[14 - Best Practices Checklist]] |

## Related

- [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/00 - Index|Integrating FastAPI, Pydantic, and SQLAlchemy]] — uses these models inside FastAPI endpoints.
- [[Pydantic]] — the schema side.
- [[Advanced Topics and Best Practices]] — Alembic migrations, connection pooling, auth.
