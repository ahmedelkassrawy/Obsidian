## Map and Unordered Map Study Guide

## Overview

- **Map**: A container in C++ STL that stores key-value pairs in a sorted order based on keys.
- **Unordered Map**: A container that stores key-value pairs in an unsorted order, optimized for faster access.
- Both are part of the C++ Standard Template Library (STL) and require the `<map>` or `<unordered_map>` header.

## Key Features of Map

- **Ordered**: Keys are stored in a sorted order (based on a balanced binary search tree, typically a Red-Black Tree).
- **Unique Keys**: Each key is unique; duplicate keys are not allowed.
- **Time Complexity**: Most operations (insert, find, erase) are O(log n) due to the balanced tree structure.
- **Default Value**: If a key is accessed that doesn't exist, it is inserted with the default value of the value type (e.g., `0` for `double`).

### Example: Basic Map Usage

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, double> mp;
    int n;
    cin >> n;
    string name;
    double salary;

    // Insert key-value pairs
    for (int i = 0; i < n; i++) {
        cin >> name >> salary;
        mp[name] = salary;
    }

    // Access a key
    cin >> name;
    cout << mp[name] << endl; // Returns 0 if name not found (default for double)
}
```

**Note**: Accessing a non-existent key (`mp[name]`) inserts it with the default value of the second type (e.g., `0.0` for `double`).

## Searching in a Map

To avoid inserting a non-existent key, use `count` or `find` to check if a key exists.

### Using `count`

```cpp
cin >> name;
if (mp.count(name) == 0) {
    cout << "NOT FOUND" << endl;
} else {
    cout << mp[name] << endl;
}
```

- `count(name)`: Returns `1` if the key exists, `0` otherwise.
- Time Complexity: O(log n).

### Using `find`

```cpp
auto it = mp.find(name);
if (it == mp.end()) {
    cout << "NOT FOUND" << endl;
} else {
    cout << mp[name] << endl;
}
```

- `find(name)`: Returns an iterator to the key-value pair if found, or `mp.end()` if not.
- Time Complexity: O(log n).

## Printing a Map

Maps can be iterated in sorted order (by key) using a range-based for loop or an iterator.

### Using Range-Based For Loop

```cpp
for (pair<string, double> p : mp) {
    cout << p.first << " " << p.second << endl;
}
```

### Using Iterator

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<char, int> mp;
    mp['u'] = 9;
    mp['o'] = 0;
    mp['t'] = 1;

    for (auto itr = mp.begin(); itr != mp.end(); itr++) 
    {
        cout << itr->first << "," << itr->second << endl;
    }
}
```

**Output** (sorted by key):

```
o,0
t,1
u,9
```

## Erasing from a Map

Remove a key-value pair using `erase`.

```cpp
mp.erase("Ahmed");
```

- Time Complexity: O(log n).
- If the key doesn't exist, no action is taken.

## Map vs. Unordered Map

| **Feature**         | **Map**                                                            | **Unordered Map**                                               |
| ------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------- |
| **Order**           | Ordered (sorted by key, using a balanced tree)                     | Unordered (uses a hash table)                                   |
| **Data Structure**  | Balanced Binary Search Tree (e.g., Red-Black Tree)                 | Hash Table                                                      |
| **Time Complexity** | O(log n) for insert, find, erase                                   | O(1) average case for insert, find, erase; O(n) worst case      |
| **Sorting**         | Keys are automatically sorted                                      | No sorting, keys stored in arbitrary order                      |
| **Use Case**        | When order matters or frequent iteration in sorted order is needed | When fast access/insertion is priority and order doesn't matter |

### Example: Unordered Map

```cpp
#include <iostream>
#include <unordered_map>
#include <string>
using namespace std;

int main() {
    unordered_map<string, double> ump;
    ump["Alice"] = 50000;
    ump["Bob"] = 60000;

    for (const auto& p : ump) 
    {
        cout << p.first << ": " << p.second << endl;
    }
}
```

**Note**: Output order is not guaranteed (e.g., Bob might appear before Alice).

## Common Use Cases

- **Map**: Use when you need sorted keys or frequent iteration in order (e.g., displaying a leaderboard).
- **Unordered Map**: Use for fast lookups and insertions where order doesn't matter (e.g., caching or quick key-value storage).

## Tips for Studying

- Practice writing code to insert, search, and erase elements in both `map` and `unordered_map`.
- Experiment with different key and value types (e.g., `map<int, string>`, `unordered_map<string, int>`).
- Understand when to use `count` vs. `find` to avoid unintended insertions.
- Compare performance by timing operations with large datasets to see the O(log n) vs. O(1) difference.

## Additional Notes

- Always include necessary headers (`<map>` for `map`, `<unordered_map>` for `unordered_map`).
- Use `auto` for iterators to simplify code and avoid type errors.
- Be cautious with `mp[key]` as it modifies the map if the key doesn't exist.