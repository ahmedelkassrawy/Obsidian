```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

df["tags"] = df["tags"].apply(lambda x: model.encode(x))
```

```python
from sklearn.metrics.pairwise import cosine_similarity

sim = cosine_similarity(list(df['tags']))

def recommend(title):
  if title not in df["title"].values:
    print(f"Movie '{title}' not found in the dataset.")
    return
  
  movie_idx = df[df["title"] == title].index[0]
  sim_scores = list(enumerate(sim[movie_idx]))
  scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
  top_5 = [
      df["title"][i] for i,score in scores[1:6]
  ]
  return top_5
```