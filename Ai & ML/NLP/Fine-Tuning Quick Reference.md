### **Architecture tweak**
- Start with the pretrained transformer (e.g., `bert-base-uncased`).
- Add a **classification head** (usually: a dense layer + softmax) on top of the `[CLS]` token’s hidden state.
- This head learns task-specific decision boundaries while the transformer weights are updated a little.
### **Steps in practice**
1. **Load the model and tokenizer**
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
```
    
2. **Prepare dataset**
    - Tokenize texts with padding/truncation.
    - Create train/validation splits.
3. **Training loop / Trainer API**
    - Use `Trainer` from Hugging Face or write a PyTorch loop.
    - Optimizer: **AdamW**.
    - Learning rate: small (`2e-5` to `5e-5`).
    - Batch size: typically 16–32 (depending on GPU).
    - Epochs: 2–4 is often enough.
---
### 4. **Fine-tuning strategies**
- **Full fine-tuning:** update all transformer layers + classification head (common).
- **Feature extraction:** freeze transformer weights, only train classification head (faster, less data-hungry).
- **Layer freezing:** unfreeze only the last few layers (a middle ground).

---
### **Tricks to improve**

- **Class imbalance?** → use weighted loss or resampling.
- **Small dataset?** → try **data augmentation** (back-translation, synonym replacement) or **few-shot methods**.
- **Overfitting?** → dropout, early stopping, layer freezing.
- **Evaluation** → track accuracy, F1, precision, recall depending on your task.

---

### **1. Install and import**

```python
!pip install transformers datasets evaluate
```

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import evaluate
import numpy as np
```

---

### **2. Load dataset**

For a demo, let’s grab a built-in dataset (IMDB reviews, binary classification).

```python
dataset = load_dataset("imdb")
```

This gives you `train`, `test`, and `unsupervised` splits.

---

### **3. Load tokenizer and model**

```python
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=2  # because IMDB is positive/negative
)
```

---

### **4. Tokenize the dataset**

We feed text into the tokenizer → model-ready tensors.

```python
def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize, batched=True)
```

---

### **5. Define metrics**

We’ll track accuracy for simplicity.

```python
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return accuracy.compute(predictions=predictions, references=labels)
```

---

### **6. Training setup**

```python
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=50,
)
```

---

### **7. Trainer API**

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"].shuffle(seed=42).select(range(5000)),  # subset for quick demo
    eval_dataset=tokenized_dataset["test"].shuffle(seed=42).select(range(1000)),
    compute_metrics=compute_metrics,
)
```

---

### **8. Train**

```python
trainer.train()
```

This will fine-tune BERT on IMDB sentiment classification .

---
## 1. Why Fine-Tuning Works

- Models like **BERT** are pretrained on massive text corpora using **self-supervised objectives** (e.g., masked language modeling).
- They learn **general-purpose language representations**: syntax, semantics, word relations.
- Fine-tuning adapts this general knowledge to your **downstream classification task** (sentiment analysis, intent detection, topic classification, etc.).
---

## 🔹 2. Architecture for Classification
- Take the **pretrained encoder** (BERT).
- Extract the hidden state of the special `[CLS]` token (or sometimes a pooled representation).
- Add a **classification head**: typically a fully connected layer + softmax for multi-class or sigmoid for multi-label.
- During training, the whole network (encoder + head) is optimized on your dataset.
---

## 🔹 3. Fine-Tuning Strategies

1. **Full Fine-Tuning**
    - All parameters (transformer + classification head) are updated.
    - Best when you have **enough labeled data** (thousands+).
2. **Feature Extraction (Frozen Encoder)**
    - Freeze transformer layers, only train classification head.
    - Useful for **small datasets** (hundreds of samples) to avoid overfitting.
3. **Layer-wise Fine-Tuning**
    - Freeze most layers, unfreeze only the last few transformer layers + head.
    - Middle ground between full fine-tuning and feature extraction.
4. **Adapters / Parameter-Efficient Fine-Tuning (PEFT)**
    - Instead of updating all parameters, add small trainable modules (like **LoRA, adapters**).
    - Efficient in low-resource settings.
---
## 🔹 4. Training Setup

- **Optimizer:** AdamW (works well with transformers).
- **Learning Rate:** small values (`2e-5` to `5e-5`), because pretrained weights are already in a good state.
- **Batch Size:** 16–32 (GPU dependent).
- **Epochs:** usually 2–4 (transformers converge quickly).
- **Regularization:** dropout, weight decay, early stopping.
---

## 🔹 5. Data Considerations

- **Tokenization:** always tokenize with the pretrained model’s tokenizer.
- **Max Length:** texts longer than the model’s max length (e.g., 512 for BERT) need truncation or chunking.
- **Class Imbalance:** handle with weighted loss, resampling, or focal loss.
- **Evaluation Metrics:**
    - Accuracy if balanced classes.
    - Precision, Recall, F1 if imbalanced or multi-label.
---

## 🔹 6. Typical Workflow

1. **Load pretrained model & tokenizer** (`bert-base-uncased`, etc.).
2. **Preprocess dataset:** tokenize, pad, truncate.
3. **Attach classification head** (often already integrated in Hugging Face models like `AutoModelForSequenceClassification`).
4. **Define training loop** (Trainer API or custom PyTorch).
5. **Train & evaluate** with chosen metrics.
6. **Save & deploy** the fine-tuned model.
---

## 🔹 7. Tricks to Improve Performance

- **Small datasets:** freeze layers, use data augmentation (back translation, synonym replacement).
- **Large datasets:** full fine-tuning works best.
- **Domain shift (e.g., medical/legal text):** consider domain-specific pretrained models (BioBERT, LegalBERT).
- **Efficiency:** use distillation (DistilBERT), quantization, pruning for faster inference.
---
## 🔹 8. Summary (Key Points)
- Pretrained language models already “understand” text — fine-tuning teaches them to make specific **decisions**.
- The classification head is small; most power comes from the pretrained encoder.
- Small learning rate, small batch size, and few epochs are usually enough.
- Strategy depends on dataset size:
    - **Large dataset → full fine-tuning**
    - **Small dataset → frozen layers or PEFT methods**

|Strategy|What It Does|When to Use|Pros|Cons|
|---|---|---|---|---|
|**Full Fine-Tuning**|Update **all transformer layers + classification head**|Large dataset (thousands+ labeled examples)|Best performance, model fully adapts|Expensive (time, GPU, memory), risk of overfitting if data is small|
|**Feature Extraction (Frozen Encoder)**|Freeze transformer, train only classification head|Small dataset (hundreds of examples)|Fast, less compute, avoids overfitting|Lower accuracy (model can’t adapt to task-specific nuances)|
|**Layer-wise Fine-Tuning**|Freeze most layers, unfreeze last few + head|Medium dataset|Balance of performance & efficiency|More tuning effort (which layers to unfreeze)|
|**Adapters / PEFT (LoRA, Prefix Tuning, etc.)**|Keep transformer frozen, add small trainable modules|Low-resource or multi-task scenarios|Efficient (few extra params), reuses base model for many tasks|Slightly less performance than full fine-tuning|
|**Domain-Adaptive Pretraining (DAPT)**|Pretrain further on domain-specific text (e.g., medical) before classification fine-tuning|When domain is very different from general text|Huge gains in domain tasks|Requires large unlabeled domain corpus|

---

## 🔹 1. Full Fine-Tuning (default)

👉 All layers + classification head are updated.

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)
# Nothing frozen → everything gets trained
```

