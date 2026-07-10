- all variables allocated automatically in the stack
- **vectors headers** are stored in the stack , but **data** at the heap
- What happens when you call a function?
	- function parameters are pushed to stack
	- N function calls are equivalent to the O(N) stack complexity
- creating an array of size N **automatically** is equivalent to O(N) stack complexity
- Creating an array of size N **dynamically** is equivalent to O(N) heap complexity

Stack: Stores function call frames, including parameters, return addresses, and local variables.

Heap -> dynamic memory allocation
**What is stored**:
- **Dynamically allocated objects**: Objects whose size or lifetime is determined at runtime (e.g., arrays, objects, or strings in many languages).
- **Large or complex data structures**: Lists, trees, or objects that require flexible sizing.

|Feature|Stack|Heap|
|---|---|---|
|**Allocation**|Automatic, by compiler|Manual (C/C++) or automatic (Java, Python)|
|**Speed**|Very fast|Slower due to dynamic allocation|
|**Size**|Limited (fixed size)|Larger, limited by system memory|
|**Lifetime**|Scope-based (function exit)|Persists until freed or GC'd|
|**Management**|Compiler-managed|Programmer or garbage collector|
|**Use Case**|Local variables, function calls|Dynamic objects, large data|
|**Risks**|Stack overflow|Memory leaks, fragmentation|
