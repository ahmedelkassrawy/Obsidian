[Sheet #2 | Binary Search - Virtual Judge](https://vjudge.net/contest/661083#problem/N)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

bool can(int k, int size, vector<pair<int, int>> &v) {
    int leftPos = 0, rightPos = 0;

    for (int i = 0; i < size; i++) 
    {
        // Check if the current range is valid considering k
        if (leftPos - k > v[i].second) return false;  // Can't move to the next segment
        if (rightPos + k < v[i].first) return false; // Can't reach the next segment

        // Update the valid range
        leftPos = max(v[i].first, leftPos - k);
        rightPos = min(v[i].second, rightPos + k);
    }
    return true;
}

int main() {
    int t;
    cin >> t;  // Number of test cases

    while (t--) {
        int n;
        cin >> n;  // Number of segments

        vector<pair<int, int>> v(n);

        // Read the segments
        for (int i = 0; i < n; i++) 
        {
            int l, r;
            cin >> l >> r;
            v[i] = {l, r};
        }

        // Binary search to find the minimum k
        int l = 0, r = 1e9, mid, ans = 0;
        while (l <= r) {
            mid = l + (r - l) / 2;
            if (can(mid, n, v)) {
                ans = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }

        cout << ans << endl;  // Output the result for this test case
    }

    return 0;
}
```

![[photo_2024-11-22_16-33-53.jpg]]