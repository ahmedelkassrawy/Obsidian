# NLP RNN

This document outlines the process of building a Recurrent Neural Network (RNN) for Part-of-Speech (PoS) tagging using TensorFlow and NLTK corpora.

## Setup and Imports

```python
import nltk
import numpy as np
import requests
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from nltk.corpus import treebank, brown, conll2000
from sklearn.model_selection import train_test_split
```

## Downloading NLTK Corpora

Download necessary NLTK datasets for PoS tagging:

```python
nltk.download('treebank')
nltk.download('brown')
nltk.download('conll2000')
nltk.download('universal_tagset')
```

## Data Preparation

Combine PoS-tagged sentences from multiple corpora:

```python
tagged_sentences = treebank.tagged_sents(tagset='universal') +\
                   brown.tagged_sents(tagset='universal') +\
                   conll2000.tagged_sents(tagset='universal')
```

Display the first sentence and dataset size:

```python
print(tagged_sentences[0])
print(f"Dataset size: {len(tagged_sentences)}")
```

Split sentences into words and tags:

```python
sentences, sentence_tags = [], []
for s in tagged_sentences:
    sentence, tags = zip(*s)
    sentences.append(list(sentence))
    sentence_tags.append(list(tags))
```

Display the first sentence and its tags:

```python
print(sentences[0])
print(sentence_tags[0])
print(len(sentences), len(sentence_tags))
```

## Train-Test-Validation Split

Define split ratios:

```python
train_ratio = 0.75
validation_ratio = 0.15
test_ratio = 0.10
```

Perform train-test split:

```python
x_train, x_test, y_train, y_test = train_test_split(sentences, sentence_tags,
                                                    test_size=1 - train_ratio,
                                                    random_state=1)
```

Perform validation-test split:

```python
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                test_size=test_ratio/(test_ratio + validation_ratio),
                                                random_state=1)
```

Display split sizes:

```python
print(len(x_train), len(y_train))
print(len(x_val), len(y_val))
print(len(x_test), len(y_test))
```

## Tokenization

Create and fit tokenizer for words:

```python
tokenizer = keras.preprocessing.text.Tokenizer(oov_token='<OOV>')
tokenizer.fit_on_texts(x_train)
print(f"Vocabulary size: {len(tokenizer.word_index)}")
```

Create and fit tokenizer for tags:

```python
tag_tokenizer = keras.preprocessing.text.Tokenizer()
tag_tokenizer.fit_on_texts(y_train)
print(f"Number of POS tags: {len(tag_tokenizer.word_index)}")
```

Convert text to sequences:

```python
x_train_seqs = tokenizer.texts_to_sequences(x_train)
print(f"Original: {x_train[0]}")
print(f"Reconstructed: {tokenizer.sequences_to_texts([x_train_seqs[0]])}")
y_train_seqs = tag_tokenizer.texts_to_sequences(y_train)
x_val_seqs = tokenizer.texts_to_sequences(x_val)
y_val_seqs = tag_tokenizer.texts_to_sequences(y_val)
```

## Padding Sequences

Determine maximum sequence length:

```python
max_len = max([len(seq) for seq in x_train_seqs])
print(f"Length of longest input: {max_len}")
MAX_LENGTH = len(max(x_train_seqs, key=len))
print(f"Length of longest input sequence: {MAX_LENGTH}")
```

Pad sequences:

```python
x_train_padded = keras.preprocessing.sequence.pad_sequences(x_train_seqs,
                                                            padding='post',
                                                            maxlen=MAX_LENGTH)
y_train_padded = keras.preprocessing.sequence.pad_sequences(y_train_seqs,
                                                            padding='post',
                                                            maxlen=MAX_LENGTH)
x_val_padded = keras.preprocessing.sequence.pad_sequences(x_val_seqs, padding='post', maxlen=MAX_LENGTH)
y_val_padded = keras.preprocessing.sequence.pad_sequences(y_val_seqs, padding='post', maxlen=MAX_LENGTH)
```

## One-Hot Encoding

Convert tags to one-hot encodings:

```python
y_train_categoricals = keras.utils.to_categorical(y_train_padded)
print(y_train_categoricals[0][0])
y_val_categoricals = keras.utils.to_categorical(y_val_padded)
```

## Model Definition

Define model parameters:

```python
num_tokens = len(tokenizer.word_index) + 1
embedding_dim = 128
num_classes = len(tag_tokenizer.word_index) + 1
```

Build the model:

```python
tf.random.set_seed(0)
model = keras.Sequential()
model.add(layers.Embedding(input_dim=num_tokens,
                           output_dim=embedding_dim,
                           input_length=max_len,
                           mask_zero=True))
model.add(layers.Bidirectional(
    layers.LSTM(embedding_dim,
                return_sequences=True,
                kernel_initializer=tf.keras.initializers.random_normal(seed=1))))
model.add(layers.Dense(num_classes,
                       activation='softmax',
                       kernel_initializer=tf.keras.initializers.random_normal(seed=1)))
```

Compile the model:

```python
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.summary()
```

## Training

Set up early stopping:

```python
es_callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
```

Train the model:

