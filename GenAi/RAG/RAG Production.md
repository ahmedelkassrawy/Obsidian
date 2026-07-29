# Retrieval-Augmented Generation (RAG): Key Concepts & Production Trade-offs

## 1. Retrieval Evaluation Metrics

Most commonly cited metrics capture the fundamental goal: **finding relevant documents**.

| Metric              | What it Measures                              | Focus Area                          | Requires Ground Truth? | Typical k values |
|---------------------|-----------------------------------------------|-------------------------------------|------------------------|------------------|
| **Precision@k**     | How many of the returned documents are relevant | Assesses irrelevant documents       | Yes                    | 5–20            |
| **Recall@k**        | How many of the relevant documents are returned | Coverage of all relevant items      | Yes                    | 5–20            |
| **Mean Average Precision (MAP)** | Precision averaged across relevant documents (ranking effectiveness) | Overall ranking quality             | Yes                    | —               |
| **Mean Reciprocal Rank (MRR)** | How well the model performs at the very top of the ranking | First relevant result position      | Yes                    | —               |

**Quick definitions:**
- **Precision** → Of the documents you returned, what fraction are actually relevant?
- **Recall** → Of all relevant documents in the collection, what fraction did you find?

All these metrics require **ground truth** relevance judgments.

---

## 2. Evolution of Vector Retrieval: From kNN to HNSW

### 2.1 The Scaling Problem: Exact k-Nearest Neighbors (kNN)
Simplest approach — but does **not** scale.

**How it works**
1. Embed every document + user prompt → vectors
2. Compute distance between prompt vector and **every** document vector
3. Sort by distance → return top-k

**Problem:** Linear scaling  
→ 1,000 docs = 1,000 calculations  
→ 1 billion docs = **1 billion** calculations  
→ Latency becomes unacceptable at web scale

### 2.2 Approximate Nearest Neighbors (ANN)

Trade tiny loss in accuracy for **massive** speed gains.

#### Navigable Small World (NSW)
Uses a **proximity graph**:

- Nodes = documents
- Edges = connections to nearest neighbors
- Search = greedy traversal ("hop" to closer neighbors)

Much faster — only compute distances for a small number of nodes.

#### Hierarchical Navigable Small World (HNSW)
State-of-the-art method used in most production vector databases today.

**Key innovation:** Multi-layer graph (hierarchy)

- **Top layers** → very sparse (big jumps, find general area quickly)
- **Bottom layer** → contains **all** vectors (fine-grained search)

**Search flow**
1. Start at the top (small) layer → make long jumps
2. Find best candidate → drop to next denser layer
3. Repeat until you reach the bottom layer
4. Final refinements happen very close to the target

**Comparison Table**

| Feature              | kNN (exact)               | HNSW (approximate)           |
|----------------------|---------------------------|-------------------------------|
| **Accuracy**         | 100% (guaranteed best)    | Very high (~95–99%)           |
| **Time Complexity**  | O(n)                      | ~O(log n)                     |
| **Speed at scale**   | Very slow                 | Milliseconds even for billions|
| **Precomputation**   | Minimal                   | High (build graph once)       |
| **Used in production**| Almost never (too slow)   | Yes (Pinecone, Weaviate, Qdrant, etc.) |

**Takeaway:** HNSW delivers near-perfect recall with orders-of-magnitude lower latency.

---

## 3. Chunking Strategies in RAG

| Method                     | Complexity | Performance | Notes / Trade-offs                              |
|----------------------------|------------|-------------|-------------------------------------------------|
| Fixed-width                | Low        | Baseline    | Simple, fast, but semantic breaks               |
| Recursive character splitting | Low–Medium | Good        | Respects sentence/paragraph boundaries          |
| Semantic chunking          | Medium–High| Higher      | Groups by meaning (often via embeddings)        |
| LLM-based chunking         | High       | Highest     | Most accurate but slow & expensive              |
| Context-aware chunking     | Medium–High| ↑ on any base method | Adds surrounding context; increases cost slightly |

