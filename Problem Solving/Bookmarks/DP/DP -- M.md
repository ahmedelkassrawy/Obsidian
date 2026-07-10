[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/M)
```C++
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 2005;  // Slightly increased to ensure safety
const int M = 2005;
string a, b, c;
int dp[N][M];

int go(int i, int j) 
{
    // Base case
    if (i == a.size() && j == b.size()) return 0;

    if (dp[i][j] != -1) return dp[i][j];

    int ch1 = INT_MAX, ch2 = INT_MAX;

    if (i < a.size()) 
        if(a[i] == c[i + j])ch1 = go(i + 1, j) + 0;
        else ch1 = go(i + 1, j) + 1;

    if (j < b.size()) 
        if(b[j] == c[i + j]) ch2 = go(i, j + 1) + 0;
        else ch2 = go(i, j + 1) + 1;

    return dp[i][j] = min(ch1, ch2);
}

int main() 
{
    int t;
    cin >> t;

    while (t--) 
    {
        cin >> a >> b >> c;
        memset(dp, -1, sizeof(dp)); 
        cout << go(0, 0) << endl;
    }
}
```