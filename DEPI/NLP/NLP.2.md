
| **Bag of words**     |
| -------------------- |
| **N-GRAM**           |
| **TF-IDF**           |
| **One Hot Encoding** |
# Bag of Words (BoW)

It is a technique used to **convert text into numeric numbers**. It is used with important tasks in NLP like **text classification** and **sentiment analysis**.

> [!info] Key Insight
> Very similar to [[One Hot Encoding]].

![[Pasted image 20260424172104.png]]

> [!important] Core Principle
> The **order of the words** here is **not important** and doesn't affect the formation of the vector. What matters is the **frequency** of each word.

## Example

| Document | Text & Frequency Breakdown |
|:--------:|:---------------------------|
| **Document D1** | *The child makes the dog happy* <br><br> the: 2, dog: 1, makes: 1, child: 1, happy: 1 |
| **Document D2** | *The dog makes the child happy* <br><br> the: 2, child: 1, makes: 1, dog: 1, happy: 1 |

### BoW Vector Representations

| | **child** | **dog** | **happy** | **makes** | **the** | **BoW Vector** |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **D1** | 1 | 1 | 1 | 1 | 2 | **[1, 1, 1, 1, 2]** |
| **D2** | 1 | 1 | 1 | 1 | 2 | **[1, 1, 1, 1, 2]** |

---
## Notes on Preprocessing

> [!warning] Important Preprocessing Steps
> - It's better to **convert all letters to lowercase** before applying BoW because if it encounters "he" and "He", it will put each one in a separate column and calculate their frequency separately.
> - Also, **remove the stop words** because they are very repetitive, so they will have high frequency numbers, and then the model will mistakenly think that they are more important, which is wrong.

### Example: Removing Stop Words

- Sentence 1 → He is a good boy **(Remove stop words →)** good boy
- Sentence 2 → She is a good girl **(Remove stop words →)** good girl
- Sentence 3 → Boy and girl are good **(Remove stop words →)** boy girl good

**Resulting Vectors:**

| | **good** | **boy** | **girl** |
|:---:|:---:|:---:|:---:|
| **Sentence 1** | 1 | 1 | 0 |
| **Sentence 2** | 1 | 0 | 1 |
| **Sentence 3** | 1 | 1 | 1 |

---
## Bag-of-Words using `sklearn`

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

data = {
    'text': [
        'I love programming in Python',
        'Python is an amazing language',
        'I dislike bugs in the code',
        'Debugging is fun',
        'I enjoy learning new technologies',
        'This is a boring task',
        'I find machine learning fascinating',
        'I hate getting errors in my code'
    ],
    'label': ['positive', 'positive', 'negative', 'positive', 'positive', 'negative', 'positive', 'negative']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42
)

# Step 4: Create Bag-of-Words Representation
vectorizer = CountVectorizer()
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

# Convert the Bag-of-Words representation to a dense array
X_train_bow_dense = X_train_bow.toarray()

# Get the feature names (words) from the vectorizer
feature_names = vectorizer.get_feature_names_out()

# Create a DataFrame for better readability
bow_df = pd.DataFrame(X_train_bow_dense, columns=feature_names)

# Print the DataFrame
print(bow_df)
```

### Output Example

```
   bugs  code  debugging  dislike  enjoy  errors  fascinating  find  fun \
0     0     0          0        0      0       0            0     0    0
1     0     1          0        0      0       1            0     0    0
2     1     1          0        1      0       0            0     0    0
3     0     0          0        0      1       0            0     0    0
4     0     0          1        0      0       0            0     0    1
5     0     0          0        0      0       0            1     1    0
```
---
# N-GRAM

> [!important] Core Idea
> Thinking of dealing with each word individually isn't the best because it makes us **lose the ==sentence's meaning==.**

For example, if we take each word separately, =="book"== could mean a book in both instances. However, ==when it's used with another word before or after it, the meaning changes.== It could be understood as a verb, meaning to reserve, and the second instance would be understood as a book.

**Consider these two sentences:**

> We need to ==book== our tickets soon.
>
> We need to read this ==book== soon.

## Types of N-GRAM

> [!info] Note
> There are many N-GRAMs, not just two (Bi-Gram).

### Example 1: `This is a sentence`

|     N     | Type     | Tokens                          |
| :-------: | :------- | :------------------------------ |
| **N = 1** | Unigrams | `this`, `is`, `a`, `sentence`   |
| **N = 2** | Bigrams  | `this is`, `is a`, `a sentence` |
| **N = 3** | Trigrams | `this is a`, `is a sentence`    |

### Example 2: `This is Big Data AI Book`

**Bigrams (N=2):**

| | **Is** | **Big** | **Data** | **AI** |
|:---|:---|:---|:---|:---|
| **is** | Is Big | Big Data | Data AI | AI Book |

**Trigrams (N=3):**

| | **Is Big** | **Big Data** | **Data AI** |
|:---|:---|:---|:---|
| **is Big** | Is Big Data | Big Data AI | Data AI Book |
## N-GRAM in `sklearn`

```python
data = {
    'text': [
        'I love programming in Python',
        'Python is an amazing language',
        'I dislike bugs in the code',
    ],
    'label': ['positive', 'positive', 'negative']
}

