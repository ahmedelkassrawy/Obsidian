Content Based Filtering
Vectorization(Tf-IDF) -> convert the description into a vector
Similarity metric (cosine similiartiy) -> Once the movies as converted into vectors

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 1. Create a simple dataset
data = {
    'Title': ['The Matrix', 'John Wick', 'Toy Story', 'Shrek', 'The Matrix Reloaded'],
    'Description': [
        'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'An ex-hitman comes out of retirement to track down the gangsters that took everything from him.',
        'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.',
        'A mean lord banishes fairytale creatures to the swamp of a grumpy ogre, who must go on a quest and rescue a princess for the lord in order to get his land back.',
        'Neo and the rebel leaders estimate that they have 72 hours until 250,000 probes discover and destroy Zion.'
    ]
}

df = pd.DataFrame(data)

# 2. Convert text descriptions into vectors (Numbers)
# TF-IDF removes common words like "the", "a" and highlights unique words like "hacker", "toy", "swamp".
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Description'])

# 3. Calculate Similarity
# We use Cosine Similarity to calculate how similar each description is to every other description.
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# 4. Function to get recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = df.index[df['Title'] == title][0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, 
				key=lambda x: x[1], 
				reverse=True)

    # Get the scores of the top 3 most similar movies (ignoring the movie itself)
    sim_scores = sim_scores[1:4]
    
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 3 most similar movies
    return df['Title'].iloc[movie_indices]

# --- TEST IT ---
print("Recommendations for 'The Matrix':")
print(get_recommendations('The Matrix'))

print("\nRecommendations for 'Toy Story':")
print(get_recommendations('Toy Story'))
```

|**Pros**|**Cons**|
|---|---|
|**No Cold Start for Items:** You can recommend a new movie immediately as long as it has a description. You don't need user viewing history.|**Limited Serendipity:** The system will never recommend something outside the user's known interests (e.g., it will only recommend Sci-Fi to a Sci-Fi fan).|
|**Transparency:** It is easy to explain _why_ a recommendation was made ("We recommended this because you watched X").|**Feature Engineering:** You rely heavily on good data (descriptions, tags, genres). If the descriptions are bad, the recommendations are bad.|

Hyrid -> Tf-IDF + Embeddings
```python
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# 1. The Data
# I added a tricky example: "The Matrix" vs "Computer Maintenance Video"
# They share the word "Computer" (Keyword match), but are totally different topics (Semantic mismatch).
data = {
    'Title': [
        'The Matrix', 
        'John Wick', 
        'Toy Story', 
        'The Matrix Reloaded',
        'PC Repair Guide' 
    ],
    'Description': [
        'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'An ex-hitman comes out of retirement to track down the gangsters that took everything from him.',
        'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.',
        'Neo and the rebel leaders estimate that they have 72 hours until 250,000 probes discover and destroy Zion.',
        'A guide on how to install a computer hard drive and fix the motherboard.'
    ]
}
df = pd.DataFrame(data)

# ---------------------------------------------------------
# STEP 2: Calculate Keyword Similarity (TF-IDF)
# ---------------------------------------------------------
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Description'])
keyword_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# ---------------------------------------------------------
# STEP 3: Calculate Semantic Similarity (Embeddings)
# ---------------------------------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['Description'].tolist())
semantic_sim = cosine_similarity(embeddings)

