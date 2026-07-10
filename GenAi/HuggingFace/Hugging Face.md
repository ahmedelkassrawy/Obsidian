## Text Classification
1. Load the tokenizer, model
```python
# Load the tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
```

2. preprocess the input text
```python
# Sample text
text = "Congratulations! You've won a free ticket to the Bahamas. Reply WIN to claim."

# Tokenize the input text
inputs = tokenizer(text, return_tensors="pt")

print(inputs)
```

3. Perform Inference
```python
with torch.no_grad():
	outputs = model(**inputs)

#model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
```

4. Get the logits
```python
logits = output.logits
logits.shape
```

5. Convert the logits to probabilites and get the predicted class
```python
#Convert logits to prob
probs = torch.softmax(logits,dim = -1)

#get the predicted class
predicted_class = torch.argmax(probs, dim = -1)

#map the predicted class to the label
label = ["NEGATIVE","POSITIVE"]
predicted_label = labels[predicted_class]

print(predicted_label)
```

## Text Generation
```python
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
```

2. preprocess text
```python
#preprocess text
prompt = "Once upon a time"

inputs = tokenizer(prompt,
                   return_tensors = "pt")
inputs
```

3. Perform Inference 
- inputs
- attention mask
- pad_token_id
- max_length
- num_return_sequence

```python
#Generate text

output_ids = model.generate(
    inputs.input_ids,
    attention_mask = inputs.attention_mask,
    pad_token_id = tokenizer.eos_token_id,
    max_length = 50,
    num_return_sequences = 1
)

output_ids
```

```python
with torch.no_grad():
  outputs = model(**inputs)

outputs
```

4. Output
```python
generated_text = tokenizer.decode(output_ids[0],
                                  skip_special_tokens = True)

print(generated_text)
```