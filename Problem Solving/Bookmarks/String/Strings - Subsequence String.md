---
description: "C++ greedy two-pointer check that one string is a subsequence of another."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/string-algorithms
aliases:
  - "Subsequence String"
hubs:
  - "[[String Algorithms]]"
---
https://codeforces.com/group/MWSDmqGsZm/contest/219856/problem/M

```C++
#include <iostream>
#include <algorithm>
#include <string>
using namespace std;
int main()
{
    string str, test = "hello", temp;
    cin >> str;
    int index = 0;
    for (int i = 0; i < str.size(); i++)
    {
        if (str[i] == test[index])
        {
            temp.push_back(str[i]);
            index++;
        }
    }
    if (temp == test)
    {
        cout << "YES";
    }
    else
    {
        cout << "NO";
    }
}
    }
}
```

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[Strings - Max Subsequences]]
- [[Strings - Longest Palindromic Substring]]
- [[Strings - Decoding]]
- [[Strings - Anagram Check]]
- [[STL - Double Strings]]
%% related:end %%
