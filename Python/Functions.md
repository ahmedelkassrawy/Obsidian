## Lambda Expressions

You can use lambda expressions to create anonymous functions. That is, functions that don’t have a name. They are helpful for creating quick functions that aren’t needed later in your code. This can be especially useful for higher order functions, or functions that take in other functions as arguments.

With a lambda expression, this function:
```python
def multiply(x, y): 
	return x * y

multiply = lambda x, y: x * y
```

#### Components of a Lambda Function

1. The `lambda` keyword is used to indicate that this is a lambda expression.
2. Following `lambda` are one or more arguments for the anonymous function separated by commas, followed by a colon `:`. Similar to functions, the way the arguments are named in a lambda expression is arbitrary.
3. Last is an expression that is evaluated and returned in this function. This is a lot like an expression you might see as a return statement in a function.

With this structure, lambda expressions aren’t ideal for complex functions, but can be very useful for short, simple functions.



## Map Functions
```python
def myfunc(n):  
  return len(n)  
  
x = map(myfunc, ('apple', 'banana', 'cherry'))
```

The `map()` function executes a specified function for each item in an iterable. The item is sent to the function as a parameter.

---> map(_function_, _iterables_)
iterable --> a sequence or collection
```python
numbers = [
              [34, 63, 88, 71, 29],
              [90, 78, 51, 27, 45],
              [63, 37, 85, 46, 22],
              [51, 22, 34, 11, 18]
           ]

def mean(num_list):
    return sum(num_list) / len(num_list)

averages = list(map(mean, numbers))
print(averages)
```