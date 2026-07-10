[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/T)

```C++
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1e9 + 7;
int n, m;
int dp[3001][3001];

int go(int x,int y)
{
    if(x > n || y > m) return 0;
    if(x == n && y == m) return 1;

    if(dp[x][y] != -1) return dp[x][y];

    int ch1 = go(x+1, y);
    int ch2 = go(x, y+1);

    return dp[x][y] = (ch1 + ch2) % MOD;
}

int main()
{
    int t;
    cin>>t;

    while(t--)
    {
        cin>>n>>m;
        
        memset(dp, -1, sizeof(dp));

        cout<<go(1, 1)<<endl;
    }
}
```

This will get us time limit so why dont we just go the other way, nm4y mn elsabt llmot8yr b7ees eny myb2a4 el values fl grid bbt8yr wtt7sb m3 kol text case all over again
```C++

```