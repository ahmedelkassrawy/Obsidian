---
description: "Hub: every note about C++ Language"
type: hub
domain: cs
tags:
  - type/hub
  - topic/c-language
---
# C++ Language

> [!info] Scope and linkage, references, pointers, templates, type conversion, overloading, headers, namespaces. Reasonable; pointers and strings are still snippet-only stubs.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/c-language`.

## Concepts
- [[Constructor]] — Explains that a constructor runs automatically when an object is declared, must share the class name, has no return type, and is where member variables get initialised.
- [[Control Flow]] — Covers `if constexpr` (the compiler drops the dead branch at compile time) and the switch statement, with the compiled-away version shown side by side.
- [[Forward Declaration]] — Explains forward declarations: declaring a function's signature before its body so callers above it compile, and the difference between a declaration and a definition.
- [[Function Overloading]] — Explains how C++ picks between same-named functions with different parameter types, and what makes a call an ambiguous match.
- [[Header Files]] — Explains why declarations go in a header and get #included, so a multi-file program does not repeat them.
- [[Lambda And Map]] — Covers default parameter values, passing arguments by reference, and a pointer to function overloading.
- [[Local and Global Variables]] — The longest C++ note here: local scope and lifetime, global variables, internal vs external linkage, and why globals are worth avoiding.
- [[Namespace]] — Explains a namespace as a named area whose contents are reached through that name, with the using-directive and scope-resolution forms.
- [[OOP]] — Beginner walkthrough of declaring a C++ class, creating objects, the access specifiers, and encapsulation through getters and setters.
- [[References]] — Explains a reference as a second name for the same storage (house vs address analogy), how it must be initialised, and how it is used for function parameters.
- [[Templates]] — Explains why templates exist - one function or class that works for many types instead of near-identical copies - and how the compiler instantiates them.
- [[Type Conversion]] — Covers implicit type conversion (no value is changed, a new one is produced), the traps of unsigned-to-signed conversion, and type aliases.
- [[Classes]] `stub` — Defines the three C++ class access specifiers (public, protected, private) in terms of what a derived class and its objects may touch.
- [[Pointers]] `stub` — A single snippet showing a pointer holding the address of a string and printing the value, the address, and the dereferenced value.
- [[Stack vs Heap]] `stub` — Bullet notes on what lives on the stack vs the heap and what happens to the stack on each function call.
- [[Static Polymorphism]] `stub` — One paragraph defining static (compile-time) polymorphism and naming function overloading and templates as the ways to get it.
- [[Strings]] `stub` — Two snippets: reading a whole line with getline, and checking whether a character is a digit.
- [[Struct With Custom Comparator]] `stub` — Snippets showing an anonymous struct instance and a named struct whose members are set through the dot operator.

## References & cheat sheets
- [[C++ Solving Tips - Ternary And Palindrome]] — Small contest habits: rewriting an if/else as a ternary, and the two-pointer palindrome check.
- [[C++ Contest Notes - Precision And Ceil]] `stub` — Two contest snippets: fixed setprecision for decimal output, and what ceil returns.
- [[C++ Contest Template]] `stub` — The contest boilerplate: the usual includes plus the sync_with_stdio / cin.tie fast-IO lines.
- [[Reading Input With Cin And Getline]] `stub` — Why cin leaves the newline behind and how that breaks a following getline, with the fix.
- [[Struct With Custom Comparator]] `stub` — A Dragon struct plus the compare function used to sort a vector of them - the custom-comparator pattern.

## Solved problems
- [[Structs - 3D Points]] — C++ solution that defines a point struct with x, y and z, stores the points in an array, and works over them; includes a short Arabic walkthrough of the struct.
- [[Structs - Highest Y]] `raw` — C++ solution that sorts an array of point structs by y descending with a custom comparator and prints them.

## Meta
- [[C++]] `stub` — Hub page for the CPP folder - a list of links to the other C++ notes plus one setprecision snippet.

## Related hubs
[[OOP]], [[String Algorithms]], [[Operating Systems]]

## Notes to self (from the audit)
- [[Stack vs Heap]]: Stub - no allocation cost or fragmentation discussion yet.
- [[Classes]]: Under 60 words - fill in with a worked class example.
- [[Forward Declaration]]: Old filename misspelled 'declaration' as 'deceleration'.
- [[OOP]]: Overlaps the OOP/ folder (which teaches the same ideas in C#) and Python/OOP.md - pick one as the canonical OOP note.
- [[Pointers]]: Code only, no explanation - needs the pointer-arithmetic and null-pointer sections.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
