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

---
Intersection 
```c++
#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>
using namespace std;

int main()
{
    long long l1,r1;
    long long l2,r2;
    cin>> l1 >> r1 >> l2 >> r2;

    
    long long l = max(l1,l2);
    long long r = min(r1,r2);

    if(l <= r) cout<<l<<" "<<r<<endl;
    else cout<<-1<<endl;

    return 0;
}
```

To get the numbers and reverse or digits
```c++
#include <iostream>
using namespace std;

int main()
{
    int n;
    cin >> n;

    int original = n;
    int reversed = 0;

    while (n)
    {
        reversed = reversed * 10 + n % 10;
        n /= 10;
    }

    cout << reversed << "\n";
    cout << (original == reversed ? "YES" : "NO") << "\n";

    return 0;
}
```