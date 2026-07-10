### Backtracking Patterns
## Table of Contents

- [1. Subset Generation]
- [2. Permutations]
- [3. Combinations]
- [4. N-Queens]
- [5. Graph Coloring]
- [Study Tips]

## 1. Subset Generation

**Description**: Generate all possible subsets of a set (e.g., for `[1,2,3]`, output `[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]`).

**When to Use**: Problems requiring all possible combinations of elements, like finding subsets or powersets.

**Approach**:

- For each element, make two choices: include it or exclude it.
- Use recursion to build subsets, adding each element to the current subset or skipping it.
- Base case: When all elements are processed, add the current subset to the result.

**Example**: Generate all subsets of `[1,2,3]`.

```cpp
#include <iostream>
#include <vector>
using namespace std;

void subsets(vector<int>& nums, int idx, vector<int>& curr, vector<vector<int>>& result) {
    if (idx == nums.size()) {
        result.push_back(curr);
        return;
    }
    // Exclude current element
    subsets(nums, idx + 1, curr, result);
    // Include current element
    curr.push_back(nums[idx]);
    
    subsets(nums, idx + 1, curr, result);
    curr.pop_back(); // Backtrack
}

int main() {
    vector<int> nums = {1, 2, 3};
    vector<vector<int>> result;
    vector<int> curr;
    subsets(nums, 0, curr, result);
    for (const auto& subset : result) {
        cout << "[ ";
        for (int x : subset) cout << x << " ";
        cout << "]" << endl;
    }
    return 0;
}
```

**Output**:

```
[ ]
[ 1 ]
[ 2 ]
[ 1 2 ]
[ 3 ]
[ 1 3 ]
[ 2 3 ]
[ 1 2 3 ]
```

**Key Points**:

- Time Complexity: O(2^n), as each element has two choices.
- Space Complexity: O(n) for recursion stack.
- Backtracking occurs when we remove the element after exploring the include path.

```C++
//include 
subset.push_back(nums[idx]);
backtrack(nums, res, subset, idx + 1);

//exclude
subset.pop_back();
backtrack(nums, res, subset, idx + 1);
```

```C++
1 2 3 
1 2 
1 3 
1 
2 3 
2 
3 
```

```C++
//include 
backtrack(nums, res, subset, idx + 1);
subset.push_back(nums[idx]);

//exclude
backtrack(nums, res, subset, idx + 1);
subset.pop_back();
```

```C++
3 
2
2 3
1
1 3
1 2
1 2 3
```

## 2. Permutations

**Description**: Generate all possible arrangements of a set (e.g., for `[1,2,3]`, output `[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]`).

**When to Use**: Problems requiring all possible orderings, like arranging items or solving puzzles.

**Approach**:

- Swap elements to create different orderings or use a visited array to track used elements.
- Recurse to place each unused element in the current position.
- Backtrack by undoing swaps or marking elements as unused.
- Base case: When the permutation is complete, add it to the result.

**Example**: Generate all permutations of `[1,2,3]`.

```cpp
#include <iostream>
#include <vector>
using namespace std;

void permute(vector<int>& nums, int idx, vector<vector<int>>& result) 
{
    if (idx == nums.size()) 
    {
        result.push_back(nums);
        return;
    }
    for (int i = idx; i < nums.size(); i++) 
    {
        swap(nums[idx], nums[i]);
        
        permute(nums, idx + 1, result);
        
        swap(nums[idx], nums[i]); // Backtrack
    }
}

int main() 
{
    vector<int> nums = {1, 2, 3};
    
    vector<vector<int>> result;
    
    permute(nums, 0, result);
    
    for (const auto& perm : result) 
    {
        cout << "[ ";
        
        for (int x : perm) cout << x << " ";
        
        cout << "]" << endl;
    }
    return 0;
}
```

**Output**:

```
[ 1 2 3 ]
[ 1 3 2 ]
[ 2 1 3 ]
[ 2 3 1 ]
[ 3 2 1 ]
[ 3 1 2 ]
```

**Key Points**:

- Time Complexity: O(n!), as there are n! permutations.
- Space Complexity: O(n) for recursion stack.
- Swapping ensures each element is tried in each position exactly once.

