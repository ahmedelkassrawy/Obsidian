## Key Characteristics of Linked Lists

- **Memory Usage**:
    - Each node in a linked list stores:
        - An **integer data value**.
        - An **address field** pointing to the next node.
    - This structure requires **more memory** compared to simple integer storage due to the additional address field.
        
- **Data Access**:
    - Accessing an arbitrary data item is **cumbersome and time-consuming**.
    - Traversal from the head node is required to reach a specific element, unlike arrays with direct index-based access.

_(Reference: Diagram [Pasted image 20251007202049.png] - Likely illustrates a linked list node structure with data and address fields.)_
## Types of Linked Lists

Linked lists are categorized into three main types:
1. **Singly Linked List**:
    - Each node contains data and a single pointer to the next node.
    - Traversal is unidirectional (forward only).
    - Simplest structure, efficient for sequential access.
2. **Doubly Linked List**:
    - Each node contains data, a pointer to the next node, and a pointer to the previous node.
    - Allows bidirectional traversal.
    - Requires more memory due to the additional pointer.
3. **Circular Linked List**:
    - The last node connects back to the first node, forming a loop.
    - Can be singly or doubly linked.
    - Useful for applications requiring cyclic traversal.
# Singly Linked List

A singly linked list is a collection of nodes where each node contains data and a pointer to the next node. The list starts from the head node.

## Basic Structure in C++
```cpp
struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

class SinglyLinkedList {
public:
    Node* head;
    SinglyLinkedList() : head(nullptr) {}

    // Other methods will be added below
};
```

## Traversing the List
Traversal involves visiting each node from head to tail.

**Code:**
```cpp
void traverse() {
    Node* current = head;
    while (current != nullptr) {
        std::cout << current->data << " ";
        current = current->next;
    }
    std::cout << std::endl;
}
```

**Time Complexity:** O(n), where n is the number of nodes.

## Inserting an Item
### Inserting at the Beginning (Before Head)
Create a new node and set its next to current head, then update head.

**Code:**
```cpp
void insertAtBeginning(int val) {
    Node* newNode = new Node(val);
    newNode->next = head;
    head = newNode;
}
```

**Time Complexity:** O(1)

### Inserting at the End (After Tail)
Traverse to the last node and append the new node.

**Code:**
```cpp
void insertAtEnd(int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        return;
    }
    Node* current = head;
    while (current->next != nullptr) {
        current = current->next;
    }
    current->next = newNode;
}
```

**Time Complexity:** O(n) (traversal required; O(1) if maintaining a tail pointer)

### Inserting at the Middle (Random Location)
Assume insertion after a given position (1-based index).

**Code:**
```cpp
void insertAtPosition(int val, int position) {
    if (position < 1) return; // Invalid
    Node* newNode = new Node(val);
    if (position == 1) {
        newNode->next = head;
        head = newNode;
        return;
    }
    Node* current = head;
    for (int i = 1; i < position - 1 && current != nullptr; ++i) {
        current = current->next;
    }
    if (current == nullptr) return; // Position out of bounds
    newNode->next = current->next;
    current->next = newNode;
}
```

**Time Complexity:** O(n) in worst case (traversal to position)

## Deleting an Item
### Deleting the First Node
Update head to the next node and delete the old head.

**Code:**
```cpp
void deleteFirst() {
    if (head == nullptr) return;
    Node* temp = head;
    head = head->next;
    delete temp;
}
```

**Time Complexity:** O(1)

### Deleting the Last Node
Traverse to the second last node and set its next to nullptr.

**Code:**
```cpp
void deleteLast() {
    if (head == nullptr) return;
    if (head->next == nullptr) {
        delete head;
        head = nullptr;
        return;
    }
    Node* current = head;
    while (current->next->next != nullptr) {
        current = current->next;
    }
    delete current->next;
    current->next = nullptr;
}
```

**Time Complexity:** O(n)

### Deleting an Intermediate Node
Assume deletion at a given position (1-based).

**Code:**
```cpp
void deleteAtPosition(int position) {
    if (position < 1 || head == nullptr) return;
    if (position == 1) {
        deleteFirst();
        return;
    }
    Node* current = head;
    for (int i = 1; i < position - 1 && current != nullptr; ++i) {
        current = current->next;
    }
    if (current == nullptr || current->next == nullptr) return;
    Node* temp = current->next;
    current->next = current->next->next;
    delete temp;
}
```

