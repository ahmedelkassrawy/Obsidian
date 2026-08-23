---
tags: [sqlalchemy, async, asyncio, AsyncSession, async_sessionmaker, fastapi, asyncpg, aiosqlite, asynccontextmanager, ingestion, pgvector]
aliases: [Async SQLAlchemy, AsyncSession, async_sessionmaker, create_async_engine, await db.execute, await db.commit, expire_on_commit, async get_db, ingest_pdf example]
source: https://github.com/h9-tec/AI_deployment#asynchronous-operations-asyncawait
---

# 10 — Async SQLAlchemy

> [!info] Source
> Your section 10 + README §7 "Asynchronous Operations", restructured around the **recommended pattern** and a **worked example** from `raaaaag/src/backend/ingest.py`.
> Back to [[00 - Index]] · Previous: [[09 - Querying Data]]

## The one-sentence version

Same ORM, async plumbing: `create_async_engine`, `async_sessionmaker(... expire_on_commit=False)`, `async with get_db() as db:`, `select()` instead of `query()`, and `await` on anything that touches the network (`execute`, `commit`, `refresh`, `flush`, `get`).

## Why async

A sync DB call blocks its thread. Inside an `async def` endpoint that blocks the **event loop** — every other request waits. `sqlalchemy.ext.asyncio` makes DB I/O awaitable so the loop keeps serving.

Drivers must be async too:

| DB | Sync driver | Async driver | URL |
|---|---|---|---|
| PostgreSQL | psycopg2 | **asyncpg** | `postgresql+asyncpg://u:p@host/db` |
| SQLite | sqlite3 | **aiosqlite** | `sqlite+aiosqlite:///./t.db` |
| MySQL | pymysql | aiomysql / asyncmy | `mysql+aiomysql://…` |

```bash
pip install sqlalchemy asyncpg        # or aiosqlite
```

## The recommended database.py (async)

This is the shape `raaaaag/src/backend/db/database.py` already has — it's the right one.

```python
# db/database.py
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,        # REQUIRED in async — see "The big trap" below
)


@asynccontextmanager
async def get_db():
    """ORM session — commits on success, rolls back on error, always closes."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_db_connection():
    """Raw Core connection — one-off SQL, DDL, run_sync."""
    async with engine.connect() as conn:
        yield conn
```

### How you use it

```python
# in scripts / jobs / services
async with get_db() as db:
    db.add(Document(chunk_text=..., embedding_vector=...))
    # commit on exit

# NEVER this:
db = get_db()          # -> _AsyncGeneratorContextManager, not a session. Nothing works.
```

### FastAPI needs the un-decorated generator

```python
async def get_db_dep():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/docs/{doc_id}")
async def read_doc(doc_id: int, db: AsyncSession = Depends(get_db_dep)):
    return await db.get(Document, doc_id)
```

