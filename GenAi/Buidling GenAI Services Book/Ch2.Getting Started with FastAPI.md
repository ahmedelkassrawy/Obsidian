---
date: 2026-09-11
tags: [fastapi, genai, book-notes, python, backend]
source: "Building Generative AI Services with FastAPI (O'Reilly) — Chapter 2"
description: Ch2 notes — FastAPI setup, features, project structures, onion architecture, limitations, tooling. Code examples verified against the official FastAPI docs (fastapi.tiangolo.com) and corrected for Pydantic v2.
---
# Ch2 — Getting Started with FastAPI

FastAPI is an **ASGI** (asynchronous) web framework for lean, high-concurrency APIs. It's a wrapper over **Starlette** (web layer) + **Pydantic** (data validation), and gives you auto OpenAPI/Swagger docs, data validation, and a dependency-injection system out of the box.

> **Note on the code below:** the book targets **Python 3.11 + Pydantic v2**. A few book snippets use old/partial code — I corrected those against the official docs and flagged each fix with ⚠️.

---

## 1. Setup + first server

```bash
# Windows (conda)
conda create -n genaiservice python=3.11
conda activate genaiservice

# macOS/Linux (venv)
python3 -m venv .venv
source .venv/bin/activate

# core packages
pip install "fastapi[standard]" uvicorn openai
```
`uvicorn` = the ASGI web server FastAPI runs on. `fastapi[standard]` pulls in Starlette + Pydantic + the `fastapi` CLI.

**Example 2-1 — a minimal server serving GPT-4o** (verified; correct as written):
```python
# main.py
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()                                   # the application object
openai_client = OpenAI(api_key="your_api_key")    # needs a real key to call OpenAI

@app.get("/")
def root_controller():
    return {"status": "healthy"}                  # dict is auto-serialized to JSON

@app.get("/chat")
def chat_controller(prompt: str = "Inspire me"):  # `prompt` becomes a query param
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    statement = response.choices[0].message.content
    return {"statement": statement}
```
Run it:
```bash
fastapi dev          # dev server + auto-reload, at http://127.0.0.1:8000
```
- `/` → `{"status": "healthy"}`, `/chat?prompt=...` → an OpenAI reply.
- Auto docs (Swagger UI) at **/docs**; the OpenAPI spec at `/openapi.json`.
- `@app.get(...)` turns a function into an HTTP endpoint. A returned dict/list is **serialized to JSON** automatically (HTTP only moves text/binary).

---

## 2. Dependency Injection (DI) — the heart of FastAPI

DI = the **inversion-of-control** pattern: break logic into small functions and *inject* them into route handlers via `Depends()`. Buys you **decoupling** (swap DB/auth/pagination without touching endpoints), **hierarchical graphs** (a dependency can depend on other dependencies), and **per-request caching** (a dependency runs once per request; its result is reused).

