---
description: "Ch8 notes on auth for AI services: registration and login flows, password hashing, JWT access and refresh tokens, logout, and role-based authorization."
domain: ai-eng
type: book
status: digested
tags:
  - domain/ai-eng
  - type/book
  - status/digested
  - topic/auth-and-security
  - topic/fastapi
aliases:
  - "JWT"
  - "OAuth"
  - "refresh tokens"
hubs:
  - "[[Auth & Security]]"
  - "[[FastAPI]]"
---
## What this chapter covers

- The difference between authentication and authorization.
- Four ways to authenticate: basic, JWT, OAuth, and key-based.
- Building basic auth and a full JWT system from scratch (hashing, tokens, login, logout).
- Single sign-on with GitHub using OAuth2, and the attacks it has to defend against (CSRF, open redirect, phishing).
- Authorization models: RBAC, ReBAC, ABAC, and hybrids, enforced with FastAPI dependencies.

> **Note on the code below:** the book targets ~2024 libraries (passlib, python-jose). I updated the code to what the current FastAPI docs use (pwdlib, PyJWT) and fixed several printed snippets that wouldn't run. Every change is marked with a `# ⚠️` comment and listed in the Verification note at the end.

---

## Authentication vs authorization

The two words get mixed up a lot, but they answer different questions.

> [!definition] Authentication
> Checking that a user (or service) is who they claim to be, using something like a password, fingerprint, or token.

> [!definition] Authorization
> Checking whether that verified identity is allowed to do a specific action on a specific resource.

Think of airport passport control. Showing your passport is authentication. Having the right visa, which says how long you can stay and what you can do, is authorization.

---

## Authentication methods

- **Basic**: the client sends a username and password to prove who it is.
- **JSON Web Tokens (JWT)**: the client sends an access token. Think of it like a cinema ticket: it says whether you can get in, which screen, and where you sit.
- **OAuth**: an outside identity provider (like GitHub or Google) verifies the user using the OAuth2 standard.
- **Key-based**: a public/private key pair proves identity instead of a token. The server issues a public key to the client and keeps the linked private key to verify it later. The book doesn't go further into this one.

![[Pasted image 20260125173927.png]]

| Type | Benefits | Limitations | Use cases |
|---|---|---|---|
| **Basic** | Simple, fast to build, easy to understand. | Sends credentials in plain text (needs HTTPS); hard to revoke without changing passwords. | Prototypes; internal, non-critical environments. |
| **Token (JWT)** | Scales well; decoupled, which suits microservices; self-contained (fewer DB lookups); travels in HTTP headers. | Short-lived tokens must be regenerated; client-side storage is tricky; hard to revoke before expiry. | Single-page apps, mobile apps, REST APIs with custom auth flows. |
| **OAuth** | Hands authentication to outside providers; standard (OAuth2) and battle-tested; can access external resources on the user's behalf. | Complex to understand and build; each provider implements the flow a bit differently. | Apps that need data from identity providers (GitHub, Google, Microsoft); enterprise SSO. |
| **Key-based** | Works like SSH; very secure for machine-to-machine; no manual login. | Keeping private keys safe is hard; a leaked key is high risk; scales poorly for human users. | Enterprise apps using SSH; small internal apps; automated API access. |

---

## Basic authentication

With basic auth, the client sends a username and password with each request. You don't need cookies, sessions, or login forms, which makes it handy for sandboxes and prototypes.

Avoid it in production. The credentials travel on **every** request, essentially in plain text, so anyone who intercepts traffic gets them.

> [!definition] Base64
> A reversible way to turn bytes into URL-safe text. It's an encoding, not encryption: anyone can decode it.

To make a basic-auth request, add an `Authorization` header with the value `Basic <credentials>`, where `<credentials>` is the Base64 encoding of `username:password` (for example, `base64.encode("ali:secretpassword")`).

### Example 8-1: basic authentication in FastAPI

```python
# main.py
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

username_bytes = b"ali"
password_bytes = b"secretpassword"

def authenticate_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("UTF-8"), username_bytes
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("UTF-8"), password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

AuthenticatedUserDep = Annotated[str, Depends(authenticate_user)]

@app.get("/users/me")
async def get_current_user(username: AuthenticatedUserDep):
    return {"message": f"Current user is {username}"}
```

- `HTTPBasic` is one of FastAPI's built-in security schemes. Used with `Depends()`, it gives you an `HTTPBasicCredentials` object holding the username and password.
- `secrets.compare_digest()` takes the same time no matter how much of the input matches, which blocks timing attacks.
- `compare_digest()` only accepts bytes or ASCII-only strings, so the inputs are UTF-8 encoded first to handle any character.
- The 401 response with `WWW-Authenticate: Basic` is the standard format browsers understand, so they show the login prompt again.
- Keep the error message generic. Saying "wrong password" would leak that the username exists.

> [!definition] Timing attack
> An attacker guesses secrets by measuring how long the server takes to check them. A check that stops at the first wrong character answers faster for bad guesses, which leaks information.

Any endpoint that injects this dependency is now protected. In `/docs` you'll see a lock icon next to `/users/me`, and the browser asks for credentials when you call it.

---

## JWT authentication

JWT auth is the safer choice for public services. All the auth details live inside the token, so the server doesn't need sessions, the data can't be tampered with, and it works across domains.

### What is a JWT?

> [!definition] JWT (JSON Web Token)
> A compact, URL-safe token that carries **claims** between applications. It has three parts separated by dots: header, payload, and signature.

> [!definition] Claim
> One piece of information inside the token's payload, like `sub` (subject: who the token is about), `exp` (expiry time), or `iss` (issuer: who created it).

The three parts:

| Part | What it holds |
|---|---|
| **Header** | The token type and signing algorithm (plus, per the book, the datetime and issuing authority). |
| **Payload** | The claims, plus any extra metadata. |
| **Signature** | Made by signing the encoded header + encoded payload with a secret and the algorithm. Change one byte of the payload and the signature no longer matches. |

> [!warning] Signed is not encrypted
> The header and payload are only Base64-encoded. Anyone holding the token can read them. Never put secrets in the payload.

JWTs can hold everything needed to authenticate a user, which saves database round trips. They're small enough to send in a POST body, a header, or a URL parameter.

### Getting started

```bash
pip install pyjwt "pwdlib[argon2]"
# ⚠️ book: pip install passlib python-jose
#    FastAPI's docs now use PyJWT for tokens and pwdlib (Argon2) for passwords.
#    pwdlib's author says passlib has been inactive and has compatibility trouble with newer Python.
```

You need two tables: `users` and `tokens`.

![[Pasted image 20260125180251.png]]

The `tokens` table has a **one-to-many** relationship with `users`: one user, many tokens. Each token row records a successful login, so you can track logins and revoke access when needed.

### Example 8-2 and 8-4: SQLAlchemy models

