[Sheet #2 | Binary Search - Virtual Judge](https://vjudge.net/contest/661083#problem/T)

```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

bool can(long long mid, long long a, vector<long long>& personal, vector<long long>& rent) {
    long long sum = 0;
    for (int i = 0; i < mid; i++) {
        sum += max(0LL, rent[i] - personal[mid - 1 - i]);
    }
    return sum <= a;
}

int main() {
    long long n, m, a;
    cin >> n >> m >> a;

    vector<long long> personal(n);
    for (int i = 0; i < n; i++) {
        cin >> personal[i];
    }

    vector<long long> rent(m);
    for (int i = 0; i < m; i++) {
        cin >> rent[i];
    }

    // Sort personal in descending order and rent in ascending order
    sort(personal.rbegin(), personal.rend());
    sort(rent.begin(), rent.end());

    long long l = 0, r = min(n, m), maxRentableBoys = 0;

    // Binary search for the maximum number of rentable boys
    while (l <= r) {
        long long mid = l + (r - l) / 2;

        if (can(mid, a, personal, rent)) {
            maxRentableBoys = mid;
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }

    // Calculate the minimum personal money needed
    long long minPersonal = 0;
    for (int i = 0; i < maxRentableBoys; i++) {
        minPersonal += rent[i];
    }

    // Output results
    cout << maxRentableBoys << " " << max(0LL, minPersonal - a) << endl;

    return 0;
}
```