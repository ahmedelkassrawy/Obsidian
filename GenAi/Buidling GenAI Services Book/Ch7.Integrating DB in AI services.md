An ORM library allows you to interact with a database and execute SQL operations without then need to write raw SQL yourself
Defining ORM Models The first step to query your database in Python is to define your ORM models with SQLAlchemy classes

#### Defining ORM Models
```python
from datetime import UTC,datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column()
    model_type: Mapped[str] = mapped_column(index = True)
    created_at: Mapped[datetime] = mapped_column(
        default = datetime.now(UTC), onupdate = datetime.now(UTC)
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message", 
        back_populates="conversation",
        cascade = "all, delete-orphan"
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key = True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id",
                   ondelete="CASCADE"), index = True
    )
    prompt_content: Mapped[str] = mapped_column()
    response_content: Mapped[str] = mapped_column()
    prompt_tokens: Mapped[int | None] = mapped_column()
    response_tokens: Mapped[int | None] = mapped_column()
    total_tokens: Mapped[int | None] = mapped_column()
    is_success: Mapped[bool | None] = mapped_column()
    status_code: Mapped[int | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default = datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default = datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    conversation: Mapped["Conversation"] = relationship(
        "Conversation", 
        back_populates="messages"
    )
```

Specify Mapped[int | None] to declare an optional typing so the column will allow NULL values (i.e., nullable=True )

Once you have your data models defined, you can create a connection to the database to create each table with the specified configurations. To achieve this, you will need to create a database engine and implement session management.

#### Creating Database Engine and Session Management
Once created, you can use the engine and the Base class to create tables for each of your data models

- With the engine created, you can now implement a factory function for creating sessions to the database. 
- Session factory is a design pattern that allows you to open, interact with, and close database connections across your services. 
- Since you may reuse a session, you can use FastAPI’s dependency injection system to cache and reuse sessions across each request runtime

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from entities import Base
from typing import Annotated
from fastapi import Depends

# Use environment variables
DATABASE_URL =  "postgresql+psycopg://fastapi:mysecretpassword@localhost:5432/backend_db"

# The engine is the connection pool
engine = create_async_engine(DATABASE_URL,echo=True)

# A factory for creating individual session objects
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit = False,
    autoflush=False,
    expire_on_commit=False, # Prevents errors when accessing attributes after commit
)

# Dependency Injection for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

db_session = Annotated[AsyncSession, Depends(get_db)]
```
1. Create an async database session factory bound to the database engine you created previously to asynchronously connect to your Postgres instance. Disable automatic committing of transactions with autocommit=false and automatic flushing of changes to the database with autoflush=False . Disabling both behaviors gives you more control, helps prevent unintended data updates, and allows you to implement more robust transaction management.
2. Define a dependency function to reuse and inject across your FastAPI app into route controller functions. Since the function uses the yield keyword within the async with , it is considered an async context manager. FastAPI will internally decorate the get_db_session as context manager when it is used as a dependency
3. Use the database session factory to create an async session. The context manager helps to manage the database session lifecycle such as opening, interacting with, and closing the database connections in each session. 
4. Yield the database session to the caller of the get_db_session function. 
5. If there are any exceptions, roll back the transaction and reraise the exception. 
6. In any case, close the database session at the end to release any resources that it holds. 
7. Declare an annotated database session dependency that can be reused across different controllers

#### Implementing CRUD Endpoints
- Before implementing CRUD endpoints, you’ll need to map database entities to Pydantic models. 
- This avoids tightly coupling your API schema with your database models to give you the freedom and flexibility in developing your API and databases independent of each other.

schemas.py
```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ConversationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title:str
    model_type:str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

class ConversationOut(ConversationBase):
    id:int
    created_at:datetime
    updated_at:datetime
