[Sheet #1 | Adhocs & Two Pointers - Virtual Judge](https://vjudge.net/contest/659188#problem/T)
```C++
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

  

int main()
{
    int n;
    cin>>n;

    int nums[n] = {};
    int l =0;
    int r = 0;
    int total = 0;
  
    for(int i = 0; i < n; i++)
    {
        cin>>nums[i];
    }

  
    while(r < n)
    {
        if(l == r)
        {
            total++;
        }
        else
        {
            if(nums[r-1] - nums[r] == nums[l] - nums[l+1])
            {
                total += r -l + 1;
            }
            else
            {
               l = r-1;
               total += 2;
            }
        }
        r++;
    }
    cout<<total;
}
```