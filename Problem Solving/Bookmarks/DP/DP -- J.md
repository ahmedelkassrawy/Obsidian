[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/J)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
using namespace std;

const int N = 101;
int n;
int a[N];
int dp[N][3];

//on this day the gym is closed and the contest is not carried out; --> 0
// on this day the gym is closed and the contest is carried out; --> 1
// on this day the gym is open and the contest is not carried out; --> 2
// on this day the gym is open and the contest is carried out

int go(int i, int last)
{
    //base case
    if(i == n) return 0;


    if(dp[i][last] != -1) return dp[i][last];

    int res = go(i + 1,0) + 1; //rest
    if(last != 1 && (a[i] == 3 || a[i] == 1)) res = min(res,go(i + 1, 1)); //contest is carried out
    if(last != 2 && (a[i] == 3 || a[i] == 2)) res = min(res,go(i + 1, 2)); //gym is open

    return dp[i][last] = res;
}

int main()
{
    cin>>n;
    for(int i=0; i<n; i++) cin>>a[i];
    memset(dp, -1, sizeof(dp));
    cout<<go(0, 0)<<endl;
}
```