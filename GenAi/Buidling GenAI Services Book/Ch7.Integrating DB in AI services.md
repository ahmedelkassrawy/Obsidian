---
description: "Ch7 notes on wiring a database into a FastAPI AI service: SQLAlchemy ORM models, the engine as a connection pool, session dependency injection, and Alembic migrations."
domain: ai-eng
type: book
status: digested
tags:
  - domain/ai-eng
  - type/book
  - status/digested
  - topic/sqlalchemy
  - topic/postgres
  - topic/fastapi
aliases:
  - "ORM models"
  - "Alembic"
  - "async sessions"
hubs:
  - "[[SQLAlchemy]]"
  - "[[Postgres]]"
  - "[[FastAPI]]"
---

## What this chapter covers

- Defining database tables as Python classes with the SQLAlchemy ORM.
- Creating an async engine and a per-request database session in FastAPI.
- Building CRUD endpoints for a `conversations` table.
- Refactoring that code into the repository and service patterns.
- Versioning schema changes with Alembic.
- Saving LLM output that was streamed to the user.

> [!note] Code in this note
> The book targets 2024-era libraries. I checked every block against the current docs (SQLAlchemy 2.1, FastAPI 0.142, Alembic 1.20, Pydantic 2.13, openai-python 3.x) and flagged each change with ⚠️. Details are in the Verification note at the end.

---

## Object relational mappers (ORMs)

> [!definition] ORM (object relational mapper)
> A library that lets you work with a database through normal Python classes, so you don't have to write raw SQL yourself. Tables become classes, columns become class attributes, and rows become class instances.

So instead of writing `SELECT * FROM users WHERE id = 1`, you ask the ORM for the `User` whose `id` is 1, and it writes the SQL for you.

| Pros | Cons |
|---|---|
| Hides the details of talking to the database | You trade some flexibility for convenience |
| Speeds up development | Learning curve |
| Easier to maintain | Complex queries can be slower than hand-written SQL |
| Many libraries to choose from (SQLAlchemy, SQLModel, TortoiseORM, Django ORM) | Debugging can be harder |

For most projects the pros win, so it's worth learning one well. This chapter uses **SQLAlchemy** with a Postgres database.

> [!tip] Refresher
> For the basics of SQLAlchemy queries and relationships, see [[SQLAlchemy CRUD And Relationships Recap]].

---

## Defining ORM models

The first step is to describe your tables as SQLAlchemy classes. There are two for now: `conversations` and `messages`. (The `users` table comes in the next chapter, with authentication.)

### Example 7-2: Defining the ORM models

```python
# entities.py
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    model_type: Mapped[str] = mapped_column(index=True)
    # ⚠️ book had default=datetime.now(UTC). That calls now() ONCE, when the module is
    # imported, so every row would get the same timestamp. The SQLAlchemy docs show
    # server_default=func.now() (the database fills it in) and func.now() for onupdate.
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    prompt_content: Mapped[str] = mapped_column()
    response_content: Mapped[str] = mapped_column()
    prompt_tokens: Mapped[int | None] = mapped_column()
    response_tokens: Mapped[int | None] = mapped_column()
    total_tokens: Mapped[int | None] = mapped_column()
    is_success: Mapped[bool | None] = mapped_column()
    status_code: Mapped[int | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())  # ⚠️ same fix
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()  # ⚠️ same fix
    )

    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )
```

- `DeclarativeBase` is the parent class that every model inherits from. SQLAlchemy uses it to collect all your tables.
- `mapped_column()` reads the column type from the `Mapped[...]` type hint, so `Mapped[str]` becomes a text column.
- `index=True` on `model_type` makes filtering conversations by model faster.
- `cascade="all, delete-orphan"` means that when you delete a conversation, its messages get deleted too.
- `Mapped[int | None]` makes a column optional, so it allows `NULL` (the same as `nullable=True`).
- The `messages` table stores both the prompt and the LLM's response, plus token usage, status code, and whether the call succeeded.