```python
# entities.py
import uuid
from datetime import UTC, datetime

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

def utc_now() -> datetime:
    return datetime.now(UTC)

class Base(DeclarativeBase):
    pass

class User(Base):  # ⚠️ my old note called this `Users`; the book and the rest of the code use `User`
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(length=255), unique=True)
    username: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=255))
    role: Mapped[str] = mapped_column(default="USER")
    is_active: Mapped[bool] = mapped_column(default=True)
    # ⚠️ book: default=datetime.now(UTC). That runs ONCE at import time, so every row
    #    would get the same timestamp. Pass the function itself so it runs per insert/update.
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_users_email", "email"),)

class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # ⚠️ book: Mapped[int]. users.id is a UUID, so the foreign key must be a UUID too.
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    ip_address: Mapped[str | None] = mapped_column(String(length=255))
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="tokens")

    __table_args__ = (
        Index("ix_tokens_user_id", "user_id"),
        Index("ix_tokens_ip_address", "ip_address"),
    )
```

- **UUIDs** for IDs, so attackers can't guess the IDs of other users or tokens.
- Only `hashed_password` is stored, never the raw password.
- `is_active` lets you disable an account or revoke a token.
- `role` (`USER`, `ADMIN`, ...) is what authorization checks will read later.
- Timestamps help with monitoring and security audits.
- The unique constraint + index on `email` blocks duplicate accounts and speeds up lookups. `user_id` and `ip_address` are indexed on `tokens` for the same reason.
- `cascade="all, delete-orphan"` deletes a user's tokens when the user is deleted.

> [!definition] ORM model vs Pydantic schema
> The **ORM model** (SQLAlchemy) describes a database table and is used in the data-access layer. The **Pydantic schema** validates data coming in and going out at the endpoint layer.

### Example 8-3 and 8-4: Pydantic schemas

```python
# schemas.py
from datetime import datetime
from typing import Annotated

# ⚠️ my old note imported `UUID` from pydantic, which doesn't exist; the book uses UUID4
from pydantic import UUID4, AfterValidator, BaseModel, ConfigDict, Field, validate_call

@validate_call
def validate_username(value: str) -> str:
    if not value.isalnum():
        raise ValueError("Username must be alphanumeric")
    return value

@validate_call
def validate_password(value: str) -> str:
    validations = [
        (lambda v: any(char.isdigit() for char in v), "Password must contain at least one digit"),
        (lambda v: any(char.isupper() for char in v), "Password must contain at least one uppercase letter"),
        (lambda v: any(char.islower() for char in v), "Password must contain at least one lowercase letter"),
    ]
    for condition, error_message in validations:
        if not condition(value):
            raise ValueError(error_message)
    return value

ValidUsername = Annotated[str, Field(min_length=3, max_length=20), AfterValidator(validate_username)]
ValidPassword = Annotated[str, Field(min_length=8, max_length=64), AfterValidator(validate_password)]

# --- users ---
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: ValidUsername
    is_active: bool = True
    role: str = "USER"

class UserCreate(UserBase):
    password: ValidPassword

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

# --- tokens ---
class TokenBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID4  # ⚠️ book: int. Must match the UUID primary key of users.
    expires_at: datetime
    is_active: bool = True
    ip_address: str | None = None

class TokenCreate(TokenBase):
    pass

class TokenUpdate(BaseModel):  # ⚠️ used by the repository but never defined in the book; minimal version
    is_active: bool | None = None

class TokenOut(BaseModel):  # ⚠️ my old note inherited TokenBase, which would force user_id/expires_at into the login response
    access_token: str
    token_type: str = "Bearer"
```

- Both username and password get validators for stronger security rules.
- `from_attributes=True` lets Pydantic read straight from SQLAlchemy objects, so you don't copy fields by hand.
- Inheritance builds several schemas from one `UserBase`.
- `UserInDB` is the **only** schema with `hashed_password`. It's used just for creating users at registration. The others leave it out so the hash can't leak in a response.

Then generate and run the migration:

```bash
alembic revision --autogenerate -m "create users and tokens tables"
alembic upgrade head
```

### Architecture

Here's the JWT system you'll build:

![[Pasted image 20260125233709.png]]

---

## Hashing and salting

Never store passwords as plain text. If the database leaks, the attacker gets every user's credentials.

> [!definition] Hashing
> A one-way function that turns a password into a fixed-length string. You can't turn the hash back into the password. That's what makes it different from encoding like Base64, which is reversible.

Hashing alone isn't enough. Attackers have **rainbow tables**.

> [!definition] Rainbow table
> A precomputed lookup table of hashes for common passwords. If your hashes are plain, an attacker can just look them up.

> [!definition] Salt
> A random value added to the password before hashing. Two users with the same password get different hashes, and precomputed tables become useless. Typical salts are 16 bytes (balanced) or 32 bytes (sensitive systems).

### Registration (storing)

1. The user sends a plain password, e.g. `P@ssword123`.
2. The system generates a random **salt**, e.g. `xyz789`.
3. Salt and password are combined: `P@ssword123xyz789`.
4. The combination is run through a hashing algorithm (Argon2 or bcrypt), giving a fixed-length, random-looking string.
5. The system stores **salt + hash** in the database. Modern libraries prefix the salt onto the stored hash string for you.

### Login (verifying)

Hashes can't be decrypted, so the system repeats the math and compares.

1. The user enters their username and plain password.
2. The system loads the stored salt and hash for that user.
3. It hashes the typed password with the **stored** salt, using the same algorithm.
4. Same hash: logged in. Different hash: access denied.

### What this protects against

| Threat | How salting and hashing help |
|---|---|
| **Database leak** | The attacker only sees hashes, which can't be reversed. |
| **Rainbow tables** | The salt makes every input unique, so precomputed tables don't match. |
| **Duplicate passwords** | Two users with `Password123` get different salts and therefore different hashes. |

![[Pasted image 20260125234635.png]]

> [!warning] What salting doesn't stop
> It doesn't protect against **password spraying** (trying a list of common passwords against many accounts) or **credential stuffing** (trying username/password pairs leaked from other sites). You need rate limits and lockouts for those.

### Example 8-6: password service

```python
# services/auth.py
from pwdlib import PasswordHash  # ⚠️ book: from passlib.context import CryptContext

class PasswordService:
    # ⚠️ book: CryptContext(schemes=["bcrypt"]). FastAPI docs now use pwdlib's
    #    recommended() setup, which is Argon2. pwdlib also supports bcrypt.
    password_hash = PasswordHash.recommended()
    # ⚠️ new, from the FastAPI docs: a dummy hash to verify against when the
    #    username doesn't exist, so both cases take the same time (see Example 8-10).
    dummy_hash = password_hash.hash("dummypassword")

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    async def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)
```

