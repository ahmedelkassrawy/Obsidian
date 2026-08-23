---
tags: [sqlalchemy, engine, connection, create_engine, text, context-manager, result]
aliases: [create_engine, engine.connect, text(), Context managers, Result objects, scalar vs fetchone]
source: https://github.com/h9-tec/AI_deployment#connecting-to-a-database
---

# 01 — Engine and Connections

> [!info] Source
> README §4 "Installation and Setup" + "Connecting to a Database", plus your own notes on context managers and result objects.
> Back to [[00 - Index]].

## The one-sentence version

`create_engine(url)` builds **one** `Engine` for the whole app; `engine.connect()` hands out short-lived `Connection`s from its pool; `text("...")` lets you run raw SQL through them.

## Install

```bash
pip install sqlalchemy psycopg2-binary   # PostgreSQL
pip install sqlalchemy                   # SQLite (driver ships with Python)
pip install sqlalchemy pymysql           # MySQL
```

SQLAlchemy is database-agnostic; the **driver** (psycopg2, pymysql, …) is what actually talks to a specific DB. The URL tells SQLAlchemy which driver to load.

## Database URLs

| DB | URL |
|---|---|
| SQLite file | `sqlite:///./test.db` (3 slashes + relative path) |
| SQLite absolute (Windows) | `sqlite:///D:/path/test.db` |
| SQLite in-memory | `sqlite:///:memory:` |
| PostgreSQL | `postgresql://user:password@host:5432/dbname` |
| PostgreSQL async | `postgresql+asyncpg://user:password@host:5432/dbname` |
| MySQL | `mysql+pymysql://user:password@host:3306/dbname` |

Format: `dialect+driver://user:pass@host:port/db`. Omit `+driver` to use the dialect's default.

## The code

```python
# database.py
from sqlalchemy import create_engine, text
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)   # create connection engine to your DB

# this creates a single engine object that manages:
#  - DB connections
#  - connection pooling
#  - executing SQL

@contextmanager
def get_db_connection():
    with engine.connect() as conn:
        yield conn

# opens a new connection from the engine
# returns a connection object which you can use to run queries

if __name__ == "__main__":
    with get_db_connection() as conn:
        res = conn.execute(text("SELECT 'Hello, SQLAlchemy!'"))
        print(res.scalar())
```

README's simpler variant (no `@contextmanager`, just return the connection and let the caller `with` it):

```python
def get_database_connection():
    return engine.connect()

with get_database_connection() as connection:
    result = connection.execute(text("SELECT 'Hello, SQLAlchemy!'"))
    print(result.scalar())
```

Both are equivalent; `engine.connect()` already returns a context manager.

## Line by line

### `engine = create_engine(DATABASE_URL)`

- **Create once, at import time, module-level.** Don't call `create_engine` per request — it builds a connection pool each time.
- The engine does **not** connect immediately (lazy). The first `connect()` / `execute()` opens the real connection.
- Useful kwargs:
  - `echo=True` — print every SQL statement. Great for learning.
  - `connect_args={"check_same_thread": False}` — **required** for SQLite under FastAPI/threads.
  - `pool_size=5, max_overflow=10` — pool tuning (ignored by SQLite).
  - `pool_pre_ping=True` — test connections before use; avoids "server closed the connection" after idle.

### `engine.connect()`

- Checks a connection out of the pool and returns a `Connection`.
- In SQLAlchemy 2.x a `Connection` starts a transaction implicitly on first execute and **does not autocommit**. You must call `conn.commit()` for writes to persist (the Core CRUD note shows this).
- `with engine.connect() as conn:` releases the connection back to the pool on exit — even if an exception happened inside.

### text() — running raw SQL

```python
conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": 5})
```

- `text()` wraps a raw SQL string so SQLAlchemy can execute it.
- Use `:name` placeholders + a dict for parameters. **Never** f-string user input into SQL — that's SQL injection.
- Prefer the expression language (`select`, `insert`…) when you can; `text()` is the escape hatch for DB-specific SQL.

## Context managers — why with works

A **context manager** is an object with:

- `__enter__` — runs setup **before** the block (open connection / file / lock)
- `__exit__` — runs cleanup **after** the block (close / release), **even if the block raised**

Typical uses:

- opening / closing DB connections
- opening / closing files
- acquiring / releasing locks

`@contextmanager` from `contextlib` lets you write one as a generator:

```python
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = engine.connect()      # __enter__ part
    try:
        yield conn               # the body of the `with` runs here
    finally:
        conn.close()             # __exit__ part
```

Everything before `yield` = setup; everything after = cleanup. This is exactly the shape of FastAPI's `get_db` dependency — see [[05 - Sessions and sessionmaker]] and [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/02 - Database Session Dependency (get_db)|the FastAPI get_db note]].

## Connection flow

```mermaid
graph TD
    A[Python Application] -->|create_engine| B[Engine + pool]
    B -->|connect| C[Connection]
    C -->|execute| D[(Database)]
    D -->|Result| C
    C -->|scalar / fetchall| A
    C -->|with-block exit| B
```

## Reading results — the full table

`conn.execute(...)` returns a `Result` (or `CursorResult`). Pick the accessor that matches what you expect back:

| Category | Method | Returns |
|---|---|---|
| Single value | `scalar()` | First column of first row (or `None`) |
| | `scalar_one()` | Same, but raises if not exactly one row |
| | `scalar_one_or_none()` | One value or `None`; raises if >1 |
| Rows | `fetchone()` | One `Row` or `None` |
| | `first()` | First `Row`, closes the result |
| | `fetchall()` / `all()` | List of all `Row`s |
| | `fetchmany(n)` | Up to `n` rows |
| Iteration | `for row in result:` | Stream rows |
| | `partitions(n)` | Yield lists of `n` rows |
| Row access | `row[0]` / `row["name"]` | By index / key |
| | `row.name` | Attribute access |
| Dict-like | `result.mappings()` | Rows as `dict`-like `RowMapping` |
| Single-row strict | `one()` | Exactly one `Row`, else raises |
| | `one_or_none()` | One `Row` or `None` |
| Metadata | `keys()` | Column names |
| | `columns` | Column objects |
| ORM | `scalars()` | First column of each row — **use this for ORM objects** |
| | `unique()` | De-duplicate ORM objects (needed after joined eager loads) |
| | `tuples()` | Typed tuples |
| Control | `freeze()` | Cache results for re-iteration |
| | `close()` | Close cursor |

### The three you'll use 90 % of the time

```python
conn.execute(text("SELECT count(*) FROM users")).scalar()            # -> 42
conn.execute(select(users_table)).fetchall()                          # -> [Row, Row, ...]
session.execute(select(User)).scalars().all()                         # -> [User, User, ...]  (ORM)
session.execute(select(User).where(User.id == 1)).scalar_one_or_none()  # -> User | None
```

> [!warning] `.all()` without `.scalars()` on an ORM `select(User)` gives `[(User,), (User,)]` — one-element tuples. Add `.scalars()` to unwrap.

## Next

→ [[02 - Core Tables with MetaData]]