# ---------------------------------------------------------
# STEP 4: The Hybrid Logic
# ---------------------------------------------------------
def get_hybrid_recommendations(title, alpha=0.5):
    """
    alpha = 1.0  --> Pure Keyword (TF-IDF)
    alpha = 0.0  --> Pure Semantic (Embeddings)
    alpha = 0.5  --> Equal mix of both
    """
    
    # Get the index of the movie
    idx = df.index[df['Title'] == title][0]

    # Get the similarity scores from both methods
    sim_scores_keywords = keyword_sim[idx]
    sim_scores_semantics = semantic_sim[idx]

    # HYBRID FORMULA: Weighted Average
    # hybrid_score = (alpha * keyword_score) + ((1-alpha) * semantic_score)
    hybrid_scores = (alpha * sim_scores_keywords) + ((1 - alpha) * sim_scores_semantics)

    # Create a list of (index, score) tuples
    score_pairs = list(enumerate(hybrid_scores))

    # Sort by the new Hybrid Score
    score_pairs = sorted(score_pairs, key=lambda x: x[1], reverse=True)

    # Filter out the movie itself (index 0) and get top results
    score_pairs = score_pairs[1:]
    
    # Print detailed results to see the logic
    print(f"\n--- Recommendations for '{title}' (Alpha={alpha}) ---")
    print(f"{'Title':<25} | {'Hybrid':<8} | {'Keyword':<8} | {'Semantic':<8}")
    print("-" * 60)
    
    for i, score in score_pairs:
        print(f"{df['Title'].iloc[i]:<25} | {score:.4f}   | {sim_scores_keywords[i]:.4f}   | {sim_scores_semantics[i]:.4f}")

# ---------------------------------------------------------
# TEST IT
# ---------------------------------------------------------

# Scenario A: Equal Weight (Balance)
get_hybrid_recommendations('The Matrix', alpha=0.5)

# Scenario B: High Keyword Weight (Focus on exact words)
# Notice "PC Repair Guide" might jump up because it shares the word "computer".
get_hybrid_recommendations('The Matrix', alpha=0.8)
```

Hybrid:
- By adjusting alpha, you can suppress the "dumb" keyword match of the PC Repair Guide while keeping the "smart" semantic match of The Matrix Reloaded.

When to tune alpha?
- Set alpha high (0.7 - 0.9): If precise part numbers, error codes, or proper nouns (names of people/places) are critical. (e.g., E-commerce search for "iPhone 15 Pro Max").

- Set alpha low (0.1 - 0.3): If the user is exploring or browsing general topics. (e.g., Netflix "Movies like this").
---
#### Collaborative Filtering
#### 1. The Core Idea: "Wisdom of the Crowd"
There are two main ways to do this:
1. **User-Based:** "Find users similar to **me**, and recommend what **they** liked."
2. **Item-Based:** "Find items similar to **this item**, based on how **other people** rated them."
```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 1. Create a Dataset (User Ratings)
# 0 means the user hasn't watched the movie yet.
data = {
    'User': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'The Matrix': [5, 5, 1, 0, 1],
    'Star Wars':  [5, 5, 1, 0, 1], # Highly correlated with Matrix (Action fans)
    'Titanic':    [1, 1, 5, 5, 5], # Correlated with Notebook (Romance fans)
    'Notebook':   [0, 1, 5, 5, 5]
}

df = pd.DataFrame(data)
df = df.set_index('User')

print("The User-Item Matrix:")
print(df)
print("-" * 30)

# 2. Transpose the Matrix
# We want to compare Movies (Columns) to Movies, not Users to Users.
# So we flip the table: Rows become Movies.
movie_matrix = df.T 

# 3. Calculate Similarity
# We calculate the cosine similarity between the rows (which are now movies).
# If User A and User B both rated "Matrix" and "Star Wars" highly, the similarity is high.
movie_sim = cosine_similarity(movie_matrix)

# Convert to DataFrame for readability
movie_sim_df = pd.DataFrame(movie_sim, index=movie_matrix.index, columns=movie_matrix.index)

# 4. The Recommendation Function
def get_collaborative_recs(movie_title, top_n=2):
    # Get similarity scores for the requested movie
    scores = movie_sim_df[movie_title]
    
    # Sort descending
    scores = scores.sort_values(ascending=False)
    
    # Exclude the movie itself
    scores = scores.drop(movie_title)
    
    return scores.head(top_n)

# --- TEST IT ---
print("\nIf you liked 'The Matrix', you might like:")
print(get_collaborative_recs('The Matrix'))

