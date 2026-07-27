[Sheet #5 | Recursion and Backtracking - Virtual Judge](https://vjudge.net/contest/669349#problem/P)

```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n, m, x; // Number of books, number of algorithms, minimum understanding level required

vector<int> cost; // Cost of each book
vector<vector<int>> skills; // Understanding levels each book contributes for each algorithm

// Recursive function to determine the minimum cost to achieve the objective
int f(int b, vector<int>& un) {
    if (b == n) { // Base case: All books have been considered
        bool f = true;

        // Check if all algorithm understanding levels meet or exceed the required level
        for (auto level : un) {
            if (level < x) f = false;
        }

        // If all levels are sufficient, return 0 (no additional cost required)
        if (f) return 0;

        // If not sufficient, return a large value to indicate infeasibility
        else return 1e9;
    }

    // Option 1: Do not take the current book
    int op1 = f(b + 1, un);

    // Add the skills from the current book to the current understanding levels
    for (int i = 0; i < m; i++) {
        un[i] += skills[b][i];
    }

    // Option 2: Take the current book and add its cost
    int op2 = cost[b] + f(b + 1, un);

    // Restore the original understanding levels (backtrack)
    for (int i = 0; i < m; i++) {
        un[i] -= skills[b][i];
    }

    // Return the minimum cost of the two options
    return min(op1, op2);
}

int main() {
    cin >> n >> m >> x; // Input number of books, algorithms, and required level

    cost.resize(n); // Resize the cost vector to store the cost of each book
    skills.resize(n, vector<int>(m)); // Resize the skills matrix to store contributions

    // Input the cost and skill contributions for each book
    for (int i = 0; i < n; i++) {
        cin >> cost[i]; // Cost of the book
        for (int j = 0; j < m; j++) {
            cin >> skills[i][j]; // Skill contributions for each algorithm
        }
    }

    vector<int> init(m); // Initialize a vector to track understanding levels for all algorithms

    int ans = f(0, init); // Start the recursive function from the first book

    // If the minimum cost is too large, print -1 (objective not achievable)
    if (ans >= 1e9) cout << -1;
    else cout << ans; // Otherwise, print the minimum cost

    cout << endl;
}

```