**Time Complexity:** O(n)

# Doubly Linked List

A doubly linked list has nodes with pointers to both next and previous nodes.

## Basic Structure in C++
```cpp
struct DoublyNode {
    int data;
    DoublyNode* next;
    DoublyNode* prev;
    DoublyNode(int val) : data(val), next(nullptr), prev(nullptr) {}
};

class DoublyLinkedList {
public:
    DoublyNode* head;
    DoublyNode* tail;
    DoublyLinkedList() : head(nullptr), tail(nullptr) {}

    // Other methods similar to singly, but with prev links
};
```

## Traversing the List
Similar to singly, but can traverse forward or backward.

**Forward Traverse Code:**
```cpp
void traverseForward() {
    DoublyNode* current = head;
    while (current != nullptr) {
        std::cout << current->data << " ";
        current = current->next;
    }
    std::cout << std::endl;
}
```

**Time Complexity:** O(n)

## Inserting an Item
### At Beginning
Update head and prev/next links.

**Code:**
```cpp
void insertAtBeginning(int val) {
    DoublyNode* newNode = new DoublyNode(val);
    if (head == nullptr) {
        head = tail = newNode;
        return;
    }
    newNode->next = head;
    head->prev = newNode;
    head = newNode;
}
```

**Time Complexity:** O(1)

### At End
Use tail for O(1) insertion.

**Code:**
```cpp
void insertAtEnd(int val) {
    DoublyNode* newNode = new DoublyNode(val);
    if (tail == nullptr) {
        head = tail = newNode;
        return;
    }
    tail->next = newNode;
    newNode->prev = tail;
    tail = newNode;
}
```

**Time Complexity:** O(1) (with tail pointer)

### At Middle (Position)
Traverse to position and adjust links.

**Code:** (Similar to singly, but update prev too)
```cpp
void insertAtPosition(int val, int position) {
    if (position < 1) return;
    DoublyNode* newNode = new DoublyNode(val);
    if (position == 1) {
        insertAtBeginning(val);
        return;
    }
    DoublyNode* current = head;
    for (int i = 1; i < position - 1 && current != nullptr; ++i) {
        current = current->next;
    }
    if (current == nullptr) return;
    newNode->next = current->next;
    newNode->prev = current;
    if (current->next != nullptr) {
        current->next->prev = newNode;
    }
    current->next = newNode;
    if (newNode->next == nullptr) tail = newNode;
}
```

**Time Complexity:** O(n)

## Deleting an Item
### First Node
Update head and links.

**Code:**
```cpp
void deleteFirst() {
    if (head == nullptr) return;
    DoublyNode* temp = head;
    head = head->next;
    if (head != nullptr) head->prev = nullptr;
    else tail = nullptr;
    delete temp;
}
```

**Time Complexity:** O(1)

### Last Node
Use tail for O(1).

**Code:**
```cpp
void deleteLast() {
    if (tail == nullptr) return;
    DoublyNode* temp = tail;
    tail = tail->prev;
    if (tail != nullptr) tail->next = nullptr;
    else head = nullptr;
    delete temp;
}
```

**Time Complexity:** O(1)

### Intermediate Node
Traverse and adjust prev/next.

**Code:**
```cpp
void deleteAtPosition(int position) {
    if (position < 1 || head == nullptr) return;
    if (position == 1) {
        deleteFirst();
        return;
    }
    DoublyNode* current = head;
    for (int i = 1; i < position && current != nullptr; ++i) {
        current = current->next;
    }
    if (current == nullptr) return;
    if (current->prev != nullptr) current->prev->next = current->next;
    if (current->next != nullptr) current->next->prev = current->prev;
    if (current == head) head = current->next;
    if (current == tail) tail = current->prev;
    delete current;
}
```

**Time Complexity:** O(n)

# Circular Linked Lists (Singly)

In a circular singly linked list, the last node's next points back to the head.

## Basic Structure in C++
Use the same Node as singly, but last->next = head.

```cpp
class CircularSinglyList {
public:
    Node* head;
    CircularSinglyList() : head(nullptr) {}

    // Methods below
};
```

