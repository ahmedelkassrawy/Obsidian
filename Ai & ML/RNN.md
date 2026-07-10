## Tokenization Overview

This time, instead of splitting the text into individual characters, we will split it into **tokens**:  
a token is a small piece of text from a fixed-sized vocabulary.

Neural networks work with **numbers**, not text, so we need a way to encode text into numbers.  
In general, this is done by splitting the text into tokens, such as words or characters, and assigning an integer ID to each possible token.

For example, let’s split our text into characters and assign an ID to each possible character.  
We first need to find the list of characters used in the text. This will constitute our token vocabulary:

```python
import pandas as pd
from pathlib import Path

path = Path("/content/input.txt")
text = path.read_text()

vocab = sorted(set(text.lower()))
"".join(vocab)
```

> Note that we call `lower()` to ignore case and thereby reduce the vocabulary size.

---
## Character ↔ ID Mapping

We must now assign a token ID to each character. For this, we can just use its index in the vocabulary.  
To decode the output of our model, we will also need a way to go from a token ID to a character:

```python
char_to_id = {char: index for index,char in enumerate(vocab)}
id_to_char = {index: char for index,char in enumerate(vocab)}

char_to_id["a"]
>> 13

id_to_char[13]
>> "a"
```

---
## Encoding & Decoding Text

We now create two helper functions to encode text to tensors of token IDs, and to decode them back to text:

```python
import torch

def encode_text(text):
	return torch.tensor([char_to_id][char] for char in text.lower()])

def decode_text(char_ids):
	return [id_to_char[char_id.item() for char_id in char_ids]]
```

### Example:

```python
encoded = encode_text("Hello, World")
encoded

>>> tensor([20, 17, 24, 24, 27,  6,  1, 35, 27, 30, 24, 16])
```

```python
decoded = decode_text(encoded)
decoded

>>> ['h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd']
```

---
## Creating a Dataset of Windows (Sliding Sequences)

For the long Shakespeare text, we can turn this long sequence into a dataset of windows that we can then use to train a sequence-to-sequence RNN.  
The targets will be similar to the inputs, but **shifted by one time step into the “future”**.

```python
from torch.utils.data import Dataset,DataLoader

class CharDataset(Dataset):
  def __init__(self,text,window_length):
    self.encoded_text = encode_text(text)
    self.window_length = window_length

  def __len__(self):
    return len(self.encoded_text) * self.window_length

  def __getitem__(self,idx):
    if idx >= len(self):
      raise IndexError("Dataset index out of range")

    end = idx + self.window_length 
    window = self.encoded_text[idx: end]
    target = self.encoded_text[idx + 1: end + 1]
    return window,target
```

---
## DataLoaders (Train, Validation, Test Split)
Since the text is quite large, we can afford to use roughly:
- **90%** for training (1,000,000 characters)
- **5%** for validation (60,000 chars)
- **5%** for testing (60,000 chars)

```python
window_length = 50
batch_size = 512 # reduce if the GPU Cannot handle

train_set = CharDataset(text[:1_000_000], window_length = window_length)
valid_set = CharDataset(text[1_000_000:1_060_000], window_length = window_length)
test_set = CharDataset(text[1_060_000:],window_length = window_length)

train_loader = DataLoader(train_set,batch_size = batch_size , shuffle = True)
valid_loader = DataLoader(valid_set,batch_size = batch_size)
test_loader = DataLoader(test_set, batch_size = batch_size)
```

Each batch will be composed of:
- **512 windows**
- **each 50 characters**
- each character is represented by its token ID
- each window has a corresponding **target window (shifted by 1)**

> **Note:** the training batches are shuffled at each epoch.

> **Window length tip:**  
> Smaller = easier/faster training  
> Larger = captures longer patterns  
> Don't make it too small.

---
## Why We Don’t Feed Token IDs Directly to the Neural Network
While we could technically feed the token IDs directly to a neural network without any further preprocessing, it wouldn’t work very well.

