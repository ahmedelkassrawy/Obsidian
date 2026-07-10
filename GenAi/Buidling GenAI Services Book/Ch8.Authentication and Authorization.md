#### Authentication and Authorization
While authentication is about verifying the identity, authorization focuses on verifying permissions of an identity to access or mutate resources.
#### Authentication Methods
- Basic
	Requiring the use of credentials such as username and password to
	verify identity.
- JSON Web Tokens (JWT)
	Requiring the use of access tokens to verify identity. You can think of
	access tokens like cinema tickets that dictate whether you can access
	the screens and which screen you’re visiting and where you’re sitting.
- OAuth
	Verifying an identity via an identity provider using the OAuth2
	standard.
- Key-based
	Using a private and public key pair to authenticate an identity. Instead
	of tokens, the authorization server issues a public key to the client
	and stores a copy of a linked private key that it can use later for
	verification

![[Pasted image 20260125173927.png]]

| **Type**        | **Benefits**                                                                                                           | **Limitations**                                                                                               | **Use Cases**                                                                                   |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Basic**       | Simplicity; Fast to implement; Easy to understand.                                                                     | Sends credentials in plain text (requires HTTPS); Hard to revoke without changing passwords.                  | Prototyping; Internal non-critical environments.                                                |
| **Token** (JWT) | Scalability; Decoupling facilitates microservices; Self-contained (reduces DB lookups); Can be passed in HTTP headers. | Need to regenerate short-lived tokens; Client-side storage complexity; Revocation is difficult before expiry. | Single Page Apps (SPAs); Mobile apps; REST APIs requiring custom auth flows.                    |
| **OAuth**       | Delegates authentication to external providers; Standardized (OAuth2); Access to external resources on user's behalf.  | Complex to implement; Variations in how different providers (Google, GitHub) implement the flow.              | Apps requiring data from external identity providers; Third-party integrations.                 |
| **Key-based**   | Similar to SSH; Highly secure for machine-to-machine communication; No manual login required.                          | Managing/securing private keys is complex; Compromised keys are high risk; Harder to scale for human users.   | Enterprise apps using SSH; Small-scale internal apps; API access within automated environments. |
|                 |                                                                                                                        |                                                                                                               |                                                                                                 |
#### Basic Authentication
In basic authentication, the client provides a username and password when making a request to access resources from the server. It is the simplest technique as it won’t require cookies, session identifiers, or any login forms to be implemented. Because of its simplicity, basic authentication is ideal for sandbox environments and when prototyping. However, avoid using it in production environments as it transmits usernames and passwords in plain text on every request, making it highly vulnerable to interception attacks.

To perform an authenticated request via basic authentication, you must add an **Authorization** header with a value of Basic for the server to successfully authenticate it. The value must be a **Base64 encoding** of the username and password joined by a single colon (i.e., **base64.encode(ali:secretpassword)** .

*Implementing basic authentication in FastAPI*
```python
import secrets
from typing import Annotated
from fastapi import Depends,FastAPI,HTTPException,status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

username_bytes = b"ali"
password_bytes = b"secretpassword"

def authenticate_user(credentials: Annotated[HTTPBasicCredentials,Depends(security)]) -> str:
    is_correct_username = secrets.compare_digest(credentials.username.encode("UTF-8"),username_bytes)
    is_correct_passsword = secrets.compare_digest(credentials.password.encode("UTF-8"),password_bytes)
    
    if not (is_correct_username and is_correct_passsword):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username

AuthenticatedUserDep = Annotated[str, Depends(authenticate_user)]

@app.get("/users/me")
async def get_current_user(username: AuthenticatedUserDep):
    return {"message": f"Current user is {username}"}
```

1. FastAPI has implemented several HTTP security mechanisms including HTTP Ba sic that can leverage the FastAPI’s dependency injection system.
2. Use the secrets built-in library to compare the provided username and password with the server’s values. Using secrets.compare_digest() ensures the duration of checking operations remain consistent no matter what the inputs are to avoid timing attacks.3 Note that secrets.compare_digest() can only accept byte or string inputs containing ASCII characters (i.e., English-only characters). To handle other characters, you will need to encode the inputs with UTF 8 to bytes first before performing the credential checks. 
3. Return a standardized authorization HTTPException compliant with security standards that browsers understand so that they show the login prompt again to the user. The exception message must be generic to avoid leaking any sensitive information, such as the existence of a user account, to attackers. 
4. Using the HTTPBasic with Depends() returns the HTTPBasicCredentials object that contains the provided username.

#### JSON Web Tokens (JWT) Authentication
What is JWT?
JWTs are a URL-safe and compact way of asserting claims between applications via tokens. 

These tokens consist of three parts
Headers 
	Specify the token type and signing algorithm in addition to the datetime and the issuing authority
Payload 
	Specify the body of the token representing the claims on the resource alongside additional metadata.
Signature 
	The function that creates the token will also sign it using the encoded payload, encoded headers, a secret, and the signing algorithm.

JWTs are secure, compact, and convenient since they can hold all the information needed to perform user authentication, avoiding the need for multiple database round trips. In addition, due to their compactness, you can transfer them across the network using the HTTP POST body, headers, or URL parameters.

#### Getting started with JWT authentication
```python
pip install passlib python-jose
```

With the dependencies installed, you will then need tables in the database to store the generated users and associated token data. For data persistence, let’s migrate the database to create the users and tokens tables
![[Pasted image 20260125180251.png]]

you will spot that the tokens table has a one-to-many relationship with the users table. You can use the token records to track successful login attempts for each user and to revoke access if needed.
#### Declare user SQLAlchemy ORM models
entities.py
```python
from datetime import UTC,datetime
import uuid
from sqlalchemy import ForeignKey,Index,String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key = True, default = uuid.uuid4)
    email: Mapped[str] = mapped_column(String(length = 255), unique = True)
    username: Mapped[str] = mapped_column(String(length = 255), unique = True, index = True)
    hashed_password: Mapped[str] = mapped_column(String(length=255))
    role: Mapped[str] = mapped_column(default="USER")
    is_active: Mapped[bool] = mapped_column(default = True)
    created_at: Mapped[datetime] = mapped_column(default = datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default = datetime.now(UTC),
                                                 onupdate = datetime.now(UTC))

    __table_args__ = (Index("ix_users_email","email"),)
```

You will be using the ORM models at the data access layer while the Pydantic schemas will validate incoming and outgoing authentication data at the endpoint layer.

Declare user Pydantic schemas with username and password field validators
schemas.py
```python
from datetime import datetime
from typing import Annotated
from pydantic import (UUID,AfterValidator,BaseModel,ConfigDict,Field,validate_call)
import uuid

@validate_call
def validate_username(value:str) -> str:
    if not value.isalnum():
        raise ValueError("Username must be alphanumeric")
    return value

@validate_call
def validate_password(value:str) -> str:
    validations = [
        (
            lambda x: any(char.isdigit() for char in x),
            "Password must contain at least one digit"
        ),
        (
            lambda x: any(char.isupper() for char in x),
            "Password must contain at least one uppercase letter"
        ),
        (
            lambda x: any(char.islower() for char in x),
            "Password must contain at least one lowercase letter"
        )
    ]
    
    for condition , error_message in validations:
        if not condition(value):
            raise ValueError(error_message)
    return value

ValidUsername = Annotated[str,Field(min_length=3, max_length = 20), 
                          AfterValidator(validate_username)]
ValidPassword = Annotated[str,Field(min_length=8, max_length=64),
                          AfterValidator(validate_password)]

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    username: ValidUsername
    is_active: bool = True
    role: str = "USER"

class UserCreate(UserBase):
    password: ValidPassword

class UserInDB(UserBase):
    hashed_password:str

class UserOut(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

1. Validate both username and password to enforce higher security requirements.
2. Allow Pydantic to read SQLAlchemy ORM model attributes instead of having to manually populate Pydantic schemas from SQLAlchemy models.
3. Use inheritance to declare several Pydantic schemas based on a user base model.
4. Create a separate schema that accepts the hashed_password field to be used only for creating new user records during the registration process. All other schemas must skip storing this field to eliminate the risk of password leakage.
#### Declare token ORM models and Pydantic schemas
entities.py
```python
class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key = True, default = uuid.uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default = True)
    ip_address: Mapped[str | None] = mapped_column(String(length = 255))
    created_at: Mapped[datetime] = mapped_column(default = datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default = datetime.now(UTC),
                                                 onupdate = datetime.now(UTC))
    
    user = relationship("Users",back_populates="tokens")

    __table_args__ = (
        Index("ix_tokens_user_id","user_id"),
        Index("ix_tokens_ip_address","ip_address")
    )
