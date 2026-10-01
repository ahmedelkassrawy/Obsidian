---
description: "An index is an extra sorted structure the database keeps up to date, so lookups skip the full table scan but every insert and update pays to maintain it."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/database-indexing
hubs:
  - "[[Database Indexing]]"
created: 2026-10-01
---
# Indexes speed up reads by slowing down writes

## The idea
Without an index, finding rows means reading the whole table (a sequential scan). An index, usually a B-tree, keeps the column's values sorted with pointers back to the rows, so the database can jump straight to what it needs.

The cost shows up on writes. Every INSERT, UPDATE or DELETE must also update every index on that table, and each index takes disk space. So you index columns you filter or join on often, not every column "just in case".

A covering index (with INCLUDE columns) goes one step further: if every column the query needs is in the index, Postgres can answer from the index alone (an index-only scan) without touching the table.

## Example
`WHERE email = ?` on a 10M-row users table: a seq scan reads every row, a B-tree index on email reads a handful of pages. On a write-heavy log table, five indexes can make inserts noticeably slower.

## Connects to
- [[Exact nearest-neighbour search doesn't scale, so vector databases approximate]] — vector indexes like HNSW are the same deal: build cost and memory up front, fast lookups later.
- [[Caching trades freshness for speed]] — both spend space and write-time work so reads get cheap.
- [[Locks trade concurrency for correctness]] — a missing index can make an UPDATE lock far more rows than it needs to.

## Sources
- [[Index Scan vs Index Only Scan]]
- [[PostgreSQL Scan Types Comparison]]
- [[Key vs Non-Key Column Indexes]]
- [[PostgreSQL EXPLAIN ANALYZE Notes]]

## 30-second answer
> An index is a sorted side-structure, usually a B-tree, that lets the database find rows without scanning the whole table. Reads get much faster, but every write has to update the index too and it costs storage. So you index what you filter and join on, and check with EXPLAIN ANALYZE that it's actually used.
