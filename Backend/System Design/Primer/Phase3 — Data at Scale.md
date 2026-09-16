---
tags: [backend, system-design, database, replication, sharding, sql, nosql, scaling]
domain: backend
type: lesson-note
status: digested
source: System Design Primer — Phase 3 (Data at Scale); Kassra growth-track session 2026-09-16
---
# Data at Scale

The whole phase answers one question: **your single database is the bottleneck (proved in Phases 0–1). What do you do, and in what order?**

The tools escalate from cheap-and-easy to expensive-and-painful. **Always try them in this order** — never shard when an index would do.

## The escalation ladder

```text
1. Index        → make existing queries faster (cheapest)
2. Replication  → spread READS across copies
3. Federation   → split by feature into separate DBs
4. Sharding     → split ONE table across machines (most painful)
5. Denormalize  → trade storage + write-cost for read speed
```

## 1. Indexing — always first

> [!definition] Index
> A lookup structure (usually a B-tree) that lets the DB jump to matching rows instead of scanning the whole table.

- **Trade-off:** faster reads, **slower writes** (every write must update the index too), more storage.
- You already met this:
  - raaaaag's `short_code` index in the URL shortener.
  - the **HNSW index** on pgvector — an index built for *vector similarity* search instead of exact match.
- **Rule:** index the columns you filter/join on. Don't index everything — each index taxes every write.

## 2. Replication — copy the DB, spread reads

> [!definition] Replication
> Keep multiple copies of the same DB. One **primary** takes writes; **replicas** copy from it and serve reads.

- **Why:** most systems are **read-heavy** (the URL shortener was ~100:1 reads:writes). Replicas absorb the read flood; the primary only handles writes.
- **Two shapes:**
  - **Master–slave (primary–replica):** one writer, many readers. Simple. If the primary dies, a replica gets promoted.
  - **Master–master (multi-primary):** multiple writers. More availability, but two nodes can edit the same row → **conflict resolution** headache.
- **The cost you already know:** **replication lag** — a replica is slightly behind → eventual consistency (Phase 1). This is exactly the Shutterabia D1 mirror.

## 3. Federation — split by feature

> [!definition] Federation
> Split one big DB into several smaller DBs **by function** — e.g. a `users` DB, a `posts` DB, an `analytics` DB.

- **Why:** each DB is smaller, gets its own hardware, and writes to different features don't compete for the same lock.
- **Cost:** a query that needs data from two features now has to **join across DBs** in your app code — the DB can't do it for you.
- **Shutterabia angle:** split the heavy `analytics` tables away from the live `posts`/`drafts` tables so a big analytics query never slows down publishing.

## 4. Sharding — split one table across machines

> [!definition] Sharding
> Split the rows of a *single* huge table across multiple machines by a **shard key** — e.g. users A–M on shard 1, N–Z on shard 2.

- **Why:** when one table is too big for any single machine (billions of rows), replication won't help — every copy is still too big. You must split the *data itself*.
- **This is the painful one. The costs:**
  - **Cross-shard queries break** — "count all users" must hit every shard and merge. Joins across shards are ugly.
  - **Rebalancing** — add a shard and you must move data around (a huge operation).
  - **Hot shards** — a bad shard key (e.g. shard by date) sends all today's traffic to one shard. Pick a key that spreads load *evenly*.
- **This is the raaaaag "10× point"** — from the M5 case study, when pgvector outgrows one box you shard the vector table by tenant/collection.

## 5. Denormalization — duplicate to avoid joins

> [!definition] Denormalization
> Deliberately store redundant copies of data so a read doesn't need an expensive join.

- **Normalized** = each fact stored once (clean, but reads need joins).
- **Denormalized** = copy the fact into the tables that read it (fast reads, but a write must update every copy).
- **Trade-off:** faster reads, **harder writes + risk of copies drifting out of sync.** Worth it when reads massively outnumber writes.

## SQL vs NoSQL — the "which database" call

> [!definition] SQL vs NoSQL
> **SQL** (relational): structured tables, strict schema, ACID transactions, joins.
> **NoSQL**: flexible schema, built to scale horizontally, usually gives up joins + strong consistency for speed and scale.

The four NoSQL families (know one line each):

| Family | Shape | Use for |
|---|---|---|
| **Key-value** | a giant dict (Redis) | caches, sessions, counters |
| **Document** | JSON blobs (MongoDB) | flexible/nested records |
| **Wide-column** | rows with huge dynamic columns (Cassandra) | massive write volume, time-series |
| **Graph** | nodes + edges (Neo4j) | relationships (social, recommendations) |

**When to pick which:**
- **SQL** when you need **transactions, joins, and consistency** — money, orders, anything relational. (Shutterabia's SQLite/D1: relational, ACID, correct choice.)
- **NoSQL** when you need **massive scale or flexible schema** and can live with eventual consistency + no joins — logs, feeds, huge key lookups.

> [!tip] The interview line
> "Start with SQL. Move to NoSQL only when a specific scale or schema-flexibility need forces it." Reaching for NoSQL by default is a red flag.

## Gate 3 

### Q1 — Shutterabia `posts`/`drafts`, read-heavy, modest writes, getting slow

Index first. Then the key move for a **read-heavy** table is **replication** — read replicas absorb the dashboard's constant reads while the primary handles the modest writes (read-heavy → replicas). Federation is a *later/different* tool (split features apart), fine to mention but not the main lever here.

> [!note] Say it out loud
> **No, don't jump to sharding.** Sharding is only for when one table is too big for any single machine. Here writes are modest and the table fits on one box → sharding's pain (cross-shard queries, rebalancing) buys nothing. **Naming why you're NOT using a tool is worth as much as picking the right one.**

### Q2 — raaaaag vector table grows to 500M chunks across tenants

Shard key = **tenant/collection**. Two real costs:
- **counting** → a "how many chunks total?" query must hit **every shard and merge** (cross-shard aggregation).
- **rebalancing** → adding a shard means physically moving data around.

> [!warning] Hot shard
> Sharding by tenant risks a **hot shard** — one giant tenant alone on shard 3 melts that box while others idle. The fix: shard by a *finer, more even* key (e.g. `hash(tenant_id + collection_id)`) so load spreads evenly. Naming the hot-shard risk is the senior move.

> [!success] Phase 3 done
> Own: the escalation ladder (index → replicate → federate → shard → denormalize), the "don't shard early" judgment, SQL-vs-NoSQL + the four families, and the hot-shard trap. **Next: Phase 4 — caching (layers + cache-aside/write-through/write-behind/refresh-ahead; invalidation is the hard part).**
