[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/D)
```C++
#include <iostream>
#include <vector>
#include <climits> // For INT_MAX
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    int n,k;
    cin >> n>>k;

    vector<int> h(n + 1);
    for (int i = 1; i <= n; i++)
        cin >> h[i];

    vector<int> dp(n + 1, INT_MAX);
    dp[1] = 0; //cost to reach the first stone is 0

    for (int i = 1; i <= n; i++) 
    {
        for(int j = 1; j <= k; j++)
        {
            if(i + j <= n)
            {
                dp[i + j] = min(dp[i + j], dp[i] + abs(h[i] - h[i + j]));
            }
        }
    }

    cout << dp[n] << endl; 
    return 0;
}
```