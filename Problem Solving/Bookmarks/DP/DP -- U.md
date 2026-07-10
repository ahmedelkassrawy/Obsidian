[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/U)
```C++
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1e8;
int dp[101][101][2];
int n1,n2,k1,k2;

int go(int f, int h, int last)
{
    //base case
    if(f == 0 && h == 0) return 1;

    if(dp[f][h][last] != -1) return dp[f][h][last];

    int ans = 0;

    if(last == 0) //footman
    {
        for(int j = 1; j <= min(k2,h); j++)
        {
            int left = h - j;
            ans += go(f, left, 1);
            ans %= MOD;
        }
    }
    else //horseman
    {
        for(int i = 1; i <= min(k1,f); i++)
        {
            int left = f - i;
            ans += go(left, h, 0);
            ans %= MOD;
        }
    }

    return dp[f][h][last] = ans;

}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin>>n1>>n2>>k1>>k2;

    memset(dp, -1, sizeof(dp));

    int ch1 = go(n1,n2,0); //starting with footman
    int ch2 = go(n1,n2,1); //starting with horseman

    cout<<(ch1 + ch2) % MOD<<endl;
}
```

```C++
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1e8;
int n1,n2,k1,k2;
int dp[105][105][15][15];

int go(int nn1, int nn2, int limit1, int limit2){
    if(nn1 > n1 || nn2 > n2 || limit1 > k1 || limit2 > k2)
        return 0;

    if(nn1 == n1 && nn2 == n2)
        return 1;

    if(dp[nn1][nn2][limit1][limit2] != -1)
        return dp[nn1][nn2][limit1][limit2];

    int op1 = go(nn1 + 1, nn2, limit1 + 1, 0);
    int op2 = go(nn1, nn2 + 1, 0, limit2 + 1);
    //the limit1 or limit2 is zero 34an mfee4 5las moslsat wra b3d zero hrfyn
    return dp[nn1][nn2][limit1][limit2] = (op1 % MOD + op2 % MOD) % MOD;
}

int main()
{
    cin >> n1 >> n2 >> k1 >> k2;
    memset(dp, -1, sizeof dp);
    cout << go(0,0,0,0) << endl;
    return 0;
}
```