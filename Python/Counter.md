---
description: "One snippet using collections.Counter and most_common(1) to get the mode of a list."
domain: cs
type: reference
status: stub
tags:
  - domain/cs
  - type/reference
  - status/stub
  - topic/python-language
aliases:
  - "mode"
  - "collections"
hubs:
  - "[[Python Language]]"
---
```python
from collections import Counter

data1 = [1, 2, 5, 10, -20, 5, 5]

def mode(data):
    count = Counter(data)  # Create a Counter object to count frequencies
    return count.most_common(1)[0][0]  # Return the most common element

```