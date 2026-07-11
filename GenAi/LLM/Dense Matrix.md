Sparse vectors are called sparse because vectors are sparsely populated with information. Typically we would be looking at thousands of zeros to find a few ones (our relevant information). Consequently, these vectors can contain many dimensions, often in the tens of thousands.
![[Pasted image 20251124143849.png]]

Dense vectors are still highly dimensional (784-dimensions are common, but it can be more or less). However, each dimension contains relevant information, determined by a neural net — compressing these vectors is more complex, so they typically use more memory.

### **Skip-gram**
- Input: **One word** (target word)
- Output: **Predict its context words**
- Example:  
    Input = “fox”  
    Model tries to predict = “the”, “quick”, “brown”, “jumps”, …
    
![[Pasted image 20251124144316.png]]

### **CBOW**
- Input: **The context words** around a missing word
- Output: **Predict the missing word**
- Example:  
    Input = “the”, “quick”, “brown”, “jumps”, …  
    Model tries to predict = “fox”
![[Pasted image 20251124144359.png]]
---
#### Explanation (Simplified)
### **1. Word2vec → only word meaning**
Word2vec gives every word one fixed vector.  
It cannot change meaning based on context (river bank vs financial bank).

### **2. Transformers → context-aware meaning**
BERT uses self-attention, meaning it looks at **all surrounding words** and adjusts the vector accordingly.  
So “bank” gets different embeddings depending on the sentence.
### **3. But BERT only gives per-token vectors**
If you feed BERT a sentence, it outputs:
- vector for token 1
- vector for token 2
- vector for token 3  
- …

Not one vector for the whole sentence — which is what we need for tasks like
- semantic similarity
- clustering sentences
- retrieval
### **4. SBERT solves this**
Sentence-BERT adds a pooling step so the final output is:  
**one embedding that represents the entire sentence**.
### **5. Token limit**
SBERT (classic version) only works up to **128 tokens**, which is fine for sentences or short paragraphs, but too short for long documents.

---
#### Word2Vec (Skip-gram / CBOW)**
### **Goal:** Embed _words_ only
### **Output:** One vector per **word**

```
WORD2VEC
────────

"fox"  ───►  [dense vector for "fox"]

Context NOT considered deeply.
"bank" = same vector in any sentence.
```

- Produces **static word embeddings**
- Same word = same vector everywhere
- Cannot represent sentence meaning
---
#### BERT (Base Transformer Encoder)**
### **Goal:** Embed _tokens_ with **context**
### **Output:** One vector per **token**

```
BERT
────

Sentence: "The bank approved my loan."

Tokens:
[The] [bank] [approved] [my] [loan]

   │      │        │      │      │
   ▼      ▼        ▼      ▼      ▼
  v1     v2       v3     v4     v5   ← contextualized embeddings
```

- Uses **self-attention** → looks at all other words
- “bank” changes meaning depending on the sentence
- But still: **No single sentence vector**
---
##### SBERT (Sentence-BERT)**
### **Goal:** One vector per entire **sentence**
### **Output:** Single embedding

```
SBERT
─────

Sentence: "The bank approved my loan."

       ┌───────────────────────────┐
Tokens │  contextual embeddings    │
       └───────────────────────────┘
                │
                ▼
        POOLING (mean/max/CLS)
                │
                ▼
   Final Sentence Vector (768-dim)
```

- Takes BERT token embeddings
- Applies **pooling** to convert them into **one sentence embedding**
- Designed for:
    - semantic similarity
    - clustering
    - retrieval
    - sentence-level tasks
---
#### Concept Summary**

| Model        | Embeds    | Context-aware? | Output                     |
| ------------ | --------- | -------------- | -------------------------- |
| **Word2Vec** | Words     | ❌ static       | 1 vector per word          |
| **BERT**     | Tokens    | ✔️ dynamic     | Many vectors (1 per token) |
| **SBERT**    | Sentences | ✔️ dynamic     | **1 vector per sentence**  |

---
Here is a high-level illustration of the Dense Passage Retriever (DPR) process, broken down into the two main phases: Indexing and Retrieval.

### Dense Passage Retriever (DPR) Process
### Phase 1: Indexing (Pre-Calculation)
This phase happens once to set up the knowledge base.
1. **Context Split:** The entire corpus of knowledge (e.g., Wikipedia) is split into small, manageable passages (contexts).
2. **Context Encoding:** Each passage is passed through the **Context Encoder** (one of the two BERT-based models).
3. **Vector Storage:** The resulting vector (embedding) for each passage is calculated and stored in a specialized, searchable database (a vector database, often using algorithms like FAISS).

**Result:** A large, searchable index of high-dimensional vectors, where each vector represents a potential answer passage.

---
### Phase 2: Retrieval (Runtime Search)
This phase happens every time a user asks a question.
1. **Question Input:** The user asks a question (e.g., "What is the capital of France?").
2. **Question Encoding:** The question is passed through the **Query Encoder** (the second BERT-based model).
3. **Vector Generation:** The Query Encoder produces a single query vector.
4. **Similarity Search:** The query vector is compared against all the pre-calculated context vectors in the database (Phase 1). The search is based on vector similarity (e.g., dot product or cosine similarity).
5. **Context Retrieval:** The top $K$ most similar context vectors are returned. These vectors correspond to the passages most likely to contain the answer.
**Result:** A small number of highly relevant passages that are then passed to the **Reader** model (the third component of ODQA) to extract the final, precise answer.
![[Pasted image 20251124161657.png]]