**Example 2-4 — a reusable pagination dependency** (verified; correct):
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def paginate(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/messages")
def list_messages_controller(pagination: dict = Depends(paginate)):
    return ...  # filter/paginate using pagination["skip"] / ["limit"]

@app.get("/conversations")
def list_conversations_controller(pagination: dict = Depends(paginate)):
    return ...
```
FastAPI also **exposes the dependency's params** (`skip`, `limit`) on the endpoint automatically — so `/messages?skip=0&limit=10` just works.

**Example 2-5 — a DB session dependency with `yield`** (verified against fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield; ⚠️ fixed the route path to a leading `/`):
```python
from fastapi import FastAPI, Depends

def get_db():
    db = ...            # create a DB session
    try:
        yield db        # hand the session to the route
    finally:
        db.close()      # always cleaned up after the request

app = FastAPI()

@app.get("/users/{email}/messages")   # ⚠️ book printed "users/..." — needs a leading /
def get_current_user_messages(email: str, db=Depends(get_db)):
    user = db.query(...)       # same session reused
    messages = db.query(...)   # same session reused (cached per request)
    return messages
```
The `yield` pattern = setup before `yield`, cleanup in `finally` after the response. The session is created once and **reused for the whole request**.

**Hierarchical graph:** dependencies inject into other dependencies (e.g. `get_token → get_user → get_user_permissions`) — great for cached auth/authorization flows.

---

## 3. Data validation with Pydantic

Define Pydantic schemas for request/response data to get automatic validation.

**Example 2-2 — password-policy validation** (⚠️ **corrected to Pydantic v2**: the book used v1 `@validator` and returned `user.name` which doesn't exist; v2 uses `@field_validator` + `@classmethod`):
```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel, field_validator   # ⚠️ book imported `validator` (v1) — v2 uses field_validator

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")                  # ⚠️ was @validator('password')
    @classmethod                                   # ⚠️ v2 field validators are classmethods
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        return value

app = FastAPI()

@app.post("/users")
async def create_user_controller(user: UserCreate):
    return {"name": user.username, "message": "Account successfully created"}  # ⚠️ was user.name (no such field)
```
A failed validation → FastAPI returns a **422** with the error detail automatically. Pydantic also validates richer types (`EmailStr`, `AnyUrl`, `UUID`, …). (v1's `@validator` still runs in v2 but is deprecated — use `field_validator`.)

---

## 4. Auto docs + redirect to /docs

**Example 2-3 — redirect base `/` to the docs page** (⚠️ added the missing `status` import; `RedirectResponse(url, status_code=...)` verified against the docs):
```python
# main.py
from fastapi import FastAPI, status                 # ⚠️ book used status.* without importing it
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/", include_in_schema=False)               # hidden from the OpenAPI schema
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)
```
⚠️ **Security:** only do this in dev. In production, if the API is public, **disable the redirect and hide `/docs`** (e.g. `FastAPI(docs_url=None)`), or have `/` return your API version instead.

---

## 5. Other features (no code, from the chapter)
- **Sync vs async routes:** `async def` runs on the main event loop; a plain `def` route runs on a **thread-pool worker**. Threads add overhead → too many sync routes limits scalability. (Detail in Ch5.)
- **Background tasks:** built-in — accept a request, queue slow work (e.g. process a doc into a vector DB), return immediately. No Celery needed for simple cases.
- **Middleware + CORS:** intercept request/response to add headers, logging, checks.
- **Lifespan events:** load heavy AI models / DB pools **once at startup**, reuse across requests, clean up at shutdown. (Replaces the old startup/shutdown events.)
- **WebSocket / SSE / GraphQL (strawberry):** for streaming model output and dynamic schemas.
- Auto-serialization, a rich plug-in ecosystem (Awesome FastAPI), security components you wire yourself (or FastAPI Users).

---

## 6. Project structures (evolve flat → nested → modular)

**Flat** — everything at root. Best for MVPs/microservices. Simple, no circular deps; hard to maintain as it grows.
```text
flat-project
├── app
│   ├── services.py
│   ├── database.py
│   ├── models.py
│   ├── routers.py
│   └── main.py
├── requirements.txt
├── .env
└── .gitignore
```

**Nested** — group by *file type* (a `models/`, `routers/`, `services/` package each). FastAPI's official rec for larger apps. Pitfall: **shotgun updates** — one feature change edits files across many folders (ambiguous coupling).
```text
nested-project
├── app
│   ├── main.py
│   ├── dependencies.py
│   ├── services/   (users.py, profiles.py)
│   ├── models/     (users.py, profiles.py)
│   └── routers/    (users.py, profiles.py)
```

**Modular** (Netflix Dispatch style) — group by *domain/feature*. All "users" code (models, routers, services, deps) in one `users` package. High encapsulation; add/remove/refactor a feature without touching unrelated code. **Preferred for large GenAI services.**
```text
modular-project
├── app
│   ├── modules
│   │   ├── auth      (routers.py, models.py, dependencies.py, guards.py, services.py)
│   │   └── users     (router.py, models.py, dependencies.py, services.py, mappers.py, pipes.py)
│   ├── providers/    (email.py, stripe.py)
│   ├── settings.py   # global config
│   ├── middlewares.py
│   ├── models.py     # global models
│   ├── exceptions.py
│   └── main.py
```
**Rule of thumb:** start flat, reorganize progressively as complexity grows. If you can't justify the file layout to another dev, rethink it.

---

## 7. Onion / layered architecture

Uses the **dependency-inversion principle**: outer layers depend inward; the core (domain) depends on nothing. Layers, outer → inner:
- **API routers** (`APIRouter`) — group controllers, apply shared logic.
- **Controllers / route handlers** — handle HTTP; stay lean; *inject* services/providers.
- **Services** (orchestrate internal business logic) & **Providers** (talk to external systems: OpenAI, Stripe, email).
- **Repositories** (data adapters) — abstract the DB via CRUD, keep SQL/ORM out of controllers.
- **Schemas/models** (center) — type-safety + validation on data flowing through.

**Cross-cutting:** DTOs (Pydantic request/response models), mappers (convert between layers, e.g. `UserRequest` → `UserInDB`), guards (auth as dependencies), pipes (cleaners/parsers), middleware, exception filters.

---

## 8. Limitations (why FastAPI alone isn't enough for heavy AI)
- **GIL / event-loop blocking:** heavy CPU/GPU inference blocks the loop even in an `async` route → freezes other requests. Offload to **multiprocessing** or a serving framework (**BentoML**).
- **No shared model memory** across workers → each horizontal worker loads its own copy (memory + cost bottleneck).
- **Limited thread pool** (AnyIO ~40 threads default).
- **No micro-batching** of inference requests; **can't split CPU/GPU** work efficiently.
- **Takeaway:** serve heavy models *outside* FastAPI (BentoML), let FastAPI handle security, business logic, and I/O.

---

## 9. Tooling
- **Env/deps:** `requirements.txt`+pip (simple) · `uv`/Conda (pip workflows) · Poetry (complex).
- **Lint/format:** **Ruff** (fast, replaces isort/black/flake8) · Autoflake · Flake8 · isort · Black.
- **Types:** **Mypy** (static type checker) · Pylance.
- **Security:** **Bandit** (hard-coded secrets), **Safety** (vulnerable deps).
- **Logging:** Loguru. Run all via pre-commit hooks before committing.

---

## Verification note
Code checked against the official FastAPI docs (fastapi.tiangolo.com): **dependencies-with-yield** and **custom-response / RedirectResponse** confirmed. Pydantic validation updated from the book's v1 `@validator` to **v2 `field_validator`** (the book states it targets Pydantic v2). All ⚠️ marks above are my corrections to the book's printed snippets.
