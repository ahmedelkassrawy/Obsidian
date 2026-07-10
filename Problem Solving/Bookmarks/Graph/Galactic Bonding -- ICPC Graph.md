[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/N)
```C++
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// Function to calculate Euclidean distance squared (avoiding precision issues)
double distanceSquared(double x1, double y1, double x2, double y2) {
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
}

// DFS function to traverse the graph
void dfs(int u, vector<vector<int>>& adj, vector<bool>& vis) 
{
    vis[u] = true;
    for (int v : adj[u]) 
    {
        if (!vis[v]) 
        {
            dfs(v, adj, vis);
        }
    }
}

int main() 
{
    int t;
    cin >> t; 

    for (int testCase = 1; testCase <= t; testCase++) 
    {
        int n;
        double d;
        cin >> n >> d; 

        vector<pair<double, double>> stars(n);
        for (int i = 0; i < n; i++) 
        {
            cin >> stars[i].first >> stars[i].second;
        }

        double dSquared = d * d;

        vector<vector<int>> adj(n);
        vector<bool> vis(n, false);

        for (int i = 0; i < n; i++) 
        {
            for (int j = i + 1; j < n; j++) 
            {
                if (distanceSquared(stars[i].first, stars[i].second, stars[j].first, stars[j].second) <= dSquared) {
                
                    adj[i].push_back(j);
                    adj[j].push_back(i);
                }
            }
        }

        // Count constellations using DFS
        int ans = 0;
        
        for (int i = 0; i < n; i++) 
        {
            if (!vis[i]) {
                dfs(i, adj, vis);
                ans++;
            }
        }

        // Output the result
        cout << "Case " << testCase << ": " << ans << endl;
    }

    return 0;
}

```