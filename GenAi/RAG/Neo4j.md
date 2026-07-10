---
name: Neo4j for AI Engineers
description: A comprehensive guide to leveraging Neo4j for AI/ML tasks, focusing on vector indexing, embeddings, and GraphRAG pipelines.
type: project
---

# Neo4j for AI Engineers: A Study Guide

This document is designed for AI engineers looking to integrate Neo4j into their machine learning and artificial intelligence workflows, particularly for tasks involving graph-enhanced data retrieval and generation. It covers core Cypher queries, vector indexing, embeddings, and advanced GraphRAG (Retrieval Augmented Generation) pipelines using Neo4j.

## 1. Core Cypher Queries for Data Exploration

Basic Cypher queries to interact with movie data in Neo4j.

### Fetching Movie Details
```python
MATCH (m:Movie {title: "Toy Story"})
RETURN m.title AS title, m.plot AS plot
```
*   **Purpose:** Retrieve the title and plot of a specific movie.

### Fetching Plot Embeddings
```python
MATCH (m:Movie {title: "Toy Story"})
RETURN m.title AS title, m.plot AS plot, m.plotEmbedding
```
*   **Purpose:** Retrieve the title, plot, and the pre-computed embedding vector for a movie. These embeddings are crucial for similarity searches.

### Filtering Movies with Embeddings
```python
MATCH (m:Movie)
WHERE m.plotEmbedding IS NOT NULL
RETURN m.title, m.plot
```
*   **Purpose:** Identify and retrieve movies that have associated plot embeddings, ensuring data quality for vector search operations.

## 2. Vector Indexing and Embeddings in Neo4j

Leveraging Neo4j's vector index for efficient similarity search.

### Creating a Vector Index
This creates a vector index named `moviePlots` on the `plotEmbedding` property of `Movie` nodes.

