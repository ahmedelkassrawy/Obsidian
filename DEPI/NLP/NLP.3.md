# Sequence Modeling Applications

| Sequence Type     | Application Example                       |
| ----------------- | ----------------------------------------- |
| one to one        | Binary Classification                     |
| one to many       | Image Captioning                          |
| many to one       | Sentiment Classification (e.g., Sentiment Analysis) |
| many to many      | Machine Translation                       |
| many to many      | Named Entity Recognition                  |

> [!note]  
> In many-to-many settings, **Machine Translation** typically uses different input/output lengths, while **Named Entity Recognition** often preserves sequence length.

# Comparison between RNN and ANN

| Feature | Artificial Neural Network (ANN) | Recurrent Neural Network (RNN) |
| :--- | :--- | :--- |
| **Data Type** | Works with fixed-size input data. | Designed for sequential data, like a sentence or a time series, where the order of data matters. |
| **Structure** | In an ANN, data flows in one direction—from the input layer, through hidden layers, to the output layer—without any feedback or loops. Each neuron processes its input and passes it to the next layer, with no revisiting of previous layers. | Has loops in its structure, allowing it to "remember" previous inputs as it processes new ones. This is crucial for understanding sequences. |
| **Memory** | Doesn't have memory. It processes each input independently without considering previous inputs. | Has memory. It keeps track of past information to influence the current output, which is important for tasks like language translation or speech recognition. |
| **Usage** | Used for tasks where the input data doesn't depend on order like classification. | • Speech Recognition<br>• Sentiment Classification<br>• Machine Translation (i.e. Chinese to English)<br>• Video Activity Recognition<br>• Name Entity Recognition — (i.e. Identifying names in a sentence) |

---

# ANN VS CNN VS RNN

### Artificial Neural Network (ANN):
* ANN is the basic type of neural network. It consists of layers of interconnected "neurons," which are simple processing units.

* **How it works:** Information flows through these layers, where each neuron processes the input data and passes it to the next layer. ANNs are used for general tasks like recognizing patterns in data.

### Convolutional Neural Network (CNN):
* CNN is a specialized type of ANN designed for processing images.

* **How it works:** CNN uses layers that automatically detect features in images, like edges, shapes, and textures. This makes it great for tasks like image recognition (e.g., identifying objects in photos).

### Recurrent Neural Network (RNN):
* RNN is another type of neural network designed to handle sequential data, like time series or text.

* **How it works:** RNNs have connections that loop back on themselves, allowing them to "remember" previous information in a sequence. This makes them suitable for tasks like predicting the next word in a sentence or analyzing speech.

# Sequence Modeling & Recurrent Neural Networks

## Sequence Modeling Applications

| Sequence Type     | Application Example                       |
| ----------------- | ----------------------------------------- |
| one to one        | Binary Classification                     |
| one to many       | Image Captioning                          |
| many to one       | Sentiment Classification (Sentiment Analysis) |
| many to many      | Machine Translation                       |
| many to many      | Named Entity Recognition                  |

> [!note]  
> In many-to-many settings, **Machine Translation** typically uses different input/output lengths, while **Named Entity Recognition** often preserves sequence length.

---

# Comprehensive Guide to Neural Networks: ANN, CNN, and RNN Architecture

## 1. High-Level Comparison: ANN vs. CNN vs. RNN

### Feature Comparison Matrix

| Feature | Artificial Neural Network (ANN) | Recurrent Neural Network (RNN) |
| :--- | :--- | :--- |
| **Data Type** | Works with fixed-size input data. | Designed for sequential data, like a sentence or a time series, where the order of data matters. |
| **Structure** | In an ANN, data flows in one direction—from the input layer, through hidden layers, to the output layer—without any feedback or loops. Each neuron processes its input and passes it to the next layer, with no revisiting of previous layers. | Has loops in its structure, allowing it to "remember" previous inputs as it processes new ones. This is crucial for understanding sequences. |
| **Memory** | Doesn't have memory. It processes each input independently without considering previous inputs. | Has memory. It keeps track of past information to influence the current output, which is important for tasks like language translation or speech recognition. |
| **Usage** | Used for tasks where the input data doesn't depend on order like classification. | • Speech Recognition<br>• Sentiment Classification<br>• Machine Translation (i.e., Chinese to English)<br>• Video Activity Recognition<br>• Name Entity Recognition (i.e., Identifying names in a sentence) |