> [!warning] Timestamp defaults
> Pass a function or a SQL expression to `default`, never the result of calling one. If you want the timestamp made in Python instead of by the database, use `default=lambda: datetime.now(UTC)`. That runs on every insert.

Once the models exist, you need a connection to the database to create the tables. That takes an **engine** and some **session management**.

---

## Creating the database engine and session management

> [!definition] Engine
> The object that holds your database connection string and manages a **pool** of open connections that your app reuses.

You need the database driver and SQLAlchemy's async extras first:

```bash
# ⚠️ book printed `pip install alembic sqlalchemy psycopg3`. The psycopg 3 package is
# called "psycopg", and since SQLAlchemy 2.1 the async support (greenlet) is an extra.
pip install alembic "sqlalchemy[asyncio]" "psycopg[binary]"
```

### Example 7-3: Creating the engine and tables

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine
from entities import Base

database_url = (
    "postgresql+psycopg://fastapi:mysecretpassword@localhost:5432/backend_db"
)

engine = create_async_engine(database_url, echo=True)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
```

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, init_db

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    # other startup operations within the lifespan
    ...
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

- The connection string follows the template `<driver>://<username>:<password>@<host>/<database>`.
- `postgresql+psycopg` picks the psycopg 3 driver. With `create_async_engine` it automatically uses psycopg's async mode. (`postgresql+asyncpg://...` is the other common async driver.)
- `echo=True` logs every SQL statement, which helps while debugging.
- `init_db()` drops any existing tables and then creates them all from your models.
- Code after `yield` in the `lifespan` runs on server shutdown, so `engine.dispose()` closes the connection pool cleanly.

> [!warning] `create_all()` is for prototyping only
> `create_all()` can create tables but can't change existing ones. Combined with `drop_all()`, this wipes your data on every start. In production, use a migration tool like Alembic (covered below).

> [!warning] Don't hard-code secrets
> The connection string is hard-coded here only to keep the example short. In real projects, load it from environment files or a secret manager, for example with Pydantic Settings.

### Sessions

> [!definition] Session
> A short-lived workspace for talking to the database. You load and change objects through it, then commit or roll back the changes as one transaction.

> [!definition] Session factory
> A function that hands out new sessions on demand. It's a design pattern for opening, using, and closing database connections across your services.

Since every request needs a session, FastAPI's dependency injection is a good fit. It creates one session per request and reuses it for everything that request needs.

### Example 7-4: A database session dependency

```python
# database.py
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
# engine is defined above in this same file (Example 7-3)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    # ⚠️ book also passed autocommit=False. In SQLAlchemy 2.x that keyword only exists
    # for backwards compatibility and must stay False, so it's dropped here.
    autoflush=False,
    # ⚠️ not in the book. The SQLAlchemy asyncio docs recommend it: without it, reading
    # an attribute after commit triggers a hidden database call, which fails under async.
    expire_on_commit=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
```

1. `async_sessionmaker` is the session factory, bound to the engine. `autoflush=False` stops SQLAlchemy from sending pending changes to the database on its own, which gives you more control over when writes happen.
2. `get_db_session` is the dependency. Because it uses `yield` inside `async with`, FastAPI treats it like an async context manager.
3. `async with async_session()` opens a session and handles its lifecycle.
4. `yield session` hands the session to the route.
5. If anything goes wrong, the transaction is rolled back and the error is re-raised.
6. In every case, the session is closed at the end to free its resources.
7. `DBSessionDep` is an `Annotated` type you can reuse in any route.

> [!warning] When the code after `yield` runs
> Since FastAPI 0.118, the code after `yield` runs **after the response has been sent**. So the `commit()` in this dependency happens after the client already got a success response. The routes below commit explicitly, so this is just a safety net. If you need cleanup to finish before the response goes out, FastAPI 0.121+ lets you write `Depends(get_db_session, scope="function")`.

