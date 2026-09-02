Talking about JS under the hood and what it offers:
High Level 
any computer needs resources , JS you don't have to manage any resources at all it does that for you, but not as fast or optimized as low level 

Garbage Collected 
it cleans the memory up for you so you don't have to

Interpreted or just in time compiled
the code is converted to machine code or compiled inside the JS engine

Multi Paradigm
a Pradigm -> an approach and mindset of structuring code which will direct your coding style and technique

the most popular paradigms are :
- Procedural programming -> What we have been doing
- OOP
- Functional Programming

Prototype based object oriented 
almost everyhting in the JS is an object except for primitive values such as numbers , strings , etc
but arrays for example as just objects and we already saw that in the practice , why can we use the push and pop methods for example on them its because of the prototypal inheritance bascially we create arrays from an array blueprint ,we create the array from a prototype and its like the blueprint for the arrays and that prototype contains all the array methods and then we inherit the methods from the prototype

![[Pasted image 20260901183419.png]]

First class functions
In a language with first class functions , functions are simply treated as variables, we can pass them into other functions and return them from functions

dynamic typed langugae 
so no data type definitions and types becomes known at runtime 

single threaded  & non blocking event loop
Concurrency model -> how the JS engine handles the multiple tasks happening at the same time 
why do we need that ?
because JS runs in one single thread so it can only do one thing at a time
but what if there is a long running task?
sounds like it would block the single thread, however we want non blocking behaviour 
how do we do that?
By using an event loop , takes long running tasks and executes them in the background and puts them back in the main thread once they are finished