[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/J)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

int n;
vector<int> vis, order, idx, us;
vector<vector<int>> adj;

bool comp(int &a, int &b) {
    return idx[a] < idx[b];
}

int main() {
    cin >> n;

    adj.resize(n + 1);
    vis.resize(n + 1, 0);
    order.resize(n); 
    idx.resize(n + 1, 0);

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for (int i = 0; i < n; i++) {
        cin >> order[i];
        idx[order[i]] = i;
    }

    for (auto &vec : adj) {
        sort(vec.begin(), vec.end(), comp);
    }

    queue<int> q;
    
    q.push(1);
    vis[1] = 1;

    vector<int> bfs_order;

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        bfs_order.push_back(curr); // Store BFS order

        for (auto v : adj[curr]) 
        {
            if (!vis[v]) 
            {
                vis[v] = 1;
                q.push(v);
            }
        }
    }

    if (bfs_order == order) cout << "Yes\n";
    else cout << "No\n";
}

```