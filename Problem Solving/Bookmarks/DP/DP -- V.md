[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/V)
```C++
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAX_ISLANDS = 30001;
const int MAX_JUMP = 505;
const int shift = 250;

int n, d,mx;
int dp[MAX_ISLANDS][MAX_JUMP]; // DP state table
vector<int> freq(MAX_ISLANDS);  // Store gems count at each island

// Recursive DP function with memoization
int go(int i, int last) {
    if (i > mx) return 0; // Out of bounds

    if (dp[i][last - d + shift] != -1) return dp[i][last - d + shift]; // Return if already computed

    int op1 = go(i + last,last) + freq[i];
    int op2 = go(i + last + 1, last + 1) + freq[i];
    int op3 = go(i + last - 1, last - 1) + freq[i];

    return dp[i][last - d + shift] = max({op1, op2, op3}); // Store and return the maximum
}

int main() {
    cin >> n >> d;

    memset(dp, -1, sizeof(dp)); // Initialize DP table
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        freq[x]++; // Store number of gems at each island
        mx = max(mx,x);
    }

    cout << go(d, d) << endl; // Start from the first jump at `d`
    return 0;
}

```