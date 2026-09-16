---
tags: [backend, system-design, caching, redis, cache-aside, invalidation]
domain: backend
type: lesson-note
status: digested
source: System Design Primer — Phase 4 (Caching); Kassra growth-track session 2026-09-16
---
# Caching

One rule underneath everything: **a cache trades freshness for speed.** You keep a copy of data somewhere faster/closer than the source, and accept it might go stale. The whole phase is *where* you cache and *which write pattern* you pick.

## Where caches live (the layers)

A request passes through many cache opportunities — from user to DB:

| Layer | Caches what | Example |
|---|---|---|
| **Client** | responses in the browser | HTTP cache headers |
| **CDN** | static assets at the edge | Cloudflare (Phase 2) |
| **Web server** | rendered pages / responses | nginx cache |
| **Application** | hot objects / query results | **Redis** in front of your DB |
| **Database** | its own query/buffer cache | Postgres internal |

The one you *design* is usually the **application cache** (Redis in front of the DB). That's where the patterns below apply.

## The core idea

> [!definition] Cache hit / miss
> **Hit** = data is in the cache → fast, DB untouched.
> **Miss** = not there → fetch from DB, (usually) store it, return it.
> Cache value = **hit rate**. A cache with a 5% hit rate is just overhead.

## The four patterns

### 1. Cache-aside (lazy loading) — the default
Your app manages the cache.

```text
read:  check cache → HIT?  return it
                   → MISS? read DB → write to cache → return
write: write to DB → delete/invalidate the cache key
```

- **You already built this** — rag-prod's Redis BM25 cache is cache-aside.
- **Pro:** only requested data is cached (no waste); cache failure ≠ app failure (falls back to DB).
- **Con:** first read is always a miss (cold cache); risk of stale if a write doesn't invalidate.

### 2. Write-through — write to cache and DB together, synchronously
- Every write goes to the cache *and* the DB before returning.
- **Pro:** cache is never stale (always matches DB).
- **Con:** slower writes (two writes every time); you cache data that may never be read.

### 3. Write-behind (write-back) — write to cache now, DB later (async)
- Write hits the cache and returns immediately; a background job flushes to the DB.
- **Pro:** very fast writes, absorbs bursts.
- **Con:** **data loss risk** — if the cache dies before the flush, those writes are gone. Only for data you can afford to lose.

### 4. Refresh-ahead — predict and pre-load before expiry
- The cache proactively refreshes popular keys *before* they expire, so hot data never causes a miss.
- **Pro:** low latency on predictable hot keys.
- **Con:** wasted work if your prediction is wrong.

## The hard part: invalidation

> [!warning] "There are only two hard things in CS: cache invalidation and naming things."
> A cache is a *copy*. The moment the source changes, the copy is a lie until you fix it. That's invalidation — the source of most cache bugs.

Three ways to invalidate:
- **TTL (expiry)** — every key auto-dies after N seconds. Simple, but you serve stale data for up to N seconds. (Your rate-limiter Redis keys used this — `EXPIRE ~2 min`.)
- **Write-invalidate** — on a write, delete the key so the next read re-fetches fresh. (Cache-aside does this.)
- **Write-update** — on a write, overwrite the cached value directly. (Write-through does this.)

> [!tip] The through-line
> **Pick the pattern from the read/write mix + how much staleness you can tolerate.**
> - Read-heavy + some staleness OK → cache-aside + TTL (the 90% answer).
> - Can't ever be stale → write-through.
> - Write-burst + loss-tolerant → write-behind.

## Gate 4 (passed 2026-09-16)

**Scenario:** raaaaag's `search_docs` is **read-heavy** — the same popular queries hit it over and over, and the docs change **rarely** (an ingest now and then).

### Q1 — pattern + placement
**Cache-aside, Redis in front of the DB.** The textbook match for read-heavy + rarely-changing (exactly rag-prod's Redis BM25 cache).

### Q2 — invalidate on a new ingest, and the trade-off
Write-invalidate = delete the key so the next read is fresh. Correct mechanism, but:

> [!warning] The blunt-invalidation problem
> A new document can affect **many different search queries** — and you *can't know which cached queries it changes*. So write-invalidate here isn't "delete one key," it's "flush a lot of keys (often all search keys)" on every ingest. Blunt, and it throws away good entries too.

The real trade-off for this case:
- **Write-invalidate** → always fresh, but each ingest nukes a big chunk of the cache (cold-cache hit right after) and you need logic to know what to clear.
- **TTL** → dead simple, no tracking, self-heals; cost = results can be stale for up to N seconds/minutes.

> [!note] The senior call
> Since docs change **rarely** and search staleness is harmless, **TTL is the cleaner pick here** (or TTL + a full flush on the occasional ingest). You don't need precise invalidation when "stale for a few minutes" costs nothing — and naming *why precise invalidation isn't worth it* is the move.

> [!success] Phase 4 done
> Own: the cache layers, the 4 write patterns, cache-aside as the default, the 3 invalidation strategies, and why invalidation is the hard part. **Next: Phase 5 — asynchronism & communication (message/task queues, back pressure, retries + idempotency, REST vs RPC, TCP vs UDP). Anchor = Temporal + Shutterabia scheduler/retry/HMAC.**
