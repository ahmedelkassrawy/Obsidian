[Problem - T - Codeforces](https://codeforces.com/group/MWSDmqGsZm/contest/219856/problem/T)

```C++
#include <iostream>
#include <algorithm>
#include <string>
using namespace std;
int main()
{
    string url; cin>>url;
    bool start = false;
    for (int i = 0; i < url.size(); i++)
    {
        if ((url[i] == '?' || url[i] == '&') && !start)
        {
            start = true;
            continue;
        }

        if (start)
        {
            if (url[i] != '=' && url[i] != '&')
            {
                cout << url[i];
            }
            else if (url[i] == '=')
            {
                cout << ": ";
            }
            else if (url[i] == '&')
            {
                cout << endl;
            }
        }
    }
}
```