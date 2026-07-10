```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <climits>
#include <algorithm>
using namespace std;

int n, wlimit;

struct item {
    int v, w;
};

vector<item> v;
int bestValue = 0; // ✅ Initialize bestValue
int dp[105][100005];

int go(int i, int val) {
    if (val < 0) return INT_MAX / 2; // ✅ Prevent invalid negative states
    if (i == n) return (val == 0 ? 0 : INT_MAX / 2); // ✅ Use INT_MAX/2 to prevent overflow

    if (dp[i][val] != -1) return dp[i][val];

    int op1 = go(i + 1, val); // Don't take item
    int op2 = (val >= v[i].v) ? go(i + 1, val - v[i].v) + v[i].w : INT_MAX / 2; // ✅ Check before subtracting

    return dp[i][val] = min(op1, op2);
}

void solve() {
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    
    cin >> n >> wlimit;
    v.resize(n);

    for (int i = 0; i < n; i++) {
        cin >> v[i].v >> v[i].w;
        bestValue += v[i].v; // ✅ Calculate max possible value
    }

    memset(dp, -1, sizeof(dp));

	//checking the loop for the best value then moving from there 
	//ma4yeen 3aks 
    for (int i = bestValue; i >= 0; i--) {
        if (go(0, i) <= wlimit) { // ✅ Check if weight is within the limit
            cout << i << endl;
            break;
        }
    }
}

int main() {
    solve();
    return 0;
}
```