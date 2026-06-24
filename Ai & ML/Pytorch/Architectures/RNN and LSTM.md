# NLP with RNN and LSTM in PyTorch

## Text Preprocessing
### Basic Preprocessing
Convert text to lowercase and remove punctuation.

```python
def preprocess(text):
  text = text.lower()
  text = text.replace("?","")
  text = text.replace("'","")
  return text.split()
```

**Usage**:

```python
preprocess(df["question"][0])
```

### Tokenization with spaCy

Tokenize text into words, excluding spaces.

```python
!pip install spacy
!python -m spacy download en_core_web_sm

import spacy
nlp = spacy.load("en_core_web_sm")

def tokenize(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if not token.is_space]
```

### Vocabulary Building and Numericalization

Create a vocabulary dictionary and convert text to indices.

```python
vocab = {'<UNK>': 0}

def build_vocab(row):
    tokenized_question = tokenize(row['question'])
    tokenized_answer = tokenize(row['answer'])
    merged_tokens = tokenized_question + tokenized_answer

    for token in merged_tokens:
        if token not in vocab:
            vocab[token] = len(vocab)

def text_to_indices(text, vocab):
    indexed_text = []
    for token in tokenize(text):
        indexed_text.append(vocab.get(token, vocab['<UNK>']))
    return indexed_text
```

**Usage**:

```python
df.apply(build_vocab, axis=1)
```

### Why These Steps?

1. **`tokenize(text)`**:
    - Splits text into tokens (words, punctuation).
    - Essential for NLP models (RNN, LSTM, Transformers).
    - Alternatives: NLTK, spaCy, or custom tokenizers.
2. **`build_vocab(df)`**:
    - Maps tokens to unique integer IDs for `nn.Embedding`.
    - Run once per dataset.
3. **`text_to_indices(text, vocab)`**:
    - Converts tokens to indices for model input.
    - Used every time text is fed to the model.

**NLP Preprocessing Pipeline**:

- Applies to RNNs, LSTMs, GRUs, Transformers, and attention-based models.
- Steps: Tokenize → Numericalize → Batch and pad sequences.

## RNN Model for Question Answering

### RNN Model Definition

A simple RNN model for processing tokenized questions.

```python
import torch.nn as nn

class RNN(nn.Module):
  def __init__(self, vocab_size):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, embedding_dim=50)
    self.rnn = nn.RNN(50, 64, batch_first=True)
    self.fc = nn.Linear(64, vocab_size)

  def forward(self, question):
    embedded_question = self.embedding(question)
    hidden, final = self.rnn(embedded_question)
    output = self.fc(final.squeeze(0))

    return output
```

### Prediction Function

Predict the answer to a question based on a probability threshold.

```python
def predict_py(model, question, threshold=0.5):
  # convert question to numbers
  numerical_question = text_to_indices(question, vocab)

  # tensor
  question_tensor = torch.tensor(numerical_question).unsqueeze(0)

  # send to model
  output = model(question_tensor)

  # convert logits to probs
  probs = torch.nn.functional.softmax(output, dim=1)

  # find index of max prob
  value, index = torch.max(probs, dim=1)

  if value < threshold:
    print("I don't know")

  print(list(vocab.keys())[index])
```

## LSTM for Next-Word Prediction

### Vocabulary Building with NLTK

Use NLTK for tokenization and vocabulary creation.

```python
from nltk.tokenize import word_tokenize

def build_vocab(text):
    tokens = word_tokenize(text)
    for token in tokens:
        token = token.lower()
        if token not in vocab:
            vocab[token] = len(vocab)

build_vocab(document)

# Token to index
def text_to_indices(text, vocab):
    return [vocab.get(token.lower(), vocab['<UNK>']) for token in word_tokenize(text)]
```

### Custom Dataset for Next-Word Prediction

Create input-output pairs for predicting the next word.

```python
from torch.utils.data import Dataset

class NextWordDataset(Dataset):
    def __init__(self, indices, seq_len=5):
        self.seq_len = seq_len
        self.data = []
        for i in range(len(indices) - seq_len):
            x = indices[i:i+seq_len]
            y = indices[i+seq_len]  # next token
            self.data.append((x, y))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x, y = self.data[idx]
        return torch.tensor(x), torch.tensor(y)
```