```python
CREATE VECTOR INDEX moviePlots IF NOT EXISTS
FOR (m:Movie)
ON m.plotEmbedding
OPTIONS {indexConfig: {
  "vector.dimensions": 1536,
  "vector.similarity_function": "cosine"
}};
```
*   **`vector.dimensions`**: Specifies the dimensionality of the embedding vectors (e.g., 1536 for OpenAI's `text-embedding-ada-002`).
*   **`vector.similarity_function`**: Defines the metric for calculating similarity (e.g., `cosine` for direction-based similarity).

### Querying the Vector Index
The `db.index.vector.queryNodes` procedure returns the approximate nearest neighbor nodes and their similarity scores.

```python
CALL db.index.vector.queryNodes(
  indexName :: STRING,
  numberOfNearestNeighbours :: INTEGER,
  query :: LIST<FLOAT>
) YIELD node, score
```
*   **`node`**: The matching node from the graph.
*   **`score`**: A similarity score ranging from `0.0` to `1.0`, where `1.0` indicates perfect similarity.

### Querying Similar Movie Plots
This example demonstrates how to find movies similar to "Toy Story" based on their plot embeddings.

```python
MATCH (m:Movie {title: "Toy Story"})

CALL db.index.vector.queryNodes("moviePlots", 6, m.plotEmbedding)
YIELD node,score

RETURN node.title AS title, node.plot AS plot,score
```
*   **Purpose:** Find the top `k` (here, 6) most similar movies to a given movie by querying the vector index with its plot embedding.

### Generating Embeddings with `genai.vector.encode`
Neo4j's `genai` procedures allow for on-the-fly embedding generation.

```python
WITH genai.vector.encode(
    "Text to create embeddings for",
    "OpenAI",
    { token: "sk-..." }) AS embedding
RETURN embedding
```
*   **Purpose:** Generate an embedding vector for a given text using a specified model (e.g., OpenAI). The token should be securely managed.

### Generating and Querying with a Custom Plot Embedding
This combines embedding generation with vector index querying to find movies similar to a user-provided plot description.

```python
WITH genai.vector.encode(
    "A mysterious spaceship lands Earth",
    "OpenAI",
    { token: "sk-..." }) AS myMoviePlot
CALL db.index.vector.queryNodes('moviePlots', 6, myMoviePlot)
YIELD node, score
RETURN node.title, node.plot, score
```
*   **Purpose:** Demonstrate how a user's textual query can be converted into an embedding and then used to find relevant movies.

## 3. Python Integration for GraphRAG

Using `neo4j-graphrag` for building sophisticated RAG pipelines.

### Vector Retriever
This section outlines setting up a `VectorRetriever` to fetch documents based on vector similarity.

```python
import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create embedder
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# Create retriever
retriever = VectorRetriever(
    driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)

# Search for similar items
result = retriever.search(query_text="Toys coming alive", top_k=5)

# Parse results
for item in result.items:
    print(item.content, item.metadata["score"])

# Close the database connection
driver.close()
```
*   **`OpenAIEmbeddings`**: Configures the embedding model (e.g., `text-embedding-ada-002`).
*   **`VectorRetriever`**: Initializes the retriever with the Neo4j driver, database, index name, embedder, and properties to return.
*   **`retriever.search`**: Performs a similarity search based on the `query_text` and retrieves the top `k` results.

### Basic GraphRAG Pipeline
This demonstrates a complete RAG pipeline that combines retrieval with an LLM for answering questions.

```python
import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create embedder
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# Create retriever
retriever = VectorRetriever(
    driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)

# Create the LLM
llm = OpenAILLM(model_name="gpt-4o")


# Create GraphRAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)

# Search
query_text = "Find me movies about toys coming alive"

response = rag.search(
    query_text=query_text,
    retriever_config={"top_k": 5}
)

print(response.answer)


# Close the database connection
driver.close()
```
*   **`OpenAILLM`**: Integrates an LLM (e.g., `gpt-4o`) for generating answers.
*   **`GraphRAG`**: Orchestrates the retrieval and generation steps, passing retrieved context to the LLM.

### Graph-Enhanced Vector Retriever (`VectorCypherRetriever`)
This retriever combines vector search with custom Cypher queries to leverage graph relationships, enriching the retrieved context.

```python
import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create embedder
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# Define retrieval query
retrieval_query = """
MATCH (node)<-[r:RATED]-()
RETURN
  node.title AS title, node.plot AS plot, score AS similarityScore,
  collect { MATCH (node)-[:IN_GENRE]->(g) RETURN g.name } as genres,
  collect { MATCH (node)<-[:ACTED_IN]->(a) RETURN a.name } as actors,
  avg(r.rating) as userRating
ORDER BY userRating DESC
"""

# Create retriever
retriever = VectorCypherRetriever(
    driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    index_name="moviePlots",
    embedder=embedder,
    retrieval_query=retrieval_query,
)

#  Create the LLM
llm = OpenAILLM(model_name="gpt-4o")

# Create GraphRAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)

# Search
query_text = "Find the highest rated action movie about travelling to other planets"

response = rag.search(
    query_text=query_text,
    retriever_config={"top_k": 5},
    return_context=True
)

print(response.answer)
print("CONTEXT:", response.retriever_result.items)

# Close the database connection
driver.close()
```
*   **`retrieval_query`**: A Cypher query that specifies how to retrieve additional context (genres, actors, user ratings) related to the vector search results. This allows for rich, contextualized retrieval.

### Text-to-Cypher Retriever (`Text2CypherRetriever`)
This powerful retriever uses an LLM to translate natural language questions directly into Cypher queries, enabling semantic search over the graph.

```python
import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create Cypher LLM
t2c_llm = OpenAILLM(
    model_name="gpt-4o",
    model_params={"temperature": 0}
)

# Build the retriever
retriever = Text2CypherRetriever(
    driver=driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    llm=t2c_llm,
)

llm = OpenAILLM(model_name="gpt-4o")
rag = GraphRAG(retriever=retriever, llm=llm)

query_text = "Which movies did Hugo Weaving acted in?"
# query_text = "What are examples of Action movies?" # Another example query

response = rag.search(
    query_text=query_text,
    return_context=True
    )

print(response.answer)
print("CYPHER :", response.retriever_result.metadata["cypher"])
print("CONTEXT:", response.retriever_result.items)

driver.close()
```
*   **`t2c_llm`**: An LLM (often with a lower temperature for more deterministic output) specifically used to generate Cypher queries.
*   **`Text2CypherRetriever`**: Converts natural language `query_text` into a Cypher query, which is then executed on the Neo4j graph.
*   **Outputs**: Shows the generated Cypher query and the retrieved context.

## 4. LangChain Integration with Neo4j

Connecting to Neo4j as a LangChain graph object.

```python
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.graphs import Neo4jGraph

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')

kg = Neo4jGraph(
    url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
)
```
*   **Purpose:** Establishes a connection to a Neo4j database using `langchain_community.graphs.Neo4jGraph`, making it accessible within LangChain applications. This is useful for building agents or chains that interact with a knowledge graph.