```

schemas.py
```python
class TokenBase(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    user_id:int
    expires_at:datetime
    is_active:bool = True
    ip_address: str | None = None

class TokenCreate(TokenBase):
    pass

class TokenOut(TokenBase):
    access_token: str
    token_type: str = "Bearer"
```

```python
alembic revision --autogenerate -m "create users and tokens tables"
```

```python
alembic upgrade head
```

The architecture of the JWT authentication system you’re going to implement in your FastAPI GenAI service.
![[Pasted image 20260125233709.png]]

#### Hashing and Salting
---
## Phase 1: User Registration (Storage)

When a user creates an account, the system doesn't just "lock" the password; it transforms it into a unique fingerprint that cannot be reversed.

1. **Password Entry:** The user provides a plain-text password (e.g., `P@ssword123`).
2. **Generating the Salt:** The system generates a **salt**—a random, unique string of characters.
3. **Combining:** The salt is appended (or prepended) to the plain password.
* *Example:* `P@ssword123` + `xyz789` (salt) = `P@ssword123xyz789`.
	1. **Hashing:** This combined string is run through a cryptographic hashing algorithm (like Argon2 or bcrypt). This produces a fixed-length string of random-looking characters.
	2. **Storage:** The system stores the **Salt + Hash** in the database. It does **not** store the plain-text password.

---
## Phase 2: User Login (Verification)
Since hashes cannot be "decrypted," the system verifies a user by repeating the math and seeing if the results match.

1. **Credential Input:** The user enters their username and plain-text password.
2. **Retrieval:** The system looks up the user in the database and retrieves the **stored salt** and the **stored hash**.
3. **Re-Hashing:** The system takes the password the user just typed and combines it with the **retrieved salt**. It then runs this through the same hashing algorithm.
4. **Comparison:**
	* **If New Hash == Stored Hash:** The password is correct, and the user is logged in.
	* **If New Hash != Stored Hash:** The password is incorrect, and access is denied.
---
## Why this protects you

| Threat | How Salting/Hashing Fixes It |
| --- | --- |
| **Database Leak** | If an attacker steals the database, they only see hashes. They cannot "reverse" them to find the actual passwords. |
| **Rainbow Tables** | These are "cheat sheets" of pre-calculated hashes. Salting makes the input unique, rendering these pre-calculated tables useless. |
| **Duplicate Passwords** | If two users use `Password123`, their salts will be different (e.g., `Salt_A` and `Salt_B`). This results in two completely different hashes in the database. |
![[Pasted image 20260125234635.png]]

---
#### Implement a password service
services/auth.py
```python
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

class PasswordService:
    secuirty = HTTPBearer()
    pwd_context = CryptContext(schemes = ["bcrypt"])

    async def verify_password(self,password:str,hashed_password:str) -> bool:
        return self.pwd_context.verify(password,hashed_password)
    
    async def hash_password(self,password:str) -> str:
        return self.pwd_context.hash(password)
```

1. Create an AuthService with a secret and password context managed by the bcrypt library that will handle all the user password hashing and verification.
2. Use bcrypt’s cryptography algorithm and application secret to hash and verify passwords.

The bcrypt cryptographic library provides the core functionality of the Password Ser vice for hashing and verifying passwords. Using this service, requests can now be authenticated. 
If a request can’t be authenticated, you will also need to raise authorization -related exceptions

exceptions.py
```python
from fastapi import HTTPException,status

UnauthorizedException = HTTPException(
    status_code= status.HTTP_401_UNAUTHORIZED,
    detail = "Unauthorized access",
    headers={"WWW-Authenticate": "Bearer"},
)

AlreadyRegisteredException = HTTPException(
    status_code= status.HTTP_400_BAD_REQUEST,
    detail = "User with given credentials already registered",
)
```

The two most common authorization HTTP exceptions you will raise are related to unauthorized access or bad requests due to using already used usernames.

- Once you have checked a user’s identity via their credentials, you will need to issue them an access token. 
- These tokens should be short-lived to reduce the time-window that an attacker can use the token to access resources if the token is stolen. 
- To reduce the size footprints of the tokens and protect against token forgery, the token service will sign (using a secret) and encode the token payloads with an encoding such as Base64. 
- The payload will normally contain the user’s details such as their ID, role, issuance system, and expiry dates.
- The token service can also decode the payload of received tokens and check their validity during the authentication process. 
- Finally, the token service will also require database access to store and retrieve tokens to perform its functions. Therefore, it should inherit a TokenRepository
#### Implement token repo
repositories.py
```python
from authentication.entities import Token
from repo.interfaces import Repository
from authentication.schemas import TokenCreate,TokenUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class TokenRepository(Repository):
    def __init__(self,session:AsyncSession):
        self.db = session

    async def list(self,skip:int=0,limit:int=100) -> list[Token]:
        async with self.db.begin():
            result = await self.db.execute(
                select(Token).offset(skip).limit(limit)
            )
        results = result.scalars().all()
        return [r for r in results]
    
    async def create(self,token:TokenCreate) -> Token:
        new_token = Token(**token.model_dump())

        async with self.db.begin():
            self.db.add(new_token)
            await self.db.refresh(new_token)
            await self.db.commit()
        return new_token

    async def get(self,token_id:int) -> Token | None:
        async with self.db.begin():
            result = await self.db.execute(
                select(Token).where(Token.id == token_id)
            )
        token = result.scalars().first()
        return token
    
    async def update(self,token_id:int, token:TokenUpdate) -> Token | None:
        async with self.db.begin():
            result = await self.db.execute(
                select(Token).where(Token.id == token_id)
            )
            existing_token = result.scalars().first()
            if not existing_token:
                return None
            
            for key, value in token.model_dump(exclude_unset=True).items():
                setattr(existing_token, key, value)
            
            self.db.add(existing_token)
            await self.db.commit()
            await self.db.refresh(existing_token)
        return existing_token
    
    async def delete(self,token_id:int) -> None:
        token = await self.get(token_id)

        if not token:
            return
        
        async with self.db.begin():
            await self.db.delete(token)
            await self.db.commit()
            await self.db.refresh(token)
            
        return
```

With the TokenRepository implemented, you can now develop the TokenService
services/auth.py
```python
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from datetime import UTC,datetime,timedelta
from exceptions import UnauthorizedException
from jose import JWTError,jwt
import os
from pydantic import UUID4
from authentication.repositories import TokenRepository
from authentication.schemas import TokenCreate,TokenUpdate

class PasswordService:
    secuirty = HTTPBearer()
    pwd_context = CryptContext(schemes = ["bcrypt"])

    async def verify_password(self,password:str,hashed_password:str) -> bool:
        return self.pwd_context.verify(password,hashed_password)
    
    async def hash_password(self,password:str) -> str:
        return self.pwd_context.hash(password)
    
class TokenService:
    secret_key  = "your_secret_key"
    algorithm = "HS256"
    expires_in_minutes = 60

    async def create_access_token(self,data:dict,
                                expires_delta:timedelta | None = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.expires_in_minutes)
        
        token_id = await self.create(TokenCreate(expires_at = expire))
        to_encode.update(
            {
                "exp":expire,
                "iss": "your_service_name",
                "sub": token_id
            }
        )
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self,encoded_token:str) -> dict:
        try:
            return jwt.decode(encoded_token,self.secret_key,algorithms=[self.algorithm])
        except JWTError:
            raise UnauthorizedException

    async def validate(self,token_id:UUID4) -> bool:
        return (token := await self.get(token_id)) is not None and token.is_active
