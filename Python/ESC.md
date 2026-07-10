```python
cast = {
           "Jerry Seinfeld": "Jerry Seinfeld",
           "Julia Louis-Dreyfus": "Elaine Benes",
           "Jason Alexander": "George Costanza",
           "Michael Richards": "Cosmo Kramer"
       }

print("Iterating through keys:")
for key in cast:
    print(key)

print("\nIterating through keys and values:")
for key, value in cast.items():
    print("Actor: {}    Role: {}".format(key, value))
```

#### Enumerate

`enumerate` is a built in function that returns an iterator of tuples containing indices and values of a list. You'll often use this when you want the index along with each element of an iterable in a loop.
```python
letters = ['a', 'b', 'c', 'd', 'e'] 
for i, letter in enumerate(letters):     
	print(i, letter)`

This code would output:

0 a 
1 b 
2 c 
3 d 
4 e
```

### Zip
```python
#You could unpack each tuple in a `for` loop like this.

letters = ['a', 'b', 'c'] 
nums = [1, 2, 3] 
for letter, num in zip(letters, nums):     
	print("{}: {}".format(letter, num))

#In addition to zipping two lists together, you can also unzip a list into tuples using an asterisk.

some_list = [('a', 1), ('b', 2), ('c', 3)] 
letters, nums = zip(*some_list)`

#This would create the same `letters` and `nums` tuples we saw earlier.
```

Transpose with Zip
```python
data = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)) 
data_transpose = tuple(zip(*data)) 
print(data_transpose)

((0, 3, 6, 9), (1, 4, 7, 10), (2, 5, 8, 11))
```

Enumarate
```python
cast = ["Barney Stinson", "Robin Scherbatsky", "Ted Mosby", "Lily Aldrin", "Marshall Eriksen"] 
heights = [72, 68, 72, 66, 76] 
for i, character in enumerate(cast): 
cast[i] = character + " " + str(heights[i]) print(cast)
```