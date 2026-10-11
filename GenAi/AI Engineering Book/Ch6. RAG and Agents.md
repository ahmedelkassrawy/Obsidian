Two dominating patterns for context construction:
- RAG
- Agent

The rag pattern allows the model to retirieve relevent info from external data sources

The agentic pattern allows the model to use tools such as web search news to gather info

RAG acts as a technique for constrtucting context specific to each query , insted of using the same context for all queries
this gives the model neccessay information to process an input

The success of RAG system depends on the quality of the retriever

A retriever has 2 main functions 
- Indexing
- Querying

Indexing involves processing data so that it can be quickly retirieved later
How to index data depends on how you want to retrieve it later

Retrieval works by ranking chunks or documents based on their relevance to a given query

Retrieval algo differ based on how relevance scores and computed

2 common retrieval mechanims:
- Term based retrieval 
- Embedding based retrieval

First Sparse VS Dense Retrieval
Sparse Retrieval 
- represent data using sparse vectors
- sparse vector is a vector where the majority of the values are 0
- Term based retrieval is considered sparse, each term can be represented using sparse one-hot vector, a vector that is 0 everywhere except one value of 1
- The vector size is the lenght of the vocab
- value of 1 is in the index corrseponding to the index of the term in the vocab

```text
{"food":0,"banana":1,"slug":2}
one hot vectors -> [1,0,0] , [0,1,0] , [0,0,1]
```

Dense Retriever 
- represent data using dense vectors
- dense vector is a vector where majority is not 0
- MEbedding based retrieval is considered dense
- Embedding are generally dense vectors

The sparisty makes embedding operations more effiecient

Term Based Retrieval
- Given query -> starightforward method is find relevant documents with keywords.
- "Lexical Retrival"
- Problems of this approach:
	- many docs might contain the same given term
	- the assumption is that more a term appears in a docuemnt , the more relevant this document is to this term (Term Frequency - TF)
	- The more the term appears in documents its importance dissappers (Inverse Document Frequency - IDF)
	- The higher IDF , the more importance it is 

TF-IDF -> combines TF and IDF
Two common term based retrieval -> ElasticSearch and BM25

ElasticSearch is built on top of Lucene 
- it uses a data strcuutre called inverted index
- Its a dict that maps from terms to documents that contain them 
- This dict allows for fast retrieval of documents given a term
- The index may also store additional info such as TF and docuemnt count

Embedding Based Retrieval 
Indexing has an extra function which is converting the original data chunks into embeddings
The database where the embeddings are stored are called Vector DB

Querying then needs 2 steps:
1. Embedding model -> convert query into an embedding using the same embedding model used during indexing
2. Retriever -> fetch k data chunks whose embeddings are closet to the query embedding

An embedding is a vector that aims to preservce the important properties of the original data

Vector db is responsible for the finding vectors in the db close to the query and returning them 
Vectors have to be indexed and stored in a way that makes the vector search fast and efficient

Vector Search is typically framed as nearest neighbour search problem
for example , given a query find the k nearst vectors -> the native solution is KNN (but its good for small datasets)

for large datasets , its done by Approximate nearest neighbour (ANN) .

Vectors can be quantized (reduced precision) or made 

2 metrics often used by RAG in evaulation:
- Context Precision -> out of all docs retrieved what % is relevant to the query
- Context Recall -> Out of all docs relevant tot he query what % is retrived
Usually in prod the context precision is the one used as its simpler to compute

If we care about ranking the retrieved doc (where more relevant docs should be ranked first)
Mean Avg Precision , Mean Reciprocal Rank . NDCG

Quality of a retriever should be evalueated in the context of the whole rag sys
a retriever is good if it helps the sys genrate high quality answers

The added latency by query embedding and vector search is minimal compared tot the answer generation 

Common traed offs between indexing and querying
- The more detailed the index is -> the more accurate the retriaval process is , but indexing process will be slower and more memory consuming.

In general, a detailed index like HNSW provides high accuracy and fast query times but requires significant time and memory to build. In contrast, a simpler index like LSH is quicker and less memory-intensive to create, but it results in slower and less accurate queries

To summarize the qualtiy of RAG system should be evaulatod by:
1. Evaluate the retrieval quality. 
2. Evaluate the final RAG outputs. 
3. Evaluate the embeddings (for embedding-based retrieval

Combining Retreival algo 
first a retriever that fecthes candidates -> then a reranking technqiue

You can use multiple retrievers to fecth candidates at the same time,then combinig these diff rankings together to generate a final ranking

One of the algo used for combinig the different rankings is RRF (Reciprocal Rank Fusion) -> it assigns each doc a score based in its ranking by a retriever 
The higher it ranks the higher is scores 
A document final score is the sum of its scores with respect to all retrievers

Retrieval Optimization 
1. Chunking Strategy 
How your data should be indexed depends on how you intend to retrieve it later

the chunking strategy can impact the perf of the retreieval system very much

The simplest strategy is to chunk documents into chunks of equal length based on a certain unit

You can also split documents recursively using increasingly smaller units until each chunk fits within your maximum chunk size.

you can start by splitting a document into sections. If a section is too long, split it into paragraphs. 
If a paragraph is still too long, split it into sentences. 

Chunking without overlap may cut off in the middle of an important context and leading to loss of critical info

- The chunk size shouldn’t exceed the maximum context length of the generative model
- the chunk size also shouldn’t exceed the embedding model’s context limit

There is no universal best chunk size or overlap size. You have to experiment to find what works best for you

2. Reranking
The initial document rankings generated by the retriever can be further reranked to be more accurate.

Reranking is especially useful when you need to reduce the number of retrieved documents, either to fit them into your model’s context or to reduce the number of input tokens.

3. Query Rewrtiign
4. COntextual Retreival
retireving each chunk with a relevant context like the metdata make it easier to retrieve the relevant chunks

The metadata may also include entities automatically extracted from the chunk.

If a document is split into multiple chunks, some chunks might lack the necessary context to help the retriever understand what the chunk is about.. To avoid this, you can augment each chunk with the context from the original document, such as the original document’s title and summary. Anthropic used AI models to generate a short context, usually 50-100 tokens,


Multimodal RAG 
If your generator is multimodal, its contexts might be augmented not only with text documents but also with images, videos, audio, etc., from external sources. 

![[Pasted image 20261012003139.png]]