```

1. Implement a TokenService for issuing and checking authentication tokens. Configurations are shared across all instances of the service.
2. Generate access tokens based on data provided to the token service with expiry dates.
3. Create a token record in the database and get a unique identifier.
4. The access token must expire within an hour, so the exp calculated field will be used to check token validity.
5. Encode the generated token into an encoded string using the base64 algorithm.

Now that you have a PasswordService and a TokenService , you can complete the core JWT authentication mechanism with a dedicated higher-level AuthService .

Implement an auth service to handle higher-level authentication logic
services/auth.py
```python
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from datetime import UTC,datetime,timedelta
from exceptions import UnauthorizedException,AlreadyRegisteredException
from jose import JWTError,jwt
import os
from pydantic import UUID4
from authentication.repositories import TokenRepository
from authentication.schemas import TokenCreate,TokenUpdate
from database import db_session
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from authentication.entities import Users
from typing import Annotated
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordRequestForm)
from entities import User,UserCreate,UserInDB
from authentication.entities import Token

# Type aliases for dependency injection
LoginFormDep = Annotated[OAuth2PasswordRequestForm, None]
AuthHeaderDep = Annotated[HTTPAuthorizationCredentials, None]


class PasswordService:
    secuirty = HTTPBearer()
    pwd_context = CryptContext(schemes = ["bcrypt"])

    async def verify_password(self,password:str,hashed_password:str) -> bool:
        return self.pwd_context.verify(password,hashed_password)
    
    async def hash_password(self,password:str) -> str:
        return self.pwd_context.hash(password)
    
class TokenService(TokenRepository):
    secret_key  = "your_secret_key"
    algorithm = "HS256"
    expires_in_minutes = 60

    async def create_access_token(self,data:dict,
                                expires_delta:timedelta | None = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.expires_in_minutes)
        
        token_id = await self.create(TokenCreate(expires_at = expire))
        to_encode.update(
            {
                "exp":expire,
                "iss": "your_service_name",
                "sub": token_id
            }
        )
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self,encoded_token:str) -> dict:
        try:
            return jwt.decode(encoded_token,self.secret_key,algorithms=[self.algorithm])
        except JWTError:
            raise UnauthorizedException

    async def validate(self,token_id:UUID4) -> bool:
        return (token := await self.get(token_id)) is not None and token.is_active
    
class UserService:
    """User service for managing user operations"""
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get(self, username: str) -> Users | None:
        """Get user by username"""
        async with self.db.begin():
            result = await self.db.execute(
                select(Users).where(Users.username == username)
            )
            return result.scalars().first()
    
    async def get_user(self, username: str) -> Users | None:
        return await self.get(username)
    
    async def create(self, user: UserInDB) -> Users:
        """Create a new user"""
        new_user = Users(
            username=user.username,
            hashed_password=user.hashed_password,
            email=getattr(user, 'email', f"{user.username}@example.com")
        )
        async with self.db.begin():
            self.db.add(new_user)
            await self.db.flush()
            await self.db.refresh(new_user)
            await self.db.commit()
        return new_user
    
    async def update_password(self, username: str, hashed_password: str) -> Users | None:
        """Update user password"""
        async with self.db.begin():
            result = await self.db.execute(
                update(Users)
                .where(Users.username == username)
                .values(hashed_password=hashed_password)
                .returning(Users)
            )
            await self.db.commit()
            return result.scalars().first()

