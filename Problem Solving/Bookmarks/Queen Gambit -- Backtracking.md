```C++
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

vector<string> arr;

bool colvis[9];
bool diag1[17];
bool diag2[17];

int f(int row)
{
    if(row == 8)
    {
        return 1;
    }

    int ans = 0;

    for(int col = 0; col < 8; col++)
    {
        if(arr[row][col] == '*' || colvis[col] || diag1[row + col] || diag2[row - col + 8])
        {
            continue;
        }

        arr[row][col] = 'Q';
        colvis[col] = diag1[row + col] = diag2[row - col + 8] = 1;

        ans += f(row + 1);

		 //for again the backtracking
        arr[row][col] = '.'; 
        colvis[col] = diag1[row + col] = diag2[row - col + 8] = 0;
    }

    return ans;

}

int main() 
{
    arr.resize(8);

    for(int i = 0; i< 8; i++)
    {
        cin>>arr[i];
    }

    cout<<f(0)<<"\n";

}

```

```C++
colvis[n + 1];
diag1[row + col];
diag2[row - col + n];

bool colvis[n + 1];
bool diag1[n*2 + 1];
bool diag2[n*2 + 1];
```