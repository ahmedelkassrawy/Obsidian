---
description: "Hub: every note about Database Replication & Sharding"
type: hub
domain: backend
tags:
  - type/hub
  - topic/database-replication-and-sharding
---
# Database Replication & Sharding

> [!info] Single-leader, multi-leader, stale reads, partitioning, consistent hashing, CAP. Missing: a real failover runbook.
> Part of [[MOC - Backend]]. Also try the tag `#topic/database-replication-and-sharding`.

## Concepts
- [[Consistent Hashing]] — Explains the consistent hashing ring, the rebalancing problem it solves, and how to present it in a system design interview.
- [[DB Replications]] — Compares master/backup and multi-master replication, synchronous vs asynchronous, and the trade-offs of each including eventual consistency.
- [[Horizontal vs Vertical Scaling]] — Compares scaling up and scaling out, when each applies, and how both play out specifically for databases.

## How-tos & recipes
- [[PostgreSQL Partitioning]] — Step-by-step PostgreSQL range partitioning: parent table, child partitions, attaching them, querying and indexing.
- [[Sharding]] `raw` — Pasted SQL and Docker commands for spinning up two PostgreSQL shards behind a hash-based URL table.

## Course notes
- [[CAP Theorem]] — Course notes on the CAP theorem: the three properties, why partition tolerance is not optional, and the AP/CP design choice.
- [[Multi-Leader Replication]] — Course notes on multi-leader replication: multi-datacenter setups, the replication loop problem and write conflict resolution.
- [[Single-Leader Replication]] — Course notes on single-leader replication: how reads and writes flow, its advantages, and follower/leader failure scenarios.
- [[Stale Reads in Replicated Databases]] — Course notes on stale reads under async replication and the fixes: read-your-own-writes, consistent prefix and monotonic guarantees.

## Related hubs
[[System Design]], [[Postgres]], [[Caching]], [[Docker]]

## Notes to self (from the audit)
- [[Sharding]]: Code-only - no explanation of the shard key choice or routing logic.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
