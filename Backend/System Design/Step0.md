---
date: 2026-09-11
tags: [system-design, interview, phase-0, backend]
source: System Design Primer (donnemartin) + kassra lesson Phase 0
description: Phase 0 of system design — the 6-step method, the numbers, and every step explained, with a worked URL-shortener example.
---
# System Design — Phase 0 (the method + the numbers)

The goal of Phase 0: given any vague design prompt, take it to a defended design. You do that with a fixed **6-step method** + a few **numbers** you keep in your head.

---

## The 6-step method (the attack for any prompt)
Memorize the **order** — it's the spine of every answer.

1. **Requirements** — what it does (functional) + the scale/latency/availability targets (non-functional). Ask questions; nail what's in and out of scope. Never draw before this.
2. **Estimate** — rough back-of-envelope: reads/writes per second (QPS), storage/year, bandwidth. This sizes everything after it.
3. **API** — the handful of endpoints the client calls (the contract).
4. **Data model** — the main tables/entities + how they're read and written (access patterns).
5. **High-level design** — the boxes and arrows: client → load balancer → app → DB / cache / queue. The happy path.
6. **Scale & bottlenecks** — find the choke point, add caching / replication / sharding / queues; say the trade-off and what breaks at 10×.

---

## The latency numbers (learn the ratios, not the exact values)
| Operation | Time |
|---|---|
| Read from **RAM** | ~100 ns |
| Read from **SSD** (random) | ~150 µs (~1,000× slower than RAM) |
| **Disk seek** | ~10 ms (~100× slower than SSD) |
| Round trip **same datacenter** | ~0.5 ms |
| Round trip **cross-continent** | ~150 ms |

**The one takeaway:** RAM ≪ SSD ≪ disk ≪ far network. So: **cache in memory, avoid disk seeks, avoid cross-region round trips.** That single ranking drives half of all design decisions.

---

## The estimation math (step 2, explained)
Rough math to figure out *how big* the system is, so you know what design it needs. Three numbers:

