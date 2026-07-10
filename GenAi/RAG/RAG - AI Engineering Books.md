
# Chapter 6: RAG (Retrieval-Augmented Generation) and Agents

## 1. Introduction to RAG and Context Construction

To solve a task, a model requires both instructions on how to proceed and the **necessary information (context)** to do so.

- **Motivation for RAG:** AI models, like humans, are more likely to make mistakes and **hallucinate** when they are missing context or lacking information.
- **Dominating Patterns for Context Construction:**
    1. **RAG (Retrieval-Augmented Generation):** This pattern allows the model to retrieve relevant information from **external data sources**.
    2. **Agents:** The agentic pattern allows the model to use tools such as web search and news APIs to gather information.
- **Definition of RAG:** RAG is a technique that enhances a model’s generation by retrieving relevant information from **external memory sources**.
- **Examples of External Memory Sources:** An internal database, a user’s previous chat sessions, or the internet.
- **Purpose:** RAG is a technique used to construct context specific to each query, rather than using the same context for all queries, and allows inclusion of data specific to a user.

### RAG and Context Limitations

RAG emerged primarily to overcome the context limitations of early foundation models.

1. **Context Length:** Relying on context length alone is unsustainable as data constantly grows, requiring models to process ever-longer inputs.
2. **Cost and Latency:** Every extra context token incurs additional cost and potential latency. RAG allows the model to use only the **most relevant information**, reducing the number of input tokens and potentially increasing performance.

## 2. Historical Background and RAG Architecture

### Historical Context

- **Retrieve-then-generate Pattern:** This pattern was first introduced in "Reading Wikipedia to Answer Open-Domain Questions" (Chen et al., 2017). The system retrieves Wikipedia pages and uses them to generate an answer.
- **Retrieval-Augmented Generation Term:** The term RAG was coined in 2020 (Lewis et al.) in the context of "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".
- RAG enables models to access relevant information directly, helping them generate more detailed responses while **reducing hallucinations**.

### RAG System Architecture

A basic RAG system consists of two main components:

1. **Retriever:** Retrieves information from external memory sources.
2. **Generator (Generative Model):** Generates a response based on the retrieved information (context relevant to the query).

#### The Role of the Retriever

The success of a RAG system heavily depends on the quality of its retriever. The retriever has two main functions:

1. **Indexing:** Processing data so it can be quickly retrieved later.
2. **Querying:** Sending a query to retrieve relevant data.

In modern RAG systems, the retriever and generator are often trained separately, and developers frequently use **off-the-shelf** components.

## 3. Retrieval Algorithms

Retrieval, which is the backbone of systems like search engines, is a century-old concept. Retrieval algorithms rank documents based on their **relevance to a given query**.

The retrieval mechanisms discussed are:

1. **Term-based retrieval** (Sparse).
2. **Embedding-based retrieval** (Dense/Semantic).

### Sparse Versus Dense Retrieval

Retrieval algorithms are often categorized based on whether they use sparse or dense vectors:

|Category|Vector Type|Characteristics|Associated Retrieval Type|
|:--|:--|:--|:--|
|**Sparse Retrievers**|**Sparse vectors** (majority of values are zero).|Represented using a **one-hot vector** where 1 corresponds to the index of a term in the vocabulary.|Term-based retrieval.|
|**Dense Retrievers**|**Dense vectors** (majority of values are non-zero).|Generated via embeddings.|Embedding-based retrieval (Semantic retrieval).|

### Term-based Retrieval (Lexical Retrieval)

Term-based retrieval finds relevant documents using **key-words** (lexical retrieval).

#### Challenges with Term-based Retrieval

- Documents may contain the necessary term but not enough context.
- It assumes that the term appearing more frequently (**term frequency, TF**) makes the document more relevant, which is not always true.
- Prompts often contain non-informative, common words (e.g., "for," "at," "home") that complicate relevance scoring.

#### Key Term-based Metrics and Algorithms

- **Inverse Document Frequency (IDF):** A metric where a term's importance is **inversely proportional** to the number of documents it appears in. The higher the IDF, the more important the term.
- **TF-IDF:** An algorithm that combines **Term Frequency (TF)** and **Inverse Document Frequency (IDF)**.
- **BM25 (Okapi BM25):** The 25th generation of the Best Matching Algorithm. BM25 improves upon naive TF-IDF by **normalizing term frequency scores by document length**. It often serves as a formidable baseline for retrieval applications.
- **Tokenization/N-grams:** Retrieval requires processing queries by breaking them into individual terms (tokenization). Using **n-grams** (e.g., bigrams like "hot dog") can help mitigate issues where breaking up multi-word terms loses their original meaning.

### Embedding-based Retrieval (Semantic Retrieval)

Embedding-based retrieval aims to rank documents based on how closely their **semantic meaning** aligns with the query. This approach is known as **semantic retrieval**.

- **Benefit:** Allows for the retrieval of documents that are relevant in meaning, even if they do not share the exact same keywords (e.g., searching "transformer architecture" may retrieve information about the electronic device _and_ the movie _Transformers_).

