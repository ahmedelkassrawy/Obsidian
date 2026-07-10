[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/W)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <deque>
#include <algorithm>

using namespace std;

const int INF = 1e9; // Represent infinity

int n, m;
vector<vector<int>> grid;
int dx[] = {1, -1, 0, 0};
int dy[] = {0, 0, 1, -1};

bool valid(int i, int j)
{
    return i >= 0 && j >= 0 && i < n && j < m;
}

vector<vector<int>> bfs(int stx, int sty, int fav) {
    vector<vector<int>> dist(n, vector<int>(m, INF));
    deque<pair<int, int>> dq;

    dq.push_front({stx, sty});
    dist[stx][sty] = 0;

    while (!dq.empty()) {
        auto [x, y] = dq.front();
        dq.pop_front();

        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if(valid(nx, ny) && (grid[x][y] == 3 || grid[x][y] == fav) && dist[nx][ny] > dist[x][y]){
                dist[nx][ny] = dist[x][y];
                dq.push_front({nx, ny});
            }
            if(valid(nx, ny) && (grid[x][y] != 3 && grid[x][y] != fav) && dist[nx][ny] > dist[x][y] + 1){
                dist[nx][ny] = dist[x][y] + 1;
                dq.push_back({nx, ny});
            }
        }
    }

    return dist;
}

int main() {
    int t;
    cin >> t;

    while (t--) {
        cin >> n >> m;
        grid.assign(n, vector<int>(m));
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                cin >> grid[i][j];
            }
        }

        vector<vector<int>> eddard = bfs(0, 0, 2);
        vector<vector<int>> partner = bfs(n - 1, m - 1, 1);

        int ans = INT_MAX;
        for (int i = 0; i < n; ++i) 
        {
            for (int j = 0; j < m; ++j) 
            {
                ans = min(ans, eddard[i][j] + partner[i][j]);
            }
        }

        cout << ans << endl;
    }

    return 0;
}

```