> "Design a RAG service that serves many tenants. Each tenant uploads documents and asks questions; answers must come only from _their_ documents. Walk me through it."

**Your givens (use these numbers):**

- 500 tenants, growing.
- Each tenant: ~100k docs → ~5M chunks. Total ~2.5B chunks.
- ~50 queries/sec across all tenants at peak.
- Ingestion is bursty (a tenant onboards → dumps 100k docs at once).

functional:
- **Ingest:** tenant uploads docs → chunk → embed → store.
- **Query:** get the question → retrieve the right chunks → feed as context to the LLM → answer.

non functional:
	latency: the LLM dominates; retrieval must be fast so the LLM is the only slow part.
	 consistency: a new doc should show up in answers soon (eventual is fine, seconds-to-minutes).
	 availability: an degrade/fail without disaster (AP-leaning).
	 
the hook we missed was thre tenant isolation 
**Tenant A must NEVER retrieve, see, or get an answer built from tenant B's documents.**
- Every query must be scoped to _only that tenant's_ data. 
- This is a **correctness + security** requirement — the one thing you can never violate. 
- Leak one tenant's docs into another's answer and the product is dead.

Estimations:
**1. Storage — do the math:**

2.5B chunks × 6 KB = 15,000,000,000 KB = ~15 TB   (just the vectors)

**15 TB does not fit on one machine.** That single number forces your hand.

**2. Query load — 50 q/s is _tiny_.**

50 q/s of reads → a single Postgres handles thousands of simple q/s

So QPS is **not** the problem. This is the reframe: despite "lots of reads," 50/s is nothing. The pressure here is **data size**, not request rate.

**3. The real bottleneck — and it picks the tool for you:**

> [!warning] Storage forces sharding, not replication  
> The bottleneck is **15 TB of vectors**, not query volume. And that rules out replication as the fix — a replica is a _full copy_, so each replica is still 15 TB (Phase 3: "replication won't help when every copy is too big"). **You must shard** — split the 2.5B chunks across machines. And you already know the shard key from Step 1's spine: **`tenant_id`** (which also enforces isolation for free — a tenant's data lives together and queries only touch their shard).

So the estimate did real work: it killed "just replicate," confirmed sharding, and confirmed the shard key. **That's** why you estimate before designing — the number eliminated an option.

**Your Step 2, with numbers:**

- Storage: **~15 TB** vectors → too big for one box → **shard**.
- Query: **50 q/s** → trivial for reads → not the bottleneck.
- Embedding: bursty on ingest → **queue + rate-limit** the embed calls (Phase 5), not the query path.
- Bottleneck: **storage size → sharding by `tenant_id`.**

**API endpoints :**
- `POST /ingest` → doc + tenant → returns doc/job id.
- `POST /query` → question + tenant → returns answer.

**The fix — the client must NOT send `tenant_id`:**

> [!warning] Derive tenant_id from auth, never from the request body  
> If `tenant_id` is a parameter the caller sets, tenant A just sends `tenant_id: B` and reads B's documents — the isolation spine is broken in one line. 
> **The tenant_id must come from the auth token** (API key / JWT), which the server decodes. 
> The client proves _who they are_; the server decides _what data that maps to_. 
> Client-supplied identity + server-trusted scoping is the whole game.

the key is _auth is what supplies tenant_id_, they're not two separate things. So:

```
POST /ingest   Authorization: Bearer <token>   body: { document }        → { job_id }
POST /query    Authorization: Bearer <token>   body: { question }        → { answer, citations }
```

Server extracts `tenant_id` from the token on every call. No tenant_id in the body, ever.

**One more (ties to Phase 5):** `/ingest` should be **async**. A tenant onboarding dumps 100k docs — you can't chunk+embed all that inside one HTTP request. So `/ingest` **returns a `job_id` immediately** and does the work on a queue/worker (your Temporal instinct). `/query` stays sync — the user's waiting on that answer.

Data Model
Table:
```
chunks(
  chunk_id     PK,
  tenant_id    ← shard key + isolation filter (indexed),
  doc_id       ← to delete/re-ingest a whole doc,
  chunk_text,
  embedding    vector(1536)
)
```

- **Shard key `tenant_id`** ✅ — isolation + even-ish distribution.
- **HNSW on `embedding`** ✅ — approximate nearest-neighbor for fast vector search (your raaaaag build).

[!warning] Vector search + a tenant filter don't compose for free  
A query must do **two things at once**: "find nearest vectors" (HNSW) **and** "only where tenant_id = me".
If a shard holds several tenants, the DB must combine the HNSW walk with the `tenant_id` filter — and naive **post-filtering** (grab top-100 by vector, then throw away other tenants') can return _too few_ of your tenant's results. 
The fix is either **pre-filtering** (scope to the tenant's rows first, then vector-search) or giving each tenant its own index/partition. 
Sharding by tenant_id already helps — the shard narrows to fewer tenants — but name that filtered-ANN is the hard part.

[!tip] Optional add  
A `chunk_uid` (your Temporal idempotency trick) lets a re-ingest of the same doc no-op instead of duplicating — reuse what you built.

---
post /ingest (+ auth token)
	decode token -> tenat id (isolation)
	drop a job on queue and return the job id immediatly (async)
-> Ingest queue / worker (temporal)
load document
chunk it
embed with the chunk and calls the embedding API , rate limited + batched
upsert the chunks into sharded chunks table (chunk uuid = idempotent)
vector db shard for that tenant id (stored chunks)