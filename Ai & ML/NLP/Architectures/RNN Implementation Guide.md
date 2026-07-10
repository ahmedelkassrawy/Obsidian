## Understanding the Task and Dataset
Your code is for a **binary text classification task** (positive vs. negative sentiment) using synthetic text data. The dataset consists of short sentences (e.g., "I love coding") with binary labels (1 for positive, 0 for negative). The model uses an `Embedding` layer, an `LSTM` layer, and a `Dense` layer for classification.

**Key Considerations for Model Design**:
- **Task**: Binary classification of short text sequences.
- **Data**: Small synthetic dataset (1000 samples, 4 unique sentences repeated 250 times).
- **Sequence Length**: Short sentences (up to 5 words, as set by `max_len=5`).
- **Vocabulary**: Small vocabulary due to synthetic data (e.g., "I", "love", "coding", "is", "fun", "hate", "bugs", "are", "bad").

The choices for layers and parameters depend on the task complexity, dataset size, sequence length, and computational resources.

---

## Breaking Down Model Specifications and Parameters

### 1. Preprocessing Parameters
#### a. `vocab_size` (Tokenizer: `num_words=1000`)
- **What it is**: The maximum number of unique words to include in the tokenizer’s vocabulary. The `Tokenizer` assigns indices to the most frequent `vocab_size` words in the corpus.
- **Your choice**: `vocab_size=1000`.
- **How to choose**:
  - **Dataset size and diversity**: Check the number of unique words in your corpus using `len(tokenizer.word_index)`. For your synthetic data, the vocabulary is very small (likely <10 unique words), so `vocab_size=1000` is overkill. A smaller value (e.g., `len(word_index) + 1`) is sufficient.
  - **Pre-trained embeddings**: If using pre-trained embeddings (e.g., GloVe, Word2Vec), set `vocab_size` to match the embedding’s vocabulary or filter your corpus to include only words present in the embedding.
  - **Out-of-vocabulary (OOV) handling**: Words beyond `vocab_size` are ignored or mapped to an OOV token. For small datasets, a large `vocab_size` is unnecessary but harmless.
- **Recommendation**: Set `vocab_size=len(word_index) + 1` (e.g., ~10 for your data) to include all unique words. For real datasets, analyze the word frequency distribution (e.g., using `tokenizer.word_counts`) and set `vocab_size` to cover 95-99% of the corpus (e.g., 10,000-20,000 for larger datasets).
- **Impact**: A smaller `vocab_size` reduces the `Embedding` layer’s memory footprint but may exclude rare words. A larger `vocab_size` increases memory usage without benefit if the vocabulary is small.

#### b. `max_len` (Padding: `maxlen=5`)
- **What it is**: The maximum length of input sequences after padding. Shorter sequences are padded with zeros, and longer ones are truncated.
- **Your choice**: `max_len=5`.
- **How to choose**:
  - **Sequence length distribution**: Compute the length of each sequence in `sequences` (e.g., `[len(seq) for seq in sequences]`) and choose `max_len` to cover most sequences without excessive padding. For your data, sentences are 3-4 words, so `max_len=5` is reasonable.
  - **Task requirements**: For short texts (e.g., tweets, reviews), `max_len` is typically 20-100. For longer texts (e.g., articles), it might be 200-500.
  - **Memory and performance**: Larger `max_len` increases memory usage and computation time in the LSTM. Smaller `max_len` may truncate important information.
- **Recommendation**: For your synthetic data, `max_len=5` is fine. For real datasets, use a percentile (e.g., 95th) of sequence lengths to avoid excessive padding (e.g., `np.percentile([len(seq) for seq in sequences], 95)`).
- **Impact**: Too small a `max_len` truncates sequences, losing context. Too large a `max_len` adds unnecessary padding, slowing training.
```python
max_len = max([len(seq) for seq in x_train_seqs])
print(f"Length of longest input:{max_len}")
```

