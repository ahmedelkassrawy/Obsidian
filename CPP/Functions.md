## Declaring the default parameter for a function

```C++
void myFunction(**string country = "Norway"**) 
{  
  cout << country << "\n";  
}  
  
int main() {  
  myFunction("Sweden");  
  myFunction("India");  
  **myFunction();**  
  myFunction("USA");  
  return 0;  
}  
  
// Sweden  
// India  
// Norway  
// USA
```

## Passing by reference

```C++
#include <iostream>
using namespace std;

void swapNums(int &x, int &y) {
  int z = x;
  x = y;
  y = z;
}


int main() {
  int firstNum = 10;
  int secondNum = 20;

  cout << "Before swap: " << "\n";
  cout << firstNum << secondNum << "\n";
  // Call the function, which will change the values of firstNum and secondNum
  swapNums(firstNum, secondNum);
  cout << "After swap: " << "\n";
  cout << firstNum << secondNum << "\n";
  return 0;
}
```

the diff between the passing reference is that at int z = x its passing the number that x is pointing to which here is 10 then equal the y which is 20 to x and passing z to y which is pointing to 10 right now

## Function Overloading

Multiple functions can have the same name as long as the number and/or type of parameters are different.
```C++
int plusFunc(int x, int y) {  
  return x + y;  
}  
  
double plusFunc(double x, double y) {  
  return x + y;  
}
```

