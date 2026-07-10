To use the STL priority queue, include the `<queue>` header:

```cpp
#include <queue>
```

## 🔼 Max-Heap (Default Behavior)

By default, `std::priority_queue` operates as a **max-heap**, where the largest element is at the top:

```cpp
#include <iostream>
#include <queue>
using namespace std;

int main() {
    priority_queue<int> pq;

    pq.push(10);
    pq.push(5);
    pq.push(20);

    cout << "Top element: " << pq.top() << endl; // Output: 20 (maximum)
    pq.pop();

    cout << "Next top element: " << pq.top() << endl; // Output: 10
    return 0;
}
```

## 🔽 Min-Heap

To create a **min-heap** (smallest element at the top), use `std::greater<T>` as the comparator:

```cpp
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
    priority_queue<int, vector<int>, greater<int>> minHeap;

    minHeap.push(10);
    minHeap.push(5);
    minHeap.push(20);

    cout << "Top element: " << minHeap.top() << endl; // Output: 5 (minimum)
    return 0;
}
```

## 📦 With Custom Struct

For custom data types, define a comparison operator to create a **max-heap**:

```cpp
#include <queue>
#include <string>
using namespace std;

struct Task {
    int priority;
    string name;

    // Max-heap: higher priority first
    bool operator<(const Task& other) const {
        return priority < other.priority;
    }
};

int main() {
    priority_queue<Task> tasks;
    tasks.push({10, "Task 1"});
    tasks.push({20, "Task 2"});
    // Top: Task 2 (priority 20)
    return 0;
}
```

For a **min-heap with custom comparator**:

```cpp
#include <queue>
#include <string>
#include <vector>
using namespace std;

struct Task {
    int priority;
    string name;
};

struct Compare {
    bool operator()(const Task& a, const Task& b) {
        return a.priority > b.priority; // Min-heap: lower priority first
    }
};

int main() {
    priority_queue<Task, vector<Task>, Compare> minTasks;
    minTasks.push({10, "Task 1"});
    minTasks.push({5, "Task 2"});
    // Top: Task 2 (priority 5)
    return 0;
}
```

## 🔁 Common Methods

|Method|Description|Time Complexity|
|---|---|---|
|`push(x)`|Inserts element `x`|O(log n)|
|`pop()`|Removes the top element|O(log n)|
|`top()`|Returns the top element|O(1)|
|`empty()`|Checks if the queue is empty|O(1)|
|`size()`|Returns the number of elements|O(1)|

## 📝 Notes

- The STL `priority_queue` is built on top of a heap, using `std::vector` as the default underlying container.
- Use in Obsidian by copying this note into a `.md` file.
- Test the code in a C++ environment (e.g., VS Code, online compilers like Replit).
- For advanced use cases, consider custom comparators or alternative containers like `deque`.