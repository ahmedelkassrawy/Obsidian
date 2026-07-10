
---
# Fine-Tuning NLP Models: Sentiment Analysis, Layer Freezing, SetFit, and MLM

This tutorial, based on the provided Python notebook, demonstrates fine-tuning pre-trained BERT models for sentiment analysis on the Rotten Tomatoes dataset, experimenting with layer freezing to optimize computation, using SetFit for few-shot learning, and pre-training for Masked Language Modeling (MLM). It also briefly introduces Named Entity Recognition (NER). The comments in the code highlight the motivation (e.g., fine-tuning vs. pre-trained models, computational efficiency) and guide the process.

Below, we break down each section with the **problem**, **goal**, **what we are doing**, and corresponding code, using the notebook’s comments to clarify intent.

## Prerequisites
- **Libraries**: Install `datasets`, `transformers`, `evaluate`, `setfit`, `wandb`.
- **Environment**: Python (e.g., Google Colab or Jupyter Notebook).
- **Dataset**: Rotten Tomatoes (binary sentiment classification: 0 = negative, 1 = positive).
- **Note**: Run commands in a Colab environment for simplicity ([Original Colab Link](https://colab.research.google.com/drive/1Gv6vS8FM67mo6Rigd7gq04bjpl5GM_fp)).

## Section 1: Loading the Dataset
### Problem
We need a dataset for sentiment analysis to train and evaluate a model.
### Goal
Load and split the Rotten Tomatoes dataset into training and test sets for binary sentiment classification.
### What We Are Doing
As per the comment: *“Prepare data and splits”*, we use the `datasets` library to load the Rotten Tomatoes dataset, which contains movie reviews labeled as positive or negative. We split it into `train_data` and `test_data` for model training and evaluation.

```python
from datasets import load_dataset

# Prepare data and splits
tomatoes = load_dataset("rotten_tomatoes")
train_data, test_data = tomatoes["train"], tomatoes["test"]
```

- **Action**: Check the dataset size.
```python
train_data.shape  # Output: (8530, 2) - 8530 examples with 'text' and 'label'
```

![[Pasted image 20250930180556.png]]

## Section 2: Setting Up Model and Tokenizer
### Problem
We need a pre-trained model and tokenizer suitable for sentiment classification.

### Goal
Initialize a BERT model and tokenizer for sequence classification with two labels (positive/negative).

### What We Are Doing
The comment implies we’re setting up a foundation for fine-tuning: *“Load model and tokenizer”*. We use `bert-base-cased` from Hugging Face’s Transformers library, configured for binary classification (`num_labels=2`).

```python
!pip install transformers --quiet

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model and tokenizer
model_id = "bert-base-cased"
model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_id)
```

![[Pasted image 20250930181910.png]]

## Section 3: Preprocessing the Data
### Problem
Raw text data needs to be converted into a format suitable for BERT (token IDs, attention masks).

### Goal
Tokenize the dataset and apply dynamic padding to ensure uniform input lengths.

### What We Are Doing
The comment explains: *“we will add padding to the input text to create equally sized representations. We use DataCollatorWithPadding for that”*. We define a preprocessing function to tokenize text with truncation and use `DataCollatorWithPadding` to pad sequences dynamically during training.

```python
from transformers import DataCollatorWithPadding

# Pad to the longest seq in the batch
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

def preprocess(examples):
    return tokenizer(examples["text"], truncation=True)

tokenized_train = train_data.map(preprocess, batched=True)
tokenized_test = test_data.map(preprocess, batched=True)
```

![[Pasted image 20250930181945.png]]

## Section 4: Defining Metrics
### Problem
We need a metric to evaluate model performance during training and testing.

### Goal
Use the F1 score to measure classification performance, suitable for balanced evaluation.

### What We Are Doing
As noted: *“Use evaluate library instead of datasets”*, we install `evaluate` and define a function to compute the F1 score by comparing predicted and true labels.

```python
!pip install evaluate --quiet

import numpy as np
import evaluate

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    pred = np.argmax(logits, axis=-1)
    load_f1 = evaluate.load("f1")
    f1 = load_f1.compute(predictions=pred, references=labels)["f1"]
    return {"f1": f1}
```

![[Pasted image 20250930182126.png]]

## Section 5: Full Fine-Tuning the Model
### Problem
Pre-trained BERT may not perform optimally on the Rotten Tomatoes dataset without task-specific tuning.

### Goal
Fine-tune the entire BERT model to achieve high F1 score (around 0.85) for sentiment classification.

### What We Are Doing
The comment states: *“It shows that fine-tuning a model yourself can be more advantageous than using a pretrained model. It only costs us a couple of minutes to train”*. We set up training arguments (e.g., learning rate, epochs) and use the `Trainer` API to fine-tune and evaluate the model.

```python
from transformers import TrainingArguments, Trainer

# Training arguments for parameter tuning
training_args = TrainingArguments(
    "model",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=1,
    weight_decay=0.01,
    save_strategy="epoch",
    report_to="none"
)

# Trainer which executes the training process
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.evaluate()  # Expected F1 ~0.85
```

![[Pasted image 20250930183401.png]]

## Section 6: Freezing Layers (Classification Head Only)
### Problem
Full fine-tuning is computationally expensive, especially with limited resources.

### Goal
Reduce computation by freezing all layers except the classification head and compare performance (expected F1 ~0.63).

### What We Are Doing
The comments guide us: *“We will freeze the main BERT model and allow only updates to pass through the classification head. This will be a great comparison as we will keep everything the same, except for freezing specific layers”* and *“We have frozen everything except for the feedforward neural network, which is our classification head”*. We inspect model layers, freeze all except those starting with “classifier”, and retrain.

```python
model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Inspect layers
for name, param in model.named_parameters():
    print(name)

# Freeze everything except classifier
for name, param in model.named_parameters():
    if name.startswith("classifier"):
        param.requires_grad = True
    else:
        param.requires_grad = False

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.evaluate()  # Expected F1 ~0.63
```

![[Pasted image 20250930183454.png]]

## Section 7: Partial Freezing (Up to Encoder Block 10)
### Problem
Freezing all layers except the classifier significantly reduces performance.

### Goal
Freeze layers only up to encoder block 10 (index < 165) to balance computation and performance (expected F1 ~0.80).

### What We Are Doing
The comment explains: *“Instead of freezing nearly all layers, let’s freeze everything up until encoder block 10... A major benefit is that this reduces computation but still allows updates to flow through part of the pretrained model”*. We freeze layers before index 165 and retrain.

```python
model_id = "bert-base-cased"
model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Freeze everything before encoder block 11 (index < 165)
for index, (name, param) in enumerate(model.named_parameters()):
    if index < 165:
        param.requires_grad = False

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.evaluate()  # Expected F1 ~0.80
```

## Section 8: Few-Shot Learning with SetFit
### Problem
Labeling large datasets is time-consuming; we need good performance with few labeled examples.

### Goal
Use SetFit to achieve high F1 (~0.85) with only 32 labeled samples (16 per class).

### What We Are Doing
The comments outline SetFit’s algorithm: *“The underlying algorithm of SetFit consists of three steps: 1. Sampling training data... 2. Fine-tuning embeddings... 3. Training a classifier”*. We sample 16 examples per class, fine-tune a SentenceTransformer model, and train a classifier on generated sentence pairs.

```python
!pip install setfit --quiet
from setfit import sample_dataset

# Sample 16 examples per class (32 total)
sampled_train_data = sample_dataset(tomatoes["train"], num_samples=16)

from setfit import SetFitModel, TrainingArguments as SetFitTrainingArguments, Trainer as SetFitTrainer

# Load SentenceTransformer model
model = SetFitModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")

args = SetFitTrainingArguments(
    num_epochs=3,
    num_iterations=20  # Number of text pairs to generate
)
args.eval_strategy = args.evaluation_strategy

trainer = SetFitTrainer(
    model=model,
    args=args,
    train_dataset=sampled_train_data,
    eval_dataset=test_data,
    metric="f1"
)

!pip install wandb --quiet
import wandb
wandb.init()

trainer.train()
trainer.evaluate()  # Expected F1 ~0.85
```

- **Note**: The comment highlights: *“Notice that the output mentions that 1,280 sentence pairs were generated... With only 32 labeled documents, we get an F1 score of 0.85... very impressive!”*.

## Section 9: Masked Language Modeling (MLM)
### Problem
The pre-trained BERT model may not be fully adapted to the Rotten Tomatoes domain.

### Goal
Continue pre-training BERT with MLM to improve domain-specific representations, then test with fill-mask tasks.

### What We Are Doing
The comments explain: *“We will be going with token masking... using DataCollatorForLanguageModeling for faster convergence”*. We pre-train BERT with MLM, masking 15% of tokens, and save the model. We then compare fill-mask predictions.

```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

# Load MLM model
model = AutoModelForMaskedLM.from_pretrained("bert-base-cased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

# Tokenize data (remove labels for MLM)
tokenized_train = train_data.map(preprocess_function, batched=True)
tokenized_train = tokenized_train.remove_columns("label")
tokenized_test = test_data.map(preprocess_function, batched=True)
tokenized_test = tokenized_test.remove_columns("label")

from transformers import DataCollatorForLanguageModeling

# Masking Tokens (15% probability)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

# Training arguments
training_args = TrainingArguments(
    "model",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=10,
    weight_decay=0.01,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Save tokenizer
tokenizer.save_pretrained("mlm")
trainer.train()
model.save_pretrained("mlm")
```

### Test MLM Performance
Compare predictions for “What a horrible [MASK]!”.

```python
from transformers import pipeline

# Original BERT
mask_filler = pipeline("fill-mask", model="bert-base-cased")
preds = mask_filler("What a horrible [MASK]!")
for pred in preds:
    print(f">>> {pred['sequence']}")

# Fine-tuned MLM
mask_filler = pipeline("fill-mask", model="mlm")
preds = mask_filler("What a horrible [MASK]!")
for pred in preds:
    print(f">>> {pred['sequence']}")
```

- **Note**: The comment suggests: *“The next step would be to fine-tune this model on the classification task”* using:
```python
from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained("mlm", num_labels=2)
tokenizer = AutoTokenizer.from_pretrained("mlm")
```

## Section 10: Introduction to Named Entity Recognition (NER)
### Problem
Classifying entire documents is insufficient for tasks requiring token-level classification, like identifying entities in sensitive data.

### Goal
Understand how to fine-tune BERT for NER to classify individual tokens (e.g., people, locations) for de-identification.

### What We Are Doing
The comments clarify: *“Instead of classifying entire documents, this procedure allows for the classification of individual tokens and/or words... especially helpful for de-identification and anonymization tasks”*. We outline the process (no full code provided) for token-level classification using `AutoModelForTokenClassification`.

- **Key Points** (from comments):
  - *“NER shares similarities with the classification example... a key distinction lies in the preprocessing and classification of data”*.
  - *“Rather than relying on the aggregation or pooling of token embeddings, the model now makes predictions for individual tokens”*.
  - Use a NER dataset (e.g., CoNLL-2003) and preprocess with token alignment.

- **Example Setup**:
```python
from transformers import AutoModelForTokenClassification
model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=NUM_NER_LABELS)  # e.g., 9 for BILOU
# Preprocess with token alignment for labels
```

label2id = { "O": 0, "B-PER": 1, "I-PER": 2, "B-ORG": 3, "I-ORG": 4, "B-LOC": 5, "I-LOC": 6, "B-MISC": 7, "I-MISC": 8 } id2label = {index: label for label, index in label2id.items()} label2id {'O': 0, 'B-PER': 1, 'I-PER': 2, 'B-ORG': 3, 'I-ORG': 4, 'B-LOC': 5, 'I-LOC': 6, 'B-MISC': 7, 'I-MISC': 8} These entities correspond to specific categories: a person (PER), organization (ORG), location (LOC), miscellaneous entities (MISC), and no entity (O). Note that these entities are prefixed with either a B (beginning) or an I (inside). If two tokens that follow each other are part of the same phrase, then the start of that phrase is indicated with B, which is followed by an I to show that they belong to each other and are not independent entities. This process is further illustrated in Figure 11-20. In the figure, since “Dean” is the start of the phrase and “Palmer” is the end, we know that “Dean Palmer” is a person and that “Dean” and “Palmer” are not individual people.

![[Pasted image 20250930183735.png]]

## Summary of Problems and Goals
- **Overall Problem**: Optimize BERT for sentiment analysis, reduce computational cost, achieve high performance with few labels, adapt to domain, and extend to token-level tasks.
- **Overall Goal**: Demonstrate fine-tuning strategies (full, partial freezing, few-shot, MLM) and introduce NER for practical NLP applications.
- **Results**:
  - Full fine-tuning: F1 ~0.85.
  - Freezing all but classifier: F1 ~0.63.
  - Freezing up to block 10: F1 ~0.80.
  - SetFit with 32 samples: F1 ~0.85.
  - MLM improves domain adaptation; NER setup outlined.

---