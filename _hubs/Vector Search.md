---
description: "Hub: every note about Vector Search"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/vector-search
---
# Vector Search

> [!info] Index types, ANN and HNSW, choosing a vector database, PGVector and Pinecone. Missing: a benchmark you ran yourself.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/vector-search`.

## Concepts
- [[ANN Tools FAISS and ScaNN]] — Explains exact vs approximate nearest-neighbour search and compares FAISS and ScaNN, with advice on when a backend should use a raw ANN library instead of a managed vector database.
- [[Anthropic RAG Cheatsheet]] — Anthropic's contextual-retrieval writeup: why embeddings miss exact matches, how prepending context to each chunk fixes it, using prompt caching to make it affordable, and reranking on top.
- [[Choosing A Vector Database]] — A decision framework for picking a vector database: scale brackets decide the shortlist, then cost vs operations, and the reminder that vector search alone always needs hybrid help.
- [[GraphRAG]] — Why plain RAG fails on relationship questions and how GraphRAG fixes it, plus the steps to build the knowledge graph: extraction of entities and relationships, and ontology design.
- [[Pinecone]] — What an index means in Pinecone: dense (embedding) vs sparse (keyword) indexes, and how real systems combine both.
- [[RAG Production]] — The production trade-offs in RAG: retrieval and generation metrics, why exact kNN does not scale and how ANN/HNSW replaces it, and chunking choices.
- [[RAG Production Best Practices]] — Production RAG strategies: query rewriting with a rephraser, and what has to change when scaling a RAG system up.
- [[Semantic Search]] — Explains semantic search versus keyword search, how embeddings plus a vector index make it work, and how it feeds into RAG, with advanced RAG techniques and evaluation metrics.
- [[Sparse Vs Dense Embeddings]] — Why sparse vectors waste dimensions and dense ones do not, then the progression from Word2Vec (word meaning) to transformers (context-aware tokens) to SBERT (one vector per sentence).
- [[Two-Tower Network architecture for collaborative filtering]] — Explains collaborative filtering and how the two-tower network is its deep-learning form, including contrastive training and ANN retrieval at serving time.

## How-tos & recipes
- [[Building a Two-Tower Retrieval System with PyTorch and FAISS]] — Builds a two-tower retrieval model on MovieLens 1M in PyTorch: feature encoding, contrastive training with in-batch negatives, then serving the item tower through FAISS.
- [[LlamaIndex RAG Pipeline]] — The LlamaIndex RAG pipeline end to end: loading with readers, transformations and chunking, adding metadata and embeddings, and building the index.
- [[Neo4j]] — Using Neo4j for AI work: the Cypher queries to explore data, creating and querying a vector index, generating embeddings with genai.vector.encode, and wiring a GraphRAG pipeline.
- [[Advanced RAG]] `stale` — Two advanced retrievers explained with code: the self-querying retriever that turns a question into a metadata filter, and the parent-document retriever.
- [[Cosine similarity]] `raw` — A numpy function that computes cosine similarity between a query vector and a list of candidate vectors.
- [[PGVector]] `raw` — Pasted PGVector code: running Postgres with pgvector in Docker, the async PGVector store, the database functions used, and the SQLAlchemy Result methods for reading rows back.
- [[RAG]] `stale` — End-to-end RAG guide: loading and splitting documents, embeddings and a vector store, retrieval, and generation.
- [[RAG Hybrid Search & Reranking]] `stale` — Hybrid retrieval explained and implemented: dense embeddings plus BM25 keyword search, merged and then reranked before the model sees the chunks.

## Book notes
- [[RAG And Agents - AI Engineering Book Ch6]] — Chip Huyen Ch6 notes on RAG and agents: why context construction matters, the RAG architecture, term-based vs embedding-based retrieval, and how retrieval feeds agents.

## Project notes
- [[RAG POC Notes]] — How a proof-of-concept retriever evolved into a 3-stage production pipeline: hybrid vector plus BM25 candidates, FlashRank cross-encoder reranking, and score-aware returns.

## Related hubs
[[RAG]], [[Embeddings & Semantic Search]], [[Recommender Systems]], [[LangChain]], [[LlamaIndex]], [[Transformers]]

## Notes to self (from the audit)
- [[LlamaIndex RAG Pipeline]]: Contains a hardcoded API key - rotate it.
- [[Advanced RAG]]: Uses pre-1.0 langchain.llms / langchain.vectorstores / langchain.chains imports - port before reusing.
- [[RAG Hybrid Search & Reranking]]: Implementation uses pre-1.0 RetrievalQA and langchain.vectorstores - port before reusing.
- [[RAG]]: Uses pre-1.0 langchain.embeddings / vectorstores / chains imports and has a hardcoded API key - port the code and rotate the key.
- [[Semantic Search]]: Reads as AI-engineering material - may belong in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
