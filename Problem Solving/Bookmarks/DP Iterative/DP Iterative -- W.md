[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/W)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int mod = 1e9 + 7;

int main() 
{
    int r,g,b;
    cin>>r>>g>>b;
    
    vector<int> R(r), G(g), B(b);
    for(int i=0; i<r; i++) cin>>R[i];
    for(int i=0; i<g; i++) cin>>G[i];
    for(int i=0; i<b; i++) cin>>B[i];

    sort(R.rbegin(), R.rend());
    sort(G.rbegin(), G.rend());
    sort(B.rbegin(), B.rend()); // Sorting in descending order

    vector<vector<vector<int>>> dp(r+1, vector<vector<int>>(g+1, vector<int>(b+1, 0)));

    for(int i = r;i >= 0; i--)
    {
        for(int j = g; j >= 0; j--)
        {
            for(int k = b; k >= 0; k--)
            {
                if(i < r && j < g)
                {
                    dp[i][j][k] = max(dp[i][j][k], dp[i+1][j+1][k] + R[i]*G[j]);
                }
                if(j < g && k < b)
                {
                    dp[i][j][k] = max(dp[i][j][k], dp[i][j+1][k+1] + G[j]*B[k]);
                }
                if(i < r && k < b)
                {
                    dp[i][j][k] = max(dp[i][j][k], dp[i+1][j][k+1] + R[i]*B[k]);
                }
            }
        }
    }

    cout<<dp[0][0][0]<<"\n";
    return 0;
}

```