---
description: "Combines a transport and a strategy into a FastAPI Users AuthenticationBackend (bearer + JWT example)."
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
  - "3.Create a backend"
  - "AuthenticationBackend"
hubs:
  - "[[Auth & Security]]"
  - "[[FastAPI]]"
---
Combination of transport and strategy

Bearer Transport + JWT Strategy
```python
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
	return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
	
auth_backend = AuthenticationBackend(
	name = "jwt",
	transport = bearer_transport,
	get_strategy = get_jwt_strategy,
)
```

Next Step:
You'll then have to pass those backends to your `FastAPIUsers` instance and generate an auth router for each one of them.