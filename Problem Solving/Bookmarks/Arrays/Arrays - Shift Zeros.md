---
description: "C++ solution that moves every zero in an array to the end while keeping the other elements in order."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/arrays-and-hashing
aliases:
  - "Shift Zeros"
hubs:
  - "[[Arrays & Hashing]]"
---
```C++
#include <iostream>
using namespace std;
int main()
{
    int size;
    cin >> size;
    int *arr = new int[size];
    for (int i = 0; i < size; i++)
    {
        cin >> arr[i];
    }
    int zeros = 0;
    for (int i = 0; i < size; i++)
    {
        if (arr[i] != 0)
        {
            cout << arr[i] << " ";
        }
        else
        {
            zeros++;
        }
    }
    for (int i = 0; i < zeros; i++)
    {
        cout << 0 << " ";
    }
}
```

[Problem - N - Codeforces](https://codeforces.com/group/MWSDmqGsZm/contest/223205/problem/N)