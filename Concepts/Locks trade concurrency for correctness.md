---
description: "Race conditions happen when two operations read-then-write the same data; locks fix it by making one wait, and the art is locking as little as possible for as short as possible."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/transactions-concurrency
  - topic/database-internals
hubs:
  - "[[Transactions & Concurrency Control]]"
created: 2026-10-01
---
# Locks trade concurrency for correctness

## The idea
A race condition happens when two operations both read a value, both decide based on it, and both write. One of the writes silently wins. The fix is to make them take turns, which is what a lock does. Taking turns means less concurrency, so locking is always a trade-off.

Databases offer two kinds. Shared locks let many readers in together. Exclusive locks let one writer in alone. Holding locks too long or grabbing them in different orders leads to deadlocks. Two-phase locking (acquire everything, then release) guarantees a correct result, at the cost of more waiting.

Often the cheapest fix is to skip the read-then-write. A single conditional `UPDATE ... WHERE seats > 0` is atomic by itself.

## Example
Double booking: two users read "seat 12A free" and both book it. Fixes: `SELECT ... FOR UPDATE` to lock the row while deciding, or one conditional UPDATE that only succeeds if the seat is still free.

## Connects to
- [[Async helps with waiting, not with computing]] — overlapping tasks need coordination even on one thread.
- [[Indexes speed up reads by slowing down writes]] — without an index on the WHERE column, the database may lock far more rows than it needs to.
- [[Replication scales reads, sharding scales writes]] — once writes happen in several places, you need conflict resolution instead of locks.

## Sources
- [[Concurrency]]
- [[Exclusive Lock VS Shared Lock]]
- [[Two Phase Locking]]
- [[Double Booking Prevention]]
- [[High Performance MySQL - Architecture, Locking and Transactions]]

## 30-second answer
> A race condition is two operations reading and writing the same data and stepping on each other. Locks make them take turns: shared for reads, exclusive for writes. You trade throughput for correctness, so you lock as little as possible, or use one atomic conditional UPDATE so you don't need a separate lock.
