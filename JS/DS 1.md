---
tags: [javascript, destructuring, spread, rest]
---

## Destructuring

> [!definition] Destructuring
> Destructuring extracts values from an array or properties from an object into separate variables. It does not remove them from the original array or object.

Array destructuring uses **positions**. Object destructuring uses **property names**.

## Array destructuring

### Extracting values

Without destructuring, we access each element by its index:

```javascript
const arr = [1, 2, 3];
const a = arr[0];
const b = arr[1];
const c = arr[2];
```

Destructuring does the same extraction in one statement:

```javascript
const [x, y, z] = arr;
console.log(x, y, z); // 1 2 3
```

We will use this restaurant object throughout the examples. Run the examples separately when they reuse variable names.

```javascript
'use strict';

const restaurant = {
  name: 'Classico Italiano',
  location: 'Via Angelo Tavanti 23, Firenze, Italy',
  categories: ['Italian', 'Pizzeria', 'Vegetarian', 'Organic'],
  starterMenu: ['Focaccia', 'Bruschetta', 'Garlic Bread', 'Caprese Salad'],
  mainMenu: ['Pizza', 'Pasta', 'Risotto'],
  openingHours: {
    thu: { open: 12, close: 22 },
    fri: { open: 11, close: 23 },
    sat: {}, // Saturday's hours were not supplied in the transcript.
  },
  orderPasta: function (ing1, ing2, ing3) {
    console.log(`Here is your delicious pasta with ${ing1}, ${ing2} and ${ing3}`);
  },
};

const [first, second] = restaurant.categories;
console.log(first, second); // Italian Pizzeria
```

### Skipping elements

Leave a gap between commas to skip an element:

```javascript
const [first, , second] = restaurant.categories;
console.log(first, second); // Italian Vegetarian
```

The variable named `second` receives the third element because its position in the pattern determines what it gets.

### Swapping variables

```javascript
let [main, , secondary] = restaurant.categories;
console.log(main, secondary); // Italian Vegetarian

[main, secondary] = [secondary, main];
console.log(main, secondary); // Vegetarian Italian
```

The right side creates an array containing the current values in reverse order. The left side assigns those values back to the existing variables.

### Nested arrays

Use a nested pattern to extract values from an array inside another array:

```javascript
const nested = [2, 4, [5, 6]];
const [i, , [j, k]] = nested;

console.log(i, j, k); // 2 5 6
```

### Default values

```javascript
const [p = 1, q = 1, r = 1] = [8, 9];
console.log(p, q, r); // 8 9 1
```

> [!definition] Default value
> A destructuring default is used when the extracted value is `undefined`, including when an element or property is missing. It does not replace `null`, `0`, `false`, or an empty string.

## Object destructuring

### Extracting properties by name

```javascript
const { name, categories } = restaurant;
console.log(name, categories);
```

Unlike arrays, the order of the properties does not matter. JavaScript looks for the named properties.

### Renaming variables

```javascript
const {
  name: restaurantName,
  location: restaurantLocation,
  categories: restaurantCategories,
} = restaurant;

console.log(restaurantName, restaurantLocation, restaurantCategories);
```

In `name: restaurantName`, `name` is the property to read and `restaurantName` is the variable to create.

### Defaults and renaming together

```javascript
const {
  menu = [],
  starterMenu: starters = [],
} = restaurant;

console.log(menu);     // []: restaurant has no menu property
console.log(starters); // The existing starterMenu array
```

### Assigning to existing variables

```javascript
let a = 111;
let b = 999;
const obj = { a: 23, b: 7, c: 14 };

({ a, b } = obj);
console.log(a, b); // 23 7
```

The parentheses make JavaScript interpret this as an assignment expression. Without them, a statement starting with `{` would be interpreted as a block.

### Nested objects

First, extract the Friday object:

```javascript
const { fri } = restaurant.openingHours;
console.log(fri); // { open: 11, close: 23 }
```