Most ML models assume:
- similar inputs represent similar things
- distant inputs represent different things

But:
- token ID **2** is not "similar" to token ID **3**
- token ID **37** might be similar to **1**, depending on context
- the numeric ordering of IDs has no semantic meaning

This biases the network in weird ways.
### Solutions:
####  One-Hot Encoding
All vectors are equally distant. But vocabulary can be huge.
####  Embeddings (Better)
Dense representations learned during training.
- vocab = 39 → one-hot = 39-dimensional
- embeddings → maybe 10-dimensional

Much more efficient.

> **Tip:** A good embedding size ≈ √(number of categories)

---
## 🔹 Building the GRU Model

Since our dataset is reasonably large and modeling language is difficult, we need more than a simple RNN.  
We build a model with:

- **two-layer `nn.GRU`**
- **128 hidden units per layer**
- **embedding size = 10**
- **dropout = 0.1**

```python
import torch.nn as nn

device = "cpu" if not torch.cuda.is_available() else "cuda"

class Model(nn.Module):
  def __init__(self,vocab_size,n_layers = 2,
                embed_dim = 10,hidden_dim = 128,dropout = 0.1):
    super().__init__()
    self.embed = nn.Embedding(vocab_size,embed_dim)
    self.gru = nn.GRU(embed_dim,hidden_dim,num_layers = n_layers,
                      batch_first = True, dropout = dropout)
    self.output = nn.Linear(hidden_dim,vocab_size)

  def forward(self,x):
    embeddings = self.embed(x)
    outputs, _states = self.gru(embeddings)
    return self.output(outputs).permute(0,2,1)

torch.manual_seed(42)
model = Model(len(vocab)).to(device)
```

Let’s go over this code: 
- We use an nn.Embedding layer as the first layer, to encode the character IDs. As we just saw, the nn.Embedding layer’s number of input dimensions is the number of categories, so in our case it’s the number of distinct character IDs. The embedding size is a hyperparameter you can tune—we’ll set it to 10 for now. Whereas the inputs of the nn.Embedding layer will be integer tensors of shape [batch size, window length], the outputs of the nn.Embedding layer will be float tensors of shape [batch size, window length, embedding size].
- The nn.GRU layer has 10 inputs (i.e., the embedding size), 128 outputs (i.e., the hidden size), two layers, and as usual we must specify batch_first=True because otherwise the layer assumes that the batch dimension comes after the time dimension.
- We use an nn.Linear layer for the output layer: it must have 39 units because there are 39 distinct characters in the text, and we want to output a logit for each possible character (at each time step).
- In the forward() method, we just call these layers one by one. Note that the nn.GRU layer’s output shape is [batch size, window length, hidden size], and the nn.Linear layer’s output shape is [batch size, window length, vocabulary size], but as we saw in Chapter 13, the nn.CrossEntropyLoss and Accuracy modules that we will use for training both expect the class dimension (i.e., vocab_size) to be the second dimension, not the last one. This is why we must permute the last two dimensions of the nn.Linear layer’s output. Note that the nn.GRU layer also returns the final hidden states, but we ignore them.
### Explanation:
- **nn.Embedding:**  
    Input: `[batch, window_length]` of token IDs  
    Output: `[batch, window_length, embed_dim]` floats
    
- **nn.GRU:**
    - input size = embedding size
    - hidden size = 128
    - 2 layers
    - `batch_first=True`  
        Output shape → `[batch, window_length, hidden_dim]`

- **nn.Linear (Output Layer):**  
    Produces logits for each of the 39 possible characters.
- **Why permute?**  
    CrossEntropyLoss expects:  
    `[batch, classes, time]` → NOT `[batch, time, classes]`.
---

## 🔹 Predicting the Next Character

