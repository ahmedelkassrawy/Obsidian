[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/E)
```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <climits>
using namespace std;

const int N = 1001;
int n;
char grid[N][N];
int dp[N][N];
int mod = 1e9 + 7;

int go(int i,int j)
{
    // Base case:
    if(i == n -1 && j == n -1) return 1;
    if(i >= n || j >= n) return 0;
    if(grid[i][j] == '*') return 0;

    if(dp[i][j] != -1) return dp[i][j];

    int ch1 = 0, ch2 = 0;

    if(grid[i + 1][j] == '.' && i + 1 < n)
    {
        ch1 = go(i + 1, j) % mod;
    }
    if(grid[i][j + 1] == '.' && j + 1 < n)
    {
        ch2 = go(i, j + 1) % mod;
    }

    return dp[i][j] = (ch1 + ch2) % mod;
}

int main()
{
    cin >>n;
    for(int i = 0;i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            cin >> grid[i][j];
        }
    }

    memset(dp, -1, sizeof(dp));

    if(grid[n - 1][n - 1] == '*')
    {
        cout << 0 << endl;
        return 0;
    }

    cout << go(0,0) << endl;
}

```