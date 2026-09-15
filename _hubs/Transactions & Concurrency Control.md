---
description: "Hub: every note about Transactions & Concurrency Control"
type: hub
domain: backend
tags:
  - type/hub
  - topic/transactions-and-concurrency-control
---
# Transactions & Concurrency Control

> [!info] Locks, two-phase locking, double booking, isolation levels. Missing: MVCC mechanics and deadlock debugging.
> Part of [[MOC - Backend]]. Also try the tag `#topic/transactions-and-concurrency-control`.

## Concepts
- [[Concurrency]] — Shows a race condition in concurrent transactions and walks the fixes: single threading, locking and fine-grained locks, with common mistakes.
- [[Exclusive Lock VS Shared Lock]] — Explains exclusive vs shared locks, the compatibility matrix between them, and how they lead to deadlocks.

## How-tos & recipes
- [[Pooling]] `empty` — Empty note - the connection pooling section was never written.

## References & cheat sheets
- [[SQL]] `raw` — A long unsectioned dump of SQL fundamentals - statement categories, schemas, joins, constraints and related concepts - in one flat run of bullets.

## Book notes
- [[High Performance MySQL - Architecture, Locking and Transactions]] — Book chapter on the MySQL layered architecture, lock granularity (table vs row), transactions and isolation levels.

## Course notes
- [[Double Booking Prevention]] — Course notes on preventing double booking with SELECT ... FOR UPDATE versus a direct conditional UPDATE, and when each is better.
- [[SQL Cursors, Identity, Snapshots and SQLCLR]] — Course notes on SQL cursors, identity columns, insert variants, database snapshots and SQLCLR.
- [[Two Phase Locking]] — Course notes on two-phase locking: growing and shrinking phases, how it guarantees serializability, and a SQL double-booking walkthrough.

## Project notes
- [[IdempotencyManager - Review & Fixes]] — Code review of a project's IdempotencyManager: the race condition, the celery_task_id coupling and the sync/async mismatch, with the fixes for each.

## Related hubs
[[Postgres]], [[SQL]], [[Celery & Message Queues]], [[SQLAlchemy]], [[Concurrency & Async]], [[System Design]]

## Notes to self (from the audit)
- [[Pooling]]: Empty file (0 words). Content likely belongs with 'Best Practices for SQL Connection Pooling'.
- [[SQL]]: 685 lines with zero headings. Needs splitting into sections before it is usable; overlaps the SQL/ folder notes.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
