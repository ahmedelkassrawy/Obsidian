---
description: "Hub: every note about MySQL"
type: hub
domain: backend
tags:
  - type/hub
  - topic/mysql
---
# MySQL

> [!info] Four High Performance MySQL chapters on architecture, benchmarking, schema and profiling. Missing: replication setup and InnoDB tuning in practice.
> Part of [[MOC - Backend]]. Also try the tag `#topic/mysql`.

## Book notes
- [[High Performance MySQL - Architecture, Locking and Transactions]] — Book chapter on the MySQL layered architecture, lock granularity (table vs row), transactions and isolation levels.
- [[High Performance MySQL - Benchmarking]] — Book chapter on benchmarking MySQL: why synthetic workloads mislead, benchmarking strategies and tactics, and the tools to use.
- [[Optimizing Schema and Data Types]] — Book chapter on picking optimal MySQL data types, identifier choice, schema gotchas and the normalization/denormalization trade-off.
- [[Profiling Server Performance]] — Book chapter on profiling MySQL server performance: where response time goes, profiling types, instrumentation and the tools.

## Course notes
- [[InnoDB]] — Course notes on the InnoDB storage engine: its structure, transactional ACID support, advanced features and when to pick it.
- [[MyISAM]] — Course notes on the MyISAM engine: index-everything design, no transactions, table-level locking and its reliability problems.

## Related hubs
[[Database Internals]], [[Observability]], [[Transactions & Concurrency Control]], [[Testing]], [[SQL]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
