```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int mod = 1e9 + 7;

int main() 
{
    int t;
    cin >> t;

    while(t--)
    {
        int n, k;
        cin >> n >> k;

        vector<int> v(n);
        for(int i = 0; i < n; i++)
            cin >> v[i];

        vector<vector<int>> dp(n + 1, vector<int>(31, 0)); // Fixed: 31 instead of 32 for valid bit shifts

        for(int i = n - 1; i >= 0; i--)
        {
            for(int j = 0; j <= 30; j++)
            {
                int divideFactor = (1 << (j + 1)); // Avoid repeated recalculations

                if(j == 0) // Good key case
                {
                    int option1 = dp[i + 1][j] + v[i] - k; // Don't switch
                    int option2 = (j < 30) ? (dp[i + 1][j + 1] + v[i] / divideFactor) : 0; // Safe bound check
                    dp[i][j] = max(option1, option2);
                }
                else // Bad key case
                {
                    dp[i][j] = (j < 30) ? (dp[i + 1][j + 1] + v[i] / divideFactor) : 0; // Safe bound check
                }
            }
        }

        cout << dp[0][0] << endl;
    }
}

// If you use a good key, you gain a[i] coins but pay k
// dp[i][j] = dp[i + 1][j + 1] + a[i] - k

// If you use a bad key, you gain a[i] / 2^(j + 1) coins
// dp[i][j] = dp[i + 1][j + 1] + a[i] / 2^(j + 1)
```