- One shared hasher handles both hashing new passwords and checking login attempts.
- The salt is generated and stored inside the hash string automatically. You never manage it yourself.
- The book's version also had an unused `security = HTTPBearer()` attribute here. I moved the bearer scheme to Example 8-10, where it's actually used.

> [!definition] Argon2
> A modern password-hashing algorithm built to be slow and memory-hungry on purpose, so brute-forcing hashes on GPUs is expensive. It's what FastAPI's docs now recommend.

### Example 8-7: auth exceptions

```python
# exceptions.py
from fastapi import HTTPException, status

UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized access",
    headers={"WWW-Authenticate": "Bearer"},
)

AlreadyRegisteredException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with given credentials already registered",
)
```

These are the two you'll raise most: unauthorized access, and a bad request when someone registers a username that's taken.

---

## Issuing tokens

Once a user's credentials check out, you issue them an access token.

> [!definition] Access token
> A short-lived credential the client sends with each request to prove it's logged in. Short life means a stolen token is only useful for a little while.

What the token service has to do:

- **Sign** the payload with a secret and encode it (Base64), so tokens stay small and can't be forged.
- Put the user's details in the payload: ID, role, issuer, expiry.
- **Decode** incoming tokens and check they're valid.
- Store and look up tokens in the database. That's why it inherits from a `TokenRepository`.

### Example 8-8: token repository

```python
# repositories.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entities import Token
from repositories.interfaces import Repository
from schemas import TokenCreate, TokenUpdate

# ⚠️ book wrapped every method in `async with session.begin():` AND called commit()
#    (and refresh()) inside that block. session.begin() already commits when the block
#    ends, so the extra calls fight it. I use the plain add/commit/refresh pattern from
#    SQLAlchemy's asyncio docs instead. Configure the sessionmaker with
#    expire_on_commit=False (also per those docs).
class TokenRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int = 0, take: int = 100) -> list[Token]:
        result = await self.session.execute(select(Token).offset(skip).limit(take))
        return list(result.scalars().all())

    async def get(self, token_id: uuid.UUID) -> Token | None:
        result = await self.session.execute(select(Token).where(Token.id == token_id))
        return result.scalars().first()

    async def create(self, token: TokenCreate) -> Token:
        new_token = Token(**token.model_dump())  # ⚠️ book: token.dict(), deprecated in Pydantic v2
        self.session.add(new_token)
        await self.session.commit()
        await self.session.refresh(new_token)
        return new_token

    async def update(self, token_id: uuid.UUID, updated_token: TokenUpdate) -> Token | None:
        token = await self.get(token_id)
        if not token:
            return None
        for key, value in updated_token.model_dump(exclude_unset=True).items():  # ⚠️ was .dict()
            setattr(token, key, value)
        await self.session.commit()
        await self.session.refresh(token)
        return token

    async def delete(self, token_id: uuid.UUID) -> None:
        token = await self.get(token_id)
        if not token:
            return
        await self.session.delete(token)
        await self.session.commit()
```

- A standard CRUD repository: list, get, create, update, delete.
- `exclude_unset=True` only applies the fields the caller actually sent, so an update doesn't wipe other columns.

### Example 8-9: token service

```python
# services/auth.py (continued)
import uuid
from datetime import UTC, datetime, timedelta

import jwt  # ⚠️ book: from jose import JWTError, jwt (python-jose). FastAPI docs now use PyJWT.

from exceptions import UnauthorizedException
from repositories import TokenRepository
from schemas import TokenCreate, TokenUpdate

class TokenService(TokenRepository):
    secret_key = "your_secret_key"  # load from an environment variable in real code
    algorithm = "HS256"
    expires_in_minutes = 60

    async def create_access_token(
        self,
        data: dict,
        user_id: uuid.UUID,  # ⚠️ book only passed expires_at to TokenCreate, but it requires user_id
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.expires_in_minutes)

        token = await self.create(TokenCreate(user_id=user_id, expires_at=expire))
        to_encode.update(
            {
                "exp": expire,
                "iss": "your_service_name",
                # ⚠️ book: "sub": token_id (the returned object). sub must be a string:
                #    PyJWT 2.10+ validates it, and a UUID isn't JSON-serializable anyway.
                "sub": str(token.id),
            }
        )
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def deactivate(self, token_id: str) -> None:
        # ⚠️ book: self.update(TokenUpdate(id=token_id, is_active=False)), which doesn't
        #    match update(token_id, data). My old note dropped this method, but logout() calls it.
        await self.update(uuid.UUID(token_id), TokenUpdate(is_active=False))

    def decode(self, encoded_token: str) -> dict:
        try:
            return jwt.decode(encoded_token, self.secret_key, algorithms=[self.algorithm])
        except jwt.InvalidTokenError:  # ⚠️ book: jose.JWTError. PyJWT's base error covers bad signature AND expiry.
            raise UnauthorizedException

    async def validate(self, token_id: str) -> bool:
        return (token := await self.get(uuid.UUID(token_id))) is not None and token.is_active
```

- Settings like `secret_key` and `algorithm` are class attributes, shared by every instance.
- Each new token gets a database row first. Its ID becomes the `sub` claim, so the token can be looked up and revoked later.
- `exp` is set to one hour out. PyJWT accepts a `datetime` here and checks it automatically on decode, raising `ExpiredSignatureError` (a subclass of `InvalidTokenError`).
- `datetime.now(UTC)` gives a timezone-aware time. Avoid the old `datetime.utcnow()`, which returns a naive datetime and is deprecated.
- `validate()` checks that the token row exists and is still active. A logged-out token fails here even if its signature and expiry are fine.

> [!definition] Token revocation
> Making a token unusable before it expires. Plain JWTs can't be revoked because they're self-contained. Storing a row per token (with `is_active`) is how this design gets revocation back.

### Example 8-10: the auth service

With a `PasswordService` and a `TokenService`, the higher-level `AuthService` ties registration, login, current-user lookup, and logout together. My note also adds a `UserService` and a password-reset method that the book left as a stub.