```

Now that you have the SQLAlchemy and Pydantic models, you can start developing your CRUD API endpoints. When implementing CRUD endpoints, you should try to leverage FastAPI dependencies as much as you can to reduce database round-trips. For instance, when retrieving, updating, and deleting records, you need to check in with the database that a record exists using its ID. You can implement a record retrieval function to use a dependency across your get, update, and delete endpoints

#### CRUD Endpoints
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine
from entities import Base
from typing import Annotated
from database import db_session
from entities import Conversation
from fastapi import Depends, FastAPI, HTTPException, status
from schemas import ConversationCreate, ConversationOut, ConversationUpdate
from sqlalchemy import select

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

async def get_conversation(conversation_id:int, session: db_session) -> Conversation:
    async with session.begin():
        result = await session.execute(select(Conversation).where(Conversation.id == conversation_id))
        conversation = result.scalars().first()

    if not conversation:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Conversation not found"
        )
      
    return conversation

get_conversation_dep = Annotated[Conversation, Depends(get_conversation)]

@app.get("/conversations")
async def list_conversations(db: db_session, skip:int=0,
                             limit:int=100) -> list[ConversationOut]:
    async with db.begin():
        result = await db.execute(select(Conversation).offset(skip).limit(limit))
        return [
            ConversationOut.model_validate(conversation) 
            for conversation in result.scalars().all()
        ]
    
@app.get("/conversations/{id}")
async def get_conversation(db:db_session,conversation:get_conversation_dep) -> ConversationOut:
    return ConversationOut.model_validate(conversation)

@app.post("/conversations",status_code=status.HTTP_201_CREATED)
async def create_conversation(db:db_session,conversation:ConversationCreate) -> ConversationOut:
    new_conversation = Conversation(**conversation.model_dump())
    async with db.begin():
        db.add(new_conversation)
        await db.commit()
        await db.refresh(new_conversation)
    return ConversationOut.model_validate(new_conversation)

@app.put("/conversations/{id}",status_code = status.HTTP_202_ACCEPTED)
async def update_conversation(db:db_session,conversation:get_conversation_dep,
                              conversation_update:ConversationUpdate) -> ConversationOut:
    for key,value in conversation_update.model_dump().items():
        setattr(conversation,key,value)

    async with db.begin():
        await db.commit()
        await db.refresh(conversation)

    return ConversationOut.model_validate(conversation)

@app.delete("/conversations/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(db:db_session,conversation:get_conversation_dep) -> None:
    async with db.begin():
        await db.delete(conversation)
        await db.commit()
    return None
```

- Define a dependency to check if the conversation record exists. Raise a 404 HTTPException if a record is not found; otherwise, return the retrieved record. This dependency can be reused across several CRUD endpoints through dependency injection. 
- Begin the async session within an async context manager during each request. 
- When listing records, it’s more efficient to retrieve only a subset of records. By default, SQLAlchemy ORM returns a subset of most recent records in the database, but you can use the .offset(skip) and .limit(take) chained methods to retrieve any subset of records. 
- Create a Pydantic model from a SQLAlchemy model using model_validate() . Raises a ValidationError if the SQLAlchemy object passed can’t be created or doesn’t pass Pydantic’s data validation checks. 
- For operations that mutate a record (i.e., create, update, and delete), commit the transaction then send the refreshed record to the client, except for the successful delete operation that should return None .

Notice how the controller logic is simplified through this dependency injection approach. Additionally, pay attention to success status codes you should to send to the client. Successful retrieval operations should return 200, while record creation operations return 201, updates return 202, and deletions return 204. Congratulations! You now have a resource-based RESTful API that you can use to perform CRUD operations on your conversations table. Now that you can implement CRUD endpoints, let’s refactor the existing code examples to use the repository and services design pattern you learned

#### Repository and Services Design Pattern 
A repository is a design pattern that mediates the business logic of your application and the database access layer—for instance, via an ORM. It contains several methods for performing CRUD operations in the database layer.
![[Pasted image 20260125023303.png]]

>[!note]
>If you’ve never used abstract classes, they’re classes that can’t be instantiated on their own. Abstract classes can contain methods without implementation that its subclasses must implement.
> A concrete class is one that inherits an abstract class and implements each of its abstract methods

