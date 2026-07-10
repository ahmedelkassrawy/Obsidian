# Caching – System Design Series

> [!info] Source
> [YouTube – Musab Khunaijir](https://www.youtube.com/watch?v=IaYr-_FhNDQ)  
> **Lecture #3** of the System Design Series  
> Presented by: [[Musab Khunaijir]] & Abu Bakr  
> *“In this lecture we talked about caching and everything related to it, starting with its definition and the benefits we can get from using it. Then we discussed different caching strategies and the trade-offs related to each. We also learned about eviction policies and how they work. One of the most important topics is cache invalidation – we all know the famous quote: ‘There are only two hard things in software engineering: cache invalidation and naming things.’ Finally, we learned when to use caching in the first place – you can’t solve every problem by throwing caching at it.”*

---

## Table of Contents

1. [Introduction: The Growing E‑Commerce System](#1-introduction-the-growing-ecommerce-system)
2. [A Request Journey Through the System](#2-a-request-journey-through-the-system)
3. [How to Think About Database Capacity](#3-how-to-think-about-database-capacity)
4. [What is Caching?](#4-what-is-caching)
5. [Caching Strategies](#5-caching-strategies)
   - [Cache‑Aside (Lazy Loading)](#51-cacheaside-lazy-loading)
   - [Read‑Through](#52-readthrough)
   - [Write‑Through](#53-writethrough)
   - [Write‑Behind (Write‑Back)](#54-writebehind-writeback)
6. [Cache Eviction Policies](#6-cache-eviction-policies)
   - [Time‑To‑Live (TTL)](#61-timetolive-ttl)
   - [Least Recently Used (LRU)](#62-least-recently-used-lru)
   - [Least Frequently Used (LFU)](#63-least-frequently-used-lfu)
   - [FIFO & Random](#64-fifo--random)
7. [Cache Invalidation](#7-cache-invalidation)
   - [Explicit Invalidation on Write](#71-explicit-invalidation-on-write)
   - [Write‑Through Invalidation](#72-writethrough-invalidation)
   - [Version Keys](#73-version-keys)
   - [Event‑Based Invalidation](#74-eventbased-invalidation)
8. [Serious Cache Problems](#8-serious-cache-problems)
   - [Cache Stampede (Thundering Herd)](#81-cache-stampede-thundering-herd)
   - [Cache Penetration](#82-cache-penetration)
   - [Cache Avalanche](#83-cache-avalanche)
   - [Stale Data & Consistency](#84-stale-data--consistency)
   - [Hot Key Problem](#85-hot-key-problem)
9. [When to Introduce Caching? Why Not Just Scale?](#9-when-to-introduce-caching-why-not-just-scale)
10. [Essential Metrics for Caching](#10-essential-metrics-for-caching)
11. [Questions & Extra Tips](#11-questions--extra-tips)
12. [Summary & Takeaways](#12-summary--takeaways)

---

## 1. Introduction: The Growing E‑Commerce System

Imagine our simple e‑commerce system from the previous session: one application server and one database.  
For a while everything was smooth – pages loaded in ~100 ms, users were happy.

Then the business took off. New marketing campaigns, investors, and a sudden spike in traffic.  
Suddenly the **homepage** – which shows books by category and best‑sellers – tanked. A query that used to take **50 ms** now takes **2.5 seconds**.

> [!warning] Bottleneck Identified  
> After checking all components, we discovered that the **database** had become the bottleneck.  
> The application server was fine, but the DB query latency had exploded.

This is the most common first bottleneck in any growing system – the database always breaks first.

---

## 2. A Request Journey Through the System

Let’s trace what happens to a single request when it hits our server:

1. **Parsing**: HTTP headers, cookies, body → ~5 ms
2. **Deserialization**: map to internal data structures → ~10 ms
3. **Middleware & Filters**: authentication, logging, etc. → ~10 ms
4. **Business Logic** → variable time
5. **Database Query** → originally 50 ms, now 2 s
6. **Serialization** (usually to JSON) → ~5 ms
7. **Response Transmission** → ~5 ms

Adding all up (with the original 50 ms DB) gave roughly 100 ms.  
Now the DB alone takes 2000 ms, pushing the total over 2.5 s.

Since the DB is the only part that changed dramatically, it’s the **throat of the bottle**.

---

## 3. How to Think About Database Capacity

How do we quantify how much load a database can handle? Two common mindsets:

### 3.1 Hardware‑First Estimation
Used by cloud architects and DevOps – stress‑test the actual hardware: fix CPU cores, RAM, disk, then vary request rates and measure. This is extremely detailed and expensive.

### 3.2 Query‑First Estimation (Rule of Thumb)
Most of the time we have a running system and we just need a quick feel for its limits.

**The Formula** (popularized by TimescaleDB):

$$
\text{QPS} \approx \frac{1}{\text{avg query time (seconds)}} \times \text{Number of CPU cores}
$$

> [!example] Applying the Formula
> **Before the spike:**
> - Avg query time = 0.05 s (50 ms)
> - 8 cores → QPS ≈ (1 / 0.05) × 8 = **160 queries/sec**
> 
> Our estimated traffic was well under 100 QPS → the server was comfortable.
> 
> **After the spike:**
> - Avg query time = 2 s
> - 8 cores → QPS ≈ (1 / 2) × 8 = **4 queries/sec**
> 
> Even if the database could theoretically serve 4 QPS, any burst would kill it.

> [!note] Important Caveats
> - The formula assumes the CPU is the bottleneck. In databases, the **disk** is often the slowest part.
> - It gives you a **feel**, not an exact plan – just like a carpenter’s thumb.
> - Real capacity depends on query types (full scans vs. index seeks), indexing, etc.

---

## 4. What is Caching?

> [!quote] The Chef Analogy
> A chef doesn’t walk to the warehouse across the street every time an order comes in.  
> He keeps a stock of 100 chickens next to him in the kitchen.  
> Even better, he has them pre‑cut and pre‑marinated from a nearby supplier.  
> That’s caching – storing what you need close to where you need it, in a form that’s faster to use.

Caching is the **temporary storage** of the result of an expensive operation so that future requests can be served faster.

- **Expensive operation** could be a heavy DB query, an external API call (with money cost), or CPU‑intensive computation.
- **Storage** is almost always **memory** (RAM) because a memory read is ~**160× faster** than a disk read.

In our system, we insert a cache layer between the application and the database.  
The cache is essentially a **key‑value store** (hash table, dictionary, Redis, etc.).

```
Request → Check Cache → HIT → return data
                ↓ MISS
           Database → store in cache → return data
```

> [!tip] Caching is Everywhere
> - **CPU** has L1, L2, L3 caches
> - **Disk** has internal buffers
> - **DNS** caches resolved IPs
> - **CDN** caches static assets near users
> - **Application** caches function results (memoization)
> 
> In system design, we usually mean **application‑level caching** (like Redis) to shield the database.

---

## 5. Caching Strategies

The strategy answers two questions:
1. **Where does a READ come from?**
2. **How do WRITEs propagate to the cache and the database?**

### 5.1 Cache‑Aside (Lazy Loading)

The most common and the first one that comes to mind.

- **Read:**  
  Application checks the cache.  
  → **Hit:** return immediately.  
  → **Miss:** query the database, write the result to the cache, then return.
- **Write:**  
  Write directly to the database.  
  **Invalidate** (or update) the corresponding cache entry.

**Pros:**
- You only cache what’s actually requested.
- Simple to understand and implement.

**Cons:**
- Code clutter – you have to write the “check → DB → cache” logic everywhere.
- If the cache is changed (e.g., from Redis to Memcached), you need to update all touchpoints unless you have good abstraction.

**Diagram:**
```
READ:
  App → Cache (miss) → DB → Store in Cache → return

WRITE:
  App → DB (update) → Invalidate Cache
```

### 5.2 Read‑Through

The cache sits **in front** of the database.  
The application only talks to the cache; the cache is responsible for fetching from the database on a miss.

- **Read:** App → Cache (miss) → Cache fetches from DB → Cache returns data to App.
- **Write:** Typically still goes directly to the DB, but invalidation must happen through the cache layer.

**Pros:**
- Clean code – the app only sees one interface (the cache).
- Easier to change the cache implementation behind that interface.

**Cons:**
- You need a cache library/framework that supports this pattern (not always trivial to build yourself).

### 5.3 Write‑Through

Every write is applied to **both** the cache and the database simultaneously.

- **Write:** App → Cache + DB (both updated).
- **Read:** Always from the cache (data is always fresh).

**Pros:**
- **Cache is always consistent** with the database. No stale data.

**Cons:**
- Every write now does double work (cache + DB). While cache writes are fast, you still have the latency of two separate operations.
- You store **everything** in the cache, not just the frequently accessed “hot” data. This consumes memory quickly.

### 5.4 Write‑Behind (Write‑Back)

Writes go **only** to the cache first. The cache then asynchronously flushes the writes to the database later.

- **Write:** App → Cache (fast, in‑memory). Cache queues the write to the DB.
- **Read:** Always from the cache.

**Pros:**
- **Extremely fast writes** – near‑instant since they’re just memory writes.
- Good for write‑heavy workloads that can tolerate eventual consistency.

**Cons:**
- **Data loss risk** – if the cache server crashes before flushing to the DB, those writes are gone forever.
- Complexity in managing the flush queue and handling failures.

> [!example] Use Case for Write‑Behind
> **Analytics & metrics** – you want to log millions of events quickly; losing a tiny fraction is acceptable.

> [!summary] Strategy Comparison
> | Strategy | Read Source | Write Path | Consistency | Complexity |
> |----------|-------------|-------------|-------------|------------|
> | Cache‑Aside | App logic | DB → invalidate cache | Strong (if invalidation done right) | Low |
> | Read‑Through | Cache proxy | DB (through cache) | Strong | Medium |
> | Write‑Through | Cache | Cache + DB | Excellent | Low |
> | Write‑Behind | Cache | Cache first, DB async | Eventual | High |

---

## 6. Cache Eviction Policies

Since memory is limited, we must evict old data to make room for new data.  
Eviction is **automatic** (unlike manual invalidation).

### 6.1 Time‑To‑Live (TTL)
Every cache entry gets an expiration time (e.g., 2 minutes, 1 hour).  
After that time, the entry is automatically deleted.

- Most common and sufficient for many use cases.
- Prevents stale data from sitting forever.

### 6.2 Least Recently Used (LRU)
Evicts the data that hasn’t been accessed for the longest time.  
Based on **recency** of access.

- Good for data with temporal locality (recently accessed items are likely to be accessed again).

### 6.3 Least Frequently Used (LFU)
Evicts the data with the **lowest access frequency** overall.

- A small, constantly accessed item stays; a one‑time accessed item gets evicted even if it was recent.

### 6.4 FIFO & Random
- **FIFO** (First‑In‑First‑Out): behaves like a queue; oldest entry evicted first.
- **Random**: picks an entry at random – surprisingly effective in some benchmarks.

> [!tip] In Practice
> Most teams start with **TTL**. It’s predictable and simple.  
> LRU is often built into caching tools like Redis when `maxmemory` is set.

---

## 7. Cache Invalidation

> [!quote] “There are only two hard things in Computer Science: cache invalidation and naming things.”
> — Phil Karlton

Invalidation means **clearing cached data that is no longer valid**.

### 7.1 Explicit Invalidation on Write
When you update the database, you **manually** delete (or update) the relevant cache key.

- Most straightforward.
- Downside: you must remember to do it everywhere a write occurs – easy to miss.

### 7.2 Write‑Through Invalidation
When using the Write‑Through strategy, the cache is updated directly, so the old data is replaced automatically.

### 7.3 Version Keys
Instead of storing `book:42`, store `book:42:v2`.  
When the data changes, you increment the version. A read will check the latest version; if the cached version doesn’t match, it’s considered invalid.

- Avoids explicit delete calls, but you must maintain a versioning layer.

### 7.4 Event‑Based Invalidation
Publish an event (e.g., `BookUpdated`) to a message broker.  
The cache subscribes to these events and invalidates the relevant entries.

- Decouples the write service from the cache logic.
- Requires an event‑driven architecture.

> [!warning] Invalidation is Hard
> - If you forget to invalidate, users see **stale data**.
> - If you invalidate too aggressively, you lose the performance benefit.
> - Cached data is **not** the source of truth – the database is.

---

## 8. Serious Cache Problems

### 8.1 Cache Stampede (Thundering Herd)

Imagine a popular cache key expires.  
At that exact moment, **10 million concurrent requests** arrive.  
They all see a cache miss and **all surge to the database** at once – potentially crushing it.

**Solution: Mutex Lock**  
When a key is missing, only one request is allowed to rebuild the cache (fetch from DB and store).  
All other requests wait (block) until that one finishes, then read the freshly cached value.

- A standard pattern using a distributed lock (e.g., Redlock in Redis).

### 8.2 Cache Penetration

When an attacker (or a buggy script) requests a key that **doesn’t exist in the database at all** (e.g., `book:9999999`).  
Every request bypasses the cache (miss) and hits the database.

**Solution:** Cache the “null” or “not_found” result for a short TTL. This way the DB is shielded from repeated requests for nonexistent data.

### 8.3 Cache Avalanche

A large number of different keys all expire **around the same time** (e.g., they were all cached at startup with the same TTL).  
The database suddenly receives a flood of requests for all those keys simultaneously.

**Solutions:**
- Add a **random jitter** to expiration times (± some percentage).
- Use a **staggered** TTL strategy.

### 8.4 Stale Data & Consistency

The cache and the database may diverge.  
This is inevitable unless you use write‑through or immediate invalidation.  
In many systems, **eventual consistency** is acceptable (e.g., a price might be a few seconds old).  
You must decide based on business requirements.

### 8.5 Hot Key Problem

One particular cache key receives a **disproportionate** amount of traffic (e.g., a superstar product).  
In a distributed cache cluster, that single node housing the hot key may become overloaded while other nodes idle.

**Mitigations:**
- **Replicate** the hot key across multiple cache nodes.
- Use client‑side local caching for the most extreme cases.
- Intelligent hashing that distributes reads.

---

## 9. When to Introduce Caching? Why Not Just Scale?

> [!question] “If my database is slow, why not just scale it up (vertical) or add replicas (horizontal)?”

**Scaling adds capacity, but it does not reduce the work.**  
If a query takes 2 s, making a bigger machine might help a bit, but you still have 2 s queries running.

**Caching reduces the work itself** – it avoids the heavy query entirely.

**Rule of thumb:**
1. First, **optimize your database**: proper indexing, query tuning, connection pooling.  
2. If that’s not enough, **cache the hot, relatively static** data.  
3. Only after caching is insufficient or inappropriate, consider heavy scaling (horizontal scaling brings its own complexity – replication, sharding, distributed caches).

> [!example] The Decision Framework
> - **Data rarely changes** (e.g., product catalog, best‑sellers of the day) → **cache.**
> - **Data per‑request is unique** (e.g., real‑time personalized calculations) → **scale your compute/database.**

> [!danger] Cache is NOT a Silver Bullet
> Adding a cache introduces complexity, invalidation logic, and new failure modes (stampede, stale data).  
> Always monitor your cache hit rate and DB load to confirm it’s helping.

---

## 10. Essential Metrics for Caching

You cannot improve what you don’t measure. Keep an eye on:

| Metric | What it tells you |
|--------|-------------------|
| **Cache Hit Rate** | `hits / (hits + misses)` → a high hit rate means your caching strategy is working. |
| **Cache Miss Rate** | `misses / (hits + misses)` → if high, review what you’re caching and how often. |
| **Cache Latency** | How long a cache read takes (usually sub‑millisecond). |
| **DB Load** | Queries per second, average query time, CPU/RAM/Disk usage on the database. Must drop after caching. |
| **Cache Size** | Memory footprint. Watch for near‑limit usage. |
| **Evictions** | Rate of items being evicted. A spike may indicate insufficient memory or bad TTL. |
| **P99 / P50 Latency** | Tells you worst‑case and median user experience. A high P99 usually means the DB was hit. |

> [!tip] Observability Tools
> Use **OpenTelemetry**, **Prometheus**, **Datadog**, or structured logging (Serilog for .NET) to track these automatically per endpoint.

---

## 11. Questions & Extra Tips

### 11.1 How to Pinpoint a Bottleneck?
Use distributed tracing (e.g., Jaeger, Zipkin) or structured logging that records timestamp of each step (deserialization → business logic → DB query → serialization).  
That way you can see exactly which leg of the journey took the most time.

### 11.2 Should I Always Optimize the DB First?
Yes. Before adding caching, exhaust all DB optimization: proper indexes, avoiding N+1 queries, using `EXPLAIN`, avoiding Cartesian explosions, connection pooling.  
Then move to caching if the hot data is read‑heavy and doesn’t change frequently.

### 11.3 Cache is NOT the Source of Truth
The **database** is the single source of truth. The cache is a **disposable performance layer**.  
If the cache server restarts, the application must survive and re‑populate from the DB.  
Never design a system where the cache is the only durable store.

### 11.4 Data Format in Cache?
Does the data type (string, binary, JSON, Protobuf) affect performance?  
- **Size** definitely matters – larger payloads fill memory faster and increase network transfer time.
- Binary formats like Protobuf can be more compact than JSON.
- But from a conceptual caching point of view, the strategy doesn’t change – it’s just a key‑value store.

### 11.5 Personalized Content and Cache Security
User‑specific data (e.g., personalized recommendations) is harder to cache because the content differs per user.  
- You can still cache fragments (e.g., pre‑computed models) and compose them with user context.
- Be cautious of **data leakage** – never cache user‑private data in a shared cache without proper isolation (e.g., use a cache key that includes the user ID, but ensure that key is not guessable).

### 11.6 Horizontal Scaling and Caching
When you scale your application horizontally, each instance has its own local memory cache.  
- **Problem:** A user’s earlier request may have been served by Instance A (which cached the data), but the next request is routed to Instance B (which doesn’t have the data).
- **Solution:** **Distributed Cache** (Redis, Memcached) – external to the instances, shared, and consistent.  
  (Discussion reserved for the upcoming session on Horizontal Scaling.)

---

## 12. Summary & Takeaways

1. **Caching is not a magic wand** – it adds complexity and new failure modes. Use it deliberately.
2. **Cache‑Aside** is the most common pattern: check cache, on miss fetch from DB and store.
3. **TTL** is the simplest eviction policy; combine it with manual invalidation for updated data.
4. **Cache Stampede, Penetration, and Avalanche** are real threats – plan for them with mutex locks, negative caching, and TTL jitter.
5. **Metrics are mandatory** – hit rate, DB load, and latency tell you if caching is working.
6. **Caching complements scaling**, not replaces it. Always optimize the DB first, then cache the hot spot, then scale if needed.
7. **The database is the source of truth** – the cache is just a temporary, fast copy.
8. **Famous truth:** “There are only two hard things in computer science: cache invalidation and naming things.” Take invalidation seriously.

> [!note] Final Rule of Thumb
> *When you have a performance problem, look for the **hot, rarely changing, and frequently read** data – that’s your perfect candidate for caching.*  
> *Start simple, measure everything, and evolve as needed.*

---

*سبحانك اللهم وبحمدك، أشهد أن لا إله إلا أنت، أستغفرك اللهم، وأتوب إليك*