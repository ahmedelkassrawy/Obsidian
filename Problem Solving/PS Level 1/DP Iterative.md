```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n,m;
    cin>>n>>m;

    vector<int> adj[n+1],ind(n + 1);

    for(int i = 0; i < m; i++)
    {
        int u,v;
        cin>>u>>v;
        adj[u].push_back(v);
        ind[v]++;
    }

    queue<int> q;
    for(int i = 1; i <= n; i++)
    {
        if(ind[i] == 0)
        {
            q.push(i);
        }
    }

    vector<int> topo;

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();
        topo.push_back(curr);

        for(auto v : adj[curr])
        {
            ind[v]--;
            if(ind[v] == 0)
            {
                q.push(v);
            }
        }
    }

    reverse(topo.begin(),topo.end());

    vector<int> dp(n + 1);
    for(int i = 0; i < n;i++)
    {
        int curr = topo[i];
        dp[curr] = 1;

        for(auto v : adj[curr])
        {
            dp[v] = max(dp[v],dp[curr] + 1);
        }
    }

    int mx = 0;
    for(int i = 1; i <= n; i++)
    {
        mx = max(mx,dp[i]);
    }
    cout<<mx<<endl;
    return 0;
}
```

```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n,mxW;
    cin >> n >> mxW; 

    int w[n],v[n];
    for(int i=0;i<n;i++) cin >> w[i] >> v[i];

    int dp[n+1][mxW+1];

    //base case
    for(int rem = 0;rem <= mxW; rem++)
    {
        dp[n][rem] = 0;
    }

    for(int i = n - 1; i >= 0; i--)
    {
        for(int rem = 0;rem <= mxW; rem++)
        {
            int ch1 = dp[i+1][rem],ch2 = 0;
            if(rem >= w[i])
            {
                ch2 = dp[i+1][rem - w[i]] + v[i];
            }
            
            dp[i][rem] = max(ch1,ch2);
        }
    }

    cout << dp[0][mxW] << endl;
    return 0;
 
}
```

### Memory Reduction
```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n,mxW;
    cin >> n >> mxW; 

    int w[n],v[n];
    for(int i=0;i<n;i++) cin >> w[i] >> v[i];

    int dp[n+1][mxW+1];

    vector<int> oldDP(mxW + 1,0);

    for(int i = n - 1; i >= 0; i--)
    {
        vector<int> newDP(mxW + 1,0);

        for(int rem = 0;rem <= mxW; rem++)
        {
            newDP[rem] = oldDP[rem];

            if(rem >= w[i])
            {
                newDP[rem] = max(newDP[rem],oldDP[rem - w[i]] + v[i]);
            }
        }
        swap(oldDP,newDP);
    }

    cout << oldDP[mxW]<< endl;
    return 0;
 
}
```

```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n, maxWeight;
    cin >> n >> maxWeight;
 
    int w[n], v[n];

    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
 
    int dp[2][maxWeight + 1]; //now the n will be 2 beacuse we are looking at the parity
    //not the value of n

    // base case
    for (int rem = 0; rem <= maxWeight; rem++)
        dp[n & 1][rem] = 0;
 
    for (int i = n - 1; i >= 0; i--) 
    {
        for (int rem = 0; rem <= maxWeight; rem++) 
        {
            dp[i & 1][rem] = dp[(i + 1) & 1][rem]; //leave

            if (rem >= w[i]) dp[i & 1][rem] = max(dp[i & 1][rem], dp[(i + 1) & 1][rem - w[i]] + v[i]);
        }
    }
 
    cout << dp[0][maxWeight] << endl;
    return 0;
}

//you could finish your code then add the &1 parity optimization at the end
```

#### Knapsack 2
```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n, mxO , mxN;
    cin>>n>>mxO>>mxN;

    int valO[n], valN[n],w[n];

    for(int i = 0; i < n; i++)
    {
        cin>>valO[i]>>valN[i]>>w[i];
    }

    int dp[n+1][mxO+1][mxN+1];

    //base case
    //if dp(n , 0 ,0) return 0
    //if dp(n,any thing, anything) --> return infinity

    for(int remO = 0; remO <= mxO; remO++)
    {
        for(int remN = 0; remN <= mxN; remN++)
        {
            dp[n][remO][remN] = 1e15;
        }
    }

    dp[n][0][0] = 0; 

    for(int i = n-1; i >= 0; i--)
    {
        for(int remO = 0; remO <= mxO; remO++)
        {
            for(int remN = 0; remN <= mxN; remN++)
            {
                dp[i][remO][remN] = dp[i+1][remO][remN]; //leave 

                if(remO >= valO[i] && remN >= valN[i])
                {
                    dp[i][remO][remN] = min(dp[i][remO][remN], dp[i+1][max(0 , remO-valO[i])][max(0,remN-valN[i])] + w[i]);
                }
            }
        }
    }

    cout<<dp[0][mxO][mxN]<<endl;
    return 0; 
}
```

