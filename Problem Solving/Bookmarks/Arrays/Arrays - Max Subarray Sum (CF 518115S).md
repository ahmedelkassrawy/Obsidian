---
description: "C++ solution that scans the array once keeping a running best sum (Kadane) to find the largest-sum contiguous subarray."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/arrays-and-hashing
aliases:
  - "Max Subarray Sum"
hubs:
  - "[[Arrays & Hashing]]"
---
https://codeforces.com/group/5pUldkahAU/contest/518115/problem/S
```C++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main()
{
    int n;
    cin>>n;

    long long arr[n] = {};

    for(int i = 0; i< n; i++)
    {
        cin>>arr[i];
    }
    long long maxsub = arr[0];
    long long cursum = 0;

    for(int i =0; i < n; i++)
    {
        if(cursum < 0)
        {
            cursum = 0;
        }
        cursum += arr[i];
        maxsub = max(maxsub , cursum);
    }
    cout<<maxsub;
}
```