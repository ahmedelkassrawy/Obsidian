### Sentence Window RAG Solution
Instead of fixed-size chunks, it retrieves **individual sentences** and then **expands around them** by adding a small _window_ of neighboring sentences — giving the retriever **semantic continuity**.

**Mechanism:**
1. Split the document into **sentences**.
2. Embed each sentence separately.
3. When retrieving, select top-N most relevant sentences.
4. For each retrieved sentence, **add neighboring sentences** (e.g., ±2 sentences).  
    → creates a local, coherent context window.

`[Sentence 1] [Sentence 2] [Sentence 3*] [Sentence 4] [Sentence 5]                        ↑ retrieved match                + window [-2, +2] = context`

---
## ⚙️ Pros and Cons

|✅ Pros|❌ Cons|
|---|---|
|Preserves semantic flow around retrieved info|Slightly slower retrieval (more embeddings)|
|Reduces chance of splitting key concepts|Higher storage/memory (more vectors)|
|Great for factual or structured documents|Harder to tune ideal window size|
|Can outperform standard chunking on QA & summarization tasks|Overlapping contexts may cause redundancy|

---
## 🧰 Best Use Cases

- **Scientific papers / textbooks** — where details are sentence-bound.
- **Legal or policy documents** — each clause is meaningful individually.
- **Educational content / PDFs** — answers often span a few sentences.
- **Technical manuals** — where each concept lives in a local neighborhood.
---
## 🧩 Implementation: Sentence Window RAG (Cohere + Gemini)

We’ll use your same setup:
- **Cohere embeddings**
- **Cohere reranker**
- **Google Gemini LLM**

and add:
- Sentence-level chunking
- A small context window
---
### Full Implementation

```python
# ==============================================
# 🚀 Sentence-Window RAG using Cohere + Reranker + Gemini
# ==============================================

# pip install langchain langchain-google-genai langchain_cohere cohere faiss-cpu nltk

from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_cohere import CohereEmbeddings
from langchain_cohere.rerank import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.docstore.document import Document

import nltk
from nltk.tokenize import sent_tokenize
import os

nltk.download("punkt")

# ---- 1. API Keys ----
os.environ["COHERE_API_KEY"] = "YOUR_COHERE_API_KEY"
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"


# ---- 2. Load your text ----
pdf_path = "/content/os.pdf"

# You can use PyPDFLoader, but for simplicity here:
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# Merge all page texts
text = " ".join([p.page_content for p in pages])

# ---- 3. Split into SENTENCES ----
sentences = sent_tokenize(text)

# ---- 4. Build sentence-window documents ----
def build_sentence_windows(sentences, window_size=2):
    docs = []
    
    for i, sent in enumerate(sentences):
        # Take ±window sentences around the target
        start = max(0, i - window_size)
        end = min(len(sentences), i + window_size + 1)
        window_text = " ".join(sentences[start:end])
        docs.append(Document(page_content=window_text))
    return docs

docs = build_sentence_windows(sentences, window_size=2)


# ---- 5. Cohere embeddings ----
embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
)

vector_store = FAISS.from_documents(docs, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 10})


# ---- 6. Cohere Reranker ----
reranker = CohereRerank(
    model="rerank-english-v2.0",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
)

compressed_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=reranker,
)


# ---- 7. LLM: Google Gemini ----
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2,
)


# ---- 8. Build QA chain ----
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=compressed_retriever,
    chain_type="stuff",
    return_source_documents=True,
)


# ---- 9. Ask question ----
query = "Explain what process synchronization means in operating systems."
result = qa_chain({"query": query})

print("\n🧠 Question:")
print(query)
print("\n💬 Answer:")
print(result["result"])
print("\n📚 Sources:")
for i, doc in enumerate(result["source_documents"], 1):
    print(f"\nSource #{i}:\n{doc.page_content[:300]}...")

```