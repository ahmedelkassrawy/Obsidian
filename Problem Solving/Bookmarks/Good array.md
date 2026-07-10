https://codeforces.com/group/u3Ii79X3NY/contest/270254/problem/R
```C++
#include <bits/stdc++.h>
using namespace std;
int freq[10000005]={0};
int main()
{
	int n ; cin>>n;
	int arr[n];
	long long sum = 0 ;
	for(int i = 0 ; i < n ; i ++)
    {
        cin>>arr[i];
        sum+=arr[i];
        freq[arr[i]]++;
    }
    int res[n];
    int j= 0 ;
    for(int i = 0 ; i < n ; i ++)
    {
        freq[arr[i]]--;
        sum-=arr[i];
        if(sum%2==0 && sum/2<=1e6 && freq[sum/2]>0)
        {
            res[j]=i;
            j++;
        }
        freq[arr[i]]++;
        sum+=arr[i];
 
    }
    cout<<j<<"\n";
    for(int i=0 ; i < j ; i ++)
    {
        cout<<res[i]+1<<" ";
    }
 
 
}
```