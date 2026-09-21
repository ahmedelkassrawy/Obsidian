---
description: "Hub: every note about RAG"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/rag
---
# RAG

> [!info] The deepest hub in the vault: chunking strategies, HyDE, sentence-window, parent-child, GraphRAG, hybrid search, reranking, and production trade-offs. Six of these notes run on pre-1.0 LangChain code.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/rag`.

## Concepts
- [[Anthropic RAG Cheatsheet]] — Anthropic's contextual-retrieval writeup: why embeddings miss exact matches, how prepending context to each chunk fixes it, using prompt caching to make it affordable, and reranking on top.
- [[Choosing A Vector Database]] — A decision framework for picking a vector database: scale brackets decide the shortlist, then cost vs operations, and the reminder that vector search alone always needs hybrid help.
- [[Fine-Tuning Use Cases And Hyperparameters]] — When fine-tuning is the right call: real-world uses, whether it adds new knowledge, how it compares to RAG, and the hyperparameters that matter during training.
- [[GraphRAG]] — Why plain RAG fails on relationship questions and how GraphRAG fixes it, plus the steps to build the knowledge graph: extraction of entities and relationships, and ontology design.
- [[Parent-child chunking]] — Parent-child (small-to-big) chunking: search over small precise chunks but hand the model the larger parent chunk, so precision and context stop fighting each other.
- [[Pinecone]] — What an index means in Pinecone: dense (embedding) vs sparse (keyword) indexes, and how real systems combine both.
- [[RAG Production]] — The production trade-offs in RAG: retrieval and generation metrics, why exact kNN does not scale and how ANN/HNSW replaces it, and chunking choices.
- [[RAG Production Best Practices]] — Production RAG strategies: query rewriting with a rephraser, and what has to change when scaling a RAG system up.
- [[Semantic Search]] — Explains semantic search versus keyword search, how embeddings plus a vector index make it work, and how it feeds into RAG, with advanced RAG techniques and evaluation metrics.

## How-tos & recipes
- [[LlamaIndex RAG Pipeline]] — The LlamaIndex RAG pipeline end to end: loading with readers, transformations and chunking, adding metadata and embeddings, and building the index.
- [[Neo4j]] — Using Neo4j for AI work: the Cypher queries to explore data, creating and querying a vector index, generating embeddings with genai.vector.encode, and wiring a GraphRAG pipeline.
- [[Advanced RAG]] `stale` — Two advanced retrievers explained with code: the self-querying retriever that turns a question into a metadata filter, and the parent-document retriever.
- [[Hyde RAG]] `stale` — HyDE explained and implemented: have the model write a fake answer first, embed that instead of the question, and retrieve against it.
- [[RAG]] `stale` — End-to-end RAG guide: loading and splitting documents, embeddings and a vector store, retrieval, and generation.
- [[RAG Hybrid Search & Reranking]] `stale` — Hybrid retrieval explained and implemented: dense embeddings plus BM25 keyword search, merged and then reranked before the model sees the chunks.
- [[Sentence Window RAG]] `stale` — Sentence-window retrieval: match on single sentences, then expand a window of neighbours around each hit so the model gets continuous context.
- [[RAG POC Snippets - Hashing Cache Async Ingest]] `raw` — Code snippets lifted from the RAG proof of concept: content hashing for duplicate detection, a global model cache, and the async document-processing function.

## Book notes
- [[FastAPI Users - Router Setup]] — The book's opening definition of RAG, spelling out what retrieve, augment and generate each mean.
- [[RAG And Agents - AI Engineering Book Ch6]] — Chip Huyen Ch6 notes on RAG and agents: why context construction matters, the RAG architecture, term-based vs embedding-based retrieval, and how retrieval feeds agents.

## Project notes
- [[2. Durable Ingestion in raaaaag (M5 W2)]] — The design calls for making the raaaaag ingestion pipeline durable: what to wrap in a workflow, how coarse each activity should be, why durable is not idempotent on its own, and when to use Celery instead.
- [[Mini-RAG Stack And Postgres Conventions]] — The Mini-RAG project stack (multilingual embeddings, Qdrant plus Postgres, Langfuse, PyMuPDF4llm) followed by the Postgres and SQLAlchemy conventions the project follows, including Alembic setup and async record creation.
- [[Project Talk to RAG]] — Project notes for a talk-to-your-documents RAG app: the extract, transform, embed and store pipeline, starting with the file-upload step.
- [[RAG POC Notes]] — How a proof-of-concept retriever evolved into a 3-stage production pipeline: hybrid vector plus BM25 candidates, FlashRank cross-encoder reranking, and score-aware returns.

## Clippings (raw)
- [[Clipping - Building Reliable Agentic AI Systems (Article)]] `raw` — Clipped case-study article on PRINCE, a production agentic RAG system for preclinical drug research: intent clarification, a planning step, researcher, reflection and writer agents, and how they built trust in it.

## Related hubs
[[Vector Search]], [[LangChain]], [[Embeddings & Semantic Search]], [[FastAPI]], [[Agents]], [[Fine-tuning]]

## Notes to self (from the audit)
- [[LlamaIndex RAG Pipeline]]: Contains a hardcoded API key - rotate it.
- [[Advanced RAG]]: Uses pre-1.0 langchain.llms / langchain.vectorstores / langchain.chains imports - port before reusing.
- [[Hyde RAG]]: Implementation uses pre-1.0 RetrievalQA and langchain.vectorstores - the idea still holds, the code does not.
- [[RAG Hybrid Search & Reranking]]: Implementation uses pre-1.0 RetrievalQA and langchain.vectorstores - port before reusing.
- [[RAG]]: Uses pre-1.0 langchain.embeddings / vectorstores / chains imports and has a hardcoded API key - port the code and rotate the key.
- [[Sentence Window RAG]]: Implementation uses pre-1.0 RetrievalQA and langchain.vectorstores - the technique is fine, the code is not.
- [[Clipping - Building Reliable Agentic AI Systems (Article)]]: Digest into AI-Eng/Agents - it is the only production multi-agent case study in the vault.
- [[Semantic Search]]: Reads as AI-engineering material - may belong in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
