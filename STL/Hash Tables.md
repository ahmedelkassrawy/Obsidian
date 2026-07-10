- In technical terminology, we’d say that a hash function “maps strings to numbers.”
- . Arrays and lists map straight to memory, but hash tables are smarter. They use a hash function to intelligently figure out where to store elements.
```Python
phone_book = {}
or 
phone_book = dict()
```

## Uses
1. Lookups are darn fast!!
2. Preventing Duplicates
3. Using hash tables as a cache

There are two lessons here: Your hash function is really important. Your hash function mapped all the keys to a single slot. Ideally, your hash function would map keys evenly all over the hash. If those linked lists get long, it slows down your hash table a lot. But they won’t get long if you use a good hash function! Hash functions are important. A good hash function will give you very few collisions.

To avoid collisions, 
- you need A low load factor 
- A good hash function

## Advanced Reading
Loading factor = num of items in hash table / total no. of slots.

*Once the load factor starts to grow, you need to add more slots to your hash table. This is called resizing.