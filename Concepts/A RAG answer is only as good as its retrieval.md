---
description: "In RAG the model can only use what retrieval hands it, so most quality problems are retrieval problems: chunking, search method and ranking, not the LLM."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/rag
hubs:
  - "[[RAG]]"
created: 2026-10-01
---
# A RAG answer is only as good as its retrieval

## The idea
RAG has two halves: retrieve relevant chunks, then have the LLM answer using them. If retrieval misses the right chunk, even the best model can't recover. It will answer from memory or make something up. So when a RAG system gives bad answers, check retrieval first.

The levers are mostly on the retrieval side: how you chunk (small chunks match precisely but lose context, which is why parent-child chunking exists), how you search (dense, keyword, or hybrid), whether you rewrite the query, and whether you rerank the top results before passing them on.

You also measure the two halves separately. Retrieval metrics (did the right chunk come back?) are a different question from generation metrics (was the answer faithful to the chunks?).

## Example
A support bot keeps answering an error-code question wrong. The answer is in the docs, but embeddings didn't match the exact code. Adding keyword search (hybrid) fixes it without touching the prompt or the model.

## Connects to
- [[Embeddings turn meaning into distance]] — the usual retrieval engine, and its blind spot on exact terms.
- [[Exact nearest-neighbour search doesn't scale, so vector databases approximate]] — ANN recall loss is one place chunks quietly go missing.
- [[The context window is a budget, not a bucket]] — retrieving more chunks isn't free. Extra noise can make answers worse.

## Sources
- [[RAG Production]]
- [[RAG Production Best Practices]]
- [[Anthropic RAG Cheatsheet]]
- [[Parent-child chunking]]
- [[GraphRAG]]

## 30-second answer
> RAG quality is capped by retrieval: if the right chunk isn't retrieved, the model can't use it. So I debug retrieval first (chunking, hybrid search, query rewriting, reranking), and I evaluate retrieval and generation separately.