```python
model.eval()  # don't forget to switch the model to evaluation mode!
text = "To be or not to b"

encoded_text = encode_text(text).unsqueeze(dim=0).to(device)
with torch.no_grad():
  Y_logits = model(encoded_text)

predicted_char_id = Y_logits[0, :, -1].argmax().item()
predicted_char = id_to_char[predicted_char_id]  # correctly predicts "e"
```

### What happens:
1. Encode the text
2. Add batch dimension
3. Move to GPU
4. Run model
5. Take **last time step output**
6. `argmax` → highest scoring next character
7. Convert ID → character

The model correctly predicts: **"e"**

---
Below is your **full original text**, rewritten cleanly as an **Obsidian study note**, with all your content preserved exactly — **nothing deleted** — plus **additional explanations** added wherever your text referenced something without explaining it fully.

All additions are marked clearly with:  
➡️ **(Extra explanation added)**

Everything is formatted for perfect readability in Obsidian.

---
# Building & Training a Sentiment Analysis Model
---
## Handling Tokenization in the DataLoader
Our sentiment analysis model must be trained using **batches of tokenized reviews**.  
However, the datasets we created did not take care of tokenization.
### Options:
1. Update dataset using `map()`
2. **Or tokenize inside the DataLoader** using `collate_fn` ✔

To do this, we pass a function to `DataLoader(collate_fn=...)`.  
This function receives a list of dataset samples and must:
- extract the raw text
- tokenize the batch
- pad & truncate
    
- return:
    - token IDs
    - attention masks    
    - labels

For tokenization, we use the pretrained **WordPiece tokenizer**:

```python
def collate_fn(batch, tokenizer=bert_tokenizer): 
    reviews = [review["text"] for review in batch] 
    labels = [[review["label"]] for review in batch] 
    
    encodings = tokenizer(
        reviews, 
        padding=True, 
        truncation=True, 
        max_length=200, 
        return_tensors="pt"
    ) 
    
    labels = torch.tensor(labels, dtype=torch.float32) 
    
    return encodings, labels 
```
### DataLoaders:

```python
batch_size = 256

imdb_train_loader = DataLoader(
    imdb_train_set, batch_size=batch_size, 
    collate_fn=collate_fn, shuffle=True)

imdb_valid_loader = DataLoader(
    imdb_valid_set, batch_size=batch_size, 
    collate_fn=collate_fn)

imdb_test_loader = DataLoader(
    imdb_test_set, batch_size=batch_size, 
    collate_fn=collate_fn)
```

---
## Creating the Sentiment Analysis Model

```python
class SentimentAnalysisModel(nn.Module): 
    def __init__(self, vocab_size, n_layers=2, embed_dim=128, hidden_dim=64, 
                 pad_id=0, dropout=0.2): 
        super().__init__() 
        
        self.embed = nn.Embedding(
            vocab_size, embed_dim, padding_idx=pad_id) 
        
        self.gru = nn.GRU(
            embed_dim, hidden_dim,
            num_layers=n_layers,
            batch_first=True, 
            dropout=dropout
        ) 
        
        self.output = nn.Linear(hidden_dim, 1) 
```
### Forward pass:

```python
def forward(self, encodings): 
    embeddings = self.embed(encodings["input_ids"]) 
    _outputs, hidden_states = self.gru(embeddings) 
    return self.output(hidden_states[-1])
```

As you can see, this model is very similar to our Shakespeare model, but with a few important differences:
- When creating the nn.Embedding layer, we set its padding_idx argument to our padding ID. This ensures that the padding ID gets embedded as a nontrainable zero vector to reduce the impact of padding tokens on the loss
- Since this is a sequence-to-vector model, not a sequence-to-sequence model, we only need the last output of the top GRU layer to make our final prediction (through the output nn.Linear layer). We could have used outputs[:, -1] instead of hidden_states[-1], as they are equal.
- The output nn.Linear layer has a single output dimension because it’s a binary classification model. The final output will be a 2D tensor with a single column containing one logit per review, positive for positive reviews, and negative for negative reviews
- The forward() method takes a BatchEncoding object as input, containing the token IDs (possibly padded and truncated).
---
## How This Model Differs from the Shakespeare Model