# Set ngram_range to (1, 2) for unigrams and bigrams
vectorizer = CountVectorizer(ngram_range=(1, 2))
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

# Convert the Bag-of-Words representation to a dense array
X_train_bow_dense = X_train_bow.toarray()

# Get the feature names (unigrams and bigrams) from the vectorizer
feature_names = vectorizer.get_feature_names_out()

# Create a DataFrame for better readability
bow_df = pd.DataFrame(X_train_bow_dense, columns=feature_names)

# Print the DataFrame
display(bow_df)
```

### Output DataFrame Example

| amazing | amazing language | an  | an amazing | bugs | bugs in | code | dislike | dislike bugs | in  | in the | is  | is an | language | python | python is | the | the code |
| :-----: | :--------------: | :-: | :--------: | :--: | :-----: | :--: | :-----: | :----------: | :-: | :----: | :-: | :---: | :------: | :----: | :-------: | :-: | :------: |
|    1    |        1         |  1  |     1      |  0   |    0    |  0   |    0    |      0       |  0  |   0    |  1  |   1   |    1     |   1    |     1     |  0  |    0     |
|    0    |        0         |  0  |     0      |  1   |    1    |  1   |    1    |      1       |  1  |   1    |  0  |   0   |    0     |   0    |     0     |  1  |    1     |

> [!tip] Key Takeaway
> The `ngram_range=(1, 2)` parameter captures both **unigrams** (single words) and **bigrams** (pairs of adjacent words), helping preserve some word order and context compared to standard Bag of Words.

---
# TF-IDF

> [!abstract] Definition
> ==TF-IDF stands for Term Frequency - Inverse Document Frequency==

- We previously discussed using [[Bag of Words|BOW]] and [[N-GRAM]] to represent text as vectors.
- TF-IDF has a big advantage over the ==BOW in that it focuses more on the weight in the sentence==, ==meaning that the most influential word in the sentence will have a higher value or number than the other words.==
- The BOW method worked on the ==frequency==, meaning that words that are repeated often have a higher value, ==which is not correct because we find that rare words have more impact on the meaning of the sentence. Also, stopwords like "the," "and," and "or" are not influential at all. So, I used to remove them before applying the BOW method. TF-IDF gives a lower value to frequently repeated words because they are not as influential as stopwords.==

---
## How TF-IDF Works

1. It calculates the **TF** for each ==unique word==, which is the number of times each word appears in the sentence divided by the total number of words in that sentence.

2. To get the **IDF** for each ==unique word,== we calculate the ==logarithm== of the total number of sentences divided by the number of sentences containing that word.

3. After that, ==multiply each column== in the TF by the IDF column to get the ==final vectors.==

4. In the end, you will have a ==set of features== that are the ==unique words== in the form of ==vectors.==

---
## Formulas

> [!info] Key Formulas
>
> $$ \text{TF} = \frac{\text{No. of repetitions in a sentence}}{\text{No. of words in a sentence}} $$
>
> $$ \text{IDF} = \log\left(\frac{\text{No. of sentences}}{\text{No. of sentences containing the word}}\right) $$

---
## Example

- **Sen 1:** good boy
- **Sen 2:** good girl
- **Sen 3:** boy girl good

### Step 1: Calculate TF

| | **Sen 1** | **Sen 2** | **Sen 3** |
|:---:|:---:|:---:|:---:|
| **Good** | 1/2 | 1/2 | 1/3 |
| **Boy** | 1/2 | 0 | 1/3 |
| **Girl** | 0 | 1/2 | 1/3 |

### ✕ *(multiplied by)*

### Step 2: Calculate IDF

| Word | IDF |
|:---:|:---|
| **Good** | log(3/3) = 0 |
| **Boy** | log(3/2) |
| **Girl** | log(3/2) |

> [!warning] Note
> The word "good" gets an IDF of **0** because it appears in **all 3 sentences**, so it's considered not discriminative.

### Step 3: Final Output Vectors (TF × IDF)

| | **good** | **boy** | **girl** |
|:---:|:---:|:---:|:---:|
| **Sen 1** | 0 | ½ × log(3/2) | 0 |
| **Sen 2** | 0 | 0 | ½ × log(3/2) |
| **Sen 3** | 0 | ⅓ × log(3/2) | ⅓ × log(3/2) |

---
## TF-IDF in `sklearn`

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Convert the TF-IDF representation to a dense array
X_train_tfidf_dense = X_train_tfidf.toarray()

# Get the feature names (words) from the vectorizer
feature_names = vectorizer.get_feature_names_out()

# Create a DataFrame for better readability
tfidf_df = pd.DataFrame(X_train_tfidf_dense, columns=feature_names)

# Print the DataFrame
display(tfidf_df)
```

