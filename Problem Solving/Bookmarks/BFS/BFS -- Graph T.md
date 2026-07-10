[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/T)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n;
    cin >> n;

    vector<int> a(n + 1); // Array to store values
    vector<vector<int>> adj(n + 1); // Adjacency list
    vector<vector<int>> dist(n + 1, vector<int>(2, -1)); // Distance matrix
    queue<pair<int, int>> q; // Queue for BFS

    // Input array and build adjacency list
    for (int i = 1; i <= n; i++)
    {
        cin >> a[i];

        // Add edges based on the rules
        if (i + a[i] <= n)
        {
            adj[i + a[i]].push_back(i);
        }
        if (i - a[i] >= 1)
        {
            adj[i - a[i]].push_back(i);
        }

        // Initialize BFS queue with starting nodes
        q.push({i, a[i] & 1}); // 0 for even, 1 for odd
        dist[i][a[i] & 1] = 0; // Distance to itself is 0
    }

    // Perform BFS
    while (!q.empty())
    {
        auto [i, parity] = q.front();
        q.pop();

        for (auto u : adj[i])
        {
            if (dist[u][parity] == -1)
            {
                dist[u][parity] = dist[i][parity] + 1;
                q.push({u, parity});
            }
        }
    }

    // Output the results
    for (int i = 1; i <= n; i++)
    {
        cout << (dist[i][!(a[i] & 1)] == -1 ? -1 : dist[i][!(a[i] & 1)]) << " ";
    }

    return 0;
}
```