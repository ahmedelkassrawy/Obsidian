a defined area where code inside refers to back.
if namespace math contain plus or minus functions then it is only accessed by math or by letting access to it manually.
```C++
#include <iostream>
using namespace std;
namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    cout << Foo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Foo
    return 0;
}
```

forward declarations can be done in namespaces also same as before.
nested namespaces:

```C++
#include <iostream>
using namespace std;
namespace Foo
{
    namespace Goo // Goo is a namespace inside the Foo namespace
    {
        int add(int x, int y)
        {
            return x + y;
        }
    }
}

int main()
{
    std::cout << Foo::Goo::add(1, 2) << '\n';
    return 0;
}
```

Namespace Alias 
```C++
#include <iostream>

namespace Foo::Goo
{
    int add(int x, int y)
    {
        return x + y;
    }
}

int main()
{
    namespace Active = Foo::Goo; // active now refers to Foo::Goo

    std::cout << Active::add(1, 2) << '\n'; // This is really Foo::Goo::add()

    return 0;
} // The Active alias ends here
```

used for big projects or libraries or in big companies.