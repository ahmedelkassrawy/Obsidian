## 🔍 What is Semantic Search?
**Semantic search** is a way of searching that tries to understand the _meaning_ (semantics) of your query, not just the _keywords_.
- **Normal search (keyword-based):** Looks for exact matches of words.
    > Example: If you search _“apple laptop”_, it literally looks for those words.
- **Semantic search:** Tries to understand what you mean and find results that are conceptually similar.
    > Example: If you search _“best notebook for coding”_, it could still return results about _MacBook_ or _Dell XPS_, even if those exact words weren’t used.
---
## ⚙️ How it works (simplified)
1. **Text → Vectors (embeddings):** Each word, sentence, or document is converted into a vector (a list of numbers) that captures its meaning.
    - Example: “king” and “queen” end up with vectors close to each other.
2. **Similarity search:** When you type a query, it’s also turned into a vector. The system finds documents whose vectors are closest to the query vector (using math like cosine similarity).
3. **Results ranked by meaning, not just exact words.**
---

## [[Semantic Search]] and [[Retrieval-Augmented Generation (RAG)]]

Search was one of the first applications of language models to see broad industry adoption.

### Overview of Key Concepts

The ability for systems to enable searching by **meaning**, rather than just keyword matching, is called **semantic search**. There are three broad categories of models used to enhance search: **dense retrieval**, **reranking**, and **RAG** (Retrieval-Augmented Generation).

RAG is a method that retrieves relevant information and provides it to a Large Language Model (LLM) to aid in generating more **factual answers**. This method is popular because it reduces the problem known as **hallucinations** (when models generate fluent, confident, but incorrect or outdated answers).

#### 1. [[Dense Retrieval]]

Dense retrieval systems rely on the concept of **embeddings**.
*   **Embeddings** turn text into numeric representations.
*   The search query and documents are converted into embeddings.
*   Similar meaning texts are close together in the vector space (like points on a graph).
*   The system retrieves results by finding the **nearest neighbors** to the search query's embedding.

**Handling Long Texts (Chunking):**
Transformer language models have limitations in context size, meaning they cannot process very long texts. To manage this, long documents must be split into smaller pieces, or **chunks**.

Approaches to representing a document's embedding:
1.  **One vector per document:** This involves embedding a representative part (like the title or beginning) or aggregating chunks. A drawback is that this often loses a lot of information contained in the document.
2.  **Multiple vectors per document (Chunking):** The document is chunked into smaller pieces, and embeddings are created for each chunk. This approach allows for better coverage of the text and enables vectors to capture individual concepts.

Possible methods for chunking include splitting by **sentence**, **paragraph**, or using **overlapping windows** of tokens or sentences, which helps retain context across chunks.

**Fine-Tuning Embedding Models:**
The performance of dense retrieval can be improved by optimizing text embeddings through **fine-tuning**. This process trains the model to make the embeddings of **relevant queries** closer to the corresponding document, while making **irrelevant queries** farther away in the vector space.

#### 2. [[Reranking]]

Reranking systems operate as a step in a multi-step search pipeline.
*   A reranking language model is tasked with **scoring the relevance** of an initial set of results (often retrieved by dense retrieval or keyword search) against the original query.
*   The results are then reordered based on these relevance scores, often resulting in vastly improved results.
*   One popular way to build LLM search rerankers is using a **cross-encoder**, where the query and each result are presented to the LLM simultaneously to assign a relevance score.

#### 3. [[Retrieval-Augmented Generation (RAG)]]

A RAG system is a type of **generative search** system that incorporates search capabilities. The RAG pipeline consists of two main steps:

1.  **Retrieval (and Reranking):** Relevant documents or chunks are retrieved from the data source.
2.  **Grounded Generation (LLM):** The LLM is prompted with the original question and the retrieved relevant information (context). This establishes a **certain context** that "grounds" the LLM's output.

RAG systems formulate an answer and (preferably) **cite its information sources**.

### Advanced RAG Techniques

To improve performance and handle complex queries, several advanced RAG techniques exist:

*   **Query rewriting:** If a user's question is verbose, an LLM can be used to **rewrite the query** into a more precise version that aids retrieval.
*   **Multi-query RAG:** Complex questions are broken down into **multiple search queries** to retrieve necessary information for the final answer.
*   **Multi-hop RAG:** A series of sequential queries is used, where the output of one step informs the follow-up questions.
*   **Query routing:** The model is given the ability to search across multiple data sources (e.g., routing an HR question to the HR information system).
*   **Agentic RAG:** The LLM takes on more responsibility, delegating tasks and acting as an agent that utilizes tools and multiple data sources.

### Evaluation Metrics

#### Search System Evaluation
Search systems are often evaluated using metrics from the Information Retrieval (IR) field, such as **Mean Average Precision (MAP)**. Evaluating search systems requires a test suite, which includes:
*   A **text archive**.
*   A **set of queries**.
*   **Relevance judgments** (indicating which documents are relevant for each query).

**Average precision** is a metric that rewards a system for placing relevant results in the most important positions (at the top of the list). MAP is calculated by taking the mean of the average precision scores across all queries in the test suite.

#### RAG Evaluation
RAG models are evaluated along multiple axes using human evaluations or by using a capable LLM as a judge (called **LLM-as-a-judge**). Key metrics include:
*   **Fluency:** Whether the generated text is cohesive and fluent.
*   **Perceived utility:** Whether the answer is helpful and informative.
*   **Citation recall:** The proportion of generated statements that are fully supported by their citations.
*   **Citation precision:** The proportion of generated citations that support their associated statements.
*   **Faithfulness:** Whether the answer is consistent with the provided context.
*   **Answer relevance:** How relevant the answer is to the original question.