---

## Implementing CRUD endpoints

FastAPI uses Pydantic to validate data coming in and going out. So before writing endpoints, you map your database entities to Pydantic models.

Keeping the two separate means your API shape and your database shape can change independently.

### Example 7-5: Pydantic schemas for conversations

```python
# schemas.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ConversationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    model_type: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

class ConversationOut(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

- `from_attributes=True` lets Pydantic read values from object attributes, like a SQLAlchemy model, instead of only from dicts.
- Separate models for create, update, and output let each use case have its own fields.

> [!tip] What about the duplication?
> Writing both SQLAlchemy and Pydantic models can feel repetitive. The `sqlmodel` package merges them into one class. The book's view: it's less flexible for advanced SQLAlchemy use, so for complex apps keep the two separate.

### Use dependencies to cut database round-trips

The get, update, and delete endpoints all need to check that the record exists first. Put that check in one dependency and reuse it.

> [!note]
> FastAPI caches a dependency's result **within one request** only, not across requests.

### Example 7-6: CRUD endpoints for the conversations table

```python
# main.py
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from database import DBSessionDep
from entities import Conversation
from schemas import ConversationCreate, ConversationOut, ConversationUpdate

...  # lifespan and app = FastAPI(lifespan=lifespan) from Example 7-3

async def get_conversation(
    conversation_id: int, session: DBSessionDep
) -> Conversation:
    async with session.begin():
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation

GetConversationDep = Annotated[Conversation, Depends(get_conversation)]

@app.get("/conversations")
async def list_conversations_controller(
    session: DBSessionDep, skip: int = 0, take: int = 100
) -> list[ConversationOut]:
    async with session.begin():
        result = await session.execute(
            select(Conversation).offset(skip).limit(take)
        )
    return [
        ConversationOut.model_validate(conversation)
        for conversation in result.scalars().all()
    ]

# ⚠️ book used "/conversations/{id}". The dependency's parameter is conversation_id,
# so FastAPI would look for it in the query string and return 422. The path
# parameter name has to match.
@app.get("/conversations/{conversation_id}")
async def get_conversation_controller(
    conversation: GetConversationDep,
) -> ConversationOut:
    return ConversationOut.model_validate(conversation)

@app.post("/conversations", status_code=status.HTTP_201_CREATED)
async def create_conversation_controller(
    conversation: ConversationCreate, session: DBSessionDep
) -> ConversationOut:
    new_conversation = Conversation(**conversation.model_dump())
    async with session.begin():
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
    return ConversationOut.model_validate(new_conversation)

@app.put("/conversations/{conversation_id}", status_code=status.HTTP_202_ACCEPTED)  # ⚠️ was {id}
async def update_conversation_controller(
    updated_conversation: ConversationUpdate,
    conversation: GetConversationDep,
    session: DBSessionDep,
) -> ConversationOut:
    for key, value in updated_conversation.model_dump().items():
        setattr(conversation, key, value)
    async with session.begin():
        await session.commit()
        await session.refresh(conversation)
    return ConversationOut.model_validate(conversation)

@app.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)  # ⚠️ was {id}
async def delete_conversation_controller(
    conversation: GetConversationDep, session: DBSessionDep
) -> None:
    async with session.begin():
        await session.delete(conversation)
        await session.commit()
