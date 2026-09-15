---
description: "Hub page for the CPP folder - a list of links to the other C++ notes plus one setprecision snippet."
domain: cs
type: meta
status: stub
tags:
  - domain/cs
  - type/meta
  - status/stub
  - topic/c-language
aliases:
  - "C++ index"
hubs:
  - "[[C++ Language]]"
---
[[Constructor]]
[[Classes]]
[[Problem Solving/PS Level 1/Struct With Custom Comparator]]
[[References]]
[[Pointers]]
[[CPP/Lambda And Map]]
[[CPP/OOP]]
[[Local and Global Variables]]
[[Forward Declaration]]
[[Header Files]]
[[Sets]]
Set precision
```C++
#include <iomanip> // for output manipulator std::setprecision()
#include <iostream>

int main()

{
    std::cout << std::setprecision(9); // show 17 digits of preision
    std::cout << 3.33333333333333333333333333333333333333f <<'\n'; // f suffix means float
    std::cout << 3.33333333333333333333333333333333333333 << '\n'; // no suffix means double
    return 0;

??if you want to make the peresicion fixed: 
 cout << fixed << setprecision(2) << num;
}
```

[4.9 — Boolean values – Learn C++ (learncpp.com)](https://www.learncpp.com/cpp-tutorial/boolean-values/)
