paraphrase-multilingual-MiniLM-L12-v2 - English , Arabic Support
Qdrant as Vector DB + Postgres for chats and users
Langfuse For Observability + Evaluation 
PyMuPDF4llm + Fibrumpdf
using lru_cache
Fastapi users -> Authentication
# PostgreSQL + SQLAlchemy Best Practices & Setup Notes

## Database Design & Conventions

- Use **`JSONB`** instead of Python `dict` columns when storing semi-structured / flexible data  
  → Better querying, indexing, and performance in PostgreSQL

- Use **`UUID`** (as `UUID(as_uuid=True)`) as a public-facing / external identifier  
  → The internal `id` (serial / integer PK) stays private  
  → `asset_uuid`, `project_uuid`, etc. are used in APIs, URLs, client-side, etc.

- **Indexing rules we follow**:
  - Primary keys and `unique=True` columns → SQLAlchemy / PostgreSQL **automatically** create indexes
  - **Foreign keys do NOT** get automatic indexes → **always** add an explicit index on FK columns
  - Frequently filtered columns (e.g. `type`, `status`, `created_at`) → consider adding indexes

## Alembic Setup Checklist (one-time)

1. Initialize Alembic  
   ```bash
   alembic init alembic
   ```

2. Add `alembic/` to `.gitignore`

3. Edit `alembic.ini`  
   Find the line:
   ```ini
   sqlalchemy.url =
   ```
   Replace with your PostgreSQL connection string, e.g.:
   ```ini
   sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/dbname
   ```

4. Configure `alembic/env.py`  
   In the `env.py` file, find:
   ```python
   target_metadata = None
   ```
   Replace with:
   ```python
   from src.models import SQLAlchemyBase   # ← adjust import path
   target_metadata = SQLAlchemyBase.metadata
   ```

5. Create first migration (initial schema)
   ```bash
   alembic revision --autogenerate -m "initial commit"
   ```

6. Apply migration
   ```bash
   alembic upgrade head
   ```

The rest of the workflow (new models → new migration → review & apply) is described in the main README.

## Recommended Patterns

### Creating records (async SQLAlchemy 2.0+ style)

```python
async def create_project(self, project: Project) -> Project:
    async with self.db_client() as session:
        async with session.begin():
            session.add(project)
            await session.commit()
            await session.refresh(project)   # gets generated fields: id, uuid, created_at, ...
            return project
```

### Use Python `enum.Enum` + PostgreSQL `ENUM` when possible

Instead of plain strings for status / type / role columns that have a fixed set of values.

Example:
```python
from enum import Enum as PyEnum

class AssetType(str, PyEnum):
    DOCUMENT = "document"
    IMAGE    = "image"
    VIDEO    = "video"
    AUDIO    = "audio"
```

(then either use native PostgreSQL ENUM or just store as `String` + check in code / constraints)

### Example Model with PGVector + our conventions

```python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from .base import SQLAlchemyBase


class Asset(SQLAlchemyBase):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Internal sequential ID (never exposed)"
    )

    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,                 # safe to index UUIDs used in lookups
        comment="Public-facing identifier"
    )

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
        index=True                  # ← important: FK index
    )

    type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True                  # frequently filtered
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    config: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Flexible configuration stored as JSONB"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="assets"
    )

    data_chunks: Mapped[list["DataChunk"]] = relationship(
        "DataChunk",
        back_populates="asset",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        # You can still add extra indexes here if needed
        Index("ix_asset_project_type", "project_id", "type"),
    )
```

### Quick Summary – Rules of Thumb

- `id` → internal integer PK (hidden)  
- `uuid` → public, unique, indexed  
- Every **foreign key column** → add `index=True` or explicit `Index`  
- Use `JSONB` for flexible structured data  
- Use modern Mapped + annotated style when possible (SQLAlchemy 2.0+)  
- Always refresh after commit when you need generated/default values
