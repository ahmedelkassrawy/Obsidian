---
tags: [sqlalchemy, cheatsheet, reference, 2.0-style]
aliases: [SQLAlchemy cheatsheet, SQLAlchemy quick reference, SQLAlchemy 2.0 cheatsheet]
---

# 12 — Cheatsheet (2.0 style)

> [!info] One screen, no prose. Back to [[00 - Index]]. Legacy `query()` equivalents: [[09 - Querying Data#Legacy query() vs 2.0 select()]].

## Project layout

```
db/
├── database.py   engine, SessionLocal, get_db (context manager), get_db_dep (FastAPI)
├── models.py     Base + models — no engine here
└── crud.py       functions taking db: Session, never committing
```

## database.py

```python
engine = create_engine(URL, pool_pre_ping=True)                      # SQLite: connect_args={"check_same_thread": False}
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

@contextmanager
def get_db():
    with SessionLocal() as s:
        try:     yield s; s.commit()
        except Exception: s.rollback(); raise

def get_db_dep():            # FastAPI: same body, NO decorator
    with SessionLocal() as s:
        try:     yield s; s.commit()
        except Exception: s.rollback(); raise
```

Async: `create_async_engine`, `async_sessionmaker(engine, expire_on_commit=False)`, `@asynccontextmanager async def get_db()`, `async with get_db() as db`.

## models.py

```python
class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    products: Mapped[list["Product"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None]
    price: Mapped[float]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner: Mapped["User"] = relationship(back_populates="products")
```

## CRUD (inside `with get_db() as db:`)

```python
u = User(username="ada", email="a@x"); db.add(u); db.flush()      # create, id available
db.add_all([Product(...), Product(...)])                            # create many (ORM)
db.execute(insert(Product), [dict, dict, ...])                      # create thousands (Core bulk)
db.get(User, 1)                                                     # read by PK
db.execute(select(User).where(User.email == e)).scalar_one_or_none()  # read one / None
db.execute(select(User).order_by(User.id).offset(s).limit(n)).scalars().all()  # page
db.execute(select(User).options(selectinload(User.products))).scalars().all()  # no N+1
u.email = "new"                                                     # update
db.delete(u)                                                        # delete
db.execute(update(Product).where(Product.price < 10).values(price=10))   # bulk update
db.execute(delete(Product).where(Product.owner_id == 42))           # bulk delete
# commit: automatic on block exit
```

Async: prefix `execute/get/flush/delete/refresh/commit` with `await`; `add`, `.scalars()`, `.scalar_one_or_none()` stay sync.

## Filters

`==` `!=` `>` `<` `.between()` `.in_()` `.not_in()` `.is_(None)` `.is_not(None)` `.like()` `.ilike()` `.startswith()` `.contains()` · `and_()` `or_()` `not_()` · `order_by(X.desc())` · `func.count()`

## Results

`scalar_one_or_none()` one obj/None · `scalar_one()` exactly one · `scalars().all()` objs · `scalar()` one value · `first()` row/None · `all()` rows (tuples!) · `mappings()` dicts

## Relationships

```python
# one-to-many: FK on the many side + relationship on both sides, back_populates both ways
# many-to-many (no extra cols):
link = Table("a_b", Base.metadata, Column("a_id", ForeignKey("a.id"), primary_key=True),
                                   Column("b_id", ForeignKey("b.id"), primary_key=True))
bs: Mapped[list["B"]] = relationship(secondary=link, back_populates="as_")
# many-to-many with extra cols: make the link a model (association object) and insert rows explicitly
```

## Core (raw / one-off)

```python
with engine.begin() as conn:                           # auto-commit
    conn.execute(text("SELECT 1")).scalar()
    conn.execute(insert(t).values(...)).inserted_primary_key[0]
```

## Tables

```python
Base.metadata.create_all(engine)                                   # dev; never alters
async with engine.begin() as c: await c.run_sync(Base.metadata.create_all)
# real projects: alembic revision --autogenerate && alembic upgrade head
```

## Errors → fix

`IntegrityError` → catch outside `with get_db()`, 409 · `PendingRollbackError` → `rollback()` first · `DetachedInstanceError` → `expire_on_commit=False` / eager-load · `MissingGreenlet` → eager-load / `expire_on_commit=False` · `check_same_thread` → `connect_args` · `db = get_db()` gives a context-manager object → `with get_db() as db` · tuples not objects → `.scalars()`
