```python
model_name='google/flan-t5-base'

original_model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)

tokenizer = AutoTokenizer.from_pretrained(model_name)
```

```python
def tokenize_function(example):
    start_prompt = 'Summarize the following conversation.\n\n'
    end_prompt = '\n\nSummary: '
    prompt = [start_prompt + dialogue + end_prompt for dialogue in example["dialogue"]]
    example['input_ids'] = tokenizer(prompt, padding="max_length", truncation=True, return_tensors="pt").input_ids
    example['labels'] = tokenizer(example["summary"], padding="max_length", truncation=True, return_tensors="pt").input_ids
    
    return example

# The dataset actually contains 3 diff splits: train, validation, test.
# The tokenize_function code is handling all data across all splits in batches.
tokenized_df = df.map(tokenize_function, batched=True)
tokenized_df = tokenized_df.remove_columns(['id', 'topic', 'dialogue', 'summary',])
```

```python
from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    r=32, # Rank
    lora_alpha=32,
    target_modules=["q", "v"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.SEQ_2_SEQ_LM # FLAN-T5
)
```

```python
peft_model = get_peft_model(original_model,
                            lora_config)

print(print_number_of_trainable_model_parameters(peft_model))
```

```python
output_dir = f'./dialogue-summary-training-{str(int(time.time()))}'
peft_training_args = TrainingArguments(
    output_dir=output_dir,
    auto_find_batch_size=True,
    learning_rate=1e-3,
    num_train_epochs=1,
    logging_steps=1,
    max_steps=1
    )

peft_trainer = Trainer(
    model=peft_model,
    args=peft_training_args,
    train_dataset=tokenized_df['train'],
    )
```

```python
peft_trainer.train()

peft_model_path ="./peft-dialogue-summary-checkpoint-local"

peft_trainer.model.save_pretrained(peft_model_path)
tokenizer.save_pretrained(peft_model_path)
```

```python
from peft import PeftModel, PeftConfig

peft_model_base = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base", torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
peft_model = PeftModel.from_pretrained(peft_model_base,
                                       peft_model_path,
                                       torch_dtype=torch.bfloat16,
                                       is_trainable=False)
```

```python
index = 200
dialogue = df['test'][index]['dialogue']
base_line_human_summary = df['test'][index]['summary']

prompt = f"""
Summarize the following conversation

{dialogue}

Summary:
"""

input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# Ensure that input_ids and the models are on the same device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
input_ids = input_ids.to(device)
original_model.to(device)
peft_model.to(device)

original_model_outputs = original_model.generate(input_ids=input_ids, generation_config=GenerationConfig(max_new_tokens=200, num_beams=1))
original_model_text_output = tokenizer.decode(original_model_outputs[0], skip_special_tokens=True)
print(original_model_text_output)

peft_model_outputs = peft_model.generate(input_ids=input_ids, generation_config=GenerationConfig(max_new_tokens=200, num_beams=1))
peft_model_text_output = tokenizer.decode(peft_model_outputs[0], skip_special_tokens=True)

print("=============================================")
print(f'BASELINE HUMAN SUMMARY: \n{base_line_human_summary}')
print("=============================================")
print(f'ORIGINAL MODEL: \n{original_model_text_output}')
print("=============================================")
print(f'PEFT MODEL: \n{peft_model_text_output}')
```

```python
dialogues = dialogsum_dataset['test'][0:10]['dialogue']
human_baseline_summaries = dialogsum_dataset['test'][0:10]['summary']
original_model_summaries = []
peft_model_summaries = []

for idx, dialogue in enumerate(dialogues):
  prompt = f"""
  summarize the following conversation
  {dialogue}
  Summary:

  """
  input_ids = tokenizer(prompt, return_tensors="pt").input_ids

  # Ensure that input_ids and the models are on the same device
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  input_ids = input_ids.to(device)

  human_baseline_text_output = human_baseline_summaries[idx]

  original_model_outputs = original_model.generate(input_ids=input_ids, generation_config=GenerationConfig(max_new_tokens=200, num_beams=1))
  original_model_text_output = tokenizer.decode(original_model_outputs[0], skip_special_tokens=True)
  original_model_summaries.append(original_model_text_output)

  peft_model_outputs = peft_model.generate(input_ids=input_ids, generation_config=GenerationConfig(max_new_tokens=200, num_beams=1))
  peft_model_text_output = tokenizer.decode(peft_model_outputs[0], skip_special_tokens=True)
  peft_model_summaries.append(peft_model_text_output)

zipped_summaries = list(zip(human_baseline_summaries, original_model_summaries,peft_model_summaries))

df = pd.DataFrame(zipped_summaries, columns=['human_baseline_summaries', 'original_model_summaries',"peft_model_summaries"])
df
```

```python
rouge = evaluate.load('rouge')

original_model_results = rouge.compute(
    predictions=original_model_summaries,
    references=human_baseline_summaries[0:len(original_model_summaries)],
    use_aggregator=True,
    use_stemmer=True,
)


peft_model_results = rouge.compute(
    predictions=peft_model_summaries,
    references=human_baseline_summaries[0:len(peft_model_summaries)],
    use_aggregator=True,
    use_stemmer=True,
)

print('ORIGINAL MODEL:')
print(original_model_results)
print('PEFT MODEL:')
print(peft_model_results)
```

```python
print("Absolute percentage improvement of PEFT MODEL over HUMAN BASELINE")

improvement = (np.array(list(peft_model_results.values())) - np.array(list(original_model_results.values())))

for key, value in zip(peft_model_results.keys(), improvement):

    print(f'{key}: {value*100:.2f}%')
```