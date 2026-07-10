[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/C)

```C++
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

vector<vector<int>> adj;
vector<bool> vis;
int maxSize;

int dfs(int u) 
{
    vis[u] = 1;
    int size = 1; // Counting the current node

    for (int v : adj[u]) {
        if (!vis[v]) 
        {
            size += dfs(v);
        }
    }
    return size;
}

int main() {
    int t;
    cin >> t;

    while (t--) 
    {
        int n, m;
        cin >> n >> m;

        adj.assign(n + 1, vector<int>());
        vis.assign(n + 1, false);

        maxSize = 0;

        for (int i = 0; i < m; i++) 
        {
            int u, v;
            cin >> u >> v;

            adj[u].push_back(v);
            adj[v].push_back(u);
        }

        for (int i = 1; i <= n; i++) 
        {
            if (!vis[i]) 
            {
                maxSize = max(maxSize, dfs(i));
            }
        }

        cout << maxSize << endl;
    }

    return 0;
}

```