# Python Programming: Session 1 - Data Structures and Control Flow

## Agenda
- Data Containers
- Control Flow

## Data Containers

Python provides several built-in data structures (or containers) to organize and manage data efficiently. These include lists, tuples, sets, and dictionaries.

### Lists

A list is an ordered, mutable collection of items. Lists can contain items of different types, including other lists.

#### Syntax
Lists are defined using square brackets `[]`.

```python
fruits = ["apple", "banana", "cherry"]
```

#### Key Characteristics
- **Ordered**: Lists allow access to items using an index.
- **Mutable**: You can add, delete, or modify items in a list.
- **Non-Unique Items**: Lists can contain duplicate elements.
- **Mixed Data Types**: Lists can hold items of different data types.

#### Lists Operations

##### Indexing
Access elements using their index (starting at 0).

```python
print(fruits[0])  # Output: apple
```

##### Slicing
Access a range of elements.

```python
print(fruits[0:2])  # Output: ['apple', 'banana']
```

##### Adding Elements
Use `append()` to add an item, `insert()` to add at a specific index.

```python
fruits.append("orange")
fruits.insert(1, "mango")
```

##### Removing Elements
Use `remove()` to delete an item, `pop()` to remove by index.

```python
fruits.remove("banana")
fruits.pop(2)
```

### Tuples

A tuple is an ordered, immutable collection of items. Once defined, its contents cannot be changed.

#### Syntax
Tuples are defined using parentheses `()`.

#### Operations
- Indexing and Slicing: Similar to lists.
- Immutability: Cannot change elements, which makes tuples faster for read-only data.

#### Key Characteristics
- **Ordered**: Tuples allow access to items using an index.
- **Immutable**: You cannot add, delete, or modify items in a tuple.
- **Non-Unique Items**: Tuples can contain duplicate elements.
- **Mixed Data Types**: Tuples can hold items of different data types.

### Sets

A set is an unordered collection of unique items. Sets are used for membership testing and eliminating duplicate entries.

#### Syntax
Sets are defined using curly braces `{}` or the `set()` function.

#### Operations
- Adding Elements: Use `add()`.
- Removing Elements: Use `remove()` or `discard()`.
- Set Operations: Union, intersection, difference.

#### Key Characteristics
- **Unordered**: Sets do not maintain a specific order of items.
- **No Indexing/Slicing**: Sets do not support indexing or slicing operations.
- **Immutable Data Types**: Sets can only contain immutable data types (e.g., numbers, strings, tuples).
- **Unique Items**: Sets automatically remove duplicate items, ensuring all elements are unique.

### Dictionaries

A dictionary is an unordered collection of key-value pairs. Keys must be unique and immutable (e.g., strings, numbers).

#### Syntax
Defined using curly braces `{}` with key-value pairs separated by colons.

```python
student = {"name": "Alice", "age": 20, "courses": ["Math", "Science"]}
```

#### Operations
- Accessing Values: Use keys.

```python
print(student["name"])  # Output: Alice
```

- Adding/Updating: Assign a value to a key.

```python
student["age"] = 21
student["grade"] = "A"
```

- Removing Items: Use `pop()` to remove a key-value pair.

#### Key Characteristics
- **Key-Value Pairs**: Dictionaries store data as key-value pairs.
- **Immutable Keys**: Dictionary keys must be immutable (e.g., numbers, strings, tuples).
- **Flexible Values**: Dictionary values can be of any data type.
- **Unique Keys**: Each key in a dictionary must be unique.
- **Unordered**: Dictionaries are not ordered; elements are accessed using keys.

### Comparing Lists, Tuples, Sets, Dictionaries