### Output Example

```
       bugs      code  debugging   dislike     enjoy    errors  fascinating      find       fun   getting ..
0  0.000000  0.000000   0.000000  0.000000  0.000000  0.000000     0.000000  0.000000  0.000000  0.000000
1  0.000000  0.361281   0.000000  0.000000  0.000000  0.440579     0.000000  0.000000  0.000000  0.440579
2  0.490779  0.402446   0.000000  0.490779  0.000000  0.000000     0.000000  0.000000  0.000000  0.000000
3  0.000000  0.000000   0.000000  0.000000  0.521823  0.000000     0.000000  0.000000  0.000000  0.000000
4  0.000000  0.000000   0.577350  0.000000  0.000000  0.000000     0.000000  0.000000  0.577350  0.000000
5  0.000000  0.000000   0.000000  0.000000  0.000000  0.000000     0.521823  0.521823  0.000000  0.000000
6 rows × 22 columns
```

> [!tip] Key Takeaway
> Unlike BOW, TF-IDF assigns **higher weights to rare, informative words** and **lower weights to frequent, less meaningful words** (including stopwords), making it a more robust text representation technique.

---
# One Hot Encoding

One-hot encoding is a technique used in natural language processing (NLP) to represent words as vectors in a high-dimensional space. This method is particularly useful for converting categorical text data into a numerical format.

## Example

**Sentence:** "Hello, I'm Ironman. I have Friday AI"

| | | | | | | | |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **AI** | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Ironman** | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **Friday** | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| **have** | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| **Hello** | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| **I** | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| **I'm** | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

---
## Limitations of One Hot Encoding

> [!failure] Why One Hot Encoding Isn't Good for Large Data

Let's assume that my vocabulary has 10k unique words. When the word "man" is encountered, it will look at its index and set it to 1, while all other indices (from 0 to 9999) will be set to 0.

==This approach creates three problems:==

1. **Large Number of Features:** It creates a very large number of features.
2. **Sparse Matrix Problem:** ==Sparse matrix== — most of the values are zeros and very few are ones.
3. **No Semantic Preservation:** It won't preserve semantics. Why? Because if words like =='orange' and 'apple'== are both very close to each other in meaning, but one comes first and the other comes last, their vectors will be completely different from each other.

---
# Word Embeddings

> [!abstract] Definition
> A word embedding is a learned representation for text where words that have the same meaning have a **similar representation**.

It is this approach to representing words and documents that may be considered one of the key breakthroughs of deep learning on challenging natural language processing problems.

---

## Why Are Word Embeddings Needed?

Consider these two sentences:
- "You can ==scale== your business."
- "You can ==grow== your business."

These two sentences have the **same meaning**. If we consider a vocabulary from these sentences, it will constitute: =={You, can, scale, grow, your, business}.==

A ==one-hot encoding of these words== would create a vector of length 6:

| Word | Vector |
|:---:|:---|
| **You** | `[1, 0, 0, 0, 0, 0]` |
| **Can** | `[0, 1, 0, 0, 0, 0]` |
| **Scale** | `[0, 0, 1, 0, 0, 0]` |
| **Grow** | `[0, 0, 0, 1, 0, 0]` |
| **Your** | `[0, 0, 0, 0, 1, 0]` |
| **Business** | `[0, 0, 0, 0, 0, 1]` |

