Header files allow us to put declarations in one location and then import them wherever we need them. This can save a lot of typing in multi-file programs.
```C++
// 1) We really should have a header guard here, but will omit it for simplicity (we'll cover header guards in the next lesson)

// 2) This is the content of the .h file, which is where the declarations go
int add(int x, int y); // function prototype for add.h -- don't forget the semicolon!
```

```C++
#include "add.h" // Insert contents of add.h at this point.  Note use of double quotes here.

#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is " << add(3, 4) << '\n';
    return 0;
}
```

using Header Guards 
**"#pragma once" is used to avoid a header file from being included multiple times.**