```python
# services/auth.py (continued)
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from entities import User
from exceptions import AlreadyRegisteredException, UnauthorizedException
from schemas import UserCreate, UserInDB

security = HTTPBearer()

# ⚠️ my old note had `Annotated[..., None]`; the book uses Depends() / Depends(security)
LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
AuthHeaderDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

class UserService:
    """User lookups and writes (my addition; the book imports a UserService without showing it)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_user(self, username: str) -> User | None:
        return await self.get(username)

    async def create(self, user: UserInDB) -> User:
        new_user = User(
            username=user.username,
            hashed_password=user.hashed_password,
            email=getattr(user, "email", f"{user.username}@example.com"),
        )
        self.session.add(new_user)  # ⚠️ dropped the begin()/commit-inside-begin pattern (see Example 8-8)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update_password(self, username: str, hashed_password: str) -> User | None:
        result = await self.session.execute(
            update(User)
            .where(User.username == username)
            .values(hashed_password=hashed_password)
            .returning(User)
        )
        await self.session.commit()
        return result.scalars().first()

class AuthService:
    def __init__(self, session: AsyncSession):
        self.password_service = PasswordService()
        self.token_service = TokenService(session)
        self.user_service = UserService(session)

    async def register_user(self, user: UserCreate) -> User:
        if await self.user_service.get(user.username):
            raise AlreadyRegisteredException
        hashed_password = await self.password_service.hash_password(user.password)
        return await self.user_service.create(
            UserInDB(username=user.username, hashed_password=hashed_password)
        )

    async def authenticate_user(self, form_data: LoginFormDep) -> str:
        if not (user := await self.user_service.get_user(form_data.username)):
            # ⚠️ new, from the FastAPI docs: still run a verify so a missing user
            #    takes as long as a wrong password (no username enumeration by timing)
            await self.password_service.verify_password(
                form_data.password, self.password_service.dummy_hash
            )
            raise UnauthorizedException
        if not await self.password_service.verify_password(form_data.password, user.hashed_password):
            raise UnauthorizedException
        # ⚠️ book: create_access_token(user._asdict()). ORM objects have no _asdict()
        #    (that's on result Rows), and dumping every column would put the password hash in the token.
        return await self.token_service.create_access_token(
            {"username": user.username, "role": user.role}, user_id=user.id
        )

    async def get_current_user(self, credentials: AuthHeaderDep) -> User:
        if credentials.scheme != "Bearer":
            raise UnauthorizedException
        if not (token := credentials.credentials):
            raise UnauthorizedException
        payload = self.token_service.decode(token)
        if not await self.token_service.validate(payload.get("sub")):
            raise UnauthorizedException
        if not (username := payload.get("username")):
            raise UnauthorizedException
        if not (user := await self.user_service.get(username)):
            raise UnauthorizedException
        return user

    async def logout(self, credentials: AuthHeaderDep) -> None:
        payload = self.token_service.decode(credentials.credentials)
        await self.token_service.deactivate(payload.get("sub"))

    async def reset_password(self, username: str, new_password: str) -> User:
        if not await self.user_service.get(username):
            raise UnauthorizedException
        hashed_password = await self.password_service.hash_password(new_password)
        if not (updated_user := await self.user_service.update_password(username, hashed_password)):
            raise UnauthorizedException
        return updated_user
```

- `register_user` refuses taken usernames, hashes the password, and stores only the hash.
- `authenticate_user` is the core login check: does the user exist, and does the password match? Any failure raises the same generic 401.
- `get_current_user` runs on protected requests: check the `Bearer` scheme, decode and verify the JWT, confirm the token row is still active, then load the user.
- `logout` decodes the token and flips its row to inactive, so it can't be reused.

> [!definition] Bearer token
> A token sent as `Authorization: Bearer <token>`. Whoever "bears" it gets access, so it must be kept secret like a password.

### Example 8-11: auth routes

First, a small dependency module so both the auth router and the resource router can get the current user:

```python
# dependencies/auth.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from entities import User
from services.auth import AuthHeaderDep, AuthService

async def get_auth_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> AuthService:
    return AuthService(session)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

# ⚠️ book used Depends(AuthService.get_current_user) / Depends(auth_service.get_current_user)
#    on an AuthService() built without a DB session. A plain function that pulls the
#    service from a dependency gives FastAPI something it can actually inject.
async def get_current_user(credentials: AuthHeaderDep, auth_service: AuthServiceDep) -> User:
    return await auth_service.get_current_user(credentials)

CurrentUserDep = Annotated[User, Depends(get_current_user)]
```

```python
# routes/auth.py
from typing import Annotated

from fastapi import APIRouter, Body

from dependencies.auth import AuthServiceDep
from schemas import TokenOut, UserCreate, UserOut
from services.auth import AuthHeaderDep, LoginFormDep

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ⚠️ switched `x: T = Depends(...)` to Annotated dependencies, the style FastAPI's docs recommend
@router.post("/register", response_model=UserOut)
async def register_user(new_user: UserCreate, auth_service: AuthServiceDep):
    return await auth_service.register_user(new_user)

@router.post("/token", response_model=TokenOut)
async def login_for_access_token(form_data: LoginFormDep, auth_service: AuthServiceDep) -> TokenOut:
    token = await auth_service.authenticate_user(form_data)
    return TokenOut(access_token=token, token_type="bearer")

@router.post("/logout")
async def logout_access_token(
    credentials: AuthHeaderDep,  # ⚠️ was `HTTPAuthorizationCredentials = Depends()`, which reads query params, not the Authorization header
    auth_service: AuthServiceDep,
) -> dict:
    await auth_service.logout(credentials)
    return {"message": "Logged out successfully"}

@router.post("/reset-password")
async def reset_password(
    username: Annotated[str, Body(embed=True)],
    new_password: Annotated[str, Body(embed=True)],
    auth_service: AuthServiceDep,
) -> dict:
    await auth_service.reset_password(username, new_password)
    return {"message": "Password has been reset successfully."}
```

- A separate `APIRouter` groups all auth endpoints under `/auth`.
- The four endpoints: register, login (issue a token), logout (revoke it), and reset password.
- `/token` takes an `OAuth2PasswordRequestForm`, so the client sends `username` and `password` as **form data**, not JSON.

> [!warning] This reset endpoint is unsafe as written
> Anyone who knows a username can set a new password, no login or proof of identity needed. The book's version only returns "If an account exists, a password reset link will be sent to the provided email", so the real reset happens through an emailed link. Treat my version as a placeholder. A real reset should also revoke all the user's active tokens (see the flows below).

### Example 8-12: wire the routers into the app

The resource endpoints move into their own router, and the whole router is protected at once.

```python
# routes/resource.py
from fastapi import APIRouter

router = APIRouter(prefix="/generate", tags=["Resource"])

@router.get("/text")  # ⚠️ book: "/generate/text" on a router already prefixed with /generate
def serve_language_model_controller():  # params from earlier chapters
    ...

@router.get("/audio")  # ⚠️ same double-prefix fix
def serve_text_to_audio_model_controller():  # params from earlier chapters
    ...

# main.py
from fastapi import Depends, FastAPI

import routes
from dependencies.auth import get_current_user

app = FastAPI(lifespan=lifespan)
app.include_router(routes.auth.router)  # ⚠️ prefix and tags are already set on the router
app.include_router(
    routes.resource.router,
    # ⚠️ book: dependencies=[AuthenticateUserDep]. The list needs Depends(...) objects,
    #    not Annotated aliases.
    dependencies=[Depends(get_current_user)],
)
```

- The controller bodies (`...`) stand for the existing code from earlier chapters.
- The router-level dependency means every `/generate/...` request now needs an `Authorization: Bearer <token>` header.

