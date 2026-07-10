[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/P)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

const int N = 1e5 + 5;  // Max nodes
vector<int> adj[N];     // Adjacency list
int in_degree[N];       // In-degree array
int dp[N];              // DP array for longest path
int n, m;               // Number of nodes and edges

int go() 
{
    queue<int> q;

    for (int i = 1; i <= n; i++) 
    {
        if (in_degree[i] == 0) 
        {
            q.push(i);
        }
    }

    int mx = 0;
    
    while (!q.empty()) 
    {
        int u = q.front();
        q.pop();

        for (int v : adj[u]) 
        {
            dp[v] = max(dp[v], dp[u] + 1);
            mx = max(mx, dp[v]);
            in_degree[v]--;

            if (in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    return mx;
}

int main() 
{
    cin >> n >> m;

    for (int i = 0; i < m; i++) 
    {
        int x, y;
        cin >> x >> y;

        adj[x].push_back(y);
        in_degree[y]++;
    }

    cout << go() << endl;

    return 0;
}

```

```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <climits>
using namespace std;

const int N = 1e5 + 5;
int n, m;
vector<vector<int>> adj;
int dp[N];

int go(int currnode)
{
    //base case
    if(adj[currnode].size() == 0) return 0;
    
    if(dp[currnode] != -1) return dp[currnode];

    int res = INT_MIN;
    for(auto v : adj[currnode])
    {
        res = max(res, go(v) + 1); //checking for all the children of the current node
    }

    return dp[currnode] = res;
}

int main()
{
    cin>>n>>m;

    adj.resize(n+1);
    for(int i=0; i<m; i++)
    {
        int u, v;
        cin>>u>>v;
        adj[u].push_back(v);
    }

    int ans = 0;
    memset(dp, -1, sizeof(dp));
    for(int i=1; i<=n; i++)
    {
        ans = max(ans, go(i));
    }

    cout<<ans<<endl;
    return 0;
}
```