## 3. Combinations

**Description**: Generate all possible combinations of k elements from a set (e.g., for `n=4, k=2`, output `[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]`).

**When to Use**: Problems requiring selections of a fixed size, like choosing teams or items.

**Approach**:

- Pick elements one by one, ensuring the combination size reaches k.
- Use an index to avoid duplicates and maintain order.
- Backtrack by removing the last element to try the next possibility.
- Base case: When k elements are selected, add the combination to the result.

**Example**: Find all combinations of 2 elements from `[1,2,3,4]`.

```cpp
#include <iostream>
#include <vector>
using namespace std;

void combine(int n, int k, int start, vector<int>& curr, vector<vector<int>>& result) 
{
    if (curr.size() == k) 
    {
        result.push_back(curr);
        return;
    }
    for (int i = start; i <= n; i++) {
        curr.push_back(i);
        combine(n, k, i + 1, curr, result);
        curr.pop_back(); // Backtrack
    }
}

int main() {
    int n = 4, k = 2;
    
    vector<vector<int>> result;
    
    vector<int> curr;
    
    combine(n, k, 1, curr, result);
    
    for (const auto& comb : result) 
    {
        cout << "[ ";
        for (int x : comb) cout << x << " ";
        cout << "]" << endl;
    }
    return 0;
}
```

**Output**:

```
[ 1 2 ]
[ 1 3 ]
[ 1 4 ]
[ 2 3 ]
[ 2 4 ]
[ 3 4 ]
```

**Key Points**:

- Time Complexity: O(n choose k), the number of combinations.
- Space Complexity: O(k) for recursion stack.
- Using `start` ensures elements are picked in order, avoiding duplicates.

## 4. N-Queens

**Description**: Place N queens on an NxN chessboard such that no two queens threaten each other (no two queens share the same row, column, or diagonal).

**When to Use**: Problems involving constraint satisfaction, like placing objects with restrictions.

**Approach**:

- Place one queen per row, trying each column.
- Check if the placement is safe (no conflicts in columns or diagonals).
- Recurse to the next row; backtrack if no valid placement is found.
- Base case: When all queens are placed, record the solution.

**Example**: Solve the 4-Queens problem.

```cpp
#include <iostream>
#include <vector>
using namespace std;

bool isSafe(vector<vector<int>>& board, int row, int col, int n) {
    // Check column
    for (int i = 0; i < row; i++)
        if (board[i][col]) return false;
    // Check upper-left diagonal
    for (int i = row, j = col; i >= 0 && j >= 0; i--, j--)
        if (board[i][j]) return false;
    // Check upper-right diagonal
    for (int i = row, j = col; i >= 0 && j < n; i--, j++)
        if (board[i][j]) return false;
    return true;
}

void solveNQueens(vector<vector<int>>& board, int row, int n, vector<vector<string>>& result) {
    if (row == n) {
        vector<string> solution;
        for (int i = 0; i < n; i++) {
            string s;
            for (int j = 0; j < n; j++)
                s += board[i][j] ? "Q" : ".";
            solution.push_back(s);
        }
        result.push_back(solution);
        return;
    }
    for (int col = 0; col < n; col++) {
        if (isSafe(board, row, col, n)) {
            board[row][col] = 1;
            solveNQueens(board, row + 1, n, result);
            board[row][col] = 0; // Backtrack
        }
    }
}

int main() {
    int n = 4;
    vector<vector<int>> board(n, vector<int>(n, 0));
    vector<vector<string>> result;
    solveNQueens(board, 0, n, result);
    for (const auto& solution : result) {
        for (const auto& row : solution)
            cout << row << endl;
        cout << endl;
    }
    return 0;
}
```

**Output**:

```
.Q..
...Q
Q...
..Q.

..Q.
Q...
...Q
.Q..
```

**Key Points**:

- Time Complexity: O(n!), as each queen placement reduces choices.
- Space Complexity: O(n²) for the board.
- The `isSafe` check ensures constraints are met before proceeding.

## 5. Graph Coloring

