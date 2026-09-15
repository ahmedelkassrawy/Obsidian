---
description: "Mounting the FastAPI Users verify router for email verification routes."
domain: backend
type: reference
status: raw
tags:
  - domain/backend
  - type/reference
  - status/raw
  - topic/auth-and-security
  - topic/fastapi
aliases:
  - "Verify Router"
  - "email verification"
hubs:
  - "[[Auth & Security]]"
  - "[[FastAPI]]"
---
This router provides routes to manage user email **verification**

```python
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from .db import User
from .schemas import UserRead

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
```