#### c. Padding (`padding='post'`)
- **What it is**: Determines whether zeros are added at the start (`pre`) or end (`post`) of sequences to reach `max_len`.
- **Your choice**: `padding='post'`.
- **How to choose**:
  - **Context**: LSTMs process sequences sequentially, so `pre` padding (zeros at the start) may dilute early context, while `post` padding preserves early words’ impact. For short sequences, the difference is minimal.
  - **Task**: `post` padding is common in NLP, as early words often carry more meaning (e.g., sentiment in reviews).
- **Recommendation**: Stick with `padding='post'` for your task, as it’s standard and works well for short sequences.
- **Impact**: Minimal for short sequences, but `pre` padding may slightly affect LSTM’s memory of early tokens in longer sequences.

### 2. Embedding Layer
#### a. `input_dim` (`len(word_index) + 1`)
- **What it is**: The size of the vocabulary for the `Embedding` layer, including all unique words plus a padding token (index 0).
- **Your choice**: `len(word_index) + 1`.
- **How to choose**:
  - **Vocabulary size**: Set to `len(word_index) + 1` to account for all unique words in the tokenizer’s dictionary plus the padding token.
  - **Pre-trained embeddings**: If using pre-trained embeddings, ensure `input_dim` covers all words in your corpus that appear in the embedding’s vocabulary.
- **Recommendation**: Your choice is correct, as it dynamically adjusts to the actual vocabulary size. For pre-trained embeddings, you may need to filter `word_index` to match the embedding’s vocabulary.
- **Impact**: Must be at least `len(word_index) + 1` to avoid index errors. Larger values are harmless but increase memory usage.

#### b. `output_dim` (Embedding dimension: 300)
- **What it is**: The dimensionality of the dense vectors produced by the `Embedding` layer for each word.
- **Your choice**: `output_dim=300`.
- **How to choose**:
  - **Task complexity**: Higher dimensions (e.g., 100-300) capture more semantic information but increase model complexity and memory usage. Lower dimensions (e.g., 50-100) are faster but may lose nuance.
  - **Pre-trained embeddings**: Common pre-trained embeddings (e.g., GloVe, Word2Vec) use 50, 100, 200, or 300 dimensions. Match `output_dim` to the pre-trained embedding if used.
  - **Dataset size**: Smaller datasets (like yours) may not benefit from large `output_dim` due to limited training data. Larger datasets can support higher dimensions.
- **Recommendation**: For your small synthetic dataset, `output_dim=100` or `50` may suffice to reduce overfitting. For real-world NLP tasks, `300` is a good default, especially with pre-trained embeddings like GloVe.
- **Impact**: Larger `output_dim` increases model capacity but risks overfitting on small datasets and increases computation. Smaller `output_dim` may underfit complex tasks.

#### c. `input_length` (`max_len`)
- **What it is**: The fixed length of input sequences, matching the padded sequence length.
- **Your choice**: `input_length=max_len` (5).
- **How to choose**: Must equal `max_len` from `pad_sequences` to ensure compatibility with the input sequences.
- **Recommendation**: Your choice is correct. Always set `input_length=max_len` to match the preprocessing step.
- **Impact**: Mismatch causes shape errors during training.

### 3. LSTM Layer
#### a. `units` (LSTM units: 128)
- **What it is**: The number of LSTM cells, determining the hidden state’s dimensionality and the model’s capacity to capture sequential patterns.
- **Your choice**: `units=128`.
- **How to choose**:
  - **Task complexity**: More units increase the model’s ability to learn complex patterns but also increase parameters and overfitting risk. For simple tasks (like your binary classification), 32-128 units are often sufficient. Complex tasks (e.g., machine translation) may need 256-512 units.
  - **Dataset size**: Small datasets (like yours, 1000 samples) can overfit with too many units. Larger datasets support more units.
  - **Sequence length**: Longer sequences may benefit from more units to capture dependencies, but your sequences are short (`max_len=5`).
- **Recommendation**: For your small dataset, try `units=64` or `32` to reduce overfitting. For larger datasets, `128` or `256` is common.
- **Impact**: More units increase computation and memory usage. Too few units may underfit, missing important patterns.

