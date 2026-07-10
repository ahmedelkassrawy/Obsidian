[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/P)
```C++
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

int mod = 1e9 + 7;

int main() 
{
    int n;
    cin>>n;

    vector<int> v(n);
    for(int i=0; i<n; i++)
        cin>>v[i];

    int l = 1;
    for(int i = 1; i <= 9; i++)
    {
        l = lcm(l, i);
    }

    vector<vector<int>> dp(n+1, vector<int>(l));
    dp[n][0] = 1;

    for(int i = n - 1; i >= 0; i--)
    {
        for(int j = 0; j < l; j++)
        {
           dp[i][j] = (dp[i + 1][j] + dp[i + 1][(v[i] * j) % l]) % mod;
        }
    }

    cout<<dp[0][l -1]<<endl;
    return 0;

}
```