print("\nIf you liked 'Titanic', you might like:")
print(get_collaborative_recs('Titanic'))
```

### How it Works (The Mechanics)
Look closely at the data in the code:
- **Alice & Bob** both loved _The Matrix_ (5) and _Star Wars_ (5), but hated _Titanic_ (1).
- **Charlie, David, & Eve** loved _Titanic_ (5) and _The Notebook_ (5), but hated _The Matrix_ (1).

The algorithm doesn't know that _The Matrix_ is a sci-fi movie. It only knows that **the specific people who liked The Matrix ALSO liked Star Wars.**

Mathematically, the vector for _The Matrix_ looks like `[5, 5, 1, 0, 1]`. The vector for _Star Wars_ looks like `[5, 5, 1, 0, 1]`. Since these vectors are identical, the similarity is **1.0**.

### The "Matrix Factorization" (Advanced)
The code above works great for small data, but real-world data (like Netflix) is **sparse**. Most users have rated only 50 out of 10,000 movies.

To solve this, pros use **Matrix Factorization (SVD)**. It breaks the big matrix down into "Latent Features."
- It effectively "guesses" the missing ratings.
- If Alice rated _Matrix_ 5/5, SVD infers she likes "Sci-Fi" (Latent Feature 1).
- Since _Inception_ is high in "Sci-Fi", SVD predicts Alice will rate _Inception_ 5/5, even if she has never seen it.

|**Feature**|**Content-Based (What we did first)**|**Collaborative (What we did now)**|
|---|---|---|
|**Basis**|Item Attributes (Keywords, Genre).|User Behavior (Votes, Ratings).|
|**New Items**|**Excellent.** Can recommend a movie the second it is uploaded.|**Fails (Cold Start).** Can't recommend a new movie until someone rates it.|
|**New Users**|**Excellent.** Just ask "What genres do you like?"|**Fails (Cold Start).** Needs user history to find similar users.|
|**Serendipity**|**Low.** Only recommends more of the same (Sci-Fi -> Sci-Fi).|**High.** Can recommend unexpected items (e.g., "People who like Sci-Fi usually also like this specific Anime").|

---
The "Two-Tower" architecture is exactly what you are looking for. It is the modern industry standard (used by YouTube, Netflix, Instagram) because it solves the biggest problem in recommendations: **How do we combine User History (Collaborative) with Item Features (Content-Based)?**

It is called "Two-Tower" because it has two separate neural networks (towers):

1. **User Tower:** Encodes everything we know about the user (Demographics, Watch History, Search Queries) into a vector.
2. **Item Tower:** Encodes everything we know about the item (Video Title, Description, Thumbnail, Tags) into a vector.

The goal is to train these two towers so that if a user likes an item, their vectors are **close together** (high dot product).

### 1. The Concept: "Meeting in the Middle"
In previous steps, we had static vectors.
- **Content-Based:** Item vector = Description embedding.
- **Collaborative:** User vector = Rating history.

In Two-Tower, the vectors are **learned**. The model learns to map "User who likes Sci-Fi" and "Movie with lasers" to the same location in vector space.

### 2. The Code: Building a Two-Tower Model

We will use `TensorFlow` / `Keras` for this. This is a simplified version of what YouTube uses for its "Retrieval" stage.

_Note: You need `tensorflow` and `tensorflow-recommenders` installed._

```python
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

# 1. Fake Data Generation
# distinct_users = 1000
# distinct_items = 1000

# Let's say we have interactions: UserID -> MovieTitle
ratings_data = pd.DataFrame({
    "user_id": ["42", "42", "50", "99", "42"], 
    "movie_title": ["The Matrix", "John Wick", "Titanic", "The Matrix", "Speed"]
})

movies_data = pd.DataFrame({
    "movie_title": ["The Matrix", "John Wick", "Titanic", "Speed", "Star Wars"]
})

# Convert to TF Datasets
ratings = tf.data.Dataset.from_tensor_slices(dict(ratings_data))
movies = tf.data.Dataset.from_tensor_slices(dict(movies_data))

# ---------------------------------------------------------
# STEP 2: The User Tower (Query Model)
# ---------------------------------------------------------
class UserModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        # Map user IDs to integers
        self.user_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=["42", "50", "99"], mask_token=None),
            # Embedding layer: transform UserID into a vector of size 32
            tf.keras.layers.Embedding(len(["42", "50", "99"]) + 1, 32)
        ])

    def call(self, inputs):
        return self.user_embedding(inputs)

