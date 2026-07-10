![[Pasted image 20251016163015.png]]

#### Staging within RAG
- **Loading**: this refers to getting your data from where it lives — whether it’s text files, PDFs, another website, a database, or an API — into your workflow. [LlamaHub](https://llamahub.ai/) provides hundreds of connectors to choose from.
- **Indexing**: this means creating a data structure that allows for querying the data. For LLMs this nearly always means creating `vector embeddings`, numerical representations of the meaning of your data, as well as numerous other metadata strategies to make it easy to accurately find contextually relevant data.
- **Storing**: once your data is indexed you will almost always want to store your index, as well as other metadata, to avoid having to re-index it
-  **Querying**: for any given indexing strategy there are many ways you can utilize LLMs and LlamaIndex data structures to query, including sub-queries, multi-step queries and hybrid strategies.
- **Evaluation**: a critical step in any flow is checking how effective it is relative to other strategies, or when you make changes. Evaluation provides objective measures of how accurate, faithful and fast your responses to queries are.
![[Pasted image 20251016163233.png]]
---
### Important Concepts
#### Loading Stage
[**Nodes and Documents**](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes): A `Document` is a container around any data source - for instance, a PDF, an API output, or retrieve data from a database. 
A `Node` is the atomic unit of data in LlamaIndex and represents a “chunk” of a source `Document`. 
Nodes have metadata that relate them to the document they are in and to other nodes.

[**Connectors**](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector): A data connector (often called a `Reader`) ingests data from different data sources and data formats into `Documents` and `Nodes`.

#### Indexing Stage
[**Indexes**](https://developers.llamaindex.ai/python/framework/module_guides/indexing): Once you’ve ingested your data, LlamaIndex will help you index the data into a structure that’s easy to retrieve. This usually involves generating `vector embeddings` which are stored in a specialized database called a `vector store`. Indexes can also store a variety of metadata about your data.

[**Embeddings**](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings): LLMs generate numerical representations of data called `embeddings`. When filtering your data for relevance, LlamaIndex will convert queries into embeddings, and your vector store will find data that is numerically similar to the embedding of your query.

#### Querying Stage
[**Retrievers**](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever): A retriever defines how to efficiently retrieve relevant context from an index when given a query. Your retrieval strategy is key to the relevancy of the data retrieved and the efficiency with which it’s done.

[**Routers**](https://developers.llamaindex.ai/python/framework/module_guides/querying/router): A router determines which retriever will be used to retrieve relevant context from the knowledge base. More specifically, the `RouterRetriever` class, is responsible for selecting one or multiple candidate retrievers to execute a query. They use a selector to choose the best option based on each candidate’s metadata and the query.

[**Node Postprocessors**](https://developers.llamaindex.ai/python/framework/module_guides/querying/node_postprocessors): A node postprocessor takes in a set of retrieved nodes and applies transformations, filtering, or re-ranking logic to them.

[**Response Synthesizers**](https://developers.llamaindex.ai/python/framework/module_guides/querying/response_synthesizers): A response synthesizer generates a response from an LLM, using a user query and a given set of retrieved text chunks.

---
## Loading Data
Before your chosen LLM can act on your data, you first need to process the data and load it. This has parallels to data cleaning/feature engineering pipelines in the ML world, or ETL pipelines in the traditional data setting.

This ingestion pipeline typically consists of three main stages:
1. Load the data
2. Transform the data
3. Index and store the data
## Loaders

Before your chosen LLM can act on your data you need to load it. The way LlamaIndex does this is via data connectors, also called `Reader`. Data connectors ingest data from different data sources and format the data into `Document` objects. A `Document` is a collection of data (currently text, and in future, images and audio) and metadata about that data.

### Loading using SimpleDirectoryReader
The easiest reader to use is our SimpleDirectoryReader, which creates documents out of every file in a given directory. It is built in to LlamaIndex and can read a variety of formats including Markdown, PDFs, Word documents, PowerPoint decks, images, audio and video.

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
```

### Using Readers from LlamaHub
Because there are so many possible places to get data, they are not all built-in. Instead, you download them from our registry of data connectors, [LlamaHub](https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub).
In this example LlamaIndex downloads and installs the connector called [DatabaseReader](https://llamahub.ai/l/readers/llama-index-readers-database), which runs a query against a SQL database and returns every row of the results as a `Document`:
```python
from llama_index.core import download_loader
from llama_index.readers.database import DatabaseReader

reader = DatabaseReader(
    scheme=os.getenv("DB_SCHEME"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dbname=os.getenv("DB_NAME"),
)

query = "SELECT * FROM users"
documents = reader.load_data(query=query)
```
### Creating Documents directly
Instead of using a loader, you can also use a Document directly.

```python
from llama_index.core import Document

doc = Document(text = "text")
```
## Transformations

After the data is loaded, you then need to process and transform your data before putting it into a storage system. These transformations include chunking, extracting metadata, and embedding each chunk. This is necessary to make sure that the data can be retrieved, and used optimally by the LLM.

Transformation input/outputs are `Node` objects (a `Document` is a subclass of a `Node`). Transformations can also be stacked and reordered.

We have both a high-level and lower-level API for transforming documents.
### High-Level Transformation API
Indexes have a `.from_documents()` method which accepts an array of Document objects and will correctly parse and chunk them up. However, sometimes you will want greater control over how your documents are split up.

```python
from llama_index.core import VectorStoreIndex

vector_index = VectorStoreIndex.from_documents(documents)
vector_index.as_query_engine()
```

Under the hood, this splits your Document into Node objects, which are similar to Documents (they contain text and metadata) but have a relationship to their parent Document.

If you want to customize core components, like the text splitter, through this abstraction you can pass in a custom `transformations` list or apply to the global `Settings`:

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

# global
Settings.text_splitter = text_splitter

#per-index
index = VectorStoreIndex.from_documents(
documents, transformations=[text_splitter]
)
```

### Lower-Level Transformation API
You can also define these steps explicitly.

You can do this by either using our transformation modules (text splitters, metadata extractors, etc.) as standalone components, or compose them in our declarative [Transformation Pipeline interface](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline).
Let’s walk through the steps below.
#### Splitting Your Documents into Nodes

A key step to process your documents is to split them into “chunks”/Node objects. The key idea is to process your data into bite-sized pieces that can be retrieved / fed to the LLM.

LlamaIndex has support for a wide range of [text splitters](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules), ranging from paragraph/sentence/token based splitters to file-based splitters like HTML, JSON.

These can be [used on their own or as part of an ingestion pipeline](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers).
```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

documents = SimpleDirectoryReader("./data").load_data()
pipeline = IngestionPipeline(transformations = [TokenTextSplitter(),..])

nodes = pipeline.run(documents = documents)
```
### Adding Metadata

You can also choose to add metadata to your documents and nodes. This can be done either manually or with [automatic metadata extractors](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor).
Here are guides on 1) [how to customize Documents](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents), and 2) [how to customize Nodes](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_nodes).

```python
document = Document(
	text = "text",
	metadata = {"filenmae": "<doc_file_name>",
				"category":"<category>"}
```
### Adding Embeddings
To insert a node into a vector index, it should have an embedding. See our [ingestion pipeline](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline) or our [embeddings guide](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings) for more details.
### Creating and passing Nodes directly
If you want to, you can create nodes directly and pass a list of Nodes directly to an indexer:

```python
from llama_index.core.schema import TextNode

node1 = TextNode(text="<text_chunk>", id_="<node_id>")
node2 = TextNode(text="<text_chunk>", id_="<node_id>")

index = VectorStoreIndex([node1, node2])
```

---
## Indexing
With your data loaded, you now have a list of Document objects (or a list of Nodes). It’s time to build an `Index` over these objects so you can start querying them.

#### What is an Index?
In LlamaIndex terms, an `Index` is a data structure composed of `Document` objects, designed to enable querying by an LLM. Your Index is designed to be complementary to your querying strategy.

LlamaIndex offers several different index types. We’ll cover the two most common here:
## Vector Store Index

A `VectorStoreIndex` is by far the most frequent type of Index you’ll encounter. The Vector Store Index takes your Documents and splits them up into Nodes. It then creates `vector embeddings` of the text of every node, ready to be queried by an LLM.

### What is an embedding?

`Vector embeddings` are central to how LLM applications function.

A `vector embedding`, often just called an embedding, is a **numerical representation of the semantics, or meaning of your text**. Two pieces of text with similar meanings will have mathematically similar embeddings, even if the actual text is quite different.

This mathematical relationship enables **semantic search**, where a user provides query terms and LlamaIndex can locate text that is related to the **meaning of the query terms** rather than simple keyword matching. This is a big part of how Retrieval-Augmented Generation works, and how LLMs function in general.

There are [many types of embeddings](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings), and they vary in efficiency, effectiveness and computational cost. By default LlamaIndex uses `text-embedding-ada-002`, which is the default embedding used by OpenAI. If you are using different LLMs you will often want to use different embeddings.

### Top K Retrieval

Once the ranking is complete, VectorStoreIndex returns the most-similar embeddings as their corresponding chunks of text. The number of embeddings it returns is known as `k`, so the parameter controlling how many embeddings to return is known as `top_k`. This whole type of search is often referred to as “top-k semantic retrieval” for this reason.

Top-k retrieval is the simplest form of querying a vector index; you will learn about more complex and subtler strategies when you read the [querying](https://developers.llamaindex.ai/python/framework/understanding/rag/querying) section.

### Using Vector Store Index

To use the Vector Store Index, pass it the list of Documents you created during the loading stage:

```python
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)
```

You can also choose to build an index over a list of Node objects directly:

```python
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex(nodes)
```

With your text indexed, it is now technically ready for [querying](https://developers.llamaindex.ai/python/framework/understanding/rag/querying)! However, embedding all your text can be time-consuming and, if you are using a hosted LLM, it can also be expensive. To save time and money you will want to [store your embeddings](https://developers.llamaindex.ai/python/framework/understanding/rag/storing) first.

---
## Querying
Now you’ve loaded your data, built an index, and stored that index for later, you’re ready to get to the most significant part of an LLM application: querying.

At its simplest, querying is just a prompt call to an LLM: it can be a question and get an answer, or a request for summarization, or a much more complex instruction.

More complex querying could involve repeated/chained prompt + LLM calls, or even a reasoning loop across multiple components.
#### Getting Started
The basis of all querying is the `QueryEngine`. The simplest way to get a QueryEngine is to get your index to create one for you, like this:
```python
query_engine = index.as_query_engine()
response = query_engine.query(
    "Write an email to the user given their background information."
)
print(response)
```
#### Stages of querying
- **Retrieval** is when you find and return the most relevant documents for your query from your `Index`. As previously discussed in [indexing](https://developers.llamaindex.ai/python/framework/module_guides/indexing), the most common type of retrieval is “top-k” semantic retrieval, but there are many other retrieval strategies.
- **Postprocessing** is when the `Node`s retrieved are optionally reranked, transformed, or filtered, for instance by requiring that they have specific metadata such as keywords attached.
- **Response synthesis** is when your query, your most-relevant data and your prompt are combined and sent to your LLM to return a response.
#### Customizing the stages of querying
LlamaIndex features a low-level composition API that gives you granular control over your querying.

In this example, we customize our retriever to use a different number for `top_k` and add a post-processing step that requires that the retrieved nodes reach a minimum similarity score to be included. This would give you a lot of data when you have relevant results but potentially no data if you have nothing relevant.

```python
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

#build index
index = VectorStoreIndex.from_documents(documents)

#configure retriever
retriever = VectorIndexRetreiver(index = index, similarity_top_k = 10)

#configure response synthesizer
response_synthesizer = get_response_synthesizer()

#query_engine
query_engine = RetrieverQueryEngine(
				retriever = retriever,
				response_synthesizer = response_synthesizer,
				node_postprocessors =[SimilarityPostprocessor(similarity_cutoff=0.7)])
				
#query
response = query_engine.query("What did the author do grwoing up?")
print(response)
```

You can also add your own retrieval, response synthesis, and overall query logic, by implementing the corresponding interfaces.
For a full list of implemented components and the supported configurations, check out our [reference docs](https://developers.llamaindex.ai/python/framework/api_reference).
Let’s go into more detail about customizing each step:
### Configuring retriever

```python
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)
```

There are a huge variety of retrievers that you can learn about in our [module guide on retrievers](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever).

### Configuring node postprocessors
We support advanced `Node` filtering and augmentation that can further improve the relevancy of the retrieved `Node` objects. This can help reduce the time/number of LLM calls/cost or improve response quality.

For example:
- `KeywordNodePostprocessor`: filters nodes by `required_keywords` and `exclude_keywords`.
- `SimilarityPostprocessor`: filters nodes by setting a threshold on the similarity score (thus only supported by embedding-based retrievers)
- `PrevNextNodePostprocessor`: augments retrieved `Node` objects with additional relevant context based on `Node` relationships.
The full list of node postprocessors is documented in the [Node Postprocessor Reference](https://developers.llamaindex.ai/python/framework/api_reference/postprocessor).
To configure the desired node postprocessors:

```python
node_postprocessors = [
    KeywordNodePostprocessor(
        required_keywords=["Combinator"], exclude_keywords=["Italy"]
    )
]

query_engine = RetrieverQueryEngine.from_args(
    retriever, 
    node_postprocessors = node_postprocessors
)
response = query_engine.query("What did the author do growing up?")
```
### Configuring response synthesis
After a retriever fetches relevant nodes, a `BaseSynthesizer` synthesizes the final response by combining the information.
You can configure it via:
```python
query_engine = RetrieverQueryEngine.from_args(
    retriever, response_mode=response_mode
)
```

Right now, we support the following options:

- `default`: “create and refine” an answer by sequentially going through each retrieved `Node`; This makes a separate LLM call per Node. Good for more detailed answers.
- `compact`: “compact” the prompt during each LLM call by stuffing as many `Node` text chunks that can fit within the maximum prompt size. If there are too many chunks to stuff in one prompt, “create and refine” an answer by going through multiple prompts.
- `tree_summarize`: Given a set of `Node` objects and the query, recursively construct a tree and return the root node as the response. Good for summarization purposes.
- `no_text`: Only runs the retriever to fetch the nodes that would have been sent to the LLM, without actually sending them. Then can be inspected by checking `response.source_nodes`. The response object is covered in more detail in Section 5.
- `accumulate`: Given a set of `Node` objects and the query, apply the query to each `Node` text chunk while accumulating the responses into an array. Returns a concatenated string of all responses. Good for when you need to run the same query separately against each text chunk.
---
# Storing

Once you have data [loaded](https://developers.llamaindex.ai/python/framework/module_guides/loading) and [indexed](https://developers.llamaindex.ai/python/framework/module_guides/indexing), you will probably want to store it to avoid the time and cost of re-indexing it. By default, your indexed data is stored only in memory.# Storing
## Persisting to disk
The simplest way to store your indexed data is to use the built-in `.persist()` method of every Index, which writes all the data to disk at the location specified. This works for any type of index.

```python
index.storage_context.persist(persist_dir="<persist_dir>")
```

Here is an example of a Composable Graph:

```python
graph.root_index.storage_context.persist(persist_dir="<persist_dir>")
```

You can then avoid re-loading and re-indexing your data by loading the persisted index like this:
```python
from llama_index.core import StorageContext, load_index_from_storage

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")

# load index
index = load_index_from_storage(storage_context)
```

## Using Vector Stores

As discussed in [indexing](https://developers.llamaindex.ai/python/framework/module_guides/indexing), one of the most common types of Index is the VectorStoreIndex. The API calls to create the [embeddings](https://developers.llamaindex.ai/python/framework/module_guides/indexing#what-is-an-embedding) in a VectorStoreIndex can be expensive in terms of time and money, so you will want to store them to avoid having to constantly re-index things.

LlamaIndex supports a [huge number of vector stores](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores) which vary in architecture, complexity and cost. In this example we’ll be using Chroma, an open-source vector store.

To use Chroma to store the embeddings from a VectorStoreIndex, you need to:
- initialize the Chroma client
- create a Collection to store your data in Chroma
- assign Chroma as the `vector_store` in a `StorageContext`
- initialize your VectorStoreIndex using that StorageContext

Here’s what that looks like, with a sneak peek at actually querying the data:
```python
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# load some documents
documents = SimpleDirectoryReader("./data").load_data()

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create your index
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# create a query engine and query
query_engine = index.as_query_engine()
response = query_engine.query("What is the meaning of life?")
print(response)
```

If you’ve already created and stored your embeddings, you’ll want to load them directly without loading your documents or creating a new VectorStoreIndex:
```python
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# initialize client
db = chromadb.PersistentClient(path="./chroma_db")

# get collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# load your index from stored vectors
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)

# create a query engine
query_engine = index.as_query_engine()
response = query_engine.query("What is llama2?")
print(response)
```
## Inserting Documents or Nodes

If you’ve already created an index, you can add new documents to your index using the `insert` method.
```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex([])
for doc in documents:
    index.insert(doc)
```

----
#### Simple RAG
```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex, get_response_synthesizer, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
import os
from llama_index.core.node_parser import SentenceSplitter

os.environ["GOOGLE_API_KEY"] = "AIzaSyD7uibWj-CX1j7ljL_jTI1ZkpRniROzk1o"

llm = GoogleGenAI( # Use the new class name
    model="models/gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# Set embedding model and LLM in Settings
Settings.embed_model = embed_model
Settings.llm = llm

doc_path = "D://me//PS//docs"
documents = SimpleDirectoryReader(doc_path).load_data()

# Improved text splitter settings for better PDF handling
text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
Settings.text_splitter = text_splitter

# Check if documents were loaded correctly
if not documents:
    print("No documents were loaded from the directory.")
    exit(1)

# Index the documents
vector_index = VectorStoreIndex.from_documents(documents, transformations=[text_splitter])

retriever = VectorIndexRetriever(index=vector_index,
                                 similarity_top_k=10)

response_synthesizer = get_response_synthesizer()

# Configure query engine with optimal settings
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
)

# Execute query
query = "What is a Manager Pattern ?"
response = query_engine.query(query)

# Print the response
print(response)
```

```python
metadata_filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="organization",
            value=CURRENT_ORGANIZATION,
            operator=FilterOperator.EQ
        ),
        # Optionally, also filter by user_id for user-specific documents
        # MetadataFilter(
        #     key="user_id",
        #     value=CURRENT_USER_ID,
        #     operator=FilterOperator.EQ
        # ),
    ]
)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,
    hybrid_top_k=3,
    filters=metadata_filters  # Apply organization filtering
)
```