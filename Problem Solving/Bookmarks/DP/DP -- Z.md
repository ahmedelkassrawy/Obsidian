[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/Z)
```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
#include <cmath>
#include <string>
#include <map>
#include <set>
#include <stack>
#include <climits>
using namespace std;

string s,t;
int dp[205][205][205];
char open = '(', close = ')';
int n,m;
string ans;

int go(int i , int j, int sum)
{
    //base case
    if(i == n && j == m) return sum; //kda yb2a 5lsna
    
    if(dp[i][j][sum] != -1) return dp[i][j][sum];

    int op1 = INT_MAX,op2 = INT_MAX;

    if(s[i] == open || t[j] == open)
    {
        op1 = go(i + (s[i] == open), j + (t[j] == open), sum + 1) + 1;
    }

    if(s[i] == close || t[j] == close)
    {
        op2 = go(i + (s[i] == close), j + (t[j] == close), (sum ? sum - 1 : 0)) + 1 + (sum == 0); 
        //checking for the close bracket
        //checking if the sum is 0 m3na kda en elbrackets lfatt et2aflt already dy bdaya gdeeda
        //we checking if the sum = 0 at the end
    }

    return dp[i][j][sum] = min(op1,op2);
}

void build(int i , int j, int sum)
{
    //base case
    if(i == n && j == m) return; //kda yb2a 5lsna

    int op1 = INT_MAX,op2 = INT_MAX;

    if(s[i] == open || t[j] == open)
    {
        op1 = go(i + (s[i] == open), j + (t[j] == open), sum + 1) + 1;
    }

    if(s[i] == close || t[j] == close)
    {
        op2 = go(i + (s[i] == close), j + (t[j] == close), (sum ? sum - 1 : 0)) + 1 + (sum == 0); 
        //checking for the close bracket
        //checking if the sum is 0 m3na kda en elbrackets lfatt et2aflt already dy bdaya gdeeda
        //we checking if the sum = 0 at the end
    }

    //begin the backtracking w build
    int optimal = min(op1,op2);

    if(optimal == op1)
    {
        ans += open;
        build(i + (s[i] == open), j + (t[j] == open), sum + 1);
    }
    else
    {
        if(sum == 0) ans += '()';
        else ans += close;

        build(i + (s[i] == close), j + (t[j] == close), (sum ? sum - 1 : 0));
    }
}

int main()
{
    cin>>s>>t;
    n = s.size();
    m = t.size();

    memset(dp,-1,sizeof(dp));

    int opens = 0;

    for(char c: ans)
    {
        if(c == open) opens++;
        else opens--;
    }

    while(opens-- > 0) ans += close; //34an el brackets elzyada lmfot7a dy y2flha
    cout<<ans<<endl;
    return 0;
}
```