This is the **standard** when you call `.from_pretrained(...)`.

---

## 🔹 2. Feature Extraction (Frozen Encoder)

👉 Freeze transformer, only train classification head.

```python
for param in model.bert.parameters():  # freeze encoder
    param.requires_grad = False

# Only classification head (model.classifier) will update
```

Best for **tiny datasets** where full fine-tuning would overfit.

---

## 🔹 3. Layer-Wise Fine-Tuning

👉 Unfreeze just the last few transformer layers.

```python
# Freeze all layers first
for param in model.bert.parameters():
    param.requires_grad = False

# Unfreeze the last two layers + classifier
for layer in model.bert.encoder.layer[-2:]:
    for param in layer.parameters():
        param.requires_grad = True

for param in model.classifier.parameters():
    param.requires_grad = True
```

Good balance for **medium-sized datasets**.

---

## 🔹 4. Adapters / Parameter-Efficient Fine-Tuning (PEFT)

👉 Use **LoRA / Adapters** with Hugging Face PEFT.

```python
!pip install peft

from peft import get_peft_model, LoraConfig, TaskType

peft_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,   # sequence classification
    r=8,                          # rank
    lora_alpha=32,
    lora_dropout=0.1
)

model = get_peft_model(model, peft_config)
```

This keeps most of BERT frozen and trains only small LoRA modules. **Efficient** for low compute and multi-task settings.

---

## 🔹 5. Domain-Adaptive Pretraining (DAPT)

👉 Extra step before fine-tuning. Pretrain on domain text with Masked LM, then fine-tune for classification.

```python
from transformers import AutoModelForMaskedLM

# Step 1: Load model for masked language modeling
mlm_model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")

# Step 2: Continue pretraining on your domain corpus
# (use Trainer with MLM objective)

# Step 3: Load pretrained weights into classifier
classifier_model = AutoModelForSequenceClassification.from_pretrained(
    "path_to_domain_adapted_checkpoint",
    num_labels=num_classes
)
```

Useful for **medical, legal, or financial NLP** where text differs from general English.

---

✅ Now you’ve got the **practical recipes** for all fine-tuning strategies.  
Think of it like a ladder:
- Start with **frozen head** if data is tiny.
- Move up to **last layers** if you have more.
- Go **full fine-tuning** when dataset is large.
- Use **LoRA/adapters** when compute is limited or you want to serve many tasks.
- Add **DAPT** if domain is highly specialized.

---
