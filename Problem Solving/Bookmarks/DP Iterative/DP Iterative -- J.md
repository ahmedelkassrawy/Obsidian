[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/K)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int mod = 1e9 + 7;

int main()
{
    int n,x;
    cin>>n>>x;

    vector<int> coins(n);
    for(int i=0;i<n;i++)
        cin>>coins[i];

    vector<int> dp(x+1,0);

    dp[0] = 1; //only one way

    //looping on the coins to get the numbered ways to get the sum x
    //fbdl mnloop aktr mn mra 3la coins how mara lkol sum wkda yb2a mfee4 ordered 
    //pairs mokrrara
    for(int j = 0; j < n; j++) 
    {
        for(int i = 1; i <= x; i++)
        {
            if(i - coins[j] >= 0)
            {
                dp[i] += dp[i - coins[j]];
                dp[i] %= mod;
            }
        }
    }

    cout<<dp[x]<<endl;
}
```