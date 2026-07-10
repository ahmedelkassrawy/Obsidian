```python
import numpy as np

#Create array with specific data type
my_array1 = np.array([1,2,3], dtype="f") #float or "float" or "f"
my_array2 = np.array([1.5, 20.15, 3.601], dtype = int) #int or "int" or "i"
my_array3 = np.array(["Osama5ara","B","Ahmed"], dtype = int) #Errror
 
#Change data type of existing array
my_array4 = np.array([0,1,2,3,4,5])
my_array4 = my_array4.astype("float")
print(my_array4.dtype)
print(my_array4) 

#Test Capacity
my_array8 = np.array([100, 200, 300, 400], dtype='f')
print(my_array8.dtype)
print(my_array8[0].itemsize) # 4 Bytes
 

my_array8 = my_array8.astype('float') # Change To Float64
print(my_array8.dtype)
print(my_array8[0].itemsize) # 8 Bytes
```