#### Embedding-based Retrieval Workflow

Embedding-based retrieval requires an extra indexing function: converting original data chunks into **embeddings** and storing them in a **vector database**. The querying process has two main steps:

1. **Embedding Model:** Converts the query into an embedding vector using the same model used during indexing.
2. **Retriever:** Fetches the $k$ data chunks whose embeddings are **closest** to the query embedding.

## 4. Vector Databases and Vector Search

Embedding-based retrieval necessitates the use of a **vector database** to store the generated embeddings.

- **Vector Search:** The core challenge is finding vectors in the database that are close to the query vector.
- **k-Nearest Neighbors (k-NN):** The naive solution for vector search. It involves:
    1. Computing similarity scores (e.g., using **cosine similarity**) between the query embedding and _all_ vectors in the database.
    2. Ranking vectors by scores.
    3. Returning the top $k$ vectors.
- **Limitation of k-NN:** It is computationally heavy and slow, suitable only for small datasets.
- **Approximate Nearest Neighbor (ANN):** For large datasets, vector search typically relies on ANN algorithms to speed up the process while trading some accuracy.

### Significant Vector Search Algorithms

|Algorithm|Description|Implementation Detail|
|:--|:--|:--|
|**HNSW (Hierarchical Navigable Small World)**|Constructs a multi-layer graph. Nodes represent vectors, and edges connect similar vectors.|Provides **high accuracy and fast query times**, but index creation requires significant time and memory.|
|**LSH (Locality-sensitive hashing)**|Uses hashing to improve similarity search speed and trading some accuracy.|Is quicker and less memory-intensive to create than HNSW, but results in slower and less accurate queries.|
|**IVF (inverted file index)**|Uses K-means clustering to organize similar vectors into clusters. Querying finds centroid clusters closest to the query.|IVF is often the backbone of **FAISS** (Facebook AI Similarity Search).|
|**Annoy**|A tree-based approach that builds multiple binary trees, splitting vectors into two branches using line and splitting vectors.|Popular for gathering candidate neighbors quickly.|
|**Product Quantization**|Reduces the dimensionality of vectors, making computations much faster.|

## 5. Comparing Retrieval Approaches

### Trade-offs Between Term-based and Embedding-based Retrieval (Hybrid Search)

Term-based retrieval is generally **faster** than embedding-based retrieval. However, embedding-based retrieval can achieve better performance with **finetuning**.

Combining the advantages of different retrieval algorithms (term-based and embedding-based) is called **hybrid search**.

|Feature|Term-based Retrieval|Embedding-based Retrieval (Semantic)|
|:--|:--|:--|
|**Querying Speed**|**Much faster** than embedding-based retrieval.|Query embedding generation and vector search can be slow.|
|**Performance**|Typically strong out of the box, but hard to improve. Can retrieve wrong documents due to term ambiguity.|Allows for the use of more natural queries, focusing on **semantics**. Can outperform term-based retrieval with finetuning.|
|**Cost**|**Much cheaper**.|Vector storage, embedding, and vector search solutions can be expensive. Generating embeddings for large datasets (e.g., 100 million documents) is costly and requires frequent regeneration if data changes.|

## 6. Retrieval Optimization Tactics

Optimizing retrieval involves tactics that increase the chance of fetching relevant documents. Key tactics include chunking strategy, reranking, query rewriting, and contextual retrieval.

### A. Chunking Strategy

Chunking is the process of splitting documents into **manageable chunks** before indexing. The chunking strategy used can significantly impact the performance of the retrieval system.

- **Simplest Strategy:** Splitting documents into chunks of equal length (based on characters, words, sentences, or paragraphs).
    - _Example Size:_ 2,048 characters or 512 words.
- **Recursive Splitting:** Using increasingly smaller units until the chunk fits within the maximum size.
- **Overlap:** Splitting chunks with overlap ensures that important boundary information (which might link two chunks) is preserved, preventing information loss. Overlap size might be around 20 characters.
- **Chunk Size Constraint:** The chunk size must not exceed the maximum context length of the generative model or the embedding model's context limit.

#### Chunk Size Trade-offs

- **Smaller Chunks:** Allow for **more diverse information** and enable fitting more chunks into the model’s context. However, they risk splitting crucial information, leading to retrieval failure.
- **Larger Chunks:** Provide a wider range of information, potentially enabling the model to produce a better answer.
- **Overhead:** Smaller chunks increase computational overhead, as there are more chunks to index and more embedding vectors to generate and store.

### B. Reranking

Reranking refines the initial document rankings provided by the retriever to make them more accurate.

- **Purpose:** Reranking is especially useful for **reducing the number of retrieved documents** or fitting them into the model’s context.
- **Mechanism:** A common pattern is using a cheap retriever to fetch many candidates, followed by a more expensive mechanism (the reranker) to refine the candidates.
- **Temporal Reranking:** Documents can be reranked based on time, prioritizing **more recent data**.
- **Reciprocal Rank Fusion (RRF):** An algorithm used for combining different rankings, often applied when multiple retrievers fetch candidates simultaneously.

## 7. Evaluating RAG Systems