## 2. Recurrent Neural Network (RNN) Deep Dive

> [!info] The RNN Approach
> The RNN is a highly preferred method, especially for sequential data. 
> Every node at a time step consists of an input from the previous node, and it proceeds using a **feedback loop**.

### How Recurrent Neural Networks Work

RNNs process sequences of vectors step-by-step:
1.  **Sequential Processing:** The network processes the sequence of vectors one by one.
2.  **State Passing:** While processing, it passes the previous hidden state to the next step of the sequence.
3.  **Memory Foundation:** The hidden state acts as the neural networks memory. It holds information on previous data the network has seen before.

At a granular level:
*   First, the input and previous hidden state are combined (concatenated) to form a new vector.
*   That vector now contains information regarding both the *current* input and *previous* inputs.
*   This combined vector passes through the **tanh activation** function.
*   The output of this activation is the **new hidden state**, or the memory of the network for the next step.

---

## 3. Architectural Breakdown & Mathematics

RNNs apply a recurrence relation at every time step to process a sequence. A core property of the RNN architecture is that **the same function and set of parameters (weights) are used at every single time step.**

### Mathematical Notation

*   $x^{(t)}$: Input vector at time step $t$ (e.g., $x_1$ could be a one-hot vector corresponding to a word in a sentence).
*   $h^{(t)}$: Hidden state at time step $t$. It acts as the "memory" of the network.
*   $\hat{y}^{(t)}$: Output vector at time step $t$.
*   $W_{hh}$: Weight matrix connecting recurrent connections between hidden states.
*   $W_{xh}$: Weight matrix connecting inputs to a hidden layer.
*   $W_{hy}$: Weight matrix connecting hidden states to outputs.
*   $b_h, b_o$: Bias terms for the hidden state and output, respectively.

### The Core Equations

In an RNN, each node generates a current hidden state and an output. These are obtained using the given input and the previous hidden state.

**1. General State Equation:**
$$h_t = f(W_h h_{t-1} + V_h x_t + b_h)$$
*(Where $f$ is a non-linear transformation such as $tanh$)*

**2. Detailed Hidden State Update:**
Using matrix notation with explicit weight matrices, the hidden state $h_t$ is calculated as:
$$h_t = \tanh(W_{hh}^T h_{t-1} + W_{xh}^T x_t)$$

**3. Output Vector:**
Once the hidden state is updated, the output vector for that time step is calculated:
$$\hat{y}_t = W_{hy}^T h_t$$
*(or more generally $o_t = f(W_o h_t + b_o)$)*

![[Pasted image 20260501004501.png]]

![[Pasted image 20260501004547.png]]

---
## 4. The Tanh Activation Function

> [!abstract] Why Tanh?
> The function $f$ in the state update equation is typically taken to be a non-linear transformation such as **tanh**.

The `tanh` (hyperbolic tangent) activation is used to help regulate the values flowing through the network. Because the RNN continuously multiplies weights and adds states in a loop, values could quickly explode or vanish. The `tanh` function **squishes values to always be between -1 and 1**, keeping the network stable over many time steps.

---
## 5. Computational Graph Unrolled Across Time
To train and understand an RNN, it is often represented as a computational graph **unrolled across time**.

1.  **Unrolling:** The single RNN cell with a feedback loop is drawn as a series of connected cells, one for each time step $t = 0, 1, 2, ...$
2.  **Shared Weights:** During the forward pass, the matrices $W_{xh}$, $W_{hh}$, and $W_{hy}$ are identical at $t_0, t_1, t_2$, etc.
3.  **Loss Calculation:** At each time step where an output $\hat{y}_t$ is generated, a Loss $L_t$ (e.g., $L_0, L_1, L_2$) is calculated. The total loss $L$ is computed from these individual step losses.
---
## 6. Back Propagation Through Time (BPTT)
Backpropagation algorithm:
1. Take the derivative (gradient) of the loss with respect to each parameter
2. shift parameters in order to minimize loss

