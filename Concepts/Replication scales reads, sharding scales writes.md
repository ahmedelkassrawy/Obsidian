---
description: "Replication copies the whole dataset to more machines so reads spread out; sharding splits the dataset so writes spread out, and each brings its own new problem."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/replication-sharding
  - topic/system-design
hubs:
  - "[[Database Replication & Sharding]]"
  - "[[System Design]]"
created: 2026-10-01
---
# Replication scales reads, sharding scales writes

## The idea
When one database server isn't enough, you have two different tools, and they fix different bottlenecks.

**Replication** copies all the data to several servers. With a single leader, writes still go to one place, but reads can go to any follower. That scales reads. The new problem is lag: with async replication, a follower can be behind, so a user might not see the change they just made (a stale read).

**Sharding** splits the data so each server owns a slice (by user id, say). Writes for different slices land on different machines, so writes scale. The new problems are picking a shard key, queries that span shards, and moving data when you add servers. Consistent hashing exists to keep that last one cheap: adding a node moves only a small share of keys instead of reshuffling everything.

## Example
A read-heavy blog: add read replicas. A chat app with huge write volume: shard by conversation id. Large systems usually do both, sharding for writes and replicas of each shard for reads and failover.

## Connects to
- [[Caching trades freshness for speed]] — a read replica is a managed cache of the leader, and it brings the same staleness problem.
- [[Locks trade concurrency for correctness]] — multi-leader setups lose the single place where conflicting writes get ordered, so conflicts move into the application.

## Sources
- [[Single-Leader Replication]]
- [[Multi-Leader Replication]]
- [[Stale Reads in Replicated Databases]]
- [[Consistent Hashing]]
- [[CAP Theorem]]
- [[Horizontal vs Vertical Scaling]]

## 30-second answer
> Replication copies all the data so you can spread reads across followers, at the cost of possible stale reads from lag. Sharding splits the data across machines so writes spread out, at the cost of shard-key choice and cross-shard queries. Read-heavy load means replicate, write-heavy load means shard, and big systems do both.
