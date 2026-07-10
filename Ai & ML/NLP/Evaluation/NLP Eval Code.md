## Categories of metrics

There are 3 high-level categories of metrics:

1. _Generic metrics_, which can be applied to a variety of situations and datasets, such as precision and accuracy.
2. _Task-specific metrics_, which are limited to a given task, such as Machine Translation (often evaluated using metrics [BLEU](https://huggingface.co/metrics/bleu) or [ROUGE](https://huggingface.co/metrics/rouge)) or Named Entity Recognition (often evaluated with [seqeval](https://huggingface.co/metrics/seqeval)).
3. _Dataset-specific metrics_, which aim to measure model performance on specific benchmarks: for instance, the [GLUE benchmark](https://huggingface.co/datasets/glue) has a dedicated [evaluation metric](https://huggingface.co/metrics/glue).

Currently supported tasks are:
- `"text-classification"`: will use the [TextClassificationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.TextClassificationEvaluator).
- `"token-classification"`: will use the [TokenClassificationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.TokenClassificationEvaluator).
- `"question-answering"`: will use the [QuestionAnsweringEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.QuestionAnsweringEvaluator).
- `"image-classification"`: will use the [ImageClassificationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.ImageClassificationEvaluator).
- `"text-generation"`: will use the [TextGenerationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.TextGenerationEvaluator).
- `"text2text-generation"`: will use the [Text2TextGenerationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.Text2TextGenerationEvaluator).
- `"summarization"`: will use the [SummarizationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.SummarizationEvaluator).
- `"translation"`: will use the [TranslationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.TranslationEvaluator).
- `"automatic-speech-recognition"`: will use the [AutomaticSpeechRecognitionEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.AutomaticSpeechRecognitionEvaluator).
- `"audio-classification"`: will use the [AudioClassificationEvaluator](https://huggingface.co/docs/evaluate/v0.4.6/en/package_reference/evaluator_classes#evaluate.AudioClassificationEvaluator).

#### BLEU 
Used for: Machine Translation or Text generation tasks.
**Idea:**  
BLEU measures how many words or short phrases (_n-grams_) in the generated text **match** the reference (true) translation.
- BLEU = 1 → Perfect match
- BLEU = 0 → Completely different
```python
from datasets import load_metric

# Load BLEU metric
bleu = load_metric("bleu")

# Example machine translation outputs
predictions = [
    ["the cat is on the mat".split()],
    ["there is a cat on the mat".split()]
]
references = [
    [["the cat is on the mat".split()]],
    [["the cat is on the mat".split()]]
]

# Compute BLEU score
results = bleu.compute(predictions=predictions, references=references)
print(results)
```

#### ROUGE
Used for: Summarization or Text Generation tasks.

**Idea:**  
ROUGE compares the **overlap** between the model’s summary and the human summary.  
It focuses more on **recall** — how much of the reference summary is captured.

**Variants:**
- **ROUGE-1:** Overlap of single words
- **ROUGE-2:** Overlap of word pairs (bigrams)
- **ROUGE-L:** Longest common subsequence
```python
from datasets import load_metric

rouge = load_metric("rouge")

predictions = ["the cat sat on the mat"]
references = ["the cat is sitting on the mat"]

results = rouge.compute(predictions=predictions, references=references)
print(results)
```

#### Seqeval
**Used for:**  
→ _Named Entity Recognition (NER)_, _Part-of-Speech tagging_, or any _sequence labeling_ task.

**Idea:**  
It measures **precision**, **recall**, and **F1-score** for entity spans (like “PERSON”, “LOCATION”).  
It checks whether the predicted entity labels **match the true entities** in both type and span.
```python
from datasets import load_metric

seqeval = load_metric("seqeval")

predictions = [["B-PER", "I-PER", "O", "B-LOC"]]
references = [["B-PER", "I-PER", "O", "B-LOC"]]

results = seqeval.compute(predictions=predictions, references=references)
print(results)
```

```python
{'overall_precision': 1.0, 
'overall_recall': 1.0, 
'overall_f1': 1.0, 
'overall_accuracy': 1.0}
```

|Metric|Used For|Measures|Typical Output|Notes|
|---|---|---|---|---|
|**BLEU**|Machine Translation|n-gram precision overlap|BLEU score (0–1)|Word order matters|
|**ROUGE**|Summarization|Recall-based word overlap|ROUGE-1, ROUGE-2, ROUGE-L|Focuses on coverage|
|**seqeval**|NER / POS tagging|Precision, Recall, F1|Entity-level metrics|Checks full span and type|
Perfect 👌 — let’s now connect those metrics (BLEU, ROUGE, and seqeval) to **Hugging Face’s `Trainer`**, which is how you typically evaluate models during fine-tuning.

We’ll go one task at a time so you can see the pattern clearly.

---

## 🟦 1. Machine Translation → **BLEU**

We’ll use a small example fine-tuning a translation model like `"Helsinki-NLP/opus-mt-en-fr"`.

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

model_name = "Helsinki-NLP/opus-mt-en-fr"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

dataset = load_dataset("wmt14", "fr-en", split="train[:1%]")

# Tokenize function
def preprocess(example):
    inputs = example["en"]
    targets = example["fr"]
    model_inputs = tokenizer(inputs, max_length=64, truncation=True)
    labels = tokenizer(targets, max_length=64, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess, batched=True)
metric = load_metric("bleu")

# Compute BLEU after each eval step
def compute_metrics(eval_pred):
    preds, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    decoded_preds = [pred.split() for pred in decoded_preds]
    decoded_labels = [[label.split()] for label in decoded_labels]
    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    return {"bleu": result["bleu"]}

args = TrainingArguments(
    output_dir="./mt_bleu",
    evaluation_strategy="epoch",
    per_device_train_batch_size=4,
    num_train_epochs=1,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
```

👉 During training, `Trainer` will print BLEU score each epoch automatically.

---

## 🟩 2. Summarization → **ROUGE**

Now let’s switch to a summarization model like `"facebook/bart-base"`.

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")

dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:1%]")

def preprocess(examples):
    inputs = [doc for doc in examples["article"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["highlights"], max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess, batched=True)
metric = load_metric("rouge")

def compute_metrics(eval_pred):
    preds, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    result = metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True)
    return {k: v.mid.fmeasure for k, v in result.items()}

args = TrainingArguments(
    output_dir="./summarization_rouge",
    evaluation_strategy="epoch",
    per_device_train_batch_size=2,
    num_train_epochs=1,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
```

👉 You’ll see ROUGE-1, ROUGE-2, and ROUGE-L scores in the training log.

---

## 🟥 3. Named Entity Recognition (NER) → **seqeval**

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

dataset = load_dataset("conll2003")
label_list = dataset["train"].features["ner_tags"].feature.names
model_name = "bert-base-cased"

model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(label_list))
tokenizer = AutoTokenizer.from_pretrained(model_name)
metric = load_metric("seqeval")

def tokenize_and_align_labels(example):
    tokenized = tokenizer(example["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(example["ner_tags"]):
        word_ids = tokenized.word_ids(batch_index=i)
        aligned_labels = []
        previous_word_id = None
        for word_id in word_ids:
            if word_id is None:
                aligned_labels.append(-100)
            elif word_id != previous_word_id:
                aligned_labels.append(label[word_id])
            else:
                aligned_labels.append(-100)
            previous_word_id = word_id
        labels.append(aligned_labels)
    tokenized["labels"] = labels
    return tokenized

tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

def compute_metrics(p):
    predictions, labels = p
    predictions = predictions.argmax(axis=2)
    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {"f1": results["overall_f1"], "accuracy": results["overall_accuracy"]}

args = TrainingArguments(
    output_dir="./ner_seqeval",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=1,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset["train"].select(range(1000)),
    eval_dataset=tokenized_dataset["validation"].select(range(200)),
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
```

👉 Here, you’ll see `overall_f1` and `accuracy` printed after each epoch — the key metrics for NER.

---

### 🧩 Recap: What You Learned

|Task|Metric|Trainer Function|Measures|
|---|---|---|---|
|Translation|BLEU|`compute_metrics(eval_pred)`|n-gram overlap|
|Summarization|ROUGE|`compute_metrics(eval_pred)`|coverage of reference|
|NER|seqeval|`compute_metrics(p)`|entity-level F1 & accuracy|

---
