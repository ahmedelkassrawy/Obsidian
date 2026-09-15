---
description: "Hub: every note about SQLAlchemy"
type: hub
domain: backend
tags:
  - type/hub
  - topic/sqlalchemy
---
# SQLAlchemy

> [!info] A rewritten 2.0-first series from engine through async, with cheatsheet, gotchas and a best-practices checklist. Missing: Alembic migrations.
> Part of [[MOC - Backend]]. Also try the tag `#topic/sqlalchemy`.

## Concepts
- [[01 - Overview and Project Layout]] — Maps which of the three libraries owns which job and traces one POST request end to end through the project layout.
- [[11 - Core vs ORM — when to use which]] — Compares the Core and ORM layers side by side and gives the rules for picking one, the other, or both.

## How-tos & recipes
- [[01 - Engine and Connections]] — Creating the engine, database URL formats, and opening connections with context managers.
- [[02 - Core Tables with MetaData]] — Describing tables in SQLAlchemy Core with Table and MetaData, column options and create_all.
- [[02 - Database Session Dependency (get_db)]] — Builds the get_db dependency: SessionLocal, yielding a session per request and closing it afterwards.
- [[03 - Core CRUD (insert, select, update, delete)]] — The four Core statement builders, why not f-strings, commit for writes, and bulk inserts.
- [[04 - API Endpoints with Database Operations]] — Writes the CRUD endpoints against the database, including where each parameter comes from and the add/commit/refresh dance.
- [[04 - ORM Models (declarative_base)]] — Defining ORM models 2.0-style with DeclarativeBase, Mapped and mapped_column, plus type-hint to column mapping.
- [[05 - Sessions and sessionmaker]] — The session factory, the commit-on-exit default, object states and the FastAPI session dependency.
- [[06 - ORM CRUD]] — ORM create/read/update/delete in one crud.py, and when to drop to Core inserts instead.
- [[07 - Relationships One-to-Many]] — Declaring and navigating one-to-many relationships, and the difference between setting the FK and setting the relationship.
- [[08 - Many-to-Many and Association Objects]] — Many-to-many mapping via a link table, composite primary keys, and when to promote the link to an association object.
- [[09 - Querying Data]] — Querying with 2.0 select() (and legacy query()): filters, ordering, paging, aggregates and relationship loading.
- [[10 - Async SQLAlchemy]] — The recommended async engine/session setup, what must be awaited, and a worked async ingest example.
- [[PGVector]] `raw` — Pasted PGVector code: running Postgres with pgvector in Docker, the async PGVector store, the database functions used, and the SQLAlchemy Result methods for reading rows back.

## References & cheat sheets
- [[07 - Full Source Listing (copy-paste ready)]] — The complete working source for the integrated app in two file layouts, ready to copy.
- [[08 - Gotchas and Troubleshooting]] — Catalogue of the real errors you hit wiring FastAPI, Pydantic and SQLAlchemy, each with cause and fix, searchable by error text.
- [[09 - Cheatsheet]] — One-screen condensed setup, schema and endpoint templates for the FastAPI + SQLAlchemy stack.
- [[12 - Cheatsheet]] — One-screen 2.0-style cheatsheet: project layout, CRUD, filters, results and relationship declarations.
- [[13 - Gotchas and Troubleshooting]] — Searchable list of common SQLAlchemy errors and silent failures with their causes and fixes.
- [[14 - Best Practices Checklist]] — A tick-box review checklist for any file that touches SQLAlchemy, each item linking to the note that explains it.
- [[FastAPI Users - SQLAlchemy Adapter]] `raw` — The SQLAlchemy database adapter setup for FastAPI Users, including the async-session expire_on_commit=False warning.

## Book notes
- [[Ch7.Integrating DB in AI services]] — Ch7 notes on wiring a database into a FastAPI AI service: SQLAlchemy ORM models, the engine as a connection pool, session dependency injection, and Alembic migrations.
- [[Creating the Database Layer]] — Book chapter building the data layer: the three layers, the models file with Player/Performance/League/Team relationships, and the database config.
- [[SQLAlchemy CRUD And Relationships Recap]] — Closing recap of the API book's CRUD layer: SQLAlchemy read queries, pagination and filtering, eager loading, and many-to-many relationships with composite keys.

## Project notes
- [[IdempotencyManager - Review & Fixes]] — Code review of a project's IdempotencyManager: the race condition, the celery_task_id coupling and the sync/async mismatch, with the fixes for each.
- [[Mini-RAG Stack And Postgres Conventions]] — The Mini-RAG project stack (multilingual embeddings, Qdrant plus Postgres, Langfuse, PyMuPDF4llm) followed by the Postgres and SQLAlchemy conventions the project follows, including Alembic setup and async record creation.

## Meta
- [[00 - Index]] — Index for the FastAPI + Pydantic + SQLAlchemy folder: reading order, look-up notes and a 'I want to find' table.
- [[00 - Index]] — Index for the SQLAlchemy folder: the recommended project shape, reading order, look-up notes and a find-it table.

## Clippings (raw)
- [[Advanced Topics and Best Practices]] `raw` — Verbatim copy of section 7 of the h9-tec/AI_deployment README on async SQLAlchemy, dependency injection and other FastAPI best practices.

## Related hubs
[[FastAPI]], [[Pydantic]], [[Postgres]], [[SQL]], [[Database Indexing]], [[Concurrency & Async]]

## Notes to self (from the audit)
- [[Advanced Topics and Best Practices]]: Copied README section - overlaps the digested 'Integrating FastAPI, Pydantic, and SQLAlchemy' folder.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
