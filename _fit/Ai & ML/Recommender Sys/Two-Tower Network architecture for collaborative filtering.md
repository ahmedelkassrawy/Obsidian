Two-Tower Networks and Collaborative Filtering are two of the most important ideas in modern recommender systems. They're deeply connected — the Two-Tower architecture is essentially a deep learning _implementation_ of collaborative filtering's core philosophy. Let me break them down layer by layer.

---

## Collaborative Filtering: the foundation

The central idea is simple: **users with similar past behavior tend to like similar future items**. You don't need to know _why_ someone likes something — just that people like them also liked it.

There are two classic flavors — user-based (find similar users, take their ratings) and item-based (find similar items to what you liked). Both reduce to the same mathematical problem: **factorize a giant sparse user-item interaction matrix** into dense low-dimensional vectors.

Matrix factorization (e.g., SVD, ALS) learns a latent vector $\mathbf{u}_i$ for each user and $\mathbf{v}_j$ for each item such that their dot product approximates the observed rating: $\hat{r}_{ij} = \mathbf{u}_i \cdot \mathbf{v}_j$.

![[Pasted image 20260505162055.png]]

The problem with classic matrix factorization is that it represents users and items as **static ID embeddings** — there's no way to incorporate rich features like user demographics, item metadata, or real-time context. Enter the Two-Tower Network.

---

## Two-Tower Network: deep learning meets collaborative filtering

The Two-Tower (or Dual Encoder) architecture replaces the simple embedding lookup tables with two independent neural networks — one per "tower" — that can consume arbitrary feature sets and produce dense embedding vectors. The interaction between the two towers is **only a dot product at the very end**. This separation is deliberate and has profound engineering consequences.

![[Pasted image 20260505162028.png]]

The most important design choice — and the one worth really understanding — is that **the towers never interact until the very end**. This makes item embeddings independent of the query, so you can pre-compute every item embedding offline and store them in an Approximate Nearest Neighbor (ANN) index. At query time you run only the user tower (fast), then retrieve the nearest items from the index (also fast). Without this architectural constraint, you'd have to score every item individually at query time, which is completely infeasible at scale.

---

## Training: contrastive learning with in-batch negatives

The model is trained to score positive (user, item) pairs — things the user actually interacted with — higher than negative pairs. The clever trick is **in-batch negatives**: each item in a mini-batch serves as a negative sample for every other user in that batch, so you get $B^2$ training signals from just $B$ examples.

![[Pasted image 20260505162009.png]]

The popularity bias correction is subtle but critical. Mainstream items (Avengers, Taylor Swift) appear as in-batch negatives far more often than they should, causing the model to unfairly penalize their scores. Subtracting $\log P(\text{item})$ — the log frequency of the item in the corpus — re-balances this.

---

## Serving: ANN retrieval in the embedding space

After training, item embeddings are indexed in an ANN structure (FAISS, ScaNN, or similar). At serving time the flow is:

1. Run user features through the user tower → get $\bar{u} \in \mathbb{R}^{64}$
2. Query the ANN index with $\bar{u}$ → retrieve top-K nearest item embeddings
3. Pass the K candidates to a ranking model (which can use more expensive cross-features)
![[Pasted image 20260505161948.png]]