
> [!abstract] Goal
> This guide walks you through building a **production-style, decoupled retrieval model** from scratch.  
> You’ll train a Two-Tower neural network (user tower & item tower) using contrastive learning with in-batch negatives, then deploy the item tower offline with **FAISS** for real-time recommendations.  
> The dataset used is **MovieLens 1M** – the perfect playground for learning modern recommendation architectures.

---

## Phase 1: Data & Features

For a portfolio project, start with the **MovieLens 1M** dataset or the **H&M Personalized Fashion Recommendations** dataset (Kaggle).  

You need to convert your raw data into features that a neural network can digest:
- **User Features:** User ID (embedded), Age (normalized), Gender (one-hot encoded), or historical watch features (average genre vectors).
- **Item Features:** Item ID (embedded), Category/Genre (multi-hot encoded), Release Year, etc.

> [!tip] Tip
> Concatenate all user features into a single `user_vector` and all item features into an `item_vector` before passing them to the model.

---

### 1.1 Loading the MovieLens 1M Files

The dataset consists of three `.dat` files: `movies.dat`, `users.dat`, `ratings.dat`.  
Because they use `::` as a separator and the `movies.dat` contains special characters (e.g., accents), we need to specify `encoding='latin-1'`.

```python
import pandas as pd

# Load Movies – latin-1 handles special characters in titles
movies = pd.read_csv(
    '/content/ml-1m/movies.dat', 
    sep='::', 
    engine='python', 
    header=None,
    encoding='latin-1',
    names=['movie_id', 'title', 'genres']
)

# Load Users
users = pd.read_csv(
    '/content/ml-1m/users.dat', 
    sep='::', 
    engine='python', 
    header=None,
    names=['user_id', 'gender', 'age', 'occupation', 'zip_code']
)

# Load Ratings
ratings = pd.read_csv(
    '/content/ml-1m/ratings.dat', 
    sep='::', 
    engine='python', 
    header=None,
    names=['user_id', 'movie_id', 'rating', 'timestamp']
)
```

---

### 1.2 Filtering Positive Interactions

We treat only **ratings ≥ 4** as positive interactions (implicit feedback).  
The Two-Tower model will learn to pull the user and these positive items closer together.

```python
positive_ratings = ratings[ratings['rating'] >= 4].copy()
```

Now merge user and movie features **onto** these positive ratings. The rating table becomes the “glue” that connects a user profile to a movie profile.

```python
interaction_df = positive_ratings.merge(users, on='user_id', how='inner')
interaction_df = interaction_df.merge(movies, on='movie_id', how='inner')
```

---

### 1.3 Dropping Columns We Won’t Feed Directly

We drop:
- **`rating`** – we already filtered by it; the model only sees “positive/negative” via the loss.
- **`title`** – raw text cannot be digested by a simple model; we keep `movie_id` which learns a dense embedding.
- **`zip_code`** – too sparse / high‑cardinality for a tiny dataset; we already have `age`, `gender`, `occupation`.
- **`timestamp`** – a basic Two‑Tower model does not understand sequences.

```python
interaction_df = interaction_df.drop(columns=['timestamp', 'rating', 'title', 'zip_code'])
```

---

### 1.4 Encoding Features into Numbers

Neural networks require numerical inputs. We need three types of encoding.

#### 1.4.1 Continuous IDs (Label Encoding)

PyTorch `Embedding` layers require IDs to be strictly continuous integers starting from `0`.  
`pd.factorize` creates new sequential IDs while keeping the original mapping for later lookup.

```python
interaction_df['user_id_idx'] = pd.factorize(interaction_df['user_id'])[0]
interaction_df['movie_id_idx'] = pd.factorize(interaction_df['movie_id'])[0]
interaction_df['occupation_idx'] = pd.factorize(interaction_df['occupation'])[0]

# Keep vocabulary sizes for the PyTorch model
num_users = interaction_df['user_id_idx'].nunique()
num_movies = interaction_df['movie_id_idx'].nunique()
num_occupations = interaction_df['occupation_idx'].nunique()
```

#### 1.4.2 Binary Encoding

