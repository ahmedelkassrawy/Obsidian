---
tags: [backend, system-design, rag, multi-tenant, sharding, full-design, interview]
domain: backend
type: lesson-note
status: digested
source: System Design Primer — Phase 6 (Full Designs); Kassra growth-track session 2026-09-16
---
# Design: Multi-Tenant RAG Service

The capstone design (Phase 6). Runs the full 6-step method on a productized raaaaag: many companies each upload their own docs and query only their own knowledge base, through one shared service.

> "Design a RAG service that serves many tenants. Each tenant uploads documents and asks questions; answers must come only from *their* documents. Walk me through it."

**Givens:**
- 500 tenants, growing.
- Each tenant: ~100k docs → ~5M chunks. Total ~2.5B chunks.
- ~50 queries/sec across all tenants at peak.
- Ingestion is bursty (a tenant onboards → dumps 100k docs at once).

## Step 1 — Requirements

**Functional:**
- **Ingest:** tenant uploads docs → chunk → embed → store.
- **Query:** get the question → retrieve the right chunks → feed as context to the LLM → answer.

**Non-functional:**
- **Latency:** the LLM dominates; retrieval must be fast so the LLM is the only slow part.
- **Consistency:** a new doc should show up in answers soon (eventual is fine, seconds-to-minutes).
- **Availability:** can degrade/fail without disaster (AP-leaning).

**The hook we missed — tenant isolation (the spine):**

> [!warning] Tenant isolation
> **Tenant A must NEVER retrieve, see, or get an answer built from tenant B's documents.** Every query must be scoped to *only that tenant's* data. This is a **correctness + security** requirement — the one thing you can never violate. Leak one tenant's docs into another's answer and the product is dead. It threads through every later step (data model, query filter, shard key, cache key).

## Step 2 — Estimate

**1. Storage:**
```text
2.5B chunks × 6 KB = 15,000,000,000 KB = ~15 TB   (just the vectors)
```
**15 TB does not fit on one machine.** That single number forces your hand.

**2. Query load — 50 q/s is tiny:**
```text
50 q/s of reads → a single Postgres handles thousands of simple q/s
```
QPS is **not** the problem. The reframe: despite "lots of reads," 50/s is nothing. The pressure is **data size**, not request rate.

**3. The real bottleneck picks the tool for you:**

> [!warning] Storage forces sharding, not replication
> The bottleneck is **15 TB of vectors**, not query volume. That rules out replication — a replica is a *full copy*, so each replica is still 15 TB (Phase 3: "replication won't help when every copy is too big"). **You must shard** — split the 2.5B chunks across machines. The shard key comes from Step 1's spine: **`tenant_id`** (which also enforces isolation for free — a tenant's data lives together, queries only touch their shard).

The estimate did real work: it killed "just replicate," confirmed sharding, and confirmed the shard key. **That's** why you estimate before designing — the number eliminated an option.

**Step 2 summary:**
- Storage: **~15 TB** → too big for one box → **shard**.
- Query: **50 q/s** → trivial → not the bottleneck.
- Embedding: bursty on ingest → **queue + rate-limit** the embed calls (Phase 5), not the query path.
- Bottleneck: **storage size → sharding by `tenant_id`.**

## Step 3 — API

```text
POST /ingest   Authorization: Bearer <token>   body: { document }   → { job_id }
POST /query    Authorization: Bearer <token>   body: { question }   → { answer, citations }
```

> [!warning] Derive tenant_id from auth, never from the request body
> If `tenant_id` is a parameter the caller sets, tenant A just sends `tenant_id: B` and reads B's documents — the isolation spine is broken in one line. **The tenant_id must come from the auth token** (API key / JWT), which the server decodes. The client proves *who they are*; the server decides *what data that maps to*. Auth **is** what supplies tenant_id — they're not two separate things. No tenant_id in the body, ever.

**`/ingest` is async:** a tenant onboarding dumps 100k docs — you can't chunk+embed all that in one HTTP request. So `/ingest` returns a `job_id` immediately and does the work on a queue/worker (Temporal). `/query` stays sync — the user is waiting on that answer.

## Step 4 — Data Model

```text
chunks(
  chunk_id     PK,
  tenant_id    ← shard key + isolation filter (indexed),
  doc_id       ← to delete/re-ingest a whole doc,
  chunk_text,
  embedding    vector(1536)
)
```
- **Shard key `tenant_id`** — isolation + even-ish distribution.
- **HNSW on `embedding`** — approximate nearest-neighbor for fast vector search (raaaaag build).