class AuthService:
    def __init__(self,db:db_session):
        self.password_service = PasswordService()
        self.token_service = TokenService(db)
        self.user_service = UserService(db)

    async def register_user(self,user:UserCreate) -> User:
        if await self.user_service.get(user.username):
            raise AlreadyRegisteredException
        
        hashed_password = await self.password_service.hash_password(user.password)
        return await self.user_service.create(
            UserInDB(username = user.username, hashed_password=hashed_password)
        )
    
    async def authenticate_user(self,form_data:LoginFormDep) -> Token:
        if not(user := await self.user_service.get_user(form_data.username)):
            raise UnauthorizedException
        if not await self.password_service.verify_password(form_data.password,
                                                           user.hashed_password):
            raise UnauthorizedException
        
        return await self.token_service.create_access_token(user._asdict())
    
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
    
    async def reset_password(self, username: str, new_password: str) -> Users:
        """Reset user password"""
        user = await self.user_service.get(username)
        if not user:
            raise UnauthorizedException
        
        hashed_password = await self.password_service.hash_password(new_password)
        updated_user = await self.user_service.update_password(username, hashed_password)
        
        if not updated_user:
            raise UnauthorizedException
        
        return updated_user 
```

The core authentication logic of the application that verifies whether a user exists and their password credentials. Returns False if any checks fail.
You can now use the AuthService to register and authenticate users using their credentials

Implement authentication controllers to enable login and registration functionality
routes/auth.py
```python
from typing import Annotated
from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from authentication.schemas import TokenOut, UserOut, UserCreate
from authentication.services.auth import AuthService
from database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_auth_service(db: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(db)

@router.post("/register", response_model=UserOut)
async def register_user(
    new_user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserOut:
    user = await auth_service.register_user(new_user)
    return user

@router.post("/token", response_model=TokenOut)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenOut:
    token = await auth_service.authenticate_user(form_data)
    return TokenOut(
        access_token=token,
        token_type="bearer"
    )

@router.post("/logout")
async def logout_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    await auth_service.logout(credentials)
    return {"message": "Logged out successfully"}

@router.post("/reset-password")
async def reset_password(
    username: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    await auth_service.reset_password(username, new_password)
    return {
        "message": "Password has been reset successfully."
    }
```

1. Create an instance of the AuthService and declare reusable annotated dependencies.
2. Create a separate API router for authentication endpoints.
3. Implement endpoints for registering users, user login (token
issuance), user logout (token revocation), and password reset.
4. Since the LogoutUserDep dependency won’t return anything, inject it within the dependency array of the router.

Once you have a dedicated authentication router, create a separate resource router to group all your resource endpoints within. With both routers, you can now add them to your FastAPI app

---
# Authentication Architecture and Flows

Implementing a JWT-based authentication system requires more than just a login button. It involves a lifecycle of core and secondary flows to ensure security, usability, and resilience.
## 1. Core Authentication Flows

These are the fundamental requirements for any identity management system.
### User Registration

* **Process:** New users provide an email and a secure password.
* **Validation:** Logic should check for password strength, email uniqueness, and confirmation matches.
* **Security:** **Never** store raw passwords. Use hashing and salting (e.g., Argon2 or bcrypt) before saving to the database.
### User Login

* **Process:** Upon providing correct credentials, the system generates a unique, temporary **Access Token (JWT)**.
* **Authorization:** Resource routers must reject any request lacking a valid JWT.
* **Verification:** Tokens are validated by checking their digital signature and ensuring they exist/are active in the database.
### User Logout

* **Process:** Revokes the currently issued token.
* **Security:** Invalidating the token in the database prevents attackers from using a stolen token after the legitimate user has ended their session.

---
## 2. Secondary Production-Ready Flows

To move from a prototype to a production system, you must handle "edge case" security and lifecycle management.

### Identity & Security Management

* **Verifying Identity:** Use email verification or CAPTCHAs to prevent spambots from bloating your database.
* **Resetting Passwords:** Provide a secure flow for forgotten passwords. **Crucial:** When a password is reset, all existing active tokens for that user must be revoked immediately.
* **Blocking Brute-Force:** Implement account lockouts or temporary cooling-off periods after multiple failed login attempts.
* **Disabling/Deleting Accounts:** Support administrative "freezing" of accounts or permanent deletion of PII (Personally Identifiable Information) upon user request.
### Advanced Token Handling

* **Forcing Logout:** A global "log out of all devices" feature that revokes every token associated with a specific User ID.
* **Refresh Tokens:** * **Access Tokens:** Short-lived (e.g., 15 minutes) to limit the attack window.
* **Refresh Tokens:** Long-lived tokens used to request new access tokens without forcing the user to re-enter their password.
### Multi-Factor Authentication (MFA/2FA)

* **Layered Security:** Adds a second step (SMS, Email OTP, or Authenticator App) before the final JWT is issued. This mitigates the risk of compromised passwords.

---

## 3. Critical Security Considerations

> [!WARNING]
> This list is not exhaustive. For a complete security posture, consult the **OWASP Top 10 Web Application Security Risks** and the **OWASP Authentication Cheat Sheet**.

### Defensive Mechanisms

To defend against automated attacks, your system should incorporate:

* **Rate Limiting:** Restrict the number of requests from a single IP.
* **Geo/IP Tracking:** Alert users or block access from suspicious or new locations.
* **Account Lockouts:** Prevent "Credential Stuffing" or "Password Spraying" attacks.

### Alternatives to Custom Implementation

Building auth from scratch is high-risk. Consider industry-standard providers:

* **SaaS:** Okta, Auth0, Firebase Auth, Amazon Cognito.
* **Self-Hosted:** KeyCloak.

### When JWTs Aren't Enough (OAuth)

If your application needs to access external resources (e.g., "Post on Twitter on the user's behalf"), you must implement **OAuth**. This protocol facilitates identity verification between your system and external providers securely.

---
#### Implementing OAuth Authentication

OAuth is an open-standard authorization framework that enables **access delegation**. It allows applications to obtain limited access to user accounts on an HTTP service—such as Google, GitHub, or Facebook—without requiring the user to share their login credentials directly with the application.

## The Role of Identity Providers (IDPs)

Identity Providers are platforms (e.g., Google, Microsoft 365, Apple, LinkedIn) that manage identity information and provide authentication services. By integrating an IDP, your application:

* **Offloads Security Risks:** You don't store passwords, reducing the risk of credential theft via brute-force or stuffing attacks.
* **Streamlines UX:** Users can log in with accounts they already own and trust.
* **Accesses External Resources:** Your app can gain permission to interact with a user's files, calendars, or social feeds.

---
## The Authorization Code Flow: Step-by-Step

The **Authorization Code Flow** is the most secure and common variant of OAuth 2.0 used in modern web and mobile applications.

### 1. Initiation

The user clicks the "Login with [Provider]" button in your application. This signals the start of the authentication handshake.

### 2. Redirection to IDP

Your application redirects the user’s browser to the Identity Provider’s authorization server. During this redirect, your app sends:

* **Client ID:** A public identifier for your app.
* **Scopes:** The specific permissions you are requesting (e.g., `read:user`, `calendar.events`).
* **Redirect URI:** The specific URL in your app where the user should be sent after authentication.

### 3. Authentication & Consent
The user logs into the IDP (if not already logged in). The IDP then displays a **Consent Screen**, detailing exactly what data your application is requesting access to.
### 4. User Approval
The user reviews the permissions and chooses to grant or deny the request.
### 5. Authorization Code Issuance
If the user grants permission, the IDP redirects the user back to your application’s **Redirect URI**. Included in the URL is a temporary **Authorization Code** (Grant Code).

> **Note:** The IDP will only send this code to a Redirect URI that you have pre-registered and "whitelisted" in their developer console to prevent hijacking.

### 6. Token Exchange
Your application receives the code and immediately sends it back to the IDP’s authorization server from your backend (server-to-server). In exchange for this code, the IDP issues:
* **Access Token:** A short-lived credential used to access the user's data.
* **Refresh Token:** A long-lived credential used to obtain new access tokens once the current one expires, without bothering the user to log in again.
### 7. Resource Access
Your application uses the **Access Token** to make requests to the Provider’s **Resource Server**. You can now fetch profile pictures, read emails, or perform other permitted actions on the user's behalf.

---
## Security Best Practices: The `state` Parameter
During the initial redirect (Step 2), your application should generate and send a unique, random string called a **state parameter** (or CSRF token).

* **The Attack:** In a Cross-Site Request Forgery (CSRF) attack, an attacker might try to inject their own authorization code into a victim's session.
* **The Defense:** The IDP returns this exact `state` string in Step 5. Your application must verify that the returned `state` matches the one it originally sent. If they don't match, the request is forged and should be rejected.

---
## Summary Comparison: Custom JWT vs. OAuth

| Feature              | Custom JWT (Self-Managed)                   | OAuth 2.0 (External IDP)                        |
| -------------------- | ------------------------------------------- | ----------------------------------------------- |
| **Password Storage** | You must hash, salt, and secure passwords.  | No password storage required.                   |
| **Complexity**       | High (must build registration, reset, MFA). | Moderate (must implement the OAuth handshake).  |
| **Trust**            | Users must trust your specific security.    | Users trust established brands (Google, Apple). |
| **Third-party Data** | No access to external resources.            | Can access calendars, files, and social data.   |
![[Pasted image 20260126015446.png]]
#### OAuth Authentication with GitHub
The first step to setting up the OAuth authentication is to create a set of client ID and secret credentials within GitHub so that their systems can identify your application.

You can generate a client ID and secret from GitHub by visiting the developer settings under your GitHub profile and creating an OAuth application

With your new application client ID and secret, you can now redirect users to the GitHub authorization server from your application

```python
from typing import Annotated
from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from authentication.schemas import TokenOut, UserOut, UserCreate
from authentication.services.auth import AuthService
from database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
import secrets
from fastapi.responses import RedirectResponse
from fastapi import APIRouter,Request,status

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_auth_service(db: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(db)

@router.post("/register", response_model=UserOut)
async def register_user(
    new_user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserOut:
    user = await auth_service.register_user(new_user)
    return user

@router.post("/token", response_model=TokenOut)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenOut:
    token = await auth_service.authenticate_user(form_data)
    return TokenOut(
        access_token=token,
        token_type="bearer"
    )

@router.post("/logout")
async def logout_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    await auth_service.logout(credentials)
    return {"message": "Logged out successfully"}

@router.post("/reset-password")
async def reset_password(
    username: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    await auth_service.reset_password(username, new_password)
    return {
        "message": "Password has been reset successfully."
    }

client_id = "your_client_id"
client_secret = "your_client_secret"

@router.get("/oauth/github/login",status_code = status.HTTP_301_REDIRECT)
def oauth_github_login(request:Request) -> RedirectResponse:
    state = secrets.token_urlsafe(16)
    redirect_uri = request.url_for("oauth_github_callback")

    response = RedirectResponse(
        url=f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id}"
        f"&scope=user"
        f"&state={state}"
        f"&redirect_uri={redirect_uri}"
    )

    csrf_token = secrets.token_urlsafe(16)
    request.session["x-csrf-state-token"] = csrf_token
    return response
```

Redirect user to the GitHub authorization server to log into their account while supplying your application credentials, a requested scope, and a CSRF state value to prevent against CSRF attacks

Adding a GitHub login button to the Streamlit client-side application
client.py
```python
import requests 
import streamlit as st 

if st.button("Login with GitHub"): 
	response = requests.get("http://localhost:8000/auth/oauth/github/login") 
	if not response.ok: 
		st.error("Failed to login with GitHub. Please try again later") 
		response.raise_for_status()
```

- You now have implemented the redirect flow that starts the OAuth authentication process with GitHub as the identity provider
- When users log into their GitHub account, GitHub will show them a consent screen
- If the user accepts the consent, GitHub will redirect the user back to your application with a grant code and a state. You should check whether the state matches the previously generated state.
- Once you have the grant code, you can send this to the GitHub authorization to exchange it for an access token

Exchanging grant code with an access token while protecting against CSRF attacks
dependencies/auth.py
```python
from typing import Annotated
import aiohttp
from fastapi import Depends,HTTPException,status
from loguru import logger

client_id = "your_client_id"
client_secret = "your_client_secret"

async def exchange_grant_with_access_token(code:str) -> str:
    try:
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://github.com/login/oauth/access_token",
                json = body, headers = headers
            ) as response:
                access_token_data = await response.json()
    except Exception as e:
        logger.warning(f"Error exchanging code for access token: {e}")

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Failed to fetch access token"
        )
    
    if not access_token_data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid access token response"
        )
    
    return access_token_data.get("access_token","")

ExchangeCodeTokenDep = Annotated[str,Depends(exchange_grant_with_access_token)]
```

You can now add a new endpoint that accepts requests from the GitHub authorization server. This callback endpoint should have a CSRF protection to guard against third parties impersonating the authorization server. If the request from GitHub is forged, the state parameter provided and the one stored in the request session won’t match.

CROSS-SITE REQUEST FORGERY
CSRF is a type of security vulnerability that allows an attacker to trick a user into performing actions on a web application where they are authenticated. This can lead to unauthorized actions being executed without the user’s consent. 

In CSRF, the attacker creates a malicious request that exploits the user’s authenticated session with a target website. These attacks can result in unauthorized transactions, data theft, or changes to user settings without their consent and knowledge. 

In the context of OAuth2, an attacker can exploit vulnerabilities such as open redirect to intercept the initial authorization requests and modify them to redirect to their own malicious site after authentication. 

Attackers can also create a replica of your application frontend and trick users into logging into their accounts. If the user logs into their GitHub account via the phishing site, the attacker can provide a redirect URL pointing to their own servers to get an authorization grant code. They can then exchange the authorization code for an access token.
![[Pasted image 20260126021538.png]]

Implement callback endpoint to get access token while protecting against CSRF attacks
routes/auth.py
```python
from fastapi.responses import RedirectResponse
from fastapi import APIRouter,Request,status
from dependencies.auth import ExchangeCodeTokenDep
from fastapi import Depends, HTTPException, Request

def check_csrf_state(request:Request,state:str) -> None:
    if state != request.session.get("x-csrf-token"):
        raise HTTPException(detail = "Bad Reqeuets",status_code = status.HTTP_401_UNAUTHORIZED)

@router.get("/oauth/github/callback",dependencies=[Depends(check_csrf_state)])
async def oauth_github_callback(access_token: ExchangeCodeTokenDep) -> RedirectResponse:
    response = RedirectResponse(url=f"http://localhost:8501")
    response.set_cookie(key="access_token",value=access_token,httponly=True)
    return response
```

you are using the request session for CSRF protection, but this won’t work without adding the Starlette’s SessionMiddlware first to maintain a secure user session that’s only mutable on the server side

Add a session middleware to manage session state for protecting against CSRF attacks
main.py
```python
from fastapi import FastAPI 
from starlette.middleware.sessions import SessionMiddleware

...

app = FastAPI(lifespan = lifespan)
app.add_middleware(SessionMiddleware,secret_key = "your_secret_key")
```

In this case, the requester is the GitHub authorization server sending you a grant code . Once you receive the grant code , you then exchange it with the GitHub authorization server for an access token
Finally, you can use the access token you received from the authorization server to fetch user information such as their name, email, and profile image to register their identity in your application

Use access token to get user information from GitHub resource servers 
routes/auth.py
```python
import secrets
from fastapi.responses import RedirectResponse
from fastapi import APIRouter,Request,status
from dependencies.auth import ExchangeCodeTokenDep
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer 

security = HTTPBearer()
HTTPBearerDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

async def get_user_info(credentials:HTTPBearerDep) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {credentials.credentials}"}

            async with session.get("https://api.github.com/user", headers=headers) as resp:
                return await resp.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
GetUserInfoDep = Annotated[dict, Depends(get_user_info)]

@router.get("/oauth/github/callback")
async def get_current_user(user_info: GetUserInfoDep) -> dict:
    return user_info
```

Congratulations! You should now have a working authentication system that leverages OAuth2 to authenticate users.

----
#### OAuth2 Flow Types
#### Understanding Authorization

While **Authentication** verifies *who* an actor is, **Authorization** determines *what* that actor is allowed to do. It is the process of enforcing permissions and ensuring that the right people have access to the right resources.

## The Authorization Function

At its core, authorization acts like a mathematical function. It takes three specific inputs and produces a binary (Yes/No) output:

* **Actor:** The user or service attempting the request.
* **Action:** What they want to do (e.g., Read, Write, Delete, Execute).
* **Resource:** The specific object being targeted (e.g., a Database record, a GenAI model, a file).

---
## Authorization Models
As applications grow, hard-coding `if/else` statements becomes unmanageable. To handle complexity, developers use established **Authorization Models**.

### 1. Role-Based Access Control (RBAC)

Access is granted based on predefined roles. Permissions are assigned to roles, and roles are assigned to users.

* *Example:* An **Admin** role can access all GenAI models, while a **Viewer** role can only see logs.

### 2. Relationship-Based Access Control (ReBAC)

Access is determined by the connections between entities. It focuses on "ownership" or "membership."

* *Example:* If a user is part of **Team Alpha**, they can access the premium models purchased by that team.

### 3. Attribute-Based Access Control (ABAC)

The most granular model. It looks at specific characteristics (attributes) of the user, the resource, and even the environment (like time of day or IP address).

* *Example:* A resource marked as `public` can be viewed by anyone, but a `premium` model can only be accessed by users with a `status: paid` attribute.

---
## Comparison of Authorization Methods

| Type | Benefits | Limitations | Use Cases |
| --- | --- | --- | --- |
| **RBAC** | Simplifies management; Easy to audit. | Limited flexibility; "Role explosion" in complex systems. | Enterprise apps, Financial systems, Healthcare. |
| **ReBAC** | Provides fine-grained control over shared resources. | Requires complex relationship data and evaluation. | Social networks, SaaS (teams/orgs), Project management. |
| **ABAC** | Highly flexible; Supports dynamic/contextual rules. | High complexity; Harder to predict outcomes at scale. | Cloud services, IoT, Regulatory compliance. |

---
## Enforcement
Once the authorization function returns a decision, the system must enforce it:
* **Allow:** The request proceeds to the resource.
* **Deny:** The system returns a `403 Forbidden` response, hides the UI elements, or redirects the user to a "Request Access" page.

![[Pasted image 20260126182655.png]]

#### Role Based Access Control
## Role-Based Access Control (RBAC)

Role-Based Access Control (RBAC) is a widely adopted model for implementing authorization. Its popularity stems from its **simplicity** and the intuitive way it maps user identities to application functionality.

---
### Core Concepts

The RBAC model operates on a hierarchy that connects users to the actions they are permitted to perform:

- **Permissions:** Specific actions a user can take on resources (e.g., "Use Paid LLM Model").
- **Roles:** Groups of permissions that correspond to a user's job function or organizational status.
- **Users:** Individuals assigned one or more roles to gain the necessary access.
### Benefits of Using Roles

- **Organizational Alignment:** Roles often mirror your organization’s actual hierarchy, making them easy to conceptualize.
- **Reduced Decision Fatigue:** Instead of manually assigning dozens of individual permissions to every new user, administrators can assign a few **predefined roles**.
- **Improved UX:** Preset permissions streamline the administrative process and ensure a consistent experience for the end user.
---
### Common Implementation: User vs. Administrator

Most commercial services start with two primary roles to distinguish between standard access and system management:

|**Feature**|**User (Member)**|**Administrator**|
|---|---|---|
|**Core Functionality**|Access to GenAI models, read/write own resources.|Full access to all resources and mutation rights.|
|**User Management**|None.|Assign/remove roles, enable/disable accounts.|
|**Data Privacy**|Cannot view other users' data.|Can view data across the entire platform.|
|**Early Access**|Standard features only.|Access to beta features or restricted GenAI models.|
dependencies/auth.py
```python
from typing import Annotated
import aiohttp
from fastapi import Depends,HTTPException,status
from loguru import logger

client_id = "your_client_id"
client_secret = "your_client_secret"

async def exchange_grant_with_access_token(code:str) -> str:
    try:
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://github.com/login/oauth/access_token",
                json = body, headers = headers
            ) as response:
                access_token_data = await response.json()
    except Exception as e:
        logger.warning(f"Error exchanging code for access token: {e}")

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Failed to fetch access token"
        )
    
    if not access_token_data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid access token response"
        )
    
    return access_token_data.get("access_token","")