#### b. `return_sequences` (Default: False)
- **What it is**: Determines whether the LSTM outputs the hidden state at each time step (3D output: `(batch_size, max_len, units)`) or only the final hidden state (2D output: `(batch_size, units)`).
- **Your choice**: `return_sequences=False` (implicit, as not specified).
- **How to choose**:
  - **Task**: For classification (like yours), `return_sequences=False` is typical, as you only need the final output for the `Dense` layer. For sequence-to-sequence tasks (e.g., translation), set `return_sequences=True` to pass the full sequence to the next layer.
  - **Model architecture**: If stacking multiple LSTMs, set `return_sequences=True` for all but the final LSTM layer to preserve the sequence dimension.
- **Recommendation**: Keep `return_sequences=False` for your binary classification task. If you add another LSTM layer, set `return_sequences=True` for the first LSTM.
- **Impact**: Incorrect setting causes shape mismatches with the next layer.

### 4. Dense Layer
#### a. Units and Activation (`units=1`, `activation='sigmoid'`)
- **What it is**: The output layer producing the final prediction. For binary classification, it outputs a single probability (0 to 1).
- **Your choice**: `Dense(1, activation='sigmoid')`.
- **How to choose**:
  - **Task**: For binary classification, use 1 unit with `sigmoid` activation. For multi-class classification (e.g., 10 classes), use `n_classes` units with `softmax` activation.
  - **Output format**: Ensure the labels match the activation (e.g., binary labels [0, 1] for `sigmoid`, one-hot encoded for `softmax`).
- **Recommendation**: Your choice is correct for binary classification. For multi-class, change to `Dense(n_classes, activation='softmax')` and use `categorical_crossentropy` loss.
- **Impact**: Mismatch between units/activation and task causes incorrect predictions or training errors.

### 5. Compilation Parameters
#### a. Optimizer (`adam`)
- **What it is**: The algorithm to update model weights during training.
- **Your choice**: `optimizer='adam'`.
- **How to choose**:
  - **Adam**: A robust default for most tasks due to its adaptive learning rate. Good for NLP and small datasets.
  - **Alternatives**: SGD (with momentum) for fine-tuning, RMSprop for RNNs with noisy gradients.
  - **Learning rate**: Default for Adam (`0.001`) works well. For small datasets, try smaller rates (e.g., `0.0001`) to prevent overfitting.
- **Recommendation**: Stick with Adam for your task. If training is unstable, try `tf.keras.optimizers.Adam(learning_rate=0.0001)`.
- **Impact**: Adam is forgiving, but tuning the learning rate can improve convergence.

#### b. Loss (`binary_crossentropy`)
- **What it is**: The objective function to minimize during training.
- **Your choice**: `loss='binary_crossentropy'`.
- **How to choose**:
  - **Binary classification**: Use `binary_crossentropy` for binary labels with `sigmoid` activation.
  - **Multi-class**: Use `categorical_crossentropy` for one-hot encoded labels with `softmax`, or `sparse_categorical_crossentropy` for integer labels.
- **Recommendation**: Your choice is correct for binary classification. Ensure labels are in `[0, 1]` format (your code converts `y_train` and `y_test` to NumPy arrays, which is good).
- **Impact**: Incorrect loss function leads to poor training or errors.

#### c. Metrics (`accuracy`)
- **What it is**: Metrics to evaluate model performance during training and testing.
- **Your choice**: `metrics=['accuracy']`.
- **How to choose**:
  - **Binary classification**: `accuracy` is suitable. For imbalanced datasets, consider `['accuracy', 'precision', 'recall']`.
  - **Multi-class**: Use `categorical_accuracy` for one-hot labels or `sparse_categorical_accuracy` for integer labels.
- **Recommendation**: Your choice is appropriate. For real-world tasks, add `precision` and `recall` if the dataset is imbalanced.
- **Impact**: Metrics don’t affect training but help monitor performance.