To summarize, the quality of a RAG system must be evaluated end-to-end, considering both the component (retriever) and the overall RAG outputs.

The general evaluation steps are:

1. Evaluate the **retrieval quality**.
2. Evaluate the final **RAG outputs**.
3. Evaluate the embeddings (for embedding-based retrieval).

### Evaluation Metrics for Retriever Quality

Two metrics are often used in RAG evaluation frameworks, both requiring a curated evaluation set where documents are annotated as relevant or not relevant:

1. **Context Precision:** Measures the percentage of retrieved documents that are relevant to the query.
2. **Context Recall (or Context Relevance):** Measures the percentage of all relevant documents (in the database) that were successfully retrieved.

When evaluating the **ranking** of retrieved documents, metrics such as **NDCG** (normalized discounted cumulative gain), **MAP** (Mean Average Precision), and **MRR** (Mean Reciprocal Rank) are used.

### Indexing and Querying Performance Metrics

Retrieval systems often involve trade-offs between indexing speed/memory and querying accuracy/speed. Metrics used to compare algorithms (e.g., HNSW vs. LSH) include:

- **Recall:** The fraction of the nearest neighbors found by the algorithm.
- **Query per Second (QPS):** The number of queries the algorithm can handle per second (critical for high-traffic applications).
- **Build time:** The time required to build the index (important if data changes frequently).
- **Index size:** The size of the index created, relevant for scalability and storage.

**BEIR (Benchmarking IR)** is an evaluation harness designed to support retrieval evaluation against 14 common benchmarks.

--- 
## Reranking Documents

- **Purpose**: Improves initial document rankings from retriever for accuracy.
- **Use Case**: Reduces number of retrieved documents to fit model’s context or minimize input tokens.
- **Common Pattern** :
    - **Step 1**: Cheap, less precise retriever fetches candidate documents.
    - **Step 2**: More precise, expensive mechanism reranks candidates.
- **Time-Based Reranking**:
    - Prioritizes recent data.
    - Useful for time-sensitive applications (e.g., news aggregation, email chatbots, stock market analysis).
- **Context Reranking vs. Search Reranking** :
    - **Search Reranking**: Exact position (e.g., 1st or 5th) is critical.
    - **Context Reranking**: Order matters less; inclusion in context is key.
    - Models process documents better at context’s beginning/end .

## Query Rewriting

- **Also Known As**: Query reformulation, normalization, or expansion.
- **Purpose**: Clarifies ambiguous queries using conversation context.
- **Example**:
    - User: “When was the last time John Doe bought something from us?”
    - AI: “John last bought a Fruity Fedora hat two weeks ago, on January 3, 2030.”
    - User: “How about Emily Doe?”
    - Rewritten Query: “When was the last time Emily Doe bought something from us?”
- **Techniques**:
    - **Traditional Search**: Uses heuristics for rewriting.
    - **AI Applications**: Uses AI models with prompts like:
        
        > “Given the following conversation, rewrite the last user input to reflect what the user is actually asking.”
        
    - Can involve identity resolution (e.g., “How about his wife?” requires database lookup).
- **Challenges**:
    - Avoid hallucinating answers if context/data is missing.

## Contextual Retrieval

- **Goal**: Augment document chunks with context to improve retrieval.
- **Techniques**:
    - **Metadata Augmentation**:
        - Add tags, keywords, or extracted entities (e.g., error code EADDRNOTAVAIL).
        - For e-commerce: Include product descriptions, reviews, or media captions.
    - **Question Augmentation**:
        - Add related questions to chunks (e.g., for customer support articles: “How to reset password?”, “I forgot my password”).
    - **Context from Original Document**:
        - If document is split into chunks, augment each chunk with original document’s title, summary, or AI-generated context.
- **Anthropic’s Approach**:
    - Generate 50-100 token context for each chunk using prompt:
        
        ```latex
        <document>
        {{WHOLE_DOCUMENT}}
        </document>
        Here is the chunk we want to situate within the whole document:
        <chunk>
        {{CHUNK_CONTENT}}
        </chunk>
        Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
        ```
        
    - Prepend context to chunk, then index for retrieval (see Figure 6-5).

## Evaluating Retrieval Solutions

- **Key Factors**:
    - **Retrieval Mechanisms**: Does it support hybrid search?
    - **Vector Database**:
        - Supported embedding models and vector search algorithms.
    - **Scalability**:
        - Data storage and query traffic handling.
        - Suitable for specific traffic patterns.
    - **Indexing**:
        - Time to index data.
        - Bulk processing capacity (add/delete).
    - **Query Latency**: Varies by retrieval algorithm.
    - **Pricing (Managed Solutions)**:
        - Based on document/vector volume or query volume.
    - **Enterprise Features**: Access control, compliance, data/control plane separation.

## Key Takeaways

- Reranking refines document selection for better model context or efficiency.
- Query rewriting clarifies ambiguous user inputs, critical for accurate retrieval.
- Contextual retrieval enhances chunk relevance with metadata or generated context.
- Evaluate retrieval solutions based on scalability, latency, and supported mechanisms.