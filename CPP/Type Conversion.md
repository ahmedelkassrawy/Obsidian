```C++
#include <iostream>
void print(double x) // print takes a double parameter
{
	std::cout << x << '\n';
}

int main()
{
	int y { 5 };
	print(y); // y is of type int

	return 0;
}
```

Even though it is called a conversion, a type conversion does not actually change the value or type of the value being converted. Instead, the value to be converted is used as input, and the conversion results in a new value of the target type (via direct initialization).

In the above example, the conversion does not change variable `y` from type `int` to `double`. Instead, the conversion uses the value of `y` (`5`) as input to create a new double value (`5.0`). This double value is then passed to function `print`.

To perform an explicit type conversion, in most cases we’ll use the `static_cast` operator. The syntax for the `static cast` looks a little funny:
```C++
static_cast<new_type>(expression);
//or
double x = 5.090787890;
int y = int(x);
cout<<x<<endl<<y;
```

## Converting unsigned numbers to signed numbers

To convert an unsigned number to a signed number, you can also use the `static_cast` operator:
```C++
#include <iostream>

int main()
{
    unsigned int u { 5 };
    int s { static_cast<int>(u) }; // return value of variable u as an int

    std::cout << s << '\n';
    return 0;
}
```

Const vs constexpr

For variables, const means that the value of an object cannot be changed after initialization. Constexpr means that an object must have a value that is known at compile-time.
Constexpr variables are implicitly const. Const variables are not implicitly constexpr (except for const integral variables with a constant expression initializer).

|Term|Definition|
|---|---|
|Compile-time constant|An object whose value must be known at compile time (e.g. literals and constexpr variables).|
|Constexpr|Keyword that declares variables as compile-time constants (and functions that can be evaluated at compile-time). Informally, shorthand for “constant expression”.|
|Constant expression|An expression that contains only compile-time constants and operators/functions that support compile-time evaluation.|
|Runtime expression|An expression that is not a constant expression.|
|Runtime constant|An constant object that is not a compile-time constant.|

|Operator|Symbol|Form|Operation|
|---|---|---|---|
|Prefix increment (pre-increment)|++|++x|Increment x, then return x|
|Prefix decrement (pre-decrement)|––|––x|Decrement x, then return x|
|Postfix increment (post-increment)|++|x++|Copy x, then increment x, then return the copy|
|Postfix decrement (post-decrement)|––|x––|Copy x, then decrement x, then return the copy|

## Type Aliases

```C++
using Distance = double; // define Distance as an alias for type double
```

```C++
#include <iostream>

int main()
{
    using Distance = double; // define Distance as an alias for type double

    Distance milesToDestination{ 3.4 }; // defines a variable of type double

    std::cout << milesToDestination << '\n'; // prints a double value

    return 0;
}
```

```C++
// The following aliases are identical
typedef long Miles;
using Miles = long;
```