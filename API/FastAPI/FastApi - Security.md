# OAuth2 and OpenID Connect Study Notes

## OAuth2

- **Definition**: A framework for third-party authentication, enabling "Login with Facebook, Google, Twitter, GitHub" functionality.
- **Purpose**: Allows secure access to resources without sharing credentials, using access tokens.
- **Key Concept**: Tokens (strings) are issued to authenticate users, often with expiration for security.

### How OAuth2 Works

1. **User Action**: User enters `username` and `password` in a frontend and submits.
2. **Frontend**: Sends credentials to a specific API endpoint (e.g., `tokenUrl="token"`).
3. **API**: Verifies credentials and returns an access token (a string used for authentication).
    - Tokens typically expire after a set time (e.g., 30 minutes) to reduce risk if stolen.
4. **Frontend Storage**: Stores the token temporarily (e.g., in memory or local storage).
5. **Authenticated Requests**:
    - Frontend sends the token in an `Authorization` header as `Bearer <token>` for protected API endpoints.
    - Example: If token is `foobar`, header is `Authorization: Bearer foobar`.

### OAuth2 in FastAPI

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

- **Explanation**:
    - `OAuth2PasswordBearer`: Defines the OAuth2 password flow, specifying the token endpoint (`tokenUrl="token"`).
    - The `/items/` endpoint requires a token, extracted from the `Authorization` header.

## OpenID Connect

- **Definition**: A specification built on OAuth2 to standardize authentication for better interoperability.
- **Use Case**: Used by Google for login, but not by Facebook (which uses its own OAuth2 flavor).
- **Key Feature**: Adds automatic discovery of OAuth2 authentication data, reducing ambiguity.

### OpenID Connect in OpenAPI

- OpenAPI supports defining security schemes, including `openIdConnect` for automatic OAuth2 discovery.
- Example: Allows APIs to specify how to fetch authentication metadata dynamically.

## OpenAPI Security Schemes

OpenAPI defines multiple security schemes for APIs:

- **`apiKey`**: Application-specific key in:
    - Query parameter
    - Header
    - Cookie
- **`http`**:
    - `bearer`: Uses `Authorization: Bearer <token>` (inherited from OAuth2).
    - HTTP Basic Authentication
    - HTTP Digest Authentication
- **`oauth2`**: Supports OAuth2 flows:
    - **Flows for Authentication Providers**:
        - `implicit`
        - `clientCredentials`
        - `authorizationCode`
    - **Flow for Internal Authentication**:
        - `password`: Used for direct authentication within the same application.
        - `openIdConnect`: Supports automatic discovery of OAuth2 data.

## FastAPI OAuth2 Implementation

Below is a complete example of OAuth2 authentication in FastAPI, including password hashing, JWT tokens, and user management.

### Configuration

```python
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key-here-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

### Pydantic Models

```python
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None

class UserInDB(User):
    hashed_password: str
```

### Utility Functions

```python
def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the current user from the token."""
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Get the current active user."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Endpoints

```python
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login endpoint to get access token."""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
```

### CORS Middleware

- **Purpose**: Allows cross-origin requests from different domains, critical for web apps.
- **Security Note**: Avoid `allow_origins=["*"]` in production; specify exact domains.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
```

## OAuth2 with SQLAlchemy

A more advanced implementation using a database (SQLAlchemy) for user storage.

### Setup

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])
SECRET_KEY = "secretkeyforjwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Pydantic Models

```python
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
```

### Database Dependency

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Password and JWT Functions

```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Current User Dependency

```python
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
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
    except JWTError:
        raise credentials_exception
    user = db.query(Auth).filter(Auth.username == username).first()
    if user is None:
        raise credentials_exception
    return user
```

### Routes

1. **Register (/auth/register)**

```python
@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    hashed_password = hash_password(user.password)
    db_user = db.query(Auth).filter(Auth.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already used")
    new_user = Auth(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

2. **Login (/auth/login)**

```python
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(Auth).filter(Auth.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

3. **Get Current User (/auth/me)**

```python
@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
```

## How It All Works

1. **Database Setup**: Uses SQLAlchemy (`Auth` model, `engine`) for persistent user storage.
2. **Registration**:
    - Client sends POST to `/auth/register` with `{"username": "alice", "password": "secret"}`.
    - Password is hashed and stored; user details are returned.
3. **Login**:
    - Client sends POST to `/auth/login` with form data (`username=alice&password=secret`).
    - Server verifies credentials and returns a JWT token.
4. **Protected Routes**:
    - Client sends GET to `/auth/me` with `Authorization: Bearer <token>`.
    - Server validates the token and returns user details.
5. **Security**:
    - Passwords are hashed with bcrypt.
    - JWT tokens are secure, stateless, and expire after a set time.
    - Invalid credentials/tokens trigger HTTP 401 errors.

## Key Points to Remember

- **OAuth2**: Use for third-party or internal authentication with tokens.
- **OpenID Connect**: Enhances OAuth2 with standardized authentication (e.g., Google).
- **OpenAPI**: Defines security schemes (`apiKey`, `http`, `oauth2`) for API documentation.
- **FastAPI**: Simplifies OAuth2 implementation with `OAuth2PasswordBearer` and dependencies.
- **CORS**: Essential for web apps; configure carefully in production.
- **Security Best Practices**:
    - Use strong `SECRET_KEY` in production.
    - Set token expiration to limit risks.
    - Avoid `allow_origins=["*"]` in production.
    - Use HTTPS to protect tokens in transit.