### LSTM Model Definition

An LSTM model for next-word prediction.

```python
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        emb = self.embedding(x)
        _, (h_n, _) = self.lstm(emb)
        out = self.fc(h_n[-1])  # use final hidden state
        return out
```

### Training Loop

Train the LSTM model using the dataset.

```python
from torch.utils.data import DataLoader
import torch

# Hyperparams
seq_len = 5
batch_size = 16
epochs = 10
lr = 0.001

# Dataset
dataset = NextWordDataset(indexed, seq_len=seq_len)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Model
model = LSTMModel(vocab_size=len(vocab))
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# Training loop
for epoch in range(epochs):
    total_loss = 0
    for x, y in dataloader:
        optimizer.zero_grad()
        output = model(x)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")
```

### Predicting the Next Word

Predict the next word given an input sequence.

```python
def predict_next_word(model, input_text, vocab, idx_to_word):
    model.eval()
    indices = text_to_indices(input_text, vocab)
    indices = indices[-seq_len:]  # keep last `seq_len` tokens
    input_tensor = torch.tensor(indices).unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_tensor)
        pred_index = torch.argmax(output, dim=1).item()
        print(f"Input: {input_text}")
        print(f"Predicted next word: {idx_to_word.get(pred_index, '<UNK>')}")
```

**Usage**:

```python
idx_to_word = {v: k for k, v in vocab.items()}
predict_next_word(model, "What is the", vocab, idx_to_word)
```

### Generating a Sentence

Generate a sentence by predicting one word at a time.

```python
def generate_sentence(model, seed_text, vocab, idx_to_word, max_length=20):
    model.eval()
    generated = text_to_indices(seed_text, vocab)

    for _ in range(max_length):
        input_seq = generated[-seq_len:]  # keep last seq_len tokens
        input_tensor = torch.tensor(input_seq).unsqueeze(0)  # shape: [1, seq_len]

        with torch.no_grad():
            output = model(input_tensor)  # shape: [1, vocab_size]
            next_token = torch.argmax(output, dim=1).item()

        generated.append(next_token)

        # Optional: stop if model repeats <UNK> or punctuation too much
        if idx_to_word.get(next_token, '<UNK>') in ['.', '?']:
            break

    # Convert indices back to words
    generated_words = [idx_to_word.get(i, '<UNK>') for i in generated]
    sentence = ' '.join(generated_words)
    return sentence
```

**Usage**:

```python
# Make sure you have idx_to_word
idx_to_word = {v: k for k, v in vocab.items()}

# Generate text
seed = "what is the course"
generated = generate_sentence(model, seed, vocab, idx_to_word, max_length=25)

print("Generated:", generated)
```

## Notes

- **Preprocessing**:
    - Use spaCy or NLTK for tokenization.
    - Build vocabulary once, then numericalize for model input.
    - `<UNK>` handles out-of-vocabulary words.
- **Models**:
    - RNN: Simple, good for short sequences but struggles with long dependencies.
    - LSTM: Better for capturing long-term dependencies.
- **Hyperparameters**:
    - `seq_len=5`: Sequence length for input context.
    - `batch_size=16`: Balances memory and training stability.
    - `epochs=10`, `lr=0.001`: Tune for better convergence.
- **Colab Tips**:
    - Install dependencies: `!pip install spacy nltk torch`.
    - Download NLTK data: `nltk.download('punkt')`.
    - Download spaCy model: `!python -m spacy download en_core_web_sm`.
    - Use GPU: `Runtime > Change runtime type > GPU`.

## Study Tips

- **Memorize Preprocessing Pipeline**: Tokenize → Build vocab → Numericalize → Batch/pad.
- **Understand RNN vs. LSTM**: RNN for simple tasks, LSTM for longer sequences.
- **Practice**: Run the code with a small text dataset (e.g., a few sentences).
- **Debugging**: Print `vocab` and `text_to_indices` outputs to verify correctness.

**Tags**: #pytorch #nlp #rnn #lstm #text-generation #next-word-prediction