ExchangeCodeTokenDep = Annotated[str,Depends(exchange_grant_with_access_token)]

from authentication.entities import User
from fastapi import Depends,HTTPException,status
from authentication.services.auth import AuthService

async def is_admin(user:User = Depends(AuthService.get_current_user)) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action"
        )
    return user
```

routers/resource.py
```python
from dependencies.auth import is_admin
from fastapi import APIRouter, Depends
from authentication.services.auth import AuthService

router = APIRouter(
    dependencies=[Depends(AuthService.get_current_user)],
    prefix="/generate",
    tags=["Resource"],
)

@router.post("/image",dependencies=[Depends(is_admin)])
async def generate_image():
    ...
    return {"message": "Image generated successfully."}

@router.post("/text")
async def generate_text():
    ...
    return {"message": "Text generated successfully."}
```

1. Implement the is_admin authorization dependency guard on top of the AuthService.get_current_user dependency. Mark the function as async since the child dependency is performing an async operation against the database.
2. Use the authorization guard dependency to deny access to the image generation service for nonadmin authenticated users.
3. Nonadmin authenticated users can still access other resource controllers since the router is secured by an authentication guard dependency.

![[Pasted image 20260126183923.png]]

Implementing complex RBAC authorization using abstract dependencies
![[Pasted image 20260126185220.png]]

dependencies/auth.py
```python
from typing import Annotated
import aiohttp
from fastapi import Depends,HTTPException,status
from loguru import logger