---

## Authentication flows

A usable JWT system is more than a login button.

### Core flows

- **Registration**: new users send an email and a strong password. Check password strength, email uniqueness, and that they confirmed both. Never store the raw password.
- **Login**: correct credentials get a unique, temporary JWT. Resource routers reject any request without a valid one. "Valid" means the signature checks out **and** the token is still active in the database.
- **Logout**: revoke the current token so nobody can reuse it.

### Production flows

- **Verifying identity**: email verification stops spambots from creating active accounts and eating server resources.
- **Resetting passwords**: when a user resets, revoke **all** their active tokens.
- **Forcing logout**: revoke every token a user has, on every device, so stolen tokens stop working.
- **Disabling accounts**: admins or users can block future logins.
- **Deleting accounts**: remove personally identifiable information (PII) on request, possibly keeping other data.
- **Blocking repeated failed logins**: temporarily lock an account after several failures in a short time.
- **Refresh tokens**: see below.
- **2FA / MFA**: add a second step (SMS/email code, one-time password, authenticator app) before the token is issued, so a leaked password isn't enough.

> [!definition] Access token vs refresh token
> The **access token** is short-lived (minutes) and sent with every request. The **refresh token** is long-lived and only used to get a new access token when the old one expires. Users stay logged in without retyping their password, and a stolen access token stops working soon.

> [!definition] MFA (multi-factor authentication)
> Requiring two or more kinds of proof, like a password plus a code from your phone. 2FA is the two-factor case.

### Security considerations

> [!warning]
> This list isn't complete. Check the **OWASP Top 10 Web Application Security Risks** and the **OWASP Authentication Cheat Sheet** before rolling your own.

- Add **rate limiting**, **geo/IP tracking**, and **account lockouts** against automated attacks.
- Building auth from scratch is risky. Third-party providers ship these features already: **Okta/Auth0, Firebase Auth, Amazon Cognito** (hosted) or **KeyCloak** (self-hosted).
- Credential-based JWT auth still stores password hashes, so password spraying and credential stuffing remain a risk.
- If you need to access a user's resources on **other** services, you need **OAuth**.

---

## OAuth authentication

> [!definition] OAuth 2.0
> An open standard for **access delegation**. A user lets your app have limited, time-boxed access to their account on another service, without giving your app their password.

> [!definition] Identity provider (IdP)
> A platform that authenticates users for other apps and issues tokens asserting who they are. GitHub, Google, Microsoft 365, Apple, Meta, and LinkedIn are a few of hundreds.

Using an IdP:

- **Offloads security risk**: you don't store passwords, so brute-force and stuffing attacks against your DB go away.
- **Smooths UX**: users log in with an account they already have and trust.
- **Unlocks external resources**: calendars, files, social feeds, profile info.

### The authorization code flow

The most common OAuth2 flow for apps with a backend.

> [!definition] Scope
> A named permission your app asks for, like `user` or `read:user`. The user sees the list and approves it.

> [!definition] Redirect URI
> The URL in your app where the IdP sends the user back after login. It has to be pre-registered with the IdP, or the IdP refuses to send a code there.

> [!definition] Authorization code (grant code)
> A short-lived, one-time code the IdP gives your app after the user consents. Your backend swaps it for tokens.

1. **Start**: the user clicks "Login with [Provider]".
2. **Redirect to the IdP**: your app sends the user to the IdP's authorization server with your **client ID**, the **scopes** you want, and your **redirect URI**.
3. **Login and consent**: the user logs into the IdP, which shows a consent screen listing the requested scopes.
4. **Decision**: the user grants all, some, or none of the scopes.
5. **Code issued**: if they consent, the IdP redirects back to your redirect URI with an **authorization code**.
6. **Token exchange**: your backend sends the code (plus client ID and secret) to the IdP, server to server, and gets back a short-lived **access token** and often a longer-lived **refresh token**.
7. **Resource access**: your app calls the provider's **resource server** with the access token, e.g. to read the user's profile.

### The `state` parameter

> [!definition] CSRF (cross-site request forgery)
> An attack that tricks a logged-in user's browser into sending a request they didn't intend, riding on their existing session.

In step 2, your app generates a random, unguessable string called **state** (a CSRF token), saves it, and sends it to the IdP. In step 5 the IdP sends the same value back. If the two don't match, a third party made the request: stop.

### Custom JWT vs OAuth

| Feature | Custom JWT (self-managed) | OAuth 2.0 (external IdP) |
|---|---|---|
| **Password storage** | You hash, salt, and protect passwords. | None. |
| **Complexity** | High: registration, reset, MFA are all on you. | Moderate: you implement the handshake. |
| **Trust** | Users must trust your security. | Users trust established brands. |
| **Third-party data** | No access to external resources. | Can access calendars, files, social data. |

![[Pasted image 20260126015446.png]]

---

## OAuth with GitHub

First, register an **OAuth App** in GitHub (Settings > Developer settings) to get a client ID and client secret. These let GitHub identify your app.

### Example 8-13: redirect to GitHub's login

```python
# routes/auth.py (continued)
import secrets
from urllib.parse import urlencode

from fastapi import Request
from fastapi.responses import RedirectResponse

client_id = "your_client_id"
client_secret = "your_client_secret"

# ⚠️ book: status_code=status.HTTP_301_REDIRECT. That constant doesn't exist, and the
#    returned RedirectResponse sets its own status (307) anyway, so I dropped it.
@router.get("/oauth/github/login")
def oauth_github_login(request: Request) -> RedirectResponse:
    state = secrets.token_urlsafe(16)
    # ⚠️ book saved a SECOND random value (csrf_token) in the session instead of `state`,
    #    so the state GitHub sends back could never match. Store the same value you send.
    request.session["x-csrf-state-token"] = state

    redirect_uri = request.url_for("oauth_github_callback")
    # ⚠️ book built the query string by hand; urlencode escapes the redirect_uri properly
    params = urlencode(
        {"client_id": client_id, "scope": "user", "state": state, "redirect_uri": str(redirect_uri)}
    )
    return RedirectResponse(url=f"https://github.com/login/oauth/authorize?{params}")
```

- `https://github.com/login/oauth/authorize` is GitHub's authorization endpoint. GitHub's docs list `state` as "strongly recommended".
- `scope=user` asks for access to the user's profile, so that's what the consent screen shows.
- `request.url_for(...)` builds the callback URL from the route's function name.
- `request.session` only works once `SessionMiddleware` is added (Example 8-17).

### Example 8-14: login button in Streamlit

```python
# client.py
import requests
import streamlit as st

if st.button("Login with GitHub"):
    response = requests.get("http://localhost:8000/auth/oauth/github/login")
    if not response.ok:
        st.error("Failed to login with GitHub. Please try again later")
        response.raise_for_status()
```

