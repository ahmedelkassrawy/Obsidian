---
tags: [fastapi, sqlalchemy, crud, endpoints, pagination, http-404, foreign-key]
aliases: [API endpoints, CRUD endpoints, create_user, read_users, read_user, create_product_for_user, read_products, read_product, add commit refresh]
source: https://github.com/h9-tec/AI_deployment#creating-api-endpoints-with-database-operations
---

# 04 — API Endpoints with Database Operations

> [!info] Source
> https://github.com/h9-tec/AI_deployment#creating-api-endpoints-with-database-operations
> Back to [[00 - Index]] · Previous: [[03 - Pydantic Schemas (Request and Response Models)]]

## The one-sentence version

Six endpoints, each following the same recipe: **declare the schema in the signature → get `db` via `Depends(get_db)` → run a query or an add/commit/refresh → return an ORM object → let `response_model` turn it into JSON.**

## What the README says

> Let's create API endpoints for users and products, demonstrating how to use the database session dependency and Pydantic models.

## The full code (second half of `main_integrated.py`)

```python
# main_integrated.py (continued)

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

## How FastAPI decides where each parameter comes from

This is the thing that confuses people most, so here it is explicitly:

| Parameter looks like | FastAPI reads it from | Example |
|---|---|---|
| Name matches a `{placeholder}` in the path | **URL path** | `user_id: int` in `/users/{user_id}` |
| Simple type (`int`, `str`, `bool`) **not** in the path | **Query string** | `skip: int = 0` → `?skip=20` |
| A Pydantic `BaseModel` subclass | **JSON request body** | `user: UserCreate` |
| Has `= Depends(...)` | **Dependency injection** | `db: Session = Depends(get_db)` |

No decorators or extra annotations needed — the type alone decides.

---

## create_user — POST /users/

```python
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

| Line | What it does |
|---|---|
| `@app.post("/users/", ...)` | Register this function for `POST /users/`. |
| `response_model=UserResponse` | Whatever the function returns gets filtered/validated through `UserResponse` before going out. |
| `status_code=status.HTTP_201_CREATED` | Default for a successful response is 200; REST convention says "created a resource" → 201. |
| `user: UserCreate` | Request body, already validated. If the JSON is missing `email`, the function never runs — client gets 422. |
| `db_user = User(username=..., email=...)` | Build a SQLAlchemy ORM instance. **Nothing hits the DB yet.** `id` is still `None`. |
| `db.add(db_user)` | Stage it in the session ("pending"). Still nothing in the DB. |
| `db.commit()` | Flush the INSERT and commit the transaction. Now the row exists and SQLite assigned an `id`. |
| `db.refresh(db_user)` | Re-SELECT the row and update the Python object, so `db_user.id` (and any DB defaults) are populated. |
| `return db_user` | Return the ORM object. `from_attributes=True` on `UserResponse` lets FastAPI serialize it. |

### The add, commit, refresh dance

Why three calls and not one?

```
User(...)      -> Python object only            id = None
db.add()       -> session tracks it (pending)   id = None
db.commit()    -> INSERT sent, transaction done id assigned in DB
db.refresh()   -> SELECT back into the object   id visible in Python
```

- After `commit()`, SQLAlchemy **expires** the object's attributes by default. Touching `db_user.id` would trigger a lazy reload anyway, but `refresh()` makes it explicit and guarantees server-side defaults (timestamps, etc.) are loaded **before** the session closes.
- If you skip `refresh()` and the session is closed before serialization, you can hit `DetachedInstanceError` — see [[08 - Gotchas and Troubleshooting]].

### Example call

```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "ada", "email": "ada@example.com"}'
```

Response `201`:

```json
{"id": 1, "username": "ada", "email": "ada@example.com"}
```

---

## read_users — GET /users/

```python
@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
```

| Line | What it does |
|---|---|
| `response_model=List[UserResponse]` | The function returns a list; each item is serialized through `UserResponse`. |
| `skip: int = 0, limit: int = 100` | Query parameters with defaults → `GET /users/?skip=10&limit=5`. Defaults make them optional. |
| `db.query(User)` | Start a SELECT on the `users` table. |
| `.offset(skip).limit(limit)` | SQL `OFFSET skip LIMIT limit` — classic offset pagination. |
| `.all()` | Execute and return a Python list of `User` objects. Empty table → `[]`, not an error. |

