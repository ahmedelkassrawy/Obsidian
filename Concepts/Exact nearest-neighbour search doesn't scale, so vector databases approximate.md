---
description: "Comparing a query against every vector is too slow at scale, so ANN indexes like HNSW give up a little recall to get huge speedups."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/vector-search
hubs:
  - "[[Vector Search]]"
created: 2026-10-01
---
# Exact nearest-neighbour search doesn't scale, so vector databases approximate

## The idea
Exact k-nearest-neighbour search compares the query to every stored vector. At a few thousand vectors that's fine. At tens of millions it's far too slow for a live request.

Approximate nearest neighbour (ANN) indexes like HNSW (a layered graph you walk toward the query) or IVF (cluster first, search only nearby clusters) skip most of the comparisons. You might miss a true neighbour now and then (lower recall), but you answer in milliseconds. Tuning parameters like HNSW's `ef_search` let you trade speed against recall on purpose.

## Example
FAISS `IndexFlatL2` is exact and fine for a prototype. Moving to HNSW or IVF is what makes it work at production scale.

## Connects to
- [[Indexes speed up reads by slowing down writes]] — same deal as a B-tree: pay build time and memory once, get cheap lookups. The difference is that ANN also gives up a bit of accuracy.
- [[Embeddings turn meaning into distance]] — this is the search half of the embeddings story.
- [[A RAG answer is only as good as its retrieval]] — lower recall here means a relevant chunk never reaches the model.

## Sources
- [[ANN Tools FAISS and ScaNN]]
- [[RAG Production]]
- [[Choosing A Vector Database]]

## 30-second answer
> Exact nearest-neighbour search is linear in the number of vectors, so it doesn't scale. ANN indexes like HNSW or IVF search only a small part of the space and trade a little recall for big speed gains. You tune that trade-off with index parameters.
