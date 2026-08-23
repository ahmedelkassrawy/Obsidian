---
tags: [fastapi, pydantic, sqlalchemy, source-code, reference]
aliases: [Full source, Complete code, models_orm.py, database_orm.py, main_integrated.py, schemas.py]
source: https://github.com/h9-tec/AI_deployment#6-integrating-fastapi-pydantic-and-sqlalchemy
---

# 07 — Full Source Listing (copy-paste ready)

> [!info] Source
> Assembled from README §5 (`models_orm.py`, `database_orm.py`) and §6 (`main_integrated.py`).
> Back to [[00 - Index]].

Two layouts below. **A** is exactly what the README ships (three files). **B** is the same code split the way the archived note labelled it (`schemas.py` + `main.py`), which is closer to how real projects are organised.

---

## Layout A — as in the README (3 files)

```
project/
├── models_orm.py        # engine, Base, User, Product
├── database_orm.py      # SessionLocal, get_db
└── main_integrated.py   # schemas + FastAPI app + endpoints
```

### `models_orm.py`

```python
# models_orm.py

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the database URL (using SQLite for simplicity)
DATABASE_URL = "sqlite:///./test_orm.db"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a declarative base
Base = declarative_base()

# Define ORM Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)

    # Define a relationship to products (one-to-many)
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

    # Define a relationship to User (many-to-one)
    owner = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

# Create tables in the database
# Base.metadata.create_all(engine)
```

> [!note] `sqlalchemy.ext.declarative.declarative_base` is the 1.x import. On SQLAlchemy 2.x it still works but warns; the modern import is `from sqlalchemy.orm import declarative_base` (or subclass `DeclarativeBase`). Also: when running with SQLite + FastAPI you'll typically add `connect_args={"check_same_thread": False}` to `create_engine` — see [[08 - Gotchas and Troubleshooting]].

### `database_orm.py`

```python
# database_orm.py

from sqlalchemy.orm import sessionmaker
from models_orm import engine, Base

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables (run this once to set up your database)
# Base.metadata.create_all(engine)
```

### `main_integrated.py`

```python
# main_integrated.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import Pydantic models (from models.py or models_orm.py if you prefer)
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True # Pydantic V2: orm_mode = True in Pydantic V1

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    owner_id: int

    class Config:
        from_attributes = True # Pydantic V2: orm_mode = True in Pydantic V1

# Import SQLAlchemy ORM models and session setup
from models_orm import Base, User, Product, engine
from database_orm import get_db # This is our dependency

# Create all tables (run once)
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/{user_id}/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_for_user(
    user_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_product = Product(**product.model_dump(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

### Run

```bash
uvicorn main_integrated:app --reload
```

---

## Layout B — split into `schemas.py` + `main.py` (same code, tidier)

```
project/
├── models_orm.py        # unchanged from Layout A
├── database_orm.py      # unchanged from Layout A
├── schemas.py           # Pydantic only
└── main.py              # FastAPI only
```

### `schemas.py`

```python
# schemas.py
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    price: float
    owner_id: int
```

### `main.py`

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models_orm import Base, User, Product, engine
from database_orm import get_db
from schemas import UserCreate, UserResponse, ProductCreate, ProductResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/{user_id}/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_for_user(user_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.id == user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_product = Product(**product.model_dump(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()


@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

Differences from Layout A (all cosmetic, behaviour identical):

- `ConfigDict(from_attributes=True)` instead of `class Config:` (no deprecation warning on Pydantic V2).
- `list[...]` instead of `typing.List[...]`.
- `User(**user.model_dump())` for consistency with the product endpoint.

### Run

```bash
uvicorn main:app --reload
```

---

## `requirements.txt`

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
```
