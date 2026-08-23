---
tags: [sqlalchemy, orm, declarative_base, model, relationship, foreignkey, tablename]
aliases: [ORM models, declarative_base, Base, __tablename__, models_orm.py, DeclarativeBase, Mapped]
source: https://github.com/h9-tec/AI_deployment#defining-orm-models
---

# 04 — ORM Models (`declarative_base`)

> [!info] Source
> README §5 "Defining ORM Models". Back to [[00 - Index]] · Previous: [[03 - Core CRUD (insert, select, update, delete)]]

## The one-sentence version

An ORM model is a Python class that inherits from `Base`; its class attributes are `Column`s (→ table columns) and `relationship`s (→ navigable links to other models).

## The code

```python
# models_orm.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./test_orm.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)

    # "products" is the attribute name here; back_populates names the
    # attribute on the OTHER class ("owner") that points back.
    products = relationship("Product", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # "owner" is the attribute name here; back_populates -> "products" on User.
    owner = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

# Base.metadata.create_all(engine)   # run once, or from main
```

## Pieces

| Piece | What it does |
|---|---|
| `Base = declarative_base()` | Factory for the parent class. Every subclass registers its table in `Base.metadata`. **One `Base` per app** — models on different `Base`s can't relate to each other. |
| `__tablename__` | Required. The SQL table name. |
| `Column(...)` as class attribute | Becomes a table column **and** an instance attribute (`user.username`). Same options as in Core — see [[02 - Core Tables with MetaData]]. |
| `ForeignKey("users.id")` | String is `"<tablename>.<column>"` — the **SQL** names, not the Python class names. Creates the FK constraint. |
| `relationship("Product", ...)` | **Not a column.** A Python-level link that SQLAlchemy resolves via the FK. String is the **class** name (resolved lazily so you can reference classes defined later). |
| `back_populates="owner"` | Makes the two `relationship`s aware of each other so `user.products.append(p)` also sets `p.owner`. Must match the attribute name on the other side exactly. |
| `__repr__` | Optional; makes `print(user)` readable. |

## Column vs relationship — the thing beginners mix up

```
Product.owner_id   -> Column(Integer, ForeignKey("users.id"))   # a real column, holds an int
Product.owner      -> relationship("User", ...)                 # NOT a column, holds a User object
```

- The **column** is what's stored in the DB.
- The **relationship** is what you navigate in Python. SQLAlchemy loads it (lazily, on first access, by default) using the FK column.
- You need the FK column for the relationship to work; the relationship is optional sugar.

Details on navigating them: [[07 - Relationships One-to-Many]].

## Import note: 1.x vs 2.x

| | 1.x (README) | 2.x modern |
|---|---|---|
| Base | `from sqlalchemy.ext.declarative import declarative_base` | `from sqlalchemy.orm import DeclarativeBase` then `class Base(DeclarativeBase): pass` |
| Columns | `id = Column(Integer, primary_key=True)` | `id: Mapped[int] = mapped_column(primary_key=True)` |
| Relationship | `products = relationship("Product", back_populates="owner")` | `products: Mapped[list["Product"]] = relationship(back_populates="owner")` |

The README style still runs on 2.x (with a `MovedIn20Warning` for the `ext.declarative` import). The 2.x style gives real type hints — your IDE knows `user.products` is `list[Product]`.

Modern rewrite of the same models, for reference:

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    products: Mapped[list["Product"]] = relationship(back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str | None]
    price: Mapped[float]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="products")
```

## Creating the tables

```python
Base.metadata.create_all(engine)
```

Same semantics as Core's `metadata.create_all` — creates missing tables, never alters existing ones.

## Where this file is used

- [[05 - Sessions and sessionmaker]] imports `engine` and `Base` from here.
- [[Backend/Deployment/Integrating FastAPI, Pydantic, and SQLAlchemy/03 - Pydantic Schemas (Request and Response Models)|The FastAPI integration]] imports `Base, User, Product, engine` from here.

## Next

→ [[05 - Sessions and sessionmaker]]
