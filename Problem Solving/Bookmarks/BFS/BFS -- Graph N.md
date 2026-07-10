[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/N)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <cmath>
using namespace std;

int n,m;
vector<vector<int>> adj;
vector<int> vis,level,team;
vector<pair<int, int>> edges;

bool bfs(int start)
{
    queue<int> q;

    q.push(start);
    vis[start] = 1;
    level[start] = 0;
    team[start] = 1;

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();

        for(auto i : adj[curr])
        {
            if(!vis[i])
            {
                q.push(i);
                vis[i] = 1;
                level[i] = level[curr] + 1;
                team[i] = 3 - team[curr];
            }
            else if(team[i] == team[curr]) return false;
        }
    }
    return true;
}

int main()
{
    cin >> n >> m;
    adj.resize(n+1);
    vis.resize(n+1);
    level.resize(n+1);
    team.resize(n+1);

    for(int i=0;i<m;i++)
    {
        int u,v;
        cin >> u >> v;

        adj[u].push_back(v);
        adj[v].push_back(u);
        edges.push_back({u, v});
    }

    for(int i=1;i<=n;i++)
    {
        if(!vis[i])
        {
            if(!bfs(i))
            {
                cout << "NO";
                return 0;
            }
        }
    }

    cout<<"YES\n";
    for(auto [u,v] : edges)
    {
        cout<<(team[u] > team[v] ? 0 : 1);
    }
    cout<<endl;


    return 0;
}
```