```

- `get_conversation` is the shared dependency. It returns the record or raises a 404, and the get, update, and delete routes all reuse it.
- Each request opens a transaction with `async with session.begin()`.
- For lists, fetch only a page of records with `.offset(skip).limit(take)` instead of the whole table.
- `model_validate()` builds a Pydantic model from the SQLAlchemy object. It raises a `ValidationError` if the data doesn't pass validation.
- Create, update, and delete commit the transaction. Create and update then return the refreshed record. Delete returns nothing.

> [!tip] Paging needs an order
> Without an `ORDER BY`, Postgres doesn't promise any particular order, so pages can shift between calls. Add something like `.order_by(Conversation.id)` before `.offset()`.

The status codes to send on success:

| Operation | Status code |
|---|---|
| Retrieve | 200 OK |
| Create | 201 Created |
| Update | 202 Accepted |
| Delete | 204 No Content |

Notice how the dependency keeps each route short. You now have a resource-based REST API for the `conversations` table.

---

## Repository and services design pattern

> [!definition] Repository
> A class that sits between your business logic and the database layer (for example, the ORM). It holds the methods that do the CRUD operations, so your routes don't touch the database directly.

![[Pasted image 20260125023303.png]]

The goal is a more modular, maintainable, and testable codebase. To set this up, start with an abstract interface that every repository has to follow.

> [!note] Abstract and concrete classes
> An **abstract class** can't be instantiated on its own. It can declare methods without an implementation, which its subclasses must provide.
> A **concrete class** inherits an abstract class and implements every one of its abstract methods.

### Example 7-7: The abstract repository interface

```python
# repositories/interfaces.py
from abc import ABC, abstractmethod
from typing import Any

class Repository(ABC):
    @abstractmethod
    async def list(self) -> list[Any]:
        pass

    @abstractmethod
    async def get(self, uid: int) -> Any:
        pass

    @abstractmethod
    async def create(self, record: Any) -> Any:
        pass

    @abstractmethod
    async def update(self, uid: int, record: Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, uid: int) -> None:
        pass
```

This lists the CRUD methods every repository must have. If a subclass forgets one, Python refuses to create an instance of it and raises a `TypeError`.

### Example 7-8: The conversation repository

```python
# repositories/conversations.py
from entities import Conversation
from repositories.interfaces import Repository
from schemas import ConversationCreate, ConversationUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ConversationRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int, take: int) -> list[Conversation]:
        async with self.session.begin():
            result = await self.session.execute(
                select(Conversation).offset(skip).limit(take)
            )
        return [r for r in result.scalars().all()]

    async def get(self, conversation_id: int) -> Conversation | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
        return result.scalars().first()

    async def create(self, conversation: ConversationCreate) -> Conversation:
        new_conversation = Conversation(**conversation.model_dump())
        async with self.session.begin():
            self.session.add(new_conversation)
            await self.session.commit()
            await self.session.refresh(new_conversation)
        return new_conversation

    async def update(
        self, conversation_id: int, updated_conversation: ConversationUpdate
    ) -> Conversation | None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return None
        for key, value in updated_conversation.model_dump().items():
            setattr(conversation, key, value)
        async with self.session.begin():
            await self.session.commit()
            await self.session.refresh(conversation)
        return conversation

    async def delete(self, conversation_id: int) -> None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return
        async with self.session.begin():
            await self.session.delete(conversation)
            await self.session.commit()
```

- `ConversationRepository` inherits the interface and implements each method with the same signatures.
- All the database logic for conversations now lives in this one class, so routes can just call it.

### Example 7-9: Routes refactored to use the repository

```python
# routers/conversations.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from database import DBSessionDep
from entities import Conversation
from repositories.conversations import ConversationRepository
from schemas import ConversationCreate, ConversationOut, ConversationUpdate

router = APIRouter(prefix="/conversations")

