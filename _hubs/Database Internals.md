---
description: "Hub: every note about Database Internals"
type: hub
domain: backend
tags:
  - type/hub
  - topic/database-internals
---
# Database Internals

> [!info] New hub: storage engines (InnoDB, MyISAM, SQLite, WiredTiger) and Memcached memory management. Missing: B+tree and LSM-tree mechanics side by side.
> Part of [[MOC - Backend]]. Also try the tag `#topic/database-internals`.

## Concepts
- [[Bloom Filters]] — What a Bloom filter is, how the bit array and hash functions work, why false positives happen and where to use one.

## Book notes
- [[High Performance MySQL - Architecture, Locking and Transactions]] — Book chapter on the MySQL layered architecture, lock granularity (table vs row), transactions and isolation levels.

## Course notes
- [[BASE Model vs ACID]] — Course notes on the BASE model used by NoSQL stores (basically available, soft state, eventually consistent) and how it contrasts with ACID.
- [[InnoDB]] — Course notes on the InnoDB storage engine: its structure, transactional ACID support, advanced features and when to pick it.
- [[Intro DB Engine]] — Course notes defining a database engine as the library that handles disk storage and indexes, and why DBMS and engine are separated.
- [[Memcached]] — Course notes on Memcached internals: slab allocation against fragmentation, listener/worker threading and LRU eviction.
- [[MongoDB Architecture]] — Course notes on MongoDB's architecture and storage engine evolution from MMAPv1 to WiredTiger and clustered collections.
- [[MongoDB Cluster Collection]] — Course notes on MongoDB 5.3+ clustered collections: storing documents inline with the clustered index, the benefits and the limits.
- [[MongoDB Internals]] — Course notes arguing all databases share a frontend/storage-engine split, applied to MongoDB's internals.
- [[MyISAM]] — Course notes on the MyISAM engine: index-everything design, no transactions, table-level locking and its reliability problems.
- [[SQLite]] — Course notes on SQLite as an embedded storage engine: its history, architecture, features and where it is the right choice.

## Related hubs
[[MongoDB]], [[MySQL]], [[Database Indexing]], [[SQLite]], [[System Design]], [[Caching]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