> [!warning] The Problem
> In a 6-dimensional space, each word occupies one dimension, meaning **none of these words has any similarity with each other** — irrespective of their literal meanings.

> [!success] The Solution
> ==**Word2Vec**==, a word embedding methodology, solves this issue and enables similar words to have similar dimensions, consequently helping bring context.

---
## Word Embedding Algorithms

- ==Embedding Layer==
- ==Word2Vec==

---
## Embedding Layer

- It's about algorithms we use to represent words as vectors.
- Its real advantage is that it can **handle semantics** — words that have the same meaning or similar context get vectors that are close to each other.
  - Example: **apple, orange, banana** → all fruits → vectors close to each other.
  - Example: **man and woman** → vectors close to each other.
- We apply it using neural network models like **Word2Vec**, **GloVe**, and **FastText**.

### Visualizing Word Embeddings

| | living being | feline | human | gender | royalty | verb | plural |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **cat** | 0.6 | 0.9 | 0.1 | 0.4 | -0.7 | -0.3 | -0.2 |
| **kitten** | 0.5 | 0.8 | -0.1 | 0.2 | -0.6 | -0.5 | -0.1 |
| **dog** | 0.7 | -0.1 | 0.4 | 0.3 | -0.4 | -0.1 | -0.3 |
| **man** | 0.6 | -0.2 | 0.8 | 0.9 | -0.1 | -0.9 | -0.7 |
| **woman** | 0.7 | 0.3 | 0.9 | -0.7 | 0.1 | -0.5 | -0.4 |
| **king** | 0.5 | -0.4 | 0.7 | 0.8 | 0.9 | -0.7 | -0.6 |
| **queen** | 0.8 | -0.1 | 0.8 | -0.9 | 0.8 | -0.5 | -0.9 |

---
## One-Hot vs. Word Embeddings

### One-Hot Encoding (Sparse, 10k dimensions)
Man index = 5k, Woman index = 9k

| man | woman |
|:---:|:---:|
| 0 | 0 |
| 0 | 0 |
| 0 | 0 |
| 1 | 0 |
| 0 | 0 |
| 0 | 0 |
| 0 | 1 |

> [!error] Issues: Sparse, no semantic similarity, high dimensionality.

### Word Embeddings (Dense Feature Representation, 10 dimensions)

| | Boy (2000) | Girl (5000) | King (6000) | Queen (9000) | Apple (1000) | Mango (7000) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Gender** | -1 | 1 | -0.92 | 0.93 | 0.0 | 0.1 |
| **Royal** | 0.01 | 0.02 | 0.95 | 0.96 | -0.02 | 0.01 |
| **Age** | 0.5 | 0.5 | 0.7 | 0.6 | 0.95 | 0.92 |
| **Food** | — | — | — | — | — | — |

> [!success] Advantages: Dense, captures semantic relationships, lower dimensionality.

---
## Summary

> [!summary] Key Points
> 1. Define the **vocab size** and get the **indices** of the words.
> 2. Apply embedding on those indices to convert them into **vectors** (features).
> 3. Evaluate word embeddings through:
>    - **Word Similarity:** How close are similar words?
>    - **Word Analogy:** e.g., King - Man + Woman ≈ Queen

---
# Word Embeddings — Implementation

> [!info] Key Evidence
> Word embeddings convert words into vectors while considering **semantic meaning** — words with similar meanings will have close vectors.
>
> If we apply **PCA** and visualize, words like **best, good, excellent** will be found very close to each other.

---

## Embedding Layer Implementation

### 1. One-Hot Representation

```python
from tensorflow.keras.preprocessing.text import one_hot

### sentences
sent = [
    'the glass of milk',
    'the glass of juice',
    'the cup of tea',
    'I am a good boy',
    'I am a good developer',
    'understand the meaning of words',
    'your videos are good',
]

### Vocabulary size >>>> the size of one hot encoding
voc_size = 10000

# will make one hot encoding and return each sentence with its indices
onehot_repr = [one_hot(words, voc_size) for words in sent]
print(onehot_repr)
```

**Output:**
```text
[[5853, 812, 6103, 5337], [5853, 812, 6103, 2686], [5853, 9090, 6103, 8774], [6067, 1010, 1760, 4399, 9258], [6067, 1010, 1760, 4399, 4352], [2859, 5853, 2496, 6103, 8076], [4424, 1094, 1493, 4399]]
```