## Counting Nodes
Traverse until back to head.

**Code:**
```cpp
int countNodes() {
    if (head == nullptr) return 0;
    int count = 1;
    Node* current = head->next;
    while (current != head) {
        ++count;
        current = current->next;
    }
    return count;
}
```

**Time Complexity:** O(n)

## Printing the Contents
Traverse and print, stopping at head.

**Code:**
```cpp
void printContents() {
    if (head == nullptr) return;
    Node* current = head;
    do {
        std::cout << current->data << " ";
        current = current->next;
    } while (current != head);
    std::cout << std::endl;
}
```

**Time Complexity:** O(n)

## Inserting a Node at the End
Traverse to last, append, and link back to head.

**Code:**
```cpp
void insertAtEnd(int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        newNode->next = head;
        return;
    }
    Node* current = head;
    while (current->next != head) {
        current = current->next;
    }
    current->next = newNode;
    newNode->next = head;
}
```

**Time Complexity:** O(n)

## Inserting a Node at the Front
Insert as new head and update last's next.

**Code:**
```cpp
void insertAtFront(int val) {
    Node* newNode = new Node(val);
    if (head == nullptr) {
        head = newNode;
        newNode->next = head;
        return;
    }
    Node* current = head;
    while (current->next != head) {
        current = current->next;
    }
    newNode->next = head;
    current->next = newNode;
    head = newNode;
}
```

**Time Complexity:** O(n) (to find last)

## Deleting the Last Node
Traverse to second last, update to point to head, delete last.

**Code:**
```cpp
void deleteLast() {
    if (head == nullptr) return;
    if (head->next == head) {
        delete head;
        head = nullptr;
        return;
    }
    Node* current = head;
    while (current->next->next != head) {
        current = current->next;
    }
    Node* temp = current->next;
    current->next = head;
    delete temp;
}
```

**Time Complexity:** O(n)

# Circular Doubly Linked Lists

Similar to circular singly, but with prev links, and both head->prev = tail, tail->next = head.

## Basic Structure in C++
Use DoublyNode, with circular links.

```cpp
class CircularDoublyList {
public:
    DoublyNode* head;
    CircularDoublyList() : head(nullptr) {}

    // Assume similar methods as above, adapted for doubly
};
```

Operations like insert front/end, delete last are O(1) if maintaining tail, but since circular, head and tail are connected.

**Insert at Front Code Example:**
```cpp
void insertAtFront(int val) {
    DoublyNode* newNode = new DoublyNode(val);
    if (head == nullptr) {
        head = newNode;
        newNode->next = newNode->prev = head;
        return;
    }
    newNode->next = head;
    newNode->prev = head->prev;
    head->prev->next = newNode;
    head->prev = newNode;
    head = newNode;
}
```

**Time Complexity for Inserts/Deletes:** O(1) for front/end, O(n) for middle.

Other operations (count, print, delete last) similar to circular singly but with bidirectional traversal possible.

**Delete Last Code:**
```cpp
void deleteLast() {
    if (head == nullptr) return;
    if (head->next == head) {
        delete head;
        head = nullptr;
        return;
    }
    DoublyNode* last = head->prev;
    last->prev->next = head;
    head->prev = last->prev;
    delete last;
}
```

**Time Complexity:** O(1)

Traversal, counting: O(n)

# A Memory-efficient Doubly Linked List (XOR Linked List)

This uses XOR of pointers to store both prev and next in one field, saving memory. Each node has data and a 'both' field (intptr_t both = prev XOR next).

Navigation requires XOR with previous pointer.

## Basic Structure in C++
```cpp
struct XORNode {
    int data;
    XORNode* both; // XOR of prev and next
    XORNode(int val) : data(val), both(nullptr) {}
};

class XORDoublyList {
public:
    XORNode* head;
    XORDoublyList() : head(nullptr) {}

    // Special traversal/insert methods
};
```

## Why Use It?
Reduces memory usage by half for pointers (one instead of two). Useful in memory-constrained environments.

## Traversing
Need to keep track of previous.

**Code (Forward Traverse):**
```cpp
void traverse() {
    XORNode* current = head;
    XORNode* prev = nullptr;
    while (current != nullptr) {
        std::cout << current->data << " ";
        XORNode* next = reinterpret_cast<XORNode*>(reinterpret_cast<uintptr_t>(prev) ^ reinterpret_cast<uintptr_t>(current->both));
        prev = current;
        current = next;
    }
    std::cout << std::endl;
}
```

