Parent-child chunking (often called "Small-to-Big Retrieval") is an advanced Retrieval-Augmented Generation (RAG) technique that solves a fundamental trade-off: **search precision vs. context completeness.**

By decoupling the text used for _searching_ from the text used for _generation_, you get the best of both worlds.

Based on your architecture diagram, here is exactly how this process works.

### The Problem It Solves

- **If chunks are too small:** A vector search is highly accurate because the embedding represents a single, specific idea. However, when you pass that tiny chunk to an LLM (like GPT-4o-mini), it lacks the surrounding context to give a thorough answer.
    
- **If chunks are too large:** An LLM gets great context, but the vector search becomes inaccurate. The embedding of a massive block of text "averages out" the meaning, making it harder to match specific user queries.
    

### 1. Ingestion Time (The Split)

During ingestion, your pipeline creates a hierarchy:

- **The Parents:** Your raw documents are split into large, comprehensive blocks (2,000 characters with a 200-character overlap). These are stored in a simple document store (`parents_store.json`) with unique IDs.
    
- **The Children:** Each Parent chunk is further divided into smaller pieces (400 characters with a 50-character overlap).
    
- **The Link:** Crucially, each Child chunk is tagged with its `parent_id` as metadata. Only these smaller Child chunks are converted into embeddings and stored in your Pinecone Vector Database and BM25 index.
    

### 2. Query Time (The Reassembly)

When a user asks a question, the system executes a "bait and switch":

- **Step A (The Search):** Your `EnsembleRetriever` searches the database of 400-character Child chunks. Because these chunks are small and focused, the semantic match (cosine similarity) and keyword match (BM25) are highly accurate.
    
- **Step B (Over-fetching):** You retrieve `k * 2` children. You intentionally fetch extra children because multiple relevant Child chunks might belong to the exact same Parent.
    
- **Step C (Parent Expansion):** Before sending anything to the LLM, the system looks at the `parent_id` metadata of the top Child chunks. It takes those IDs, goes to `parents_store.json`, and pulls the full 2,000-character Parent chunks.
    
- **Step D (Deduplication):** If three of your retrieved children belong to "Parent A", you only pass "Parent A" to the LLM once.

### The Result

Your GPT-4o-mini model receives the full 2,000-character sections, preserving the narrative flow, formatting, and surrounding context of the document, while your retrieval mechanism maintains the pinpoint accuracy of a 400-character search.

```python
def split_parent_child(
    documents: List[Document],
) -> Tuple[List[Document], List[Document]]:
    """
    Parent-Child chunking strategy.

    For each source document:
      → N parent chunks (PARENT_CHUNK_SIZE chars)
          → M child chunks per parent (CHILD_CHUNK_SIZE chars)

    children carry parent_id in metadata → used at retrieval time
    to swap the small child for the full parent context.

    Returns
    -------
    parents  : List[Document]  stored in Pinecone namespace="parents"
    children : List[Document]  embedded & stored in namespace="children"
    """
    parents:  List[Document] = []
    children: List[Document] = []

    for doc in documents:
        source = doc.metadata.get("source", "")

        # ── 1. Parent chunks ─────────────────────────────────────────────────
        for p_idx, parent_text in enumerate(
            _parent_splitter.split_text(doc.page_content)
        ):
            parent_id = str(uuid.uuid4())

            parent = _make_doc(parent_text, {
                **doc.metadata,                     # inherit source, etc.
                "doc_id":        parent_id,
                "chunk_type":    "parent",
                "parent_index":  p_idx,
                "section_title": _first_heading(parent_text),
                "char_count":    len(parent_text),
                "source":        source,
            })
            parents.append(parent)

            # ── 2. Child chunks ──────────────────────────────────────────────
            for c_idx, child_text in enumerate(
                _child_splitter.split_text(parent_text)
            ):
                child = _make_doc(child_text, {
                    **doc.metadata,
                    "doc_id":        str(uuid.uuid4()),
                    "parent_id":     parent_id,     # ← key link
                    "chunk_type":    "child",
                    "child_index":   c_idx,
                    "section_title": _first_heading(child_text),
                    "char_count":    len(child_text),
                    "source":        source,
                })
                children.append(child)

    logger.info(
        f"🌲 Split → {len(parents)} parents, "
        f"{len(children)} children from {len(documents)} docs"
    )
    return parents, children
```