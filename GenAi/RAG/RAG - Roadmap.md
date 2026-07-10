![[Pasted image 20251011175322.png]]

1. Knowledge Base Creation
2. Generation Part
#### Knowledge Base Creation
This process involves:
- **Chunking**: Split the text into chunks of sub-documents to simplify ingestion.
- **Embedding**: Compute numerical embeddings for each chunk to understand the semantic similarity to queries.
- **Storage**: Store the embeddings in a way that allows quick retrieval. While a vector store/DB is often used, this tutorial shows that it's not essential.

Core Steps:
1. **Data Loading:** Read text data from a file.
2. **Chunking:** Split the text into manageable chunks.
3. **Embedding Simulation:** Create simple numerical representations (simulated embeddings).
4. **Semantic Search (Similarity):** Implement a basic similarity calculation.
5. **Response Generation (Placeholder):** Use a simple string concatenation as a placeholder for LLM response.
6. **Evaluation (Basic String Matching):** Evaluate the generated response against a known answer.