`gender` is a simple `'F'` → `0`, `'M'` → `1`.

```python
interaction_df['gender_idx'] = interaction_df['gender'].map({'F': 0, 'M': 1})
```

#### 1.4.3 Multi-hot Encoding for Genres

The `genres` column contains pipe‑separated strings like `"Action|Sci-Fi"`.  
Pandas’ `str.get_dummies()` turns this into a binary matrix where each genre is a column.

```python
genres_df = interaction_df['genres'].str.get_dummies(sep='|')
num_genres = genres_df.shape[1]

interaction_df = pd.concat([interaction_df, genres_df], axis=1)
```

Finally drop the original string columns, leaving only numbers.

```python
interaction_df = interaction_df.drop(columns=['user_id', 'movie_id', 'occupation', 'gender', 'genres'])
```

Now every row is a pure numerical representation of one user–movie positive interaction.

---

## Phase 2: Bridging Pandas to PyTorch

We need to create a custom `torch.utils.data.Dataset` that takes our DataFrame and yields a dictionary of tensors for each interaction.

```python
import torch
from torch.utils.data import Dataset, DataLoader

class TwoTowerDataset(Dataset):
    def __init__(self, df):
        core_cols = ['age', 'user_id_idx', 'movie_id_idx', 'occupation_idx', 'gender_idx']
        self.genre_cols = [col for col in df.columns if col not in core_cols]

        # User features
        self.user_ids = torch.tensor(df['user_id_idx'].values, dtype=torch.long)
        self.occupations = torch.tensor(df['occupation_idx'].values, dtype=torch.long)
        self.genders = torch.tensor(df['gender_idx'].values, dtype=torch.long)
        self.ages = torch.tensor(df['age'].values, dtype=torch.float32)

        # Item features
        self.movie_ids = torch.tensor(df['movie_id_idx'].values, dtype=torch.long)
        self.genres = torch.tensor(df[self.genre_cols].values, dtype=torch.float32)

    def __len__(self):
        return len(self.user_ids)

    def __getitem__(self, idx):
        return {
            "user_features": {
                "user_id": self.user_ids[idx],
                "occupation": self.occupations[idx],
                "gender": self.genders[idx],
                "age": self.ages[idx]
            },
            "item_features": {
                "movie_id": self.movie_ids[idx],
                "genres": self.genres[idx]
            }
        }

# Instantiate dataset and DataLoader
dataset = TwoTowerDataset(interaction_df)
dataloader = DataLoader(dataset, batch_size=1024, shuffle=True)
```

> [!important] Batch Size for Contrastive Learning
> The batch size directly controls the number of **negative examples** the model sees.  
> With a batch of 1024, each positive pair is contrasted against 1023 other items – much richer training signal.

---

## Phase 3: The Two-Tower Architecture

We decouple the model into two independent towers that output L2‑normalised embeddings of the same dimension. The dot product between them therefore equals **cosine similarity**.

### 3.1 User Tower

```python
import torch.nn as nn
import torch.nn.functional as F

class UserTower(nn.Module):
    def __init__(self, num_users, num_occupations, emb_dim=32):
        super().__init__()
        # Embeddings for categorical IDs
        self.user_emb = nn.Embedding(num_embeddings=num_users, embedding_dim=emb_dim)
        self.occ_emb = nn.Embedding(num_embeddings=num_occupations, embedding_dim=emb_dim)
        self.gender_emb = nn.Embedding(num_embeddings=2, embedding_dim=8)

        # Input size = 32 (user) + 32 (occ) + 8 (gender) + 1 (age) = 73
        self.fc_layers = nn.Sequential(
            nn.Linear(73, 128),
            nn.ReLU(),
            nn.Linear(128, 64)   # final output size 64
        )

    def forward(self, user_id, occupation, gender, age):
        u_vec = self.user_emb(user_id)
        o_vec = self.occ_emb(occupation)
        g_vec = self.gender_emb(gender)
        a_vec = age.unsqueeze(1)          # make it (batch, 1)

        x = torch.cat([u_vec, o_vec, g_vec, a_vec], dim=1)
        return self.fc_layers(x)
```

### 3.2 Item Tower