---

### 2. Padding Sequences

```python
from tensorflow.keras.preprocessing.sequence import pad_sequences

sent_length = 8
embedded_docs = pad_sequences(onehot_repr, padding='pre', maxlen=sent_length)
print(embedded_docs)
```

**Output:**
```text
[[   0    0    0    0 2304 4048  200 7085]
 [   0    0    0    0 2304 4048  200 6410]
 [   0    0    0    0 2304 1861  200 5028]
 [   0    0    0 3536 9320 8210  995 1424]
 [   0    0    0 3536 9320 8210  995 8627]
 [   0    0    0 5261 2304  987  200 1845]
 [   0    0    0    0 6496 1088 9507  995]]
```

---

### 3. Creating the Embedding Model

```python
from keras.models import Sequential
from keras.layers import Embedding

model = Sequential()
model.add(Embedding(voc_size, 10))
model.compile('adam', 'mse')
```

> [!info] Parameter Explanations
>
> | Parameter | Description |
> |:---:|:---|
> | **`voc_size`** | The size of the vocabulary (number of unique tokens/words in your dataset). |
> | **`10`** | The size of the dense embedding vectors. Each token is mapped to a **10-dimensional vector**. |

> [!note] Key Function
> This layer converts integer-encoded tokens into **dense vectors** of size 10.

---

### 4. Predicting with the Model

```python
# first sentence after onehot + padding
print(embedded_docs[0])
```
**Output:** `array([   0,    0,    0,    0, 5853,  812, 6103, 5337], dtype=int32)`

```python
# first sentence after embedding
print(model.predict(embedded_docs)[0])
```
**Output (A dense 8×10 matrix representing the 8 padded tokens):**
```text
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 20ms/step
[[ 0.02706667  0.04142978  0.03326375 -0.01022017  0.03536961  0.01260928
  -0.03661736 -0.00810615 -0.02808102 -0.0149346 ]
 [ 0.02706667  0.04142978  0.03326375 -0.01022017  0.03536961  0.01260928
  -0.03661736 -0.00810615 -0.02808102 -0.0149346 ]
 ...
 [-0.00304006  0.04683647 -0.00914602 -0.0212866  -0.02520748 -0.00275395
  -0.00500282  0.02024866 -0.04726223  0.03458563]]
```

---

# Word2Vec

> [!abstract] Definition
> Word2Vec is a **statistical method** for efficiently learning a standalone word embedding from a text corpus.

## Two Learning Models

Word2Vec introduced two different learning models:

- ==Continuous Bag-of-Words (CBOW)==
- ==Continuous Skip-Gram==

### Architectural Differences

| Model | Description |
|:---:|:---|
| **CBOW** | Predicts a **target word** based on its surrounding context words. |
| **Skip-gram** | Predicts **surrounding context words** based on a single target word. |

> [!tip] Semantic Relationships
> These embeddings capture spatial and semantic relationships, often visualized as parallel vectors in high-dimensional space.
>
> **Classic Example:**
> The vector relationship between `man` → `woman` is parallel to `king` → `queen`.
>
> $$ \text{king} - \text{man} + \text{woman} \approx \text{queen} $$

---
# Word2Vec Architectures

> [!abstract] Key Insight
> Even though ==Word2Vec is an unsupervised model== where you can give a corpus without any label information and the model can create dense word embeddings, Word2Vec **internally leverages a supervised classification model** to get these embeddings from the corpus.

---
## CBOW (Continuous Bag-of-Words)

### How Does CBOW Work?

The CBOW architecture comprises a deep learning classification model in which we take in **context words as input ($X$)** and try to **predict our target word ($Y$)** .

> [!example] Example
> Consider the sentence: "Word2Vec has a deep learning model working in the backend."
>
> With a **context window size of 2**, we get pairs like:
> - ==([deep, model], learning)==
> - ==([model, in], working)==
> - ==([a, learning], deep)==
>
> The deep learning model tries to predict these target words based on the context words.

### CBOW Architecture Flow

```
Input Context Words: w(t-2), w(t-1), w(t+1), w(t+2)
              ↓
            SUM
              ↓
    Output Target Word: w(t)
```

### Steps: How the Model Works