Same body as `get_db`, **no `@asynccontextmanager`** — FastAPI drives generator dependencies itself. Keep both helpers in `database.py`. Full explanation of the two shapes: [[05 - Sessions and sessionmaker#The FastAPI dependency is a different shape — don't mix them up]].

## What gets awaited and what doesn't

| Call | Await? | Why |
|---|---|---|
| `await db.execute(stmt)` | yes | network I/O |
| `result.scalar_one_or_none()`, `.scalars().all()`, `.first()` | **no** | rows are already in memory |
| `db.add(obj)`, `db.add_all(objs)` | **no** | just stages in the session |
| `await db.flush()` | yes | sends INSERT/UPDATE |
| `await db.commit()` / `await db.rollback()` | yes | |
| `await db.refresh(obj)` | yes | SELECT |
| `await db.get(Model, pk)` | yes | may SELECT |
| `await db.delete(obj)` | yes | (it's a coroutine on AsyncSession) |
| `obj.field = value` | no | plain attribute set |

Forgetting an `await` on `commit()` = nothing saved + `RuntimeWarning: coroutine ... was never awaited`.

## The operations (your 10.1–10.10, tightened)

```python
from sqlalchemy import select, insert

# SELECT one
result = await db.execute(select(Order).where(Order.order_id == oid))
order = result.scalar_one_or_none()

# SELECT many
docs = (await db.execute(select(Document).order_by(Document.id))).scalars().all()

# by primary key
doc = await db.get(Document, 5)

# INSERT (ORM) — default path
db.add(Document(chunk_text=t, embedding_vector=v))
await db.flush()          # only if you need doc.id before the block ends

# INSERT many (ORM)
db.add_all([Document(...) for ...])

# INSERT many (Core bulk) — thousands of rows
await db.execute(insert(Document), [{"chunk_text": t, "embedding_vector": v} for t, v in rows])

# UPDATE
doc.chunk_text = "new"    # then commit (get_db does it)

# DELETE
await db.delete(doc)
```

No `db.query()` on `AsyncSession` — `select()` only.

## Worked example — PDF ingestion

The real file: `raaaaag/src/backend/ingest.py`. What was wrong:

```python
db = get_db()                                   # (1) context manager object, not a session
...
for t in texts:
    embedding_vector = embeddings.embed_documents([t.page_content])[0]   # (2) one API call per chunk
    document = Document(chunk_text=t.page_content, embedding_vector=embedding_vector)
    chunks = await db.execute(Insert)            # (3) Insert undefined; and you built an ORM object — use add()
                                                 # (4) no session scope, so no commit
```

**Fixed (recommended: `db.add` inside one `async with get_db()` block):**

```python
# ingest.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_cohere import CohereEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import get_settings
from src.backend.db.database import get_db
from src.backend.db.models import Document

settings = get_settings()


def get_embeddings() -> CohereEmbeddings:
    return CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=settings.COHERE_API_KEY)


async def ingest_pdf(file_path: str) -> int:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Invalid file type. Please provide a PDF file.")

    docs = PyPDFLoader(file_path).load()
    texts = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50).split_documents(docs)
    if not texts:
        return 0

    # one embeddings call for the whole document, not one per chunk
    vectors = get_embeddings().embed_documents([t.page_content for t in texts])

    async with get_db() as db:                          # one session, one transaction, commit on exit
        db.add_all(
            Document(chunk_text=t.page_content, embedding_vector=v)
            for t, v in zip(texts, vectors)
        )

    return len(texts)
```

Why this is the better option here:

- A PDF yields tens to low thousands of chunks → `add_all` is fast enough and keeps the code ORM-only.
- `get_db` handles commit/rollback — if Cohere or the DB fails mid-way, nothing half-written lands.
- `expire_on_commit=False` means the returned count/objects are safe to use after the block.

When to switch to the bulk `insert()` path: tens of thousands of chunks per run, or you're re-ingesting and want `ON CONFLICT DO NOTHING`. Then:

```python
from sqlalchemy import insert

async with get_db() as db:
    await db.execute(
        insert(Document),
        [{"chunk_text": t.page_content, "embedding_vector": v} for t, v in zip(texts, vectors)],
    )
```

### Creating the tables (async)

`create_all` is sync DDL; bridge it with `run_sync`. Do it once at startup, not per ingest:

```python
from sqlalchemy import text
from src.backend.db.database import engine
from src.backend.db.models import Base

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))   # pgvector, Postgres only
        await conn.run_sync(Base.metadata.create_all)
```

## The big trap — lazy loading in async

Attribute access can't `await`, so a lazy relationship load (`user.products`) or an expired attribute after `commit()` raises `sqlalchemy.exc.MissingGreenlet`. Defences, in order:

1. `expire_on_commit=False` on the sessionmaker (done above).
2. Eager-load in the query: `select(User).options(selectinload(User.products))`.
3. Or on the model: `relationship(..., lazy="selectin")`.
4. Explicit: `await db.refresh(user, attribute_names=["products"])`.
5. To *catch* accidental lazy loads in tests: `relationship(..., lazy="raise")`.

Background: [[07 - Relationships One-to-Many#Lazy loading and the N+1 problem]].

## App startup / shutdown (FastAPI)

`@app.on_event("startup")` is deprecated; use `lifespan`:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()             # create tables / extensions
    yield
    await engine.dispose()      # close the pool cleanly

app = FastAPI(lifespan=lifespan)
```

## Sync vs async side by side

```python
# sync
def read_user(user_id: int, db: Session = Depends(get_db_dep)):
    return db.get(User, user_id)

# async
async def read_user(user_id: int, db: AsyncSession = Depends(get_db_dep)):
    return await db.get(User, user_id)
```

## Summary table

| Operation | Sync | Async |
|---|---|---|
| Engine | `create_engine(url)` | `create_async_engine(url)` |
| Factory | `sessionmaker(bind=engine, expire_on_commit=False)` | `async_sessionmaker(engine, expire_on_commit=False)` |
| Scope helper | `@contextmanager def get_db()` | `@asynccontextmanager async def get_db()` |
| Use it | `with get_db() as db:` | `async with get_db() as db:` |
| FastAPI dep | plain generator `def` | plain `async def` generator |
| Query | `db.execute(select(...))` | `await db.execute(select(...))` |
| By PK | `db.get(M, id)` | `await db.get(M, id)` |
| Stage | `db.add(obj)` | `db.add(obj)` (no await) |
| Flush / commit / refresh | `db.flush()` … | `await db.flush()` … |
| Delete | `db.delete(obj)` | `await db.delete(obj)` |
| DDL | `Base.metadata.create_all(engine)` | `await conn.run_sync(Base.metadata.create_all)` |
| Lazy relationships | work (extra query) | **fail** → eager-load |

## Next

→ [[11 - Core vs ORM — when to use which]]
