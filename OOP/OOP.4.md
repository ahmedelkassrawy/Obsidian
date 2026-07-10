### Object Methods
```C#
class Human
{
	public int ID;
	public string Name;
	
	public override bool equals(object obj)
	{
		//Human h = (Human)obj; 
		//casting the object to Human class
		//not safe casting as it can throw an exception if casting is wrong
	
		// Human h1 = obj as Human; //safe casting
		//doesnt throw exception it just makes the refrence to be null
	
		// if(h1 == null)
		// {
		//     return false;
		// }
	
		// return this.ID == h.ID;
		//-----------------------------------------------
		if(obj is Human)
		{
			Human h = (Human)obj;
			return this.ID == h.ID;
		}
		else
		{
			return false;
		}
	
	}//to override the object class equal method
	
	public override string ToString()
	{
		return "Human";
	}//to override the object class ToString method
}
```

```C#
public Human Clone()
{
    // Step 1: Create a shallow copy using MemberwiseClone()
    // MemberwiseClone() creates a new object and copies all fields (value types and references).
    // However, for reference types, it only copies the reference, not the actual object.
    Human clonedHuman = (Human)this.MemberwiseClone();

    // Step 2: Deep copy reference types
    // If the class contains reference types, we need to manually create new instances
    // and copy their values to ensure the cloned object is independent of the original.

    // Example: If Human has a reference type like another Human object (e.g., Friend),
    // we need to clone it recursively.
    if (this.Friend != null)
    {
        clonedHuman.Friend = this.Friend.Clone(); // Recursively clone the Friend object
    }

    // Step 3: Copy value types (if needed)
    // For value types (e.g., Name, ID), MemberwiseClone() is sufficient because it copies the actual value.
    // No additional work is needed here unless you want to explicitly reassign them.
    clonedHuman.Name = this.Name; // Copy the Name (value type)
    clonedHuman.ID = this.ID;     // Copy the ID (value type)

    // Step 4: Return the deep-cloned object
    return clonedHuman;
}
```

```C#
class Program
{
	static void Test(object obj)
	{

	}
	//here you wont know the type of class that is being passed
	//called dynamic binding and happens at runtime

	static void myfunc(Employee emp)
	{

	}
	//here you know the type of class that is being passed which is Employee

	static void Main(string[] args)
	{
		//Human h = new Human();
		
		object h = new Human();
		//an object of Human class is created and stored in a variable of type object

		Human h1 = new Human();
		Human h2 = new Human();
		h1.equals(h2); //a method of the object class
		//this will compare the references of the two objects and not the values

		string msg = h1.ToString(); //a method of the object class
		//this will return the name of the class
	}
}
```