client_id = "your_client_id"
client_secret = "your_client_secret"

async def exchange_grant_with_access_token(code:str) -> str:
    try:
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://github.com/login/oauth/access_token",
                json = body, headers = headers
            ) as response:
                access_token_data = await response.json()
    except Exception as e:
        logger.warning(f"Error exchanging code for access token: {e}")

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Failed to fetch access token"
        )
    
    if not access_token_data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid access token response"
        )
    
    return access_token_data.get("access_token","")

ExchangeCodeTokenDep = Annotated[str,Depends(exchange_grant_with_access_token)]

from authentication.entities import User
from fastapi import Depends,HTTPException,status
from authentication.services.auth import AuthService

async def is_admin(user:User = Depends(AuthService.get_current_user)) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action"
        )
    return user

CurrentUserDep = Annotated[User,Depends(AuthService.get_current_user)]

async def has_role(user:CurrentUserDep,roles:list[str]):
    if user.role not in roles:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action"
        )
    return user
```

routes/resource.py
```python
from dependencies.auth import is_admin,has_role
from fastapi import APIRouter, Depends
from authentication.services.auth import AuthService

router = APIRouter(
    dependencies=[Depends(AuthService.get_current_user)],
    prefix="/generate",
    tags=["Resource"],
)

@router.post("/image",dependencies=[Depends(is_admin)])
async def generate_image():
    ...
    return {"message": "Image generated successfully."}

