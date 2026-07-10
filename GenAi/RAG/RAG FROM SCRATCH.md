```python
!pip install rank_bm25

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
import torch

documents = [
    "The capital of France is Paris.",
    "The Great Wall of China is visible from space is a common myth.",
    "PyTorch is a machine learning framework based on the Torch library.",
    "A memory leak in Python can be debugged using the tracemalloc module."
]

tokenized_ds = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_ds)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(documents , convert_to_tensor = True)

```

```python
def get_hybrid_result(query, top_k = 3):
  #BM25
  tokenized_query = query.lower().split()
  bm25_scores = bm25.get_scores(tokenized_query)
  bm25_top_ids = np.argsort(bm25_scores)[::-1][:top_k]

  #semantic
  query_embedding = embed_model.encode(query,convert_to_tensor = True)
  cosine_scores = util.cos_sim(query_embedding,embeddings)[0]
  semantic_top_ids = torch.argsort(cosine_scores,descending = True)[:top_k].tolist()

  return bm25_top_ids.tolist() , semantic_top_ids

```

```python
def rrf(bm25_ranks,semantic_ranks,k = 60):
  scores = {}

  for rank,doc_id in enumerate(bm25_ranks):
    scores[doc_id] = scores.get(doc_id,0) + 1 / (k + rank)

  for rank,doc_id in enumerate(semantic_ranks):
    scores[doc_id] = scores.get(doc_id,0) + 1 / (k + rank)

  # sort
  fused_results = sorted(
      scores.items(),
      key = lambda x: x[1],
      reverse = True
  )
  return fused_results

```

```python
from transformers import pipeline

# Load a local generator (or use an API)
generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta", device_map="auto")

query = "How do I fix memory issues in Python?"
bm25_ids, semantic_ids = get_hybrid_results(query)
final_ranked = rrf(bm25_ids, semantic_ids)

# Get the top document text
best_doc_id = final_ranked[0][0]
context = documents[best_doc_id]

prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
response = generator(prompt, max_new_tokens=100)
print(response[0]['generated_text'])
```