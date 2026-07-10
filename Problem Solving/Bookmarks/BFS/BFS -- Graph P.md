[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/P)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <array>
#include <map>
using namespace std;

int dx[8] = { 1, 0, -1, 0, 1, 1, -1, -1 };
int dy[8] = { 0, 1, 0, -1, -1, 1, -1, 1 };
map<pair<int,int>,vector<pair<int,int>>> adj; //pair mn w pair ila

int main()
{
    int x0,y0,x1,y1;
    cin >> x0 >> y0 >> x1 >> y1;

    int n;
    cin>>n;

    for(int i = 0; i < n; i++)
    {
        int r,a,b;
        cin>>r>>a>>b;

        for(int j = a; j <= b; j++)
        {
            adj[{r,j}]; //making sure that the key exists
        }

        for(int j = a; j <= b;j++)
        {
            for(int k = 0; k < 8; k++)
            {
                int nx = r + dx[k];
                int ny = j + dy[k];

                if(adj.count({nx,ny})) //if the key exists m3naha eno cell fadya
                {
                    adj[{r,j}].push_back({nx,ny}); //adding the edge between the two cells
                    adj[{nx,ny}].push_back({r,j});
                }
            }
        }
    }


    queue<pair<int,int>> q;
    map<pair<int,int>,int> dist; //pair x,y w distance b2a

    q.push({x0,y0});
    dist[{x0,y0}] = 0;

    while(!q.empty())
    {
        auto curr = q.front();
        q.pop();

        for(auto u : adj[curr])
        {
            if(!dist.count(u)) //if the cell is not visited
            {
                dist[u] = dist[curr] + 1;
                q.push(u);
            }
        }
    }

    cout<<(dist.count({x1,y1}) ? dist[{x1,y1}] : -1)<<endl;   
}
```