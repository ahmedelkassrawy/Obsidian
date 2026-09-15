---
description: "The four ways classes relate in C#: association (an object is passed or created in a method), aggregation, composition, and inheritance."
domain: cs
type: course
status: digested
tags:
  - domain/cs
  - type/course
  - status/digested
  - topic/oop
aliases:
  - "OOP.1"
hubs:
  - "[[OOP]]"
---
### Association 
```C#
class Instructor
    {
        public void WriteOnBoard(Marker marker) //association
        {
           ////////////////////
        }

        public void WriteOnBoard()
        {
            Marker marker = new Marker(); //still association
        }
    }
```

### Aggregation 
```C#
class Room
    {
        Instructor instructor;//reference to an object
  
        public Room()
        {
            instructor = null;
        }
  
        public void InstructorEntered(Instructor ins)
        {
            instructor = ins;
        }

        public void InstructorLeft()
        {
            instructor = null;
        }
    }
```
```C#
class Room
    {
        Instructor instructor;//reference to an object

        Students[] students; //reference to an array of objects
        int index = 0;

        public Room()
        {
            instructor = null;
            students = new Students[10]; //each element here will be a refrence to an object
        }
  
        public void InstructorEntered(Instructor ins)
        {
            instructor = ins;
        }

        public void InstructorLeft()
        {
            instructor = null;
        }

        public void StudentEntered(Students std)
        {
            students[index++] = std;
        }
    }
```

### Composition
```C#
class HumanBody
    {
        Head head;

        public HumanBody()
        {
            head = new Head(); //composition
        }

        public void Think() //can access head
        {
        }
    }
```

### Inheritance
```C#
class Human : Creature
    {
        public int ID;

        public Human():base()  //calling the constructor of the parent class (parameterless)
        {
        }

        public Human(int id, int age) : base(age) //calling the constructor of the parent class (parameterized)
        {
            ID = id;
        }

        public void Think()
        {
            //nameof = "";
            //this.Name = "";
            base.Name = ""; //reference pointing to the parent class
        }
        weight = 100;
    }
```