```python
history = model.fit(x_train_padded,
                    y_train_categoricals,
                    epochs=20,
                    batch_size=256,
                    validation_data=(x_val_padded, y_val_categoricals),
                    callbacks=[es_callback])
```

## Evaluation

Preprocess test data and evaluate:

```python
x_test_seqs = tokenizer.texts_to_sequences(x_test)
x_test_padded = keras.preprocessing.sequence.pad_sequences(x_test_seqs, padding='post', maxlen=MAX_LENGTH)
y_test_seqs = tag_tokenizer.texts_to_sequences(y_test)
y_test_padded = keras.preprocessing.sequence.pad_sequences(y_test_seqs, padding='post', maxlen=MAX_LENGTH)
y_test_categoricals = keras.utils.to_categorical(y_test_padded)
model.evaluate(x_test_padded, y_test_categoricals)
```

## Inference

Define a function to tag sentences:

```python
def tag_sentences(sentences):
    sentences_seqs = tokenizer.texts_to_sequences(sentences)
    sentences_padded = keras.preprocessing.sequence.pad_sequences(sentences_seqs,
                                                                maxlen=MAX_LENGTH,
                                                                padding='post')
    tag_preds = model.predict(sentences_padded)
    sentence_tags = []
    for i, preds in enumerate(tag_preds):
        tags_seq = [np.argmax(p) for p in preds[:len(sentences_seqs[i])]]
        words = [tokenizer.index_word[w] for w in sentences_seqs[i]]
        tags = [tag_tokenizer.index_word[t] for t in tags_seq]
        sentence_tags.append(list(zip(words, tags)))
    return sentence_tags
```

Test the model with sample sentences:

```python
samples = [
    "Brown refused to testify.",
    "Brown sofas are on sale.",
]
tagged_sample_sentences = tag_sentences(samples)
print(tagged_sample_sentences[0])
print(tagged_sample_sentences[1])
```

Additional test sentences:

```python
sentences = ["I am Ahmed"]
example = tag_sentences(sentences)
print(example)

sentences = ["Can you help me?"]
example = tag_sentences(sentences)
print(example)

sentences = ["Sentences are a lot of word connected together"]
example = tag_sentences(sentences)
print(example)
```

# NLP RNN Pipeline for PoS Tagging

This document outlines the pipeline for training a Recurrent Neural Network (RNN) for Part-of-Speech (PoS) tagging.

## Data Preparation

- Combine PoS-tagged sentences from `treebank`, `brown`, and `conll2000` corpora with the `universal` tagset.
- Split sentences into words and corresponding PoS tags, storing them in separate lists (`sentences` and `sentence_tags`).

## Train-Test-Validation Split

- Define split ratios: 75% training, 15% validation, 10% test.
- Use `train_test_split` to create training and test sets, then further split the test set into validation and test sets.

## Tokenization

- Create a word tokenizer (`keras.preprocessing.text.Tokenizer`) with an out-of-vocabulary (`<OOV>`) token and fit it on the training sentences.
- Create a tag tokenizer and fit it on the training tags.
- Convert training, validation, and test sentences and tags to sequences of indices using the tokenizers.

## Padding Sequences

- Determine the maximum sequence length (`MAX_LENGTH`) from the training sequences.
- Pad all sequences (words and tags) to `MAX_LENGTH` using `keras.preprocessing.sequence.pad_sequences` with `padding='post'`.

## One-Hot Encoding

- Convert padded tag sequences for training and validation sets to one-hot encodings using `keras.utils.to_categorical`.

## Model Definition

- Define model parameters:
    - `num_tokens`: Vocabulary size + 1 (for padding token).
    - `embedding_dim`: 128 (size of word embeddings).
    - `num_classes`: Number of PoS tags + 1.
- Build a sequential model:
    - `Embedding` layer: Input dimension = `num_tokens`, output dimension = `embedding_dim`, input length = `max_len`, `mask_zero=True`.
    - `Bidirectional LSTM` layer: Units = `embedding_dim`, `return_sequences=True`.
    - `Dense` layer: Units = `num_classes`, activation = `softmax`.
- Compile the model with `categorical_crossentropy` loss, `adam` optimizer, and `accuracy` metric.

## Training

- Set up early stopping with `monitor='val_loss'` and `patience=3`.
- Train the model using `model.fit` with padded training data, one-hot encoded tags, 20 epochs, batch size of 256, validation data, and the early stopping callback.

## Evaluation

- Preprocess test data: Convert to sequences, pad, and one-hot encode tags.
- Evaluate the model on the test set using `model.evaluate`.

## Inference

- Define a `tag_sentences` function to:
    - Convert input sentences to sequences and pad them.
    - Predict tag probabilities using the trained model.
    - Extract the most probable tag for each word (excluding padding).
    - Convert sequences back to words and tags using the tokenizers.
    - Return a list of (word, tag) tuples for each sentence.
- Test the function with sample sentences.

```text
Corpus (treebank/brown/conll2000)
   ↓
Token-tag pairs → sentences & sentence_tags
   ↓
Split into train/val/test
   ↓
Tokenization → integer sequences
   ↓
Padding → fixed length arrays
   ↓
One-hot encode tags → categorical 3D arrays
   ↓
Model training
   ↓
Evaluation
   ↓
Inference (POS tag prediction)
```