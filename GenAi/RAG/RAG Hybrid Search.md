You’re talking about a **hybrid search RAG pipeline** — which means combining **dense (embedding-based)** retrieval _and_ **sparse (keyword or BM25)** retrieval.

This approach gives you **the best of both worlds**:
- **Dense retrieval (Cohere embeddings)** → semantic understanding
- **Sparse retrieval (BM25)** → exact keyword matches  
    Then you **merge and rerank** both sets before sending them to Gemini.
    
Let’s go step-by-step, and then I’ll show you the **full code** using:
- LangChain
- Cohere embeddings
- BM25 retriever
- Optional Cohere reranker
- Google Gemini as the LLM

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