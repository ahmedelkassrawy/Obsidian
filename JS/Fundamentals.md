```javascript
let js = "amazing";

if (js === "amazing") alert("JS is FUN!");
```

# JavaScript Fundamentals

## What JavaScript Is
- A **high-level language** → you don't worry about memory management yourself.
- **Object-based** → most kinds of data are stored using objects.

The three languages of a web page:
- **Content** → HTML → the *nouns* (a paragraph, an image).
- **Presentation** → CSS → the *adjectives* (make it red, make it big).
- **Programming** → JS → the *verbs / logic* (make things happen).

---

## Values and Variables
- A **value** is a piece of data.
- A **variable** stores a value.

**Declaring a variable** creates it in your computer's memory and puts a value inside it:
```javascript
let js = "amazing";
```

Think of a variable as a **box**: the box holds an object, and the label on the box describes what's inside.

---

## Objects vs Primitives
Every value is either an **object** or a **primitive** (everything that isn't an object).

**Object:**
```javascript
let me = { name: "Jonas" };
```

**Primitive:**
```javascript
let firstName = "Jonas";
let age = 5;
```

### Primitive data types
`number`, `string`, `boolean`, `undefined`, `null`, `symbol`, `bigint`.

- **Number**: every number is the same type, `number`, whether whole or decimal. `23` is really stored as `23.0` (floating point).
  ```javascript
  let age = 23;
  ```
- **String**: text.
- **Boolean**: `true` or `false`.
- **Undefined**: the value of a variable that has been declared but not given a value yet (an empty value).
  ```javascript
  let children; // undefined
  ```
- **Null**: also an empty value (you set it on purpose).
- **Symbol**: a unique value that can never be changed, often used as a special identifier.
- **BigInt**: for integers larger than the `number` type can safely hold.

> Note: `symbol` and `bigint` are advanced, so you rarely touch them early on. Just know they exist.

### Dynamic typing
JS has **dynamic typing**: you don't declare the type of a value. JS figures it out automatically, and a variable can even hold a different type later.

`typeof` tells you the type of a value or variable:
```javascript
let country = "EGYPT";
console.log(typeof country); // "string"
```

```javascript
let js;
console.log(js);        // undefined
console.log(typeof js); // "undefined"
```

---

## let, const, and var
- **`let`**: you can reassign it later (mutate it):
  ```javascript
  let age = 30;
  age = 31; // OK
  ```
- **`const`**: you **cannot** reassign it:
  ```javascript
  const birthYear = 1981;
  birthYear = 1980; // TypeError: Assignment to constant variable
  ```
  Because you can't leave it empty, **there is no such thing as an undefined `const`**: you must give it a value right away.

> Avoid declaring a variable with no keyword (`x = 5;`). It doesn't create a proper variable in the current scope. Instead, JS quietly creates a property on the global object. Bad practice.

---

## Operators
```javascript
const ageJonas = 2038 - 1919;
const ageSarah = 2038 - 2018;

console.log(ageJonas, ageSarah); // 119 20
```

String concatenation with `+`:
```javascript
const firstName = "Jonas";
const lastName = "Schmedtmann";

console.log(firstName + lastName);         // "JonasSchmedtmann"
console.log(firstName + " " + lastName);   // "Jonas Schmedtmann"
```

`+=`, `-=`, `x++`, `x--` all work like in C++.

### Template literals
Use backticks `` ` `` and `${ }` to drop values straight into a string, much cleaner than `+`:
```javascript
const jonas = `I'm ${firstName} ${lastName}, ${ageJonas} years old`;
console.log(jonas);
```

Backtick strings can also span multiple lines directly:
```javascript
// These two produce the same thing:
console.log("String with \n\
multiple \n\
lines");

console.log(`String
multiple
lines`);
```

---

## Type Conversion vs Type Coercion
- **Conversion**: *you* manually change a type.
- **Coercion**: JS changes types automatically, behind the scenes, without you seeing it.

**Conversion:**
```javascript
const input = "1991";
console.log(Number(input) + 91); // 2082
console.log(String(input));      // "1991"
console.log(Boolean(input));     // true
```
`Number(...)` gives **`NaN`** ("Not a Number") when the conversion fails.

**Coercion:**
```javascript
console.log("I'm a " + 23 + " years old");   // "+" makes numbers into strings
console.log("I'm a " + "23" + " years old");

console.log("23" - "10" - 3); // 10  → converted to numbers
console.log("23" + "10" + 3); // "23103" → converted to strings

console.log("23" * "2");      // 46 → converted to numbers
```

Rule of thumb:
- `+` triggers **string** conversion.
- `-`, `*`, `/` trigger **number** conversion.

---

## Truthy and Falsy Values
**Falsy** values become `false` when converted to a boolean. There are only a few:
`0`, `""` (empty string), `undefined`, `null`, `NaN`, and `false`. Everything else is **truthy**.
```javascript
console.log(Boolean(0));         // false
console.log(Boolean(undefined)); // false
console.log(Boolean("Jonas"));   // true
console.log(Boolean({}));        // true  (even an empty object is truthy)
```

---

## Equality Operators
- **`===`** strict equality, **no** coercion. Only `true` when both value *and* type match.
  ```javascript
  console.log(19 === 19); // true
  ```
- **`==`** loose equality, **does** coercion, so it can give surprising results. Avoid it.
  ```javascript
  console.log("19" == 19); // true — "19" was coerced to a number
  ```

> Default to `===`. It saves you from sneaky bugs.

---

## Taking Input
```javascript
const num = prompt("What's the number you want to check?");
// prompt() always returns a string — convert with Number() if you need a number
```

---

## Logical Operators
- `&&` → AND
- `||` → OR
- `!` → NOT

---

## Expressions vs Statements
- An **expression** produces a value (`3 + 4`, `"a" + "b"`).
- A **statement** is a bigger piece of code that performs an action but doesn't itself produce a value (like an `if` block or a `for` loop).

---

## Ternary Operator
A compact `if/else` that *is* an expression (produces a value):
```javascript
const drink = age >= 18 ? "wine" : "water";
console.log(drink);
```

---

## Strict Mode
Put this at the very top of a file to catch more errors and forbid unsafe things. It **must** use quotes (backticks don't work here):
```javascript
"use strict";
```

---

## Functions
Declare a function with the `function` keyword:
```javascript
function logger() {
  console.log("My name is Jonas");
}

logger();

function fruit(numApples, numOranges) {
  console.log(numApples, numOranges);
  const juice = `Juice with ${numApples} apples and ${numOranges} oranges.`;
  return juice; // hands a value back to whoever called it
}

const appleJuice = fruit(5, 0);
console.log(appleJuice);

const appleOrangeJuice = fruit(2, 4);
console.log(appleOrangeJuice);
```

### Functions are values
In JS, **functions are just values**, not a separate type. Because a function is a value, you can store it in a variable.

### Function expression (anonymous function)
You don't name the function; you store it in a variable. The function is written as an *expression*, which always produces a value:
```javascript
// Function declaration
function calcAge(birthYear) {
  return 2026 - birthYear;
}
const age = calcAge(1990);
console.log(age); // 36

// Function expression (anonymous)
const calcAge2 = function (birthYear) {
  return 2026 - birthYear;
};
console.log(calcAge2(1990)); // 36
```

**Key difference:** you can call a function **declaration** *before* it appears in the code (this is called *hoisting*). You **cannot** do that with a function expression.
```javascript
const agee = calcAge(1990); // works, even though calcAge is defined below

function calcAge(birthYear) {
  return 2026 - birthYear;
}

console.log(agee);
```

### Arrow functions
A shorter form of a function expression. With one line, the `return` is **implicit**:
```javascript
const calcAge = birthYear => 2026 - birthYear;
console.log(calcAge(1990));
```

With a code block (`{ }`), you must write `return` yourself:
```javascript
const yearsUntilRetirement = birthYear => {
  const age = 2026 - birthYear;
  const retirement = 65 - age;
  return retirement;
};

console.log(yearsUntilRetirement(1990)); // 29
```

For multiple parameters, wrap them in parentheses: `(birthYear, firstName) => ...`.

### Functions calling other functions
```javascript
function cutFruit(fruit) {
  return fruit * 4;
}

function fruitProcessor(apples, oranges) {
  const applePieces = cutFruit(apples);
  const orangePieces = cutFruit(oranges);

  const juice = `Juice with ${applePieces} pieces of apple and ${orangePieces} pieces of orange.`;
  return juice;
}

console.log(fruitProcessor(2, 3));
```

> You can't write `if (apples > 0) const applePieces = ...`: a `const` can't be the single-line body of an `if`, and even if it could, the variable would only exist *inside* that `if` and be invisible below. Declare the variables outside any `if`.

![[Pasted image 20260820212316.png]]

---

## Arrays
> "You said `const` variables can't be changed, so how did I change an element in this array?"
> Only **primitive values** are immutable. An array is **not** a primitive, so you can still change (mutate) its *contents*. What you *can't* do is reassign the whole variable to a brand-new array.

You also can't do math on arrays as a whole.

```javascript
const friend1 = "Michael";
const friend2 = "Steven";
const friend3 = "Peter";

// Two ways to make an array:
const friends = [friend1, friend2, friend3];
const years = new Array(1991, 1984, 2008, 2020);

console.log(friends[0]);                    // first element  → "Michael"
console.log(friends.length);                // how many elements → 3
console.log(friends[friends.length - 1]);   // last element → "Peter"

friends[2] = "Jay"; // mutate an element (allowed even with const)
console.log(friends);

// Arrays can hold mixed types, other arrays, and results of functions:
const firstName = "Jonas";
const array2 = [firstName, "Bob", 2037 - 1991, friends];

const calcAge = function (birthYear) {
  return 2037 - birthYear;
};

const ages = [
  calcAge(years[0]),
  calcAge(years[1]),
  calcAge(years[years.length - 1]),
];
console.log(ages);
```

### Array methods
**`push`**: add to the **end**. Returns the array's new length:
```javascript
const friends = ["Michael", "Steven", "Peter"];
const len = friends.push("Jay");
console.log(friends); // [..., "Jay"]
console.log(len);     // 4
```

**`unshift`**: add to the **beginning**:
```javascript
friends.unshift("Bruno");
```

**`pop`**: remove the **last** element (returns the removed one):
```javascript
const popped = friends.pop();
console.log(popped);
```

**`shift`**: remove the **first** element (returns the removed one):
```javascript
const removed = friends.shift();
console.log(removed);
```

**`indexOf`**: the index of an element, or `-1` if it's not there:
```javascript
console.log(friends.indexOf("Steven")); // 1
console.log(friends.indexOf("Bruno"));  // -1
```

**`includes`**: `true`/`false` whether the element exists. Uses `===`, so **no coercion**: looking for `23` won't match `"23"`:
```javascript
console.log(friends.includes("Steven")); // true
console.log(friends.includes("Bruno"));  // false
```

---

## Objects
Objects store data as **key-value pairs**, so each value has a name. Use objects to **group things that belong together**; use **arrays** for ordered lists.

### Object literal syntax
```javascript
const jonas = {
  firstName: "Jonas",
  lastName: "Schmedtmann",
  age: 2037 - 1991,
  friends: ["Michael", "Peter", "Steven"],
};

console.log(jonas);
console.log(jonas.lastName);    // dot notation → "Schmedtmann"
console.log(jonas["lastName"]); // bracket notation → same
```

**Dot vs bracket:** bracket notation can take **any expression** inside the `[ ]`, so you can compute the key name:
```javascript
const nameKey = "Name";
console.log(jonas["first" + nameKey]); // reads jonas.firstName → "Jonas"
console.log(jonas["last" + nameKey]);  // reads jonas.lastName  → "Schmedtmann"
```

That's why bracket notation is what you need when the key comes from a variable or user input:
```javascript
const interested = prompt(
  "What do you want to know about Jonas? firstName, lastName, age, or friends"
);
console.log(jonas[interested]); // works — the string is evaluated as the key
console.log(jonas.interested);  // undefined — there's no key literally called "interested"
```

### Adding new keys
```javascript
jonas.location = "Portugal";
jonas["twitter"] = "@jonasschmedtman";
console.log(jonas);
```

Objects, like arrays, can hold any type of data, including functions.

### Methods (functions inside objects)
```javascript
const jonas = {
  firstName: "Jonas",
  lastName: "Schmedtmann",
  birthYear: 1991,
  friends: ["Michael", "Peter", "Steven"],
  calcAge: function (birthYear) {
    return 2037 - birthYear;
  },
};

console.log(jonas.calcAge(jonas.birthYear));    // 46
console.log(jonas["calcAge"](jonas.birthYear)); // 46
```

### The `this` keyword
Instead of passing `birthYear` in, the method can read it off the object it belongs to using `this`:
```javascript
const jonas = {
  firstName: "Jonas",
  lastName: "Schmedtmann",
  birthYear: 1991,
  friends: ["Michael", "Peter", "Steven"],
  calcAge: function () {
    return 2037 - this.birthYear; // this = the object that called the method
  },
};

console.log(jonas.calcAge()); // 46
```

`this` refers to the object **calling** the method. So inside `jonas.calcAge()`, `this` **is** `jonas`:
```javascript
this.birthYear;  // same as jonas.birthYear
console.log(this); // logs the whole jonas object
```

**Caching a computed value**: calculate once, store it on the object, and reuse it:
```javascript
const jonas = {
  firstName: "Jonas",
  lastName: "Schmedtmann",
  birthYear: 1991,
  friends: ["Michael", "Peter", "Steven"],
  calcAge: function () {
    this.age = 2037 - this.birthYear; // store the result on the object
    return this.age;
  },
};

console.log(jonas.calcAge()); // calculates and stores
console.log(jonas.age);       // reads the stored value — no recalculation
```

---

## Loops

### for loop
Runs **as long as** the condition is true:
```javascript
for (let rep = 0; rep < 10; rep++) {
  console.log("Hello World");
}
```

You can use the counter inside the loop:
```javascript
for (let rep = 0; rep < 10; rep++) {
  console.log(`Hello world ${rep + 1}`);
}
```

**Looping over an array:**
```javascript
const arr1 = [1, 2, 3];
for (let i = 0; i < arr1.length; i++) {
  console.log(arr1[i]);
}
```

**Backwards:**
```javascript
const arr1 = [1, 2, 3];
for (let i = arr1.length - 1; i >= 0; i--) {
  console.log(arr1[i]);
}
```

**Nested (double) loops:**
```javascript
for (let i = 0; i < 5; i++) {
  console.log(`##### hello round: ${i}`);
  for (let j = 0; j < 5; j++) {
    console.log(`world round: ${j}`);
  }
}
```

### for...in: looping over an object's keys
```javascript
const jonas = {
  firstName: "Jonas",
  lastName: "Schmedtmann",
};

for (const key in jonas) {
  console.log(`Key: ${key}`);
  console.log(`Value: ${jonas[key]}`); // bracket notation, because key is a variable
}
```

### while loop
Use when you don't know how many times you'll loop (no counter needed up front):
```javascript
let cnt = 0;
while (cnt < 10) {
  cnt++;
  console.log(cnt);
}
```