1. The **context words** are first passed as an input to an **embedding layer** (initialized with some random weights).
2. The word embeddings are then passed to a **lambda layer** where we **average out** the word embeddings.
3. We then pass these embeddings to a **dense SoftMax layer** that predicts our target word. We match this with our target word and compute the loss, then perform **backpropagation** with each epoch to update the embedding layer.
4. We can extract the embeddings of the needed words from our embedding layer once training is completed.

### CBOW Model Visualization

```
> Input: W(t-n) ... W(t-1) W(t+1) ... W(t+n)
        ↓
Embedding Layer (vocab_size × embed_dim)
        ↓
Lambda Layer (Average Embeddings)
        ↓
Dense Layer (Softmax)
        ↓
> Output: w(t)
  (Compute Loss and BackProp)
```

---
## Skip-Gram

### How Does Skip-Gram Work?

==In the skip-gram model==, given a **target (centre) word**, the **context words** are predicted using ==word representations==.

> [!example] Example
> Consider the same sentence: "Word2Vec has a ==neural networks== working in the backend." with a context window size of 2.
>
> Given the centre word **'learning'**, the model tries to predict **[‘deep’, ‘model’]** and so on.
>
> This prediction process is fundamental to ==language modeling== and the creation of ==vector representations== of words.

Since the skip-gram model has to predict **multiple words from a single given word**, we feed the model pairs of **(X, Y)** where X is input and Y is label. This is done by creating ==positive input samples and negative input samples.==

### Skip-Gram Architecture Flow

```
Target Word: w(t)
       ↓
    predicts
       ↓
Context Words: w(t-2), w(t-1), w(t+1), w(t+2)
```
*(Example: The word "sat" is used to predict surrounding context like "The cat ... on the mat")*

---

### Positive and Negative Samples

| Sample Type | Format | Label | Description |
|:---|:---|:---:|:---|
| **Positive Input** | `[(target, context), 1]` | 1 | Target word paired with actual surrounding context words (relevant pair). |
| **Negative Input** | `[(target, random), 0]` | 0 | Target word paired with randomly selected words (irrelevant pair). |

> [!tip] Purpose
> These samples make the model aware of contextually relevant words and consequently generate **similar embeddings for similar meaning words**.

### Steps: How the Model Works

1. Both the **target** and **context word pairs** are passed to individual **embedding layers** from which we get dense word embeddings for each of these two words.
2. We then use a **'merge layer'** to compute the **dot product** of these two embeddings and get the dot product value.
3. This dot product value is then sent to a **dense sigmoid layer** that outputs either **0 or 1**.
4. The output is compared with the actual label and the loss is computed followed by **backpropagation** with each epoch to update the embedding layer.

### Skip-Gram Model Visualization

```
> Inputs: Target Word W(t) AND Context Word W(c)
        ↓
Embedding Layer (vocab_size × embed_dim) [for both inputs]
        ↓
Merge Layer (Dot Product of W(t) and W(c) embeddings)
        ↓
Dense Layer (Sigmoid)
        ↓
> Output: Y' (1 or 0)
  (Compare with actual Y label, Compute Loss and BackProp)
```

---

## CBOW vs. Skip-Gram

| | CBOW | Skip-Gram |
|:---|:---|:---|
| **Direction** | Context → Target Word | Target Word → Context |
| **Speed** | Faster to train | Slower to train |
| **Performance** | Better for frequent words | Better for rare words |
| **Architecture** | Averages context embeddings | Uses dot product of target & context |

---

## Word2Vec in Python (Gensim)

```python
import gensim
from gensim.models import Word2Vec

# Sample data: list of sentences
sentences = [
    ['hello', 'world'],
    ['I', 'love', 'natural', 'language', 'processing', 'like', 'python'],
    ['word2vec', 'is', 'a', 'great', 'tool'],
    ['chatgpt', 'helps', 'with', 'coding', 'and', 'writing'],
    ['this', 'is', 'a', 'simple', 'example']
]

# Train the Word2Vec model
model = Word2Vec(sentences, vector_size=50, window=3, min_count=1, sg=0)
```

> [!info] Parameter Explanations
>
> | Parameter | Description |
> |:---|:---|
> | **`vector_size`** | Dimensionality of the word vectors. |
> | **`window`** | Maximum distance between the current and predicted word within a sentence. |
> | **`min_count`** | Ignores all words with total frequency lower than this. |
> | **`sg`** | Training algorithm: **1** for skip-gram; **0** for CBOW. |

### Get Vector for a Specific Word

```python
# Get the vector for a specific word
word_vector = model.wv['word2vec']
print(word_vector)
```