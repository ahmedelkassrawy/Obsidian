```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

int n,m;
vector<vector<char>> grid;
vector<vector<bool>> vis;

int dx[] = {-1,1,0,0}; // up down left right
int dy[] = {0,0,-1,1}; // up down left right
//e3tbr eno da directions 3shan a3rf aro7 lel 7eta ely 3andy 3la 7sb el x w y
//up = x-1 , down = x+1 , left = y-1 , right = y+1

void dfs(int x , int y)
{
    vis[x][y] = 1; 

    for(int i = 0; i < 4; i++) //for loop 3shan aro7 lel 4 directions ely 3andy
    {
        int nx = x + dx[i]; //nx = new x
        int ny = y + dy[i]; //ny = new y

        if(nx >= 0 && nx < n && ny >= 0 && ny < m && !vis[nx][ny] && grid[nx][ny] == '.')
        {
            dfs(nx,ny);
        }
        //if condition 3shan a3rf eno el new x w y msh 3la el borders w msh visited w msh wall
        //checking if the new x and y are not out of the borders and not visited and not wall
    }

}

int main()
{
    cin >> n >> m;
    grid.resize(n,vector<char>(m));
    vis.resize(n,vector<bool>(m,0));

    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            cin >> grid[i][j];
        }
    }

    int cnt = 0;
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            if(!vis[i][j] && grid[i][j] == '.')
            {
                dfs(i,j);
                cnt++;
            }
        }
    }

    cout << cnt << endl;

    return 0;
}
```