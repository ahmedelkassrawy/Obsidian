**Function overloading** allows us to create multiple functions with the same name, so long as each identically named function has different parameter types (or the functions can be otherwise differentiated).

```C++
int add(int x, int y) // integer version
{
    return x + y;
}

double add(double x, double y) // floating point version
{
    return x + y;
}

int main()
{
    return 0;
}
```

```C++
int add(int x, int y)
{
    return x + y;
}

int add(int x, int y, int z) //based on no. of parameters.
{
    return x + y + z;
}
```

```C++
void print(int)
{
}

void print(double)
{
}

int main()
{
    print('a'); // promoted to match print(int)
    print(true); // promoted to match print(int)
    print(4.5f); // promoted to match print(double)

    return 0;
}
```


## Ambiguous matches
With non-overloaded functions, each function call will either resolve to a function, or no match will be found and the compiler will issue a compile error:
```C++
void foo()
{
}

int main()
{
     foo(); // okay: match found
     goo(); // compile error: no match found

     return 0;
}
```

With overloaded functions, there is a third possible outcome: an `ambiguous match` may be found. An **ambiguous match** occurs when the compiler finds two or more functions that can be made to match in the same step. When this occurs, the compiler will stop matching and issue a compile error stating that it has found an ambiguous function call.

Since every overloaded function must be differentiated in order to compile, you might be wondering how it is possible that a function call could result in more than one match. Let’s take a look at an example that illustrates this:

```C++
void print(int)
{
}

void print(double)
{
}

int main()
{
    print(5L); // 5L is type long

    return 0;
}
```

Since literal `5L` is of type `long`, the compiler will first look to see if it can find an exact match for `print(long)`, but it will not find one. Next, the compiler will try numeric promotion, but values of type `long` can’t be promoted, so there is no match here either.

Following that, the compiler will try to find a match by applying numeric conversions to the `long` argument. In the process of checking all the numeric conversion rules, the compiler will find two potential matches. If the `long` argument is numerically converted into an `int`, then the function call will match `print(int)`. If the `long` argument is instead converted into a `double`, then it will match `print(double)` instead. Since two possible matches via numeric conversion have been found, the function call is considered ambiguous.