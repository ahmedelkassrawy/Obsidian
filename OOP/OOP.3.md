### Static Functions ,Members
```C#
class MathHelper
{
	public static int Fact(int n)
	{
		if (n == 0)
			return 1;
		return n * Fact(n - 1);
	}
}

class Program
{
	
	Employee e1 = new Employee();
	e1.ID = 1;
	e1.Name = "John";

	Employee e2 = new Employee();
	e2.ID = 2;
	e2.Name = "Jane";

	e1.Display();
	e2.Display();

	MathHelper m1 = new MathHelper();
	MathHelper m2 = new MathHelper();

	int x = m1.Fact(5);
	x = m2.Fact(5);
	//this func doesnt change by change of object
	//it depeneds on the input instead of the object itself
	//so it is a static function
	//in constrast to the display function in the employee class
	//which is a non-static function cause it depends on the object itself

	//the display func depend on the data of the object itself
	//the fact func depend on the input only and not the object itself

	int x = MathHelper.Fact(5); //this is a static function
	//now we call the function using the class itself

	//static member in class is a member that is shared among all objects of the class
	//and loaded one time only in the memory
	//loaded in heap memory
	//cant be accessed using the object of the class
	//can be accessed using the class itself

	Employee.NumberofEmployees = 100;

	//static function can access static members only
}

```

### Overloading Functions,operators
```C#
class Complex
{
	public int Real;
	public int Img;

	public Complex(int real,int img)
	{
		Real = real;
		Img = img;
	}

	public static Complex add(Complex c1,Complex c2)
	{
		Complex result = new Complex();
		result.Real = c1.Real + c2.Real;
		result.Img = c1.Img + c2.Img;

		return result;
	}

	public Complex Add(Complex c2)
	{
		Complex result = new Complex(0,0);

		result.Real = c1.Real + c2.Real;
		result.Img = c1.Img + c2.Img;

		return result;
	}

	public void Add(Complex c1,Complex c2)
	{
		this.Real = c1.Real + c2.Real;
		this.Img = c1.Img + c2.Img;
	}

	public static Complex operator+(Complex c1,Complex c2)
	{
		Complex result = new Complex(0,0);

		result.Real = c1.Real + c2.Real;
		result.Img = c1.Img + c2.Img;

		return result;
	}

	public static Complex operator+(Complex c1,int num)
	{
		Complex result = new Complex(0,0);

		result.Real = c1.Real + num;
		result.Img = c1.Img;

		return result;
	}

	public static bool operator==(Complex c1,Complex c2)
	{
		if(c1.Real == c2.Real && c1.Img == c2.Img)
		{
			return true;
		}
		else
		{
			return false;
		}
	}

	public static bool operator!=(Complex c1,Complex c2)
	{
		if(c1.Real != c2.Real || c1.Img != c2.Img)
		{
			return true;
		}
		else
		{
			return false;
		}
	}

	public static implicit operator Complex(int num)
	{
		return new Complex(num,num);
	}
}
```

```C#
static void main(string[] args)
{
	Complex c1 = new Complex(1, 2);
	Complex c2 = new Complex(3, 4);

	Complex result = c1.add(c1, c2);

	Console.WriteLine("Real: " + result.Real);
	Console.WriteLine("Img: " + result.Img);

	Complex c3 = Complex.add(c1, c2);

	complex c4 = c1 + c2; //Complex.Add(c1,c2)
	//this is an operator overloading
	//we can overload the operators in c#
	//overloading has a necessity of being static
	//why static? cause the operator is not a member of the object

	if(c1 == c2)
	{
		Console.WriteLine("Equal");
	}
	else
	{
		Console.WriteLine("Not Equal");
	}
	//the compiler will let us make a != operator also
	//altohugh we made a else statement to deal with that but 
	//it insists on making a != operator

	 
}
```