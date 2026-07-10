# Text Preprocessing and Neural Networks for NLP

## Tokenizer and Sequence Conversion

The `Tokenizer` from TensorFlow Keras converts text into numerical sequences for neural network input.

### Basic Usage

```python
from tensorflow.keras.preprocessing.text import Tokenizer 

lines = [ 
    'The quick brown fox', 
    'Jumps over $$$ the lazy brown dog',
    'Who jumps high into the blue sky after counting 123', 
    'And quickly returns to earth' 
] 

tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines)
```

**Key Points:**
- `fit_on_texts()` builds vocabulary dictionary from input text
- `texts_to_sequences()` converts text to arrays of word indices
- **Converts text to lowercase and removes most symbols**
- **Does NOT remove stop words or numbers by default**

**Output example:**
```text
[[1, 4, 2, 5],
 [3, 6, 1, 7, 2, 8],
 [9, 3, 10, 11, 1, 12, 13, 14, 15, 16],
 [17, 18, 19, 20, 21]]
```

### Reverse Process

```python
# Convert sequences back to text
lines = tokenizer.sequences_to_texts(sequences)
```

## Stop Words Removal

Tokenizer doesn't remove stop words. Use NLTK for this:

```python
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import nltk 
nltk.download('stopwords')
nltk.download('punkt_tab')

def remv_stopwords(text):
    text = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    text = [word for word in text if word not in stop_words]
    return " ".join(text)

# Apply to all lines
lines = list(map(remv_stopwords, lines))
```

**Note:** Removing stop words often has **little effect** on text classification performance.

## Padding Sequences

Neural networks require fixed-length input. Use `pad_sequences`:

```python
from tensorflow.keras.preprocessing.sequence import pad_sequences

padded_seq = pad_sequences(sequences, maxlen=4)
```

**Padding Behavior:**
- **Default**: Pads/truncates on the **left**
- Use `padding='post'` to pad/truncate on the **right** (important for translation tasks)

## Embedding Layer

Converts word indices to dense vectors:

```python
Embedding(input_dim=10000, output_dim=32, input_length=100)
```

**Parameters:**
- `input_dim`: Vocabulary size (from Tokenizer)
- `output_dim`: Embedding dimensions (m) - typically 32-512
- `input_length`: Padded sequence length (n)

**How it works:**
- Each word → m-dimensional vector
- Vectors learned during training
- **More dimensions = more capacity but longer training**
- **Small datasets may not learn effective embeddings**

**Output**: 2D matrix of shape `(m, n)` where m=embedding dimensions, n=sequence length

## Text Classification Architecture

```
Input → Embedding → Flatten → Dense → Output
```

The **Flatten** layer converts 2D embedding output to 1D for dense layers.

## Automated Text Vectorization

Use `TextVectorization` layer instead of manual Tokenizer + pad_sequences:

```python
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Flatten, Embedding 
from tensorflow.keras.layers import TextVectorization, InputLayer 
import tensorflow as tf 

model = Sequential() 
model.add(InputLayer(input_shape=(1,), dtype=tf.string))
model.add(TextVectorization(max_tokens=max_words, 
                           output_sequence_length=max_length))
model.add(Embedding(max_words, 32, input_length=max_length))
model.add(Flatten()) 
model.add(Dense(128, activation='relu')) 
model.add(Dense(1, activation='sigmoid')) 

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
```

### Adaptation Step

```python
# Must adapt TextVectorization to training data
model.layers[1].adapt(x_train)  # x_train = your training texts
```

### Prediction with Raw Text

```python
text = 'Why pay more for expensive meds when you can order them online and save $$$?'
prediction = model.predict([text])[0][0]
```

**Advantages:**
- No manual preprocessing needed
- Direct raw text input for predictions
- **Cannot save in H5 format** - use SavedModel format:
```python
model.save('saved_model')
```

**Note:** TextVectorization doesn't remove stop words by default.

## N-grams

Capture word pairs (or n consecutive words):

```python
model.add(TextVectorization(max_tokens=max_words,
                           output_sequence_length=max_length, 
                           ngrams=2))  # Consider word pairs
```

**Limitation**: Only captures directly adjacent words.

## Convolutional Neural Networks (CNNs) for Text

Replace dense layers with 1D convolutions:

```python
from tensorflow.keras.layers import Conv1D, MaxPooling1D, GlobalMaxPooling1D 

model = Sequential() 
model.add(InputLayer(input_shape=(1,), dtype=tf.string)) 
model.add(TextVectorization(max_tokens=max_words,
                           output_sequence_length=max_length)) 
model.add(Embedding(max_words, 32, input_length=max_length)) 

model.add(Conv1D(32, 7, activation='relu'))  # 7-word window
model.add(MaxPooling1D(5)) 
model.add(Conv1D(32, 7, activation='relu')) 
model.add(GlobalMaxPooling1D()) 
model.add(Dense(1, activation='sigmoid')) 
```

**How CNNs work with text:**
- `Conv1D` extracts features from word groups (like pixel blocks in images)
- `MaxPooling1D` reveals higher-level patterns
- Often **more accurate than bag-of-words** but requires experimentation

## Recurrent Neural Networks (RNNs)

### Basic Concept

RNNs process sequences while maintaining "memory" of previous words through hidden states.

**Key Idea**: Each word's processing depends on previous words, capturing context and order.

### Long Short-Term Memory (LSTM)

Addresses vanishing gradient problem in long sequences:

```python
from tensorflow.keras.layers import LSTM 

model = Sequential() 
model.add(InputLayer(input_shape=(1,), dtype=tf.string)) 
model.add(TextVectorization(max_tokens=max_words,
                           output_sequence_length=max_length)) 
model.add(Embedding(max_words, 32, input_length=max_length)) 
model.add(LSTM(32))  # Single LSTM layer
model.add(Dense(1, activation='sigmoid')) 
```

**LSTM Strengths:**
- Learns which words are important
- Maintains long-term dependencies better than basic RNNs
- **Compute intensive** - trains slower

### Stacked LSTMs

For complex sequence modeling:

```python
model.add(LSTM(32, return_sequences=True))  # Return all hidden states
model.add(LSTM(32, return_sequences=True))  
model.add(LSTM(32))  # Only last layer returns final state
```

**Note**: `return_sequences=True` for all but final LSTM layer.

### GRU Alternative

Gated Recurrent Units - simplified LSTM that trains faster:

```python
from tensorflow.keras.layers import GRU
model.add(GRU(32))  # Replace LSTM with GRU
```

## Key Takeaways

1. **Preprocessing consistency**: Tokenize and pad prediction text same as training text
2. **Embedding dimensions**: 32-512, balance capacity vs training time
3. **TextVectorization**: Automates preprocessing, accepts raw text
4. **Model choice**: Experiment with Dense, CNN, LSTM based on task and data
5. **N-grams**: Capture local word relationships
6. **Compute cost**: LSTMs > CNNs > Dense layers

## When to Use Each Approach

- **Dense + Flatten**: Simple, fast baseline
- **CNNs**: Good for local patterns, faster than RNNs
- **LSTM/GRU**: Complex sequence dependencies, slower training
- **N-grams**: When word co-occurrence matters

**Pro Tip**: Bag-of-words (Dense) models are often surprisingly effective and fast!