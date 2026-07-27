[Sheet #2 | Binary Search - Virtual Judge](https://vjudge.net/contest/661083#problem/H)
```C++
#include <iostream>
#include <vector>
using namespace std;

int n, k;

// Function to check if `cookies` can be baked
bool can(int cookies, vector<int>& have, vector<int>& need) 
{
    long long needmagic = 0;

    for (int i = 0; i < n; i++) 
    {
        // Check if additional magic powder is needed
        if (1LL * cookies * need[i] > have[i]) 
        {
            needmagic += (1LL * cookies * need[i] - have[i]);
        }
        // If magic powder exceeds available limit, return false
        if (needmagic > k) 
        {
            return false;
        }
    }
    return true;
}

int main() 
{
    cin >> n >> k;

    vector<int> have(n), need(n);
    for (int i = 0; i < n; i++) 
    {
        cin >> need[i];
    }
    for (int i = 0; i < n; i++) 
    {
        cin >> have[i];
    }

    int l = 0, r = 2e9, mid, ans = 0;

    while (l <= r) 
    {
        mid = l + (r - l) / 2;  
        if (can(mid, have, need)) 
        {
            ans = mid;  
            l = mid + 1;  
        } 
        else 
        {
            r = mid - 1;  
        }
    }

    cout << ans << endl;  
}
```