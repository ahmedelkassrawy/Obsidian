```C++
#include <iostream>

int add(int x, int y); // forward declaration of add() (using a function declaration)

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n'; // this works because we forward declared add() above
    return 0;
}

int add(int x, int y) // even though the body of add() isn't defined until here
{
    return x + y;
}
```

As declaring the function before main is the best option but if you want to declare after the main function make a declaration using only the parameters with no body.

## Declarations VS Definitions
A **declaration** tells the _compiler_ about the _existence_ of an identifier and its associated type information. Here are some examples of declarations:
```C++
int add(int x, int y); // tells the compiler about a function named "add" that takes two int parameters and returns an int.  No body!
int x;                 // tells the compiler about an integer variable named x
```

A **definition** is a declaration that actually implements (for functions and types) or instantiates (for variables) the identifier.

Here are some examples of definitions:
```C++
int add(int x, int y) // implements function add()
{
    int z{ x + y };   // instantiates variable z

    return z;
}
int x;                // instantiates variable x
```

<span style="background:#40a9ff">In C++, all definitions are declarations</span>

