```python
import numpy as np
#create arrays
my_list = [1,2,3,4,5]
my_array = np.array(my_list)
  
print(my_list)
print(my_array)


print(type(my_list)) #class list
print(type(my_array)) #class numpy.ndarray
#number dimensional array

#Accessing Elements
print(my_list[0]) #same as usual
print(my_array[0]) #same as usual

a = np.array(10) #zero dimensional since its just a number 
b = np.array([10,20]) #1 dimesnion could access in one command
c = np.array([[1,2],[3,4]]) #2 dimension requires 2 commands
d = np.array( [ [ [5,6 ], [ 7,9 ] ] , [ [ 1,3] , [4,8] ] ]) #3 dimension requires 3 commands  

print(d[1,1,1])

#Number of dimensions
print(a.ndim) #returns the number of dimensions
print(b.ndim)
print(c.ndim)
print(d.ndim)

#Custom Dimensions
my_custom_array = np.array([1,2,3], ndmin = 3) # lets min dimesnions = 3
```