### 6. Training Parameters
#### a. `epochs` (5)
- **What it is**: Number of passes through the training data.
- **Your choice**: `epochs=5`.
- **How to choose**:
  - **Dataset size**: Small datasets (like yours) may need fewer epochs (3-10) to avoid overfitting. Larger datasets may need 10-50 epochs.
  - **Early stopping**: Use `tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)` to stop training when validation performance plateaus.
- **Recommendation**: For your small dataset, `epochs=5` is reasonable. Add early stopping to prevent overfitting:
  ```python
  early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
  model.fit(..., callbacks=[early_stopping])
  ```
- **Impact**: Too many epochs cause overfitting; too few cause underfitting.

#### b. `batch_size` (32)
- **What it is**: Number of samples processed before updating weights.
- **Your choice**: `batch_size=32`.
- **How to choose**:
  - **Trade-off**: Smaller batches (e.g., 16-32) provide noisy gradients but better generalization. Larger batches (e.g., 64-128) are faster but may converge to suboptimal solutions.
  - **Memory**: Larger batches require more GPU/CPU memory. For small datasets, smaller batches are fine.
- **Recommendation**: `batch_size=32` is a good default. For larger datasets, try `64` or `128` if memory allows.
- **Impact**: Affects training speed and stability. Smaller batches may improve performance on small datasets.

#### c. `validation_data` (`(X_test, y_test)`)
- **What it is**: Data to evaluate the model after each epoch.
- **Your choice**: `validation_data=(X_test, y_test)`.
- **How to choose**: Use a separate validation set (e.g., 20% of data, as in your code). Alternatively, use `validation_split=0.2` in `model.fit` to automatically split training data.
- **Recommendation**: Your choice is good. Ensure the test set isn’t used for hyperparameter tuning to avoid data leakage.
- **Impact**: Validation data helps monitor overfitting and tune hyperparameters.

---

## General Guidelines for Choosing Layers and Architecture
### Why These Layers?
- **Embedding**: Converts integer-encoded words into dense vectors, capturing semantic relationships. Essential for NLP tasks.
- **LSTM**: Captures sequential dependencies in text, suitable for your short sequences. Alternatives (e.g., GRU) are lighter but may perform similarly.
- **Dense**: Produces the final classification output. Simple and effective for your task.

### When to Add More Layers?
- **Stacking LSTMs**: For complex tasks (e.g., longer sequences, translation), add another LSTM with `return_sequences=True`:
  ```python
  model.add(layers.LSTM(128, return_sequences=True))
  model.add(layers.LSTM(64))
  ```
- **Dropout**: Add `Dropout` layers to prevent overfitting, especially for small datasets:
  ```python
  model.add(layers.Dropout(0.2))  # After LSTM
  ```
- **Bidirectional LSTM**: For tasks where future context matters (e.g., named entity recognition), use:
  ```python
  model.add(layers.Bidirectional(layers.LSTM(128)))
  ```
- **Dense Layers**: For complex tasks, add hidden `Dense` layers before the output layer:
  ```python
  model.add(layers.Dense(64, activation='relu'))
  model.add(layers.Dropout(0.2))
  ```

### Tuning Parameters
- **Hyperparameter tuning**: Use grid search or random search (e.g., with `keras-tuner`) to test combinations of `lstm_units`, `embedding_dim`, `batch_size`, etc.
- **Cross-validation**: For small datasets, use k-fold cross-validation to assess model stability.
- **Learning rate scheduling**: Use `tf.keras.callbacks.ReduceLROnPlateau` to reduce the learning rate when validation loss plateaus.

---

## Specific Recommendations for Your Model
Your model is well-suited for the synthetic dataset, but here are tailored suggestions:
1. **Reduce `vocab_size`**: Set `vocab_size=len(word_index) + 1` (~10) to match the actual vocabulary.
2. **Lower `embedding_dim`**: Try `output_dim=50` or `100` to reduce overfitting on your small dataset.
3. **Lower `lstm_units`**: Try `units=64` or `32` to simplify the model.
4. **Add Dropout**: Add `layers.Dropout(0.2)` after the LSTM to prevent overfitting.
5. **Early Stopping**: Add `EarlyStopping` to stop training if validation loss doesn’t improve.

