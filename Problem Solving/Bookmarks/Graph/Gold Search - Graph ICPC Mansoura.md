[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/L)
```C++
#include <iostream>
#include <vector>
using namespace std;

int n, m;
vector<vector<char>> adj;
vector<vector<bool>> vis;

int dx[] = {-1, 1, 0, 0}; 
int dy[] = {0, 0, -1, 1};  

int dfs(int x, int y) //recursive calls
{
    vis[x][y] = true;
    
    //first check for traps and curr gold
    for (int i = 0; i < 4; i++) 
    {
        int nx = x + dx[i];
        int ny = y + dy[i];

        if (adj[nx][ny] == 'T') //checking if the new direction has a trap
        {
            return (adj[x][y] == 'G') ? 1 : 0; //if the curr x,y have a gold return 1 or return 0
        }
    }

    int gold = (adj[x][y] == 'G') ? 1 : 0; //checking if the curr pos ana wa2f feh has gold or not

    //search all directions for gold
    for (int i = 0; i < 4; i++) 
    {
        int nx = x + dx[i];
        int ny = y + dy[i];

        if (nx >= 0 && nx < n && ny >= 0 && ny < m && !vis[nx][ny] && adj[nx][ny] != '#') {
            gold += dfs(nx, ny);
        }
    }

    return gold;
}

int main() {
    while (cin >> m >> n) 
    {  
        adj.assign(n, vector<char>(m));
        vis.assign(n, vector<bool>(m, false));

        pair<int, int> player;

        for (int i = 0; i < n; i++) 
        {
            for (int j = 0; j < m; j++) 
            {
                cin >> adj[i][j];

                if (adj[i][j] == 'P') 
                {
                    player = {i, j};  //start position
                }
            }
        }

        // Starting mn 3and p
        cout << dfs(player.first, player.second) << endl;
    }
    
    return 0;
}

```