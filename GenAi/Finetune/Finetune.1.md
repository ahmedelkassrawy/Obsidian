
## Loading the Dataset

The MRPC dataset is part of the GLUE benchmark, used for paraphrase detection (binary classification: equivalent or not equivalent).

```python
from datasets import load_dataset

raw_datasets = load_dataset("glue", "mrpc")
raw_datasets
```

**Output**:

```python
DatasetDict({
    train: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 3668
    })
    validation: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 408
    })
    test: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 1725
    })
})
```

### Dataset Features

Check the features of the training dataset to understand its structure:

```python
raw_train_dataset.features
```

**Output**:

```python
{
  'sentence1': Value(dtype='string', id=None),
  'sentence2': Value(dtype='string', id=None),
  'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
  'idx': Value(dtype='int32', id=None)
}
```

- **Features**:
    - `sentence1`, `sentence2`: Strings representing two sentences to compare.
    - `label`: Binary label (`not_equivalent` = 0, `equivalent` = 1).
    - `idx`: Integer index for each example.

---

## Tokenization

Use the `bert-base-uncased` tokenizer to preprocess the text data.

### Initialize Tokenizer

```python
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenized_sentences_1 = tokenizer(raw_datasets["train"]["sentence1"])
```

### Tokenized Output

Tokenizing two sentences (e.g., "This is the first sentence." and "This is the second one.") produces:

```python
{
  'input_ids': [101, 2023, 2003, 1996, 2034, 6251, 1012, 102, 2023, 2003, 1996, 2117, 2028, 1012, 102],
  'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
  'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}
```

- **Components**:
    - **`input_ids`**: Integer IDs for each token in the input, mapped to the tokenizer’s vocabulary.
        - `[CLS]` (101): Start token.
        - `[SEP]` (102): Separator between sentences or end of input.
    - **`token_type_ids`**: Segment IDs to distinguish sentences:
        - `0`: Tokens from sentence 1 (e.g., "This is the first sentence.").
        - `1`: Tokens from sentence 2 (e.g., "This is the second one.").
    - **`attention_mask`**: Indicates valid tokens vs. padding:
        - `1`: Pay attention (real token).
        - `0`: Ignore (padding token, not present in this example).

### Decode `input_ids` to Tokens

Convert `input_ids` back to words for verification:

```python
tokenizer.convert_ids_to_tokens(inputs["input_ids"])
```

**Output**:

```python
['[CLS]', 'this', 'is', 'the', 'first', 'sentence', '.', '[SEP]', 'this', 'is', 'the', 'second', 'one', '.', '[SEP]']
```

### Tokenize Function

Define a function to tokenize both sentences in the dataset:

```python
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
```

Apply the function to the dataset with batch processing:

```python
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
```

### Data Collator

Use `DataCollatorWithPadding` to dynamically pad sequences to the same length within a batch:

```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```

---

## Model Training

Fine-tune a BERT model for sequence classification (paraphrase detection).

### Initialize Model

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
```

- `num_labels=2`: Binary classification (not_equivalent, equivalent).

### Set Up Trainer

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments("test-trainer", eval_strategy="epoch")

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)
```

- **`TrainingArguments`**:
    - `"test-trainer"`: Directory to save model outputs.
    - `eval_strategy="epoch"`: Evaluate after each epoch.
- **`Trainer`**: Handles training and evaluation loops.

### Train the Model

```python
trainer.train()
```

---

## Evaluation

Evaluate the model on the validation set using the GLUE MRPC metrics (accuracy, F1 score).

### Predict and Compute Metrics

```python
import evaluate
import numpy as np

predictions = trainer.predict(tokenized_datasets["validation"])
print(predictions.predictions.shape, predictions.label_ids.shape)

preds = np.argmax(predictions.predictions, axis=-1)

metric = evaluate.load("glue", "mrpc")
metric.compute(predictions=preds, references=predictions.label_ids)
```

- **`predictions.predictions`**: Logits for each class (shape: `[num_examples, num_labels]`).
- **`predictions.label_ids`**: True labels (shape: `[num_examples]`).
- **`np.argmax`**: Selects the predicted class (0 or 1).
- **`metric.compute`**: Returns accuracy and F1 score for MRPC.

### Custom Compute Metrics Function

Define a function to compute metrics during training:

```python
def compute_metrics(eval_preds):
    metric = evaluate.load("glue", "mrpc")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)
```

### Updated Trainer with Metrics

Incorporate the `compute_metrics` function into the `Trainer`:

```python
training_args = TrainingArguments("test-trainer", eval_strategy="epoch")
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)
```

---
[Copy of finetune_llama3_1_unsloth.ipynb - Colab](https://colab.research.google.com/drive/12U6fGeMQxAKZPJueL_OUYS8UtggDixGE)