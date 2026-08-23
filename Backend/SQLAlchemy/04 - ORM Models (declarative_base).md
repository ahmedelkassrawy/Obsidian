---
tags: [sqlalchemy, orm, model, DeclarativeBase, Mapped, mapped_column, relationship, foreignkey, declarative_base]
aliases: [ORM models, DeclarativeBase, Mapped, mapped_column, declarative_base, Base, __tablename__, models.py]
source: https://github.com/h9-tec/AI_deployment#defining-orm-models
---

# 04 — ORM Models (`DeclarativeBase`, `Mapped`, `mapped_column`)

> [!info] Source
> README §5 "Defining ORM Models", rewritten in **SQLAlchemy 2.0 style** (the README's 1.x style is kept at the bottom for reference).
> Back to [[00 - Index]] · Previous: [[03 - Core CRUD (insert, select, update, delete)]]

## The one-sentence version

A model is a class inheriting from your `Base`; each `Mapped[type]` attribute is a column, each `relationship()` is a navigable link, and the type hints are real — your editor knows `user.products` is `list[Product]`.

## The recommended way (2.0)

```python
# models.py
from datetime import datetime
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """One Base per app. Every model inherits from it; Base.metadata knows all tables."""


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    products: Mapped[list["Product"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None]                    # Optional -> nullable=True, no mapped_column needed
    price: Mapped[float]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    owner: Mapped["User"] = relationship(back_populates="products")

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} price={self.price}>"
```

## Reading the syntax

| Piece | Meaning |
|---|---|
| `class Base(DeclarativeBase)` | Your base class. Replaces `declarative_base()`. Put it in `models.py` (or `db/base.py`) and import it everywhere. |
| `id: Mapped[int] = mapped_column(primary_key=True)` | Column of type int, primary key. Type comes from the hint, options from `mapped_column`. |
| `description: Mapped[str \| None]` | Nullable string column. **No `mapped_column` needed** when you have nothing to configure — the hint alone defines it. |
| `price: Mapped[float]` | Non-null float (no `None` in the hint → `nullable=False`). |
| `Mapped[list["Product"]] = relationship(...)` | One-to-many. The `list[...]` hint tells SQLAlchemy it's a collection; no need to pass the class name as a string arg anymore. |
| `Mapped["User"] = relationship(...)` | Many-to-one, scalar. |
| `ForeignKey("users.id", ondelete="CASCADE")` | FK to the **SQL** table/column; `ondelete` makes the DB delete products when their user goes. |
| `cascade="all, delete-orphan"` | The ORM-side equivalent: deleting a `User` in the session deletes its products; removing a product from `user.products` deletes it. |
| `server_default=func.now()` | DB fills the timestamp. Prefer server defaults over Python `default=` for timestamps — they're consistent across processes. |

### Type hint → column type mapping

| Hint | Column |
|---|---|
| `Mapped[int]` | `Integer`, NOT NULL |
| `Mapped[str]` | `String` (unbounded; pass `String(n)` in `mapped_column` for MySQL) |
| `Mapped[str \| None]` | `String`, nullable |
| `Mapped[float]` | `Float` |
| `Mapped[bool]` | `Boolean` |
| `Mapped[datetime]` | `DateTime` |
| `Mapped[Decimal]` | `Numeric` — use for money |
| `Mapped[dict]` / `Mapped[list]` | needs `mapped_column(JSON)` explicitly |
| custom (e.g. `pgvector.sqlalchemy.Vector`) | `mapped_column(Vector(1024))` |

Override anything via `mapped_column(Type, ...)`.

## Column vs relationship — don't confuse them

```
Product.owner_id   -> mapped_column(ForeignKey("users.id"))   # real column, stores an int
Product.owner      -> relationship(...)                       # NOT a column, yields a User object
```

The FK column is what's in the DB. The relationship is Python-side navigation built on top of it. You need the column; the relationship is optional sugar. Navigation details: [[07 - Relationships One-to-Many]].

## Best practices baked into the example above

- [x] One `Base` per application.
- [x] `String(n)` lengths on anything that might hit MySQL.
- [x] `index=True` on every FK column and every column you filter by.
- [x] `unique=True` where the business rule says unique — let the DB enforce it, catch `IntegrityError`.
- [x] `ondelete="CASCADE"` + `cascade="all, delete-orphan"` together, so DB and ORM agree.
- [x] `server_default=func.now()` for created-at timestamps.
- [x] `__repr__` for readable logs.
- [ ] Don't put `engine` in `models.py` (the README does) — models shouldn't know about connections. Engine lives in `database.py` → [[05 - Sessions and sessionmaker]].
- [ ] Don't call `Base.metadata.create_all` at import time — do it in a startup hook or use Alembic.

## Common model additions

```python
# soft timestamps on every table — a mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class User(TimestampMixin, Base): ...

# enum column
import enum
class Role(enum.Enum):
    admin = "admin"; member = "member"
role: Mapped[Role] = mapped_column(default=Role.member)

# pgvector embedding (what raaaaag uses)
from pgvector.sqlalchemy import Vector
embedding_vector: Mapped[list[float]] = mapped_column(Vector(1024), nullable=False)
```

## Creating the tables

```python
Base.metadata.create_all(engine)                       # sync, dev only
# async:
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
```

Creates missing tables only; never alters. For real schema changes use Alembic ([[Advanced Topics and Best Practices]]).

## Legacy style (what the README shows) — recognise it, don't write it

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base   # 2.x: from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    products = relationship("Product", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")
```

| Legacy | 2.0 |
|---|---|
| `declarative_base()` | `class Base(DeclarativeBase)` |
| `Column(Integer, primary_key=True)` | `Mapped[int] = mapped_column(primary_key=True)` |
| `Column(String)` (nullable by default) | `Mapped[str \| None]` |
| `relationship("Product", back_populates=...)` | `Mapped[list["Product"]] = relationship(back_populates=...)` |
| no IDE types | full IDE types |

Both run on SQLAlchemy 2.x; the legacy one just gives you no type checking and a deprecation warning on the `ext.declarative` import.

## Next

→ [[05 - Sessions and sessionmaker]]