@router.post("/text")
async def generate_text():
    ...
    return {"message": "Text generated successfully."}

@router.post("/image",dependencies=[Depends(lambda user: has_role(user, ["ADMIN","MODERATOR"]))])
async def generate_image():
    ...
    return {"message": "Image generated successfully for ADMIN or MODERATOR."}

@router.post("/text",dependencies=[Depends(lambda user: has_role(user, ["EDITOR"]))])
async def generate_text():
    ...
    return {"message": "Text generated successfully for EDITOR."}
```

##### Relationship Based Access Control
**Relationship-Based Access Control (ReBAC)** serves as an extension of the traditional RBAC model. While RBAC focuses on what a user _is_, ReBAC focuses on the **relationships** between users and specific resources.

---
### Key Characteristics

- **Resource-Level Granularity:** Instead of global roles, permissions are defined at the resource level. You must define what a role can do for every specific resource type (e.g., conversations, teams, or documents).
    
- **Graph-Based Logic:** ReBAC is often visualized as a **graph**.
    - **Nodes:** Represent resources or identities.
    - **Edges:** Represent the relationships (permissions) between them.
        
- **Hierarchical Inheritance:** This model supports nested structures. Permissions can flow from a parent resource to its "children," significantly reducing manual overhead.

---
### RBAC vs. ReBAC: A Practical Example
To illustrate the difference, consider how a **Moderator** role might be treated in each system:

|**Feature**|**Role-Based (RBAC)**|**Relationship-Based (ReBAC)**|
|---|---|---|
|**Scope**|Broad access across the entire app.|Granular access per resource type.|
|**Conversation Access**|Can moderate everything.|Can **Read** and **Delete** conversations.|
|**Team Access**|Can moderate everything.|Restricted to **Read-Only** for team data.|
|**Implementation**|"User is a Moderator."|"User has X relationship to Resource Y."|

---
### The Power of Inheritance

ReBAC is particularly efficient for managing bulk permissions through grouping. Instead of sharing private LLM conversations individually, you can:

1. **Group** conversations into a **Folder** or **Team**.
2. Assign permissions to that parent entity.
3. Allow the **children instances** (the conversations) to automatically inherit the parent's permissions.

> **Note:** This "set once, apply to many" approach saves significant administrative time and prevents errors when managing complex data structures.

![[Pasted image 20260126190927.png]]

>[!tip]
>If you decide to adopt the ReBAC model, I recommend visualy mapping out the relationships between resources and identities in your application. 

A big problem that ReBAC solves by extending RBAC is the explosion of roles within the RBAC model by combining relationships with roles. It is ideal for managing permissions in complex hierarchical structures and allows for reverse queries, enabling efficient permission definitions using teams and groups. 

However, ReBAC can be complex to implement and maintain, resource-intensive, difficult to audit, and not as fine-grained as ABAC for dynamic permissions based on attributes like time or location.

---
#### Attribute Base Access Control
**Attribute-Based Access Control (ABAC)** is a highly flexible authorization model that expands upon basic RBAC. It determines access by evaluating specific **attributes** (characteristics) of the user, the resource, and the environment against a set of rules.

---
### How ABAC Works

Unlike roles, which are static, ABAC uses conditional logic to implement granular policies.
- **User Attributes:** Role, department, subscription status (e.g., "Paid").
- **Resource Attributes:** Sensitivity level, owner, file type, or content metadata (e.g., `has_pii=true`).
- **Environmental Attributes:** Time of day, IP address, or geographic location.
---
### Real-World Examples

- **Data Protection:** A policy can prevent users from uploading documents to a RAG (Retrieval-Augmented Generation) service if the document contains personally identifiable information (i.e., `upload.has_pii = true`).

- **Monetization:** In SaaS applications like ChatGPT, access to premium GenAI models is granted only if the user's `account_type` attribute equals "Paid."

---
### Advantages vs. Challenges

|**Pros**|**Cons**|
|---|---|
|**Fine-Grained Control:** Virtually infinite freedom to create specific, complex policies.|**Complex Auditing:** It is difficult to determine exactly _who_ has access to a resource without evaluating attributes for every single user.|
|**Dynamic Logic:** Can react to real-time data like user location or document content.|**Management Overhead:** Can become cumbersome in large applications with thousands of attributes and roles.|
|**Scalability of Rules:** A single rule can apply to many users if they share the same attribute.|**Implementation Difficulty:** Harder to implement than RBAC, though generally less structurally complex than ReBAC.|

---
### Comparison at a Glance

- **RBAC:** "You can do this because you are a **Manager**."
- **ABAC:** "You can do this because you are a **Manager** in the **HR Department** accessing **Internal Data** during **Business Hours**."

![[Pasted image 20260126191253.png]]

---
#### Hybrid Authorization Models 
If you’ve worked with larger applications in the past, you will notice that they combine features of the RBAC, ReBAC, and ABAC authorization models. For instance, administrators may have access to any resource and user management/authentication features (RBAC), and users can share their private resources by setting visibility attribute to public (ABAC) and can add members to their team for collaborating on private resources. 

A hybrid approach combining RBAC, ReBAC, and ABAC models may give you the strengths of all the authorization models: 
- RBAC simplifies permission management by assigning roles to users, making it easy to manage and audit. 
- ReBAC is perfect for managing hierarchical relationships and reverse queries, making it suitable for complex hierarchical structures. 
- ABAC provides fine-grained control based on user and resource attributes, allowing for dynamic and context-aware permissions.
![[Pasted image 20260126192555.png]]

Implementing the hybrid authorization model combining RBAC, ReBAC, and ABAC
dependencies/auth.py
```python

