(https://github.com/h9-tec/AI_deployment#7-advanced-topics-and-best-practices)

This section delves into more advanced features and best practices for building robust, scalable, and maintainable applications with FastAPI, Pydantic, and SQLAlchemy.

### Asynchronous Operations (Async/Await)

(https://github.com/h9-tec/AI_deployment#asynchronous-operations-asyncawait)

FastAPI is built on ASGI (Asynchronous Server Gateway Interface), which allows it to handle requests asynchronously. This is particularly beneficial for I/O-bound operations, such as database queries, network requests, or long-running machine learning inferences, as it allows the server to handle other requests while waiting for these operations to complete.

To leverage asynchronous operations, you use the `async` and `await` keywords in Python. SQLAlchemy 2.0 and later versions provide excellent asynchronous support.

First, ensure you have an async database driver installed. For PostgreSQL, `asyncpg` is a common choice:

```shell
pip install asyncpg
```

Then, modify your database connection and session setup to use `asyncio` and `AsyncSession`:

```python
# database_async.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models_orm import Base # Assuming Base is defined in models_orm.py

# For PostgreSQL example:
# DATABASE_URL_ASYNC = "postgresql+asyncpg://user:password@host:port/dbname"
# For SQLite (async support is limited, often requires aiohttp-sqlite or similar for true async):
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./test_async.db"

async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
```

Now, your FastAPI endpoints can use `async` and `await` with the `AsyncSession`:

```python
# main_async.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from models_orm import User, Product # Your SQLAlchemy ORM models
from database_async import get_async_db, init_db # Your async database setup
from pydantic import BaseModel # Assuming your Pydantic models are defined

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/async_users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_async_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/async_users/", response_model=List[UserResponse])
async def read_async_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@app.get("/async_users/{user_id}", response_model=UserResponse)
async def read_async_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Dependency Injection

[](https://github.com/h9-tec/AI_deployment#dependency-injection)

FastAPI has a very powerful and easy-to-use Dependency Injection system. It allows you to declare dependencies (functions, classes, etc.) that your path operation functions need. FastAPI then takes care of resolving these dependencies and passing their results to your functions.

We've already seen this with `db: Session = Depends(get_db)` or `db: AsyncSession = Depends(get_async_db)`. Other common uses include:

- **Authentication**: Injecting the current authenticated user.
- **Authorization**: Checking user permissions.
- **Configuration**: Providing application settings.
- **Business Logic**: Injecting services that encapsulate specific business operations.

```python
# main_dependencies.py

from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

app = FastAPI()

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

async def get_current_user(x_token: Annotated[str, Depends(verify_token)]):
    # In a real app, you'd decode JWT or query a database
    return {"username": "john_doe", "id": 123}

@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]

@app.get("/users/me/")
async def read_users_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user
```

### Authentication and Authorization (OAuth2, JWT)
[(https://github.com/h9-tec/AI_deployment#authentication-and-authorization-oauth2-jwt)]

FastAPI provides utilities for implementing various authentication and authorization schemes, including OAuth2 with JSON Web Tokens (JWT). This is crucial for securing your API endpoints.

```python
# auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

# Replace with a strong secret key in production
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # In a real app, you'd fetch the user from DB based on username
    user = {"username": token_data.username, "email": f"{token_data.username}@example.com"}
    if user is None:
        raise credentials_exception
    return user

# main_auth.py

from fastapi import FastAPI, Depends
from auth import get_current_user_from_token, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

app = FastAPI()

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # In a real app, verify username and password against a database
    if form_data.username == "testuser" and form_data.password == "testpassword":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.get("/secure_data/")
async def read_secure_data(current_user: Annotated[dict, Depends(get_current_user_from_token)]):
    return {"message": f"Hello {current_user["username"]}, this is secure data!"}
```

### Testing FastAPI Applications
[(https://github.com/h9-tec/AI_deployment#testing-fastapi-applications)]

FastAPI makes testing easy with `TestClient` from `fastapi.testclient`. This allows you to simulate requests to your application without actually running a server.

```python
# test_main.py

from fastapi.testclient import TestClient
from main_integrated import app # Assuming your main app is in main_integrated.py

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert "id" in response.json()

# You would typically add more tests for edge cases, error handling, etc.
```

Run tests using `pytest`:

```shell
pip install pytest
pytest
```

### Migrations with Alembic

[](https://github.com/h9-tec/AI_deployment#migrations-with-alembic)

As your application evolves, your database schema will likely change. Alembic is a lightweight database migration tool for SQLAlchemy that helps manage these changes in a structured way.

1. **Install Alembic**: `pip install alembic`
2. **Initialize Alembic**: Navigate to your project root and run `alembic init alembic`. This creates an `alembic` directory with configuration and an `env.py` file.
3. **Configure `alembic.ini`**: Point `sqlalchemy.url` to your database connection string.
4. **Configure `env.py`**: In `alembic/env.py`, import your `Base` (from `models_orm.py`) and set `target_metadata = Base.metadata`.
5. **Generate Migration**: `alembic revision --autogenerate -m "Initial migration"`
6. **Apply Migration**: `alembic upgrade head`

This process allows you to track schema changes, apply them to different environments, and revert if necessary.

### Error Handling

[](https://github.com/h9-tec/AI_deployment#error-handling)

FastAPI provides robust error handling mechanisms. You can raise `HTTPException` for standard HTTP errors, and FastAPI will automatically convert them into appropriate JSON responses. For custom exceptions, you can use `@app.exception_handler`.

```python
# main_error_handling.py

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

# Custom exception
class CustomError(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomError)
async def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT, # Just for demonstration
        content={
            "message": f"Oops! {exc.name} did something wrong.",
            "code": "CUSTOM_ERROR_CODE"
        },
    )

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 404:
        raise HTTPException(status_code=404, detail="Item not found")
    if item_id == 500:
        raise CustomError(name="Server")
    return {"item_id": item_id}
```

This allows for centralized and consistent error responses across your API.