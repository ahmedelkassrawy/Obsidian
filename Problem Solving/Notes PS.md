## Set Precision
``` C++
#include <iostream>
#include <iomanip>
using namespace std;

int main()
{
	double num = 15.23456;
	cout<<fixed<<setprecision(2);
	cout<<num;
}

```

### Notes
The `ceil` function is a mathematical function that returns the smallest integer greater than or equal to a given number.
- `ceil(4.2)` returns `5` because `5` is the smallest integer greater than or equal to `4.2`.
- `ceil(3.7)` returns `4` for the same reason.
- `ceil(2.0)` returns `2` because `2` is already an integer, so no rounding is necessary.
- `ceil(-3.8)` returns `-3` because it's the next smallest integer greater than `-3.8` (closer to zero in this case).