**Time Complexity:** O(n)

## Inserting (e.g., at End)
Adjust XOR links carefully.

**Code (Insert at Beginning):**
```cpp
void insertAtBeginning(int val) {
    XORNode* newNode = new XORNode(val);
    if (head == nullptr) {
        head = newNode;
        return;
    }
    newNode->both = head;
    head->both = reinterpret_cast<XORNode*>(reinterpret_cast<uintptr_t>(newNode) ^ reinterpret_cast<uintptr_t>(head->both));
    head = newNode;
}
```

Insertions/deletions are O(1) at ends, but middle requires traversal O(n). More complex due to XOR.

**Time Complexities:** Similar to doubly, but implementation trickier.

# Unrolled Linked Lists

An unrolled linked list stores multiple elements in each node (as an array), reducing pointer overhead and improving cache performance.

## Why Do We Need It?
Improves locality of reference for better cache hits, reduces memory for pointers, faster traversals for large lists.

## Basic Structure in C++
```cpp
const int NODE_CAPACITY = 10; // Example

struct UnrolledNode {
    int numElements;
    int elements[NODE_CAPACITY];
    UnrolledNode* next;
    UnrolledNode() : numElements(0), next(nullptr) {}
};

class UnrolledLinkedList {
public:
    UnrolledNode* head;
    UnrolledLinkedList() : head(nullptr) {}

    // Methods
};
```

## Search for an Element
Traverse nodes, then linear search within array.

**Code:**
```cpp
bool search(int val) {
    UnrolledNode* current = head;
    while (current != nullptr) {
        for (int i = 0; i < current->numElements; ++i) {
            if (current->elements[i] == val) return true;
        }
        current = current->next;
    }
    return false;
}
```

**Time Complexity:** O(n/k + k) worst case, where k is capacity (effectively O(n))

## Insert an Element
Insert into current node if space, else split or add new node.

**Code (Insert at End, Simplified):**
```cpp
void insert(int val) {
    if (head == nullptr) {
        head = new UnrolledNode();
        head->elements[0] = val;
        head->numElements = 1;
        return;
    }
    UnrolledNode* current = head;
    while (current->next != nullptr) {
        current = current->next;
    }
    if (current->numElements < NODE_CAPACITY) {
        current->elements[current->numElements++] = val;
    } else {
        UnrolledNode* newNode = new UnrolledNode();
        // Split: move half to newNode, but simplified here
        newNode->elements[0] = val;
        newNode->numElements = 1;
        current->next = newNode;
    }
}
```

**Time Complexity:** Amortized O(1) for end, O(n) worst for traversal.

## Performing Shift Operation
Shift means rotating elements left/right within the list.

**Code (Left Shift by 1, Simplified):**
Shift involves moving elements across nodes, potentially merging/splitting.

This is complex; time O(n) as need to traverse and adjust arrays.

**Time Complexity:** O(n)

# Skip Lists

A skip list is a probabilistic data structure for sorted elements, with multiple layers of linked lists for faster search (like a balanced tree).

## Why Use It?
Average O(log n) search/insert/delete, easier to implement than balanced trees, good for concurrent operations.

## Basic Structure in C++
Nodes have multiple forward pointers.

```cpp
const int MAX_LEVEL = 16;

struct SkipNode {
    int data;
    SkipNode* forward[MAX_LEVEL];
    SkipNode(int val) : data(val) {
        std::fill(forward, forward + MAX_LEVEL, nullptr);
    }
};

class SkipList {
public:
    SkipNode* head;
    int level;
    SkipList() : level(0) {
        head = new SkipNode(-1); // Sentinel
    }

    // Random level generator
    int randomLevel() {
        int lvl = 1;
        while (lvl < MAX_LEVEL && (rand() % 2 == 0)) ++lvl;
        return lvl;
    }

    // Other methods
};
```

## Search for an Element
Start from top level, move forward until overshoot, drop level.