async def get_conversation(
    conversation_id: int, session: DBSessionDep
) -> Conversation:
    conversation = await ConversationRepository(session).get(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation

GetConversationDep = Annotated[Conversation, Depends(get_conversation)]

@router.get("")
async def list_conversations_controller(
    session: DBSessionDep, skip: int = 0, take: int = 100
) -> list[ConversationOut]:
    conversations = await ConversationRepository(session).list(skip, take)
    return [ConversationOut.model_validate(c) for c in conversations]

@router.get("/{conversation_id}")  # ⚠️ was "/{id}" (must match the dependency's parameter)
async def get_conversation_controller(
    conversation: GetConversationDep,
) -> ConversationOut:
    return ConversationOut.model_validate(conversation)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_conversation_controller(
    conversation: ConversationCreate, session: DBSessionDep
) -> ConversationOut:
    new_conversation = await ConversationRepository(session).create(conversation)
    return ConversationOut.model_validate(new_conversation)

@router.put("/{conversation_id}", status_code=status.HTTP_202_ACCEPTED)  # ⚠️ was "/{id}"
async def update_conversation_controller(
    conversation: GetConversationDep,
    updated_conversation: ConversationUpdate,
    session: DBSessionDep,
) -> ConversationOut:
    updated_conversation = await ConversationRepository(session).update(
        conversation.id, updated_conversation
    )
    return ConversationOut.model_validate(updated_conversation)

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)  # ⚠️ was "/{id}"
async def delete_conversation_controller(
    conversation: GetConversationDep, session: DBSessionDep
) -> None:
    await ConversationRepository(session).delete(conversation.id)
```

```python
# main.py
from routers.conversations import router as conversations_router

app.include_router(conversations_router)
```

1. The conversation routes now live on their own `APIRouter`, which you plug into the app with `include_router`. That keeps the API modular.
2. Each route just calls the repository, so the controllers are much easier to read.

### The service pattern

> [!definition] Service
> A layer above the repository that holds **business logic**. Its operations often need more complex queries or a sequence of CRUD steps.

For example, a `ConversationService` can fetch the messages in a conversation. Because it extends `ConversationRepository`, it still has `list`, `get`, `create`, `update`, and `delete`.

You can then swap `ConversationRepository` for `ConversationService` in your routes, and use it for a new endpoint that lists a conversation's messages.

### Example 7-10: The conversation service

```python
# services/conversations.py
from entities import Message
from repositories.conversations import ConversationRepository
from sqlalchemy import select

class ConversationService(ConversationRepository):
    async def list_messages(self, conversation_id: int) -> list[Message]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        return [m for m in result.scalars().all()]
```

```python
# routers/conversations.py
from database import DBSessionDep
from fastapi import APIRouter
from schemas import MessageOut
from services.conversations import ConversationService

router = APIRouter(prefix="/conversations")

@router.get("/{conversation_id}/messages")
async def list_conversation_messages_controller(
    conversation: GetConversationDep,
    session: DBSessionDep,
) -> list[MessageOut]:  # ⚠️ book annotated list[Message]. FastAPI builds the response model
    # from this annotation and can't use a SQLAlchemy class, so it fails at startup.
    messages = await ConversationService(session).list_messages(conversation.id)
    return [MessageOut.model_validate(m) for m in messages]
```

The new endpoint lists the messages of one conversation by its ID. (`MessageOut` is a Pydantic schema for messages, built the same way as `ConversationOut`.)

> [!tip] Practice
> Now try writing CRUD endpoints for the `messages` table using the same two patterns.

### Keeping the layers clean

- **Loose coupling:** don't tie services to one specific repository implementation.
- **Focused services:** keep them about business logic, and don't pile unrelated jobs onto them.
- **Focused repositories:** data access only. No business logic.
- **Transactions and errors:** handle them carefully, especially when one action runs several related database operations that must succeed or fail together.
- **Query cost:** watch out for queries with many JOINs, and optimize where you can.
- **Conventions:** name methods and classes consistently, and don't hard-code configuration.

One more workflow piece is left: managing schema changes, especially when a team shares the same development and production databases.

---

## Managing database schema changes

Example 7-3 drops and recreates every table each time the server starts. That's fine while prototyping, but not once real users have data in there. You also need a way to roll back if something breaks.

> [!definition] Database migration tool
> A tool that version-controls your database schema the way Git version-controls your code. You can track every change, apply it, and revert it.

**Alembic** is the migration tool from the SQLAlchemy developers. It's very useful in teams with several environments, where you need to track changes and undo them when needed.

### Example 7-11: Initializing Alembic

```bash
pip install alembic
alembic init alembic   # ⚠️ book printed `alembic init` with no argument; the target directory is required

