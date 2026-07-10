all vectors + push_front() + pop_front()
double ended queue (mftoo7 mn n7yteen)
![[Pasted image 20240604174858.png]]

```C++
// C++ program to demonstrate the
// working of deque
#include <bits/stdc++.h>
using namespace std;

// Driver Code
int main()
{
	// Declare a deque
	deque<int> dq;

	// Insert element in the front
	dq.push_front(10);
	dq.push_front(5);
	dq.push_front(3);

	// Delete elements from the front
	dq.pop_front();
	dq.pop_front();

	// Insert elements in the back
	dq.push_back(1);
	dq.push_back(50);
	dq.push_back(2);

	// Delete elements from the back
	dq.pop_back();
	dq.pop_back();

	cout << "Elements in deque are: ";

	// Print the element stored
	// in deque
	while (!dq.empty()) {
		cout << " " << dq.front();
		dq.pop_front();
	}

	return 0;
}

```

- max_size(): Returns the maximum number of elements deque can contain.
- push_front( ) push the elements into a deque from the front
- push_back( ) push elements into a deque from the back.
- pop_front() function is used to pop elements from a deque from the front and pop_back( ) function is used to pop elements from a deque from the back
- - clear() and erase():  clear is used to remove all the elements from the deque and erase is used to remove some specified elements.
- - insert(): increases the container side by inserting element in the specified position.
- resize(): changes the size of the element’s container as per requirement.