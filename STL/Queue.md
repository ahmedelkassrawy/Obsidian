![[Pasted image 20240604174738.png]]
**Functions:**

- [empty()](https://www.geeksforgeeks.org/queueempty-queuesize-c-stl/): Tests whether the queue is empty.
- [size()](https://www.geeksforgeeks.org/queueempty-queuesize-c-stl/): Returns the unsigned int, size of the queue.
- [queue::front() and queue::back()](https://www.geeksforgeeks.org/queuefront-queueback-c-stl/): front() function returns a reference to the first element or the oldest of the queue. back() function returns a reference to the last or the newest element of the queue.
- [push(k) and pop()](https://www.geeksforgeeks.org/queuepush-and-queuepop-in-cpp-stl/): push() function adds the element ‘k’ at the end of the queue. pop() function deletes the element from the beginning of the queue and reduces its size by 1.
- [swap()](https://www.geeksforgeeks.org/queue-swap-cpp-stl/): exchanges two queues with each other 
```C++
queue<int> q;
queue<int> p;
q.swap(p);
```
- [emplace()](https://www.geeksforgeeks.org/queueemplace-c-stl/): it is used to insert a new element at end of the queue

I believe the difference meant to be conveyed between “**push**” and “**emplace**” is the difference between “**moving an object to a location**” and “**constructing an object at a location**.”

```C++
queue <data_type> q
```
```C++
// C++ program to demonstrate the
// working of queue
#include <bits/stdc++.h>
using namespace std;

// Driver Code
int main()
{
	// Declare a queue
	queue<int> q;

	// Insert elements in the queue
	q.push(10);
	q.push(5);
	q.push(15);
	q.push(1);

	// Delete elements from the queue
	q.pop();
	q.pop();

	cout << "Elements in Queue are: ";

	// Print the element stored
	// in queue
	while (!q.empty()) {
		cout << q.front() << ' ';

		// Pop the front element
		q.pop();
	}

	return 0;
}

```