> [!warning] Filtered-ANN is the hard part
> A query must do **two things at once**: "find nearest vectors" (HNSW) **and** "only where tenant_id = me". If a shard holds several tenants, naive **post-filtering** (grab top-100 by vector, then drop other tenants') can return *too few* of your tenant's results. The fix: **pre-filtering** (scope to the tenant's rows first, then vector-search) or a per-tenant index/partition. Sharding by tenant_id already helps by narrowing to fewer tenants per shard.

> [!tip] Optional add
> A `chunk_uid` (the Temporal idempotency trick) lets a re-ingest of the same doc no-op instead of duplicating — reuse what you built.

## Step 5 — High-level design

**Ingest flow (async):**
```text
POST /ingest (+ auth token)
  → API server: decode token → tenant_id (isolation); drop job on QUEUE, return { job_id }
  → Ingest queue / worker (Temporal)
        load document → chunk → embed (embedding API, rate-limited + batched)
        → upsert into sharded chunks table (chunk_uid = idempotent)
  → Vector DB shard for that tenant_id  (stored chunks)
```

**Query flow (sync — user waiting):**
```text
POST /query (+ auth token)
  → API server: decode token → tenant_id
  → CACHE check (Redis, cache-aside)
        HIT (same tenant + same question)? → return cached answer, done
        MISS ↓
  → Retrieval: route to tenant's shard → filtered vector search (HNSW + tenant_id) → top-k
  → LLM: prompt = question + top-k chunks (context) → grounded answer   ← slow box
  → write answer to CACHE (key = tenant_id + question) → return { answer, citations }
```

> [!warning] The cache key must include tenant_id
> Two tenants can ask the identical question and must get answers from *their own* docs. `cache[question]` would leak across tenants; `cache[tenant_id + question]` is correct. Isolation reaches even into the cache.

**Cross-cutting guarantees:** tenant isolation (token→tenant_id→shard/filter) · idempotency (chunk_uid) · back pressure (batching + rate limits) · durability (Temporal retries/resumes) · scale (~15 TB across shards).

## Step 6 — Scale & 10× thinking

**10× (5,000 tenants, 25B chunks ≈ 150 TB):**

> [!note] Separate the trivial tiers from the real bottleneck
> The **stateless tiers scale for free** — API servers + LB + rate limiters are stateless, so at 10× you just add more boxes behind the LB. What **breaks first is the data layer**: shards are now 10× bigger → you must **add shards and rebalance ~135 TB** of vectors across machines while serving traffic (the slow, risky Phase-3 operation). Secondary: 10× ingest load hammers the embedding API → the queue backs up → more workers + backpressure.

**Hot tenant (one tenant 50× the rest) = the hot-shard trap:**

Hashing `tenant_id+collection` spreads *evenly-sized* tenants, but can't hide a 50× elephant — split finely, that one tenant still swamps whatever shards it lands on, dragging down small tenants sharing them.

> [!tip] Dedicated vs pooled shards
> **Pooled = shared building:** many small tenants share shards (cheap — none is heavy enough to cause trouble). Right for the 4,999 small ones.
> **Dedicated = the whale gets its own house(s):** pull the giant tenant OUT of the pool onto machines only for them, sharded internally by collection/doc.
> **Rule: big tenants get dedicated shards; small tenants stay pooled.** Decide per-tenant by size. Two bonuses: (1) noisy-neighbor gone — the whale's spikes hit only its own machines; (2) isolation spine hardened — the whale's data physically lives on separate hardware, so a query can't even accidentally touch another tenant's rows.

```text
BAD  (pooled, whale mixed in):        GOOD (whale dedicated, smalls pooled):
  shard 1: [whale bit][A][B]            shard 1: [ WHALE only ]
  shard 2: [whale bit][C][D]            shard 2: [ WHALE only ]
  shard 3: [whale bit][E][F]            shard 3: [A][B][C][D][E][F]...
```

## Refinements the diagram flagged (add these)

- **Load balancer** in front of *many* API servers — one API box is a single point of failure (Phase 2).
- **Reranker** — real RAG is retrieval → **rerank** (Cohere) → top-k → LLM; don't jump retrieval → LLM.

> [!success] Design complete + Excel Gate met
> All 6 steps + 10× + hot-tenant defended. This is the AI-bank design (built on raaaaag); with the URL shortener + rate limiter it clears the gate's "3 full designs, ≥1 AI." Diagram: `ME/Excalidraw/rag_system_design (1).excalidraw`.

## Interview polish notes (carry into every design)
- **Give the number**, not "a lot" (15 TB, 50 q/s, ~150 TB at 10×).
- **Commit a CP/AP verdict**, don't describe both.
- **Ask "static or dynamic?"** first when tracing a request (decides if the CDN works or just forwards).
- **Name why you're NOT using a tool** (e.g. not sharding when the table fits one box) — worth as much as picking the right one.
- **Name backoff + idempotency together** on every retry (backoff protects the downstream, idempotency protects the data).
- **Separate trivial (stateless) tiers from the real bottleneck** at 10×.
