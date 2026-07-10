In the DP paradigm, when we break down the larger problem into its smaller parts, those subproblems actually _overlap._
the DP paradigm finds the optimal solution for _every single subproblem_, and chooses the best option from all of the subproblems.
a DP algorithm will exhaustively search through all of the possible subproblems, and then choose the best solution based on that.
> Given the fact that the memoized version of Fibonacci needs to remember old subproblem solutions, the DP paradigm sacrifices some space in order to save time.

This is part of the tradeoff of using a dynamic programming approach,

1. How to recognize a DP problem
2. Identify problem variables
3. Clearly express the recurrence relation
4. Identify the base cases
5. Decide if you want to implement it iteratively or recursively
6. Add memoization
7. Determine time complexity
## 1. Fibonacci Sequence (Memoization)

This example calculates the Fibonacci sequence using memoization to avoid redundant calculations.

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 1e6 + 1;
int memo[N];

int f(int x) {
    if (x <= 1) return x; // Base case
    if (memo[x] != -1) return memo[x]; // Memoization
    int ans = f(x-1) + f(x-2);
    memo[x] = ans;
    return ans;
}

int main() {
    int n;
    cin >> n;
    memset(memo, -1, sizeof(memo));
    cout << f(n) << endl;
    return 0;
}
```

**Key Points**:

- **Base Case**: `x <= 1` returns `x`.
- **Memoization**: Stores results in `memo` array to avoid recomputation.
- **Time Complexity**: O(n) with memoization, compared to O(2^n) without.

## 2. Minimum Path Sum in Grid

This problem finds the minimum cost path from the top-left to the bottom-right of a grid, moving only right or down.

```cpp
#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;
int n, m;
vector<vector<int>> cost, dp;

int go(int x, int y) {
    if (x >= n || y >= m) return INF; // Out of bounds
    if (x == n - 1 && y == m - 1) return cost[x][y]; // Destination
    if (dp[x][y] != -1) return dp[x][y]; // Memoization
    int ch1 = go(x + 1, y); // Move down
    int ch2 = go(x, y + 1); // Move right
    return dp[x][y] = cost[x][y] + min(ch1, ch2);
}

int main() {
    cin >> n >> m;
    cost.assign(n, vector<int>(m));
    dp.assign(n, vector<int>(m, -1));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> cost[i][j];
    cout << go(0, 0) << endl;
    return 0;
}
```

**Key Points**:

- **Base Cases**: Out-of-bounds returns `INF`; destination returns cell cost.
- **Recurrence**: Minimum of moving down or right, plus current cell cost.
- **Time Complexity**: O(n * m).

## 3. Count Paths with Sum Constraint

This example counts the number of paths from top-left to bottom-right in a grid where the sum of costs does not exceed `max_sum`.

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 1001;
int cost[N][N], dp[N][N];
int n, m, max_sum;

int go(int x, int y, int sum) {
    if (sum > max_sum || x >= n || y >= m) return 0; // Invalid path
    if (x == n - 1 && y == m - 1) {
        sum += cost[x][y];
        return sum <= max_sum ? 1 : 0; // Valid path
    }
    if (dp[x][y] != -1) return dp[x][y]; // Memoization
    int ch1 = go(x + 1, y, sum + cost[x][y]); // Down
    int ch2 = go(x, y + 1, sum + cost[x][y]); // Right
    return dp[x][y] = ch1 + ch2;
}

int main() {
    cin >> n >> m >> max_sum;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> cost[i][j];
    memset(dp, -1, sizeof(dp));
    cout << go(0, 0, 0) << endl;
    return 0;
}
```

**Key Points**:

- **Base Case**: Invalid if sum exceeds `max_sum` or out of bounds; valid at destination if sum is within limit.
- **Recurrence**: Sum paths from moving down or right.
- **Time Complexity**: O(n * m).

## 4. Knapsack Problem

This is a classic 0/1 knapsack problem to maximize value within a weight constraint.

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 101;
int n, W, w[N], val[N];
int dp[N][N];

int go(int i, int weight) {
    if (weight > W) return INT_MIN; // Invalid
    if (i == n) return 0; // No more items
    if (dp[i][weight] != -1) return dp[i][weight]; // Memoization
    int ch1 = go(i + 1, weight); // Leave item
    int ch2 = go(i + 1, weight + w[i]) + val[i]; // Take item
    return dp[i][weight] = max(ch1, ch2);
}

