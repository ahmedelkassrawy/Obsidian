- Arrays all your data is stored contiguously (right next to each other) in memory.
- Linked lists are great if you’re going to read all the items one at a time: you can read one item, follow the address to the next item, and so on. But if you’re going to keep jumping around, linked lists are terrible.
- Arrays are great if you want to read random elements, because you can look up any element in your array instantly.
- Selection sort bybda2 y4oof howa lrkm lb3do akbr as8r mno y7to mkan l2blo b3deen ytl3 wa7da hal lb3do akbr wla as8ar lw akbar kml llb3do.
- ****Selection sort**** is a simple and efficient sorting algorithm that works by repeatedly selecting the smallest (or largest) element from the unsorted portion of the list and moving it to the sorted portion of the list.

```python
def findSmallest(arr):
	smallest = arr[0]
	smallest_index = 0
	for i in range(1,len(arr)):
		if arr[i] < smallest:
			smallest =arr[i]
			smallest_index = i
	return smallest_index
	
def selectionSort(arr):
	newArr = []
	for i in range(len(arr)):
		smallest =findSmallest(arr)
		newArr.append(arr.pop(smallest))
	return newArr
```

```C++
#include <iostream>
#include <vector>

using namespace std;

void selectionSort(vector<int>& arr) 
{
    for(int i = 0; i < arr.size(); i++)
    {
        int smallestidx = i;

        for(int j = i + 1; j < arr.size();j++)
        {
            if(arr[j] < arr[smallestidx])
            {
                smallestidx = j;
            }
        }

        if(smallestidx != i)
        {
            swap(arr[i], arr[smallestidx]);
        }
    }

}

int main() 
{
    vector<int> numbers = {5, 2, 4, 6, 1, 3};
    selectionSort(numbers);

    cout << "Sorted array: ";
    for (int i : numbers)
    {
        cout << i << " ";
    }
    cout << endl;

    return 0;
}
```