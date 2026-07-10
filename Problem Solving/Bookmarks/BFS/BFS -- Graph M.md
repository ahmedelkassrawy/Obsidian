[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/M)

```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <array>
using namespace std;

vector<int> vis, init, goal, ans;
vector<vector<int>> adj;

vector<int> bfs()
{
    queue <array<int , 4>> q; // node , level , even_flip , odd_flip

    q.push({1 , 1, 0 , 0});
    vis[1] = 1; 

    while (!q.empty())
    {
        auto [node , level , even_flip , odd_flip] = q.front();
        q.pop();

        int i = init[node];
        int g = goal[node];

        if(level % 2 == 1)
        {
            if(odd_flip == true)
            {
                i = 1 - i;
            }
            if(i != g) // flip the node
            {
                odd_flip = !odd_flip;
                ans.push_back(node);
            }
        }
        else
        {
            if(even_flip == true)
            {
                i = 1 - i;
            }
            if(i != g) // flip the node
            {
                even_flip = !even_flip;
                ans.push_back(node);
            }
        }

        // **Fix: Loop must be inside the while loop**
        for(int v : adj[node]) // Change `u` → `node`
        {
            if(!vis[v])
            {
                vis[v] = 1;
                q.push({v, level + 1, even_flip, odd_flip});
            }
        }
    }

    return ans;
}

int main()
{
    int n;
    cin >> n;

    vis.resize(n+1);
    init.resize(n+1);
    goal.resize(n+1);
    adj.resize(n+1);

    for(int i = 0; i < n - 1; i++)
    {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for(int i = 1; i <= n; i++) cin >> init[i];
    for(int i = 1; i <= n; i++) cin >> goal[i];

    auto ans = bfs();

    cout << ans.size() << '\n';

    for(int i : ans) cout << i << '\n';
}
```