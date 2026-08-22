# RAG Hybrid Search & Reranking

Hybrid search combines **dense (embedding-based)** retrieval and **sparse (keyword / BM25)** retrieval, then reranks the merged results before sending them to the LLM.

- **Dense retrieval (e.g. Cohere embeddings)** → semantic understanding
- **Sparse retrieval (BM25)** → exact keyword matches
- **Merge and rerank** both sets, then pass the top docs to the LLM (e.g. Gemini)

```text
        ┌─────────────────┐
Query → │ BM25 Retriever  │ ──┐
        └─────────────────┘   │
                              ├─> Merge → Rerank → Top docs → LLM (Gemini)
        ┌────────────────────┐│
Query → │ Cohere Embeddings  │┘
        │ Retriever (FAISS)  │
        └────────────────────┘
```

Hybrid retrieval = (dense + sparse) → rerank → generate.

---

## Why reranking?

**LLM recall** is the LLM's ability to find information in the text placed in its context window. You can increase the number of documents returned by the vector DB to raise *retrieval* recall, but you can't pass all of them to the LLM without hurting *LLM* recall.

The fix: maximize retrieval recall by retrieving plenty of documents, then maximize LLM recall by minimizing how many actually reach the LLM. You reorder the retrieved documents and keep only the most relevant ones — that reordering is **reranking**.

After reranking you keep more relevant information and less noise, which usually means significantly better RAG performance. Reranking is one of the simplest ways to dramatically improve recall in a RAG (or any retrieval-based) pipeline.

---

## Full hybrid pipeline (LangChain: Cohere + BM25 + Gemini)

```python
!pip install langchain langchain-google-genai langchain_cohere cohere faiss-cpu rank-bm25
```

```python
# ==============================================
# 🚀 Hybrid RAG Pipeline using Cohere + BM25 + Gemini
# ==============================================

from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever

from langchain_cohere import CohereEmbeddings
from langchain_cohere.rerank import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_google_genai import ChatGoogleGenerativeAI

import os

# ---- 1. API keys ----
os.environ["COHERE_API_KEY"] = "YOUR_COHERE_API_KEY"
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

# ---- 2. Load your documents ----
loader = PyPDFLoader("/content/os.pdf")
docs = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# ---- 3. Dense retriever (Cohere embeddings + FAISS) ----
embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

vector_store = FAISS.from_documents(chunks, embeddings)
dense_retriever = vector_store.as_retriever(search_kwargs={"k": 10})

# ---- 4. Sparse retriever (BM25 keyword-based) ----
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 10

# ---- 5. Combine both retrievers (hybrid) ----
hybrid_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, bm25_retriever],
    weights=[0.6, 0.4],  # tune weights as needed
)

# ---- 6. Optional: Rerank results using Cohere ----
reranker = CohereRerank(
    model="rerank-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

compressed_retriever = ContextualCompressionRetriever(
    base_retriever=hybrid_retriever,
    base_compressor=reranker,
)

# ---- 7. LLM: Google Gemini ----
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2,
)

# ---- 8. RetrievalQA chain ----
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=compressed_retriever,
    chain_type="stuff",
    return_source_documents=True,
)

# ---- 9. Ask your question ----
query = "Explain the concept of process scheduling in operating systems."
result = qa_chain({"query": query})

print("\n🧠 Question:")
print(query)
print("\n💬 Answer:")
print(result["result"])
print("\n📚 Sources:")
for i, doc in enumerate(result["source_documents"], 1):
    print(f"\nSource #{i}:\n{doc.page_content[:250]}...")
```

---

## Reranker-only pipeline (dense + Cohere rerank, no BM25)

Same idea without the sparse retriever: retrieve a wide set with the vector store (`k=20`), then let the Cohere reranker compress it down to the most relevant docs.

