[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/E)
```C++
#include <iostream>
#include <vector>
using namespace std;

const int INF = 1e9;  // Safe large number

int main() 
{
    int n, x;
    cin >> n >> x;

    vector<int> coins(n);
    for (int i = 0; i < n; i++) 
        cin >> coins[i];

    vector<int> dp(x + 1, INF);
    dp[0] = 0;

    for (int i = 0; i <= x; i++)  // Fix: i <= x
    {
        if (dp[i] == INF) continue;  // Fix: Skip invalid values

        for (int j = 0; j < n; j++) 
        {
            if (i + coins[j] <= x) 
            {
                dp[i + coins[j]] = min(dp[i + coins[j]], dp[i] + 1);
            }
        }
    }

    cout << (dp[x] == INF ? -1 : dp[x]) << endl;  
    return 0;
}

```