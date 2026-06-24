## 1. Generating Text Embeddings with Sentence Transformers

**Purpose**: Convert text data into dense vector representations (embeddings) for downstream tasks like classification.

**Key Concepts**:

- Use pre-trained models like `all-mpnet-base-v2` for robust embeddings.
- Embeddings capture semantic meaning of text.
- Suitable for tasks like sentiment analysis, topic classification, etc.

**Code Example**:

```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Convert text to embeddings
train_embeddings = model.encode(ds["train"]["text"], show_progress_bar=True)
test_embeddings = model.encode(ds["test"]["text"], show_progress_bar=True)
```

**Notes**:

- `ds` is assumed to be a dataset (e.g., from Hugging Face `datasets` library) with `train` and `test` splits containing `text` and `label` fields.
- `show_progress_bar=True` displays encoding progress for large datasets.
- Ensure sufficient memory for large datasets, as encoding can be resource-intensive.

## 2. Training a Logistic Regression Classifier

**Purpose**: Train a simple classifier on text embeddings to predict labels (e.g., positive/negative sentiment).

**Key Concepts**:

- Logistic regression is lightweight and effective for linearly separable embeddings.
- Evaluate model performance using metrics like precision, recall, and F1-score.

**Code Example**:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Train a logistic regression on our train embeddings
clf = LogisticRegression(random_state=42)
clf.fit(train_embeddings, ds["train"]["label"])

# Predict on test embeddings
y_pred = clf.predict(test_embeddings)

# Evaluate performance
print(classification_report(ds["test"]["label"], y_pred))
```

**Notes**:

- `random_state=42` ensures reproducibility.
- `classification_report` provides precision, recall, F1-score, and support for each class.
- Consider hyperparameter tuning (e.g., `C` for regularization) for better performance.

## 3. Zero-Shot Classification with Cosine Similarity

**Purpose**: Perform classification without training by comparing text embeddings to label embeddings.

**Key Concepts**:

- Zero-shot learning leverages semantic similarity (e.g., cosine similarity) between text and predefined labels.
- Useful when labeled data is scarce or for rapid prototyping.

**Code Example**:

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Zero-shot model
label_embeddings = model.encode(["A negative review", "A positive review"])

# Find the best matching label for each document
sim_matrix = cosine_similarity(test_embeddings, label_embeddings)
y_pred = np.argmax(sim_matrix, axis=1)

# Evaluate performance
print(classification_report(ds["test"]["label"], y_pred))
```

**Notes**:

- `label_embeddings` represent class descriptions (e.g., "A negative review" for class 0, "A positive review" for class 1).
- `cosine_similarity` computes similarity scores between test embeddings and label embeddings.
- `np.argmax` assigns the label with the highest similarity score.
- Performance depends on how well label descriptions capture class semantics.

## 4. Text Classification with Transformers (T5)

**Purpose**: Use a pre-trained transformer model (e.g., Flan-T5) for text-to-text generation to classify sentiment.

**Key Concepts**:

- T5 models treat all tasks as text-to-text, making them versatile for classification.
- Prompt engineering is critical for guiding the model to produce desired outputs.
- GPU acceleration (`device="cuda:0"`) improves inference speed.

**Code Example**:

```python
from transformers import pipeline
from tqdm import tqdm

# Load T5 model
pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device="cuda:0"
)

# Prepare data with prompt
prompt = "Is the following sentence positive or negative? "
data = ds.map(lambda example: {"t5": prompt + example['text']})

# Run inference
y_pred = []
for example in tqdm(data["test"], total=len(data["test"])):
    output = pipe(example['t5'])
    text = output[0]["generated_text"]
    y_pred.append(0 if text.lower() == "negative" else 1)  # Convert to lowercase for robust comparison

# Evaluate performance
print(classification_report(ds["test"]["label"], y_pred))
```

**Notes**:

- `pipeline` simplifies model loading and inference.
- The prompt `"Is the following sentence positive or negative?"` guides T5 to output "positive" or "negative."
- `tqdm` displays a progress bar for inference.
- Use `lower()` to handle case variations in model output.
- Larger T5 models (e.g., `flan-t5-base`) may improve accuracy but require more resources.