![[Pasted image 20260501004831.png]]

## 7. RNN without Tanh
- **Vanishing Exploding Gradients**: During back propagation , RNN suffers from the vanishing gradient problem. Gradients are values used to update a neural network weights. The vanishing gradient problem is when the gradient shrinks as it back propagates through time. If a gradient value becomes extremely small , it doesn't contribute too much learning

- **Loss of Non Linearity**: Activation functions like tanh introduce non linearity , which is crucial for the network to learn complex patterns. Without it the RNN becomes more like a linear model, severally limiting its ability to learn and represent complex sequences or time dependent data

- **Reduced Expressive Power**: Non linear activation function enable the network to learn more complex mappings from inputs to outputs. Removing the tanh reduces the expressive power of RNN, making it less effective in capturing the underlying patterns in sequential data.

```python
# 1. Import Required Libraries
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 2. Prepare Simple Text Data
sentences = [
    "I love machine learning",
    "Deep learning is a subset of machine learning",
    "I don't enjoy machine learning at all",
    "LSTM networks are not very useful and often frustrating"
]

# Labels (for simplicity, let's just use binary labels)
labels = np.array([1, 1, 0, 0])

# 3. Text Preprocessing
# Initialize the Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(sentences)

# Padding sequences to have equal length
padded_sequences = pad_sequences(sequences, padding='post')

# Display tokenized and padded sequences
print("Word Index:", word_index)
print("Padded Sequences:\n", padded_sequences)

# 4. Build the RNN Model
# Define RNN model
rnn_model = Sequential([
    Embedding(input_dim=len(word_index) + 1, output_dim=8, input_length=padded_sequences.shape[1]),
    SimpleRNN(16),
    Dense(1, activation='sigmoid')
])

rnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Summary of the RNN model
rnn_model.summary()

# Train the RNN model
rnn_model.fit(padded_sequences, labels, epochs=10)

# 5. Make Predictions
# New sentences for prediction
new_sentences = ["I love deep learning", "I don't enjoy machine learning at all"]
new_sequences = tokenizer.texts_to_sequences(new_sentences)
new_padded_sequences = pad_sequences(new_sequences, padding='post', maxlen=padded_sequences.shape[1])

# Predictions
rnn_predictions = rnn_model.predict(new_padded_sequences)

print("RNN Predictions:\n", rnn_predictions)
```

## 8. Problems Of RNN
- Difficulty with long sequence: RNNS struggle to remember info from the beginning of a long sequence. As the sequence gets longer, it becomes harder for the network to retain important details which can lead to poor perf.

- Slower Computation: Since RNNS process one step at a time , they can be slower compared to other types of NN that process data in parallel
---
## LSTM 
- Long Short Term Memory Networks is an advanced RNN, a sequential network, that allows information to persist. It is capable of handling the vanishing gradient problem faced by RNN. A recurrent neural network is also known as RNN is used for persistent memory.

- It fails to store information for a longer period of time. At times, a reference to certain information stored quite a long time ago is required to predict the current output. But RNNs are absolutely incapable of handling such “long-term dependencies”.

- Other issues with RNNs like vanishing gradients (explained later) which occur during the training process of a network through backtracking.

![[Pasted image 20260501011130.png]]

## 1. Sigmoid
- LSTM gates contains sigmoid activations. Sigmoid function squishes values between 0 and 1.
- Any number getting multiplied by O is 0, causing values to disappears or be "forgotten." 
- Any number multiplied by 1 is the same value therefore that value stay's the same or is "kept."
- 
![[Pasted image 20260501011323.png]]

![[Pasted image 20260501011355.png]]

![[Pasted image 20260501011429.png]]

![[Pasted image 20260501011452.png]]

- The forget gate determines which relevant information from the prior steps is needed. 
- The input gate decides what relevant information can be added from the current step.
- The output gates finalize the next hidden state.

