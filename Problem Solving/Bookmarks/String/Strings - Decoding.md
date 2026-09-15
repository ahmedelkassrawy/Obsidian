---
description: "C++ decoding solution; the comment notes this version saves more memory than the author's second attempt."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/string-algorithms
aliases:
  - "Decoding"
hubs:
  - "[[String Algorithms]]"
---
https://codeforces.com/group/MWSDmqGsZm/contest/223206/problem/Z
```C++
#include <iostream>
#include <algorithm>
#include <cstring>

using namespace std;
int main()
{
    // this solution is save more memory than solution2
    int size;
    cin >> size;

    string encode;
    cin >> encode;

    char *decode = new char[size];

    int left = size / 2;
    int right = size / 2;

    int index = 0;
    // vol
    for (int i = size; i > 0; i--)
    {
        if (i == size)
        {
            decode[left] = encode[index];
            left--;
        }

        if (i % 2 == 0) // even -> left
        {
            decode[left] = encode[index];
            left--;
        }
        else // odd -> right
        {
            decode[right] = encode[index];
            right++;
        }

        index++;
    }

    for (int i = 0; i < size; i++)
    {
        cout << decode[i];
    }
}
```

