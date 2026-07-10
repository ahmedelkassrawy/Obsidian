To create a class, use the `class` keyword:
```C++
class MyClass {       // The class  
  public:             // Access specifier  
    int myNum;        // Attribute (int variable)  
    string myString;  // Attribute (string variable)  
};
```

To create an object we use
```C++
int main() {  
  MyClass myObj;  // Create an object of MyClass  
  
  // Access attributes and set values  
  myObj.myNum = 15;   
  myObj.myString = "Some text";  
  
  // Print attribute values  
  cout << myObj.myNum << "\n";  
  cout << myObj.myString;  
  return 0;  
}
```

To create class methods outside of the class itself
```C++
class MyClass {        // The class  
  public:              // Access specifier  
    void myMethod();   // Method/function declaration  
};  
  
// Method/function definition outside the class  
void MyClass::myMethod() {  
  cout << "Hello World!";  
}  
  
int main() {  
  MyClass myObj;     // Create an object of MyClass  
  myObj.myMethod();  // Call the method  
  return 0;  
}
```

[[Constructor]]

## Access Specifiers

In C++, there are three access specifiers:

- `public` - members are accessible from outside the class
- `private` - members cannot be accessed (or viewed) from outside the class
- `protected` - members cannot be accessed from outside the class, however, they can be accessed in inherited classes.

*From Top to bottom in terms on publicity:*
1.Public  2.Protected 3.Private

```C++
class MyClass {  
  public:   // Public access specifier  
    int x;   // Public attribute  
  private:   // Private access specifier  
    int y;   // Private attribute  
};  
  
int main() {  
  MyClass myObj;  
  myObj.x = 25;  // Allowed (public)  
  myObj.y = 50;  // Not allowed (private)  
  return 0;  
}
```

*by default without declaring its access specifier C++ puts all members of class as private (until declaration)*

## Encapsulation 

is to make sure that "sensitive" data is hidden from users. To achieve this, you must declare class variables/attributes as <font color="#ff0000">`private`</font> (cannot be accessed from outside the class). If you want others to read or modify the value of a private member, you can provide public <font color="#00b050">**get**</font> and <font color="#00b050">**set**</font> methods.

```C++
class Employee {
  private:
    // Private attribute
    int salary;
  public:
    // Setter
    void setSalary(int s) 
    {
      salary = s;
    }
    // Getter
    int getSalary() 
    {
      return salary;
    }
};
```

*setters must take a parameter but with return type of void*
*getters don't take parameters but must have the correct return type*

[[Inheritance]]
[[Polymorphism]]
[[UML]]