LLM recall refers to the ability of an LLM to find information from the text placed within its context window.
We can increase the number of documents returned by our vector DB to increase retrieval recall, but we cannot pass these to our LLM without damaging LLM recall.

The solution to this issue is to maximize retrieval recall by retrieving plenty of documents and then maximize LLM recall by minimizing the number of documents that make it to the LLM. To do that, we reorder retrieved documents and keep just the most relevant for our LLM — to do that, we use reranking.
After reranking, we have far more relevant information. Naturally, this can result in significantly better performance for RAG. It means we maximize relevant information while minimizing noise input into our LLM.

Reranking is one of the simplest methods for dramatically improving recall performance in Retrieval Augmented Generation (RAG) or any other retrieval-based pipeline.

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
os.environ["COHERE_API_KEY"] = "Up1yTRmr2bZ73o4fzSseBaonBJLaHBN9ZCeVh1xG"
os.environ["GOOGLE_API_KEY"] = "AIzaSyD7uibWj-CX1j7ljL_jTI1ZkpRniROzk1o"


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