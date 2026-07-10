[#Sheet 3 : Dynamic Programming (Recursive) - Virtual Judge](https://vjudge.net/contest/694272#problem/N)
```C++
#include <iostream>
#include <vector>
#include <cstring>
#include <climits>
using namespace std;
const int N = 2e5 + 5;

int n;
long long a[N];
long long dp[N][2];

long long go(int i, int parity) {
    // Base case
    if (i == n) return 0;
    
    if (dp[i][parity] != -1) return dp[i][parity];
    
    long long ch1 = go(i + 1, parity); //skip
    
    long long ch2;
    
    if (parity == 0) //0 even , 1 for odd
    {
        //kda 5lsna even n5o4 odd
        ch2 = a[i] + go(i + 1, 1);
    } 
    else 
    {
        //kda 5lsna odd n5o4 even
        ch2 = 2 * a[i] + go(i + 1, 0);
    }
    
    return dp[i][parity] = max(ch1, ch2);
}

int main() 
{
    cin >> n;
    for (int i = 0; i < n; i++) cin >> a[i];
    
    memset(dp, -1, sizeof(dp));
    cout << go(0, 0) << endl;
    
    return 0;
}
```