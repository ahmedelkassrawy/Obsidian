---
description: "Hub: every note about Embeddings & Semantic Search"
type: hub
domain: ml
tags:
  - type/hub
  - topic/embeddings-and-semantic-search
---
# Embeddings & Semantic Search

> [!info] BoW, TF-IDF, Word2Vec, sentence transformers, semantic search and ANN libraries. Bridges into the ai-eng RAG notes.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/embeddings-and-semantic-search`.

## Concepts
- [[ANN Tools FAISS and ScaNN]] — Explains exact vs approximate nearest-neighbour search and compares FAISS and ScaNN, with advice on when a backend should use a raw ANN library instead of a managed vector database.
- [[Embeddings Representations And Latent Space]] — Answers what embeddings, representations and latent space have in common and how they differ, from the Machine Learning Q and AI book.
- [[NLP Concepts]] — Compares the main text-representation methods (BoW, TF-IDF, Word2Vec), then BERT vs sentence transformers, and BLEU vs ROUGE for evaluation.
- [[Pinecone]] — What an index means in Pinecone: dense (embedding) vs sparse (keyword) indexes, and how real systems combine both.
- [[Semantic Search]] — Explains semantic search versus keyword search, how embeddings plus a vector index make it work, and how it feeds into RAG, with advanced RAG techniques and evaluation metrics.
- [[Sparse Vs Dense Embeddings]] — Why sparse vectors waste dimensions and dense ones do not, then the progression from Word2Vec (word meaning) to transformers (context-aware tokens) to SBERT (one vector per sentence).
- [[Stanford CS224n]] — A very long single-file NLP walkthrough from Bag of Words and TF-IDF through embeddings, RNNs and attention to BERT's encoder internals, with formulas and mermaid diagrams.
- [[Transformers]] — A synthesis note that stitches the transformer story together: why RNNs fell short, how attention fixed it, then embeddings, positional encoding, multi-head attention and the full stack.
- [[Two-Tower Network architecture for collaborative filtering]] — Explains collaborative filtering and how the two-tower network is its deep-learning form, including contrastive training and ANN retrieval at serving time.

## How-tos & recipes
- [[Building a Two-Tower Retrieval System with PyTorch and FAISS]] — Builds a two-tower retrieval model on MovieLens 1M in PyTorch: feature encoding, contrastive training with in-batch negatives, then serving the item tower through FAISS.
- [[Modern Tokenization]] — Shows modern subword tokenization with the BERT tokenizer and how to run text through BERT to get contextual embeddings.
- [[NLP]] — An end-to-end NLP guide with code: lowercasing, stop words, tokenization, stemming vs lemmatization, n-grams, feature extraction, model training and saving.
- [[NLP - AI BOOK]] — Shows the Keras text pipeline end to end: Tokenizer to sequences, stop-word removal, padding, an Embedding layer, and a TextVectorization-based classification model.
- [[Recommendation sys]] — Builds content-based recommenders step by step: TF-IDF vectors over descriptions, cosine similarity, and where keyword matching fails versus semantic embeddings.
- [[Text Classification]] — Four ways to classify text: sentence-transformer embeddings plus logistic regression, zero-shot cosine similarity against label embeddings, and a T5 generative classifier.
- [[Cosine similarity]] `raw` — A numpy function that computes cosine similarity between a query vector and a list of candidate vectors.
- [[LLM And Embedding Provider Interface]] `stub` — An abstract base class sketch for swapping LLM and embedding providers behind one interface.
- [[Semantic Caching - Redis]] `raw` — Pasted code for a Redis semantic cache: a cache-optimized embedding model, loading FAQ data into the cache, and a TTL policy to keep it fresh.

## References & cheat sheets
- [[Cosine Similarity]] `stub` — A tiny content-based recommender: embed item tags with a sentence transformer, build a cosine similarity matrix, and return the closest titles.

## Book notes
- [[Ch3. Eval]] — Chip Huyen Ch3: why evaluation is its own hard problem, the entropy/perplexity metrics, exact vs subjective evaluation, embedding similarity, and AI-as-a-judge.
- [[Text Classification - AI Book]] — Book-chapter notes on text classification: turning a corpus into vectors with CountVectorizer and TfidfVectorizer, then training and scoring a classifier on that matrix.
- [[Word2Vec And Word Embeddings]] `stub` — A paragraph on Word2Vec - predicting a word from its context so that words used alike end up near each other in the embedding space.

## Course notes
- [[Text Representation - BoW TF-IDF And N-Grams]] — NLP lecture 2: turning text into numbers with Bag of Words, N-grams, TF-IDF and one-hot encoding, worked by hand and then with sklearn vectorizers into a classifier.

## Interviews
- [[Designing Instagram's Feed Ranking Model]] — A mock Meta ML system design interview: framing Instagram feed ranking, the 3-stage retrieval/ranking/re-rank pipeline, features, offline vs online metrics, and the model architecture.

## Related hubs
[[NLP Preprocessing]], [[Vector Search]], [[Recommender Systems]], [[Transformers]], [[Classification]], [[LLM Internals]]

## Notes to self (from the audit)
- [[Word2Vec And Word Embeddings]]: 84 words from a book chapter that was never finished.
- [[Stanford CS224n]]: Not a raw lecture transcript despite the name - it is a 13.5k-word structured guide with 200+ headings and no CS224n lecture content. Too big for one note: split it per topic and rename.
- [[Semantic Search]]: Reads as AI-engineering material - may belong in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