To implement a repository pattern, you can use an abstract interface
repo/interface.py
```python
from abc import ABC,abstractmethod
from typing import Any, List,Dict,Optional
from pydantic import BaseModel

class Repository(ABC):
    @abstractmethod
    async def list(self) -> list[Any]:
        pass

    @abstractmethod
    async def get(self, id:int) -> Any:
        pass

    @abstractmethod
    async def create(self, record:Any) -> Any:
        pass

    @abstractmethod
    async def update(self, id:int, record:Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, id:int) -> None:
        pass
```

Define the abstract Repository interface with several CRUD-related abstract method signatures that subclasses must implement. If an abstract method is not implemented in a concrete subclass, a NotImplementedError will be raised.

Implementing the conversation repository using the abstract repository interface
repo/conversations.py
```python
from entities import Conversation
from repo.interfaces import Repository
from schemas import ConversationCreate, ConversationUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ConversationRepository(Repository):
    def __init__(self,session:AsyncSession):
        self.db = session

    async def list(self,skip:int=0, limit:int=100) -> list[Conversation]:
        async with self.db.begin():
            result = await self.db.execute(
                select(Conversation).offset(skip).limit(limit)
            )
            results = result.scalars().all()
            return [r for r in results]

    async def get(self, conversation_id:int) -> Conversation | None:
        async with self.db.begin():
            result = await self.db.execute(select(Conversation).where(Conversation.id == conversation_id))
            return result.scalars().first()
        
    async def create(self, conversation:ConversationCreate) -> Conversation:
        new_conversation = Conversation(**conversation.model_dump())
        async with self.db.begin():
            self.db.add(new_conversation)
            await self.db.commit()
            await self.db.refresh(new_conversation)
        return new_conversation
    
    async def update(self,conversation_id:int, conversation:ConversationUpdate) -> Conversation | None:
        conversation = await self.get(conversation_id)

        if not conversation:
            return None

        for k,v in conversation.model_dump().items():
            setattr(conversation,k,v)

        async with self.db.begin():
            await self.db.commit()
            await self.db.refresh(conversation)
        
        return conversation
    
    async def delete(self,conversation_id:int) -> None:
        conversation = await self.get(conversation_id)

        if not conversation:
            return None

        async with self.db.begin():
            await self.db.delete(conversation)
            await self.db.commit()
        
        return None
```

- You have now moved the database logic for conversations into the ConversationRepository . 
- This means you can now import this class into your route controller functions and start using it right away.
- Go back to your main.py file and refactor your route controllers to use the ConversationRepository 
#### Refactoring the conversation CRUD endpoints to use the repository pattern
routers/conversations.py

```python
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from requests import session
from entities import Conversation
from repo.conversations import ConversationRepository
from database import db_session
from schemas import ConversationCreate, ConversationOut,ConversationUpdate
from entities import Conversation

#Other controllers and depencies implementations

router = APIRouter(prefix = "/conversations")

async def get_conversation(conversation_id:int,db: db_session) -> Conversation:
    conversation = await ConversationRepository(db).get(conversation_id)

    if not conversation:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Conversation not found"
        )
    return conversation

get_conversation_dep = Annotated[Conversation, Depends(get_conversation)]

@router.get("")
async def list_conversations_controller(
    db: db_session, skip: int = 0, limit: int = 100) -> list[ConversationOut]:
    conversations = await ConversationRepository(db).list(skip, limit)
    return [ConversationOut.model_validate(c) for c in conversations]

@router.get("/{id}")
async def get_conversation_controller(conversation: get_conversation_dep) -> ConversationOut:
    return ConversationOut.model_validate(conversation) 

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_conversation_controller(
    conversation: ConversationCreate, db: db_session) -> ConversationOut:
    new_conversation = await ConversationRepository(db).create(
        conversation
    ) 
    return ConversationOut.model_validate(new_conversation)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_conversation_controller(
    conversation: get_conversation_dep,updated_conversation: ConversationUpdate,
    db: db_session) -> ConversationOut:
    updated_conversation = await ConversationRepository(db).update(conversation.id, updated_conversation)
    return ConversationOut.model_validate(updated_conversation)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_controller(conversation: get_conversation_dep, db: db_session) -> None:
    await ConversationRepository(db).delete(conversation.id)
```

main.py
```python
from routers.conversations import router as conversations_router

app.include_router(conversations_router)
```

