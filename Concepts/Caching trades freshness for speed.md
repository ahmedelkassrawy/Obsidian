---
description: "A cache is a fast copy of slow data; the price is that the copy can go stale, so every caching design is really a choice about how much staleness you accept."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/caching
hubs:
  - "[[Caching]]"
created: 2026-10-01
---
# Caching trades freshness for speed

## The idea
A cache keeps a copy of data somewhere faster than where it really lives: memory instead of disk, a nearby server instead of a far one, a saved answer instead of a recomputed one. Reads get much faster. The catch is that the original can change while the copy doesn't, so the cache can hand back old data.

Every caching decision is about that trade-off. A TTL says "stale for at most N seconds is fine". Write-through says "never stale, but every write is slower". Invalidation on write says "stale only until I remember to clear it", which is where most cache bugs live.

## Example
A product page is cached in Redis for 60 seconds. Prices change rarely, so 60 seconds of staleness is fine. Stock count changes every sale, so caching it the same way would show "in stock" for items that just sold out. Same system, two different freshness budgets.

## Connects to
- [[Prompt caching only pays off when the prefix stays identical]] — the same idea applied to LLM prefill: reuse work you already did, as long as the input hasn't changed.
- [[Replication scales reads, sharding scales writes]] — a read replica is a cache that the database keeps in sync for you, and it has the same stale-read problem.
- [[Indexes speed up reads by slowing down writes]] — both spend extra space and write-time work to make reads cheap.

## Sources
- [[Caching]]
- [[Caching - Capacity Estimation and Strategies]]
- [[Memcached]]

## 30-second answer
> A cache stores a copy of slow data somewhere fast. You gain read speed but risk serving stale data, so the real design question is how stale is acceptable for this data. That picks your strategy: TTL, write-through, or invalidate on write.
