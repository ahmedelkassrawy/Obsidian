[Sheet #2 | Binary Search - Virtual Judge](https://vjudge.net/contest/661083#problem/G)
```C++
#include <iostream>
#include <set>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <queue>
#include <deque>
#include <unordered_map>
using namespace std;
int n,goal;

bool can(long long time,vector<int> &machines,int &goal)
{
    long long totalproducts = 0;
    for(int i = 0;i < n; i++)
    {
        totalproducts += time/machines[i];
        if(totalproducts >= goal)
        {
            return true;
        }
    }
    return totalproducts >= goal;
    
}

int main() 
{
    cin>>n>>goal;

    vector<int> machines(n);
    for(int i = 0; i < n; i++)
    {
        cin>>machines[i];
    }

    long long l =1,r=1e18,mid,ans;
    while(l <= r)
    {
        mid = l + (r-l)/2;
        if(can(mid,machines,goal))
        {
            ans = mid;
            r = mid - 1;
        }
        else
        {
            l = mid + 1;
        }
    }

    cout<<ans;
}
```