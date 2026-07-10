[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/O)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

int n,m;
vector<vector<int>> adj;
vector<bool> vis;
vector<vector<int>> grp[4];
vector<int> comp;

void dfs(int u)
{
    vis[u]=true;

    comp.push_back(u);

    for(int v:adj[u])
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

    adj.resize(n+1);

    for(int i=0;i<m;i++)
    {
        int u,v;
        cin>>u>>v;

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vis.resize(n+1,false);

    for(int i =1; i <= n; i++)
    {
        if(!vis[i])
        {
            comp.clear();
            dfs(i);

            int sz = comp.size();

            if(sz > 3)
            {
                cout<<-1;
                return 0;
            }

            grp[sz].push_back(comp);
        }
    }

    vector<vector<int>> ans;
    while(!grp[3].empty())
    {
        ans.push_back(grp[3].back());
        grp[3].pop_back();
    }

    if(grp[2].size() > grp[1].size())
    {
        cout<<-1;
        return 0;
    }

    while(!grp[2].empty())
    {
        vector<int> team = grp[2].back();
        grp[2].pop_back();

        vector<int> add = grp[1].back();
        grp[1].pop_back();

        vector<int> merge;

        for(int v : team)
        {
            merge.push_back(v);
        }

        for(int v : add)
        {
            merge.push_back(v);
        }

        ans.push_back(merge);
    }

    if(grp[1].size() % 3 != 0)
    {
        cout<<-1;
        return 0;
    }

    while(!grp[1].empty())
    {
        vector<int> team1 = grp[1].back();
        grp[1].pop_back();

        vector<int> team2 = grp[1].back();
        grp[1].pop_back();

        vector<int> team3 = grp[1].back();
        grp[1].pop_back();

        vector<int> merge;

        for(int v : team1)
        {
            merge.push_back(v);
        }

        for(int v : team2)
        {
            merge.push_back(v);
        }

        for(int v : team3)
        {
            merge.push_back(v);
        }

        ans.push_back(merge);
    }

    for(vector<int> team : ans)
    {
        for(int v : team)
        {
            cout<<v<<' ';
        }
        cout<<endl;
    }

    
}
```