---
tags: [sqlalchemy, core, table, metadata, column, create_all, schema]
aliases: [Core tables, Table and MetaData, metadata.create_all, Column types]
source: https://github.com/h9-tec/AI_deployment#defining-tables-metadata
---

# 02 — Core Tables with MetaData

> [!info] Source
> README §4 "Defining Tables (Metadata)". Back to [[00 - Index]] · Previous: [[01 - Engine and Connections]]

## The one-sentence version

In **Core** you describe tables as `Table(...)` objects registered in a `MetaData` container, then `metadata.create_all(engine)` turns them into real `CREATE TABLE` statements.

## The code

```python
# models_core.py
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True, index=True),
    Column("description", String),
    Column("price", Float),
)

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("email", String, unique=True),
)

metadata.create_all(engine)
```

> [!bug] Your original note had `Column("name", String, primary_key=True, index=True)` on `products`
> That makes `(id, name)` a **composite primary key** — almost certainly not intended. The README uses `unique=True`. Fixed here; keep `unique=True`.

## Pieces

| Piece | What it is |
|---|---|
| `MetaData()` | A registry. Every `Table` you build with it gets added. `create_all` / `drop_all` act on everything inside. |
| `Table("name", metadata, *columns)` | One table. First arg = SQL table name, second = the registry, rest = `Column`s and constraints. |
| `Column("col", Type, **options)` | One column. |
| `products_table.c.id` | `.c` = "columns" namespace. That's how you reference a column in queries (`where(products_table.c.id == 5)`). |

## `Column` options you'll reach for

| Option | Meaning |
|---|---|
| `primary_key=True` | PK. Integer PKs auto-increment on SQLite/Postgres/MySQL. |
| `unique=True` | UNIQUE constraint → `IntegrityError` on duplicates. |
| `index=True` | Create an index (faster lookups on that column). |
| `nullable=False` | NOT NULL. Default is nullable **except** for primary keys. |
| `default=value` | Python-side default applied at insert. |
| `server_default=text("now()")` | DB-side default (in the `CREATE TABLE`). |
| `ForeignKey("users.id")` | FK to another table — `"table.column"` string. |
| `onupdate=...` | Value to set on every UPDATE (e.g. `datetime.utcnow`). |

## Common column types

| SQLAlchemy | SQL-ish | Note |
|---|---|---|
| `Integer` | INT | |
| `BigInteger` | BIGINT | |
| `String(50)` | VARCHAR(50) | Length optional on SQLite/Postgres, **required** on MySQL |
| `Text` | TEXT | unbounded |
| `Float` | FLOAT/REAL | not for money |
| `Numeric(10, 2)` | DECIMAL | use for money |
| `Boolean` | BOOL | |
| `DateTime` / `DATETIME` | TIMESTAMP | `DateTime(timezone=True)` for tz-aware |
| `Date`, `Time` | | |
| `JSON` | JSON/JSONB | Postgres has `JSONB` via `sqlalchemy.dialects.postgresql` |
| `Enum(MyEnum)` | ENUM / CHECK | |
| `LargeBinary` | BLOB | |

## `metadata.create_all(engine)`

- Emits `CREATE TABLE IF NOT EXISTS` for every table in `metadata` that's missing.
- **Idempotent** — safe to call repeatedly.
- **Does not alter** existing tables. Add a column to `Table(...)` → `create_all` does nothing. That's what Alembic migrations are for.
- `metadata.drop_all(engine)` — the inverse. Dangerous; dev only.
- The README leaves it commented out in `models_core.py` and calls it from `crud_core.py`'s `__main__`; your note calls it at import. Either works; just don't rely on import-order side effects in real apps.

## Core `Table` vs ORM class — same thing, two syntaxes

```python
# Core
users_table = Table("users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True))

# ORM (next notes)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
```

The ORM class *generates* a `Table` behind the scenes — reach it via `User.__table__`, and its metadata via `Base.metadata`. So `Base.metadata.create_all(engine)` in ORM code is literally the same call as here.

## Next

→ [[03 - Core CRUD (insert, select, update, delete)]]
