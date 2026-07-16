Sort numbers in an array in asceding
```c++
#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>
using namespace std;

int main()
{
    int a,b,c;
    cin>>a>>b>>c;
    
    int arr[3] = {a,b,c};
    
    for(int i = 0; i < 3;i++)
    {
	    for(int j = i + 1; j < 3;j++)
	    {
		    if(arr[i] > arr[j])
		    {
				swap(arr[i],arr[j]);    
		    }
	    }
    }
    
    cout<<arr[0]<<endl;
    cout<<arr[1]<<endl;
    cout<<arr[2]<<endl;
}

```