**Code:**
```cpp
bool search(int val) {
    SkipNode* current = head;
    for (int i = level - 1; i >= 0; --i) {
        while (current->forward[i] != nullptr && current->forward[i]->data < val) {
            current = current->forward[i];
        }
    }
    current = current->forward[0];
    return (current != nullptr && current->data == val);
}
```

**Time Complexity:** O(log n) average

## Insert an Element
Find position like search, insert at random levels, update forwards.

**Code (Simplified):**
```cpp
void insert(int val) {
    SkipNode* update[MAX_LEVEL];
    SkipNode* current = head;
    for (int i = level - 1; i >= 0; --i) {
        while (current->forward[i] != nullptr && current->forward[i]->data < val) {
            current = current->forward[i];
        }
        update[i] = current;
    }
    int newLevel = randomLevel();
    if (newLevel > level) {
        for (int i = level; i < newLevel; ++i) {
            update[i] = head;
        }
        level = newLevel;
    }
    SkipNode* newNode = new SkipNode(val);
    for (int i = 0; i < newLevel; ++i) {
        newNode->forward[i] = update[i]->forward[i];
        update[i]->forward[i] = newNode;
    }
}
```

**Time Complexity:** O(log n) average

## Delete
Similar to insert, find and remove from all levels.

**Time Complexity:** O(log n) average

Note: All codes are illustrative; in practice, add error handling, destructors for memory cleanup.

---
### Double Linked List
```c++
#include <iostream>
using namespace std;

struct DoubleNode 
{
    int data;
    DoubleNode *next;
    DoubleNode *prev;

    DoubleNode(int val): data(val) , next(nullptr), prev(nullptr) {}    
};

class DoubleLinkedList 
{
    public:
        DoubleNode *head;
        DoubleNode *tail;
        DoubleLinkedList(): head(nullptr), tail(nullptr) {}

        void traverseForward()
        {
            DoubleNode *curr = head;

            while(curr != nullptr)
            {
                cout << curr->data << " ";
                curr = curr->next;
            }
            cout << endl;
        }

        void traverseBackward()
        {
            DoubleNode *curr = tail;
            while(curr != nullptr)
            {
                cout << curr->data << " ";
                curr = curr->prev;
            }
            cout << endl;
        }

        void insertAtBeginning(int val)
        {
            DoubleNode *temp = new DoubleNode(val);

            head -> prev = temp;
            temp -> next = head;
            head = temp;
        }

        void insertatEnd(int val)
        {
            DoubleNode *temp = new DoubleNode(val);

            tail -> next = temp;
            temp -> prev = tail;
            tail = temp;
        }

        void insertAtPosition(int val, int pos)
        {
            DoubleNode *temp = new DoubleNode(val);
            DoubleNode *curr = head;

            for(int i = 1; i < pos - 1;i++)
            {
                curr = curr -> next;
            }

            temp -> next = curr -> next;
            
            if(curr -> next != nullptr)
            {
                curr -> next -> prev = temp;
            }
            else
            {
                tail = temp;
            }
            curr -> next = temp;
            temp -> prev = curr;
        }

        void deleteatBeginning()
        {
            DoubleNode *temp = head;

            head = head -> next;
            head -> prev = nullptr;

            delete temp;
        }

        void deleteatEnd()
        {
            DoubleNode *temp = tail;

            tail = tail -> prev;
            tail -> next = nullptr;

            delete temp;
        }

        void deleteAtPosition(int pos)
        {
            DoubleNode *curr = head;

            for(int i = 1; i < pos - 1;i++)
            {
                curr = curr -> next;
            }

            DoubleNode *temp = curr -> next;
            curr -> next = temp -> next;
            temp -> next -> prev = curr;

            delete temp;
        }

        void deleteAtEnd()
        {
            DoubleNode *temp = tail;

            tail = tail -> prev;
            tail -> next = nullptr;

            delete temp;
        }

        ~DoubleLinkedList()
        {
            DoubleNode *curr = head;

            while(curr != nullptr)
            {
                DoubleNode *temp = curr -> next;
                delete curr;
                curr = temp;
            }
        }
};

int main()
{
    DoubleLinkedList dll;
    
    dll.head = new DoubleNode(10);

    //no tail still
    dll.tail = dll.head;
    
    dll.insertAtPosition(20,2);
    dll.insertAtPosition(80,3);
    dll.insertatEnd(25);

    dll.traverseForward();
    dll.traverseBackward();

    dll.deleteatBeginning();
    dll.traverseForward();

    dll.deleteatEnd();
    dll.traverseForward();
}
```

