[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/H)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <stack>
using namespace std;

int n, m;
vector<int> vis, levels, indegree, order;
vector<vector<int>> adj;

void bfs()
{
    queue<int> q;
    order.clear(); // Clear order vector before each test case

    for (int i = 1; i <= n; i++)
    {
        if (indegree[i] == 0)
        {
            q.push(i);
            levels[i] = 1;
        }
    }

    while (!q.empty())
    {
        int curr = q.front();
        q.pop();

        order.push_back(curr);

        for (int v : adj[curr])
        {
            indegree[v]--;

            if (indegree[v] == 0)
            {
                q.push(v);
                levels[v] = levels[curr] + 1;
            }
        }
    }
}

int main()
{
    while (cin >> n >> m, n || m)
    {
        adj.assign(n + 1, vector<int>()); // Proper reset
        vis.assign(n + 1, 0);
        levels.assign(n + 1, 0);
        indegree.assign(n + 1, 0);
        order.clear();

        for (int i = 0; i < m; i++)
        {
            int u, v;
            cin >> u >> v;
            
            adj[u].push_back(v);
            indegree[v]++;
        }

        bfs();

        if (order.size() == n)
        {
            for (int i : order)
            {
                cout << i << endl;
            }
        }
        else cout << "IMPOSSIBLE" << endl;
    }
    return 0;
}
```