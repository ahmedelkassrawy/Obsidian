[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/V)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

int n, m, k;
vector<vector<char>> grid;
vector<vector<int>> cost(26, vector<int>(26)); // Minimum cost to place character j after i
int di[] = {1, -1, 0, 0};
int dj[] = {0, 0, 1, -1};

vector<int> bfs(int c)
{
    queue<pair<int, int>> q;
    vector<vector<int>> dist(n, vector<int>(m, -1));
    vector<int> curcost(26, -1); // Minimum cost from c to all characters

    curcost[c] = 0; // Cost to place 'c' after 'c' is 0

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            if (grid[i][j] == char(c + 'a'))
            {
                q.push({i, j});
                dist[i][j] = 0;
            }
        }
    }

    while (!q.empty())
    {
        auto [i, j] = q.front();
        q.pop();

        for (int d = 0; d < 4; d++)
        {
            int nx = i + di[d];
            int ny = j + dj[d];

            if (nx >= 0 && nx < n && ny >= 0 && ny < m && dist[nx][ny] == -1)
            {
                dist[nx][ny] = dist[i][j] + 1;

                if (curcost[grid[nx][ny] - 'a'] == -1 || curcost[grid[nx][ny] - 'a'] > dist[nx][ny])
                {
                    curcost[grid[nx][ny] - 'a'] = dist[nx][ny];
                }

                q.push({nx, ny});
            }
        }
    }

    return curcost;
}

int main()
{
    int t;
    cin >> t;

    while (t--)
    {
        cin >> n >> m >> k;
        grid.assign(n, vector<char>(m));
        cost.assign(26, vector<int>(26, -1));

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                cin >> grid[i][j];
            }
        }

        for (int i = 0; i < 26; i++)
        {
            cost[i] = bfs(i);
        }

        string target;
        cin >> target;

        long long ans = 0;
        for (int i = 1; i < target.size(); i++)
        {
            if (cost[target[i - 1] - 'a'][target[i] - 'a'] == -1)
            {
                ans = -1;
                break;
            }
            ans += cost[target[i - 1] - 'a'][target[i] - 'a'];
        }
        
        cout << ans << endl;
    }
}

```