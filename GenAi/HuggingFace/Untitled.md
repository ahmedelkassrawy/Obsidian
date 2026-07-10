#### Encoding Text
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

encoded_input = tokenizer("Hello, I'm a single sentence!")
print(encoded_input)
```

```python
{'input_ids': [101, 8667, 117, 1000, 1045, 1005, 1049, 2235, 17662, 12172, 1012, 102], 
 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
```

We get a dictionary with the following fields:
- input_ids: numerical representations of your tokens
- token_type_ids: these tell the model which part of the input is sentence A and which is sentence B (discussed more in the next section)
- attention_mask: this indicates which tokens should be attended to and which should not (discussed more in a bit)

We can decode the input IDs to get back the original text:
```python
tokenizer.decode(encoded_input["input_ids"])
```

```python
"[CLS] Hello, I'm a single sentence! [SEP]"
```

You can encode multiple sentences at once, either by batching them together (we’ll discuss this soon) or by passing a list:

```python
encoded_input = tokenizer("How are you?", "I'm fine, thank you!")
print(encoded_input)
```

```python
{'input_ids': [[101, 1731, 1132, 1128, 136, 102], [101, 1045, 1005, 1049, 2503, 117, 5763, 1128, 136, 102]], 
 'token_type_ids': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 
 'attention_mask': [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]}
```

We can also ask the tokenizer to return tensors directly from PyTorch:
```python
encoded_input = tokenizer("How are you?", "I'm fine, thank you!", return_tensors="pt")
print(encoded_input)
```

### Padding inputs

If we ask the tokenizer to pad the inputs, it will make all sentences the same length by adding a special padding token to the sentences that are shorter than the longest one:

```python
encoded_input = tokenizer(
    ["How are you?", "I'm fine, thank you!"], padding=True, return_tensors="pt"
)
print(encoded_input)

```

```python
{'input_ids': tensor([[  101,  1731,  1132,  1128,   136,   102,     0,     0,     0,     0],
         [  101,  1045,  1005,  1049,  2503,   117,  5763,  1128,   136,   102]]), 
 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 
 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}
```
### Truncating inputs

The tensors might get too big to be processed by the model. For instance, BERT was only pretrained with sequences up to 512 tokens, so it cannot process longer sequences. If you have sequences longer than the model can handle, you’ll need to truncate them with the `truncation` parameter:

```python
encoded_input = tokenizer(
    "This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence.",
    truncation=True,
)
print(encoded_input["input_ids"])
```

```python
[101, 1188, 1110, 170, 1505, 1505, 1505, 1505, 1505, 1505, 1505, 1505, ... 1505, 1505, 1505, 1179, 5650, 119, 102]
```

# Tokenizer Example

As we'll see in some examples below, this method is very powerful. First, it can tokenize a single sequence:

```python
sequence = "I've been waiting for a HuggingFace course my whole life."

model_inputs = tokenizer(sequence)
```

It also handles multiple sequences at a time, with no change in the API:

```python
sequences = ["I've been waiting for a HuggingFace course my whole life.", "So have I!"]

model_inputs = tokenizer(sequences)
```

It can pad according to several objectives:

```python
# Will pad the sequences up to the maximum sequence length
model_inputs = tokenizer(sequences, padding="longest")

# Will pad the sequences up to the model max length
# (512 for BERT or DistilBERT)
model_inputs = tokenizer(sequences, padding="max_length")

# Will pad the sequences up to the specified max length
model_inputs = tokenizer(sequences, padding="max_length", max_length=8)
```

It can also truncate sequences:

```python
sequences = ["I've been waiting for a HuggingFace course my whole life.", "So have I!"]

# Will truncate the sequences that are longer than the model max length
# (512 for BERT or DistilBERT)
model_inputs = tokenizer(sequences, truncation=True)

# Will truncate the sequences that are longer than the specified max length
model_inputs = tokenizer(sequences, max_length=8, truncation=True)
```

The tokenizer object can handle the conversion to specific framework tensors, which can then be directly sent to the model. For example, in the following code sample we are prompting the tokenizer to return tensors from the different frameworks — "pt" returns PyTorch tensors and "np" returns NumPy arrays:

```python
sequences = ["I've been waiting for a HuggingFace course my whole life.", "So have I!"]

# Returns PyTorch tensors
model_inputs = tokenizer(sequences, padding=True, return_tensors="pt")

# Returns NumPy arrays
model_inputs = tokenizer(sequences, padding=True, return_tensors="np")
```

## Special Tokens

If we take a look at the input IDs returned by the tokenizer, we will see they are a tiny bit different from what we had earlier:

```python
sequence = "I've been waiting for a HuggingFace course my whole life."

model_inputs = tokenizer(sequence)
print(model_inputs["input_ids"])

tokens = tokenizer.tokenize(sequence)
ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)
```

```python
[101, 1045, 1005, 2310, 2042, 3403, 2005, 1037, 17662, 12172, 2607, 2026, 2878, 2166, 1012, 102]
[1045, 1005, 2310, 2042, 3403, 2005, 1037, 17662, 12172, 2607, 2026, 2878, 2166, 1012]
```

One token ID was added at the beginning, and one at the end. Let’s decode the two sequences of IDs above to see what this is about:

```python
print(tokenizer.decode(model_inputs["input_ids"]))
print(tokenizer.decode(ids))
```

```python
"[CLS] i've been waiting for a huggingface course my whole life. [SEP]"
"i've been waiting for a huggingface course my whole life."
```

The tokenizer added the special word `[CLS]` at the beginning and the special word `[SEP]` at the end.

## 🧩 **Steps to Preprocess a Sentence Pair Dataset for BERT**

---

### **Step 1️⃣ — Load the Tokenizer**

Load a pretrained tokenizer that matches your model checkpoint.  
This tokenizer will convert your text into numerical tokens the model understands.

```python
from transformers import AutoTokenizer

checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
```

---

### **Step 2️⃣ — Tokenize Sentences Individually (Optional)**

You can tokenize each sentence separately to inspect how tokenization works.

```python
tokenized_sentences_1 = tokenizer(raw_datasets["train"]["sentence1"])
tokenized_sentences_2 = tokenizer(raw_datasets["train"]["sentence2"])
```

💡 _This helps you understand how the tokenizer processes single sentences, but it’s not how you’ll feed data into the model._

---

### **Step 3️⃣ — Tokenize a Pair of Sentences Together**

BERT expects sentence pairs in a specific format:

```
[CLS] sentence1 [SEP] sentence2 [SEP]
```

You can tokenize two sentences at once like this:

```python
inputs = tokenizer("This is the first sentence.", "This is the second one.")
print(inputs)
```

Example output:

```python
{
  'input_ids': [...],
  'token_type_ids': [...],
  'attention_mask': [...]
}
```

---

### **Step 4️⃣ — Understand the Tokenization Output**

- **`input_ids`** → numerical IDs for each token
    
- **`attention_mask`** → 1 for real tokens, 0 for padding
    
- **`token_type_ids`** → 0 for tokens from the first sentence, 1 for the second
    

If you decode `input_ids`, you’ll see:

```python
tokenizer.convert_ids_to_tokens(inputs["input_ids"])
# ['[CLS]', 'this', 'is', 'the', 'first', 'sentence', '.', '[SEP]', 'this', 'is', 'the', 'second', 'one', '.', '[SEP]']
```

And the **token_type_ids** will align like this:

```
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
```

---

### **Step 5️⃣ — Apply Tokenization to the Whole Dataset**

Now that the tokenizer can handle pairs, you can tokenize all pairs at once:

```python
tokenized_dataset = tokenizer(
    raw_datasets["train"]["sentence1"],
    raw_datasets["train"]["sentence2"],
    padding=True,
    truncation=True,
)
```

⚠️ **Note:**  
This returns a dictionary (not a dataset) and requires enough RAM to hold everything — not ideal for large datasets.

---

### **Step 6️⃣ — Define a Tokenization Function**

To keep your dataset efficient and on-disk, define a function that tokenizes each example:

```python
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
```

---

### **Step 7️⃣ — Apply Tokenization Using `.map()`**

Use the 🤗 Datasets `map()` method to apply your tokenization function to all splits.  
This adds new fields (`input_ids`, `attention_mask`, `token_type_ids`) to each dataset split.

```python
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
```

Example result:

```python
DatasetDict({
    train: Dataset({
        features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
        num_rows: 3668
    }),
    validation: Dataset({
        features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
        num_rows: 408
    }),
    test: Dataset({
        features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
        num_rows: 1725
    })
})
```

💡 Use `batched=True` for faster preprocessing.  
Optionally, you can add `num_proc` for multiprocessing when not using a fast tokenizer.

---

### **Step 8️⃣ — Use Dynamic Padding When Batching**

Don’t pad the dataset during tokenization. Instead, pad dynamically when creating batches.  
This saves memory by padding only to the longest sequence _within each batch_, not the entire dataset.

```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```

---

## ✅ **Summary of the Full Workflow**

|Step|Action|Purpose|
|---|---|---|
|1|Load pretrained tokenizer|Initialize preprocessing tool|
|2|(Optional) Tokenize individually|Inspect single sentence tokenization|
|3|Tokenize pairs|Match BERT input format|
|4|Understand outputs|Learn how IDs, masks, and types work|
|5|Tokenize dataset (simple way)|Test on full dataset (in-memory)|
|6|Define tokenize function|Prepare reusable function|
|7|Use `map()` with batching|Efficient preprocessing|
|8|Apply dynamic padding|Memory-efficient batching|

---

Here is a short summary recapping what you need:

```python
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding

raw_datasets = load_dataset("glue", "mrpc")
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)

tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```