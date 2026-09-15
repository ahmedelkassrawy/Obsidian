---
description: "Two snippets for writing data to disk: dump a dict or list as JSON, and append to an existing JSON array while surviving a corrupted file."
domain: ai-eng
type: howto
status: raw
tags:
  - domain/ai-eng
  - type/howto
  - status/raw
  - topic/python-language
aliases:
  - "SW Notes"
  - "json.dump"
  - "append to json"
hubs:
  - "[[Python Language]]"
---
```python
if isinstance(data, (dict, list)):
	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(data, 
				  f, indent=2, 
				  ensure_ascii=False, default=str)
else:
	with open(file_path, 'w', encoding='utf-8') as f:
		f.write(str(data))
```

```python
 if isinstance(data, (dict, list)):
	existing_data = []
	if file_path.exists():
		try:
			with open(file_path, 'r',encoding = 'utf-8') as f:
				existing_data = json.load(f)

				if not isinstance(existing_data, list):
					existing_data = [existing_data]

		except json.JSONDecodeError:
			# file corrupted start fresh
			existing_data = []

	if isinstance(data, list):
		existing_data.extend(data)
	else:
		existing_data.append(data)

	with open(file_path,'w',encoding = 'utf-8') as f:
		json.dump(existing_data, f, indent=2, ensure_ascii=False, default=str)
else:
	with open(file_path,'a',encoding = 'utf-8') as f:
		f.write(str(data) + '\n')
```