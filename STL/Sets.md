```C++
std::set <data_type> set_name;
```

Sets same as in Maths
- By default, the std::set is sorted in ascending order.
- if you want to change the order to descending
```C++
std::set <data_type, greater<data_type>> set_name;
```
- Follow Binary Search Tree implementation
- The values in set are unindexed

## Functions
- [begin()](https://www.geeksforgeeks.org/setbegin-setend-c-stl/) – Returns an iterator to the first element in the set.
- [end()](https://www.geeksforgeeks.org/setbegin-setend-c-stl/) – Returns an iterator to the theoretical element that follows the last element in the set.
- [size()](https://www.geeksforgeeks.org/setsize-c-stl/) – Returns the number of elements in the set.
- [max_size()](https://www.geeksforgeeks.org/set-max_size-function-in-c-stl/) – Returns the maximum number of elements that the set can hold.
- [empty()](https://www.geeksforgeeks.org/setempty-c-stl/) – Returns whether the set is empty.
- insert();
- erase();

```C++
#include <iostream>
#include <set>
using namespace std;
int main()
{
    set<int> st;
    st.insert(5);
    st.insert(4)
    st.insert(6);
    st.erase(4);
    set<int>::iterator it = st.find(5);  //byroo7 y7otly pointer 3la el rakm bs
    if(it == st.end()) //lw 2alk end yb2a kda howa bara asln
    {
        cout<<"NOT FOUND"<<endl;
    }
    else cout<< *it << endl;

	if(st.count(5) == 0) //mhowa ya 1 ya 0 fdy ashl fl search 3n lfoo2 logical wise aktar y3ny
    {
        cout<<"NOT FOUND"<<endl;
    }
    else cout<< *it << endl;


	set<int>::iterator it = st.upper_bound(5); //hydeek lb3d el rakm
	set<int>::iterator it = st.lower_bound(5); //hydeek l2ablo lw fy

	for(int x : st)
	{
		cout << x << endl;
	
	}

	for(auto it = st.rbegin(); it != st.rend(); it++) //reverse printing
	{
		cout<< *it <<endl
	}
}
```

all of them O(log(n))

             end or rebegin
			^
[ 1 2 3 4 5 6 7 8 ]
   ^
---                  
begin
rend

r means reversed so if you ++ the iterator it goes back in case of rebegin <---
and the opp in rend --->