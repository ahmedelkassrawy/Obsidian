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

