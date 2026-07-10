In C++, the template system was designed to simplify the process of creating functions (or classes) that are able to work with different data types.

Instead of manually creating a bunch of mostly-identical functions or classes (one for each set of different types), we instead create a single _template_. Just like a normal definition, a **template** describes what a function or class looks like.

# Key insight
The compiler can use a single template to generate a family of related functions or classes, each using a different set of types.
# Key insight

Templates can work with types that didn’t even exist when the template was written. This helps make template code both flexible and future proof!

A **function template** is a function-like definition that is used to generate one or more overloaded functions, each with a different set of actual types. This is what will allow us to create functions that can work with many different types.

```C++
#include <iostream>
using namespace std;

template <typename T> // this is the template parameter declaration
T mullet(T x, T y) // this is the function template definition for max<T>
{
    return (x < y) ? y : x;
} 

int main()
{
    cout<<mullet(9.8,4.7);
}
```

templates are just functions that aren't existing unless called.