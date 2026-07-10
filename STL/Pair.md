[Pair in C++ Standard Template Library (STL) - GeeksforGeeks](https://www.geeksforgeeks.org/pair-in-cpp-stl/)

Pair is used to combine together two values that may be of different data types.

- The first element is referenced as ‘first’ and the second element as ‘second’ and the order is fixed (first, second).
- - Pair can be assigned, copied, and compared. The array of objects allocated in a [map](http://www.geeksforgeeks.org/map-associative-containers-the-c-standard-template-library-stl/) or hash_map is of type ‘pair’ by default in which all the ‘first’ elements are unique keys associated with their ‘second’ value objects.
- To access the elements, we use variable name followed by dot operator followed by the keyword first or second.

```C++
pair <data_type1, data_type2> Pair_name
```

- you could have the pairs different types not only same types.

## Functions:
1. make_pair()
	1. allows to create a pair without writing it the types explicity .
```C++
	`PAIR3 = make_pair(``"GeeksForGeeks is Best"``, 4.56);`
```

1. swap()
	1. swaping a pair with another pair of the same type.
```C++
	pair1.swap(pair2) ;
```

1. tie()
	1. works same as tuple
	2. creates a tuple lvalue refrences to its arguments
```C++
	pair<int,int> pair1 = { 1, 2 };
    int a, b;
    tie(a, b) = pair1;
    cout << a <<` `" "` `<< b <<` `"\n"``;

//could ignore a value of the pair either x or y
	pair<int,int> pair2 = { 3, 4 };
    tie(a, ignore) = pair2;


```

![[Pasted image 20241020182255.png]]
**it sorts according to the first element so if you want to sort a value make it in first not in second**