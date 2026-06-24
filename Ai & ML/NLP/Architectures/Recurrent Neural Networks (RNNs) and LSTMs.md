## Overview of RNNs

RNNs are designed for sequential data, leveraging a "memory" to capture context from previous inputs. This makes them ideal for tasks where order or context is crucial.

### Applications of RNNs

- **Next word prediction**: Predicting the next word in a sentence.
- **Music composition**: Generating sequences of musical notes.
- **Image captioning**: Generating descriptive captions for images.
- **Speech recognition**: Converting audio sequences to text.
- **Time series anomaly detection**: Identifying outliers in sequential data.
- **Stock market prediction**: Forecasting stock prices based on historical data.

## Text Preprocessing for RNNs

### Key Considerations

1. **Avoid Standard Preprocessing with Pre-trained Embeddings**
    
    - When using pre-trained embeddings (e.g., Word2Vec, GloVe), avoid stemming or stopword removal. These techniques are more suited for word count-based feature extraction (e.g., TF-IDF), as they can lead to loss of semantic information critical for embeddings.
    - Example: Stemming "running" to "run" or removing stopwords like "the" may disrupt the contextual meaning captured by embeddings.
2. **Align Vocabulary with Embeddings**
    
    - Ensure your vocabulary closely matches the pre-trained embeddings' vocabulary to maximize compatibility and performance. This may involve filtering out rare words or handling out-of-vocabulary (OOV) tokens.

### Tokenization with Keras Tokenizer

The `Tokenizer` in Keras processes text data as follows:

1. Builds a dictionary of unique words in the corpus, with words as keys and their frequency as values.
2. Sorts the dictionary by frequency in descending order.
3. Assigns indices starting from 1 (most frequent word gets index 1, second most frequent gets 2, etc.).
4. Converts text to sequences of these indices, where each word is represented by its index.
    - Example: If "the" is the most frequent word, it’s assigned index 1, and its one-hot vector would be `[1, 0, 0, ...]`.

![[Pasted image 20250204044255.png]]

**Example Code**:

```python
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample texts
texts = ["I love coding", "Coding is fun"]
max_len = 5  # Maximum sequence length

# Initialize and fit tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index
print(word_index)  # Example output: {'coding': 1, 'i': 2, 'love': 3, 'is': 4, 'fun': 5}

# Convert texts to sequences
sequences = tokenizer.texts_to_sequences(texts)
print(sequences)  # Example output: [[2, 3, 1], [1, 4, 5]]

# Pad sequences for uniform length
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
print(padded_sequences)  # Example output: [[2 3 1 0 0], [1 4 5 0 0]]
```

**Why Pad Sequences?**

- Ensures uniform input size for batch processing in neural networks.
- Adds padding (zeros) to shorter sequences to match the maximum sequence length (`max_len`).

## Embedding Layer

The `Embedding` layer transforms integer-encoded words into dense vectors (e.g., 300-dimensional vectors).

- **Input**: One-hot vectors or integer indices representing words.
- **Output**: Dense vectors learned during training, similar to pre-trained embeddings like Word2Vec.
- **Advantages**: The embedding layer adapts during training, enhancing the quality of word representations for the specific task.
- **Configuration**:
    - `input_dim`: Size of the vocabulary (`len(word_index) + 1` to account for zero padding).
    - `output_dim`: Dimension of the embedding vectors (e.g., 300).
    - `input_length`: Length of input sequences (`max_len`).

**Example**:

```python
from tensorflow.keras import layers
model = tf.keras.Sequential()
model.add(layers.Embedding(input_dim=len(word_index) + 1, output_dim=300, input_length=max_len))
```

## Understanding LSTM Inputs and Outputs

LSTMs (Long Short-Term Memory) are a type of RNN that handle long-term dependencies better than simple RNNs by using gates (input, forget, output).

### Input Shape

- LSTMs expect a **3D array**: `(batch_size, timesteps, features)`.
    - `batch_size`: Number of sequences in a batch (can be unspecified for flexibility).
    - `timesteps`: Number of time steps in each sequence (e.g., words in a sentence).
    - `features`: Number of features per time step (e.g., 1 for integer-encoded words, or embedding dimension after an `Embedding` layer).

**Example 1: Flexible Batch Size**

```python
model = tf.keras.Sequential()
model.add(layers.LSTM(units=3, input_shape=(2, 10)))
```

- **Timesteps**: 2
- **Features**: 10
- **Units**: 3 (number of LSTM cells)
- **Batch Size**: Unspecified (model accepts variable batch sizes)
- **Output Shape**: `(None, 3)` (2D array: batch_size × units)

**Example 2: Fixed Batch Size**

```python
model = tf.keras.Sequential()
model.add(layers.LSTM(units=3, batch_input_shape=(8, 2, 10)))
```

- **Batch Size**: 8 (fixed)
- **Timesteps**: 2
- **Features**: 10
- **Output Shape**: `(8, 3)` (2D array: batch_size × units)

### Effect of `return_sequences`

- **return_sequences=False** (default):
    - Outputs only the final hidden state for each sequence.
    - Shape: `(batch_size, units)` (2D array).
- **return_sequences=True**:
    - Outputs the hidden state at each time step.
    - Shape: `(batch_size, timesteps, units)` (3D array).

**Example with `return_sequences=True`**:

```python
model = tf.keras.Sequential()
model.add(layers.LSTM(units=3, batch_input_shape=(8, 2, 10), return_sequences=True))
```

- **Output Shape**: `(8, 2, 3)` (3D array: batch_size × timesteps × units)

### Summary of LSTM Shapes

- **Input**: Always a 3D array `(batch_size, timesteps, features)`.
- **Output**:
    - If `return_sequences=False`: 2D array `(batch_size, units)`.
    - If `return_sequences=True`: 3D array `(batch_size, timesteps, units)`.

## Example RNN Model for Text Classification

Below is a complete example combining tokenization, padding, embedding, and LSTM layers for a binary text classification task.

```python
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np

# Set random seed
tf.random.set_seed(42)
np.random.seed(42)

# Synthetic text data
texts = ["I love coding", "Coding is fun", "I hate bugs", "Bugs are bad"] * 250
labels = [1, 1, 0, 0] * 250  # Positive (1) or negative (0) sentiment

# Tokenization
max_len = 5
vocab_size = 1000
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
word_index = tokenizer.word_index

# Split data
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# Build model
model = tf.keras.Sequential([
    layers.Embedding(input_dim=len(word_index) + 1, output_dim=300, input_length=max_len),
    layers.LSTM(units=128),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

# Train model
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")
```

## Notes

- **Optimizer**: Adam is used for its adaptive learning rate, suitable for most NLP tasks.
- **Metrics**: Accuracy is used for binary classification. For multi-class, use `categorical_accuracy` with a softmax output.
- **Padding**: Ensures all sequences have the same length (`max_len`) for efficient batch processing.
- **Pre-trained Embeddings**: If using pre-trained embeddings (e.g., GloVe), load them into the `Embedding` layer and set `trainable=False` to preserve the pre-trained weights.