```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n, mxO , mxN;
    cin>>n>>mxO>>mxN;

    int valO[n], valN[n],w[n];

    for(int i = 0; i < n; i++)
    {
        cin>>valO[i]>>valN[i]>>w[i];
    }

    int dp[2][mxO+1][mxN+1];

    //base case
    //if dp(n , 0 ,0) return 0
    //if dp(n,any thing, anything) --> return infinity

    for(int remO = 0; remO <= mxO; remO++)
    {
        for(int remN = 0; remN <= mxN; remN++)
        {
            dp[n&1][remO][remN] = 1e15;
        }
    }

    dp[n&1][0][0] = 0; 

    for(int i = n-1; i >= 0; i--)
    {
        for(int remO = 0; remO <= mxO; remO++)
        {
            for(int remN = 0; remN <= mxN; remN++)
            {
                dp[i&1][remO][remN] = dp[(i+1)&1][remO][remN]; //leave 

                if(remO >= valO[i] && remN >= valN[i])
                {
                    dp[i&1][remO][remN] = min(dp[i&1][remO][remN], dp[(i+1)&1][max(0 , remO-valO[i])][max(0,remN-valN[i])] + w[i]);
                }
            }
        }
    }

    cout<<dp[0][mxO][mxN]<<endl;
    return 0; 
}
```

```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n,k;
    cin>>n>>k;

    int arr[n];
    for(int i=0;i<n;i++)
    {
        cin>>arr[i];
    }

    int dp[n + 1][k + 1];

    //base case
    for(int rem = 0; rem <= k; rem++)
    {
        dp[n][rem] = 0;
    }

    dp[n][0] = 1; //if the sum is 0 then there is 1 way to get it by not selecting any element

    for(int i = n - 1; i >= 0; i--)
    {
        for(int j = 1;j <= k; j++)
        {
            dp[i + 1][j] += dp[i + 1][j - 1];  //prefix sum
        }

        for(int rem = 0; rem <= k; rem++)
        {
            dp[i][rem] = 0;

            int len = arr[i] + 1;
            int r = rem;
            int l = r - len + 1;
            int sum = dp[i + 1][r] - ((l == 0) ? 0 : dp[i + 1][l - 1]);
        }
    }

    cout<<dp[0][k]<<endl;

}

// for(int i = n - 1; i >= 0; i--)
//     {
//         for(int rem = 0; rem <= k; rem++)
//         {
//             dp[i][rem] = 0;

//             for(int j = 0; j <= arr[i]; j++)
//             {
//                 if(rem - j >= 0)
//                 {
//                     dp[i][rem] += dp[i + 1][rem - j];
//                 }
//             }
//         }
//     }

//     cout<<dp[0][k]<<endl;

//Time complexity: O(n*k*k) --> 1e5 * 1e5 * 100

//#######################################

int main()
{
    int n, k; cin >> n >> k;
 
    int a[n];
    for(int i = 0; i < n; i++) cin >> a[i];
 
    int dp[2][k+1];
    for( int rem = 1 ; rem <= k ; rem++ )
        dp[n&1][rem] = 0;
    dp[n&1][0] = 1;
 
    for (int idx = n-1; idx >= 0 ; idx--) {
        for( int i = 1 ; i <= k ; i++ ) {
            dp[(idx + 1)&1][i] += dp[(idx + 1)&1][i - 1];
            dp[(idx + 1)&1][i] %= MOD;
        }
        for (int rem = 0; rem <= k; rem++) {
            int l = max(0ll, rem - a[idx]);
            int r = rem;
 
            dp[idx&1][rem] = dp[(idx + 1)&1][r] - ((l == 0)? 0 : dp[(idx + 1)&1][l-1]);
            dp[idx&1][rem] += MOD;
            dp[idx&1][rem] %= MOD;
        }
    }
 
    cout << dp[0][k];
    return 0;
}
```

e7na bnm4y 3aks y3ny m3aya target 3ayz awslo
asmo to sub problems wt loop 3la target mn zero to target masln
kda sub problems 
lw m3ak refrence aw value aw 7aga htdeefha wdy fy for loop tanya nested gowa targt for loop
daymn lhs = dp[i + ...] = min(dp[i + ...] , dp[i] + coins[j] aw 1 lw number of ways)