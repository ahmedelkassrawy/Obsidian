---
tags: [fastapi, pydantic, sqlalchemy, troubleshooting, errors, debugging]
aliases: [Gotchas, Troubleshooting, Common errors, DetachedInstanceError, check_same_thread, IntegrityError, orm_mode deprecated]
---

# 08 — Gotchas and Troubleshooting

> [!info] Not in the README
> This note is **added** — a catalogue of the errors you actually hit when wiring these three libraries, with the cause and the fix. Back to [[00 - Index]].

Search this note by the error text.

---

## `ImportError: cannot import name 'get_db' from 'database_orm'`

**Cause:** you're not running from the folder that contains `database_orm.py`, or the file is named differently (`database.py` from §4 vs `database_orm.py` from §5).
**Fix:** `cd` into the project folder before `uvicorn ...`, and make sure the three filenames match the imports in [[07 - Full Source Listing (copy-paste ready)]].

---

## `ModuleNotFoundError: No module named 'main_integrated'`

**Cause:** same as above — uvicorn imports by module name relative to the current directory.
**Fix:** run uvicorn from the folder that contains `main_integrated.py`, or use `--app-dir path/to/project`.

---

## `sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread`

**Cause:** FastAPI runs plain `def` endpoints in a threadpool; SQLite's default connection refuses to be used from a thread other than the one that created it. The README's `create_engine(DATABASE_URL)` doesn't disable that check.
**Fix:** in `models_orm.py`:

```python
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

Only needed for SQLite. Postgres/MySQL drivers don't have this restriction.

---

## `sqlalchemy.exc.OperationalError: no such table: users`

**Cause:** tables were never created. Either `Base.metadata.create_all(...)` is commented out (it is, in `models_orm.py` and `database_orm.py`), or it ran against a **different** SQLite file than the one the app is using (relative path `./test_orm.db` depends on the working directory).
**Fix:** keep the `Base.metadata.create_all(bind=engine)` call in `main_integrated.py` (the README does), and always start uvicorn from the same directory.

---

## `sqlalchemy.exc.IntegrityError: UNIQUE constraint failed: users.username`

**Cause:** `username` and `email` are `unique=True`. Creating a second "ada" raises on `db.commit()`. Uncaught, FastAPI returns a 500.
**Fix:** catch it and return a 409:

```python
from sqlalchemy.exc import IntegrityError

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    db.refresh(db_user)
    return db_user
```

Always `rollback()` before reusing the session after a failed commit.

---

## `sqlalchemy.orm.exc.DetachedInstanceError: Instance <User> is not bound to a Session; attribute refresh operation cannot proceed`

**Cause:** you returned an ORM object **after** its session closed, and Pydantic tried to read an expired attribute. Typically happens when you skip `db.refresh()` after `commit()`, or when you build the session yourself instead of via `Depends(get_db)`.
**Fix:** always `db.refresh(obj)` after `db.commit()` before returning; always get `db` through `Depends(get_db)` so it's still open during serialization.

---

## `pydantic.errors.PydanticUserError: ... from_attributes` / `TypeError: 'User' object is not subscriptable` / response `500` when returning an ORM object

**Cause:** `from_attributes = True` is missing on the response schema, so Pydantic expects a dict and gets an ORM instance.
**Fix:** add `model_config = ConfigDict(from_attributes=True)` (or `class Config: from_attributes = True`) to every `...Response` schema. Details in [[03 - Pydantic Schemas (Request and Response Models)]].

---

## Warning: `Support for class-based config is deprecated, use ConfigDict instead`

**Cause:** Pydantic V2 with the old `class Config:` block.
**Fix:** cosmetic — switch to `model_config = ConfigDict(from_attributes=True)`. Not an error.

---

## `AttributeError: 'UserCreate' object has no attribute 'dict'` **or** `'model_dump'`

**Cause:** Pydantic version mismatch. `.model_dump()` is V2; `.dict()` is V1.
**Fix:** `pip show pydantic`. On V2 use `model_dump()`; on V1 use `dict()`. The README targets V2.

---

## `orm_mode` has no effect / warning `'orm_mode' has been renamed to 'from_attributes'`

**Cause:** V1 setting name used on V2.
**Fix:** rename to `from_attributes`.

---

## `TypeError: 'description' is an invalid keyword argument for Product`

**Cause:** `Product(**product.model_dump())` — a field exists in the Pydantic schema but not on the ORM model (or is spelt differently).
**Fix:** keep schema field names identical to ORM column names, or pass fields explicitly.

---

## Endpoint returns `422 Unprocessable Entity` when you expected it to run

**Cause:** request body didn't match the `Create` schema (missing field, wrong type), **or** a path/query param couldn't be parsed (`/users/abc` with `user_id: int`).
**Fix:** read `detail[].loc` in the response — it names the exact field. See the example in [[05 - Running and Testing the App]].

---

## Endpoint returns `200` but the `db` parameter is a `<generator object get_db>`

**Cause:** you wrote `db = get_db()` inside the function or `db: Session = get_db()` as a default, instead of `Depends(get_db)`.
**Fix:** `db: Session = Depends(get_db)`. Only FastAPI should call `get_db`.

---

## Changes to a model (new column) don't appear in the DB

**Cause:** `create_all` only creates **missing tables**; it never alters existing ones.
**Fix (dev):** delete `test_orm.db` and restart. **Fix (real):** Alembic migrations — README §7 "Database Migrations" and §9.

---

## `--reload` restarts but SQLite file is locked / `database is locked`

**Cause:** a previous process (or a DB browser app) still holds the file.
**Fix:** close other processes/tools touching `test_orm.db`; SQLite allows one writer at a time.

---

## Swagger shows the endpoint but "Try it out" returns `CORS` errors from a frontend

**Cause:** not a FastAPI+SQLAlchemy issue; browsers block cross-origin calls.
**Fix:** `from fastapi.middleware.cors import CORSMiddleware` and `app.add_middleware(CORSMiddleware, allow_origins=[...], ...)`. Covered in README §7.

---

## Quick diagnosis flow

```
Request fails
├── 422 -> your JSON / URL param doesn't match the schema -> read detail[].loc
├── 404 -> your own HTTPException fired -> row really doesn't exist (check the id)
├── 409 -> (if you added it) unique constraint hit
└── 500 -> look at the uvicorn terminal traceback
       ├── IntegrityError        -> unique/FK violation -> catch + rollback
       ├── DetachedInstanceError -> missing refresh() or session closed too early
       ├── ProgrammingError (thread) -> add check_same_thread=False
       ├── OperationalError (no such table) -> create_all didn't run / wrong cwd
       └── PydanticUserError / not subscriptable -> missing from_attributes=True
```