```python
# 1. Import Required Libraries
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 2. Prepare Simple Text Data
sentences = [
    'I love machine learning',
    'Deep learning is a subset of machine learning',
    'I don’t enjoy machine learning at all',
    'LSTM networks are not very useful and often frustrating'
]

# Labels (for simplicity, let's just use binary labels)
labels = np.array([1, 1, 0, 0])

# 3. Text Preprocessing
# Initialize the Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(sentences)

# Padding sequences to have equal length
padded_sequences = pad_sequences(sequences, padding='post')

#or for max length
max_len = 100
padded_sequences = pad_sequences(X_train,maxlen = maxlen)

# Display tokenized and padded sequences
print("Word Index:", word_index)
print("Padded Sequences:\n", padded_sequences)

# 4. Build the RNN Model
# Define LSTM model
lstm_model = Sequential([
    Embedding(input_dim=len(word_index) + 1, output_dim=8, input_length=padded_sequences.shape[1]),
    LSTM(16),
    Dense(1, activation='sigmoid')
])

lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Summary of the LSTM model
lstm_model.summary()

# Train the LSTM model
lstm_model.fit(padded_sequences, labels, epochs=10, verbose=1)

# 5. Make Predictions
# New sentences for prediction
new_sentences = ['I love deep learning']
new_sequences = tokenizer.texts_to_sequences(new_sentences)
new_padded_sequences = pad_sequences(new_sequences, padding='post', maxlen=padded_sequences.shape[1])

# Predictions
lstm_predictions = lstm_model.predict(new_padded_sequences)

print("LSTM Predictions:", lstm_predictions)
```

