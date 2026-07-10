[Problem - Z - Codeforces](https://codeforces.com/group/MWSDmqGsZm/contest/219158/problem/Z)
```C++
#include <iostream> 
#include <cmath>
using namespace std;
int main()
{
    double num1, num2, num3, num4;
    cin >> num1 >> num2 >> num3 >> num4;
    double res1 = num2 * log(num1);
    double res2 = num4 * log(num3);
    if (res1 > res2)
    {
        cout << "YES" << endl;
    }
    else
    {
        cout << "NO" << endl;
    }
}
```
![[Pasted image 20240419174921.png]]