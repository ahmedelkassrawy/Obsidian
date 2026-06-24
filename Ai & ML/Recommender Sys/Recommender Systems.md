# Recommender Systems — Overview & Examples

This folder contains a consolidated guide and runnable examples for collaborative-filtering recommender systems (matrix factorization, item-based CF, and from-scratch pivot-table approaches). It merges the previous `Steps.md` and `Untitled.md` into a single, organized reference.

## Overview

- **Goal:** Predict user preferences for items (movies, books, etc.) and produce ranked recommendations.
- **Common approaches:** Matrix factorization (SVD), Neural Collaborative Filtering (NCF), KNN-based item/user similarity, and custom pivot-table solutions.

## Pipeline (High-level)

1. Data preparation: load, clean, and map IDs (use `LabelEncoder` or integer mappings for `user_idx` and `item_idx`).
2. Train/test split: hold out a test set for evaluation.
3. Build user–item matrix (pivot table) for exploratory analysis and some algorithms.
4. Check matrix sparsity and decide on strategy (SVD, imputation, hybrid, etc.).
5. Choose and train model (SVD, KNN, NCF, or custom).
6. Evaluate (RMSE/MAE for explicit ratings; ranking metrics for top-N recommender).
7. Serve recommendations: predict or compute top-N per user.

## Important Concepts

- **User–Item Matrix (pivot):** rows = users, columns = items, values = ratings.
  ```python
  user_item_matrix = data.pivot_table(index='user_idx', columns='title', values='rating')
  ```
- **Sparsity:** fraction of missing entries in the matrix. High sparsity often requires matrix factorization or hybrid methods.
  ```python
  sparsity = 1.0 - (user_item_matrix.count().sum() / user_item_matrix.size)
  print(f"Matrix sparsity: {sparsity:.2%}")
  ```

## Models: SVD vs NCF (short)

- **SVD (matrix factorization):** linear factorization into user/item latent vectors. Good for explicit ratings, lightweight and interpretable.
- **NCF (Neural Collaborative Filtering):** uses embeddings + MLPs to learn non-linear interactions; more flexible for implicit feedback and hybrid inputs but heavier.

Comparison summary:

| Feature | SVD | NCF |
|---|---:|---:|
| Model type | Linear MF | Deep (non-linear) |
| Data | Explicit ratings | Implicit or explicit |
| Interpretability | High | Low |
| Compute | Light | Higher |

## Quick Examples

1) Surprise library — SVD (matrix factorization)

```python
# pip install scikit-surprise
from surprise import SVD, Dataset
from surprise.model_selection import train_test_split
from surprise import accuracy

data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
model = SVD()
model.fit(trainset)
predictions = model.test(testset)
accuracy.rmse(predictions)
```

2) Surprise — Item-based KNN (item-item CF)

```python
from surprise import KNNBasic, Dataset
from surprise.model_selection import train_test_split
from surprise import accuracy

data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
sim_options = {'name': 'cosine', 'user_based': False}
model = KNNBasic(sim_options=sim_options)
model.fit(trainset)
predictions = model.test(testset)
accuracy.rmse(predictions)
```

3) From-scratch pivot table + item-item cosine similarity

```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# example data -> build pivot table
df = pd.DataFrame({'user_id':[1,1,2,3], 'item_id':[10,20,10,20], 'rating':[5,3,4,2]})
pivot = df.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)
item_sim = cosine_similarity(pivot.T)
item_sim_df = pd.DataFrame(item_sim, index=pivot.columns, columns=pivot.columns)
```

## Practical Tips

- Start simple (SVD or item-KNN) on small datasets (MovieLens) before moving to NCF.
- For high sparsity, use regularized matrix factorization or hybrid models that incorporate content.
- Evaluate for both rating prediction (RMSE/MAE) and ranking (Precision@K, Recall@K, NDCG).
