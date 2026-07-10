```C++
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct point
{
    int x,y,z;
};

int main()
{
    int n;
    cin>>n; 

    point a[n];

    for(int i = 0; i < n; i++)
    {
        cin>>a[i].x>>a[i].y>>a[i].z;
    }

    for(int i = 0; i < n; i++)
    {
        int cntx = 0;
        int cnty = 0;
        int cntz = 0;
        for(int j = 0; j < n; j++)
        {
            if( i == j ) continue;
            if(a[i].x == a[j].x) cntx++;
            if(a[i].y == a[j].y) cnty++;
            if(a[i].z == a[j].z) cntz++;
        }
        cout<<cntx<<" "<<cnty<<" "<<cntz<<endl;
    }  
}
```

3amlna a new struct called point with the variable x y ,z which will be the dimensions 
then we made an array using the point struct with the size of n,
at each input i have to specify the dimension i want it to store the input in.

https://codeforces.com/group/5pUldkahAU/contest/511788/problem/D
[[Problem Solving/Structs]]