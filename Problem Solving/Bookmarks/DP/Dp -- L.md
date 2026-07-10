[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/L)
```C++
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int N = 2005;
int n, h, l, r;
vector<int> a;
int dp[N][N];

int go(int i, int t) 
{
    //base case
    if (i == n) return 0; 

    if (dp[i][t] != -1) return dp[i][t]; 
    

    int ch1 = (t + a[i]) % h; //howa da el time el gdeed
    //heteet el modulus gt mn chatgpt w notes
    int ch2 = (t + a[i] - 1) % h;

    int good1 = (l <= ch1 && ch1 <= r); //if time in range
    int good2 = (l <= ch2 && ch2 <= r); 

    return dp[i][t] = max(go(i + 1, ch1) + good1, go(i + 1, ch2) + good2);
}

int main() 
{
    cin >> n >> h >> l >> r;
    a.resize(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    memset(dp, -1, sizeof(dp)); 
    cout << go(0, 0) << endl; 
    return 0;
}

```