```python
class ItemTower(nn.Module):
    def __init__(self, num_movies, num_genres, emb_dim=32):
        super().__init__()
        self.movie_emb = nn.Embedding(num_embeddings=num_movies, embedding_dim=emb_dim)

        # Input size = 32 (movie emb) + num_genres (e.g., 18) = 50
        self.fc_layers = nn.Sequential(
            nn.Linear(emb_dim + num_genres, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )

    def forward(self, movie_id, genres):
        m_vec = self.movie_emb(movie_id)
        x = torch.cat([m_vec, genres], dim=1)
        return self.fc_layers(x)
```

### 3.3 Main Model – L2 Normalisation

```python
class TwoTowerModel(nn.Module):
    def __init__(self, num_users, num_occupations, num_movies, num_genres):
        super().__init__()
        self.user_tower = UserTower(num_users, num_occupations)
        self.item_tower = ItemTower(num_movies, num_genres)

    def forward(self, user_features, item_features):
        u_out = self.user_tower(**user_features)
        i_out = self.item_tower(**item_features)

        # Normalise to unit vectors (essential for FAISS inner product)
        u_out = F.normalize(u_out, p=2, dim=1)
        i_out = F.normalize(i_out, p=2, dim=1)
        return u_out, i_out

model = TwoTowerModel(num_users, num_occupations, num_movies, num_genres)
```

---

## Phase 4: Contrastive Training with In-Batch Negatives

We do **not** feed explicit negative samples. Instead, we compute the dot‑product matrix of the user and item embeddings **within the batch**. The diagonal entries are the positive pairs; everything else is treated as a negative.

Using `CrossEntropyLoss` on this matrix automatically pushes the diagonal up and the rest down.

> [!info] Why Temperature?
> Since embeddings are L2‑normalised, dot products lie between −1 and 1.  
> Dividing by a small `temperature` (e.g., 0.1) sharpens the distribution, helping the model converge.

```python
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

optimizer = optim.Adam(model.parameters(), lr=0.001)
temperature = 0.1
epochs = 20

print(f"Training on {device}...\n")

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for batch_idx, batch in enumerate(dataloader):
        optimizer.zero_grad()

        # Move features to device
        user_feats = {k: v.to(device) for k, v in batch['user_features'].items()}
        item_feats = {k: v.to(device) for k, v in batch['item_features'].items()}

        u_emb, i_emb = model(user_feats, item_feats)

        # Compute all pairwise dot products (batch_size x batch_size)
        logits = torch.matmul(u_emb, i_emb.T) / temperature

        batch_size = u_emb.size(0)
        labels = torch.arange(batch_size).to(device)   # 0,1,2,...,B-1

        loss = F.cross_entropy(logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if batch_idx % 100 == 0:
            print(f"Epoch {epoch+1} | Batch {batch_idx}/{len(dataloader)} | Loss: {loss.item():.4f}")

    avg_loss = total_loss / len(dataloader)
    print(f"=== Epoch {epoch+1} Completed | Average Loss: {avg_loss:.4f} ===\n")
```

> [!tip] Expected Loss Behaviour
> Initial loss ≈ ln(batch_size) ≈ 6.93 (for 1024).  
> As the model learns, it should drop steadily into the 6.6 – 6.0 range after a few epochs.  
> A small drop is normal; the large batch size means each step improves discrimination among many items.

---

## Phase 5: Offline Indexing & Serving with FAISS

After training, the two towers are completely independent. We freeze the model, pre‑compute item embeddings once, and build a FAISS index for real‑time retrieval.

### 5.1 Install FAISS (CPU)

```bash
!pip install faiss-cpu
```

### 5.2 Pre‑compute All Item Embeddings

```python
import numpy as np
import faiss

model.eval()

# Get every unique movie and its features
unique_movies = interaction_df.drop_duplicates(subset=['movie_id_idx'])

all_movie_ids = torch.tensor(unique_movies['movie_id_idx'].values, dtype=torch.long).to(device)
all_genres = torch.tensor(unique_movies[dataset.genre_cols].values, dtype=torch.float32).to(device)

with torch.no_grad():
    item_embeddings = model.item_tower(all_movie_ids, all_genres)
    # Re‑apply L2 normalisation (must match training)
    item_embeddings = F.normalize(item_embeddings, p=2, dim=1)

item_embeddings_np = item_embeddings.cpu().numpy()
print(f"Successfully generated embeddings for {item_embeddings_np.shape[0]} movies!")
```

