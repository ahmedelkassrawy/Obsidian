---
description: "Hub: every note about Python Language"
type: hub
domain: cs
tags:
  - type/hub
  - topic/python-language
---
# Python Language

> [!info] The best-maintained language cluster: decorators, data modeling, JSON/serialization, Protocol vs ABC, Pydantic, pytest. Missing generators/iterators, async, and typing beyond Pydantic.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/python-language`.

## Concepts
- [[Data Modeling]] — Why a class and why an enum: a type is the set of values a slot may hold, so pick types that make illegal states unrepresentable and validate once at the boundary.
- [[Decorators]] — Decorators built from the one fact that `@deco` means `f = deco(f)`: the two-layer basic decorator with functools.wraps, then the three-layer decorator that takes an argument.
- [[Exceptions]] — The try statement's clauses - try, except, else, finally - and what each one is for.
- [[JSON Serialization]] — Serialization as two arrows - object to text when saving, text to object when loading - with the real output shown at each step and how enums and datetimes have to be converted.
- [[Lambda And Map]] — Lambda expressions as anonymous one-off functions, and using them with map and other higher-order functions.
- [[OOP]] — Python classes end to end: defining a class and methods, what `self` actually refers to, instances, class attributes, and inheritance with super().
- [[Protocol vs ABC]] — Two ways to write an interface in Python: Protocol (structural, duck typing, nothing to inherit) vs ABC (nominal, explicit inheritance, can share code) - with a side-by-side of when each fits.
- [[Singleton]] — Explains the Singleton pattern, a __new__-based Python implementation, and its pros, cons and sane use cases.

## How-tos & recipes
- [[Creating a CLI (argparse)]] — How to build a subcommand CLI with argparse: main parser, subparsers, arguments and routing to handlers.
- [[Testing with pytest]] — pytest aimed at validation: the habit of testing that bad input is rejected with pytest.raises, not just that good input constructs, and isolating one variable per test.
- [[Reading And Writing Files]] `stub` — Opening a file for read and for write, and the `with` form that closes it automatically.
- [[Saving Data To JSON Snippets]] `raw` — Two snippets for writing data to disk: dump a dict or list as JSON, and append to an existing JSON array while surviving a corrupted file.

## References & cheat sheets
- [[Iterating With Enumerate And Zip]] — Looping helpers: iterating a dict by key and by items, enumerate for index-plus-value, and zip for walking two iterables together.
- [[Pydantic]] — Pydantic v2 in practice: when to use it and when not to, BaseModel basics, enums to close a value set, field_validator for one field vs model_validator across fields.
- [[Python Review]] — A refresher sweep over Python basics - containers (lists, dicts) and control flow (if/elif/else, nesting) - written as a quick review.
- [[Counter]] `stub` — One snippet using collections.Counter and most_common(1) to get the mode of a list.

## Course notes
- [[Data Structures]] — Session 1 course notes on Python's built-in containers - lists, tuples, sets, dictionaries - with a table comparing them, plus control flow.

## Related hubs
[[Pydantic]], [[OOP]], [[System Design]], [[Testing]]

## Notes to self (from the audit)
- [[Iterating With Enumerate And Zip]]: Old name 'ESC' was not a word - it was shorthand for the enumerate/zip section.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
