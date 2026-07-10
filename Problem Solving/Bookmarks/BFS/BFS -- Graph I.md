[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/I)
```C++
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int n, k;
vector<int> vis, indegree, levels, topo, par;
vector<vector<int>> adj;

void bfs(int boss)
{
    queue<int> q;
    q.push(boss);
    vis[boss] = 1;
    levels[boss] = 0;

    topo.push_back(0); //howa 3ayzk t3ml kda

    while (!q.empty())
    {
        int curr = q.front();
        q.pop();

        topo.push_back(curr);

        for (auto v : adj[curr])
        {
            indegree[v]--;

            if (indegree[v] == 0)
            {
                q.push(v);
                vis[v] = 1;
                levels[v] = levels[curr] + 1;
            }
        }
    }
}

int main()
{
    cin >> n >> k;

    vis.resize(n + 1, 0);
    indegree.resize(n + 1, 0);
    levels.resize(n + 1, 0);
    adj.resize(n + 1);
    par.resize(n + 1, -1); // Initialize parents with -1 (no parent)

    for (int i = 1; i <= k; i++)
    {
        int sz;
        cin >> sz;

        while (sz--)
        {
            int u;
            cin >> u;

            adj[i].push_back(u);
            indegree[u]++;
        }
    }

    int boss = 0;
    for (int i = 1; i <= n; i++)
    {
        if (indegree[i] == 0)
        {
            boss = i;
            break;
        }
    }

    // Ensure all orphan nodes are connected to the boss
    for (int i = 1; i <= n; i++)
    {
        if (boss != i && indegree[i] == 0)
        {
            adj[boss].push_back(i);
            indegree[i]++;
        }
    }

    bfs(boss); // Run BFS from the root

    // Assign parents correctly
    for (int i = 1; i <= n; ++i)
    {
        par[topo[i]] = topo[i - 1];
    }

    // Output the parent of each node
    for (int i = 1; i <= n; i++)
    {
        cout << par[i] << "\n";
    }
}

```