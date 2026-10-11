destructing arrays is a way of unpacking values from an array or an object into seperate varibales 

destructing is break the complex data strcutures into a smaller datas ctructure like a variable

```javascript

const arr = [1,2,3];
const a = arr[0];
const b = arr[1];
const c = arr[2];

const [x, y, z] = arr;
console.log(x, y, z);
```

```javascript
"use strict";

const restaurant = {
  name: "Classico Italiano",
  location: "Via Angelo Tavanti 23, Firenze, Italy",
  categories: ["Italian", "Pizzeria", "Vegetarian", "Organic"],
  starterMenu: ["Focaccia", "Bruschetta", "Garlic Bread", "Caprese Salad"],
  mainMenu: ["Pizza", "Pasta", "Risotto"],
}

const [first, second] = restaurant.categories;
console.log(first, second);
```

if we want the third one, we use
```javascript
const [first, , second] = restaurant.categories;
```

for swapping elements or variables
```javascript
let [main, , secondary] = restaurant.categories;
console.log(main, secondary);

//swapping both variables
[main, secondary] = [secondary, main];
console.log(main, secondary);
```

Nested Destructing
```javascript
const nested = [2,4,[5,6]];

const [i, , [j,k]] = nested;

console.log(i,j,k);
```

Default values
```javascript
const [p = 1, q = 1,r = 1] = [8,9]
console.log(p,q,r)  //8,9,1
```

Deconstructing Objects
```javascript
const restaurant = {
  name: "Classico Italiano",
  location: "Via Angelo Tavanti 23, Firenze, Italy",
  categories: ["Italian", "Pizzeria", "Vegetarian", "Organic"],
  starterMenu: ["Focaccia", "Bruschetta", "Garlic Bread", "Caprese Salad"],
  mainMenu: ["Pizza", "Pasta", "Risotto"],
}

const {name,categories} = restaurant;
console.log(name,categories);
```

if we want to rename them 
```javascript
"use strict";

  

const restaurant = {

  name: "Classico Italiano",

  location: "Via Angelo Tavanti 23, Firenze, Italy",

  categories: ["Italian", "Pizzeria", "Vegetarian", "Organic"],

  starterMenu: ["Focaccia", "Bruschetta", "Garlic Bread", "Caprese Salad"],

  mainMenu: ["Pizza", "Pasta", "Risotto"],

}

  

const {

  name: restaurantName,

  location: restaurantLocation,

  categories: restaurantCategories,

} = restaurant;

console.log(restaurantName, restaurantLocation, restaurantCategories);
```

if we want to have default values in case the destructing found out there is no values for such key instead of getting undefined
```javascript
"use strict";

  

const restaurant = {

  name: "Classico Italiano",

  location: "Via Angelo Tavanti 23, Firenze, Italy",

  categories: ["Italian", "Pizzeria", "Vegetarian", "Organic"],

  starterMenu: ["Focaccia", "Bruschetta", "Garlic Bread", "Caprese Salad"],

  mainMenu: ["Pizza", "Pasta", "Risotto"],

}

  

const {

  menu = [],

  starterMenu: starters = []

} = restaurant;

console.log(menu, starters);
```

Overwritting the varibales 
```javascript
//mutating variables

let a = 111;

let b = 999;

const obj = { a: 23, b: 7, c: 14 };

({ a, b } = obj);

console.log(a, b);

```

Nested objects
```javascript
//nested objects
const {fri} = restaurant.openingHours;
console.log(fri)
```

```javascript
const {
  fri: { open, close }
} = restaurant.openingHours;

console.log(open, close); 
// Output: 11 23
```

---
The spread operator( )
bascically expand the array into all its elements, unpacking all the aray elements all at one

```javascript
const arr = [7,6,8];

const newArr = [1,2,3,...arr];

console.log(newArr);
```

for dict by expanding an array
```javascript
const newMenu = {...restaurant.mainMenu,`GNocci`};
console.log(newMenu);
```

Diff between the spread operator and destrcutuing :
- both extract elements from tthe arrays  , the spread operator takes them all elements from an array at once and does nto create a new variables
- COnstartins -> becuas ehte spread opertore doesn not crewate new variabeles , it can only be used in places where you would otherwise ,write values seperated by commas 

```javascript
//copy array 
const mainMenuCopy = [...restaurant.mainMenu]; //shallow copy

//join 2 arrays
const menu = [...restaurant.starterMenu, ...restaurant.mainMenu];
console.log(menu);
```

spread operator works on all iterables
iterables are arrays , strings , maps , sets -- Anything except the object
```javascript
const str = "Jonas";

const leters = [...str, ' ', 'S'];

console.log(leters);

console.log("-------------------");

console.log(...str);
```

```
[
  'J', 'o', 'n',
  'a', 's', ' ',
  'S'
]
-------------------
J o n a s
```

multiple values seperated by a comma are usually only expected when we pass arguments into a function or building a new array

on function's arguments
```javascript
"use strict";

const restaurant = {
  name: "Classico Italiano",
  location: "Via Angelo Tavanti 23, Firenze, Italy",
  categories: ["Italian", "Pizzeria", "Vegetarian", "Organic"],
  starterMenu: ["Focaccia", "Bruschetta", "Garlic Bread", "Caprese Salad"],
  mainMenu: ["Pizza", "Pasta", "Risotto"],
  openingHours: {
    thu: {
      open: 12,
      close: 22,
    },
    fri: {
      open: 11,
      close: 23,
    },
  },
  orderPasta: function (ing1, ing2, ing3) {
    console.log(`Here is your delicious pasta with ${ing1}, ${ing2} and ${ing3}`);
  },
}

const ingredients = ["tomato", "basil", "mozzarella"];
restaurant.orderPasta(...ingredients);
```

Objects spreading
```javascript
//Objects
const newRestaurant = {
	foundedIn = 1998,
	...restaurant,
	founder = "Guispise"
}
console.log(newRestaurant)
```

```javascript
const resaturantCopy = {...restaurant};
restaurantCopy.name = "Reisisnt ROma";

console.log(restaurantCopy.name);
console.log(restaurant.name);
```

----
Rest Patterns and Parameters
