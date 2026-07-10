```C++
#include <iostream>
using namespace std;
int main()
{
    int size;
    cin >> size;
    int *arr = new int[size];
    for (int i = 0; i < size; i++)
    {
        cin >> arr[i];
    }
    int zeros = 0;
    for (int i = 0; i < size; i++)
    {
        if (arr[i] != 0)
        {
            cout << arr[i] << " ";
        }
        else
        {
            zeros++;
        }
    }
    for (int i = 0; i < zeros; i++)
    {
        cout << 0 << " ";
    }
}
```

[Problem - N - Codeforces](https://codeforces.com/group/MWSDmqGsZm/contest/223205/problem/N)