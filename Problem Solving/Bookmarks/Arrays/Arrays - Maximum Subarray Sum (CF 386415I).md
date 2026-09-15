---
description: "C++ solution for the maximum contiguous subarray sum on a Codeforces group problem, using a running sum reset at negatives."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/arrays-and-hashing
aliases:
  - "Maximum Subarray Sum"
hubs:
  - "[[Arrays & Hashing]]"
---
[Problem - I - Codeforces](https://codeforces.com/group/isP4JMZTix/contest/386415/problem/I)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    long long max_sum = arr[0];
    long long current_sum = arr[0];

    for (int i = 1; i < n; i++) {
        current_sum = max(arr[i], current_sum + arr[i]);
        max_sum = max(max_sum, current_sum);
    }

    cout << max_sum << endl;
    return 0;
}

```