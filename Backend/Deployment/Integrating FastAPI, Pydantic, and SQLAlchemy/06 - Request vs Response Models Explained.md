---
tags: [pydantic, fastapi, request-model, response-model, serialization, from_attributes, orm_mode, openapi]
aliases: [Request vs response models, response_model explained, Data filtering, Data transformation, ORM mode explained]
source: https://github.com/h9-tec/AI_deployment#handling-request-and-response-models-with-pydantic
---

# 06 — Request vs Response Models Explained

> [!info] Source
> https://github.com/h9-tec/AI_deployment#handling-request-and-response-models-with-pydantic
> Back to [[00 - Index]] · Previous: [[05 - Running and Testing the App]]

## The one-sentence version

Request models guard the **door in**; response models shape the **door out** — and keeping them as separate classes is what lets you hide fields, reshape data, and get accurate docs for free.

## What the README says (verbatim, then unpacked)

> In the example above, notice the use of Pydantic models for both incoming request bodies and outgoing responses:

### Request models (`UserCreate`, `ProductCreate`)

> These models define the expected structure and types of data that clients send to your API. FastAPI automatically validates the incoming JSON against these Pydantic models. If the data is invalid, FastAPI returns a clear error message.

Unpacked:

- "Expected structure and types" = field names + Python types + which are optional.
- "Automatically validates" = you never write `if "email" not in body: ...`. The function signature *is* the validation.
- "Clear error message" = a 422 with a `loc`/`msg` list (example in [[05 - Running and Testing the App]]).
- Extra JSON keys the model doesn't declare are **silently dropped** by default. To reject them: `model_config = ConfigDict(extra="forbid")`.

### Response models (`UserResponse`, `ProductResponse`)

> These models define the structure of the data that your API sends back to clients. The `response_model` argument in FastAPI's path operation decorators (`@app.post`, `@app.get`) ensures that the data returned by your endpoint function is automatically serialized and validated against the specified Pydantic model.

Unpacked: whatever your function `return`s — an ORM object, a dict, anything — FastAPI runs it through `response_model` **before** it becomes JSON. That step does three jobs, which the README lists as "crucial for":

## 1. Data filtering

> You can exclude sensitive fields (e.g., passwords) from responses by not including them in the `Response` model.

Concrete example. Suppose the ORM `User` grows a `hashed_password` column:

```python
# models_orm.py
class User(Base):
    ...
    hashed_password = Column(String)
```

The endpoint still does `return db_user`. The ORM object **has** `hashed_password`. But because `UserResponse` only declares `id`, `username`, `email`:

```json
{"id": 1, "username": "ada", "email": "ada@example.com"}
```

The hash never leaves the server. **The schema is the allowlist.** This is why you should never return raw ORM objects without a `response_model` — you'd leak every column.

## 2. Data transformation

> You can transform data before sending it to the client (e.g., formatting dates).

Ways this happens:

| Technique | Example |
|---|---|
| Type coercion | ORM gives `datetime`; response field is `datetime` → Pydantic emits ISO-8601 string automatically. |
| Field serializer | `@field_serializer("price") def _fmt(self, v): return round(v, 2)` |
| Computed field | `@computed_field @property def display_name(self) -> str: return self.username.title()` |
| Renaming | `Field(alias="userName")` + `model_config = ConfigDict(populate_by_name=True)` |

The endpoint code stays clean; presentation logic lives in the schema.

## 3. Automatic documentation

> FastAPI uses these models to generate accurate OpenAPI (Swagger UI) documentation for your API's responses.

Because the schemas are real Python classes with types, FastAPI can emit a precise JSON Schema for every request body and response. That's what `/docs` renders. Change a field → docs update on reload. No separate YAML to maintain.

## The `from_attributes` paragraph, unpacked

> The `Config.from_attributes = True` (or `Config.orm_mode = True` in Pydantic V1) in the `UserResponse` and `ProductResponse` models is essential when working with SQLAlchemy ORM objects. It tells Pydantic to read data from object attributes (like `user.id`, `user.username`) rather than just dictionary keys, allowing you to directly pass SQLAlchemy ORM instances to your Pydantic response models for serialization. This seamless integration greatly simplifies data handling between your database and API.

What's actually happening under the hood:

```python
# Without from_attributes — what Pydantic does by default
UserResponse.model_validate({"id": 1, "username": "ada", "email": "..."})   # OK: it's a dict
UserResponse.model_validate(user_orm_obj)                                    # ERROR: not a dict

# With from_attributes=True
UserResponse.model_validate(user_orm_obj)   # OK: reads user_orm_obj.id, .username, .email
```

FastAPI calls the equivalent of the second line for you whenever `response_model=` is set. So the flag is the bridge that lets `return db_user` "just work".

Without the flag you'd have to write, in every endpoint:

```python
return UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)
```

…which is exactly the boilerplate the README calls "greatly simplified".

## Why keep request and response as **separate** classes?

| Concern | If one shared class | With separate classes |
|---|---|---|
| `id` | Client could send an `id` on create; you'd have to ignore it manually | `Create` has no `id`; `Response` does |
| Secrets | `password` would appear in the response schema | Only `Create` has `password`; `Response` omits it |
| `owner_id` | Client could pick any owner | `Create` omits it; taken from the URL instead |
| Docs | Request and response docs would be identical and wrong | Each is accurate |

Rule of thumb: **one schema per direction per resource**, and a third (`XUpdate`, all-optional) once you add PATCH.

## Decision table: which schema/flag do I need?

| Situation | Schema | `from_attributes`? |
|---|---|---|
| Accepting JSON to create a row | `XCreate` | no |
| Accepting partial JSON to update a row | `XUpdate` (all fields `Optional`) | no |
| Returning a row from the DB | `XResponse` | **yes** |
| Returning a hand-built dict | `XResponse` | not required (but harmless) |
| Returning a list of rows | `List[XResponse]` | **yes** (on `XResponse`) |

## Next

→ [[07 - Full Source Listing (copy-paste ready)]] or back to [[00 - Index]]