1. Place conversation CRUD routes on a separate API router and include on the FastAPI application for modular API design. 
2. Refactor conversation CRUD routes to use the repository pattern for more readable controller implementation.

Do you notice how cleaner your route controllers appear now that the database logic has been abstracted within the ConversationRepository class? 
You can take this approach one step further and implement a service pattern as well. A service pattern is an extension of the repository pattern that encapsulates the business logic and operations in a higher layer. These higher-level operations often require more complex queries and a sequence of CRUD operations to be performed to implement the business logic

As an example, you can implement a ConversationService to fetch messages related to a conversation or a specific user
Since it extends a ConversationRepository , you can still access the lower-level data access CRUD methods such as list , get , create , update , and delete .

Once again you can go back to your controllers and replace references to the ConversationRepository with the ConversationService instead. Additionally, you can use the same service to add a new endpoint for fetching messages within a single conversation.

#### Implementing the conversation services pattern
services/conversations.py
```python
from entities import Message
from repo.conversations import ConversationRepository
from sqlalchemy import select

class ConversationService:
    async def list_message(self,conversation_id:int) -> list[Message]:
        result = await self.session.execute(select(Message).where(Message.conversation_id == conversation_id))
        results = result.scalars().all()
        return [r for r in results]
```

routers/conversations.py
```python
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from requests import session
from entities import Conversation,Message
from repo.conversations import ConversationRepository
from database import db_session
from schemas import ConversationCreate, ConversationOut,ConversationUpdate
from entities import Conversation
from services.conversations import ConversationService
from schemas import MessageOut

#Other controllers and depencies implementations

router = APIRouter(prefix = "/conversations")

@router.get("/{conversation_id}/messages")
async def list_conversation_messages(conversation: get_conversation_dep,db:db_session) -> list[Message]:
    messages = await ConversationService(db).list_message(conversation.id)
    return messages
```
Add a new endpoint to list messages of a conversation using the conversation ID.

>[!tip]
>Now that you’re more familiar with the repository and services pattern, you can try implementing CRUD endpoints for the messages table

When implementing repository and service patterns, maintaining a clean separation of concerns is vital for a scalable architecture. Here are the key points to keep in mind:

* **Loose Coupling:** Avoid tightly coupling services to specific repository implementations. Use interfaces to ensure that your business logic remains independent of the underlying data access technology.
* **Separation of Concerns:** * **Services:** Keep these focused on business logic and avoid overloading them with unrelated responsibilities.
* **Repositories:** Limit these strictly to data access and manipulation. Do not place business logic within repository methods.
* **Transaction & Exception Management:** Handle database transactions and exceptions carefully, particularly when a single service action involves multiple related database operations that must succeed or fail together.
* **Performance Optimization:** Be mindful of query complexity. Minimize the use of excessive **JOINs** and optimize your queries to prevent performance bottlenecks.
* **Standardization & Flexibility:** * Use **consistent naming conventions** for all methods and classes to improve maintainability.
* Avoid **hard-coding configuration settings**; use environment variables or configuration files instead.
* **Schema Management:** Establish a robust workflow for managing database schema changes, especially in collaborative environments where multiple developers are interacting with the same development and production databases.

---
#### Managing DB Schemas changes
Alembic allows you to version control your database schemas the same way that tools like Git can help you version control your code. They’re extremely useful when you’re working in a team with multiple application environments and need to keep track of changes or revert updates as needed
```python
alembic init alembic
```

Alembic environment within your project root directory 
project/ 
	alembic.ini 
	alembic/ 
		env.py 
		README 
		script.py.mako 
		versions/
#### Connect the Alembic environment with your SQLAlchemy models
With Alembic connected to your SQLAlchemy models, Alembic can now auto-generate your migration files by comparing the current schema of your database with your SQLAlchemy models
```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from entities import Base
from settings import get_settings

from alembic import context

settings = get_settings()
db_url = settings.database_url
context.config.set_main_option("sqlalchemy.url", db_url)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
```

```python
$ alembic revision --autogenerate -m "Initial Migration"
```

