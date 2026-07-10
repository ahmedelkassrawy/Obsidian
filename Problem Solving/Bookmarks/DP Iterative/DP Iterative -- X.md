[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/X)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int INF = 1e9;

int main() 
{
    freopen("talent.in", "r", stdin);  // Read input from file
    freopen("talent.out", "w", stdout); // Write output to file
    
    int n, W;
    cin >> n >> W;

    int max_talent = 0;
    vector<int> w(n), t(n);
    for (int i = 0; i < n; i++) {
        cin >> w[i] >> t[i];
        max_talent += t[i];
    }

    vector<int> dp(max_talent + 1, INF);
    dp[0] = 0;

    // For each cow, update the DP table
    for(int i = 0; i < n; i++)
    {
        // Process in reverse to avoid counting the same cow multiple times
        for(int j = max_talent; j >= t[i]; j--)
        {
            if(dp[j - t[i]] != INF) {
                dp[j] = min(dp[j], dp[j - t[i]] + w[i]);
            }
        }
    }

    int ans = 0;
    for(int i = 1; i <= max_talent; i++)
    {
        if(dp[i] >= W && dp[i] != INF)  // Changed <= to >= for weight constraint
        {
            ans = max(ans, (i * 1000) / dp[i]);
        }
    }

    cout << ans << endl;
    return 0;
}
```