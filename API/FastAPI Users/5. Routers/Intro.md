## Configure `FastAPIUsers`
Configure `FastAPIUsers` object with the elements we defined before. More precisely:

- `get_user_manager`: Dependency callable getter to inject the user manager class instance.
- `auth_backends`: List of authentication backends.
```python
import uuid

from fastapi_users import FastAPIUsers

from .db import User

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager,
[auth_backend],)
```

Available routers
- [Auth router](https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/auth/): Provides `/login` and `/logout` routes for a given [authentication backend](https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/).
- [Register router](https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/register/): Provides `/register` routes to allow a user to create a new account.
- [Reset password router](https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/reset/): Provides `/forgot-password` and `/reset-password` routes to allow a user to reset its password.
- [Verify router](https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/verify/): Provides `/request-verify-token` and `/verify` routes to manage user e-mail verification.
- [Users router](https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/users/): Provides routes to manage users.
- [OAuth router](https://fastapi-users.github.io/fastapi-users/latest/configuration/oauth/): Provides routes to perform an OAuth authentication against a service provider (like Google or Facebook).
