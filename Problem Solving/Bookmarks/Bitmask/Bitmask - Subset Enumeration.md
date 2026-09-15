---
description: "Explains the subset-enumeration loop: an integer bitmask stands for a subset, bit j set means element j is included, so looping 0..2^n-1 walks every subset."
domain: cs
type: concept
status: digested
tags:
  - domain/cs
  - type/concept
  - status/digested
  - topic/bitmask
aliases:
  - "subset enumeration"
  - "2^n loop"
hubs:
  - "[[Bitmask]]"
---
```C++
for(int mask = 0; mask < (1 << n); mask++)
    {
        sum = 0,mx = 0, mn = LLONG_MAX;

        if(bit_count(mask) < 2)
        {
            continue;
        }

        for(int i = 0; i < n; i++)
        {
            if((mask & (1 << i)) == 0)
            {
                continue;
            }
```


bitmask: Encodes a subset of the array where:
If the 
𝑗
j-th bit in bitmask is 1, then the 
𝑗
j-th element of arr is included in the subset.
If the 
𝑗
j-th bit is 0, the element is excluded.
