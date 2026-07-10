- Binary search is an algorithm; its input is a sorted list of elements (I’ll explain later why it needs to be sorted). 
- If an element you’re looking for is in that list, binary search returns the position where it’s located. Otherwise, binary search returns null.
- With each step of binary search, you cut the number of words in half until you’re left with only one word
- Binary Search takes O(log2 n steps).
- Simple Search takes O(n) steps.
- Logs are the flip of exponentials.
- 10^2 = log10 (100)
- log always means log2

```python 
low = 0
high = len(list) - 1
```

each time, you check the middle element:
```python
mid = (low + high) / 2
guess = list[mid]
#mid is rounded by python automatically not done in other languages.
```

the whole code
```python
def binary_search(list,item):
	#low and high keep track of which part of the list you'll search in.
	low = 0
	high = len(list) - 1
#while you haven't narrowed it down to one element
	while low <= high:
		mid = (low+high) / 2 #check the middle element
		guess = list[mid]
	if guess == mid: #found the item
		retrun mid
	if guess > item: #the guess was too high
		high = mid -1 
	else: #the guess was too low.
		low = mid + 1
	return None
```

- O notation lets you compare the number of operations. It tells you how fast the algorithm grows.
- O(log n), also known as log time. Example: Binary search.
- O(n), also known as linear time. Example: Simple search.