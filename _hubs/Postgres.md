---
description: "Hub: every note about Postgres"
type: hub
domain: backend
tags:
  - type/hub
  - topic/postgres
---
# Postgres

> [!info] Indexing, cursors, partitioning, SSL and the wire protocol. Missing: VACUUM/autovacuum and configuration tuning.
> Part of [[MOC - Backend]]. Also try the tag `#topic/postgres`.

## Concepts
- [[Best Practices for SQL Table Creation]] — Whether to run CREATE TABLE IF NOT EXISTS at application startup, and what to do instead in production (migrations).
- [[Why Avoid SQL OFFSET for Paging]] — Why OFFSET paging degrades and duplicates rows, demonstrated in PostgreSQL, plus keyset (seek) pagination as the replacement.

## How-tos & recipes
- [[Best Practices for SQL Connection Pooling]] — Lessons from a Node.js/PostgreSQL to-do app on connection pooling and database permissions, with the problems hit and the fixes applied.
- [[Enabling SSL,TLS]] — Step-by-step guide to enabling SSL/TLS on a Dockerised PostgreSQL, including generating certs and proving the traffic is encrypted.
- [[PostgreSQL EXPLAIN ANALYZE Notes]] — Reading PostgreSQL EXPLAIN ANALYZE output across four example queries, and the performance lessons from each plan.
- [[PostgreSQL Partitioning]] — Step-by-step PostgreSQL range partitioning: parent table, child partitions, attaching them, querying and indexing.
- [[Indexes Concurrently]] `stub` — Short note on CREATE INDEX CONCURRENTLY: it keeps reads and writes running but is slower and can fail.
- [[PGVector]] `raw` — Pasted PGVector code: running Postgres with pgvector in Docker, the async PGVector store, the database functions used, and the SQLAlchemy Result methods for reading rows back.
- [[Pooling]] `empty` — Empty note - the connection pooling section was never written.
- [[Sharding]] `raw` — Pasted SQL and Docker commands for spinning up two PostgreSQL shards behind a hash-based URL table.

## Book notes
- [[Ch7.Integrating DB in AI services]] — Ch7 notes on wiring a database into a FastAPI AI service: SQLAlchemy ORM models, the engine as a connection pool, session dependency injection, and Alembic migrations.

## Course notes
- [[Deep Look into Postgres Wire Protocol with Wireshark]] — Course notes tracing a Node.js to PostgreSQL connection in Wireshark: TCP handshake, startup message, auth request, query and teardown.
- [[Double Booking Prevention]] — Course notes on preventing double booking with SELECT ... FOR UPDATE versus a direct conditional UPDATE, and when each is better.
- [[Index Scan vs Index Only Scan]] — Course notes on PostgreSQL index scan vs index-only scan, covering indexes with INCLUDE, and leftmost-column rules for composite indexes.
- [[Intro Cursors]] — Course notes on PostgreSQL cursors: fetching a huge result set incrementally, the SQL to do it, and the pros and cons.
- [[Key vs Non-Key Column Indexes]] — Course notes distinguishing key-column indexes (constraints, uniqueness) from non-key INCLUDE columns, with the trade-offs.
- [[PostgreSQL Scan Types Comparison]] — Compares sequential, index and bitmap index scans in PostgreSQL, when the planner picks each, and a worked plan walkthrough.
- [[Server-Side vs. Client-Side]] — Course notes comparing server-side and client-side cursors in PostgreSQL from Python, with a one-million-row demo.

## Project notes
- [[Mini-RAG Stack And Postgres Conventions]] — The Mini-RAG project stack (multilingual embeddings, Qdrant plus Postgres, Langfuse, PyMuPDF4llm) followed by the Postgres and SQLAlchemy conventions the project follows, including Alembic setup and async record creation.

## Related hubs
[[Database Indexing]], [[SQLAlchemy]], [[Auth & Security]], [[SQL]], [[Cursors & Pagination]], [[Docker]]

## Notes to self (from the audit)
- [[Indexes Concurrently]]: Stub - add the failure/cleanup procedure for an invalid index.
- [[Sharding]]: Code-only - no explanation of the shard key choice or routing logic.
- [[Pooling]]: Empty file (0 words). Content likely belongs with 'Best Practices for SQL Connection Pooling'.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
