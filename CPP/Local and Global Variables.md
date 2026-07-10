local variables are variables inside the body of a function
```C++
int add(int x, int y) //functions parameters are also local.
{
    int z{ x + y }; // z is a local variable

    return z;
} //z,y,x lifetime ends at the end of the function
```

## Local Scope

```C++
#include <iostream>

// x is not in scope anywhere in this function
void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    // x can not be used here because it's not in scope yet
    int x{ 0 }; // x enters scope here and can now be used within this function

    doSomething();
    
    return 0;
} // x goes out of scope here and can no longer be used
```

It turns out that C++ actually doesn’t have a single attribute that defines a variable as being a local variable. Instead, local variables have several different properties that differentiate how these variables behave from other kinds of (non-local) variables. We’ll explore these properties in this and upcoming lessons.

```C++
int main() // outer block
{
    int x { 5 }; // x enters scope and is created here
    { // nested block
        int y { 7 }; // y enters scope and is created here
    } // y goes out of scope and is destroyed here
    // y can not be used here because it is out of scope in this block
    return 0;
} // x goes out of scope and is destroyed here
```

In nested blocks, the situation is diff since the variable declaration is linked the block once the block ends, the variable dies.

## Global
```C++
#include <iostream>
using namespace std;
namespace Foo // Foo is defined in the global scope
{
    int g_x {}; // g_x is now inside the Foo namespace, but is still a global variable
}

void doSomething()
{
    // global variables can be seen and used everywhere in the file
    Foo::g_x = 3;
    cout << Foo::g_x << '\n';
}

int main()
{
    doSomething();
    cout << Foo::g_x << '\n';

    // global variables can be seen and used everywhere in the file
    Foo::g_x = 5;
    cout << Foo::g_x << '\n';
    return 0;
}
```

**Consider using a “g” or “g_” prefix when naming non-const global variables, to help differentiate them from local variables and function parameters.
```C++
// Non-constant global variables
int g_x;                 // defines non-initialized global variable (zero initialized by default)
int g_x {};              // defines explicitly value-initialized global variable
int g_x { 1 };           // defines explicitly initialized global variable

// Const global variables
const int g_y;           // error: const variables must be initialized
const int g_y { 2 };     // defines initialized global const

// Constexpr global variables
constexpr int g_y;       // error: constexpr variables must be initialized
constexpr int g_y { 3 }; // defines initialized global constexpr
```

Each block defines its own scope region. So what happens when we have a variable inside a nested block that has the same name as a variable in an outer block? When this happens, the nested variable “hides” the outer variable in areas where they are both in scope. This is called **name hiding** or **shadowing**.

```C++
#include <iostream>

int main()
{ // outer block
    int apples { 5 }; // here's the outer block apples
    { // nested block
        // apples refers to outer block apples here
        std::cout << apples << '\n'; // print value of outer block apples
        int apples{ 0 }; // define apples in the scope of the nested block
        // apples now refers to the nested block apples
        // the outer block apples is temporarily hidden
        apples = 10; // this assigns value 10 to nested block apples, not outer block apples
        std::cout << apples << '\n'; // print value of nested block apples
    } // nested block apples destroyed
    std::cout << apples << '\n'; // prints value of outer block apples
    return 0;
} // outer block apples destroyed
```

```C++
5
10
5
```

## Linkage
Static Variables
```C++
// C++ program to demonstrate
// the use of static Static
// variables in a Function
#include <iostream>
#include <string>
using namespace std;

void demo()
{
	// static variable
	static int count = 0;
	cout << count << " ";

	// value is updated and
	// will be carried to next
	// function calls
	count++;
}

int main()
{
	for (int i = 0; i < 5; i++)
		demo();
	return 0;
}

```

```RESULT
0 1 2 3 4 
```

## Avoid Global Variables

```C++
#include <iostream>

int g_mode; // declare global variable (will be zero-initialized by default)

void doSomething()
{
    g_mode = 2; // set the global g_mode variable to 2
}

int main()
{
    g_mode = 1; // note: this sets the global g_mode variable to 1.  It does not declare a local g_mode variable!
    doSomething();
    // Programmer still expects g_mode to be 1
    // But doSomething changed it to 2!
    if (g_mode == 1)
    {
        std::cout << "No threat detected.\n";
    }
    else
    {
        std::cout << "Launching nuclear missiles...\n";
    }
    return 0;
}
```

