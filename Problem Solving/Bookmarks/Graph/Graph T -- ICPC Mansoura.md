[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/T)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

int n; // Number of nodes in the tree
vector<vector<int>> adj; // Adjacency list representation of the tree
vector<bool> vis; // Boolean vector to track visited nodes
vector<int> dist; // Distance vector to store depth of each node

// Depth-First Search (DFS) function to compute distances
void dfs(int u, int p, int d)
{
    vis[u] = 1; // Mark the current node as visited
    dist[u] = d; // Store the distance from the starting node

    for (int v : adj[u]) // Iterate over all adjacent nodes
    {
        if(v == p) continue; // Skip the parent node to prevent revisiting
        dfs(v, u, d + 1); // Recursive DFS call with updated depth
    }
}

int main()
{
    cin >> n; // Read the number of nodes

    adj.resize(n + 1); // Resize adjacency list to hold n+1 nodes (1-based indexing)
    vis.resize(n + 1, false); // Initialize the visited array with false

    // Read edges and construct the tree
    for(int i = 0; i < n - 1; i++)
    {
        int u, v;
        cin >> u >> v;

        adj[u].push_back(v); // Add edge u-v
        adj[v].push_back(u); // Add edge v-u (since it's an undirected tree)
    }

    dist.resize(n + 1, 0); // Initialize distance array with 0
    dfs(0, -1, 0); // Perform DFS from node 0 (assuming 0-based indexing)

    int big = -1; // Variable to store the maximum distance found
    int node = -1; // Variable to store the farthest node

    // Find the farthest node from node 0
    for(int i = 1; i <= n; i++)
    {
        if(dist[i] > big)
        {
            big = dist[i];
            node = i; // Store the farthest node
        }
    }

    dist.assign(n + 1, 0); // Reset distance array
    dfs(node, -1, 0); // Perform DFS from the farthest node found earlier

    big = 0; // Reset max distance
    // Find the longest path in the tree (diameter)
    for(int i = 1; i <= n; i++)
    {
        if(dist[i] > big)
        {
            big = dist[i];
        }
    }

    cout << big << endl; // Output the tree diameter
}
```