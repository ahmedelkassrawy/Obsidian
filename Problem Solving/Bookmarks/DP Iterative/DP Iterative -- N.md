[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/N)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
using namespace std;
const int MOD = 1e9 + 7;

int main() 
{
   int n;
   cin >> n;

   vector<int> coins(n);

   for (int i = 0; i < n; i++) {
      cin >> coins[i];
   }

   set<int> st;
   st.insert(0); // 0 base case

   for(int i = 0; i < n; i++)
   {
      set<int> tmp;
      for(auto x : st)
      {
         tmp.insert(x + coins[i]);
      }
      st.insert(tmp.begin(), tmp.end());
   }

   //remove zero
   st.erase(0);
   cout<<st.size()<<"\n";

   for(auto x : st)
   {
      cout<<x<<" ";
   }
   cout<<"\n";
   return 0;
}
```

```C++
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

int main() 
{
    int n;
    cin>>n;

    vector<int> v(n);
    for(int i=0; i<n; i++)
    {
        cin>>v[i];
    }

    int mxsum = accumulate(v.begin(), v.end(), 0);
    vector<vector<bool>> dp(n+1, vector<bool>(mxsum));
    dp[n][0] = 1;

    for(int i = n - 1; i >= 0;i--)
    {
        for(int j = 0; j <= mxsum; j++)
        {
            dp[i][j] = dp[i + 1][j]; //leave

            if(j - v[i] >= 0)
            {
                dp[i][j] = dp[i][j] || dp[i + 1][j - v[i]]; //take
            }
        }
    }

    vector<int> ans;
    for(int i = 1; i <= mxsum; i++)
    {
        if(dp[0][i]) ans.push_back(i);
    }

    cout<<ans.size()<<endl;
    for(int i = 0; i < ans.size(); i++)
    {
        cout<<ans[i]<<" ";
    }
    return 0;

}
```

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

    if(((n*(n+1)) / 2 ) % 2 != 0)
    {
        cout<<"0";
        return 0;
    }

    int mxsum = (n*(n+1)) / 4; //to get the mxsum of the subset
    vector<vector<int>> dp(2, vector<int>(mxsum + 1));
    dp[n & 1][0] = 1;

    for(int i = n - 1; i >= 1 ;i--)
    {
        for(int j = 0; j <= mxsum; j++)
        {
            dp[i & 1][j] = dp[(i+1) & 1][j];

            if(j - i >= 0)
            {
                dp[i & 1][j] += dp[(i+1) & 1][j-i];
                dp[i & 1][j] %= mod;
            }
        }
    }

    cout<<dp[1 & 1][mxsum]<<"\n";
    return 0;

}
```