---
tags: [fastapi, uvicorn, swagger, openapi, testing, curl]
aliases: [Run the integrated app, uvicorn main_integrated, Swagger docs, Test the API]
source: https://github.com/h9-tec/AI_deployment#creating-api-endpoints-with-database-operations
---

# 05 — Running and Testing the App

> [!info] Source
> Tail of https://github.com/h9-tec/AI_deployment#creating-api-endpoints-with-database-operations
> Back to [[00 - Index]] · Previous: [[04 - API Endpoints with Database Operations]]

## What the README says

> To run this integrated application, save the code above as `main_integrated.py` (or merge it into your `main.py` if you prefer) and run:
>
> ```bash
> uvicorn main_integrated:app --reload
> ```
>
> Then, navigate to `http://127.0.0.1:8000/docs` to interact with the API.

## Prerequisites checklist

- [ ] Python 3.10+ (the schemas use `str | None`; on 3.9 change to `Optional[str]`).
- [ ] Installed: `pip install fastapi "uvicorn[standard]" sqlalchemy pydantic`
- [ ] Three files in the **same folder**: `models_orm.py`, `database_orm.py`, `main_integrated.py` (see [[07 - Full Source Listing (copy-paste ready)]]).
- [ ] Run from **that folder** so `from models_orm import ...` resolves.

## Start the server

```bash
uvicorn main_integrated:app --reload
```

Breaking the command down:

| Part | Meaning |
|---|---|
| `uvicorn` | The ASGI server that actually listens on a port and hands requests to FastAPI. |
| `main_integrated` | Python module name = filename without `.py`. |
| `:app` | The variable inside that module holding the `FastAPI()` instance. |
| `--reload` | Watch files and restart on change. **Dev only** — never in production. |

Useful extras:

```bash
uvicorn main_integrated:app --reload --port 8001          # different port
uvicorn main_integrated:app --host 0.0.0.0 --port 8000     # reachable from LAN / Docker
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Application startup complete.
```

On first start a `test_orm.db` SQLite file appears in the folder (created by `Base.metadata.create_all`).

## The auto-generated docs

| URL | What |
|---|---|
| `http://127.0.0.1:8000/docs` | **Swagger UI** — interactive; click an endpoint → "Try it out" → fill JSON → Execute. |
| `http://127.0.0.1:8000/redoc` | ReDoc — read-only, nicer for browsing. |
| `http://127.0.0.1:8000/openapi.json` | The raw OpenAPI schema both UIs render. |

The request/response examples shown in Swagger come **directly from your Pydantic schemas** — that's the "Automatic Documentation" benefit described in [[06 - Request vs Response Models Explained]].

## A full manual test run (curl)

Run these in order; each builds on the previous.

```bash
# 1. Create a user -> expect 201 and an id
curl -s -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "ada", "email": "ada@example.com"}'

# 2. List users -> expect a list with ada
curl -s http://127.0.0.1:8000/users/

# 3. Get user 1 -> expect ada
curl -s http://127.0.0.1:8000/users/1

# 4. Get user 999 -> expect 404 {"detail":"User not found"}
curl -s -i http://127.0.0.1:8000/users/999

# 5. Create a product for user 1 -> expect 201 with owner_id 1
curl -s -X POST http://127.0.0.1:8000/users/1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "description": "A thing", "price": 9.99}'

# 6. Create a product for a missing user -> expect 404
curl -s -i -X POST http://127.0.0.1:8000/users/999/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Ghost", "price": 1}'

# 7. Send bad input -> expect 422 with a field-level error
curl -s -i -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "bob"}'

# 8. Pagination
curl -s "http://127.0.0.1:8000/products/?skip=0&limit=10"
```

PowerShell users: replace `curl` with `curl.exe` (plain `curl` is an alias for `Invoke-WebRequest` on Windows PowerShell 5.1 and has different flags).

## What a 422 looks like (step 7)

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "email"],
      "msg": "Field required",
      "input": {"username": "bob"}
    }
  ]
}
```

`loc` tells you exactly which field, in which part of the request, was wrong. This is Pydantic's validation error surfaced by FastAPI — you wrote zero code for it.

## Resetting the database

Because it's SQLite, "reset" = delete the file:

```bash
rm test_orm.db        # then restart uvicorn; create_all rebuilds it
```

## Next

→ [[06 - Request vs Response Models Explained]]
