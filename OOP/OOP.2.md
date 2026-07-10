### Continue Inheritance
```C#
class Creature
{
	public int age;
	public void Move()
	{
		Console.WriteLine("Creature is moving");
	}

	public void Eat()
	{
		Console.WriteLine("Creature is eating");
	}

}

class Human : Creature
{
	public void think()
	{
		base.Move();
		Console.WriteLine("Human is thinking");
	}

	public void Move()
	{
		Console.WriteLine("Human is moving");
	}  
}

-------------------------------------
static void Main(string[] args)
{
	Human h = new Human();

	h.Move(); // Human is moving
	h.think(); // Creature is moving, Human is thinking
}
```

### Polymorphism
```C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Day3
{
    abstract class Creature 
    {
        public int age;
        public void abstract Move()
        {
            Console.WriteLine("Creature is moving");
        }
        public void Eat()
        {
            Console.WriteLine("Creature is eating");
        }

        public virtual void XYZ()
        {
            Console.WriteLine(" creature XYZ");
        }

    }
}
```

```C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Program
{
    abstract class Animal:Creature
    {
        public void override Move()
        {
            Console.WriteLine("Animal is moving");
        }
    }
}
```

```C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Program
{
    class Program
    {
        public static void MoveCreature(Creature[] arr)
        {
            for(int i = 0; i < arr.Length; i++)
            {
                arr[i].Move();
            }
        }
        static void MoveCreature(Creature c)
        {
            c.Move();
        }
        static void Main(string[] args)
        {
            // Human h = new Human();
            // h.Move(); // Human is moving
            // h.think(); // Creature is moving, Human is thinking

            creature c = new Human(); //polymorphism
            //now we are looking at the human object as a creature 
            //this happend because the compiler already knows there is a relation between
            //human and creature inheritance
            // c.think(); //error

            // c.Move(); //Creature is moving 
            //this happens because the compiler is looking at the object as a creature 

            //logically this is wrong because the object is a human object
            //although u are a creature but when i tell u move,do u move as a creature or as a human

            //this is where polymorphism comes in
            //polymorphism is the ability of an object to take many forms
            //in this case the object is a human object but the compiler is looking at it as a creature object
            //we add the virtual keyword to the method in the parent class and the override keyword to the method in the child class

            c.Move(); //Human is moving

            Human h = new Human();
            h.Move(); //Human is moving

            Animal a = new Animal(); 
            //////////////////////////////////
            MoveCreature(h); //Human is moving
            MoveCreature(a); //Animal is moving

            Creature[] arr = new Creature[3];
            arr[0] = new Creature();
            arr[1] = new Human();
            arr[2] = new Animal();

            //abstract classes cannot be instantiated
            // Creature c = new Creature(); //error
            //abstract classes can only be used as base classes

            Creature c = new Employee();
            c.Move(); //Employee is moving

            //writing the keyword 'new' before the method in the child class hides the method in the parent class
            //this is called method hiding
            //this is not polymorphism
            //this is not overriding

            c.XYZ(); //creature XYZ
            h.XYZ(); //Human XYZ

        }
    }
}
```