---
tags: [sqlalchemy, cheatsheet, reference]
aliases: [SQLAlchemy cheatsheet, SQLAlchemy quick reference]
---

# 12 — Cheatsheet

> [!info] One screen, no prose. Back to [[00 - Index]].

## Engine

```python
from sqlalchemy import create_engine, text
engine = create_engine("sqlite:///./test.db", echo=False,
                       connect_args={"check_same_thread": False})   # SQLite+threads only
with engine.connect() as conn:
    conn.execute(text("SELECT 1")).scalar()
with engine.begin() as conn:          # auto-commit on success
    conn.execute(insert(t).values(...))
```

URLs: `sqlite:///./f.db` · `postgresql://u:p@h:5432/db` · `postgresql+asyncpg://…` · `mysql+pymysql://…`

## Core

```python
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, select, update, delete
metadata = MetaData()
t = Table("users", metadata, Column("id", Integer, primary_key=True), Column("username", String, unique=True))
metadata.create_all(engine)

conn.execute(insert(t).values(username="ada")).inserted_primary_key[0]
conn.execute(select(t).where(t.c.id == 1)).fetchone()
conn.execute(update(t).where(t.c.id == 1).values(username="ada2"))
conn.execute(delete(t).where(t.c.id == 1))
conn.commit()
```

## ORM models

```python
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")

Base.metadata.create_all(engine)
```

## Session

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:     yield db
    finally: db.close()
```

## ORM CRUD

```python
obj = User(username="ada"); db.add(obj); db.commit(); db.refresh(obj)   # create
db.query(User).filter(User.id == 1).first()                              # read one / None
db.query(User).offset(0).limit(10).all()                                 # read many
obj.username = "new"; db.commit()                                        # update
db.delete(obj); db.commit()                                              # delete
db.get(User, 1)                                                          # by PK (2.x)
```

## 2.0 select

```python
db.execute(select(User).where(User.id == 1)).scalar_one_or_none()
db.execute(select(User)).scalars().all()
db.execute(select(User).join(Product).where(Product.name == "Keyboard")).scalars().all()
db.execute(select(User).options(selectinload(User.products))).scalars().all()
```

## Filters

`==` `!=` `>` `<` `.between()` `.in_()` `.not_in()` `.is_(None)` `.is_not(None)` `.like()` `.ilike()` `.startswith()` `.contains()` · `and_()` `or_()` `not_()`

## Results

`scalar()` one value · `scalar_one_or_none()` one obj/None · `scalars().all()` list of objs · `first()` row/None · `all()` rows · `mappings()` dicts

## Many-to-many

```python
link = Table("a_b", Base.metadata, Column("a_id", ForeignKey("a.id"), primary_key=True),
                                    Column("b_id", ForeignKey("b.id"), primary_key=True))
class A(Base): bs = relationship("B", secondary=link, back_populates="as_")
# with extra columns -> make the link a class (association object) and insert rows explicitly
```

## Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
engine = create_async_engine("sqlite+aiosqlite:///./t.db")
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async def get_db():
    async with AsyncSessionLocal() as s: yield s

r = await db.execute(select(User).where(User.id == 1)); u = r.scalar_one_or_none()
db.add(obj); await db.commit(); await db.refresh(obj)
async with engine.begin() as c: await c.run_sync(Base.metadata.create_all)
```

## Errors → fix

`IntegrityError` → `db.rollback()`, return 409 · `DetachedInstanceError` → `refresh` before close · `check_same_thread` → `connect_args` · `MissingGreenlet` → eager-load / `expire_on_commit=False` · `PendingRollbackError` → call `rollback()` first
