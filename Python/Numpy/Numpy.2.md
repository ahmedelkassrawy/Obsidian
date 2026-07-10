```python
print(id(my_list[0])) #located away from each other
print(id(my_list[1]))

print(id(my_array[0]))
print(id(my_array[1])) #located beside each other

my_list_of_data = [ 1,2,"A","B" ,True,10.50]
my_array_of_data = np.array([1,2,"A","B",True,10.50])

print(my_list_of_data) #deals with each type of data on its own
print(my_array_of_data) #he deals with the data as same type which is string
  
print(type(my_list_of_data[0])) #integer
print(type(my_array_of_data[0])) #numpy.str

my_array_of_data_two = np.array([1,2]) #numpy.int32 after removing the data
#if we put 10.5 it becomes float
#if we put "A" it becomes string
```