**Updated Model Code**:
```python
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras import layers

# Set random seed
tf.random.set_seed(42)
np.random.seed(42)

# Synthetic text data
texts = ["I love coding", "Coding is fun", "I hate bugs", "Bugs are bad"] * 250
labels = [1, 1, 0, 0] * 250

# Tokenization
max_len = 5
tokenizer = Tokenizer()  # Remove vocab_size limit
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
word_index = tokenizer.word_index
vocab_size = len(word_index) + 1

# Split data
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
y_train = np.array(y_train)
y_test = np.array(y_test)

# Build model
model = tf.keras.Sequential([
    layers.Embedding(input_dim=vocab_size, output_dim=100, input_length=max_len),
    layers.LSTM(units=64),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
              loss='binary_crossentropy', 
              metrics=['accuracy'])

# Model summary
model.summary()

# Early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, 
          validation_data=(X_test, y_test), 
          callbacks=[early_stopping], verbose=1)

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")
```

---

## Obsidian Markdown Artifact
Here’s an updated markdown file summarizing the guidance for choosing model specifications and parameters, tailored to your code.


# RNN Model Specifications for Text Classification

## Task Overview
- **Task**: Binary text classification (positive vs. negative sentiment).
- **Dataset**: Synthetic data with 1000 samples (4 unique sentences repeated 250 times).
- **Model**: `Embedding` → `LSTM` → `Dense` with `sigmoid` for binary classification.

## Preprocessing Parameters
### 1. `vocab_size` (Tokenizer)
- **Purpose**: Maximum number of unique words in the vocabulary.
- **Choice**: Set to `len(word_index) + 1` to include all unique words plus padding token.
- **Considerations**:
  - For small datasets, use the actual vocabulary size (e.g., ~10 for synthetic data).
  - For pre-trained embeddings, align with embedding vocabulary.
- **Impact**: Too large increases memory; too small excludes words.

### 2. `max_len` (Padding)
- **Purpose**: Fixed length of input sequences after padding/truncation.
- **Choice**: `max_len=5` (matches short sentences in dataset).
- **Considerations**:
  - Set to cover 95% of sequence lengths (e.g., `np.percentile([len(seq) for seq in sequences], 95)`).
  - Larger `max_len` increases computation; smaller `max_len` truncates data.
- **Impact**: Affects memory usage and information retention.

### 3. `padding` (`post`)
- **Purpose**: Adds zeros at the start (`pre`) or end (`post`) of sequences.
- **Choice**: `padding='post'` (standard for NLP).
- **Considerations**: `post` preserves early context; minimal impact for short sequences.
- **Impact**: Slight effect on LSTM’s focus for longer sequences.

## Embedding Layer
- **Purpose**: Converts word indices to dense vectors.
- **Parameters**:
  - `input_dim=len(word_index) + 1`: Matches vocabulary size.
  - `output_dim=100`: Embedding vector size (reduced from 300 to avoid overfitting).
  - `input_length=max_len`: Matches padded sequence length.
- **Considerations**:
  - Smaller `output_dim` (50-100) for small datasets; 300 for larger datasets or pre-trained embeddings.
  - Use pre-trained embeddings (e.g., GloVe) for better initialization.
- **Impact**: Larger `output_dim` increases capacity but risks overfitting.

## LSTM Layer
- **Purpose**: Captures sequential dependencies in text.
- **Parameters**:
  - `units=64`: Number of LSTM cells (reduced from 128 for small dataset).
  - `return_sequences=False`: Outputs final hidden state for classification.
- **Considerations**:
  - Use 32-64 units for simple tasks; 128-256 for complex tasks.
  - Set `return_sequences=True` for stacked LSTMs or sequence-to-sequence tasks.
- **Impact**: More units increase capacity but risk overfitting; too few may underfit.