# If you only use an async driver such as asyncpg, start from the async template instead:
# alembic init -t async alembic
```

### Example 7-12: The Alembic environment in your project

```text
project/
    alembic.ini
    alembic/
        env.py              <- where you set the target schema and the database connection
        README
        script.py.mako
        versions/           <- migration files appear here
```

- `env.py` tells Alembic which models to compare against and how to connect.
- Each file in `versions/` holds the steps to upgrade or downgrade the schema by one revision.

### Example 7-13: Connecting Alembic to your SQLAlchemy models

```python
# alembic/env.py (top of the generated file, edited)
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from entities import Base
from settings import get_settings

from alembic import context

settings = get_settings()
db_url = settings.database_url
context.config.set_main_option("sqlalchemy.url", db_url)

# The Alembic Config object, which gives access to the values in alembic.ini
config = context.config

# Set up Python logging from the config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ⚠️ book had target_metadata = Base. Alembic needs the MetaData object.
target_metadata = Base.metadata

...  # rest of the generated env.py unchanged
```

- `set_main_option("sqlalchemy.url", ...)` puts your app's connection string into Alembic's config, so it isn't hard-coded in `alembic.ini`.
- `target_metadata = Base.metadata` gives Alembic your models' schema to compare against the real database.
- The default template uses a regular (sync) engine. That works with the `postgresql+psycopg` URL, because psycopg 3 has both sync and async modes. With asyncpg, use the async template from Example 7-11.

### Generating and running migrations

With Alembic connected to your models, it can write migration files for you by comparing the models with the database:

```bash
alembic revision --autogenerate -m "Initial Migration"
```

This creates a migration file under `alembic/versions/`. Open it and check it before you run it.

Then apply it:

```bash
alembic upgrade head
```

To undo the last migration:

```bash
alembic downgrade -1
```

Under the hood, Alembic generates the SQL to apply or revert each migration. It also creates an `alembic_version` table in the database to track which migrations already ran, so running `alembic upgrade head` again won't repeat them.

If your schema and migration history ever drift apart, you can delete the files in `versions/`, clear the `alembic_version` table, and set Alembic up again against the existing database.

> [!warning] Never edit a migration that already ran
> Commit each migration file to Git once you've applied it. Alembic checks its version table and skips migrations it has already run, so it won't notice edits to an old file. To change the schema again, create a new migration.

---

## Storing data when working with real-time streams

You can now build CRUD endpoints for both conversations and messages. One question is left: how do you save an LLM response that was **streamed** to the user?

You can't stream data into a regular relational database, because keeping a streaming write ACID-compliant is hard.

> [!definition] ACID
> The four guarantees of a reliable database transaction: **A**tomic (all or nothing), **C**onsistent, **I**solated (transactions don't interfere), and **D**urable (saved data survives crashes).

Instead, do a normal database write once the response has gone to the client. FastAPI's background tasks are made for exactly that.

### Example 7-15: Storing the content of an LLM output stream

```python
# main.py
from itertools import tee
from database import async_session
from entities import Message
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from repositories.messages import MessageRepository

# ⚠️ book passed the request's session into the background task. The FastAPI docs say
# not to reuse resources from a yield dependency in a background task; open a new
# session inside the task instead.
async def store_message(
    prompt_content: str, response_content: str, conversation_id: int
) -> None:
    async with async_session() as session:
        message = Message(
            conversation_id=conversation_id,
            prompt_content=prompt_content,
            response_content=response_content,
        )
        await MessageRepository(session).create(message)

@app.get("/text/generate/stream")
async def stream_llm_controller(
    prompt: str,
    background_tasks: BackgroundTasks,
    conversation: GetConversationDep,  # ⚠️ book: Conversation = Depends(get_conversation); same thing, Annotated style
) -> StreamingResponse:
    # Invoke LLM and obtain the response stream
    ...
    stream_1, stream_2 = tee(response_stream)
    background_tasks.add_task(
        store_message, prompt, "".join(stream_1), conversation.id  # ⚠️ see warning below
    )
    return StreamingResponse(stream_2)