**Recommendation:** Start with recursive character splitting → experiment with semantic/LLM chunking if quality is insufficient.

---

## 4. The Core Production Trade-off: Latency vs. Quality

> **Almost all latency in modern RAG comes from Transformer inference (LLM calls).**

### Use-case determines priority

- **Latency-critical**: E-commerce, chat support, real-time recommendations  
- **Quality-critical**: Legal, medical, scientific research

### Strategies to Reduce Latency

#### A. Optimize the Core Generation Model
1. Smaller / quantized models (e.g. 7B → 4-bit)
2. **LLM Routing**  
   - Tiny router classifies query  
   - → fast path (small model)  
   - → slow path (large reasoning model)
3. **Semantic caching** — cache common prompt ↔ response pairs
4. **Personalized cache tweaking** — small model adapts cached answer

#### B. Streamline / Remove Optional Components
Measure **incremental value** of each stage:

- Query rewriting
- Re-ranking
- Router / classifier LLMs

If it adds >300–500 ms but improves quality <1–2% → consider removing.

#### C. Faster Retrieval
- Binary / scalar quantization
- Database sharding / partitioning
- Index parameter tuning (efConstruction, M in HNSW)

### Implementation Order (when system is too slow)

| Priority | Area                  | Typical Actions                                  |
|--------|-----------------------|--------------------------------------------------|
| 1      | Core LLM              | Quantization, smaller model, routing             |
| 2      | Secondary LLM calls   | Remove / simplify re-ranker, query rewriter      |
| 3      | Retrieval             | Binary quantization, sharding, HNSW parameters   |

**Golden advice:**  
Install observability → **measure** where time is actually spent.  
Never optimize based on intuition alone.

---

## 5. The Semantic Gap — Why Most RAG Problems Are Retrieval Problems

> *"If your RAG depends solely on Vector Search... then you have a Retrieval Problem, not a Model Problem."*

The **Semantic Gap** is the disconnect between how a user phrases a query and how the source document expresses the same intent. Example:

- User: *"The product turned out to be damaged"*
- Document: *"Refund and Replacement Policy"* or *"Return Eligibility"*

An embedding model may fail to connect the two even though they share the same intent. The fix is **not** a better LLM — it's a better **retrieval pipeline**.

### Multi-stage Retrieval Architecture

In production, the retrieval pipeline typically looks like this:

```
User Query
    ↓
Query Reformulation      ← HyDE / Query Expansion
    ↓
Hybrid Retrieval          ← Vector Search + BM25
    ↓
Metadata Filtering       ← Intent tags, business categories, entity linking
    ↓
Cross-Encoder Re-ranking  ← Replace cosine similarity with a cross-encoder
    ↓
Context Compression      ← Extract relevant spans, reduce noise
    ↓
LLM Generation           ← The LLM is the last step, not the first
```

Each stage addresses a specific failure mode:

| Stage | Technique | What It Solves |
|---|---|---|
| Query Reformulation | HyDE / Query Expansion | Vague or terse queries that don't match document wording |
| Hybrid Retrieval | Vector Search + BM25 | Semantic misses (BM25 catches exact keyword matches, vectors catch meaning) |
| Metadata Filtering | Intent tags, categories, entity linking | Raw text ambiguity — structured context narrows the search space |
| Cross-Encoder Re-ranking | Cross-encoder scores on top-50 docs | Cosine similarity is a weak relevance signal; cross-encoders are far more precise |
| Graph-aware Retrieval | Knowledge Graphs + Graph Traversal | Multi-step relationships vector search can't express |
| Context Compression | Extract relevant spans | Too many noisy documents dilute LLM performance |

### The Key Insight

> "The LLM is the last step in the pipeline, not the first. Most RAG problems aren't solved by changing the model, but by improving retrieval quality and context engineering."

If you had budget to improve only one component in a RAG system, the most leveraged choice is usually the **retrieval pipeline** (multi-stage architecture) — not the embedding model, not the re-ranker, and not the chunking strategy — because it governs what reaches the LLM in the first place.
