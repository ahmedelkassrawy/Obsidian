## 1. Tokenization with BERT

Before feeding text into a model, it must be converted into tokens. Modern models like BERT use subword tokenization (e.g., "replayed" → ["replay", "##ed"]). This allows the model to handle unknown words by breaking them into recognizable parts (e.g., "unkindness" ≈ "un" + "kind" + "ness").

### Example: Tokenizing Text

```python
from transformers import AutoTokenizer

# Load BERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Text to tokenize
text = "She replayed the song"

# Tokenize
tokens = tokenizer.tokenize(text)
input_ids = tokenizer.encode(text, add_special_tokens=True)

print("Tokens:", tokens)
print("Input IDs:", input_ids)
```

**Output**:

```
Tokens: ['she', 'replay', '##ed', 'the', 'song']
Input IDs: [101, 2016, 15712, 2098, 1996, 2299, 102]
```

- **Explanation**:
    - `AutoTokenizer`: Automatically selects the appropriate tokenizer for BERT.
    - `bert-base-uncased`: A case-insensitive English BERT model.
    - `input_ids`: Numerical IDs for tokens, including special tokens `[CLS]` (101) and `[SEP]` (102).
    - Tokens are subwords; `##ed` indicates a continuation of the previous token.

## 2. Understanding BERT

BERT (Bidirectional Encoder Representations from Transformers) is a language model developed by Google. It understands context by analyzing text bidirectionally, making it ideal for tasks like sentiment analysis.

### How BERT Works

- **Bidirectional Context**: BERT looks at both left and right context to understand words (e.g., "bank" in "The bank was flooded" could mean a river or financial institution).
- **Masked Language Modeling (MLM)**: BERT masks random words in a sentence and predicts them based on context (e.g., "I love [MASK] models" → "language").

### Embeddings

- **Token Embeddings**: Each token is represented as a 768-dimensional vector.
- **Sentence Embeddings**: The `[CLS]` token provides a representation of the entire sentence.
- **Example Output**: For a sentence with 7 tokens, the embedding matrix is shaped `[1, 7, 768]` (1 sentence, 7 tokens, 768 dimensions).

```python
from transformers import AutoTokenizer, AutoModel
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Input text
text = "She replayed the song"

# Tokenize into PyTorch tensors
inputs = tokenizer(text, return_tensors="pt")

# Run through BERT
with torch.no_grad():
    outputs = model(**inputs)

# Extract embeddings
cls_embedding = outputs.last_hidden_state[:, 0, :]  # Sentence-level embedding
print("CLS Vector shape:", cls_embedding.shape)
print("Last hidden state shape:", outputs.last_hidden_state.shape)
```

**Output**:

```
CLS Vector shape: torch.Size([1, 768])
Last hidden state shape: torch.Size([1, 7, 768])
```

- **Explanation**:
    - `last_hidden_state`: Embeddings for each token in the sentence.
    - `[CLS]` embedding: A single vector representing the entire sentence.

### BERT Architecture

- **Layers**: BERT-base has 12 layers, each using self-attention to process tokens and pass them to the next layer.
- **Self-Attention**: Allows the model to weigh the importance of each token relative to others in the sentence.

## 3. IMDb Sentiment Analysis Example

This section demonstrates how to apply BERT to the IMDb dataset for sentiment analysis (positive/negative movie reviews).

### 3.1 Loading the Dataset

```python
from datasets import load_dataset

# Load IMDb dataset and select a subset
dataset = load_dataset("imdb")
train_subset = dataset["train"].shuffle(seed=42).select(range(500))
```

- **Explanation**:
    - `load_dataset("imdb")`: Loads the IMDb dataset with movie reviews (text) and labels (0 = negative, 1 = positive).
    - `.shuffle(seed=42)`: Randomizes the dataset order.
    - `.select(range(500))`: Takes the first 500 examples for faster processing.

### 3.2 Tokenization

```python
# Define tokenization function
def tokenize_fn(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=256)

# Apply tokenization
tokenized_dataset = train_subset.map(tokenize_fn, batched=True)
```

**Output**:

```
Dataset({
    features: ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask'],
    num_rows: 500
})
```

- **Explanation**:
    - `tokenize_fn`: Converts text to token IDs, truncates to 256 tokens, and pads shorter sequences with zeros.
    - `map(batched=True)`: Applies tokenization efficiently across the dataset.

### 3.3 Data Formatting

```python
# Prepare dataset for PyTorch
tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
```

- **Explanation**:
    - `rename_column`: Renames "label" to "labels" to match BERT's expected input.
    - `set_format("torch")`: Converts data to PyTorch tensors.

### 3.4 Load BERT Model

```python
from transformers import AutoModelForSequenceClassification

# Load BERT for classification
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
```

- **Explanation**:
    - `num_labels=2`: Configures the model for binary classification (positive/negative).

### 3.5 Define Metrics

```python
import numpy as np

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = (predictions == labels).astype(np.float32).mean().item()
    return {"accuracy": acc}
```

- **Explanation**:
    - Computes accuracy by comparing predicted labels (highest logit) to true labels.

### 3.6 Training Setup

```python
from transformers import TrainingArguments, Trainer

# Define training arguments
training_args = TrainingArguments(
    output_dir="./bert-imdb",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=2,
    save_strategy="epoch",
    logging_dir="./logs",
)
```

- **Explanation**:
    - `output_dir`: Where to save the trained model.
    - `evaluation_strategy="epoch"`: Evaluates after each epoch.
    - `batch_size=8`: Processes 8 examples per batch to manage memory.
    - `num_train_epochs=2`: Trains for 2 epochs.

### 3.7 Train the Model

```python
# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset.select(range(400)),
    eval_dataset=tokenized_dataset.select(range(400, 500)),
    compute_metrics=compute_metrics,
)

# Train and evaluate
trainer.train()
trainer.evaluate()
```

**Output**:

```
Epoch  Training Loss  Validation Loss  Accuracy
1      No log         0.361679         0.860000
2      No log         0.358970         0.880000

{'eval_loss': 0.358970046043396,
 'eval_accuracy': 0.8799999952316284,
 'eval_runtime': 41.3065,
 'eval_samples_per_second': 2.421,
 'eval_steps_per_second': 0.315,
 'epoch': 2.0}
```

- **Explanation**:
    - Trains the model on 400 samples and evaluates on 100 samples.
    - Achieves ~88% accuracy on the validation set.

### 3.8 Predicting New Text

```python
# New text for prediction
new_text = "This movie was absolutely fantastic! The story was gripping and the acting was superb."

# Tokenize
inputs = tokenizer(
    new_text,
    return_tensors="pt",
    truncation=True,
    padding="max_length",
    max_length=256
)

# Predict
with torch.no_grad():
    outputs = model(**inputs)

# Get predicted class
logits = outputs.logits
predicted_class = torch.argmax(logits, dim=1).item()

# Interpret result
if predicted_class == 1:
    print("✅ Positive review!")
else:
    print("❌ Negative review.")
```

**Output**:

```
✅ Positive review!
```

- **Explanation**:
    - Tokenizes the new text similarly to training data.
    - Runs the model to get logits and predicts the class with the highest score.

## Notes

- This example uses `bert-base-uncased` for simplicity. Other models (e.g., `distilbert-base-uncased`) may be faster for experimentation.
- The IMDb dataset is large; using a subset (500 samples) speeds up processing for demonstration purposes.
- Adjust `max_length` or `batch_size` based on your hardware constraints.