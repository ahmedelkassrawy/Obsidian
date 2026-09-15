---
description: "Defines the three C++ class access specifiers (public, protected, private) in terms of what a derived class and its objects may touch."
domain: cs
type: concept
status: stub
tags:
  - domain/cs
  - type/concept
  - status/stub
  - topic/c-language
  - topic/oop
aliases:
  - "access specifiers"
hubs:
  - "[[C++ Language]]"
  - "[[OOP]]"
---
## Class Access Specifiers

- `public`: the _object_ of the **derived** class can be treated as an object of the **base** class.
- `protected`: more restrictive than `public`, but allows **derived** classes to know details of _parents_.
- `private`: prevents objects of the **derived** class to be treated as objects of **base** class.

