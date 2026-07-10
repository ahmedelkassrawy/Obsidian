### **What is a Self-Querying Retriever?**

- **Definition**: A retriever that uses a large language model (LLM) to convert a natural language query into a structured format, which is then used to query a vector store. It combines semantic search with metadata filtering.
- **Key Capability**: It extracts filters (e.g., "movies rated above 8.5" or "directed by Greta Gerwig") from the query and applies them to the metadata of stored documents, alongside performing a similarity search on document content.
- **Use Case**: Ideal for applications like recommendation systems, search engines, or Retrieval-Augmented Generation (RAG) where precise filtering and relevance are critical (e.g., finding movies by genre, year, or rating).

```python
docs = [
    Document(
        page_content="Complex, layered, rich red with dark fruit flavors",
        metadata={"name":"Opus One", "year": 2018, "rating": 96, "grape": "Cabernet Sauvignon", "color":"red", "country":"USA"},
    ),
    Document(
        page_content="Luxurious, sweet wine with flavors of honey, apricot, and peach",
        metadata={"name":"Château d'Yquem", "year": 2015, "rating": 98, "grape": "Sémillon", "color":"white", "country":"France"},
    ),
    Document(
        page_content="Full-bodied red with notes of black fruit and spice",
        metadata={"name":"Penfolds Grange", "year": 2017, "rating": 97, "grape": "Shiraz", "color":"red", "country":"Australia"},
    ),
    Document(
        page_content="Elegant, balanced red with herbal and berry nuances",
        metadata={"name":"Sassicaia", "year": 2016, "rating": 95, "grape": "Cabernet Franc", "color":"red", "country":"Italy"},
    ),
    Document(
        page_content="Highly sought-after Pinot Noir with red fruit and earthy notes",
        metadata={"name":"Domaine de la Romanée-Conti", "year": 2018, "rating": 100, "grape": "Pinot Noir", "color":"red", "country":"France"},
    ),
    Document(
        page_content="Crisp white with tropical fruit and citrus flavors",
        metadata={"name":"Cloudy Bay", "year": 2021, "rating": 92, "grape": "Sauvignon Blanc", "color":"white", "country":"New Zealand"},
    ),
    Document(
        page_content="Rich, complex Champagne with notes of brioche and citrus",
        metadata={"name":"Krug Grande Cuvée", "year": 2010, "rating": 93, "grape": "Chardonnay blend", "color":"sparkling", "country":"New Zealand"},
    ),
    Document(
        page_content="Intense, dark fruit flavors with hints of chocolate",
        metadata={"name":"Caymus Special Selection", "year": 2018, "rating": 96, "grape": "Cabernet Sauvignon", "color":"red", "country":"USA"},
    ),
    Document(
        page_content="Exotic, aromatic white with stone fruit and floral notes",
        metadata={"name":"Jermann Vintage Tunina", "year": 2020, "rating": 91, "grape": "Sauvignon Blanc blend", "color":"white", "country":"Italy"},
    ),
]

vectorstore = Chroma.from_documents(docs,embeddings)

from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(
        name="grape",
        description="The grape used to make the wine",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="name",
        description="The name of the wine",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="color",
        description="The color of the wine",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="year",
        description="The year the wine was released",
        type="integer",
    ),
    AttributeInfo(
        name="country",
        description="The name of the country the wine comes from",
        type="string",
    ),
    AttributeInfo(
        name="rating", description="The Robert Parker rating for the wine 0-100", type="integer" #float
    ),
]
document_content_description = "Brief description of the wine"


retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info,
    verbose=True
)

retriever.get_relevant_documents("What are some red wines")
```

```python
[Document(metadata={'year': 2017, 'color': 'red', 'grape': 'Shiraz', 'name': 'Penfolds Grange', 'rating': 97, 'country': 'Australia'}, page_content='Full-bodied red with notes of black fruit and spice'),
 Document(metadata={'year': 2016, 'grape': 'Cabernet Franc', 'rating': 95, 'color': 'red', 'name': 'Sassicaia', 'country': 'Italy'}, page_content='Elegant, balanced red with herbal and berry nuances'),
 Document(metadata={'country': 'USA', 'grape': 'Cabernet Sauvignon', 'name': 'Opus One', 'year': 2018, 'color': 'red', 'rating': 96}, page_content='Complex, layered, rich red with dark fruit flavors'),
 Document(metadata={'name': 'Domaine de la Romanée-Conti', 'rating': 100, 'grape': 'Pinot Noir', 'color': 'red', 'country': 'France', 'year': 2018}, page_content='Highly sought-after Pinot Noir with red fruit and earthy notes')]
```

### **What is the ParentDocumentRetriever?**

- **Definition**: A retriever that splits large documents into smaller child chunks for embedding and similarity search, but retrieves the full or larger parent document when a relevant child chunk is found.
- **Key Capability**: Combines the benefits of small-chunk embeddings (better for similarity search) with full-document context (better for understanding or generation).
- **Use Case**: Ideal for RAG applications involving long documents (e.g., PDFs, books, or articles) where small chunks improve retrieval accuracy, but the full document is needed for comprehensive answers.
```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Sample documents
docs = [
    Document(
        page_content="This is a long article about machine learning advancements in 2023...",
        metadata={"source": "ml_article.pdf", "title": "ML Advancements"}
    ),
    Document(
        page_content="A detailed guide to natural language processing techniques...",
        metadata={"source": "nlp_guide.pdf", "title": "NLP Guide"}
    ),
]

# Define splitters
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
# Optional: parent_splitter for larger chunks (if not using full documents)
# parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

# Initialize vector store, document store, and embeddings
vectorstore = Chroma(collection_name="split_docs", embedding_function=embeddings)
store = InMemoryStore()


# Instantiate the retriever
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    # parent_splitter=parent_splitter,  # Uncomment if using
    search_kwargs={"k": 2},  # Number of parent documents to return
)

# Add documents to the retriever
retriever.add_documents(docs)

# Query the retriever
query = "What are recent advancements in machine learning?"
results = retriever.invoke(query)

# Print results
for doc in results:
    print(f"Title: {doc.metadata['title']}")
    print(f"Content: {doc.page_content[:200]}...\n")
```