> [!warning] The browser has to follow the redirect
> `requests.get` follows the redirect on the Streamlit **server**, so the user's browser never actually lands on GitHub's login page. In practice the button needs to open the backend's login URL in the user's browser.

What happens next:

- The user logs into GitHub and sees the consent screen.
- If they accept, GitHub redirects back to your app with a **code** and the **state**. Check that the state matches.
- Swap the code for an access token.

### Example 8-15: exchange the code for an access token

```python
# dependencies/auth.py (continued)
from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException
from loguru import logger

client_id = "your_client_id"
client_secret = "your_client_secret"

async def exchange_grant_with_access_token(code: str) -> str:
    try:
        body = {"client_id": client_id, "client_secret": client_secret, "code": code}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://github.com/login/oauth/access_token", json=body, headers=headers
            ) as resp:
                access_token_data = await resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch the access token. Error: {e}")
        raise HTTPException(status_code=503, detail="Failed to fetch access token")

    if not access_token_data:
        raise HTTPException(status_code=503, detail="Failed to obtain access token")

    return access_token_data.get("access_token", "")

ExchangeCodeTokenDep = Annotated[str, Depends(exchange_grant_with_access_token)]
```

- `code` arrives as a query parameter on the callback URL. FastAPI fills it in because it's a plain function argument.
- `POST https://github.com/login/oauth/access_token` with client ID, secret, and code is GitHub's documented exchange. `Accept: application/json` makes GitHub reply in JSON instead of URL-encoded form.
- Any network failure turns into a 503 with a generic message. The details go to the log.

### CSRF and open redirects in OAuth

The callback endpoint must check the state, so nobody can pretend to be GitHub's authorization server.

- In OAuth2, an attacker can abuse an **open redirect** to intercept the initial authorization request and send the user to the attacker's site after login.
- An attacker can also clone your frontend. If a user logs into GitHub through the fake site, the attacker can use a redirect URL pointing at their own server, grab the code, and swap it for a token.

> [!definition] Open redirect
> A bug where your app redirects to any URL given in a parameter. Attackers use it to bounce users (and codes) to their own servers.

![[Pasted image 20260126021538.png]]

Defenses:

- The **state** parameter ties the response to the session that started the flow.
- **Pre-register** redirect URLs with the IdP and validate them strictly.
- Teach users about phishing, and log and monitor for suspicious requests.

### Example 8-16: the callback endpoint

```python
# routes/auth.py (continued)
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from dependencies.auth import ExchangeCodeTokenDep

def check_csrf_state(request: Request, state: str) -> None:
    # ⚠️ book read "x-csrf-token", but Example 8-13 writes "x-csrf-state-token"
    if state != request.session.get("x-csrf-state-token"):
        raise HTTPException(detail="Bad request", status_code=status.HTTP_401_UNAUTHORIZED)

@router.get("/oauth/github/callback", dependencies=[Depends(check_csrf_state)])
async def oauth_github_callback(access_token: ExchangeCodeTokenDep) -> RedirectResponse:
    response = RedirectResponse(url="http://localhost:8501")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,     # ⚠️ new: only send the cookie over HTTPS (Starlette's default is False)
        samesite="lax",  # ⚠️ new: written out explicitly; "lax" is also Starlette's default
    )
    return response
```

- `check_csrf_state` runs first as a router dependency. If the state is wrong, the code exchange never happens.
- FastAPI resolves `ExchangeCodeTokenDep` before the handler runs, so `access_token` is already GitHub's token.
- The token goes into an **HttpOnly** cookie, which JavaScript in the page can't read.

> [!definition] Cookie flags
> - **HttpOnly**: page JavaScript can't read the cookie, which limits XSS theft.
> - **Secure**: the browser only sends it over HTTPS.
> - **SameSite**: controls whether it's sent on cross-site requests. `lax` sends it on top-level navigations but not on cross-site form posts or embedded requests.

> [!warning] Don't hand the user's GitHub token to the browser
> The book warns that if this token is stolen, your app has exposed the user's GitHub account. Better: issue your **own** short-lived token tied to the GitHub token. Then a stolen token only works inside your app.

### Example 8-17: session middleware

The session used for the state check needs Starlette's `SessionMiddleware`. It keeps the session in a signed cookie that the client can't modify.

```python
# main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

...

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key="your_secret_key",
    # https_only=True,  # ⚠️ new: Starlette's docs say to turn this on in production (default False)
)
```

> [!warning]
> Don't store or trust OAuth state in ordinary cookies you read yourself: third parties can read and change them. Never trust data from the client. Starlette's session cookie is **signed**, so it can't be changed, but it's still readable, so keep secrets out of it.

Here the "requester" being checked is GitHub's authorization server, which is sending you the code. Once the state matches, you swap the code for an access token.

> [!tip]
> The open-source **authlib** package handles most of this OAuth plumbing for you.

### Example 8-18: fetch the user's GitHub profile

With the access token you can call GitHub's API for the user's name, email, and avatar, and register them in your app.

```python
# routes/auth.py (continued)
from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
HTTPBearerDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

async def get_user_info(credentials: HTTPBearerDep) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {credentials.credentials}"}
            async with session.get("https://api.github.com/user", headers=headers) as resp:
                return await resp.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to obtain user info - Error: {e}")

GetUserInfoDep = Annotated[dict, Depends(get_user_info)]

# ⚠️ book reused "/oauth/github/callback", which clashes with Example 8-16's route
@router.get("/oauth/github/user")
async def get_current_user_controller(user_info: GetUserInfoDep) -> dict:
    return user_info
```

- The client sends the GitHub token as a bearer token, and `HTTPBearer` pulls it out.
- `GET https://api.github.com/user` with `Authorization: Bearer <token>` returns the profile, matching GitHub's docs.

---

## OAuth2 flow types

What you just built is the **authorization code flow**. IdP docs mention others, which can be confusing until you know when each one fits.

> [!definition] PKCE (proof key for code exchange, "pixie")
> An add-on to the authorization code flow. You send a hashed secret (`code_challenge`) with the first request, then the unhashed `code_verifier` when exchanging the code. Someone who steals the code can't use it without the verifier.

| Flow | How it works | Watch out for | Use it for |
|---|---|---|---|
| **Authorization code (+PKCE)** | Get a code via user login, swap it for a token. | Keep the provider's token on the server, never in the browser. Use PKCE when you can. | Web apps with a backend; mobile apps with PKCE (they can't hide a client secret). |
| **Implicit** | Get an access token directly, no code. | Less secure: the token is exposed to the browser. | SPAs with no backend, prototypes, when the code flow isn't possible. |
| **Client credentials** | Your app swaps its own client ID + secret for a token. | No user involved; you only reach **your own** resources. Store the credentials safely. | Machine-to-machine, server-to-server. |
| **Resource owner password** | Swap the user's username + password for a token. | High risk: you handle the user's credentials directly. Avoid it. | Legacy systems only. |
| **Device authorization** | Visit a URL on another device and enter a code. | Needs a second device with a browser. | Smart TVs, consoles, IoT. |

