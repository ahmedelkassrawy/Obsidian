---
description: "Map of Content for the Backend domain"
type: moc
domain: backend
tags:
  - type/moc
  - domain/backend
---
# MOC - Backend

This is the backend half of the vault: building APIs, talking to databases, and getting the result onto a server.
Strongest areas: FastAPI and SQLAlchemy (two well-linked rewritten folders), database indexing and engine internals from the Fundamentals of Database Engineering course, and T-SQL from the eleven-part SQL series.
System design, caching, replication and concurrency control are solid at concept level but have no worked end-to-end designs.
Biggest gaps: Docker and Linux have no note that is actually yours (a copied tutorial and three copies of one command list), testing is nearly absent, and Redis, Nginx, Alembic and CI/CD have no note at all.
See 'Knowledge Gaps Audit 2026-09-15' for the full gap list.

**155 notes** — digested 118, raw 29, stub 6, stale 0, empty 2. Search tip: tag `#domain/backend`.

## Hubs
- [[API Design]] (18) — REST constraints, URL naming, idempotency, pagination and input validation. Missing: versioning in practice and an OpenAPI-first contract workflow.
- [[FastAPI]] (53) — The most complete area: async routes, params, Pydantic models, response models, security, webhooks, file uploads and project structure. Missing: background tasks vs Celery, and testing with TestClient.
- [[Pydantic]] (18) — Models, validation, serialization and settings. Missing: custom validators and v1-to-v2 migration gotchas.
- [[Auth & Security]] (28) — JWT, OAuth2/OpenID, RBAC and the whole FastAPI Users series. Most FastAPI Users notes are still doc excerpts rather than your own words.
- [[HTTP & Networking]] (16) — SSL/TLS, headers vs cookies, the Postgres wire protocol. Missing: HTTP caching headers, CORS in depth and load balancers.
- [[gRPC]] (2) — One good note from HTTP/2 through protobuf to a working service. Missing: streaming modes and gRPC in production.
- [[Concurrency & Async]] (12) — asyncio, coroutines, and async in FastAPI and SQLAlchemy. Missing: thread pools, the GIL in detail and structured concurrency.
- [[Celery & Message Queues]] (7) — A complete Celery guide, a RabbitMQ concept note and an idempotency code review. Missing: retries, dead-letter handling and worker monitoring.
- [[Testing]] (6) — Almost empty - only a manual curl run and the SQLAlchemy review checklist. This is the single biggest hole in the backend domain.
- [[SQLAlchemy]] (30) — A rewritten 2.0-first series from engine through async, with cheatsheet, gotchas and a best-practices checklist. Missing: Alembic migrations.
- [[SQL]] (22) — The eleven-part T-SQL course series plus a one-page summary. Missing: a clean rewrite of the unsectioned 'Database/SQL/SQL.md' dump.
- [[Postgres]] (19) — Indexing, cursors, partitioning, SSL and the wire protocol. Missing: VACUUM/autovacuum and configuration tuning.
- [[MySQL]] (6) — Four High Performance MySQL chapters on architecture, benchmarking, schema and profiling. Missing: replication setup and InnoDB tuning in practice.
- [[SQLite]] (3) — One engine note. Missing: WAL mode and the concurrency limits that bite in production.
- [[MongoDB]] (5) — Architecture, internals, clustered collections and a FastAPI+Motor howto. Missing: the aggregation pipeline and index design.
- [[Database Indexing]] (15) — Well covered: scan types, index-only scans, covering and composite indexes, EXPLAIN ANALYZE, bloom filters. Missing: index maintenance and bloat.
- [[Cursors & Pagination]] (3) — Server-side vs client-side cursors and why OFFSET paging fails. Missing: cursor pagination expressed in an actual API response format.
- [[Transactions & Concurrency Control]] (9) — Locks, two-phase locking, double booking, isolation levels. Missing: MVCC mechanics and deadlock debugging.
- [[Database Replication & Sharding]] (9) — Single-leader, multi-leader, stale reads, partitioning, consistent hashing, CAP. Missing: a real failover runbook.
- [[Database Internals]] (11) — New hub: storage engines (InnoDB, MyISAM, SQLite, WiredTiger) and Memcached memory management. Missing: B+tree and LSM-tree mechanics side by side.
- [[System Design]] (30) — A six-step method with latency numbers, scaling, queues, consistent hashing and layering patterns. Missing: worked end-to-end designs.
- [[Docker]] (11) — Only a copied docker.com tutorial (moved to _inbox). Nothing here is yours - write a real Dockerfile and compose note.
- [[Kubernetes]] (3) — Core concepts and a local-cluster MLOps blueprint. Missing: ingress, secrets/configmaps and resource limits.
- [[Cloud Deployment]] (12) — EC2 + compose, Azure App Service twice, Hugging Face Spaces. Missing: CI/CD beyond a sketch, and secrets management.
- [[Git]] (4) — One solid hands-on reference from the Git-Gud exercises; the older duplicate goes to _inbox. Missing: rebase-vs-merge policy and bisect.
- [[Linux & Shell]] (3) — Three notes that are the same command list at three depths; only the longest stays. Missing: shell scripting, systemd, permissions in depth and process/network debugging.
- [[Operating Systems]] (5) — Two OSTEP chapters and a stack-vs-heap stub. Missing: scheduling, virtual memory and everything after OSTEP chapter 2.

Gaps: [[Knowledge Gaps Audit 2026-09-15]]. Back to [[00 Home]].
