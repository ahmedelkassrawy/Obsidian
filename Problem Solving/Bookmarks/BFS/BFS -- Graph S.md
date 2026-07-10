[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/S)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <array>
#include <map>
#include <climits> // For INT_MAX
using namespace std;

struct state
{
    int x, y;
    bool is_closed; // 1 for closed, 0 for open
};

int n, m;
int dx[4] = {1, 0, -1, 0};
int dy[4] = {0, 1, 0, -1};

bool valid(int i, int j)
{
    return i >= 0 && j >= 0 && i < n && j < m;
}

int main()
{
    while (cin >> n >> m && n != -1)
    {
        vector<vector<char>> grid(n, vector<char>(m));

        int x, y;

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                cin >> grid[i][j];

                if (grid[i][j] == 'H')
                {
                    x = i;
                    y = j;
                    grid[i][j] = '.'; // Make it passable
                }
            }
        }

        vector<vector<vector<int>>> dist(n, vector<vector<int>>(m, vector<int>(2, -1)));
        // 3D array to store distance; 3rd dimension is for door state (0=open, 1=closed)
        queue<state> q;

        q.push({x, y, 1});
        dist[x][y][1] = 0; // Starting position with the door closed

        while (!q.empty())
        {
            auto [x, y, is_closed] = q.front();
            q.pop();

            for (int i = 0; i < 4; i++)
            {
                int nx = x + dx[i];
                int ny = y + dy[i];

                if (!valid(nx, ny) || grid[nx][ny] == 'W')
                    continue; // If the cell is out of bounds or a wall, skip

                if (grid[nx][ny] == '.')
                {
                    if (dist[nx][ny][is_closed] == -1) // If cell not visited
                    {
                        dist[nx][ny][is_closed] = dist[x][y][is_closed] + 1;
                        q.push({nx, ny, is_closed});
                    }
                }
                else if (grid[nx][ny] == 'O') // Open door
                {
                    if (dist[nx][ny][0] == -1)
                    {
                        dist[nx][ny][0] = dist[x][y][is_closed] + 1;
                        q.push({nx, ny, 0});
                    }
                }
                else if (grid[nx][ny] == 'C') // Closed door
                {
                    if (dist[nx][ny][1] == -1)
                    {
                        dist[nx][ny][1] = dist[x][y][is_closed] + 1;
                        q.push({nx, ny, 1});
                    }
                }
                else if (!is_closed) // If the door is open
                {
                    if (dist[nx][ny][0] == -1)
                    {
                        dist[nx][ny][0] = dist[x][y][is_closed] + 1;
                        q.push({nx, ny, 0});
                    }
                }
            }
        }

        int ans = INT_MAX; // Initialize with a large number

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                if (i == 0 || j == 0 || i == n - 1 || j == m - 1) // Check boundary cells
                {
```
                    if (dist[i][j][0] != -1)
                        ans = min(ans, dist[i][j][0] + 1);
                    if (dist[i][j][1] != -1)
                        ans = min(ans, dist[i][j][1] + 1);
```
                }
            }
        }

        cout << (ans == INT_MAX ? -1 : ans) << endl;
    }
}
```