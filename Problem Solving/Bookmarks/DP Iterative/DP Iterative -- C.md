[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/C)
```C++
#include <iostream>
#include <vector>
#include <climits> // For INT_MAX
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    int n;
    cin >> n;

    vector<int> h(n + 1);
    for (int i = 1; i <= n; i++)
        cin >> h[i];

    vector<int> dp(n + 1, INT_MAX);
    dp[1] = 0; //cost to reach the first stone is 0

    for (int i = 1; i < n; i++) 
    {
        //i+1
        dp[i + 1] = min(dp[i + 1], dp[i] + abs(h[i] - h[i + 1]));

        //i+2
        if (i + 2 <= n)
            dp[i + 2] = min(dp[i + 2], dp[i] + abs(h[i] - h[i + 2]));
    }

    cout << dp[n] << endl; 
    return 0;
}

```