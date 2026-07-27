[Sheet #2 | Binary Search - Virtual Judge](https://vjudge.net/contest/661083#problem/O)
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
    int t;
    cin>>t;
  
    while(t--)
    {
	    int n;
        cin >> n;

        vector<int> arr(n);
        for (int i = 0; i < n; i++)
        {
            cin >> arr[i];
        }


        int ans = 0;
        vector<int> validIndices;

        for (int i = 0; i < n; i++)
        {
            if (arr[i] < i + 1)
            { // Condition: a[i] < i + 1 (1-based index)
                // Count valid indices j < i using binary search
                ans += lower_bound(validIndices.begin(),validIndices.end(),arr[i]) - validIndices.begin();
                // Add current index (1-based) to validIndices
                validIndices.push_back(i + 1);
            }
        }
        cout << ans << '\n';
    }
}
```