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
