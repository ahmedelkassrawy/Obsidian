---
description: "Hub: every note about OOP"
type: hub
domain: cs
tags:
  - type/hub
  - topic/oop
---
# OOP

> [!info] Classes, inheritance, polymorphism, static members, enums, boxing. Split three ways - C#, C++ and Python notes all teaching the same ideas. Pick a canonical one.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/oop`.

## Concepts
- [[Constructor]] — Explains that a constructor runs automatically when an object is declared, must share the class name, has no return type, and is where member variables get initialised.
- [[OOP]] — Beginner walkthrough of declaring a C++ class, creating objects, the access specifiers, and encapsulation through getters and setters.
- [[OOP]] — Python classes end to end: defining a class and methods, what `self` actually refers to, instances, class attributes, and inheritance with super().
- [[Protocol vs ABC]] — Two ways to write an interface in Python: Protocol (structural, duck typing, nothing to inherit) vs ABC (nominal, explicit inheritance, can share code) - with a side-by-side of when each fits.
- [[Classes]] `stub` — Defines the three C++ class access specifiers (public, protected, private) in terms of what a derived class and its objects may touch.
- [[Static Polymorphism]] `stub` — One paragraph defining static (compile-time) polymorphism and naming function overloading and templates as the ways to get it.

## Course notes
- [[Association Aggregation And Composition]] — The four ways classes relate in C#: association (an object is passed or created in a method), aggregation, composition, and inheritance.
- [[Enums Structs And Boxing]] — Enums instead of magic integers, structs and how they differ from classes, and boxing/unboxing between value and reference types in C#.
- [[Inheritance And Polymorphism]] — Continues inheritance in C# - calling base methods with `base.` - then polymorphism through virtual and overridden methods.
- [[Overriding Object Methods]] — Overriding the methods every C# object inherits - Equals, and the safe-casting problem it creates - so two objects compare by value.
- [[Static Members And Overloading]] — Static members and static methods in C# (a factorial helper with no instance), then overloading both functions and operators.

## Related hubs
[[C++ Language]], [[Python Language]]

## Notes to self (from the audit)
- [[Classes]]: Under 60 words - fill in with a worked class example.
- [[OOP]]: Overlaps the OOP/ folder (which teaches the same ideas in C#) and Python/OOP.md - pick one as the canonical OOP note.
- [[Association Aggregation And Composition]]: The OOP/ folder is a C# course, not C++ - every snippet in this note is C#.
- [[Inheritance And Polymorphism]]: The OOP/ folder is a C# course, not C++ - every snippet in this note is C#.
- [[Static Members And Overloading]]: The OOP/ folder is a C# course, not C++ - every snippet in this note is C#.
- [[Overriding Object Methods]]: The OOP/ folder is a C# course, not C++ - every snippet in this note is C#.
- [[Enums Structs And Boxing]]: The OOP/ folder is a C# course, not C++ - every snippet in this note is C#.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
