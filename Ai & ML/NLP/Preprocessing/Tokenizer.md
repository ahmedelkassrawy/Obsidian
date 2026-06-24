**Tokenizer** -> make the text have numerical representations called token indices
### Types
- Word based
- Char based
- Subword based

```python
#Word Based
#NLTK

import nltk 
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')

text = text = "This is a sample sentence for word tokenization."
tokens = word_tokenize(text)
print(tokens)
```

```python
#spacy

import spacy
from spacy.lang.en.stop_words import STOP_WORDS


text = "I couldn't help the dog. Can't you do it? Don't be afraid if you are."
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

for w in doc:
  print(w)
```

```python
text = "I couldn't help the dog. Can't you do it? Don't be afraid if you are."
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

#make a list of tokenbs , print the list
token_list = [token.text for token in doc]
print("Tokens:",token_list)

for token in doc:
  print(token.text,token.pos_,token.dep_)
```
## DataLoaders

Finally, a data loader can be used for tasks such as tokenizing, sequencing, converting your samples to the same size, and transforming your data into tensors that your model can understand.
You will begin by defining a custom data set called CustomDataset.
This data set inherits from the `torch.utils.data.Dataset` class and is initialized with a list of sentences. The data set comprises two essential methods:
- **init**(self, sentences): Initializes the data set with a list of sentences.
- **getitem**(self, idx): Retrieves an item (in this case, a sentence) at a specific index, idx.


The changes made to the CustomDataset class are as follows:
- **init**: The constructor takes a list of sentences, a tokenizer function, and a vocabulary (vocab) as input.
- **len**: This method returns the total number of samples in the data set.
- **getitem**: This method is responsible for processing a single sample. It tokenizes the sentence using the provided tokenizer and then converts the tokens into tensor indices using the vocabulary.

```python
sentences = [
    "If you want to know what a man's like, take a good look at how he treats his inferiors, not his equals.",
    "Fame's a fickle friend, Harry.",
    "It is our choices, Harry, that show what we truly are, far more than our abilities.",
    "Soon we must all face the choice between what is right and what is easy.",
    "Youth can not know how age thinks and feels. But old men are guilty if they forget what it was to be young.",
    "You are awesome!"
]

#Define custom dataset
class CustomDataset(Dataset):
  def __init__(self,sentences):
    self.sentences = sentences

  def __len__(self):
    return len(self.sentences)

  def __getitem__(self, idx):
    return self.sentences[idx]

custom_dataset = CustomDataset(sentences)

batch_size = 2
dataloader = DataLoader(custom_dataset,
                        batch_size = batch_size,
                        shuffle = True)

for batch in dataloader:
    print(batch)
```

You will begin by defining a custom collate function named `collate_fn`. This function plays a crucial role when handling sequences of varying lengths, such as sentences in NLP. Its purpose is to pad sequences within a batch to have equal lengths, which is a common preprocessing step in NLP tasks.

`pad_sequence`: This function is a part of PyTorch and is utilized to pad sequences in a batch, ensuring uniform length. It takes a batch of sequences as input and pads them to match the length of the longest sequence. The `padding_value=0` argument specifies the value to use for padding.

```python
sentences = [
    "If you want to know what a man's like, take a good look at how he treats his inferiors, not his equals.",
    "Fame's a fickle friend, Harry.",
    "It is our choices, Harry, that show what we truly are, far more than our abilities.",
    "Soon we must all face the choice between what is right and what is easy.",
    "Youth can not know how age thinks and feels. But old men are guilty if they forget what it was to be young.",
    "You are awesome!"
]

class CustomDataset(Dataset):
  def __init__(self,sentences,tokenizer,vocab):
    self.sentences = sentences
    self.tokenizer = tokenizer
    self.vocab = vocab

  def __len__(self):

    return len(self.sentences)

  def __getitem__(self, idx):
    tokens = self.tokenizer(self.sentences[idx])

    #Convert tokens to tensor indices using vocab
    tensor_indices = [self.vocab[token] for token in tokens]
    return torch.tensor(tensor_indices)
```

Here are the correct answers for your graded assignment:
### ✅ **Question 1**

**Which tokenization method generates a smaller vocabulary but increases input dimensionality and computational needs?**

**Answer:** `Character-based tokenization`

- ✔ Smaller vocabulary (characters instead of words or subwords)
- ❗ Increases sequence length → higher dimensionality and computational cost
---
### ✅ **Question 2**

**What concept addresses varied sequence lengths when using data loaders?**

**Answer:** `Padding`

