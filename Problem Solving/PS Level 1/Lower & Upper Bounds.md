## Overview

In C++, `lower_bound` and `upper_bound` are algorithms from the `<algorithm>` library used to find positions of elements in a sorted range (e.g., a vector). They are particularly useful for binary search operations on sorted data.

## Key Functions

### `lower_bound(begin, end, x)`

- **Returns**: An iterator to the **first element** in the range `[begin, end)` that is **not less than** `x` (i.e., `>= x`).
- **Use Case**: Finds the first position where `x` could be inserted without violating the sorted order.

### `upper_bound(begin, end, x)`

- **Returns**: An iterator to the **first element** in the range `[begin, end)` that is **greater than** `x` (i.e., `> x`).
- **Use Case**: Finds the first position after all occurrences of `x`.

## Converting Iterators to Indices

Both functions return iterators. To get the **index** in a container (e.g., a vector), subtract the starting iterator:

```cpp
index = iterator - container.begin()
```

## Example

Consider a sorted vector:

```cpp
vector<int> avengers = {1, 3, 5, 7, 8};
int l = 3; // Lower bound value
int r = 7; // Upper bound value
```

### Step-by-Step

1. **Lower Bound**:
    
    ```cpp
    auto left = lower_bound(avengers.begin(), avengers.end(), l) - avengers.begin();
    // Points to 3 (value >= 3) → index = 1
    ```
    
2. **Upper Bound**:
    
    ```cpp
    auto right = upper_bound(avengers.begin(), avengers.end(), r) - avengers.begin();
    // Points to 8 (value > 7) → index = 4
    ```
    
3. **Count Elements in Range `[l, r]`**:
    
    ```cpp
    long long num_avengers = right - left; // 4 - 1 = 3
    ```
    
    - Elements in range `[3, 7]`: `{3, 5, 7}` (3 elements).

## Key Notes

- **Precondition**: The range must be **sorted** in ascending order.
- **Time Complexity**: `O(log n)` for random-access iterators (e.g., vectors).
- **Usage**: Ideal for finding ranges, counting occurrences, or determining insertion points in sorted containers.

## Practical Application

To count elements in a range `[l, r]` in a sorted vector:

```cpp
#include <vector>
#include <algorithm>
using namespace std;

vector<int> avengers = {1, 3, 5, 7, 8};
int l = 3, r = 7;

long long left = lower_bound(avengers.begin(), avengers.end(), l) - avengers.begin();
long long right = upper_bound(avengers.begin(), avengers.end(), r) - avengers.begin();
long long count = right - left; // 3 elements
```

This will include all elements `x` where `l <= x <= r`.

[[Binary Search.2]][[Binary Search]]