[twitter_sentiment_analysis_with_lstm.ipynb - Colab](https://colab.research.google.com/drive/1r8M5qP6ikt9QwYp73Ord_3az5nF6S498?usp=sharing#scrollTo=g6nrfG-1Z_ez)

---
## Steps in the Notebook (Focus on LSTM Part)

1. **Import Libraries**  
   - Data handling: `pandas`, `numpy`  
   - Text preprocessing: `re`, `nltk` (tokenizer, stopwords, lemmatizer)  
   - Machine learning: `sklearn.model_selection.train_test_split`, `LabelEncoder`  
   - Deep learning: `tensorflow.keras` (Tokenizer, pad_sequences, Sequential, Embedding, LSTM, Dense, Dropout, etc.)

2. **Load Data**  
   - Read `twitter_training.csv` and `twitter_test.csv`  
   - Rename columns: `['Header1', 'company', 'labels', 'text']`  
   - Drop `Header1` and `company` columns – keep only `labels` and `text`

3. **Combine & Clean**  
   - Concatenate training and test sets into one DataFrame (`sentiment`)  
   - Drop missing values (686 rows with null text) → 74994 rows left  
   - Drop duplicate rows (4743 duplicates) → final size

4. **Text Preprocessing**  
   - Function `process_text(text)`:
     - Remove extra spaces, special characters, single characters, non-alphabetical characters
     - Convert to lowercase
     - Tokenize with `word_tokenize`
     - Lemmatize with `WordNetLemmatizer`
     - Remove stopwords (English)
     - Remove words shorter than 4 characters
     - Keep only unique words per text (using `np.unique`)
   - Apply function to all texts → `cleaned_text` (list of word lists)

5. **Train/Test Split**  
   - `X_train`, `X_test`, `y_train`, `y_test` (80/20 split)

6. **Tokenization & Padding**  
   - `Tokenizer(num_words=20000)` fitted on `X_train`  
   - Vocabulary size = 24048  
   - Convert texts to sequences (`texts_to_sequences`)  
   - Pad sequences to `maxlen=100` (`pad_sequences`)

7. **Build LSTM Model**  
   - Input shape: `(maxlen,)`  
   - `Embedding(vocab_size+1, 100)` – output dimension 100  
   - `Dropout(0.5)`  
   - `LSTM(150)`  
   - `Dense(32, activation='relu')`  
   - `Dense(4, activation='softmax')` (4 classes: Negative, Positive, Neutral, Irrelevant)  
   - Optimizer: `Adam(learning_rate=0.0001)`  
   - Loss: `categorical_crossentropy`  
   - Metrics: `accuracy`

8. **Label Encoding & Training**  
   - `LabelEncoder` to convert `y_train`/`y_test` to integers  
   - One‑hot encode with `to_categorical`  
   - Train for 2 epochs (batch size default 32, 1757 steps per epoch)

9. **Evaluation & Visualization**  
   - Plot training/validation accuracy & loss  
   - Confusion matrix (seaborn heatmap)  
   - Test accuracy: ~70.1%, loss: ~0.787

---

## What is Used in the LSTM Model

| Layer / Component          | Details                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| **Embedding**              | `Embedding(24049, 100)` – Input dimension = vocab size + 1 (24049), output dimension = 100 |
| **Dropout**                | Rate = 0.5 – applied after embedding to prevent overfitting             |
| **LSTM**                   | 150 units – returns only the last output (default `return_sequences=False`) |
| **Dense (first)**          | 32 neurons, ReLU activation                                             |
| **Dense (output)**         | 4 neurons, softmax activation (class probabilities)                     |
| **Optimizer**              | Adam with learning rate = 0.0001                                        |
| **Loss function**          | Categorical crossentropy (multi‑class classification)                   |
| **Metrics**                | Accuracy                                                                |

**Training settings:**  
- Epochs = 2  
- Validation split = 20% (using separate `X_test` / `y_test`)  
- Batch size = default (32)  
---
## Steps for the SimpleRNN Model (from the notebook)

1. **Data Preparation**  
   - The same preprocessed data from earlier is reused:  
     - `X_train`, `X_test` – padded sequences (maxlen=100)  
     - `y_train_encoded`, `y_test_encoded` – label-encoded integers  
     - `y_train_one_hot`, `y_test_one_hot` – one‑hot encoded for 4 classes  

2. **Model Definition**  
   - **Input layer**: `Input(shape=(maxlen,))` where `maxlen = 100`  
   - **Embedding layer**: `Embedding(v + 1, D)` where `v = 24048` (vocab size), `D = 100` (embedding dimension)  
   - **Dropout**: `Dropout(0.5)` after embedding  
   - **SimpleRNN layer**: `SimpleRNN(150)` – returns last output (default)  
   - **Dense (hidden)**: `Dense(32, activation='relu')`  
   - **Output layer**: `Dense(4, activation='softmax')` (4 sentiment classes)  

3. **Compilation**  
   - Optimizer: `Adam(learning_rate=0.0001)`  
   - Loss: `categorical_crossentropy`  
   - Metrics: `accuracy`

4. **Training**  
   - Epochs: **2**  
   - Validation data: `(X_test, y_test_one_hot)`  
   - Training steps: `1757` steps per epoch (default batch size 32)

5. **Evaluation**  
   - Test accuracy: **~66.77%**  
   - Test loss: **~0.851**

6. **Visualization**  
   - Plots of training/validation accuracy and loss (similar to LSTM)

---
## What is Used in the SimpleRNN Model

| Component          | Specification                                          |
| ------------------ | ------------------------------------------------------ |
| **Embedding**      | `Embedding(24049, 100)` – vocab size → 100‑dim vectors |
| **Dropout**        | Rate = 0.5 (after embedding)                           |
| **SimpleRNN**      | 150 units – basic recurrent layer (no LSTM gates)      |
| **Dense (hidden)** | 32 neurons, ReLU activation                            |
| **Dense (output)** | 4 neurons, softmax activation                          |
| **Optimizer**      | Adam with learning rate = 0.0001                       |
| **Loss**           | Categorical crossentropy                               |
| **Epochs**         | 2                                                      |

### Key differences from LSTM:
- SimpleRNN has **no forget gate, input gate, or output gate** – it uses a single tanh activation for the hidden state update, making it simpler and faster but less effective at capturing long‑term dependencies.
- Number of parameters: ~2.45 million (vs LSTM had slightly more due to additional gates, but both are comparable here).