![[Pasted image 20251012172042.png]]

#### Indexes
- Dense Index
- Sparse Index

##### Dense Index
A dense index stores [dense vectors](https://docs.pinecone.io/guides/get-started/concepts#dense-vector), which are a series of numbers that represent the meaning and relationships of text, images, or other types of data.

When you query a dense index, Pinecone retrieves the dense vectors that are the most semantically similar to the query. This is often called **semantic search**, nearest neighbor search, similarity search, or just vector search.

##### Sparse Index
- A sparse index stores [sparse vectors](https://docs.pinecone.io/guides/get-started/concepts#sparse-vector), which are a series of numbers that represent the words or phrases in a document.
- Sparse vectors have a very large number of dimensions, where only a small proportion of values are non-zero.
- The dimensions represent words from a dictionary, and the values represent the importance of these words in the document.
- When you search a sparse index, Pinecone retrieves the sparse vectors that most exactly match the words or phrases in the query.
- Query terms are scored independently and then summed, with the most similar records scored highest. This is often called **lexical search** or **keyword search**.

### Step 1. What does “index” mean here?

An **index** is a data structure that helps you **find documents fast** — instead of scanning the entire dataset every time.

There are two main styles of indexes used for retrieval:
- **Sparse index** → classic keyword-based (like BM25 or TF-IDF)
- **Dense index** → modern embedding-based (like FAISS, Pinecone, etc.)
---
### 🔹 Step 2. Sparse index — keyword-based

A **sparse index** represents text as a **sparse vector** (most entries are zero).

Example:
`"cats like milk"  → [1, 1, 1, 0, 0, ...]  # only words that appear get a 1`

- Each dimension corresponds to a **word** in the vocabulary.
- Weighting schemes like **TF-IDF** or **BM25** adjust for word frequency.
- Search compares **overlapping words** — using dot product or cosine similarity.

✅ **Pros:**
- Interpretable: you can see why a doc matches.
- Fast for small/medium corpora.
- Doesn’t need training.

❌ **Cons:**
- Ignores meaning (synonyms won’t match).
- Language-dependent.
- Fails on paraphrases or multilingual text.
---
### 🔹 Step 3. Dense index — embedding-based

A **dense index** represents each document or passage as a **dense vector** of floating-point numbers learned by a neural network (like BERT, Sentence Transformers, or OpenAI embeddings).
Example:
`"cats like milk" → [0.27, -0.14, 0.91, ...]  # 768-dimensional embedding`

- Similar texts get **closer vectors** in embedding space.
- Searching uses **cosine similarity** or **dot product** between embeddings.
- Libraries like **FAISS**, **Chroma**, **Weaviate**, **Pinecone** manage these efficiently.

✅ **Pros:**
- Captures **semantic meaning** (e.g., “dog” ≈ “puppy”).
- Works across paraphrases, languages, or noisy data.
- Great for RAG, Q&A, semantic search.

❌ **Cons:**
- Needs a trained model.
- Higher memory footprint (vectors are dense floats).
- Harder to interpret.
---
### 🔹 Step 4. Hybrid approach (real-world)

Most modern RAG systems use a **hybrid retriever**, combining both:

Score=α×DenseSimilarity+(1−α)×BM25Score\text{Score} = \alpha \times \text{DenseSimilarity} + (1 - \alpha) \times \text{BM25Score}Score=α×DenseSimilarity+(1−α)×BM25Score

This gives:
- The **semantic coverage** of dense embeddings, and
- The **precision** of sparse keyword matching.
---
### 🔹 Step 5. ASCII summary

```text
+------------------+-------------------+---------------------+
| Type             | Sparse Index      | Dense Index         |
+------------------+-------------------+---------------------+
| Representation   | Word frequencies  | Neural embeddings   |
| Example method   | TF-IDF, BM25      | BERT, OpenAI, SBERT |
| Similarity metric| Lexical overlap   | Cosine similarity   |
| Strength         | Exact matches     | Semantic matches    |
| Weakness         | No synonyms       | Requires embeddings |
| Used in RAG?     | Often hybridized  | Yes (primary)       |
+------------------+-------------------+---------------------+

```

Index Overview:
Metadata:
- Every record in an index must contain an ID and a vector.
- when you query the index, you can then include a metdata filter to limit the search to records matching a filter expression
```python
{
  "document_id": "document1",
  "document_title": "Introduction to Vector Databases",
  "chunk_number": 1,
  "chunk_text": "First chunk of the document content...",
  "is_public": true,
  "tags": ["beginner", "database", "vector-db"],
  "scores": ["85", "92"]
}
```

![[Pasted image 20251012175927.png]]

#### Hybrid Search
![[Pasted image 20251123014004.png]]

Sparse Vectors
several methods exist for building sparse vector embeddings
```python
from transformers import BertTokenizerFast  # !pip install transformers

# load bert tokenizer from huggingface
tokenizer = BertTokenizerFast.from_pretrained(
   'bert-base-uncased'
)

#to tokenize
inputs = tokenizer(
   contexts[0], padding=True, truncation=True,
   max_length=512
)
inputs.keys()
#dict_keys(['input_ids', 'token_type_ids', 'attention_mask'])
```

The output from this includes a few arrays that are all important when using transformer models. As we’re doing tokenization only, we need the `input_ids`.
```python
input_ids = inputs['input_ids']
input_ids
```

`[101, 16984, 3526, 2331, 1006, 7473, 2094, ...]`

These input IDs represent a unique word or sub-word token translated into integer ID values. This transformation is done using the BERT tokenizer’s rule-based tokenization logic.

Pinecone expects to receive sparse vectors in dictionary format. For example, the vector:

`[0, 2, 9, 2, 5, 5]`

Would become:

`{ "0": 1, "2": 2, "5": 2, "9": 1 }`

Each token is represented by a single _key_ in the dictionary, and its frequency is counted by the respective key-_value_. We apply the same transformation to our `input_ids` like so:
```python
from collections import Counter

#convert the input_ids list to a dict
sparse_vec = dict(Counter(input_ids))
sparse_vec
```

`{101: 1, 16984: 1, 3526: 2, 2331: 2, 1006: 10, ... }`

We can reformat all of this logic into two functions; `build_dict` to transform input IDs into dictionaries and `generate_sparse_vectors` to handle the tokenization _and_ dictionary creation.

```python
def build_dict(input_batch):
	#store batch of sparse embeddings
	sparse_emb = []
	
	#iterate through batch
	for token_ids in input_batch:
		indices = []
		values = []
		
		#convert input_ids list to a dict
		d = dict(Counter(token_ids))
		
		for idx in d:
			indices.append(idx)
			values.append(d[idx])
		sparse_emb.append({"indices":indices,"values":values})
		
	return sparse_emb
	
def generate_sparse_vectors(context_batch):
   # create batch of input_ids
   inputs = tokenizer(
           context_batch, padding=True,
           truncation=True,
           max_length=512, special_tokens=False
   )['input_ids']
   
   # create sparse dictionaries
   sparse_embeds = build_dict(inputs)
   return sparse_embeds
```