Or extract its properties directly:

```javascript
const {
  fri: { open, close },
} = restaurant.openingHours;

console.log(open, close); // 11 23
```

Here, `fri` selects the nested object; `open` and `close` are the variables created.

## Destructuring objects passed as function arguments

### Receiving an object normally

```javascript
const person = {
  firstName: 'Jonas',
  age: 30,
};

function greet(person) {
  console.log(`Hey ${person.firstName}, you are ${person.age}`);
}

greet(person); // Hey Jonas, you are 30
```

The function receives one object and reads its properties using dot notation.

### Destructuring directly in the parameter

```javascript
function greet({ firstName, age }) {
  console.log(`Hey ${firstName}, you are ${age}`);
}

greet(person); // Hey Jonas, you are 30
```

> [!important] One object argument
> `{ firstName, age }` is a destructuring pattern. The function still receives one object, rather than two separate arguments. It extracts the object's properties into local parameter variables.

This works like destructuring at the beginning of the function:

```javascript
function greet(person) {
  const { firstName, age } = person;
  console.log(`Hey ${firstName}, you are ${age}`);
}
```

Properties are matched by name, so this call works too:

```javascript
greet({ age: 30, firstName: 'Jonas' });
```

### Several options, with defaults

Passing an object makes it clear which value belongs to which option:

```javascript
function orderDelivery({
  address,
  time = '19:00',
  mainIndex = 0,
  starterIndex = 0,
}) {
  console.log(`Deliver to ${address} at ${time}`);
  console.log(`Main: ${mainIndex}, starter: ${starterIndex}`);
}

orderDelivery({
  time: '20:00',
  address: 'Cairo',
  starterIndex: 1,
  mainIndex: 2,
});
// Deliver to Cairo at 20:00
// Main: 2, starter: 1

orderDelivery({ address: 'Cairo' });
// Deliver to Cairo at 19:00
// Main: 0, starter: 0
```

### Renaming a parameter variable

```javascript
function greet({ firstName: name, age }) {
  console.log(`Hey ${name}, you are ${age}`);
}

greet(person); // Hey Jonas, you are 30
```

The incoming property is still called `firstName`; the local variable is called `name`.

## Spread syntax

> [!definition] Spread
> Spread syntax (`...`) expands values into another array or into individual function arguments. In an object literal, object spread copies properties into the new object.

### Expanding and extending arrays

```javascript
const arr = [7, 6, 8];
const newArr = [1, 2, 3, ...arr];
console.log(newArr); // [1, 2, 3, 7, 6, 8]

const newMenu = [...restaurant.mainMenu, 'GNocci'];
console.log(newMenu); // ['Pizza', 'Pasta', 'Risotto', 'GNocci']
```

Spread does not create a variable for each extracted element. It supplies values where they are needed.

### Copying and joining arrays

```javascript
const mainMenuCopy = [...restaurant.mainMenu]; // Shallow copy
const menu = [...restaurant.starterMenu, ...restaurant.mainMenu];
console.log(menu);
```

### Iterables and strings

> [!definition] Iterable
> An iterable is a value that can supply its elements one by one. Arrays, strings, maps, and sets are examples.

```javascript
const str = 'Jonas';
const letters = [...str, ' ', 'S'];

console.log(letters); // ['J', 'o', 'n', 'a', 's', ' ', 'S']
console.log(...str);  // J o n a s
```

> [!note] Ordinary objects are different
> Array spread and function-call spread require an iterable. Ordinary objects are not iterable by default, but object spread still works because it copies properties rather than iterating over elements.

### Spreading function arguments

```javascript
const ingredients = ['tomato', 'basil', 'mozzarella'];
restaurant.orderPasta(...ingredients);
```

This passes three separate arguments, as if we had written:

```javascript
restaurant.orderPasta('tomato', 'basil', 'mozzarella');
```

### Spreading object properties