| Feature          | List              | Tuple             | Set               | Dictionary        |
|------------------|-------------------|-------------------|-------------------|-------------------|
| Syntax           | `[]` or `list()`  | `()` or `tuple()` | `{}` or `set()`   | `{}` or `dict()`  |
| Order            | Ordered           | Ordered           | Unordered         | Unordered         |
| Mutability       | Changeable        | Unchangeable      | Unchangeable      | Changeable        |
| Access           | Indexed           | Indexed           | Unindexed         | Key-Value pair    |
| Duplicates       | Allows Duplicates | Allows Duplicates | No Duplicates     | No Duplicates     |
| Slicing          | Allows Slicing    | Allows Slicing    | No Slicing        | No Slicing        |

## Control Flow

Control flow statements are essential in programming as they enable the execution of specific blocks of code based on conditions. This allows for dynamic decision-making within a program. In Python, the primary control flow statements include `if`, `elif`, and `else`.

### If Statements

The `if` statement is used to test a specific condition. If the condition evaluates to `True`, the code block under the `if` statement is executed.

#### Syntax
```python
if condition:
    # Code to execute if condition is true
```

#### Examples

##### Check Positive Number
This code checks if the number is greater than zero. Since 5 > 0 is true, it prints "The number is positive."

##### Check String Length
The code checks if the length of the string name is greater than 3. Since "Alice" has 5 characters, the condition is true, and it prints "The name is longer than 3 characters."

##### Check Membership in List
```python
fruits = ["apple", "banana", "cherry"]
if "banana" in fruits:
    print("Banana is in the list.")
```
Output: Banana is in the list.

##### Check if Variable is Not None
```python
result = None
if result is None:
    print("Result is not set yet.")
```
Output: Result is not set yet.

### If-Else Statements

The `if-else` statement provides an alternative block of code that is executed if the condition is `False`.

#### Examples

##### Check Even or Odd Number
This code checks if number is even by using the modulus operator %. Since 4 % 2 == 0 is true, it prints "Even number."

##### Age Verification
```python
age = 17
if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
```
Output: You are not eligible to vote.

##### Check for Empty List
```python
items = []
if items:
    print("The list is not empty.")
else:
    print("The list is empty.")
```
Output: The list is empty.

##### Temperature Check
This code checks if the temperature is greater than 20. Since 15 is not greater than 20, it prints "It's cold outside."

### If-Elif-Else Statements

The `if-elif-else` statement allows checking multiple conditions sequentially. Only the block of the first `True` condition is executed. If none of the conditions are `True`, the `else` block is executed.

#### Examples

##### Grading System
This code assigns grades based on score. Since the score is 72, it matches the `elif score >= 70:` condition, so it prints "Grade C."

##### Traffic Light Signal
```python
traffic_light = "yellow"
if traffic_light == "red":
    print("Stop")
elif traffic_light == "yellow":
    print("Slow down")
elif traffic_light == "green":
    print("Go")
else:
    print("Invalid signal")
```
Output: Slow down

##### Classify Age Group
```python
age = 35
if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
elif age < 65:
    print("Adult")
else:
    print("Senior")
```
Output: Adult

##### Check Temperature Range
```python
temperature = 30
if temperature < 0:
    print("Freezing")
elif temperature <= 20:
    print("Cold")
elif temperature <= 30:
    print("Warm")
else:
    print("Hot")
```
Output: Warm

### Nested If Statements

If statements can be nested within other if statements to create complex conditions.

#### Examples

##### Permission Check with Age
This code checks if age is less than 18 and then checks if has_permission is True. Since both conditions are met, it prints "You can enter with permission."

##### Nested Condition for Shopping
```python
has_discount = True
is_member = False
if has_discount:
    if is_member:
        print("You get a 20% discount.")
    else:
        print("You get a 10% discount.")
else:
    print("No discount available.")
```
Output: You get a 10% discount.

##### Nested Temperature and Time Check
```python
temperature = 22
time_of_day = "morning"
if temperature > 20:
    if time_of_day == "morning":
        print("It's warm and morning time.")
    else:
        print("It's warm but not morning.")
else:
    print("It's cold.")
```
Output: It's warm and morning time.

##### Bank Account Balance Check
This code checks if the balance is sufficient for the withdraw_amount and then checks if the amount is positive. Since both conditions are true, it prints "Transaction successful."