```python
# ==============================================
# 🚀 RAG Pipeline using Cohere Embeddings + Reranker + Google Gemini
# ==============================================

# ---- 1. Install dependencies (uncomment if needed) ----
# pip install langchain langchain-google-genai langchain_cohere cohere faiss-cpu

# ---- 2. Imports ----
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA

from langchain_cohere import CohereEmbeddings
from langchain_cohere.rerank import CohereRerank

from langchain.retrievers import ContextualCompressionRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# ---- 3. API Keys (Replace with your own) ----
os.environ["COHERE_API_KEY"] = "YOUR_COHERE_API_KEY"
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"


# ---- 4. Load and preprocess your documents ----
# Example: you can replace this with a folder of text, PDFs, etc.
loader = PyPDFLoader("/content/os.pdf")
docs = loader.load()

# Split into smaller chunks for embeddings
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)


# ---- 5. Create vector embeddings with Cohere ----
embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
)

# Build a FAISS vector store
vector_store = FAISS.from_documents(chunks, embeddings)

# Create the base retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 20})


# ---- 6. Add Cohere Reranker ----
reranker = CohereRerank(
    model="rerank-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
)

# Wrap retriever with reranker
compressed_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=reranker,
)

# ---- 7. Initialize Google Gemini LLM ----
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",          # or "gemini-1.5-flash", etc.
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2,
)


# ---- 8. Build RetrievalQA chain ----
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=compressed_retriever,
    chain_type="stuff",  # options: "stuff", "map_reduce", "refine"
    return_source_documents=True,
)

# ---- 9. Ask questions ----
query = "Explain OS."
result = qa_chain({"query": query})

print("\n🧠 Question:")
print(query)

print("\n💬 Answer:")
print(result["result"])

print("\n📚 Sources used:")
for i, doc in enumerate(result["source_documents"], 1):
    print(f"\nSource #{i}:\n{doc.page_content[:300]}...")
```

---

## From scratch (BM25 + sentence-transformers + Reciprocal Rank Fusion)

No framework — raw BM25 for sparse, `sentence-transformers` for dense, then fuse the two rankings with **Reciprocal Rank Fusion (RRF)**.

```python
!pip install rank_bm25

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
import torch

documents = [
    "The capital of France is Paris.",
    "The Great Wall of China is visible from space is a common myth.",
    "PyTorch is a machine learning framework based on the Torch library.",
    "A memory leak in Python can be debugged using the tracemalloc module."
]

tokenized_ds = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_ds)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(documents , convert_to_tensor = True)
```

```python
def get_hybrid_result(query, top_k = 3):
  #BM25
  tokenized_query = query.lower().split()
  bm25_scores = bm25.get_scores(tokenized_query)
  bm25_top_ids = np.argsort(bm25_scores)[::-1][:top_k]

  #semantic
  query_embedding = embed_model.encode(query,convert_to_tensor = True)
  cosine_scores = util.cos_sim(query_embedding,embeddings)[0]
  semantic_top_ids = torch.argsort(cosine_scores,descending = True)[:top_k].tolist()

  return bm25_top_ids.tolist() , semantic_top_ids
```

```python
def rrf(bm25_ranks,semantic_ranks,k = 60):
  scores = {}

  for rank,doc_id in enumerate(bm25_ranks):
    scores[doc_id] = scores.get(doc_id,0) + 1 / (k + rank)

  for rank,doc_id in enumerate(semantic_ranks):
    scores[doc_id] = scores.get(doc_id,0) + 1 / (k + rank)

  # sort
  fused_results = sorted(
      scores.items(),
      key = lambda x: x[1],
      reverse = True
  )
  return fused_results
```

```python
from transformers import pipeline

# Load a local generator (or use an API)
generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta", device_map="auto")

query = "How do I fix memory issues in Python?"
bm25_ids, semantic_ids = get_hybrid_results(query)
final_ranked = rrf(bm25_ids, semantic_ids)

# Get the top document text
best_doc_id = final_ranked[0][0]
context = documents[best_doc_id]

prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
response = generator(prompt, max_new_tokens=100)
print(response[0]['generated_text'])
```