![[Pasted image 20240426201732.png]]

extern--> keyword for variable that it can be used any where else, LITERALLY ANYWHERE.

**Best practice**
Initialize your static local variables. Static local variables are only initialized the first time the code is executed, not on subsequent calls.

[7.11 — Scope, duration, and linkage summary – Learn C++ (learncpp.com)](https://www.learncpp.com/cpp-tutorial/scope-duration-and-linkage-summary/)

Inline Namespaces
```C++
#include <iostream>

void doSomething()
{
    std::cout << "v1\n";
}

int main()
{
    doSomething();
    return 0;
}
```

```C++
#include <iostream>

inline namespace V1 // declare an inline namespace named V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

namespace V2 // declare a normal namespace named V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // calls the V1 version of doSomething()
    V2::doSomething(); // calls the V2 version of doSomething()

    doSomething(); // calls the inline version of doSomething() (which is V1)
    return 0;
}
```


## Summary
A **compound statement** or **block** is a group of zero or more statements that is treated by the compiler as if it were a single statement. Blocks begin with a `{` symbol, end with a `}` symbol, with the statements to be executed placed in between. Blocks can be used anywhere a single statement is allowed. No semicolon is needed at the end of a block. Blocks are often used in conjunction with `if statements` to execute multiple statements.

**User-defined namespaces** are namespaces that are defined by you for your own declarations. Namespaces provided by C++ (such as the `global namespace`) or by libraries (such as `namespace std`) are not considered user-defined namespaces.

You can access a declaration in a namespace via the **scope resolution operator (::)**. The scope resolution operator tells the compiler that the identifier specified by the right-hand operand should be looked for in the scope of the left-hand operand. If no left-hand operand is provided, the global namespace is assumed.

Local variables are variables defined within a function (including function parameters). Local variables have **block scope**, meaning they are in-scope from their point of definition to the end of the block they are defined within. Local variables have **automatic storage duration**, meaning they are created at the point of definition and destroyed at the end of the block they are defined in.

A name declared in a nested block can **shadow** or **name hide** an identically named variable in an outer block. This should be avoided.

Global variables are variables defined outside of a function. Global variables have **file scope**, which means they are visible from the point of declaration until the end of the file in which they are declared. Global variables have **static duration**, which means they are created when the program starts, and destroyed when it ends. Avoid dynamic initialization of static variables whenever possible.

An identifier’s **linkage** determines whether other declarations of that name refer to the same object or not. Local variables have no linkage. Identifiers with **internal linkage** can be seen and used within a single file, but are not accessible from other files. Identifiers with **external linkage** can be seen and used both from the file in which they are defined, and from other code files (via a forward declaration).

Avoid non-const global variables whenever possible. Const globals are generally seen as acceptable. Use **inline variables** for global constants if your compiler is C++17 capable.

Local variables can be given static duration via the **static** keyword.

A **qualified name** is a name that includes an associated scope (e.g. `std::string`). An **unqualified name** is a name that does not include a scoping qualifier (e.g. `string`).

**Using statements** (including **using declarations** and **using directives**) can be used to avoid having to qualify identifiers with an explicit namespace. A **using declaration** allows us to use an unqualified name (with no scope) as an alias for a qualified name. A **using directive** imports all of the identifiers from a namespace into the scope of the using directive. Both of these should generally be avoided.

**Inline functions** were originally designed as a way to request that the compiler replace your function call with inline expansion of the function code. You should not need to use the inline keyword for this purpose because the compiler will generally determine this for you. In modern C++, the `inline` keyword is used to exempt a function from the one-definition rule, allowing its definition to be imported into multiple code files. Inline functions are typically defined in header files so they can be #included into any code files that needs them.

Finally, C++ supports **unnamed namespaces**, which implicitly treat all contents of the namespace as if it had internal linkage. C++ also supports **inline namespaces**, which provide some primitive versioning capabilities for namespaces.