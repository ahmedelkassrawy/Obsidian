### lower bound
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

  
int main()
{
    int n,q;
    cin>>n>>q;
  
    int arr[n] = {};
    for(int i = 0; i< n; i++)
    {
        cin>>arr[i];
    } 

    while(q--)
    {
        int x;
        cin>>x;

        int l = 0,r = n - 1, mid = 0;
        int ans = -1; //cause if the target x is not available in the array
        //then printing the answer with -1

        while(l <= r)
        {
            mid = (l+r) /2;
            if(arr[mid] >= x)
            {
                r = mid - 1;
                ans = mid + 1;
            }
            else
            {
                l = mid + 1;
            }
        }
        cout<<ans<<endl;
    }
}
```

### upper bound

diff between upper bound and lower bound we wanted the fnumber >= target now we only want the number > target
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


int main()
{
    int n,q;
    cin>>n>>q;

    int arr[n] = {};
    for(int i = 0; i< n; i++)
    {
        cin>>arr[i];
    }


    while(q--)
    {
        int x;
        cin>>x;

        int l = 0,r = n - 1, mid = 0;
        int ans = -1; //cause if the target x is not available in the array 
        //then printing the answer with -1

        while(l <= r)
        {
            mid = (l+r) /2;
            if(arr[mid] > x)
            {
                r = mid - 1;
                ans = mid + 1;
            }
            else
            {
                l = mid + 1;
            }
        }
        cout<<ans<<endl;
    }  
}
```

### Using STLS for the upper, lower
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

  
int main()
{
    int n,q;
    cin>>n>>q;
    
    vector<int> arr(n);
    for(int i = 0; i< n; i++)
    {
        cin>>arr[i];
    }

    while(q--)
    {
        int x;
        cin>>x;
        
        auto it = upper_bound(arr.begin(),arr.end(),x);

        if(it == arr.end())
        {
            cout<<-1;
        }
        else
        {
            int ans = it - arr.begin();
            cout<<ans + 1<<endl; //for 1 indexed
        }
    }
}
```