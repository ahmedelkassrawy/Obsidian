to check the bits of the number in array
```C++
for (int bit = 30; bit >= 0; bit--)
{
	 int cost = 0;
	 
	 for (int i = 0; i < n; i++)
	 {
		if ((arr[i] & (1 << bit)) == 0) cost++;
	 }
}
```

```C++
for(int mask = 0; mask < (1 <<n); mask++)
    {
        int mn = 2e9,mx = 0,cnt = 0,sum = 0;
        for(int i = 0; i < n; i++)
        {
            if(mask & (1<<i))
            {
                cnt++;
                sum += arr[i];
                mn = min(mn,arr[i]);
                mx = max(mx,arr[i]);
            }
        }
```