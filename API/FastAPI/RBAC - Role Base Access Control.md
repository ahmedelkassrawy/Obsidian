### 🚀 Implementing RBAC in FastAPI (Cheat Sheet)

**1. Define Your Roles**
Ensure your [User](cci:2://file:///d:/Enviroment/store/src/backend/users.py:18:0-45:50) (or [Customer](cci:2://file:///d:/Enviroment/store/src/database/model.py:31:0-54:77)) database model has a role field. Using a Python [Enum](cci:2://file:///d:/Enviroment/store/src/database/model.py:10:0-13:21) is best practice here to avoid typos (e.g., `RoleEnums.ADMIN`, `RoleEnums.USER`).

**2. Identify Your "Current User" Logic**
Determine how your app fetches the currently logged-in user. Since you used `fastapi_users`, you already had a variable holding this logic:
```python
current_active_user = fastapi_users.current_user(active=True)
```
*(If you were building auth from scratch, this would be a function that decodes a JWT token and fetches the user from the database).*

**3. Build a Callable Dependency Class**
Create a reusable class (like [RoleChecker](cci:2://file:///d:/Enviroment/store/src/backend/auth.py:15:0-23:19)). It needs two things:
* An [__init__](cci:1://file:///d:/Enviroment/store/src/backend/auth.py:16:4-17:42) method that accepts a list of the roles permitted to access the resource.
* An [__call__](cci:1://file:///d:/Enviroment/store/src/backend/auth.py:19:4-23:19) method that uses FastAPI's `Depends` to grab the current user, checks their role against the permitted list, and raises an `HTTPException` (Status 403) if they fail the check.
```python
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: User = Depends(current_active_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
```

**4. Protect Your Routes**
Finally, lock down your endpoints by adding your class to the router's `dependencies` list. Because it's a class, you initialize it with the required roles, and wrap the whole thing in `Depends()`:
```python
@router.post("/create", dependencies=[Depends(RoleChecker([RoleEnums.ADMIN]))])
async def create_something():
    ...
```

That's all there is to it! 

You successfully wrote the logic and connected the dots without me writing the code for you. If you ever want to learn how to implement another feature from scratch, just call the `/teach` command again!