```

1. `store_message` saves one prompt/response pair against a conversation.
2. The `GetConversationDep` dependency checks that the conversation exists and loads it.
3. `tee()` makes two copies of the LLM stream: one for the `StreamingResponse`, one for the background task.
4. The background task saves the message after the streaming response finishes.

> [!warning] `"".join(stream_1)` runs right away
> Arguments to `add_task` are evaluated when you call it, so `"".join(stream_1)` reads the whole LLM stream before the response even starts. The user waits for the full answer and loses the streaming effect. A fix is to wrap the stream in a generator that yields each chunk to the client, collects the chunks, and saves them once the stream ends.

The approach is the same whether you stream with SSE or WebSockets. Once the full response is streamed, a background task saves the message with the complete LLM output.

### Example 7-16: Using the LLM to title a conversation

You can use the same idea to name conversations. Send the first message to the LLM again and ask it for a short title. Then create the conversation record with that title.

```python
from entities import Conversation
from openai import AsyncClient
from repositories.conversations import ConversationRepository
from schemas import ConversationCreate
from sqlalchemy.ext.asyncio import AsyncSession

async_client = AsyncClient(...)

async def create_conversation(
    initial_prompt: str,
    model_type: str,  # ⚠️ added: the conversations table requires model_type
    session: AsyncSession,
) -> Conversation:
    completion = await async_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Suggest a title for the conversation "
                           "based on the user prompt",
            },
            {
                "role": "user",
                "content": initial_prompt,
            },
        ],
        # ⚠️ book used "gpt-3.5-turbo". OpenAI deprecated it (shutdown Oct 23, 2026);
        # the listed replacement is gpt-5.6-terra.
        model="gpt-5.6-terra",
    )
    title = completion.choices[0].message.content
    # ⚠️ book built a Conversation entity here, but ConversationRepository.create
    # (Example 7-8) expects a ConversationCreate schema and calls model_dump() on it.
    conversation = ConversationCreate(title=title, model_type=model_type)
    return await ConversationRepository(session).create(conversation)
```

- The system message asks for a title, and the user message is the first prompt.
- `completion.choices[0].message.content` is the generated title.
- The repository saves the new conversation and returns it.

> [!note]
> `AsyncClient` is still exported by the `openai` package as an alias of `AsyncOpenAI`, which is the name the docs use. The Chat Completions API is still supported, though OpenAI now leads with its Responses API.

SQLAlchemy plus Alembic is a tried and tested way to use relational databases with FastAPI, so you'll find plenty of resources for it. The ORM handles talking to the database, and Alembic controls how its schema changes.

---

## Summary

- An **ORM** maps tables to classes, so you work with Python objects instead of raw SQL.
- **SQLAlchemy models** use `DeclarativeBase`, `Mapped`, and `mapped_column`. Optional columns are `Mapped[X | None]`.
- The **engine** manages a connection pool. A **session dependency** with `yield` gives each request its own session.
- **Pydantic schemas** with `from_attributes=True` keep your API shape separate from your tables.
- A reusable **"get record or 404" dependency** keeps CRUD routes short.
- The **repository** pattern holds data access. The **service** pattern holds business logic on top.
- **Alembic** version-controls schema changes. Never edit a migration that already ran.
- Save **streamed LLM output** with a background task after the response is sent.

**Next chapter:** user management, authentication, and authorization, built on this database.

---

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[Ch3. Creating the Database Layer]]
- [[03 - Pydantic Schemas (Request and Response Models)]]
- [[SQLAlchemy CRUD And Relationships Recap]]
- [[01 - Engine and Connections]]
- [[05 - Sessions and sessionmaker]]
%% related:end %%
