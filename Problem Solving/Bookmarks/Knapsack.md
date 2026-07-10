**https**://codeforces.com/group/MWSDmqGsZm/contest/223339/problem/U

```C++
#include <iostream>
#include <vector>
using namespace std;

int knapsack(int capacity, vector<int>& weights, vector<int>& values, int index) {
    // Base case: If capacity becomes 0 or all items are explored
    if (capacity == 0 || index == 0) {
        return 0;
    }

    // If the weight of the current item exceeds the remaining capacity, skip it
    if (weights[index - 1] > capacity) {
        return knapsack(capacity, weights, values, index - 1);
    }

    // Recursive step: Choose the maximum of including and excluding the current item

    return max(values[index - 1] + knapsack(capacity - weights[index - 1], weights, values, index - 1),knapsack(capacity, weights, values, index - 1));
}
  
int main() {
    int size, req;
    cin >> size >> req;
    vector<int> weights(size);
    vector<int> values(size);

    for (int i = 0; i < size; ++i) {
        cin >> weights[i] >> values[i];
    }

    cout << knapsack(req, weights, values, size);
    return 0;
}
```