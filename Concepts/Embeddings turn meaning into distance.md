---
description: "An embedding maps text (or anything) to a vector so that similar meanings land close together, which turns 'find related things' into 'find nearby points'."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/embeddings
  - topic/nlp
hubs:
  - "[[Embeddings & Semantic Search]]"
  - "[[Vector Search]]"
created: 2026-10-01
---
# Embeddings turn meaning into distance

## The idea
Older text representations like bag-of-words and TF-IDF are sparse: one dimension per word, mostly zeros, and "car" and "automobile" share nothing. Dense embeddings squeeze meaning into a few hundred numbers learned from data, so related texts end up near each other.

That's the useful trick. Once meaning is a position, similarity is just distance (usually cosine similarity). Search, recommendations, clustering and RAG retrieval all become "find the nearest vectors".

The weak spot: embeddings capture meaning, not exact strings. A product code or error ID can get lost. That's why real systems mix in keyword search (hybrid search).

## Example
The query "how do I cancel my plan" matches a doc titled "Ending your subscription" even though they share no words. Keyword search would miss it. Embeddings find it.

## Connects to
- [[Exact nearest-neighbour search doesn't scale, so vector databases approximate]] — once everything is a vector, the next problem is finding neighbours fast.
- [[A RAG answer is only as good as its retrieval]] — embeddings are the usual retrieval engine in RAG.
- [[Attention lets every token decide what to look at]] — transformers produce contextual embeddings, where the same word gets a different vector in each sentence.

## Sources
- [[Sparse Vs Dense Embeddings]]
- [[Embeddings Representations And Latent Space]]
- [[Semantic Search]]
- [[NLP Concepts]]

## 30-second answer
> An embedding is a dense vector that represents meaning, trained so similar things land close together. That turns semantic similarity into distance, usually cosine. It's great for meaning but weak on exact terms like IDs, so production search usually combines it with keyword search.