> [!tip] PKCE on GitHub
> GitHub's docs now list `code_challenge` (S256 only) and `code_verifier` as "strongly recommended" for OAuth apps, so it's worth adding to Examples 8-13 and 8-15.

---

## Authorization

Authentication tells you **who** someone is. Authorization decides **what** they can do.

An authorization system works like a function with three inputs and a yes/no output:

- **Actor**: the user, or a service acting for the user.
- **Action**: read, write, delete, execute, ...
- **Resource**: the thing being targeted (a DB record, a GenAI model, a file).

To decide, it uses authorization data: user attributes, relationships (team/group/org memberships), resource ownership, roles, and permissions.

Then it **enforces** the decision:

- **Allow**: the request continues.
- **Deny**: return `403 Forbidden`, hide the UI, redirect, or lock the account.

A few `if` statements work at first. As checks spread through the app, logic gets duplicated and tangled with business code. Authorization models give that logic a structure.

---

## Authorization models

> [!definition] RBAC (role-based access control)
> Permissions are grouped into roles, and users get roles. Example: admins can use every GenAI model.

> [!definition] ReBAC (relationship-based access control)
> Access depends on relationships between entities: user-to-user (follower, friend) or user-to-resource (team, group, org). Example: members of a team can use the premium models that team bought.

> [!definition] ABAC (attribute-based access control)
> Access depends on attributes of the user, the resource, and the environment (time, IP, location). Example: a conversation marked `public` is visible to everyone; users with a `paid` attribute get premium models.

RBAC is simplest but least flexible. ReBAC can extend or override RBAC rules, and ABAC is the most fine-grained and can override both.

| Type | Benefits | Limitations | Use cases |
|---|---|---|---|
| **RBAC** | Simple to manage and audit. | Limited flexibility; "role explosion" in complex systems. | Enterprise apps, finance, healthcare. |
| **ReBAC** | Fine-grained control over shared resources. | Needs relationship data from many sources; complex evaluation. | Social networks, collaborative SaaS, project tools. |
| **ABAC** | Very flexible; dynamic, context-aware rules. | Needs attribute data from many sources; complex evaluation. | Cloud services, IoT, compliance, personalized UX. |

![[Pasted image 20260126182655.png]]

---

## Role-based access control (RBAC)

Roles are popular because they're easy to grasp. They usually match who the user is and what they do, and sometimes map straight onto your org chart.

- **Permission**: an action on a resource, like "use the paid LLM".
- **Role**: a group of permissions.
- **User**: gets one or more roles.

Preset roles cut decision fatigue: instead of setting dozens of permissions per user, an admin picks a role.

Most services start with two roles:

| Feature | User (member) | Administrator |
|---|---|---|
| **Core features** | Use GenAI models; read/write own resources. | Full access to every resource. |
| **User management** | None. | Assign/remove roles; enable/disable accounts. |
| **Data privacy** | Can't see other users' data. | Can see data across the platform. |
| **Early access** | Standard features. | Beta features or restricted models. |

### Example 8-19: RBAC with a dependency

```python
# dependencies/auth.py (continued)
from fastapi import HTTPException, status

from entities import User

# ⚠️ book: user: User = Depends(AuthService.get_current_user). That's an unbound method,
#    so FastAPI would treat `self` as a request parameter. CurrentUserDep is defined above.
async def is_admin(user: CurrentUserDep) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform this action",
        )
    return user
```

```python
# routes/resource.py
from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user, is_admin

router = APIRouter(
    dependencies=[Depends(get_current_user)],  # ⚠️ was Depends(AuthService.get_current_user)
    prefix="/generate",
    tags=["Resource"],
)

@router.post("/image", dependencies=[Depends(is_admin)])
async def generate_image():
    ...
    return {"message": "Image generated successfully."}

@router.post("/text")
async def generate_text():
    ...
    return {"message": "Text generated successfully."}
```

- `is_admin` builds on the current-user dependency. It's `async` because the child dependency hits the database.
- `/image` is admin-only. Logged-in non-admins get a 403.
- `/text` is open to any logged-in user, because the router itself only requires authentication.
- With the same pattern you can pick different system prompts or fine-tuned model variants per role.

![[Pasted image 20260126183923.png]]

> [!warning] Don't let the model enforce permissions
> Do authorization in your application code, not in the prompt. LLMs can be **prompt-injected** into ignoring their instructions and producing unauthorized output.

### Example 8-20: more complex RBAC

When new roles share a subset of another role's permissions (say, moderators and admins), you can use sub-dependencies or one **parameterized** dependency:

![[Pasted image 20260126185220.png]]

```python
# dependencies/auth.py (continued)
# ⚠️ book: has_role(user, roles) used as Depends(lambda user: has_role(user, [...])).
#    FastAPI reads the lambda's signature, treats `user` as a query parameter, and never
#    injects the logged-in user. FastAPI's docs parameterize a dependency with a callable
#    class instance instead.
class RoleChecker:
    def __init__(self, roles: list[str]) -> None:
        self.roles = roles

    async def __call__(self, user: CurrentUserDep) -> User:
        if user.role not in self.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to perform this action",
            )
        return user
```

```python
# routes/resource.py
from dependencies.auth import RoleChecker

@router.post("/image", dependencies=[Depends(RoleChecker(["ADMIN", "MODERATOR"]))])
async def generate_image():
    ...
    return {"message": "Image generated successfully for ADMIN or MODERATOR."}

@router.post("/text", dependencies=[Depends(RoleChecker(["EDITOR"]))])
async def generate_text():
    ...
    return {"message": "Text generated successfully for EDITOR."}
```

- `RoleChecker([...])` is built once with the allowed roles. FastAPI calls its `__call__` per request and injects the current user into it.
- One class covers every role combination, so you don't need a new function per role.

**RBAC in short:** permissions attach to roles, not people, which keeps things easy to manage and audit. But many fine-grained roles lead to role explosion, and RBAC can't express team hierarchies or dynamic rules (time, preferences, privacy settings).

---

## Relationship-based access control (ReBAC)

ReBAC extends RBAC by focusing on **relationships** between users and resources. RBAC asks what a user *is*; ReBAC asks how the user relates to *this* resource.

- **Resource-level roles**: instead of one global role, you define what each role can do on each resource type.
- **A graph**: nodes are resources or identities, edges are relationships.
- **Inheritance**: permissions flow from a parent to its children.

