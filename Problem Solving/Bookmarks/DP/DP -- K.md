[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/K)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
using namespace std;

const int N = 2e5 + 5;
int n,t;
int a[N];
int dp[N];

int go(int i)
{
    //base case
    if(i > n) return INT_MAX;
    if(i == n) return 0;

    if(dp[i] != -1) return dp[i];

    int ch1 = go(i + 1) + 1; //remove curr element , move to next idx
    int ch2 = go(i + a[i] + 1); //start from i + the number of steps and add 1 

    return dp[i] = min(ch1,ch2);
}

int main()
{
    cin>>t;

    while(t--)
    {
        cin>>n;
        for(int i=0;i<n;i++) cin>>a[i];
        memset(dp,-1,sizeof(dp));
        cout<<go(0)<<endl;
    }
}
```