**Description**: Assign colors to vertices of a graph such that no adjacent vertices share the same color, using at most m colors.

**When to Use**: Problems involving scheduling or resource allocation with conflicts, like coloring maps or assigning frequencies.

**Approach**:

- Assign a color to a vertex and check if it’s valid (no adjacent vertices have the same color).
- Recurse to the next vertex; backtrack if no color works.
- Base case: When all vertices are colored, the solution is valid.

**Example**: Color a graph with 3 vertices and edges `{(0,1), (1,2), (2,0)}` using 3 colors.

```cpp
#include <iostream>
#include <vector>
using namespace std;

bool isSafe(vector<vector<int>>& graph, vector<int>& colors, int v, int c, int n) {
    for (int i = 0; i < n; i++)
        if (graph[v][i] && colors[i] == c) return false;
    return true;
}

bool graphColoring(vector<vector<int>>& graph, int m, int v, vector<int>& colors, int n) {
    if (v == n) return true;
    for (int c = 1; c <= m; c++) {
        if (isSafe(graph, colors, v, c, n)) {
            colors[v] = c;
            if (graphColoring(graph, m, v + 1, colors, n)) return true;
            colors[v] = 0; // Backtrack
        }
    }
    return false;
}

int main() {
    int n = 3, m = 3;
    vector<vector<int>> graph = {{0, 1, 1}, {1, 0, 1}, {1, 1, 0}};
    vector<int> colors(n, 0);
    if (graphColoring(graph, m, 0, colors, n)) {
        cout << "Solution exists: ";
        for (int i = 0; i < n; i++)
            cout << "Vertex " << i << ": Color " << colors[i] << endl;
    } else {
        cout << "No solution exists" << endl;
    }
    return 0;
}
```

**Output**:

```
Solution exists: 
Vertex 0: Color 1
Vertex 1: Color 2
Vertex 2: Color 3
```

**Key Points**:

- Time Complexity: O(m^n), as each vertex tries m colors.
- Space Complexity: O(n) for the color array.
- The `isSafe` function checks constraints before assigning a color.

## 6. Counting Ways

```C++
#include <iostream>
using namespace std;

int printS(int idx, int sum, int target, int arr[], int n) {
    // Base case
    if(idx == n) 
    {
        if(sum == target) return 1;  // Valid subset found
        return 0;                // Invalid subset
    }

    // Include current element
    sum += arr[idx];
    int ch1 = printS(idx + 1, sum, target, arr, n);

    sum -= arr[idx];
    int ch2 = printS(idx + 1, sum, target, arr, n);

    return ch1 + ch2;
}

int main() {
#ifndef ONLINE_JUDGE
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
#endif

    int arr[] = {1, 2, 1};
    int n = 3;
    int target = 2;

    cout << printS(0, 0, target, arr, n) << endl;

    return 0;
}

```

## Study Tips

- **Recognize Patterns**: Identify if the problem involves generating all possibilities (subsets, permutations), selecting a fixed number (combinations), or satisfying constraints (N-Queens, graph coloring).
- **Understand Base Cases**: The recursion stops when a solution is found (e.g., all elements processed) or constraints are met.
- **Master Backtracking**: Practice undoing changes (e.g., popping elements, resetting board) to explore other paths.
- **Use Small Inputs**: Test with small cases (e.g., n=2) to trace recursion and backtracking steps.
- **Optimize with Pruning**: Skip invalid paths early (e.g., `isSafe` checks) to reduce time.
- **Link to Recursion**: Backtracking builds on recursion, as seen in your factorial example. The stack unwinds similarly, but backtracking explores multiple paths.
- **Practice Problems**: Try LeetCode problems like "Subsets," "Permutations," "Combinations," "N-Queens," and "Graph Coloring" to reinforce patterns.

### General Rule for Placement

- **Place push_back() before the recursive call** for the path where the element is included, so the recursive call sees the updated state.
- **Place pop_back() after the recursive call** to undo the change only after the path is fully explored, ensuring the state is clean for other paths.


**Related Notes**:

- [[Recursion Notes]] (for base cases and stack mechanics)
- [[Dynamic_Programming_Notes]] (for contrast with backtracking)