| | RBAC | ReBAC |
|---|---|---|
| **Scope** | Broad, app-wide. | Per resource type. |
| **Moderator on conversations** | Can moderate everything. | Can **read** and **delete** conversations. |
| **Moderator on teams** | Can moderate everything. | **Read-only** on team data. |
| **How it's expressed** | "User is a moderator." | "User has relationship X to resource Y." |

Inheritance saves a lot of work. Instead of sharing private LLM conversations one by one:

1. Group them in a **folder** or **team**.
2. Set permissions on the parent.
3. The conversations inside inherit them.

![[Pasted image 20260126190927.png]]

> [!tip]
> If you go with ReBAC, draw the relationships between resources and identities first: the policies, resources and their actions, resource-level roles, and how entities connect.

ReBAC fixes RBAC's role explosion by combining roles with relationships. It handles hierarchies well and supports **reverse queries** ("who can see this?"), so permissions through teams and groups stay efficient. The cost: it's complex to build and maintain, resource-heavy, hard to audit, and less fine-grained than ABAC for rules based on time or location.

---

## Attribute-based access control (ABAC)

ABAC extends basic roles with rules that check **attributes**:

- **User**: role, department, subscription status (`paid`).
- **Resource**: sensitivity, owner, file type, metadata (`has_pii=true`).
- **Environment**: time of day, IP address, location.

Examples:

- **Data protection**: block uploads to a RAG service when the document contains PII (`upload.has_pii = true`).
- **Monetization**: like ChatGPT, only users whose account is `paid` get premium models.

> [!definition] PII (personally identifiable information)
> Data that can identify a person, like a name, email, phone number, or ID number.

| Pros | Cons |
|---|---|
| **Fine-grained**: almost unlimited freedom to write specific policies. | **Hard to audit**: to know who can access a resource, you have to evaluate the attributes of every user. |
| **Dynamic**: reacts to live data like location or document content. | **Overhead**: gets cumbersome with thousands of attributes and roles. |
| **Rules scale**: one rule covers everyone who shares an attribute. | **Implementation**: harder than RBAC, though less structurally complex than ReBAC. |

The difference in one line each:

- **RBAC**: "You can do this because you're a **manager**."
- **ABAC**: "You can do this because you're a **manager** in **HR** accessing **internal data** during **business hours**."

![[Pasted image 20260126191253.png]]

---

## Hybrid authorization

Large apps usually mix all three. Admins can reach any resource and manage users (RBAC). Users can make private resources public with a visibility attribute (ABAC) and add teammates to collaborate (ReBAC).

- **RBAC** keeps permission management simple and auditable.
- **ReBAC** handles hierarchies and reverse queries.
- **ABAC** adds fine-grained, context-aware rules.

![[Pasted image 20260126192555.png]]

### Example 8-21: a hybrid check

```python
# dependencies/auth.py (continued)
from typing import Annotated

from fastapi import Depends, HTTPException, status

...  # import services and entities here (Team, Resource, TeamService, ResourceService)

# CurrentUserDep is defined earlier in this file
# ⚠️ same unbound-method issue as Example 8-19: TeamService.get_current_team and
#    ResourceService.get_resource are placeholders and need the same function wrapper
TeamMembershipDep = Annotated[Team, Depends(TeamService.get_current_team)]
ResourceDep = Annotated[Resource, Depends(ResourceService.get_resource)]

def authorize(user: CurrentUserDep, resource: ResourceDep, team: TeamMembershipDep) -> bool:
    if user.role == "ADMIN":    # RBAC
        return True
    if user.id in team.members:  # ReBAC
        return True
    if resource.is_public:      # ABAC
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")
```

```python
# routes/resource.py
from fastapi import APIRouter, Depends

from dependencies.auth import authorize

router = APIRouter(dependencies=[Depends(authorize)], prefix="/generate", tags=["Resource"])

@router.post("/image")
async def generate_image(): ...

@router.post("/text")
async def generate_text(): ...
```

- Each `if` is one model: role, then relationship, then attribute. The first match allows the request.
- One router-level dependency protects every endpoint in the router.

Every bypass rule you add ("admins skip this", "public skips that") makes this logic harder to maintain.

### Example 8-22: a separate authorization service

If permissions change often, move decisions into their own service. Your app's code stays the same while the rules change.

![[Pasted image 20260126193059.png]]

```python
# authorization_api.py (Authorization Service)
from typing import Annotated, Literal

from fastapi import Depends, FastAPI
from pydantic import BaseModel

...  # import services and entities here

ActionRep = Annotated[Literal["READ", "CREATE", "UPDATE", "DELETE"], str]

class AuthorizationResponse(BaseModel):
    allowed: bool

app = FastAPI()

@app.get("/authorize")  # ⚠️ book printed `app.get(...)` without the @, so the route was never registered
def authorization_controller(
    user: CurrentUserDep, resource: ResourceDep, action: ActionRep
) -> AuthorizationResponse:
    if user.role == "ADMIN":
        return AuthorizationResponse(allowed=True)
    if action in user.permissions.get(resource.id, []):
        return AuthorizationResponse(allowed=True)
    ...  # other permission checks
    return AuthorizationResponse(allowed=False)
```

```python
# genai_api.py (GenAI Service)
from fastapi import APIRouter, Depends, HTTPException, status  # ⚠️ book forgot to import Depends
from pydantic import BaseModel

class AuthorizationData(BaseModel):
    user_id: int
    resource_id: int
    action: str

authorization_client = ...  # create the authorization client

async def enforce(data: AuthorizationData) -> bool:
    response = await authorization_client.decide(data)
    if response.allowed:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")

router = APIRouter(dependencies=[Depends(enforce)], prefix="/generate", tags=["Resource"])

@router.post("/text")
async def generate_text_controller():
    ...
```

- The authorization service answers one question: is this actor allowed this action on this resource?
- The GenAI service just asks and enforces the answer with a 403.

Building a full authorization service from scratch takes a lot of time. Providers like **Oso, Permify, and Okta/Auth0** do this for you.

---

## Summary

- **Authentication** proves who someone is. **Authorization** decides what they can do.
- Four authentication methods: **basic**, **token (JWT)**, **OAuth**, and **key-based**.
- Built from scratch: basic auth, then JWT with **salted password hashes**, signed access tokens stored in the DB for **revocation**, login, and logout.
- **OAuth2 with GitHub**: the authorization code flow, the **state** parameter against CSRF, and other flows (PKCE, implicit, client credentials, password, device).
- Attacks to know: **credential stuffing, password spraying, CSRF, open redirect, phishing**.
- Authorization models: **RBAC, ReBAC, ABAC**, hybrids, and a separate authorization service, all enforced with FastAPI dependencies.

**Next chapter:** testing GenAI services: unit, integration, end-to-end, and regression tests, plus mocking, patching, and dealing with probabilistic models.

---
%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[FastApi - Security]]
- [[JWT - API AUTH]]
- [[FastAPI Users - Auth Backend]]
%% related:end %%