# ---------------------------------------------------------
# STEP 3: The Item Tower (Candidate Model)
# ---------------------------------------------------------
class MovieModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        # Map movie titles to integers
        self.movie_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=["The Matrix", "John Wick", "Titanic", "Speed", "Star Wars"], mask_token=None),
            # Embedding layer: transform MovieTitle into a vector of size 32
            tf.keras.layers.Embedding(len(["The Matrix", "John Wick", "Titanic", "Speed", "Star Wars"]) + 1, 32)
        ])

    def call(self, inputs):
        return self.movie_embedding(inputs)

# ---------------------------------------------------------
# STEP 4: The Combined Two-Tower Model (Siamese Network)
# ---------------------------------------------------------
class TwoTowerModel(tfrs.Model):
    def __init__(self, user_model, movie_model):
        super().__init__()
        self.user_model = user_model
        self.movie_model = movie_model
        
        # The task is to predict which movie a user will watch.
        # It optimizes the "dot product" between user and movie vectors.
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=movies.batch(128).map(self.movie_model)
            )
        )

    def compute_loss(self, features, training=False):
        # Pass user features into User Tower
        user_embeddings = self.user_model(features["user_id"])
        
        # Pass movie features into Item Tower
        movie_embeddings = self.movie_model(features["movie_title"])

        # Calculate loss (how far off was the prediction?)
        return self.task(user_embeddings, movie_embeddings)

# ---------------------------------------------------------
# STEP 5: Train and Serve
# ---------------------------------------------------------
user_tower = UserModel()
item_tower = MovieModel()
model = TwoTowerModel(user_tower, item_tower)

model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

# Train!
# In reality, you'd run this for many epochs
model.fit(ratings.batch(4096), epochs=5)

# ---------------------------------------------------------
# STEP 6: Get Recommendations (Inference)
# ---------------------------------------------------------
# To recommend, we create a specialized index (BruteForce or ScaNN)
index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)

# Load the candidate movies into the index
index.index_from_dataset(
  tf.data.Dataset.zip((movies.batch(100).map(lambda x: x["movie_title"]), movies.batch(100).map(model.movie_model)))
)

# Get recommendations for User "42"
_, titles = index(tf.constant(["42"]))
print(f"Top 3 recommendations for User 42: {titles[0, :3]}")
```

### 3. Why is this better?

The Two-Tower architecture gives you the **"Best of Both Worlds"**:

1. **Flexibility (Content-Based):**
    - You can easily add extra features to the towers.
    - _User Tower Input:_ User ID + Age + Country + Last 5 Searches.
    - _Item Tower Input:_ Movie Title + Genre + Description Embedding + Director.
        
2. **Generalization (Collaborative):**
    - Because it learns from interaction data (who watched what), it captures the "wisdom of the crowd."
        
3. **Speed (Inference):**
    - Once trained, you pre-calculate all Item Vectors and save them in a Vector Database (Faiss/Pinecone).
    - When a user arrives, you only run the User Tower once to get their vector, then search the database. This is **extremely fast** ($<10$ms).
### 4. The YouTube Architecture
To visualize where this fits in a real system (like YouTube):
1. **Candidate Generation (The Two-Tower Model):**
    - **Input:** Millions of videos.
    - **Output:** The top ~100 relevant videos.
    - **Goal:** High Recall (Don't miss anything relevant).
2. **Ranking (A different model):**
    - **Input:** The 100 candidates from step 1.
    - **Output:** The top 10 to show on screen.
    - **Goal:** High Precision (Optimize for clicks/watch time).
### 5. Summary and Next Step
You have now learned the progression of Recommender Systems:
1. **Content-Based (TF-IDF):** Simple keyword matching.
2. **Semantic (Embeddings):** Understanding meaning.
3. **Collaborative (Matrix Factorization):** Understanding user behavior.
4. **Deep Learning (Two-Tower):** Combining all the above into a learnable, scalable architecture.

This is the state-of-the-art.

---
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

- **SVD (matrix factorization):** linear factorization into user/item latent vectors. 
	- Good for explicit ratings, lightweight and interpretable.
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
