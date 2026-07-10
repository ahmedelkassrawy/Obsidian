[Sheet #5 | Recursion and Backtracking - Virtual Judge](https://vjudge.net/contest/669349#problem/E)
```C++
#include <iostream>
#include <vector>
using namespace std;

vector<long long> arr;
long long n;

long long f(long long i,long long sum1,long long sum2) 
{
    if(i == n) return abs(sum1 - sum2);

    long long op1 = f(i + 1,sum1 + arr[i],sum2);
    long long op2 = f(i + 1,sum1,sum2 + arr[i]);

    return min(op1,op2);
}

int main() 
{
    cin>>n;
    arr.resize(n);

    for(int i = 0; i< n; i++)
    {
        cin>>arr[i];
    }

    long long min = f(0,0,0);
    cout<<min<<"\n";

}
```