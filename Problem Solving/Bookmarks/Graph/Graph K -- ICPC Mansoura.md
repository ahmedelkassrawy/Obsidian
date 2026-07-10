[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/K)
```C++
#include <iostream>
#include <vector>
#include <map>
using namespace std;

map<int, vector<int>> graph; // Adjacency List
map<int, int> vis, in_degree;

bool dfs(int u) {
    vis[u] = 1; // Mark as visited
    bool isTree = true;

    for (int v : graph[u]) {
        if (!vis[v]) {
            isTree &= dfs(v); // Continue DFS
        } else {
            return false; // Cycle detected
        }
    }

    return isTree;
}

int main() {
    int u, v, case_num = 0;

    while (true) {
        graph.clear();
        vis.clear();
        in_degree.clear();

        bool hasEdges = false;

        while (cin >> u >> v) {
            if (u == -1 && v == -1) return 0; // End of input
            if (u == 0 && v == 0) break; // End of test case

            hasEdges = true;
            graph[u].push_back(v);
            in_degree[v]++;
            if (in_degree.find(u) == in_degree.end()) in_degree[u] = 0; // Ensure all nodes are tracked
        }

        case_num++;

        // If there are no edges, it's a tree
        if (!hasEdges) {
            cout << "Case " << case_num << " is a tree." << endl;
            continue;
        }

        // Finding the root (node with in-degree 0)
        int root = -1, many_roots = 0;
        for (auto &i : in_degree) {
            if (i.second == 0) { // Root node
                root = i.first;
                many_roots++;
            }
        }

        // If there are multiple roots or no root, it's not a tree
        if (many_roots != 1 || root == -1) {
            cout << "Case " << case_num << " is not a tree." << endl;
            continue;
        }

        // Run DFS to check connectivity & cycles
        if (dfs(root) && vis.size() == in_degree.size()) {
            cout << "Case " << case_num << " is a tree." << endl;
        } else {
            cout << "Case " << case_num << " is not a tree." << endl;
        }
    }
}

```