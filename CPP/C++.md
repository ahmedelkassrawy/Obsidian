[[Constructor]]
[[Classes]]
[[Problem Solving/PS Level 1/Structs]]
[[References]]
[[Pointers]]
[[CPP/Functions]]
[[CPP/OOP]]
[[Local and Global Variables]]
[[Forward deceleration]]
[[Header Files]]
[[Sets]]
Set precision
```C++
#include <iomanip> // for output manipulator std::setprecision()
#include <iostream>

int main()

{
    std::cout << std::setprecision(9); // show 17 digits of preision
    std::cout << 3.33333333333333333333333333333333333333f <<'\n'; // f suffix means float
    std::cout << 3.33333333333333333333333333333333333333 << '\n'; // no suffix means double
    return 0;

??if you want to make the peresicion fixed: 
 cout << fixed << setprecision(2) << num;
}
```

[4.9 — Boolean values – Learn C++ (learncpp.com)](https://www.learncpp.com/cpp-tutorial/boolean-values/)
