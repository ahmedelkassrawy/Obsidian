# Retrieval-Augmented Generation (RAG) Guide

1. Chunking
2. Embedding
3. Vector DB
4. Retrieval Process
5. Generation

## Setup: Installs and Imports

Start by installing required packages and importing modules. These are essential for document loading, splitting, embeddings, vector stores, LLMs, and chains.

### Installs
```python
!pip install chromadb
!pip install -U langchain-community
!pip install langchain_google_genai
!pip install langchain_core
!pip install pypdf
!pip install langchain_community tiktoken langchain-openai langchainhub chromadb langchain
```

### Imports
Combine imports from both sources for completeness.

```python
from typing_extensions import TypedDict
from langchain.schema.runnable import RunnableMap
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import chromadb
import os

from langchain.load import dumps, loads
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader

from langchain import hub
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph, END
from typing_extensions import List, TypedDict
```

## Step 1: Document Loading and Indexing

Load documents (PDF or text), split them into chunks, embed them, and store in a vector database like Chroma.

### Loading and Splitting Documents
Use `PyPDFLoader` for PDFs or `TextLoader` for text files. Split into chunks to handle large docs.

```python
# Example with PDF
pdf_path = "/content/os.pdf"  # Replace with your path
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Splitting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(docs)
```

Alternative splitting (smaller chunks for finer retrieval):
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(docs)
```

For text files or conditional loading:
```python
doc_path = ""  # Your document path
if doc_path.endswith(".pdf"):
    loader = PyPDFLoader(doc_path)
else:
    loader = TextLoader(doc_path)
docs = loader.load()
```

### Embeddings and Vector Store
Embed chunks and store in Chroma. Options include HuggingFace, Google, or Cohere embeddings.

Using HuggingFace Embeddings:
```python
# Embeddings (HuggingFace)
embeddings = HuggingFaceEmbeddings()  # Default model

# Vector store
vector_store = Chroma.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
```

Using Google Embeddings:
```python
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma.from_documents(chunks, embedding)
```

Using Cohere Embeddings (with persistence):
```python
embeddings = CohereEmbeddings(model="embed-english-v3.0")
vector_store = Chroma.from_documents(
    documents=chunks,
    persist_directory="persist_dir",  # Optional: For persistence
    collection_name="example_collection",
    embedding=embeddings,
)
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5},
    search_type="similarity"
)
```

## Step 2: Basic Retrieval and Generation

Set up an LLM, prompt, and chain for querying the retriever.

### LLM Setup
Use Google Generative AI.
```python
api_key = "AIzaSyB38nvrIt6MFrEchALd6Eouz9UHVrt9Tso"  # Replace with your key
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
```

### Basic RAG Chain
Format docs, pull a prompt from LangChain Hub, and create a chain.

```python
# Prompt from Hub (expects 'question' and 'context')
prompt = hub.pull("rlm/rag-prompt")

# Post-process docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Invoke with question
response = rag_chain.invoke("What is Task Decomposition?")
print(response)
```

Alternative chain using `create_retrieval_chain`:
```python
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# Interactive
msg = input("write what you want to ask: ")
res = rag_chain.invoke({"input": msg})
print(res["answer"])
```

Simple prompt-based invocation (no chain):
```python
query = "Your question here"  # Replace
relevant_docs = retriever.invoke(query)
context = format_docs(relevant_docs)

prompt_template = """
You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question: {question}

Answer:"""

prompt = prompt_template.format(context=context, question=query)
response = llm.invoke(prompt)
result = response.content.strip()
print(result)
```

## Step 3: Advanced Techniques

Enhance retrieval with query expansion, fusion, or graph-based workflows.

### MultiQueryRetriever
Generates multiple queries from one to improve recall. Useful for complex or ambiguous queries.

```python
# Prompt for generating queries
query_template = """You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents from a vector
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search.
Provide these alternative questions separated by newlines. Original question: {question}"""

generate_queries = (
    ChatPromptTemplate.from_template(query_template)
    | llm
    | StrOutputParser()
    | (lambda x: x.split("\n"))  # Split into list
)

# Unique union of docs
def get_unique_union(documents):
    return [loads(doc) for doc in set(dumps(doc) for sublist in documents for doc in sublist)]

# Retrieval chain
retrieval_chain = generate_queries | retriever.map() | get_unique_union

# RAG template
rag_template = """Answer the following question based on this context:

{context}

Question: {question}
"""

rag_chain = (
    {"context": retrieval_chain, "question": itemgetter("question")}
    | ChatPromptTemplate.from_template(rag_template)
    | llm
    | StrOutputParser()
)

# Example
question = "What is task decomposition for LLM agents?"
response = rag_chain.invoke({"question": question})
print(response)
```

Use Cases: Improve recall, reduce bias, handle complex info.

### RAG Fusion
Generates multiple queries and uses Reciprocal Rank Fusion (RRF) to rerank results.

```python
# Prompt for queries
prompt = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
Generate multiple search queries related to: {question} \n
Output (4 queries):"""
prompt_rag_fusion = ChatPromptTemplate.from_template(prompt)

generate_queries = (
    prompt_rag_fusion
    | llm
    | StrOutputParser()
    | (lambda x: x.split("\n"))
)

# RRF function
def reciprocal_rank_fusion(results: list[list], k=60):
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)
    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked_results

# Retrieval chain
retrieval_chain = generate_queries | retriever.map() | reciprocal_rank_fusion

# RAG chain
template = """Answer the following question based on this context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

final_rag = (
    {"context": retrieval_chain, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Invoke
question = "What is task decomposition for LLM agents?"  # Example
response = final_rag.invoke({"question": question})
print(response)
```

### LangGraph Workflow
Use a state graph for modular retrieval and generation.

```python
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

# Build graph
workflow = StateGraph(State)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
graph = workflow.compile()

# Invoke
response = graph.invoke({"question": "What is Process States"})
print(response["answer"])
```

## Step 4: Search Methods Explained

Understand different retrieval strategies for RAG.

### 1. BM25 (Classical Keyword Search)
BM25 scores documents based on term frequency (TF), inverse document frequency (IDF), and document length normalization.

- **Intuition**: Prefers exact matches for keywords like "renewable energy policy".
- **Strength**: Precise for keywords, names, numbers.
- **Weakness**: Misses semantic synonyms (e.g., "car" vs. "automobile").

### 2. Semantic Search
Uses vector embeddings for similarity (e.g., cosine distance).

- Captures meaning: "car insurance" ≈ "automobile coverage".
- **Weakness**: May miss exact terms like dates or rare names.

### 3. Hybrid Search
Combines BM25 (lexical precision) + embeddings (semantic recall).

- **Methods**:
  - Score fusion: Weighted sum of scores.
  - Result fusion: Merge top results and rerank.
- **Use in RAG**: Ensures reliable docs for LLM (facts from BM25 + context from semantics).
- **Example Query**: "When was Tesla founded?" – BM25 finds exact phrases; semantics finds paraphrases.

This structure provides a complete, study-friendly guide. Experiment with code by replacing paths, keys, and questions!