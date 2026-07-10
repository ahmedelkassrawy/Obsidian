[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/B)
```C++
#include <iostream>
#include <vector>
using namespace std;

int MOD = 1e9 + 7;

int main()
{
    int n;
    cin >> n;

    int arr[] = {1,2,3,4,5,6};
    vector<int> dp(n+1, 0);

    dp[0] = 1; //only one wayy

    for(int sum = 1; sum <= n; sum++)
    {
        for(int dice = 1; dice <= 6; dice++)
        {
            if(sum - dice >= 0)
            {
                dp[sum] = (dp[sum] + dp[sum - dice]) % MOD;
            }
        }
    }

    cout<<dp[n]<<endl;
    return 0;
}
```