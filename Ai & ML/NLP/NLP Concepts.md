Here's a concise comparison of **Bag of Words (BoW)**, **TF-IDF**, and **Word2Vec**, which are techniques used in natural language processing (NLP) for text representation:

### 1. **Bag of Words (BoW)**
- **Definition**: Represents text as a collection of words, ignoring grammar and word order. Each document is a vector of word frequencies or binary indicators (word present or not).
- **How it works**: Creates a vocabulary of all unique words in the corpus and counts their occurrences in each document.
- **Pros**:
  - Simple and interpretable.
  - Works well for tasks like text classification with small datasets.
- **Cons**:
  - Ignores word order and semantics (e.g., "dog bites man" vs. "man bites dog" are treated the same).
  - High-dimensional sparse vectors.
  - Sensitive to frequent but meaningless words (e.g., "the", "is").
- **Use case**: Basic text classification, document retrieval.

### 2. **TF-IDF (Term Frequency-Inverse Document Frequency)**
- **Definition**: Enhances BoW by weighting words based on their importance. Words that appear frequently in a document but rarely across the corpus get higher weights.
- **How it works**:
  - **TF (Term Frequency)**: Frequency of a word in a document (normalized by document length).
  - **IDF (Inverse Document Frequency)**: Log of the total number of documents divided by the number of documents containing the word.
  - **TF-IDF score**: TF * IDF for each word.
- **Pros**:
  - Reduces the impact of common words (e.g., stopwords).
  - Captures word importance better than BoW.
- **Cons**:
  - Still ignores word order and semantics.
  - Sparse representation.
  - Computationally more expensive than BoW.
- **Use case**: Information retrieval, keyword extraction, text classification.

### 3. **Word2Vec**
- **Definition**: A neural network-based model that represents words as dense, low-dimensional vectors capturing semantic relationships.
- **How it works**:
  - Uses algorithms like **CBOW (Continuous Bag of Words)** or **Skip-gram** to predict words from their context (or vice versa) in a large corpus.
  - Words with similar meanings are mapped to nearby points in the vector space (e.g., "king" - "man" + "woman" ≈ "queen").
- **Pros**:
  - Captures semantic relationships (e.g., synonyms, analogies).
  - Dense vectors are computationally efficient.
  - Generalizes well across tasks.
- **Cons**:
  - Requires large training data.
  - Static embeddings (same word always has the same vector, regardless of context).
  - Doesn't handle out-of-vocabulary words well without retraining.
- **Use case**: Semantic analysis, text similarity, input to deep learning models.

### Key Differences
| Feature                | BoW                          | TF-IDF                       | Word2Vec                     |
|------------------------|------------------------------|------------------------------|------------------------------|
| **Representation**     | Sparse vector (word counts)  | Sparse vector (weighted)     | Dense vector (semantic)      |
| **Semantics**          | None                         | Limited (via weighting)      | Strong (context-based)       |
| **Word Order**         | Ignored                      | Ignored                      | Captured indirectly          |
| **Complexity**         | Low                          | Medium                       | High (training)              |
| **Use Case**           | Basic classification         | Information retrieval        | Semantic tasks, embeddings   |

### When to Use
- **BoW**: Quick prototyping or when word frequency is sufficient.
- **TF-IDF**: When you need to prioritize important words (e.g., search engines).
- **Word2Vec**: When semantic understanding is critical (e.g., recommendation systems, chatbots).

### NLP Pipeline
1. Data Loading 
2. Preprocessing ->
	- Tokenization -> split text into words
	- Stopword Removal -> removes the stopwords and common
	- Lemmatization -> reduce words to their base form
3. Feature Extraction ->
	- BOW -> BoW: Uses CountVectorizer to create a sparse matrix of word counts.
	- TF-IDF: Uses TfidfVectorizer to create a sparse matrix of weighted word scores.
	- Word2Vec : Represents words as dense, low-dimensional vectors capturing semantic relationships.
4. Model Training
5. Evaluation

### BERT 
 
 - A **transformer**-based model
 - Bi Directional **Encoder** Representations from Transformers
 - Generates **contextual word embeddings** by considering the entire sentence **bidirectionally** (both left and right context).
 - Produces contextual word embeddings
 - Each word's embedding depends on its surrounding words (e.g., "bank" in "river bank" vs. "bank account" has different embeddings).

**Use Case**: Fine-tuning for tasks like sentiment analysis, text classification, or question answering.

### Sentence Transformers

- Designed to generate sentence-level embeddings
- tasks like semantic similarity, clustering, or information retrieval.
- Produces dense, fixed-size sentence embeddings (e.g., 768-dimensional vectors) directly usable for tasks like semantic search or clustering.

**Use Case**: Semantic textual similarity, sentence clustering, paraphrase detection, or embedding documents for search.

### Key Differences

|Feature|BERT|Sentence-Transformers|
|---|---|---|
|**Output**|Token-level contextual embeddings|Fixed-size sentence embeddings|
|**Context**|Bidirectional, word-level|Sentence-level, derived from tokens|
|**Primary Use**|Fine-tuning for diverse NLP tasks|Sentence similarity, clustering|
|**Training Objective**|MLM, NSP|Sentence-pair tasks (e.g., STS, NLI)|
|**Computational Cost**|High (large model)|Moderate (optimized models available)|
|**Ease of Use**|Requires pooling for sentences|Ready-to-use sentence embeddings|

### BLEU 

- Focuses on precision, ignoring recall
- Sensitive to word order and exact matches
- Machine translation

**Use Case**: Evaluating machine translation, where exact n-gram matches are important.

### ROUGE

- Focusing on recall
- **ROUGE-N**: Measures overlap of n-grams (e.g., ROUGE-1 for unigrams, ROUGE-2 for bigrams).
- **ROUGE-L**: Measures the longest common subsequence (LCS), capturing sentence structure and word order.
- **ROUGE-S**: Measures skip-bigram overlap (allows gaps between words).
- Better for summarization where including key content is critical.
- ROUGE-L accounts for word order and structure.

**Use Case**: Evaluating text summarization, where capturing key ideas matters more than exact phrasing.

### Key Differences

| Feature                | BLEU                              | ROUGE                                   |
| ---------------------- | --------------------------------- | --------------------------------------- |
| **Focus**              | Precision (n-gram matches)        | Recall (n-gram or LCS overlap)          |
| **Penalty**            | Brevity penalty for short outputs | No explicit brevity penalty             |
| **Variants**           | Single metric (n-gram based)      | ROUGE-N, ROUGE-L, ROUGE-S               |
| **Best For**           | Machine translation               | Text summarization                      |
| **Output**             | Single score (0 to 1)             | Multiple scores (recall, precision, F1) |
| **Semantic Awareness** | None                              | None                                    |