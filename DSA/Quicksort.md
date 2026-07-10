- Quicksort uses divide-and-conquer.
- here’s how D&C works:
- 1. Figure out a simple case as the base case. 
- 2. Figure out how to reduce your problem and get to the base case.
- quicksort to sort an array. What’s the simplest array that a sorting algorithm can handle (remember my tip from the previous section)? Well, some arrays don’t need to be sorted at all.
- then base case is array with 1 element or empty.
```python
def quicksort(array): 
	if len(array) < 2: 
		return array
```

## How quicksort works
1. First, pick an element from the array. This element is called the pivot.
2. Now find the elements smaller than the pivot and the elements larger than the pivot.
3. ![[Pasted image 20240423230435.png]]
4. Call quicksort recursively on the two sub-arrays.

![[Pasted image 20240423230725.png]]
```python
def quicksort(array):
	if len(array) < 2:
		return array
	else:
		pivot =array[0]
		less = [i for i in array[1:] if i<=pivot]

		greater =[i for i in array[i:] if i> pivot]

		retrun quicksort(less) + [pivot] + quicksort(greater)


```