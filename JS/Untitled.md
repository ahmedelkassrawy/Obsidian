```javascript
let js = "amazing"

if(js === "amazing") alert("JS is FUN!")
```

high level language -> dont worry about memory stuff
Based on objects for storing most kind of data

content -> HTML5 -> Nouns like paragraph
Presentation  -> CSS -> adjectives
Programming language -> JS -> hide

a value is a a piece of data
variables can store values

Declaring a variable 
 this will actually create a variable in your computers memory and we store the value inside of that variable
```javascript
let js = "aamzing"
```

imagine the varaiable as a box, in real world a box can hold an object , and then you can write  a label on the box to describe whats init 

every value is either an object or a primitive value (everything else)

Object
```javascript
let me = {name: "Jonas"};
```

Primitive
```javascript
let firstName = "Jonas";
let age = 5;
```

value is primitive when its not an object 

Primitive data types
number , string , boolean , undefined , null , symbol and big int

Number -> floating numbers
```javascript
let age = 23;
```

this means that this number is 23.0, all numbers are of the type number

Undefined: value taken by a variable that is not defined (empty value) 
```javascript
let children;
```

Null = empty value
Symbol : large int than the number type can hold

JS has dynamic typing , we don't have to manually define the data type of the value stored in a variable , instead the data types are determined automatically 

typeof -> tells you the data type of a variable or a value
```javascript
let country = "EGYPT";

console.log(typeof country); // Output: string
```

undefined
```javascript
let js;
console.log(js); //undefined
console.log(typeof js) //undefined
```

let -> we can reassign a value to variables any time (mutate the variable)
```javascript
let age = 30;
age = 31;
```

const -> creates a variable we cannot reassign (immutable variable)
```javascript
const birthYear = 1981;
birthYear = 1980;
```

**there is no undefined const variables 

You can just say the variable = value , without using  let or const 
but a warning its not a good convention because this doesnt create a variable in the current so called scope, instead JS will create a property on the global object  

Operators
we can print two values using the same console.log
```javascript
const ageJonas = 2038 - 1919;
const ageSarah = 2038 - 2018;

console.log(ageJonas, ageSarah); // prints 46 19
```

```javascript
const firstName = 'Jonas';

const lastName = 'Schmedtmann';

console.log(firstName + LastName); //JonasSchemedtman
console.log(firstName + " " + LastName); //Jonas Schemedtman
```

we can still use "+=" sign like c++ and "x++" also works
  
Template Literals
```javascript
const jonas = `I'm ${firstName} ${lastName}, a ${ageJonas} years old`;

console.log(jonas);
```

They are both the same lines
```javascript
console.log(`String with \n\
    multiple \n\
    lines`);

console.log(`String
    multiple
    lines`)
```               

Type conversion and Type Coercion
- conversion is when we manually convert from one type to another
- coercion is when JS automatically convert types behind the scenes for us but it happens implicilty , completely hidden from us

Conversion
```javascript
const input = "1991";
console.log(Number(input) + 91);
console.log(String(input))
console.log(Boolean(input))
```

Number function gives us a NaN (Not a number) if any number operations fail

Coercion
```javascript
console.log(`I'm a` + 23 + `years old`);
console.log(`I'm a` + `23` + `years old`);

console.log(`23` - `10` - 3); //converted to numbers
console.log(`23` + `10` + 3); //converted to strings

console.log(`23` * `2`) //converted to numbers
```

the +  operator triggers the strings conversion 
the - ,"**" , /  operator triggers the number conversion

Truthy and Falsy values
Falsy values are the values that when converted to boolean will give false
```javascript
console.log(Boolean(0)); //false
console.log(Boolean(undefined)); //false
console.log(Boolean("Jonas")); //true
console.log(Boolean({})); //true
```

=== (Strict equality operator) -> because it doesnt perform type coercion and so it only returns true when both values are exactly the same
```javascript
console.log(19 === 19); //true
```

== (loose equality operator) -> does type coercion
```javascript
console.log("19" == 19) //true, coercion happend and it was converted to a number
```

taking input
```javascript
const nuu = prompt("Whats the number you want to check?");
//it takes it as a string
```

&& -> AND 
| | -> OR
! -> NOT

expression is something that gives a value
statement is a bigger code that is executed and which doesnt producer a value on itself

ternanry operator
```javascript
const drink = age >= 18 ? "wine" : "water";
console.log(drink);
```

Use strict mode to get a better view of the errors
```javascript
`use strict`;
```

Functions
we declare a function using the keyword function
```javascript
function logger()
{
    console.log('My name is Jonas');
}

logger();

function fruit(num_apples,num_oranges)
{
    console.log(num_apples,num_oranges);
    const juice = `Juice with ${num_apples} apples and ${num_oranges} oranges.`;
    return juice;
}

const appleJuice = fruit(5,0);
console.log(appleJuice);

const appleOrangeJuice = fruit(2,4);
console.log(appleOrangeJuice);
```

anonymous function
we dont give the function a name we just declare a variable and attach the function to it , it appears as an expression which always produces a value
```javascript
function calcAge(birthYear) 
{
    return 2026 - birthYear;
}

const age = calcAge(1990);
console.log(age); // Output: 36

////////////////////////////////////////////
///////////////////////////////////////////

//anonymous function
const ageee = function (birthYear)
{
    return 2026 - birthYear;
}
console.log(ageee(1990)); // Output: 36
```

In fact in javascript functions are actually just values so just as a number or a string or a boolean so function is not a type, its not like a string or a number type its a value and since its a value it can be stored in a variable

difference between function declarations and function expressions is we can actually call function declarations before they are defined in the code
```javascript
const agee = calcAge(1990);

function calcAge(birthYear)
{
    return 2026 - birthYear;
}

console.log(agee);
```

arrow function is simply a special form of function expression  is shorter and therefore faster to write
return happens implicitly 
```javascript
const calcAge = birthYear => 2026 - birthYear;
const agee = calcAge(1990);
console.log(agee);
```

```javascript
const yearsUntilRetirement = birthYear => {
    const age = 2026 - birthYear;
    const retirement = 65 - age;
    return retirement;
}

console.log(yearsUntilRetirement(1990)); // Output: 29
```

for multiple params use ( ) at the params like (birthYear,firstName)

Functions calling other functions
```javascript
function cutFruit(fruit)
{
    return fruit * 4;
}

function fruitProcessor(apples,oranges)
{
    if(apples > 0) const applePieces = cutFruit(apples);
    if(oranges > 0) const orangePieces = cutFruit(oranges);

    const juice = `Juice with ${applePieces} pieces of apple and ${orangePieces} pieces of orange.`;
    return juice;
}

const appleJuice = fruitProcessor(2, 0);
console.log(appleJuice);
```