from typing import Annotated
from fastapi import Depends, HTTPException, status

async def has_role(user:CurrentUserDep,roles:list[str]):
    if user.role not in roles:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed to perform this action"
        )
    return user

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]
TeamMembershipRep = Annotated[Team, Depends(TeamService.get_current_team)]
ResourceDep = Annotated[Resource, Depends(ResourceService.get_resource)] 

def authorize(user: CurrentUserDep, resource: ResourceDep, team: TeamMembershipRep) -> bool: 
    if user.role == "ADMIN": 
        return True 
    if user.id in team.members: 
        return True 
    if resource.is_public: 
        return True 
    raise HTTPException( 
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Access Denied") 
```

routes/resource.py
```python
from dependencies.auth import authorize
from fastapi import APIRouter, Depends 
 
router = APIRouter( 
    dependencies=[Depends(authorize)], prefix="/generate", tags=["Resource"]
) 
 
@router.post("/image")
async def generate_image(): ... 
 
@router.post("/text")
async def generate_text(): ...
```

As you define rules and permissions based on each authorization model, you also may decide to bypass rules if certain conditions are met. This can lead to complex logic and create a maintenance burden on your application code. 

Since implementing a hybrid model can be complex, you may consider developing a separate authorization service to eliminate the need for significant code changes with volatile permissions that change frequently. Using an external system for authorization decisions allows your application’s authorization logic to remain consistent
![[Pasted image 20260126193059.png]]

Using an authorization service with the GenAI service
authorization_api.py
```python
from typing import Annotated, Literal
from fastapi import Depends, FastAPI
from pydantic import BaseModel 

... #import services and entities here

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]
ActionRep = Annotated[Literal["READ", "CREATE", "UPDATE", "DELETE"], str]
ResourceDep = Annotated[Resource, Depends(ResourceService.get_resource)] 

class AuthorizationResponse(BaseModel):
    allowed:bool 

app = FastAPI()

@app.get("/authorize")
def authorization_controller( 
    user: CurrentUserDep, resource: ResourceDep, action: ActionRep
) -> AuthorizationResponse: 
    if user.role == "ADMIN": 
        return AuthorizationResponse(allowed=True) 
    if action in user.permissions.get(resource.id, []): 
        return AuthorizationResponse(allowed=True) 
    ...  # Other permission checks 
    return AuthorizationResponse(allowed=False) 
```

 genai_api.py (GenAI Service) 
 ```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel 
 
class AuthorizationData(BaseModel): 
    user_id: int 
    resource_id: int 
    action: str 
 
authorization_client = ...  # Create authorization client 
 
async def enforce(data: AuthorizationData) -> bool: 
    response = await authorization_client.decide(data) 
    if response.allowed: 
        return True 
    raise HTTPException( 
        status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied" 
    ) 
 
router = APIRouter( 
    dependencies=[Depends(enforce)], prefix="/generate", tags=["Resource"]
) 
 
@router.post("/text")
async def generate_text_controller(): 
    ...
```
