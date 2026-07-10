### Subarray 
is a contiguous part of an array.
since [1,2,3,4]
(1), (2), (3), (4), (1,2), (2,3), (3,4), (1,2,3), (2,3,4), and (1,2,3,4)
rule = n*(n+1)/2

Counting how many subarrays

```C++
#include <iostream>
using namespace std;

int main()
{
    int t;
    cin>>t;
    while(t--)
    {
        int size;
        cin >> size;
        int arr[size] = {};
        
        for (int i = 0; i < size; i++)
            cin >> arr[i];
            
        int counter = 0;
        
        for (int i = 0; i < size; i++)
        {
            for (int j = i; j < size; j++)
            {
                if (i == j)
                {
                    counter++;
                    continue;
                }

                if (arr[j] > arr[j - 1])
                    counter++;
                else
                    break;
            }
        }
        cout << counter << endl;
    }
}
```

### Subsequence 
A ****subsequence**** is a sequence that can be derived from another sequence by removing zero or more elements, without changing the order of the remaining elements.

## Multi Dimensional Array (2D)

```C++
#include <iostream>
using namespace std;
int main()
{
    int row,col;
    cin>>row>>col;
    int arr[row][col] = {};
    for(int i =0; i < row; i++)
    {
        for(int j = 0; j < col; j++)
        {
            cin>>arr[i][j];
        }
    }
}
```