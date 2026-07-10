## Enums
How to specify an employee's gender ?!

```C#
staiuc void Main(string[] args)
{
	const int Male = 0;
	const int Female = 1;

	Employee e1 = new Employee();
	e1.Gender = Male:
}
```

Using integers as they are the simplest fastest data type for the compiler to process. 
But defining them as local variables in main only will cause future problems.
HERE COMES THE ENUMS!

*Enums : set of constant values that are related to each other.*
```C#
enum Gender
    {
        Male = 0;
        Female = 1;
    }
    // enumeration -> set of constant values
    // by default enum values are int or any derived int datatype

    enum Color 
    {
        //Red,Green,Blue // 0,1,2

        // Red , // 0
        // Green = 20,
        // Blue // 21

        Red = 1,
        Green = 2,
        Blue = 4

    }
    //enums take the last number you gave to the previous enum and add 1 to it

    class Program
    {
        static void Main(string[] args)
        {
            // Employee emp = new Employee();
            // emp.ID = 101;
            // emp.Name = "John";
            // e1.Gender = "male"
            // //processing on string is hard sometimes to validate

            Gender g = Gender.Male;
            Employee emp = new Employee();
            emp.gender = Gender.Male;

            if(emp.gender == Gender.Male)
            {

            }

            Color c = Color.Red | Color.Green;
        }
    }
```
```C#
class Employee()
{
	...
	public Gender gender; 
	//enums of Gender of attribute name gender.
}
```

## Struct
```C#
struct Complex
{
	public int Real;
	public int Img;
}
```
```C#
static void Main()
{
	Complex c1 = new Complex();
	c1.Real =9;
	c1.Img = 8;
}
```

### Structs VS Class 
Struct is of value type , while class is of object type
In Terms of implementation in main no diff in terms of syntax, but diff concepts are accomplished by using the same syntax.
At classes the same code would <span style="background:#9254de">first go to Heap, make an object , return back its address to c1 , c1 becomes the refrence of an object of class Complex</span>

At Structs, this code would do nothing in Heap <span style="background:#9254de">except initializing the c1 as a struct + giving it the attributes written in structs </span>
(NOT AS REFRENCE BUT AS A REAL STRUCT) 

There is no initialization in the struct code for any variable + the solution is either to input them your self or by using [[Constructor]] (also initializing all variables ).

No inheritance from other structs or classes, but struct is an inheritance of class object.

Big data , have to use references , inheritance --> Class
if Using numbers a lot such as "fraction" or "complex" --> Structs
<font color="#ff0000">*Usage aren't only these but for knowledge purposes*</font>

```C#
struct Complex
{
	public int real;
	public int img;

	public Complex(int real, int img)
	{
		this.real = real;
		this.img = img;
	}
}

class Program
{
	static void Main(string[] args)
	{
		Complex c1 = new Complex();
		//At Structs, this code would do nothing in Heap 
		//except initializing the c1 as a struct + giving it the attributes written in structs 

		Complex c2; //At Structs, this code would do nothing in Heap except initializing the c2 as a struct
		c2.real = 10;
		c2.img = 20;
		//no intialization for default values in structs

		//you can never intiallize a struct without giving it values
		//even if you give it one value you should give it all the values

		//constructors are not a limit in creation for structs
		//you can create a struct without a constructor
		//but you can't create a struct without giving it values
		//and constructors with paramters dont override the default constructor(parametless)
		//which is the opposite of classes

		//here you cant make a paramterless constructor for the struct
		//because the struct has no default values

		//no inheritance for structs
		//no inheritance from classes to structs
		//no polymorphism for structs
		//no abstract for structs

		//when class and when struct
		//if you have a small object that you want to pass by value
		//because ur storing in stack not heap
		//use struct
		//if you have a big object that you want to pass by reference
		//use class
		//also inheritance and polymorphism are only for classes
		//fractions , complex numbers aree good examples for structs
	}
}
```


## Boxing and Unboxing
Boxing is the process of converting a value type to the type `object.`

When the common language runtime (CLR) boxes a value type, it wraps the value inside a System.Object instance and stores it on the managed heap.

Unboxing extracts the value type from the object.
The concept of boxing and unboxing underlies the C# unified view of the type system in which a value of any type can be treated as an object.

```C#
int i = 123;
// The following line boxes i.
object o = i;

```
```C#
o = 123;
i = (int)o;  // unboxing
```

In terms of performance its very expensive to use boxing and unboxing excessively ; when a value type is boxed, a new object must be allocated and constructed. then the cast required for unboxing is also expensive.

# Step by step:
### 1.Boxing
```C#
int i = 123;
// Boxing copies the value of i into object o.
object o = i;
```
1.The result of this statement is creating an object reference `o`
2.on the stack, that references a value of the type `int`, on the heap.
3.This value is a copy of the value-type value assigned to the variable `i`

![[Pasted image 20240408153703.png]]

### 2.Unboxing
- Checking the object instance to make sure that it is a boxed value of the given value type.
    
- Copying the value from the instance into the value-type variable.

```C#
int i = 123;      // a value type
object o = i;     // boxing
int j = (int)o;   // unboxing
```

![[Pasted image 20240408153916.png]]