---
### Circular Single
```c++
#include <iostream>
using namespace std;

struct Node 
{
    int data;
    Node *next;

    Node(int val): data(val),next(nullptr) {};
};

class CircularSingleLinkedList
{
    public:
        Node *head;
        CircularSingleLinkedList(): head(nullptr) {}

    int countNodes()
    {
        if(head == nullptr) return 0;

        Node *curr = head;
        int cnt = 0;

        while(curr -> next != head)
        {
            cnt++;
            curr = curr -> next;
        }
        
        return cnt;
    }

    void printList()
    {
        Node *curr = head;

        while(curr -> next != head)
        {
            cout<< curr -> data << " ";
            curr = curr -> next;
        }

        cout<<endl;
    }

    void insertatEnd(int val)
    {
        Node *temp = new Node(val);

        if(head == nullptr)
        {
            head = temp;
            temp -> next = head;
        }
        else
        {
            Node *curr = head;

            while(curr -> next != head)
            {
                curr = curr -> next;
            }
            curr -> next = temp; //we are at head
            temp -> next = head; //point to head
        }
    }

    void deleteFirst()
    {
        Node *curr = head;

        while(curr -> next != head)
        {
            curr = curr -> next;
        }

        curr -> next = head -> next;
        delete head;
        head = curr;
    }

    ~CircularSingleLinkedList()
    {
        if(head == nullptr) return;

        Node *curr = head->next;

        while(curr != head)
        {
            Node *temp = curr->next;
            delete curr;
            curr = temp;
        }

        delete head;
    }
};

int main()
{
    CircularSingleLinkedList csll;

    csll.insertatEnd(10);
    csll.insertatEnd(20);
    csll.insertatEnd(30);
    csll.insertatEnd(40);

    csll.printList();

    cout << "Node count: " << csll.countNodes() << endl;

    csll.deleteFirst();
    csll.printList();

    cout << "Node count: " << csll.countNodes() << endl;

    return 0;
}
```

----
#### Circular Double
```c++
#include <iostream>
using namespace std;

struct Node
{
    int data;
    Node *next;
    Node *prev;

    Node(int val): data(val), next(nullptr), prev(nullptr) {}
};

class DoubleCircularLinkedList
{
    public:
        Node *head;
        DoubleCircularLinkedList(): head(nullptr) {}

    void insertatBeginning(int val)
    {
        Node *temp = new Node(val);

        if(head == nullptr)
        {
            head = temp;
            head -> next = head;
            head -> prev = head;
        }
        else
        {
            Node *tail = head -> prev;
            
            temp -> next = head;
            temp -> prev = tail;
            head -> prev = temp;
            tail -> next = temp;
            head = temp;
        }
    }

    void insertatEnd(int val)
    {
        Node *temp = new Node(val);

        if(head == nullptr)
        {
            head = temp;
            head -> next = head;
            head -> prev = head;
        }
        else
        {
            Node *tail = head -> prev;

            tail -> next = temp;
            temp -> prev = tail;
            temp -> next = head;
            head -> prev = temp;
        }
    }

    void printList()
    {
        Node *curr = head;

        while(curr -> next != head)
        {
            cout << curr -> data << " ";
            curr = curr -> next;
        }
        cout << curr -> data << endl;
    }

    void deleteatBeginning()
    {
        if(head == nullptr) return;

        Node *tail = head -> prev;
        Node *temp = head;

        head = head -> next;
        tail -> next = head;
        head -> prev = tail;

        delete temp;
    }

    void deleteAtEnd()
    {
        if(head == nullptr) return;

        Node *tail = head -> prev;
        Node *newTail = tail -> prev;

        newTail -> next = head;
        head -> prev = newTail;

        delete tail;
    }

};

int main()
{
    DoubleCircularLinkedList dcll;

    dcll.insertatEnd(10);
    dcll.insertatEnd(20);
    dcll.insertatBeginning(5);
    dcll.printList();

    dcll.deleteatBeginning();
    dcll.printList();

    dcll.deleteAtEnd();
    dcll.printList();

    return 0;
}
```