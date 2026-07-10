```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstring>
#include <climits>
using namespace std;

int n, m;
const int N = 1e5 + 5;
const int M = 101;
vector<int> v;
const int MOD = 1e9 + 7;
int dp[N][M];

int go(int i, int last)
{
    // Base case: If we have reached the end of the array, return 1 valid configuration
    if (i == n) return 1;

    // If the current value is already set and invalid based on the previous one, return 0
    if (i > 0 && v[i] != 0 && abs(v[i] - last) > 1) return 0;

    // Check if we have already computed this state
    if (dp[i][last] != -1) return dp[i][last];

    // If v[i] is already assigned, proceed with that value
    if (v[i] != 0) return dp[i][last] = go(i + 1, v[i]) % MOD;

    int ret = 0;

    // Special case for the first element
    if (i == 0 && v[i] == 0)
    {
        for (int j = 1; j <= m; j++)
        {
            ret = (ret + go(i + 1, j)) % MOD;
        }
        return dp[i][last] = ret;
    }

    // Three possible choices: last - 1, last, last + 1 (within valid bounds)
    int op1 = 0, op2 = 0, op3 = 0;

    if (last < m) op1 = go(i + 1, last + 1) % MOD;
    
    op2 = go(i + 1, last) % MOD;
    
    if (last > 1) op3 = go(i + 1, last - 1) % MOD;

    return dp[i][last] = (op1 + op2 + op3) % MOD;
}

int main()
{
    cin >> n >> m;

    v.resize(n);

    for (int i = 0; i < n; i++)
    {
        cin >> v[i];
    }

    memset(dp, -1, sizeof(dp));

    cout << go(0, 0) << endl;
}
```