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
