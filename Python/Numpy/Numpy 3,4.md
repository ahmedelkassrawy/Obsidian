Memory Usage in arrays using numpy = 800
while using normal lists use 2800

The time of execution also takes round 0.0xx secs in numpy
in the list takes about 15.xx secs

```python
import numpy as np

#Slicing => [Start:End:Steps] Not including end
a = np.array(["A","B","c","D","E","F"])
  
print(a.ndim)
print(a[1])
print(a[2:4])

b = np.array([["A","B","X"],["C","D","Y"],["E","F","Z"], ["M","N","O"]])
print(b.ndim)
print(b[0:3])
print("#" * 50)
print(b[:3, :2]) #accessing the first 3 arrays then accessing the first and second element inside of each array
```