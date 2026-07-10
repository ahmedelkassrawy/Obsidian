```python
class Dog: #class definition
    def bark(self): #Method
        print("bark") #method implmentation

d = Dog() #Instance Creation
d.bark() #using method
print(type(d))

```

`self` is a reference to the current instance of the class.
`d` is a variable that is being assigned a new instance of the `Dog` class.
`Dog()` calls the constructor of the `Dog` class to create a new `Dog` object.

```python
class Dog:
    def __init__(self,name,age): #initialization of the dog class
        self.name = name  #atrribute for dog called name
        self.age = age

    def get_name(self): #getter
        return self.name

    def get_age(self): #getter
        return self.age

    def set_age(self,age): #setter
        self.age = age

  
d = Dog("Tim",34)
d.set_age(23)
print(d.get_age())
```

```python
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def get_grade(self): #getter 
        return self.grade
    
class Course:
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = [] #attributes dont have to be included in intialiaztion arguments above

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student) #adding the student of class Student to the list of students in class of course
            return True
        return False
    
    def get_average_grade(self):
        value = 0
        for student in self.students: #for loop in the list of students of class course
            value += student.get_grade() #attribute of class student
        return value / len(self.students) if self.students else 0
    
s1 = Student("Tim", 19, 95)
s2 = Student("Bill", 19, 75)
s3 = Student("Jill", 19, 65)

course = Course("Science", 2)
course.add_student(s1)
course.add_student(s2)
print(course.get_average_grade())
```

#### `add_student` Method

```python
def add_student(self, student):
    if len(self.students) < self.max_students:
        self.students.append(student)
        return True
    return False

```
- **Purpose:** Adds a student to the course if the course is not full.
- **Parameters:**
    - `student`: An instance of the `Student` class.
- **Functionality:** Checks if the number of enrolled students is less than the maximum allowed. If so, adds the student to the `students` list and returns `True`; otherwise, returns `False`.

## Inheritance
```python
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print("I am {} and I am {} years old".format(self.name, self.age))

  
class Cat(Pet):
    def speak(self):
        print("Meow")
class Dog(Pet):
    def speak(self):
        print("Bark")

p = Pet("Tim", 19)
p.show() # Output: I am Tim and I am 19 years old
c = Cat("Bill",19)
c.show()
```

```python
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print("I am {} and I am {} years old".format(self.name, self.age))


class Cat(Pet):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def show(self):
        print("I am {} and I am {} years old. My color is {}".format(self.name, self.age, self.color))


class Dog(Pet):
    def speak(self):
        print("Bark")


p = Pet("Tim", 19)
p.show()  # Output: I am Tim and I am 19 years old
c = Cat("Bill", 19, "brown")
c.show()  # Output: I am Bill and I am 19 years old. My color is brown

```

Using `super().__init__(name, age)` in the `Cat` class ensures that the initialization logic defined in the `Pet` class is executed. This is especially useful in a hierarchy of classes where the base class (`Pet`) has specific initialization that needs to be carried out for all derived classes.

Here's why using `super().__init__` is important, even though we already inherit from `Pet`:

1. **Code Reusability**: It allows the `Cat` class to reuse the initialization logic from the `Pet` class without duplicating code. If the `Pet` class has complex initialization logic, this ensures that it is correctly executed for all subclasses.
    
2. **Maintenance**: If the initialization logic in the `Pet` class changes (e.g., additional attributes or setup steps are added), using `super().__init__` ensures that these changes are automatically propagated to all subclasses without needing to modify each one.
    
3. **Multiple Inheritance**: In cases where a class inherits from multiple base classes, using `super()` ensures that the correct initialization order is maintained according to the method resolution order (MRO).
    

Here's an example to illustrate the benefits of using `super()`:
```python
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print("Pet initialized")

    def show(self):
        print("I am {} and I am {} years old".format(self.name, self.age))


class Cat(Pet):
    def __init__(self, name, age, color):
        super().__init__(name, age)  # Calls Pet's __init__
        self.color = color
        print("Cat initialized")

    def show(self):
        print("I am {} and I am {} years old. My color is {}".format(self.name, self.age, self.color))


class Dog(Pet):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # Calls Pet's __init__
        self.breed = breed
        print("Dog initialized")

    def speak(self):
        print("Bark")


p = Pet("Tim", 19)
p.show()  # Output: I am Tim and I am 19 years old
c = Cat("Bill", 19, "brown")
c.show()  # Output: I am Bill and I am 19 years old. My color is brown
d = Dog("Max", 5, "Golden Retriever")
d.show()  # Output: I am Max and I am 5 years old

# Outputs:
# Pet initialized
# Cat initialized
# Pet initialized
# Dog initialized

```

- The `Pet`'s `__init__` method is called for both `Cat` and `Dog` because of `super().__init__`.
- The initialization message from the `Pet` class is printed for both `Cat` and `Dog`, showing that the base class initialization is performed.
- This ensures consistent initialization logic across all subclasses.
## Class Attributes AND Methods

```python
class Person:
    number_of_people = 0  # Class attribute, shared by all instances

    def __init__(self, name):
        self.name = name
        Person.number_of_people += 1  # Increment the class attribute

# Create instances of Person
p1 = Person("Tim")
p2 = Person("Jill")

# Print the number of Person instances created
print(Person.number_of_people)  # Output: 2

```

for class method example
```python
class Person:
    number_of_people = 0  # class attribute, shared among all instances

    def __init__(self, name):
        self.name = name
        Person.add_people()
    
    @classmethod
    def number_of_people_(cls):
        return cls.number_of_people
    
    @classmethod
    def add_people(cls):
        cls.number_of_people += 1

p1 = Person("Tim")
p2 = Person("Jill")
print(Person.number_of_people)

```
### Explanation:

1. **Class Attribute (`number_of_people`)**: This is a class attribute that belongs to the class itself rather than any instance. It keeps track of the number of `Person` instances created.
    
2. **Constructor (`__init__`)**: The constructor method (`__init__`) initializes an instance of the class with the given name and then calls the class method `add_people` to increment the `number_of_people` counter.
    
3. **Class Method (`number_of_people_`)**: This class method returns the current count of people (the value of `number_of_people`).
    
4. **Class Method (`add_people`)**: This class method increments the `number_of_people` counter by 1 each time a new instance of `Person` is created.

Static Method
This means that you can call a static method without creating an object of the class first
```python
class Math:
    @staticmethod
    def add5(x):
        return x + 5
        
    @staticmethod
    def add10(x):
        return x + 10

print(Math.add5(5))
```