> [!note] Offset pagination scales badly on huge tables (the DB still scans the skipped rows). Fine for learning; for millions of rows look at keyset/cursor pagination.

### Example

```bash
curl "http://127.0.0.1:8000/users/?skip=0&limit=2"
```

---

## read_user — GET /users/{user_id}

```python
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

| Line | What it does |
|---|---|
| `"/users/{user_id}"` | Path parameter. `GET /users/abc` → 422 because `user_id: int` fails to parse. |
| `.filter(User.id == user_id)` | SQL `WHERE users.id = :user_id`. The `==` here is overloaded by SQLAlchemy to build SQL, not compare Python values. |
| `.first()` | Execute with `LIMIT 1`; returns the object **or `None`**. (Contrast `.one()`, which raises if 0 or >1 rows.) |
| `if user is None: raise HTTPException(404, ...)` | The standard "not found" pattern. The client gets `{"detail": "User not found"}` with status 404. |

### Why `raise`, not `return`?

`HTTPException` is an exception on purpose: raising it **aborts** the endpoint immediately, skips `response_model` validation, and still runs `get_db`'s `finally` so the session is closed. Returning a dict with an error would get validated against `UserResponse` and fail.

---

## create_product_for_user — POST /users/{user_id}/products/

```python
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
```

This one combines **all three** parameter sources: path (`user_id`), body (`product`), dependency (`db`).

| Line | What it does |
|---|---|
| Look up `db_user` first | Verify the parent exists before inserting a child. Otherwise SQLite (with FK enforcement off by default) would happily insert an orphan product. |
| `product.model_dump()` | Pydantic V2 method → plain dict `{"name": ..., "description": ..., "price": ...}`. (V1 name: `.dict()`.) |
| `Product(**product.model_dump(), owner_id=user_id)` | Unpack the dict as keyword args and add `owner_id` from the URL. Works because the Pydantic field names **match the ORM column names exactly**. |
| add / commit / refresh | Same dance as `create_user`. |

### Why `**model_dump()` instead of listing fields?

`User(username=user.username, email=user.email)` is fine for 2 fields. For 10 fields it's repetitive and easy to forget one. `**product.model_dump()` passes everything. The trade-off: if the schema gains a field the ORM doesn't have, you get `TypeError: 'foo' is an invalid keyword argument for Product` — which is a useful early failure.

### Example

```bash
curl -X POST http://127.0.0.1:8000/users/1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "price": 9.99}'
```

Response `201`:

```json
{"id": 1, "name": "Widget", "description": null, "price": 9.99, "owner_id": 1}
```

---

## read_products — GET /products/

```python
@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
```

Identical shape to `read_users`, different table. Same pagination.

---

## read_product — GET /products/{product_id}

```python
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

Identical shape to `read_user`.

---

## The pattern, abstracted

Every endpoint in this file is one of two templates. Once you see it you can write any CRUD endpoint from memory.

**Read template**

```python
@app.get("/things/{thing_id}", response_model=ThingResponse)
def read_thing(thing_id: int, db: Session = Depends(get_db)):
    obj = db.query(Thing).filter(Thing.id == thing_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Thing not found")
    return obj
```

**Create template**

```python
@app.post("/things/", response_model=ThingResponse, status_code=status.HTTP_201_CREATED)
def create_thing(thing: ThingCreate, db: Session = Depends(get_db)):
    obj = Thing(**thing.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
```

## What the README does NOT cover (left as exercises)

- `PUT`/`PATCH` update endpoints (fetch → set attributes → commit → refresh).
- `DELETE` endpoints (fetch → `db.delete(obj)` → commit → return 204).
- Handling the `IntegrityError` you get when `username` or `email` violates `unique=True` (see [[08 - Gotchas and Troubleshooting]]).
- Returning a user **with** their nested products (needs a `products: list[ProductResponse]` field on `UserResponse`).

## Next

→ [[05 - Running and Testing the App]]
