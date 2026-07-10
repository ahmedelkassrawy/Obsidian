```python
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-mpnet-base-v2")
faq_embeddings = encoder.encode(faq_df["question"].tolist())

print(f"Sample (first 10 dimensions): {faq_embeddings[0][:10]}")
```

```python
def cosine_dist(a: np.array, b: np.array):
    """Compute cosine distance between two sets of vectors."""
    a_norm = np.linalg.norm(a, axis=1)
    b_norm = np.linalg.norm(b) if b.ndim == 1 else np.linalg.norm(b, axis=1)
    sim = np.dot(a, b) / (a_norm * b_norm)
    return 1 - sim


def semantic_search(query: str) -> tuple:
    """Find the most similar FAQ question to the query."""
    query_embedding = encoder.encode([query])[0]

    distances = cosine_dist(faq_embeddings, query_embedding)

    # Find the most similar question (lowest distance)
    best_idx = int(np.argmin(distances))
    best_distance = distances[best_idx]

    return best_idx, best_distance
```

#### Moving To Redis
```python
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
```

```python
import redis

try:
    r = redis.Redis.from_url(REDIS_URL)
    r.ping()
    print("✅ Redis is running and accessible")
except redis.ConnectionError:
    print("❌ Cannot connect to Redis")
    raise
```

### Using a Cache-Optimized Embedding Model (langcache-embed-v1)
```python
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.extensions.cache.embeddings import EmbeddingsCache

langcache_embed = HFTextVectorizer(
    model="redis/langcache-embed-v1",
    cache=EmbeddingsCache(redis_client=r, ttl=3600)
)
```

### Create the Redis Semantic Cache
```python
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.extensions.cache.embeddings import EmbeddingsCache

langcache_embed = HFTextVectorizer(
    model="redis/langcache-embed-v1",
    cache=EmbeddingsCache(redis_client=r, ttl=3600)
)
```

### Load the Cache with FAQ Data
```python
for i in range(len(faq_df)):
    cache.store(
        prompt=faq_df.iloc[i]["question"],
        response=faq_df.iloc[i]["answer"]
    )
    
result = cache.check("I need a refund for my purchase")
```

### Implement TTL (time-to-live) policy to keep cache fresh
```python
cache.set_ttl(86400)
```