---
tags: [fastapi, pydantic, sqlalchemy, cheatsheet, reference]
aliases: [Integration cheatsheet, FastAPI SQLAlchemy cheatsheet, CRUD cheatsheet]
---

# 09 — Cheatsheet

> [!info] One screen, no prose
> Condensed from every note in this folder. Back to [[00 - Index]].

## Setup (once)

```python
# models_orm.py
engine = create_engine("sqlite:///./test_orm.db", connect_args={"check_same_thread": False})
Base = declarative_base()
class User(Base): __tablename__ = "users"; id = Column(Integer, primary_key=True); ...

# database_orm.py
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:     yield db
    finally: db.close()

# main.py
Base.metadata.create_all(bind=engine)
app = FastAPI()
```

## Schemas

```python
class XCreate(BaseModel):            # client -> API, no id
    field: str
    optional_field: str | None = None

class XResponse(BaseModel):          # API -> client, has id
    model_config = ConfigDict(from_attributes=True)   # <- REQUIRED to return ORM objects
    id: int
    field: str
```

## Endpoint templates

```python
# CREATE
@app.post("/x/", response_model=XResponse, status_code=status.HTTP_201_CREATED)
def create_x(x: XCreate, db: Session = Depends(get_db)):
    obj = X(**x.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

# LIST (paginated)
@app.get("/x/", response_model=list[XResponse])
def read_xs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(X).offset(skip).limit(limit).all()

# GET ONE or 404
@app.get("/x/{x_id}", response_model=XResponse)
def read_x(x_id: int, db: Session = Depends(get_db)):
    obj = db.query(X).filter(X.id == x_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="X not found")
    return obj

# CREATE CHILD under parent
@app.post("/parents/{parent_id}/x/", response_model=XResponse, status_code=201)
def create_x_for_parent(parent_id: int, x: XCreate, db: Session = Depends(get_db)):
    if db.query(Parent).filter(Parent.id == parent_id).first() is None:
        raise HTTPException(404, "Parent not found")
    obj = X(**x.model_dump(), parent_id=parent_id)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
```

## Where parameters come from

| Signature | Source |
|---|---|
| name in `{path}` | URL path |
| `int`/`str`/`bool` not in path | query string |
| `BaseModel` subclass | JSON body |
| `= Depends(fn)` | dependency |

## The write dance

`X(...)` → `db.add` → `db.commit` → `db.refresh` → `return`

## Version names

| Thing | Pydantic V1 | Pydantic V2 |
|---|---|---|
| ORM attribute reading | `orm_mode = True` | `from_attributes = True` |
| Model → dict | `.dict()` | `.model_dump()` |
| Config style | `class Config:` | `model_config = ConfigDict(...)` |

## Run

```bash
uvicorn main_integrated:app --reload     # docs at http://127.0.0.1:8000/docs
```

## Status codes used

| Code | When |
|---|---|
| 200 | default success |
| 201 | created (set via `status_code=`) |
| 404 | `raise HTTPException(404, ...)` |
| 409 | unique-constraint conflict (add yourself) |
| 422 | Pydantic validation failed (automatic) |
| 500 | uncaught exception — check terminal |

## Full details

[[02 - Database Session Dependency (get_db)]] · [[03 - Pydantic Schemas (Request and Response Models)]] · [[04 - API Endpoints with Database Operations]] · [[06 - Request vs Response Models Explained]] · [[08 - Gotchas and Troubleshooting]]
