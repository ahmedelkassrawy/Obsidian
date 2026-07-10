```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n, we;
vector<int> weights, val;

// Recursive function for solving the knapsack problem
int f(int i, int rem, const vector<int>& weights, const vector<int>& val) {
    // Base case: No items left or weight capacity exhausted
    if (i == n || rem == 0) return 0;

    // If the current item's weight exceeds the remaining weight, skip it
    if (weights[i] > rem) {
        return f(i + 1, rem, weights, val);
    }

    // Option 1: Include the current item
    int op1 = val[i] + f(i + 1, rem - weights[i], weights, val);
    // Option 2: Exclude the current item
    int op2 = f(i + 1, rem, weights, val);

    // Return the maximum of the two options
    return max(op1, op2);
}

int main() {
    cin >> n >> we;

    // Resize the vectors to hold n elements
    weights.resize(n);
    val.resize(n);

    // Read weights and values
    for (int i = 0; i < n; i++) {
        cin >> weights[i] >> val[i];
    }

    // Call the recursive function and print the result
    cout << f(0, we, weights, val) << endl;

    return 0;
}

```