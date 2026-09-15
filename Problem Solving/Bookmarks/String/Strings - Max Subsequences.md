---
description: "C++ solution counting the maximum subsequences that can be pulled out of the given string."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/string-algorithms
aliases:
  - "Max Subsequences"
hubs:
  - "[[String Algorithms]]"
---
[Problem - N - Codeforces](https://codeforces.com/group/MWSDmqGsZm/contest/219856/problem/N)

```C++
#include <iostream>
#include <string>
using namespace std;
int main()
{
    int size;
    cin >> size;
    
    string str;
    cin >> str;
    
    char temp = str[0];
    int counter = 1;
    
    for (int i = 1; i < size; i++)
    {
        if (str[i] != temp)
        {
            counter++;
            temp = str[i];
        }
    }
    cout<< counter;
}
```