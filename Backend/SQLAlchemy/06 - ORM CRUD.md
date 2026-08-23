---
tags: [sqlalchemy, orm, crud, add, commit, refresh, query, filter]
aliases: [ORM CRUD, crud_orm.py, add commit refresh, db.query, update with ORM, delete with ORM]
source: https://github.com/h9-tec/AI_deployment#basic-crud-operations-with-orm
---

# 06 — ORM CRUD

> [!info] Source
> README §5 "Basic CRUD Operations with ORM". Back to [[00 - Index]] · Previous: [[05 - Sessions and sessionmaker]]

## The one-sentence version

Create = build object → `add` → `commit` → `refresh`. Read = `db.query(Model).filter(...)`. Update = change attributes → `commit`. Delete = `db.delete(obj)` → `commit`.

## The code

```python
# crud_orm.py
from sqlalchemy.orm import Session
from models_orm import User, Product, Base, engine
from database_orm import SessionLocal

Base.metadata.create_all(engine)

def create_user(db: Session, username: str, email: str):
    db_user = User(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_product_for_user(db: Session, product_name: str, description: str, price: float, user_id: int):
    db_product = Product(name=product_name, description=description, price=price, owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        user1 = create_user(db, "alice", "alice@example.com")
        user2 = create_user(db, "bob", "bob@example.com")
        print(f"Created users: {user1}, {user2}")

        product1 = create_product_for_user(db, "Keyboard", "Mechanical keyboard", 120.0, user1.id)
        product2 = create_product_for_user(db, "Mouse", "Gaming mouse", 50.0, user1.id)
        product3 = create_product_for_user(db, "Monitor", "4K Monitor", 300.0, user2.id)
        print(f"Created products: {product1}, {product2}, {product3}")

        retrieved_user1 = get_user(db, user1.id)
        print(f"\n{retrieved_user1.username}'s products:")
        for p in retrieved_user1.products:          # relationship -> lazy SELECT
            print(f"  - {p.name}")

        all_products = get_products(db)
        print("\nAll products:")
        for p in all_products:
            print(f"  - {p.name} (Owner: {p.owner.username})")   # relationship the other way
    finally:
        db.close()
```

Note the pattern: **every function takes `db: Session` as its first argument.** The caller owns the session's lifetime; the CRUD functions just use it. That's what makes these functions reusable from a script, a FastAPI endpoint, or a test.

## The write dance

```
User(...)        Python object only            id = None
db.add(obj)      session tracks it (pending)   id = None
db.commit()      INSERT sent, tx committed     id assigned in DB, attrs expired
db.refresh(obj)  SELECT back into the object   id visible, defaults loaded
```

- `refresh` is what makes `user1.id` usable right after `create_user` returns.
- Skip it and you *usually* still get the id (lazy reload on access) — until the session is closed, when you get `DetachedInstanceError` instead.

## Read patterns (legacy `query()` API)

| Want | Code |
|---|---|
| One by PK | `db.get(User, 1)` (2.x) or `db.query(User).get(1)` (legacy) |
| One by condition or `None` | `db.query(User).filter(User.email == e).first()` |
| Exactly one (raise otherwise) | `db.query(User).filter(...).one()` |
| Many | `db.query(User).all()` |
| Paged | `db.query(User).offset(skip).limit(limit).all()` |
| Count | `db.query(User).count()` |
| Exists | `db.query(User).filter(...).first() is not None` |

`filter(User.id == user_id)` — the `==` is overloaded by SQLAlchemy to build `WHERE users.id = ?`. `filter_by(id=user_id)` is the keyword shorthand.

2.0-style equivalents (`select()`) are in [[09 - Querying Data]].

## Update

Not in the README, but you'll need it:

```python
def update_user_email(db: Session, user_id: int, new_email: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    user.email = new_email       # just assign — the session notices ("dirty")
    db.commit()
    db.refresh(user)
    return user
```

Bulk update without loading objects:

```python
from sqlalchemy import update
db.execute(update(Product).where(Product.price < 10).values(price=10))
db.commit()
```

## Delete

```python
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True
```

> [!warning] Deleting a `User` that still has `Product`s
> With the README models, SQLite by default **doesn't enforce** FKs, so the products become orphans with a dangling `owner_id`. Postgres would raise `IntegrityError`. Fix by declaring `relationship("Product", back_populates="owner", cascade="all, delete-orphan")` on `User.products`, or `ForeignKey("users.id", ondelete="CASCADE")` on the column.

## Handling unique-constraint violations

```python
from sqlalchemy.exc import IntegrityError

try:
    db.commit()
except IntegrityError:
    db.rollback()
    raise ValueError("username or email already taken")
```

Always `rollback()` after a failed commit before reusing the session.

## Next

→ [[07 - Relationships One-to-Many]]