- ✔ Ensures all sequences in a batch are the same length
- Commonly used with a `<pad>` token

---
### ✅ **Question 3**

**In subword-based tokenization, the ________ indicates that the word should be attached to the previous word without a space.**

**Answer:** `## symbol`

- ✔ In WordPiece (used in BERT), `##` indicates subword continuation

---
### ✅ **Question 4**

**Identify an advantage of word-based tokenization.**

**Answer:** `It preserves the semantic meaning`

- ✔ Full words retain clearer semantic meaning
- ❌ But large vocab size and OOV (Out-of-Vocabulary) issues
---
### ✅ **Question 5**

**Which input during data loader creation helps prevent the model from learning patterns based on data order?**

**Answer:** `The shuffle argument`

- ✔ Randomizes data order each epoch → avoids learning order-based biases

---

# Tokenization: Word-Based, Character-Based, and Subword-Based

## Overview

Tokenization is a fundamental step in NLP, enabling models to process text by converting it into manageable units. The choice of tokenization method impacts model performance, vocabulary size, and handling of out-of-vocabulary (OOV) words.

## Comparison of Tokenization Methods

|**Aspect**|**Word-Based**|**Character-Based**|**Subword-Based**|
|---|---|---|---|
|**Definition**|Splits text into individual words.|Splits text into individual characters.|Splits text into subword units (e.g., morphemes or frequent word fragments).|
|**Example**|"I love coding" → ["I", "love", "coding"]|"I love coding" → ["I", " ", "l", "o", "v", "e", " ", "c", "o", "d", "i", "n", "g"]|"I love coding" → ["I", "lov", "##e", "cod", "##ing"]|
|**Vocabulary Size**|Large (one token per unique word).|Small (one token per character).|Moderate (depends on algorithm).|
|**OOV Handling**|Struggles with unseen words (e.g., "coders").|No OOV issue; every word is broken into characters.|Good; can construct unseen words from subword units.|
|**Granularity**|Coarse (word-level).|Fine (character-level).|Balanced (subword-level).|
|**Context Preservation**|Good for common words; loses context for rare words.|Poor; individual characters lack meaning.|Better; captures meaningful word parts.|
|**Computational Cost**|Moderate; depends on vocabulary size.|High; long sequences increase computation.|Moderate; shorter sequences than character-based.|
|**Use Cases**|Simple NLP tasks, traditional models.|Spelling correction, low-resource languages.|Modern NLP models (e.g., BERT, GPT).|
|**Examples of Algorithms**|Whitespace splitting, rule-based tokenizers.|Simple character splitting.|WordPiece, BPE, SentencePiece.|

## Detailed Explanation

### Word-Based Tokenization

- **Process**: Text is split into words based on spaces, punctuation, or rules.
- **Pros**:
    - Intuitive and aligns with human understanding of language.
    - Smaller sequence lengths for models to process.
- **Cons**:
    - Large vocabulary size (every unique word is a token).
    - Poor handling of OOV words (e.g., typos, new words).
    - Language-specific rules needed for splitting.
- **Example in Practice**: Early NLP models like bag-of-words or TF-IDF.

### Character-Based Tokenization

- **Process**: Text is split into individual characters, including spaces and punctuation.
- **Pros**:
    - Small vocabulary (e.g., 26 letters for English, plus punctuation).
    - No OOV issues; any text can be tokenized.
    - Useful for languages with complex morphology or low resources.
- **Cons**:
    - Long sequences increase computational cost.
    - Characters lack semantic meaning, making it harder for models to learn context.
- **Example in Practice**: Text generation, spelling correction models.

### Subword-Based Tokenization

- **Process**: Text is split into subword units (e.g., morphemes, frequent word parts) using algorithms like Byte Pair Encoding (BPE) or WordPiece.
- **Pros**:
    - Balances vocabulary size and sequence length.
    - Handles OOV words by breaking them into known subword units.
    - Captures morphological patterns (e.g., "coding" → "cod" + "##ing").
- **Cons**:
    - Requires training a tokenizer model on a corpus.
    - May split words in unintuitive ways for humans.
- **Example in Practice**: Modern transformer models like BERT, GPT, and T5.

## When to Use Each Method

- **Word-Based**: Suitable for simple tasks or when vocabulary is limited and well-defined.
- **Character-Based**: Ideal for low-resource languages or tasks requiring fine-grained analysis (e.g., spelling correction).
- **Subword-Based**: Preferred for modern NLP models, especially for multilingual tasks or handling diverse vocabularies.