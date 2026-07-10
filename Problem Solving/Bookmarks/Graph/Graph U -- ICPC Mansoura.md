[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/U)
```C++
#include <vector>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
using namespace std;

int n,m;
vector<int> a;
vector<vector<int>> adj;
vector<bool> vis;
int cnt = 0;

void dfs(int u , int c)
{
    vis[u] = true;
     
    if(a[u]) c++;
    else c = 0;

    if(c > m) return;

    bool isleaf = true;

    for(auto v : adj[u])
    {
        if(!vis[v])
        {
            isleaf = false;
            dfs(v,c);
        }
    }

    if(isleaf) cnt++; //2abl my5ls elfunction wyrg3 yb2a lw 3ada mn kol lfo2 da tb2a leaf
}

int main()
{
    cin>>n>>m;

    a.resize(n+1);
    adj.resize(n+1);
    vis.resize(n+1);

    for(int i= 1;i <= n;i++)
    {
        cin>>a[i];
    }

    for(int i = 1;i <= n-1;i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    dfs(1,0);
    cout<<cnt;
}
```