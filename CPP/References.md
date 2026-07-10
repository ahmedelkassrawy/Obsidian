Refrencing is just pointing to the same data type
```C++
int x =9;
int &y = x;
//then this means there is x with actual value of x 
//and y only pointing at it is if x is the house
//and y is the address of that house.
```

The declaration of the data type is a must as the reference will weigh the same as the weigh of the data type its declared to.

## Check the difference

```C++
string food = "Pizza";  
cout << &food; // Outputs 0x6dfed4
```

```C++
#include <iostream>
using namespace std;

int main()

{
    int x = 10;
    int y = 9;
    
    int &a = x;
    int &b = y;
    
    cout<< a <<"\n"; //prints 10
    cout<< b <<"\n"; //prints 9
}
```

# Continue

A reference can be considered as a constant pointer (not to be confused with a pointer to a constant value) which always points to (references) the same object. They are declared using the `&` (ampersand) symbol.

## Declaration and Initialization

To declare a reference, use the `&` symbol followed by the variable type and the reference’s name. Note that you must initialize a reference when you declare it.

```C++
int var = 10;        // Declare an integer variable
int& ref = var;      // Declare a reference that "points to" var
```

## Usage

You can use the reference just like you’d use the original variable. When you change the value of the reference, the value of the original variable also changes, because they both share the same memory location.

```C++
var = 20;            // Sets the value of var to 20
cout << ref << endl; // Outputs 20

ref = 30;            // Sets the value of ref to 30
cout << var << endl; // Outputs 30
```

## Function Parameters

You can use references as function parameters to create an alias for an argument. This is commonly done when you need to modify the original variable or when passing an object of considerable size to avoid the cost of copying.

```C++
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
   int x = 5, y = 10;
   cout << "Before Swap: x = " << x << " y = " << y << endl; // Outputs 5 10
   
   swap(x, y);
   cout << "After Swap: x = " << x << " y = " << y << endl;  // Outputs 10 5
}
```