## Dense Layer
- **Purpose**: Produces classification output.
- **Parameters**:
  - `units=1`, `activation='sigmoid'`: For binary classification.
- **Considerations**: Use `n_classes` and `softmax` for multi-class tasks.
- **Impact**: Must match task and label format.

## Compilation Parameters
- **Optimizer**: `Adam` (learning_rate=0.0001 for stability).
- **Loss**: `binary_crossentropy` for binary classification.
- **Metrics**: `accuracy` (add `precision`, `recall` for imbalanced data).
- **Considerations**: Tune learning rate for small datasets; use `categorical_crossentropy` for multi-class.

## Training Parameters
- **Epochs**: 10 with `EarlyStopping(patience=3)` to prevent overfitting.
- **Batch Size**: 32 (good balance for small datasets).
- **Validation Data**: 20% test split to monitor performance.
- **Considerations**: Use early stopping and learning rate scheduling for better convergence.

## Example Code
```python
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras import layers

# Set random seed
tf.random.set_seed(42)
np.random.seed(42)

# Synthetic text data
texts = ["I love coding", "Coding is fun", "I hate bugs", "Bugs are bad"] * 250
labels = [1, 1, 0, 0] * 250

# Tokenization
max_len = 5
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
word_index = tokenizer.word_index
vocab_size = len(word_index) + 1

# Split data
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
y_train = np.array(y_train)
y_test = np.array(y_test)

# Build model
model = tf.keras.Sequential([
    layers.Embedding(input_dim=vocab_size, output_dim=100, input_length=max_len),
    layers.LSTM(units=64),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
              loss='binary_crossentropy', 
              metrics=['accuracy'])

# Model summary
model.summary()

# Early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, 
          validation_data=(X_test, y_test), 
          callbacks=[early_stopping], verbose=1)

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")
```

## Tips for Real Datasets
- **Analyze data**: Compute vocabulary size and sequence length distribution.
- **Pre-trained embeddings**: Use GloVe/Word2Vec for better initialization.
- **Regularization**: Add `Dropout` and reduce `units`/`output_dim` for small datasets.
- **Hyperparameter tuning**: Use `keras-tuner` or grid search for optimal parameters.
- **Cross-validation**: Use k-fold CV for small datasets to assess stability.



---

## Final Notes
- **Your Model**: Well-suited for the synthetic dataset but slightly overparameterized (`embedding_dim=300`, `lstm_units=128`). The updated code reduces these to prevent overfitting and adds `Dropout` and `EarlyStopping`.
- **Real Datasets**: For larger or real-world datasets, analyze the data to set `vocab_size`, `max_len`, and layer sizes. Consider pre-trained embeddings for better performance.
- **Tuning**: Experiment with `embedding_dim` (50-300), `lstm_units` (32-256), and `batch_size` (16-128) using validation performance as a guide.
- **Further Questions**: If you have a specific dataset or task (e.g., multi-class, longer texts), provide details, and I can tailor the recommendations further.

Let me know if you want to adjust the model for a specific dataset, add pre-trained embeddings, or explore other architectures!

```python
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras import layers

# Set random seed
tf.random.set_seed(42)
np.random.seed(42)

# Synthetic text data
texts = ["I love coding", "Coding is fun", "I hate bugs", "Bugs are bad"] * 250
labels = [1, 1, 0, 0] * 250

# Tokenization
max_len = 5
tokenizer = Tokenizer()  # Remove vocab_size limit
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
word_index = tokenizer.word_index
vocab_size = len(word_index) + 1

# Split data
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
y_train = np.array(y_train)
y_test = np.array(y_test)

# Build model
model = tf.keras.Sequential([
    layers.Embedding(input_dim=vocab_size, output_dim=100, input_length=max_len),
    layers.LSTM(units=64),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
              loss='binary_crossentropy', 
              metrics=['accuracy'])

# Model summary
model.summary()

# Early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, 
          validation_data=(X_test, y_test), 
          callbacks=[early_stopping], verbose=1)

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")
```