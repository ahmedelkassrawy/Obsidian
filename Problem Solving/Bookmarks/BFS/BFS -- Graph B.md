[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/B)
```C++
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int n, m;
vector<int> indegree, topo;
vector<vector<int>> adj;

void bfs() {
    priority_queue<int, vector<int>, greater<int>> q;


    // Push nodes with indegree == 0 into the queue
    for (int i = 1; i <= n; i++) {
        if (indegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int curr = q.top();
        q.pop();
        topo.push_back(curr);

        for (int v : adj[curr]) {
            indegree[v]--; // Reduce indegree of child nodes
            if (indegree[v] == 0) {
                q.push(v);
            }
        }
    }
}

int main() {
    cin >> n >> m;

    adj.resize(n + 1);
    indegree.resize(n + 1, 0);

    for (int i = 0; i < m; i++) 
    {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v); // Directed graph

        indegree[v]++;
    }

    bfs();

    // If topo.size() < n, a cycle exists
    if (topo.size() < n) 
    {
        cout << "Sandro fails." << endl;
        return 0;
    }

    for (int i : topo) 
    {
        cout << i << " ";
    }
    cout << endl;

    return 0;
}

```