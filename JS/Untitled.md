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