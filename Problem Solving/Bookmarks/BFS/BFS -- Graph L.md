[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/L)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

int n;
vector<int> vis, level, teams;
vector<vector<int>> adj;

bool bfs(int s)
{
    queue<int> q;
    q.push(s);
    vis[s] = 1;
    teams[s] = 1;

    while (!q.empty())
    {
        int curr = q.front();
        q.pop();

        for (int v : adj[curr])
        {
            if (!vis[v])
            {
                q.push(v);
                vis[v] = 1;
                teams[v] = 3 - teams[curr]; 
            }
            else if (teams[v] == teams[curr])
            {
                return false;  // Conflict found, not bipartite
            }
        }
    }
    return true;
}

int main()
{
    int t;
    cin >> t;

    while (t--)
    {
        cin >> n;
        adj.assign(n + 1, vector<int>());
        vis.assign(n + 1, 0);
        level.assign(n + 1, 0);
        teams.assign(n + 1, 0);

        for (int i = 0; i < n; i++)
        {
            int u, v;
            cin >> u >> v;

            adj[u].push_back(v);
            adj[v].push_back(u);
        }

        bool isBipartite = 1;

        for(auto vec : adj) //goz2 gdeed 
        {
            if(vec.size() > 2) isBipartite = 0;
        }

        if(!isBipartite) 
        {
            cout << "NO\n";
            continue;
        }

        for (int i = 1; i <= n; i++)
        {
            if (!vis[i] && !teams[i])
            {
                if (!bfs(i))
                {
                    isBipartite = false;
                    break;
                }
            }
        }

        cout << (isBipartite ? "YES\n" : "NO\n");
    }

    return 0;
}

```