**1. QPS — queries per second** (how much traffic hits it)
- `requests per day ÷ 86,400` (seconds/day ≈ 100,000 = 10⁵).
- **Peak ≈ 2× average** (traffic isn't flat).
- Track **reads/sec and writes/sec separately** — they scale differently.
- *Why it matters:* 100 writes/s fits one DB box; 100,000 writes/s needs sharding. The number picks the design.

**2. Storage/year** = `writes per day × bytes per write × days kept`.
- *Why:* a few GB fits one Postgres; petabytes/year → object storage + sharding.

**3. Bandwidth** = `QPS × bytes per request`.
- *Why:* tells you if you need a CDN and whether the network (not the CPU) is the bottleneck.

**Sizes:** KB = 10³, MB = 10⁶, GB = 10⁹, TB = 10¹² bytes.

**Worked example — a photo service, 10M uploads/day, 1 MB each:**
- write QPS = 10,000,000 ÷ 100,000 = **100 writes/s** (peak ~200)
- storage/day = 10M × 1 MB = **10 TB/day** → ~3.65 PB/year
- upload bandwidth = 100 × 1 MB = **100 MB/s**
→ From those three numbers alone you *know* one DB won't hold it (object storage + sharding) and you'll want a CDN. **The estimate picks the design before you draw a box.**

Rules of thumb: **seconds/day ≈ 10⁵**, **peak ≈ 2× average**, **read:write ratio matters** (most systems read far more than they write → cache the reads).

---

## Step 3 — API (explained)
Write the exact operations a client can call, with inputs and outputs — the **contract** between client and system. Once you name the operations, the data model and the boxes almost fall out of them.

Each endpoint needs: a verb, its inputs, its output. **HTTP verb rule: GET = read (safe, changes nothing), POST = create/write.**

Keep it small — the 3–5 core endpoints that define what the system does. (Shutterabia's MCP tools are exactly this: each tool = a name + inputs + output.)

---

## Step 4 — Data model + access patterns (explained)
Two halves:
1. **The shape** — tables/entities, fields, primary key, links.
2. **The access patterns** — *how* each piece is read and written, and how often. This matters more than the shape.

**An access pattern answers four things:**
1. How do I **read** it? (by what key?)
2. How do I **write** it? (insert / update / append?)
3. **Read-heavy or write-heavy?** (the ratio)
4. **How much, how fast?** (from the estimate)

**Why it's the most important part:** the access pattern decides three concrete choices:
- **What to index** — you index the field you *look up by*.
- **SQL vs NoSQL** — simple key lookups suit key-value; complex joins suit SQL.
- **What to cache / how to shard** — read-heavy → cache; "by user_id" → shard by user_id.

The one-line habit: before choosing a DB or index, write *"I read this by ___ and write it by ___, mostly reads/writes."* That sentence picks your storage.

*Contrast:* URL shortener reads by short_code (100:1) → index short_code + cache. Twitter timeline reads "newest posts from everyone I follow" → a hard pattern that forces precomputing timelines. Same-ish data, different pattern, different design.

---

## Step 5 — High-level design (explained)
Draw the components as boxes, connect with arrows, trace the **happy path** (normal, no failures yet).

**The standard boxes (add one only when justified):**
- **Client** — browser/app/service making the request.
- **Load balancer (LB)** — one front door spreading requests across many identical app servers.
- **App servers** — your logic; usually several identical copies behind the LB.
- **Database** — durable source of truth.
- **Cache** — fast in-memory store (Redis) in front of the DB for hot reads.
- **Queue** — buffer for async/slow work so the request returns fast; a worker does the slow part.

Start with the dumbest version that works (client → app → DB), get the happy path flowing, *then* add cache/queue/LB as the estimate demands. Knowing what to **leave out** is part of the skill.

### CDN (explained)
**CDN = Content Delivery Network** — servers spread worldwide that keep **copies** of your static files close to users, so a request doesn't travel to your one origin.
- *Problem it solves:* a cross-world round trip is ~150 ms; a nearby edge is a few ms.
- *How:* caches images/video/CSS/JS at ~hundreds of edge locations. First request fetches from origin + caches; everyone after gets the fast local copy. Also takes load off your origin.
- *When to use:* read-heavy static content served to a wide geography.
- *Two flavors:* **pull** (CDN fetches from origin on first request — easy, common) vs **push** (you upload to the CDN — more control, large/rare files).
- You already use one: **Cloudflare in front of Shutterabia.**

---

## Step 6 — Scale & bottlenecks (explained)
Look at the happy-path design under the real load, find the **one box that maxes out first** (usually the DB), fix it, then ask "what breaks *next* at 10×."

**The four fixes — each does one thing and costs one thing:**
| Fix | What it does | Trade-off (what you give up) |
|---|---|---|
| **Caching** | serve hot reads from memory, skip the DB | staleness; invalidation is hard |
| **Replication** | DB copies; spread reads + failover | replication lag (replicas slightly behind = eventual consistency); writes still go to one primary |
| **Sharding** | split data across DBs by a key | cross-shard queries hard; rebalancing painful; hot shards |
| **Queues** | absorb spikes; do slow work async | work happens later (eventual); more moving parts; ordering/retries |

Pattern: **reads don't scale → cache + replicas. Writes/storage don't scale → shard. Slow/spiky work → queue.**

**"What breaks at 10×"** is the senior discipline: after each fix, name the *next* choke point (e.g. "10× corpus → pgvector flat scan slows → add an HNSW index").

The habit: never present the scaled design first. Show the simple happy path, then say "the DB is the bottleneck at N QPS — here's how I relieve it, and here's what gives."

---

## Worked example — URL shortener (bit.ly)
Givens: 100M new URLs/month, ~500 bytes/record, read:write = 100:1.

**1. Requirements**
- Functional: **create** (long URL → short code, with sanitization of tracking params) + **redirect** (short code → long URL, a 302).
- Non-functional: read-heavy; **low latency on redirect** (it's in the click path → cache); **high availability** (down = every link breaks); **short codes unique**. Write-light (we do write, ~100× less than we read).

**2. Estimate**
- write QPS = 100M / 2.6M ≈ **38/s** (peak ~77/s) → tiny, one DB handles writes.
- read QPS = 100 × 38 ≈ **3,850/s** (peak ~7,700/s) → needs cache + read replicas.
- storage/year = 100M × 12 × 500 B ≈ **600 GB/year** → fits one DB for years, no sharding yet.

**3. API**
```
POST /shorten   { long_url }        -> { short_url }
GET  /{short_code}                  -> 302 redirect to long_url
```
(POST = write/create, GET = read/redirect.)

**4. Data model**
```
urls
  short_code  (PK, unique, indexed)   "aX9k2"
  long_url
  created_at
access: read by short_code (hot, 100:1) · write = insert one row (rare)
```
The access pattern (read by short_code) is what makes short_code the index.

**5. High-level design**
```
READ (hot, 100:1):
  client → LB → app → cache?  hit → return; miss → DB → fill cache → return → 302
WRITE (rare):
  client → LB → app → DB (insert short_code → long_url)
Components: client → Load Balancer → App servers (stateless) → Cache (Redis) + Database
```

**6. Scale & bottlenecks**
- Bottleneck = **DB reads**. Cache absorbs most (100:1 + good hit rate); **read replicas** spread the misses. Writes (~77/s) fine on one primary.
- Trade-off: **replication lag** — a just-created link may not be on a replica yet (could 404 for a second). Mitigate: read new codes from primary, or the write-time cache.
- 10×: reads (~80k/s) → cache is critical (guard against a cache-flush stampede); storage → eventually **shard** by short_code.

### Deep-dive: generating the short code (unique, at scale, no bottleneck)
- **Counter + base62** — a global incrementing number encoded to base62 (`aX9k2`). Guaranteed unique; the counter is a single point → hand out ID *ranges* per server to avoid it. **Best default.**
- **Random + check** — generate random, check the DB for a collision, retry. Simple; collisions rise as it fills.
- **Why NOT SHA-256** — a hash is 64 chars → you must **truncate** → truncation reintroduces collisions → you're back to "random + check." Also a hash is **deterministic** (same URL → same code), which blocks separate links for the same URL, blocks custom codes, and makes codes predictable. It doesn't remove the per-write DB check either. (Hashing *is* fine separately if you *want* dedup — "have I shortened this URL before?")

---

## Phase 0 checklist (grokked-when)
On a blank page, no AI: list the **6 steps** in order, the **5 latency numbers / the ranking**, and do **one estimate** (writes/day → storage/year). Then run the full method on a novel prompt.
