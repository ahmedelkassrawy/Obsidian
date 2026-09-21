---
description: "The LLM-app caching stack — exact-match (Redis), semantic (RedisVL), prompt/prefix caching, embedding cache, and KV cache — with Redis code, invalidation, and best practices."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/llmops
  - topic/caching
  - topic/redis
  - llm-caching
  - semantic-cache
  - redis
  - prompt-caching
  - embedding-cache
hubs:
  - "[[MLOps]]"
  - "[[Redis]]"
date: 2026-09-21
source: "Kassra growth-track session 2026-09-21"
---
# LLM Caching

> Related: [[LLM Gateways]] (the gateway's cache is this) · [[Agent Memory with Redis]] (same Redis, different key prefix) · system-design Phase 4 caching · transformers KV cache / vLLM prefix caching.

LLM calls are slow and expensive, so cache at several levels — each catches a different kind of repeat. Separate from DB caching (system-design Phase 4); this is LLM-specific.

## The layers (cheapest/closest first)
```text
request
  ├─ 1. exact-match cache    same prompt → stored response      (skip the call)
  ├─ 2. semantic cache       similar prompt → stored response    (catch paraphrases)
  ├─ 3. prompt/prefix cache  reuse the big static prefix         (provider-side)
  ├─ 4. embedding cache      same text → stored vector           (skip re-embedding)
  └─ 5. KV cache             reuse past tokens within one gen    (in the model)
```
Layer 5 = transformers KV cache; vLLM prefix caching (M2) sits near layer 3. Below are the app-level ones, on **Redis**.

```bash
pip install redis redisvl
```

## 1. Exact-match response cache — Redis
Key = hash of everything that changes output; `SET ... EX` = TTL invalidation for free.
```python
import redis, hashlib, json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def cached_call(model, messages, ttl=3600, **params) -> str:
    key = "llm:" + hashlib.sha256(
        json.dumps({"model": model, "messages": messages, **params},
                   sort_keys=True).encode()
    ).hexdigest()

    hit = r.get(key)                 # 1. look up
    if hit is not None:
        return hit                   #    HIT — skip the paid call

    resp = llm.invoke(messages).content
    r.set(key, resp, ex=ttl)         # 2. store with TTL (auto-expires)
    return resp
```

> [!warning] The key must include everything that changes the output
> model + messages + temperature + system prompt + tools. Miss one → wrong cached answer. And only cache **deterministic** calls (`temperature=0`); caching a random sample freezes one roll as "the" answer.

## 2. Semantic cache — RedisVL `SemanticCache`
Embeds the prompt, stores it as a vector in Redis, returns a past answer when a new prompt is close enough.
```python
from redisvl.extensions.llmcache import SemanticCache

llmcache = SemanticCache(
    name="llmcache",
    redis_url="redis://localhost:6379",
    distance_threshold=0.1,          # lower = stricter (see note)
    ttl=3600,
)

def semantic_cached(query: str) -> str:
    hit = llmcache.check(prompt=query)          # vector search over past prompts
    if hit:
        return hit[0]["response"]               # HIT — close-enough past prompt
    ans = llm.invoke(query).content
    llmcache.store(prompt=query, response=ans)  # MISS — store for next time
    return ans
```

> [!warning] `distance_threshold` is a DISTANCE, not a similarity
> **Lower = stricter** (more similar required). `0.1` ≈ near-identical only; raising toward `0.2–0.3` gets more hits but risks **false hits** ("enable X" matching "disable X"). Start strict, test on real paraphrases, loosen carefully. Never use semantic cache where a near-miss is harmful.

Share the vector space with raaaaag by passing your own embedder:
```python
from redisvl.utils.vectorize import HFTextVectorizer
llmcache = SemanticCache(
    name="llmcache", redis_url="redis://localhost:6379",
    vectorizer=HFTextVectorizer(model="sentence-transformers/all-MiniLM-L6-v2"),
    distance_threshold=0.15,
)
```

## 3. Auto-cache every LangChain call (Redis, zero per-call code)
```python
from langchain_community.cache import RedisSemanticCache
from langchain_core.globals import set_llm_cache
from langchain_openai import OpenAIEmbeddings

set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=OpenAIEmbeddings(),
    score_threshold=0.2,
))
# every llm.invoke(...) now checks/fills the semantic cache automatically
```

## 4. Prompt / prefix caching (the big one for agents)
Most of an agent's prompt is static and huge (system prompt, tool defs, retrieved docs) and resent every turn. Prompt caching tells the **provider** to cache that prefix and reuse it — full price once, a fraction after.
```text
[ system + tools + docs ]  [ this turn's question ]
└──── static, CACHE ──────┘ └── changes each call ──┘
```
```python
# Anthropic prompt caching — mark the static prefix
messages = [{
    "role": "system",
    "content": [{"type": "text", "text": BIG_SYSTEM_PROMPT,
                 "cache_control": {"type": "ephemeral"}}],   # ← cache this block
}]
```
Provider-side cousin of KV cache / vLLM prefix caching — same idea (don't reprocess the unchanging prefix). **Rule:** static content **first** in the prompt, variable content **last** — caching only bites on a stable prefix.

## 5. Embedding cache — Redis
Never re-embed the same text.
```python
import numpy as np

def embed_cached(text: str) -> list[float]:
    key = "emb:v1:" + hashlib.sha256(text.encode()).hexdigest()   # v1 = model version!
    hit = r.get(key)
    if hit:
        return json.loads(hit)
    vec = embedder.embed(text)
    r.set(key, json.dumps(vec))          # embeddings stable → no TTL needed
    return vec
```
Key includes the embedding-model version (`v1`): a new model = different vectors, so old entries must not be reused. Pairs with `chunk_uid` idempotency in RAG ingestion.

## Invalidation — the hard part (same as Phase 4)
> [!warning] A cache is a copy; when the source changes, it's stale
> - **Response / semantic cache:** on a new ingest, old answers are wrong → TTL, or clear on ingest (the raaaaag `search_docs` TTL-vs-invalidate call).
> - **Prompt cache:** short provider TTL (minutes) — fine, it's perf not correctness.
> - **Embedding cache:** safe to keep per model — but key on the model version.

## Best practices
- **Cache key = everything that changes output** (model, params, system prompt, tool set, embedding-model version).
- **Only cache deterministic calls** (`temperature=0`) for response caches.
- **Static-first prompt layout** so prefix caching bites.
- **Semantic cache: high threshold + test**; never on harmful-if-wrong surfaces.
- **TTL or event-invalidate** anything tied to changing data; don't buy precise invalidation when "stale for minutes" is harmless.
- **Measure hit rate** — a 5%-hit cache is just overhead (Phase 4 rule).
- **One Redis, many prefixes** — `llm:`, `llmcache:`, `emb:` alongside memory keys (see [[Agent Memory with Redis]]).

> [!tip] The through-line
> LLM caching = **skip work you've already done** at four levels: same request (exact), similar request (semantic), same prefix (prompt/KV), same text (embedding). Exact + prompt caching are almost always safe wins; semantic caching is powerful but risky (false hits). Invalidation is the hard part — tie every cache to how fast its source changes.

## Fits
- **raaaaag** Redis BM25 cache = cache-aside response caching; **vLLM prefix caching** (M2) + **KV cache** = layers 5/3 in the model.
- **Anthropic prompt caching** = the layer-4 knob for any agent with a big system prompt + docs.
- The **[[LLM Gateways]]** cache layer is exactly layers 1–2 here, centralized in the gateway.