This command will compare the defined SQLAlchemy models against the existing database schema and automatically generate a SQL migration file under the alembic/versions directory.

Now that you’ve updated your first migration file, you’re ready to run it against the database:
```python
$ alembic upgrade head
```

If your ever need to revert the operation, you can run alembic downgrade instead. What Alembic does under the hood is to generate the raw SQL needed to run or revert a migration and create an alembic_versions table in the database. It uses this table to keep track of migrations that have already been applied on your database so that rerunning the alembic upgrade head command won’t perform any duplicate migrations. 
If in any case, your database schemas and your migration history drift away, you can always remove files from the versions directory and truncate the alembic_revision table. Then reinitialize Alembic to start with a fresh environment against an existing database.

>[!warning]
>After migrating a database with a migration file, make sure to commit to a Git repository. Avoid re-editing migration files after migrating a database as Alembic will skip existing migrations by cross-checking them with its versioning table. If a migration file has already been run, it won’t detect changes in its content. To update your database schema, create a new migration file instead.
#### Storing Data when working with Real-Time Streams
- You should now be in a position to implement your own CRUD endpoints to retrieve and mutate both user conversation and message records in your database
- One question that remains unanswered is how to handle transactions within data streaming endpoints, such as an LLM streaming outputs to a client
- You can’t stream data into a traditional relational database as ensuring ACID compliance with streaming transactions will prove challenging. Instead, you will want to perform your standard database operation as soon as your FastAPI server returns a response to the client. This challenge is exactly what a FastAPI’s background task can solve

Storing content of an LLM output stream
main.py
```python
async def store_message(prompt_content:str, response_content:str,
                        conversation_id:int, session:AsyncSession):
    message = Message(
        conversation_id = conversation_id,
        prompt_content = prompt_content,
        response_content = response_content
    )
    await MessageRepository(session).create(message)

@app.get("/text/generate/stream")
async def stream_llm(prompt:str,background_tasks: BackgroundTasks,
                     db: db_session, conversation: Conversation = Depends(get_conversation)) -> StreamingResponse:
    #llm.generate(prompt)
    stream1,stream2 = tee(response_stream)
    background_tasks.add_task(
        store_message,
        prompt,
        "".join(stream1),
        conversation.id,
        db
    )
    return StreamingResponse(stream2)
```

1. Create a function to store a message against a conversation.
2. Check that the conversation record exists and fetch it within a dependency.
3. Create two separate copies of the LLM stream, one for the StreamingResponse and another to process in a background task.
4. Create a background task to store the message after the StreamingResponse is finished.

It won’t matter whether you’re using an SSE or WebSocket endpoint. Once a request a response is fully streamed, invoke a background task passing in the full stream response content. Within the background task, you can then run a function to store the message after the request is sent, with the full LLM response content. Using the same approach, you can even generate a title for a conversation based on the content of the first message. To do this, you can invoke the LLM again with the content of the first message in the conversation, requesting for an appropriate title for the conversation. Once a conversation title is generated, you can create the conversation record in the database

Using the LLM to generate conversation titles based on the initial user prompt
```python
from entities import Conversation
from openai import AsyncClient
from repositories.conversations import ConversationRepository
from sqlalchemy.ext.asyncio import AsyncSession

async_client = AsyncClient(...)

async def create_conversation(
    initial_prompt: str, 
    session: AsyncSession
) -> Conversation:
    # Request a title generation from the LLM
    completion = await async_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Suggest a title for the conversation based on the user prompt",
            },
            {
                "role": "user", 
                "content": initial_prompt,
            },
        ],
        model="gpt-3.5-turbo",
    )

    # Extract the title from the response
    title = completion.choices[0].message.content

    # Instantiate the Conversation entity
    conversation = Conversation(
        title=title,
        # add other conversation properties ...
    )

    # Persist and return the new conversation
    return await ConversationRepository(session).create(conversation)
```

Using SQLAlchemy with Alembic is a tried and tested approach to working with relational databases in FastAPI, so you’re more likely to find a lot of resources on integrating these technologies. Both the SQLAlchemy ORM and Alembic allow you to interact with your database and control the changes to its schemas.