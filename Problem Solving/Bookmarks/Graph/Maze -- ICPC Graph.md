[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/Q)
```C++
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int n,m,k;
vector<string> maze;
vector<vector<bool>> vis;
vector<pair<int,int>>emptyy;

int dx[] = {-1,1,0,0};
int dy[] = {0,0,-1,1};

void dfs(int u,int v)
{
    vis[u][v] = 1;
    emptyy.push_back({u,v});

    for(int i=0;i<4;i++)
    {
        int x = u + dx[i];
        int y = v + dy[i];

        if(x >=0 && x < n && y >= 0 && y < m && maze[x][y]=='.' && !vis[x][y])
        {
            dfs(x,y);
        }
    }
}

int main()
{
    cin>>n>>m>>k;
    maze.resize(n);
    vis.resize(n,vector<bool>(m,0));

    for(int i = 0; i < n; i++)
    {
        cin>>maze[i];
    }

    bool found = 0;
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            if(maze[i][j] == '.' && !found)
            {
                dfs(i,j);
                found = 1;
            }
        }
    }

    for(int i = emptyy.size() - 1; i >= emptyy.size() - k; i--)
    {
        maze[emptyy[i].first][emptyy[i].second] = 'X';
    }

    for(int i = 0;i < n; i++)
    {
        cout<<maze[i]<<endl;
    }

    return 0;
}
```