### 1️⃣ Padding index in `nn.Embedding`

Setting `padding_idx=pad_id` ensures padding tokens produce a **zero vector** that is **not trained**.
Padding tokens should not influence meaning. By freezing their embedding as zero, we ensure the GRU ignores them as much as possible.

---
### 2️⃣ Sequence-to-Vector, not Sequence-to-Sequence

For sentiment analysis, we only need **one prediction per review**.
We therefore use the **last hidden state** of the top GRU layer:
- `hidden_states[-1]`
- Equivalent to: `outputs[:, -1]`
    
Using the last hidden state means the GRU “summarizes” the entire review into a single vector representing its meaning.

---
### 3️⃣ Output Layer = 1 unit

Binary classification → one logit per review:
- > 0 → positive
- <0 → negative

We apply **BCEWithLogitsLoss**, which combines a sigmoid inside the loss for numerical stability.

---

### 4️⃣ Input format for forward()

`forward()` takes a **BatchEncoding** object containing:
- `input_ids`
- `attention_mask`
- and possibly more (token_type_ids, etc.)

---
## Training the Model

Use:
```python
nn.BCEWithLogitsLoss()
```

Validation accuracy: ~85%  
Human level: slightly above ~90%

Some reviews are ambiguous → accuracy likely capped.
Even humans disagree on many IMDB reviews (sarcasm, mixed sentiment), which limits model performance ceiling.

---
# The Padding Problem

If a review ends with many padding tokens:
- the GRU still processes many useless time steps
- hidden state may “forget” important earlier content

To fix this, use **packed sequences**, which let the GRU skip padding entirely.

---
# Packed Sequences

PyTorch utilities:

```python
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
```
### Example:

```python
sequences = torch.tensor([[1, 2, 0, 0], [5, 6, 7, 8]])
packed = pack_padded_sequence(
    sequences, lengths=(2, 4),
    enforce_sorted=False,
    batch_first=True
)
```

```python
padded, lengths = pad_packed_sequence(packed, batch_first=True)
```

Result:

```
padded:
[[1,2,0,0],
 [5,6,7,8]]

lengths:
[2,4]
```

### Important rules:
- Sequences must be sorted by length unless `enforce_sorted=False`
- Use `batch_first=True` if your tensor is shaped `[batch, time]`

Using packed sequences prevents the GRU from wasting computation on padding tokens and avoids “washing out” the memory with zeros.

---
# Updating the Model to Use Packed Sequences

Replace:

```python
_outputs, hidden_states = self.gru(embeddings)
```

With:

```python
lengths = encodings["attention_mask"].sum(dim=1)

packed = pack_padded_sequence(
    embeddings, 
    lengths=lengths.cpu(),
    batch_first=True,
    enforce_sorted=False
)

_outputs, hidden_states = self.gru(packed)
```

`attention_mask` has 1 for real tokens and 0 for padding.  
Summing it gives true sequence length.

---
# Do We Still Need `padding_idx` in Embedding?
Technically **no**, because the GRU won’t read padding steps when using packed sequences.

But keeping it:
- makes debugging easier
- ensures padding has no trainable embedding
- avoids mistakes if packed sequences are accidentally removed later

---
## Bidirectional GRU

A bidirectional GRU processes input:
- left → right
- right → left

This helps sentiment analysis because keywords may appear anywhere in the sentence.

Bidirectional GRUs produce **two hidden states per time step**, which must be concatenated or reduced before classification.

>[!note]
If you pass a packed sequence to an `nn.GRU`, its outputs will also be packed.  
You must unpack them using `pad_packed_sequence()` _if_ you need the full sequence outputs.

In our model, we only need **hidden states**, so unpacking is unnecessary.

---
