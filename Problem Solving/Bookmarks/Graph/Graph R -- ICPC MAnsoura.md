[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/R)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

int n,m;
vector<vector<int>> adj,comp;
vector<bool> vis;
int comp_cnt,ed = 0;

void dfs(int u)
{
    vis[u] = true;
    comp_cnt++;

    for(int v : adj[u])
    {
        if(!vis[v])
        {
            dfs(v);
        }
    }

    ed += adj[u].size();
    //counting the number of edges in the connected component
}


int main()
{
    cin>>n>>m;

    adj.resize(n+1);
    vis.resize(n + 1,false);
    
    for(int i =0; i < m; i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for(int i = 1; i <= n; i++)
    {
        if(!vis[i])
        {
            comp_cnt = 0;
            ed = 0;

            dfs(i);

            ed /= 2;
            
            if(ed != (comp_cnt*(comp_cnt - 1) / 2))
            {
                cout<<"NO";
                return 0;
            }
        }
    }

    cout<<"YES";
}

//this code is checking if the graph is complete or not
//if the graph is complete then the number of edges in the connected component should be equal to the number of vertices in the connected component
```

![[Screenshot (88).png]]