int main() {
    cin >> n >> W;
    for (int i = 0; i < n; i++)
        cin >> w[i] >> val[i];
    memset(dp, -1, sizeof(dp));
    cout << go(0, 0) << endl;
    return 0;
}
```

**Key Points**:

- **Base Case**: Invalid if weight exceeds `W`; return 0 if no items remain.
- **Recurrence**: Choose maximum between taking or leaving the current item.
- **Time Complexity**: O(n * W).

## 5. Longest Common Subsequence (LCS) with Result Reconstruction

This example finds the longest common subsequence between two strings and reconstructs the result.

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 101;
string s, t, res;
int dp[N][N];

int go(int i, int j) {
    if (i >= s.size() || j >= t.size()) return 0; // Base case
    if (dp[i][j] != -1) return dp[i][j]; // Memoization
    if (s[i] == t[j])
        return dp[i][j] = go(i + 1, j + 1) + 1; // Take
    int ch1 = go(i + 1, j); // Leave s[i]
    int ch2 = go(i, j + 1); // Leave t[j]
    return dp[i][j] = max(ch1, ch2);
}

void build(int i, int j) {
    if (i >= s.size() || j >= t.size()) return;
    if (s[i] == t[j]) {
        res += s[i];
        build(i + 1, j + 1);
    } else {
        int ch1 = go(i + 1, j);
        int ch2 = go(i, j + 1);
        if (ch1 > ch2) build(i + 1, j);
        else build(i, j + 1);
    }
}

int main() {
    cin >> s >> t;
    memset(dp, -1, sizeof(dp));
    build(0, 0);
    cout << res << endl;
    return 0;
}
```

**Key Points**:

- **Base Case**: Return 0 if either string is exhausted.
- **Recurrence**: If characters match, include them; otherwise, take maximum of skipping either character.
- **Reconstruction**: Trace back decisions to build the result string.
- **Time Complexity**: O(|s| * |t|).
The build function does not reverse the go function. Instead, it uses the results of go (stored in the dp array or recomputed) to construct the LCS string. While go determines the length of the LCS, build translates those decisions into the actual sequence of characters. They work together to solve the LCS problem: go for computation, build for construction.

## 6. Queries with Sum Constraint

This example processes multiple queries to count paths in a grid with a sum constraint, using a starting point specified in each query.

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 1001;
int cost[N][N], dp[N][N];
int n, m, max_sum;

int go(int x, int y, int sum) {
    if (sum > max_sum || x >= n || y >= m) return 0; // Invalid
    if (x == n - 1 && y == m - 1) {
        sum += cost[x][y];
        return sum <= max_sum ? 1 : 0; // Valid
    }
    if (dp[x][y] != -1) return dp[x][y]; // Memoization
    int ch1 = go(x + 1, y, sum + cost[x][y]); // Down
    int ch2 = go(x, y + 1, sum + cost[x][y]); // Right
    return dp[x][y] = ch1 + ch2;
}

int main() {
    cin >> n >> m >> max_sum;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> cost[i][j];
    memset(dp, -1, sizeof(dp));
    int q;
    cin >> q;
    while (q--) {
        int x, y;
        cin >> x >> y;
        cout << go(x, y, 0) << endl;
    }
    return 0;
}
```

**Key Points**:

- **Queries**: Each query specifies a starting point `(x, y)`.
- **Memoization**: Reuses results for overlapping subproblems.
- **Time Complexity**: O(n * m * q) without memoization; memoization reduces redundant calculations.

## 7. Queries with Dynamic Sum Constraint

This variant allows `max_sum` to vary per query, using a 3D DP array to account for remaining sum.

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 1001;
int cost[N][N], dp[N][N][N];
int n, m;

int go(int x, int y, int rem) {
    if (rem < 0 || x >= n || y >= m) return 0; // Invalid
    if (x == n - 1 && y == m - 1) {
        rem -= cost[x][y];
        return rem >= 0 ? 1 : 0; // Valid
    }
    if (dp[x][y][rem] != -1) return dp[x][y][rem]; // Memoization
    int ch1 = go(x + 1, y, rem - cost[x][y]); // Down
    int ch2 = go(x, y + 1, rem - cost[x][y]); // Right
    return dp[x][y][rem] = ch1 + ch2;
}

int main() {
    cin >> n >> m;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> cost[i][j];
    memset(dp, -1, sizeof(dp));
    int q;
    cin >> q;
    while (q--) {
        int x, y, max_sum;
        cin >> x >> y >> max_sum;
        cout << go(x, y, max_sum) << endl;
    }
    return 0;
}
```

**Key Points**:

- **Dynamic Sum**: `max_sum` varies per query, requiring a 3D DP array.
- **Time Complexity**: O(n * m * max_sum * q) in worst case, mitigated by memoization.
- **Space Complexity**: O(n * m * max_sum).

## Summary

These examples illustrate common DP patterns:

- **Memoization**: Avoids redundant calculations (Fibonacci, all examples).
- **Grid-Based DP**: Solves path problems (Minimum Path Sum, Count Paths).
- **Knapsack**: Optimizes choices under constraints (Knapsack Problem).
- **Result Reconstruction**: Builds solutions from DP table (LCS).
- **Query Handling**: Adapts DP for multiple inputs (Queries).

Each example uses a top-down approach with memoization, but they can be converted to bottom-up DP for potentially better space efficiency.