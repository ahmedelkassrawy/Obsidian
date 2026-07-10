[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/W)
```C++
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstring>
#include <climits>
#include <algorithm>
#include <queue>
#include <stack>
#include <set>
#include <map>
using namespace std;

const int N = 5000000 + 5;

int t, a, b, dp[N][2];

int go(int fullness, int drink){
    if(fullness > t)
        return INT_MIN;

    if(dp[fullness][drink] != -1)
        return dp[fullness][drink];

    int op1 = fullness;
    int op2 = go(fullness + a, drink);
    int op3 = go(fullness + b, drink);
    int op4 = INT_MIN;
    if(drink == 0) op4 = go(fullness / 2, 1);

    return dp[fullness][drink] = max({op1, op2, op3, op4});
}

void solve()
{
    freopen("feast.in", "r", stdin);
    freopen("feast.out", "w", stdout);
    cin >> t >> a >> b;
    memset(dp, -1, sizeof dp);
    cout << go(0, 0);
}

```