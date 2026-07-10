[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/G)
```C++
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int dx[] = {1, 1, -1, -1, 2, 2, -2, -2};
int dy[] = {2, -2, 2, -2, 1, -1, 1, -1};

int bfs(string start, string end) {
    int sx = start[0] - 'a';
    int sy = start[1] - '1';
    int ex = end[0] - 'a';
    int ey = end[1] - '1';

    if (sx == ex && sy == ey) return 0; // Already at destination

    queue<pair<int, pair<int, int>>> q;
    vector<vector<bool>> vis(8, vector<bool>(8, false)); // Reset for each test case

    q.push({0, {sx, sy}});
    vis[sx][sy] = true;

    while (!q.empty()) {
        int moves = q.front().first;
        int x = q.front().second.first;
        int y = q.front().second.second;
        q.pop();

        for (int i = 0; i < 8; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if (nx >= 0 && nx < 8 && ny >= 0 && ny < 8 && !vis[nx][ny]) {
                if (nx == ex && ny == ey) {
                    return moves + 1;
                }
                vis[nx][ny] = true;
                q.push({moves + 1, {nx, ny}});
            }
        }
    }

    return -1; // This should never happen for a valid chessboard
}

int main() 
{
    string start, end;

    while (cin >> start >> end) 
    {
        cout << "To get from " << start << " to " << end << " takes " << bfs(start, end) << " knight moves." << endl;
    }

    return 0;
}
```