[#Sheet 4 : Dynamic Programming (Iterative) - Virtual Judge](https://vjudge.net/contest/696069#problem/Y)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <string>
using namespace std;

const int INF = 1e9 + 7;

// Function for modular exponentiation (a^b % mod)
long long mod_pow(long long base, long long exp, long long mod) {
    long long result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {  // If odd, multiply with base
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp /= 2;
    }
    return result;
}

int main() 
{
    int n, m, k;
    cin >> n >> m >> k;

    vector<int> l(n), t(n);
    for (int i = 0; i < n; i++) {
        cin >> l[i] >> t[i];
    }

    vector<int> freq(26, 0);
    for (int i = 0; i < m; i++) {
        char c;
        cin >> c;
        freq[c - 'A']++;
    }

    vector<int> dp(k + 1, 0);
    dp[0] = 1;

    // Compute DP table
    for (int i = 1; i <= k; i++) {
        for (int j = 0; j < n; j++) {
            if (i - l[j] >= 0) {  // Ensure valid index
                dp[i] = (dp[i] + dp[i - l[j]]) % INF;
            }
        }
    }

    vector<int> cntways(n + 1, 0);
    for (int i = 0; i < n; i++) {
        if (k - l[i] >= 0) {  // Ensure valid index
            cntways[t[i]] = (cntways[t[i]] + dp[k - l[i]]) % INF;
        }
    }

    int ans = 1;
    for (auto x : freq) {
        if (x == 0) continue;  // Ignore unused letters

        int add = 0;
        for (int i = 1; i <= n; i++) {
            if (cntways[i] > 0) {  
                add = (add + mod_pow(cntways[i], x, INF)) % INF;  // Use modular exponentiation
            }
        }

        ans = (1LL * ans * add) % INF;  // Ensure multiplication doesn't overflow
    }

    cout << ans << endl;
    return 0;
}
```