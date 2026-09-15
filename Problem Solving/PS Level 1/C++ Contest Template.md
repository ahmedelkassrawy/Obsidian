---
description: "The contest boilerplate: the usual includes plus the sync_with_stdio / cin.tie fast-IO lines."
domain: cs
type: reference
status: stub
tags:
  - domain/cs
  - type/reference
  - status/stub
  - topic/c-language
aliases:
  - "MUST HAVE"
  - "boilerplate"
hubs:
  - "[[C++ Language]]"
---
# MUST HAVE

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <math.h>
#include <algorithm>
#include <numeric>
using namespace std;

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
}
```
