---
tags: [sqlalchemy, orm, database, python, moc]
aliases: [SQLAlchemy, SQLAlchemy Study Notes, SQLAlchemy Index]
source: https://github.com/h9-tec/AI_deployment#4-sqlalchemy-core-database-interaction
---

# SQLAlchemy — Index

> [!abstract] What this folder is
> The old single-page `SQLAlchemy.md` split into focused notes, enriched with README §4 (Core) and §5 (ORM) from `h9-tec/AI_deployment`, plus your own additions (context managers, result-object table, many-to-many / association objects, async).
> The archived single-page version is in [[_archived_ Original single-page note]].
>
> For the FastAPI wiring (Depends, Pydantic schemas, endpoints) see the sibling folder: [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/00 - Index|Integrating FastAPI, Pydantic, and SQLAlchemy]].

## Reading order (first time)

**Part A — Core (SQL expression language, no classes)**
1. [[01 - Engine and Connections]] — `create_engine`, `engine.connect()`, `text()`, context managers, how to read results.
2. [[02 - Core Tables with MetaData]] — `Table`, `Column`, `MetaData`, `create_all`.
3. [[03 - Core CRUD (insert, select, update, delete)]] — building statements and executing them.

**Part B — ORM (classes mapped to tables)**
4. [[04 - ORM Models (declarative_base)]] — `Base`, `__tablename__`, `Column`, `relationship`, `ForeignKey`.
5. [[05 - Sessions and sessionmaker]] — `SessionLocal`, `get_db`, transaction scope.
6. [[06 - ORM CRUD]] — `add / commit / refresh`, `query().filter().first()`.
7. [[07 - Relationships One-to-Many]] — `back_populates`, navigating `user.products` / `product.owner`.
8. [[08 - Many-to-Many and Association Objects]] — `secondary=`, composite primary keys, `back_populates` vs `backref`.
9. [[09 - Querying Data]] — `filter`, `join`, `order_by`, legacy `query()` vs 2.0 `select()`.

**Part C — Beyond the basics**
10. [[10 - Async SQLAlchemy]] — `AsyncSession`, `async_sessionmaker`, `await db.execute(select(...))`.
11. [[11 - Core vs ORM — when to use which]] — decision guide + key takeaways.

## Look-up notes

- [[12 - Cheatsheet]] — one screen of the patterns.
- [[13 - Gotchas and Troubleshooting]] — errors you'll hit and the fix.

## "I want to find…" quick table

| I want to… | Go to |
|---|---|
| Run raw SQL once | [[01 - Engine and Connections#text() — running raw SQL]] |
| Remember `scalar()` vs `first()` vs `fetchall()` vs `scalars().all()` | [[01 - Engine and Connections#Reading results — the full table]] |
| Understand `@contextmanager` / `with` | [[01 - Engine and Connections#Context managers — why with works]] |
| Define a table without classes | [[02 - Core Tables with MetaData]] |
| `insert(...).values(...)`, `select(...).where(...)` | [[03 - Core CRUD (insert, select, update, delete)]] |
| Get the new row's id after insert (Core) | [[03 - Core CRUD (insert, select, update, delete)#Getting the inserted id]] |
| Write a model class | [[04 - ORM Models (declarative_base)]] |
| `sessionmaker(autocommit=False, autoflush=False, ...)` | [[05 - Sessions and sessionmaker]] |
| `db.add` → `commit` → `refresh` | [[06 - ORM CRUD#The write dance]] |
| `relationship(..., back_populates=...)` | [[07 - Relationships One-to-Many]] |
| Many-to-many with extra columns on the link table | [[08 - Many-to-Many and Association Objects]] |
| `back_populates` vs `backref` | [[08 - Many-to-Many and Association Objects#back_populates vs backref]] |
| `startswith`, `>`, `join` | [[09 - Querying Data]] |
| 2.0 style `select(User).where(...)` | [[09 - Querying Data#Legacy query() vs 2.0 select()]] |
| Async session / `await db.commit()` | [[10 - Async SQLAlchemy]] |
| `expire_on_commit=False` — why | [[10 - Async SQLAlchemy#10.1 Creating an async session]] |
| Decide Core or ORM | [[11 - Core vs ORM — when to use which]] |
| `DetachedInstanceError`, `check_same_thread`, `MissingGreenlet` | [[13 - Gotchas and Troubleshooting]] |

## Related

- [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/00 - Index|Integrating FastAPI, Pydantic, and SQLAlchemy]] — uses these models inside FastAPI endpoints.
- [[Pydantic]] — the schema side.
- [[Advanced Topics and Best Practices]] — async, Alembic migrations, connection pooling.
