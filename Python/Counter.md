```python
from collections import Counter

data1 = [1, 2, 5, 10, -20, 5, 5]

def mode(data):
    count = Counter(data)  # Create a Counter object to count frequencies
    return count.most_common(1)[0][0]  # Return the most common element

```