### 5.3 Build the FAISS Index

We use `IndexFlatIP` because normalised vectors make inner product equal to cosine similarity.

```python
embedding_dim = 64
index = faiss.IndexFlatIP(embedding_dim)

index.add(item_embeddings_np)

print(f"FAISS index built with {index.ntotal} items.")
```

### 5.4 Real‑Time Recommendation for a User

Pick a test user from the dataset, run them through the user tower, and query FAISS.

```python
# Example: first user in unique_movies
test_user = unique_movies.iloc[0]

# Prepare user features with batch dimension = 1
u_id = torch.tensor([test_user['user_id_idx']], dtype=torch.long).to(device)
u_occ = torch.tensor([test_user['occupation_idx']], dtype=torch.long).to(device)
u_gen = torch.tensor([test_user['gender_idx']], dtype=torch.long).to(device)
u_age = torch.tensor([test_user['age']], dtype=torch.float32).to(device)

with torch.no_grad():
    user_vector = model.user_tower(u_id, u_occ, u_gen, u_age)
    user_vector = F.normalize(user_vector, p=2, dim=1)

K = 10
user_vector_np = user_vector.cpu().numpy()
distances, indices = index.search(user_vector_np, K)

print("Top 10 Recommended Movie Row Indices:", indices[0])
print("Cosine Similarity Scores:", distances[0])
```

---

## Phase 6: Decoding the Recommendations

FAISS returns the row indices of our `unique_movies` DataFrame. We must map those back to the original `movie_id` and then look up the real movie titles.

```python
# Recreate the original movie_id mapping used during pd.factorize
temp_df = positive_ratings.merge(movies, on='movie_id', how='inner')
original_movie_id_mapping = pd.factorize(temp_df['movie_id'])[1]

# Convert FAISS indices back to original movie IDs
recommended_idx = indices[0]
recommended_original_ids = original_movie_id_mapping[recommended_idx]

# Look up titles
final_recommendations = movies.set_index('movie_id').loc[recommended_original_ids]

print("🎯 TOP 10 MOVIE RECOMMENDATIONS FOR THIS USER:\n")
for rank, (movie_id, row) in enumerate(final_recommendations.iterrows(), 1):
    print(f"{rank}. {row['title']} (Genres: {row['genres']})")
```

---

## Phase 7: Next Level – The Ranking Stage

This two‑tower + FAISS pipeline is a **retrieval** model. It quickly narrows down millions of items to a few hundred candidates.  
To make this truly production‑grade, you would take those top‑K candidates and feed them into a **ranking model** (XGBoost, LightGBM, or a deep cross‑network). The ranking model is computationally heavier but only runs on those 100 candidates, not the entire catalog.

> [!example] Full Pipeline Flow
> 1. **User logs in** → User tower produces embedding (`O(1)` ms)
> 2. **FAISS search** over pre‑computed item embeddings → returns top‑100 candidates (`O(log N)` ms)
> 3. **Ranking model** scores the 100 candidates using rich features (user history, item metadata, context)
> 4. **Final ordered list** displayed to the user

---

## Final Remarks

What you’ve built is the exact backbone of modern retrieval systems used by YouTube, TikTok, Spotify, and others:

- Decoupled towers → offline indexing → real‑time ANN search.
- The model learns to push sequels and thematically similar items together without ever reading the movie titles, simply by observing overlapping user behaviour.
- The entire pipeline—data processing, custom Dataset, contrastive training, FAISS serving, and result decoding—is production‑ready.

Feel free to extend this project by:
- Adding more features (occupation, age bins, temporal dynamics)
- Incorporating text embeddings via pretrained language models for the cold‑start problem
- Implementing a ranking model on top of the retrieved candidates

Congratulations on completing a full, end‑to‑end retrieval architecture!