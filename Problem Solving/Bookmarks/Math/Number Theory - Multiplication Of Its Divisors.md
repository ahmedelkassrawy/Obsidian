---
description: "C++ solution that multiplies all divisors of n, walking only up to sqrt(n) and pairing each divisor with its partner."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/math-and-number-theory
aliases:
  - "Multiplication Of its divisors"
hubs:
  - "[[Math & Number Theory]]"
---
https://codeforces.com/group/MWSDmqGsZm/contest/223338/problem/G

```C++
#include <iostream>
#include <cmath>
using namespace std;
int main()
{
    int num,sum = 0;
    cin>>num;
    for(int i =1; i <= sqrt(num); i++)
    {
        if(num % i == 0)
        {
            sum += i;
            if(i != sqrt(num))
                sum += (num /i);
        }
    }
    cout<<sum;
}
```

