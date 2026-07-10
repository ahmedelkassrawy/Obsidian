[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/R)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstring>
#include <climits>
using namespace std;

const int N = 1e5 + 3;
int n,mx;
int dp[N];
vector<int> freq(N);

int go(int i)
{
    if(i > mx) return 0; //if the number exceeds the max number then we return 0

    if(dp[i] != -1) return dp[i];

    int op1 = go(i + 1); //leave
    int op2 = go(i + 2) + freq[i]*i; //take , skip the number at (i + 1) to
    //satisfy the removal
    
    return dp[i] = max(op1, op2);
}

int main()
{
    cin>>n;

    for(int i = 0; i < n; i++)
    {
        int x;
        cin>>x;
        freq[x]++;
        mx = max(mx,x); //34an mn3dee4 limit
    }

    memset(dp,-1,sizeof(dp));

    cout<<go(1);
}
```