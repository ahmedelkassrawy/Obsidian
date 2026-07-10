- are dynamic arrays ==> array that can change its size.
- vector is a class template.
```C++
#include <vector>
vector<TYPE> Variablename
------
vector<int> numsone = {10,20,30,40};
vector<int> numstwo{100,200,300,400};
vector<int> numthree(4,50);//size of 4 , values of 50
-------
for(int i = 0; i < numsone.size(); i++)
{
	cout<<numsone.at(i);
}
```

## Add
```C++
// add the integers 6 and 7 to the vector
  num.push_back(6);
  num.push_back(7);
```

## Access 
```C++
#include <iostream>
#include <vector>
using namespace std;

int main() {
  vector<int> num {1, 2, 3, 4, 5};

  cout << "Element at Index 0: " << num.at(0) << endl;
  cout << "Element at Index 2: " << num.at(2) << endl;
  cout << "Element at Index 4: " << num.at(4);

  return 0;
}
```

**the `at()` function is preferred over `[]` because `at()` throws an exception whenever the vector is out of bound, while `[]` gives a garbage value.

## Changing
```C++
//changing values at certain pos
num.at(1) =9;
num.at(4) = 7;
```

### Vector VS Array
Vector
--> need standard header
-->can be resized after insertion or deletion 
--> not index based.
--> vectors are slower than arrays
--> vectors occupy more memory
--> vectors only in c++

Array
--> cannot be resized
--> arrays are faster
--> elements accessed by index
--> occupy less memory
____________________________________________
When do we use Vectors
---> when we dont know the size of the list.
_____________________________________________
Use array if looking for performance and memory.

## Deletion
```C++
//removes the last element added
num.pop_back();
```

## OTHER FUNCTIONS
|   |   |
|---|---|
|`size()`|returns the number of elements present in the vector|
|`clear()`|removes all the elements of the vector|
|`front()`|returns the first element of the vector|
|`back()`|returns the last element of the vector|
|`empty()`|returns **1** (true) if the vector is empty|
|`capacity()`|check the overall size of a vector|

*Vectors have Automatic Memory Management were it does it allocation and deallocation on its one.

```C++
// Declare a vector of vectors to represent the 2D array 
vector<vector<int>> arr(size, vector<int>(size));
```

**`vector<vector<int>>`**: This part declares a two-dimensional vector
**`arr`**: This is the name of the two-dimensional vector being declared.
**`size`**: This specifies the number of inner vectors (rows) in the outer vector. 

**`vector<int>(size)`**: This creates a temporary vector of integers with `size` elements, which serves as the default value for each inner vector in the outer vector.
## How it works
lets say 3ayz t7ot rakm 35 ht3mlo push back, hyroo7 ydwr fy array of size 1? la2 , y3ml wa7da wy7ot 35, tegy enta tzwd rakm yroo7 ys2l larray lt3mlt enty fy mkan , LA2 , yegy 3aml <font color="#c00000">DOUBLE THE PREVIOUS SIZE </font> fkda m3ana array of 2, tegy tzwd rakm kman fy mkan t2olk la2 fy3ml <font color="#c00000">DOUBLE THE PREVIOUS SIZE</font> b2a m3ana size of 4 tkfy rakm da wwa7d kman wlb3dha htb2a size of 8 whkza

Amortized Complexity