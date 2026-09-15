---
description: "Hub: every note about Recommender Systems"
type: hub
domain: ml
tags:
  - type/hub
  - topic/recommender-systems
---
# Recommender Systems

> [!info] Content-based filtering, collaborative filtering, two-tower retrieval with FAISS and the 3-stage pipeline. Surprisingly complete for a side topic.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/recommender-systems`.

## Concepts
- [[ANN Tools FAISS and ScaNN]] — Explains exact vs approximate nearest-neighbour search and compares FAISS and ScaNN, with advice on when a backend should use a raw ANN library instead of a managed vector database.
- [[Mastering the 3-Stage Recommendation Pipeline]] — Explains the industry-standard three-stage recommender pipeline - candidate generation, ranking, post-processing - and why serving at scale needs it.
- [[Two-Tower Network architecture for collaborative filtering]] — Explains collaborative filtering and how the two-tower network is its deep-learning form, including contrastive training and ANN retrieval at serving time.

## How-tos & recipes
- [[Building a Two-Tower Retrieval System with PyTorch and FAISS]] — Builds a two-tower retrieval model on MovieLens 1M in PyTorch: feature encoding, contrastive training with in-batch negatives, then serving the item tower through FAISS.
- [[Recommendation sys]] — Builds content-based recommenders step by step: TF-IDF vectors over descriptions, cosine similarity, and where keyword matching fails versus semantic embeddings.

## References & cheat sheets
- [[Recommender Systems]] — A consolidated recommender-systems reference: the collaborative filtering pipeline, SVD vs neural collaborative filtering, and runnable pivot-table and surprise examples.
- [[Cosine Similarity]] `stub` — A tiny content-based recommender: embed item tags with a sentence transformer, build a cosine similarity matrix, and return the closest titles.

## Interviews
- [[Designing Instagram's Feed Ranking Model]] — A mock Meta ML system design interview: framing Instagram feed ranking, the 3-stage retrieval/ranking/re-rank pipeline, features, offline vs online metrics, and the model architecture.

## Related hubs
[[Embeddings & Semantic Search]], [[Vector Search]], [[ML System Design]], [[Evaluation Metrics]], [[PyTorch]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
