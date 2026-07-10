[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/P)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

int n,m;
vector<vector<int>> adj;
vector<bool> vis;

void dfs(int u)
{
    vis[u] = true;
    for(int v: adj[u])
    {
        if(!vis[v])
        {
            dfs(v);
        }
    }
}

int main()
{
    cin>>n>>m;
    
    adj.resize(n + 1);
    vis.resize(n + 1,false);

    for(int i = 0;i < m;i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    if(n != m) //one of the conditions for a graph to be a tree is that it should have n - 1 edges
    {
        cout<<"NO";
        return 0;
    }

    int cnt = 0;
    for(int i = 1; i <= n;i++)
    {
        if(!vis[i])
        {
            dfs(i);
            cnt++;
        }
    }

    if(cnt == 1)
    {
        cout<<"FHTAGN!";
    }
    else
    {
        cout<<"NO";
    }

}

//so mn la5er check en el graph 3ndna tree wla la2
//wlw cnt == 1 y3ny kolhom y2dro yb2o one component rg3 yes
```

![[Screenshot (87).png]]