```javascript
const newRestaurant = {
  foundedIn: 1998,
  ...restaurant,
  founder: 'Guispise',
};

console.log(newRestaurant);
```

Object properties use `:`, not `=`, in an object literal.

```javascript
const restaurantCopy = { ...restaurant };
restaurantCopy.name = 'Reisisnt ROma';

console.log(restaurantCopy.name); // Reisisnt ROma
console.log(restaurant.name);     // Classico Italiano
```

> [!definition] Shallow copy
> A shallow copy creates a new outer array or object. Nested objects and arrays are still shared through their references.

## Rest patterns in destructuring

> [!definition] Rest
> Rest syntax (`...`) collects the remaining values into one array, or the remaining object properties into a new object. Spread expands; rest collects.

### Collecting remaining array elements

```javascript
const [a, b, ...others] = [1, 2, 3, 4, 5];
console.log(a, b, others); // 1 2 [3, 4, 5]
```

`a` receives the first value, `b` receives the second, and `others` collects everything after them.

```javascript
const [pizza, , risotto, ...otherFood] = [
  ...restaurant.mainMenu,
  ...restaurant.starterMenu,
];

console.log(pizza);     // Pizza
console.log(risotto);   // Risotto
console.log(otherFood); // ['Focaccia', 'Bruschetta', 'Garlic Bread', 'Caprese Salad']
```

The right side uses spread to build an array. The left side uses rest to collect the elements remaining after the first three positions. The skipped second element, `'Pasta'`, is not included in `otherFood`.

### Collecting remaining object properties

```javascript
const { sat, ...weekdays } = restaurant.openingHours;

console.log(sat);      // {} in this example
console.log(weekdays);
// {
//   thu: { open: 12, close: 22 },
//   fri: { open: 11, close: 23 }
// }
```

`sat` receives the Saturday property value. `weekdays` is a new object containing the remaining properties: `thu` and `fri`.

The original `openingHours` object keeps all three properties. The nested day objects are not deep-cloned.

## Rest parameters in functions

> [!definition] Rest parameter
> A rest parameter collects the remaining arguments passed to a function into an actual array.

### Accepting any number of arguments

```javascript
function add(...numbers) {
  let sum = 0;

  for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i];
  }

  console.log(sum);
}

add(2, 3);       // 5
add(5, 3, 7, 2); // 17
```

For the first call, `numbers` is `[2, 3]`. For the second, it is `[5, 3, 7, 2]`.

### Spread at the call, rest in the function

```javascript
const x = [23, 5, 7];
add(...x); // 35
```

1. `...x` spreads the array into three arguments: `23`, `5`, and `7`.
2. `...numbers` collects those arguments back into an array inside `add`.

This lets us call the same function with individual numbers or with values spread from an array.

### A first parameter followed by the rest

```javascript
restaurant.orderPizza = function (mainIngredient, ...otherIngredients) {
  console.log(mainIngredient);
  console.log(otherIngredients);
};

restaurant.orderPizza('mushrooms', 'onion', 'olives', 'spinach');
// mushrooms
// ['onion', 'olives', 'spinach']

restaurant.orderPizza('mushrooms');
// mushrooms
// []
```

The first argument goes into `mainIngredient`. All remaining arguments go into `otherIngredients`. If none remain, the rest parameter is an empty array.

> [!warning] A named parameter does not enforce a required argument
> The lecture describes the pizza's main ingredient as required, but this parameter alone does not enforce that rule. If no arguments are passed, `mainIngredient` is `undefined`; validation would be needed to reject that call.

## Recognizing spread versus rest

Look at what `...` is doing:
- **Spread:** supplies individual values or copies properties into a new object.
- **Rest:** collects remaining values or properties into one variable.

In destructuring, rest appears in the assignment pattern on the left. In functions, it appears in the parameter list. Spread appears when building an array or object, or when supplying arguments at a call.

> [!tip] Rest comes last
> A rest element in these destructuring patterns, or a rest parameter in a function, must come last so it can collect everything remaining.
