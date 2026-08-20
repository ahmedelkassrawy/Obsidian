---
tags: [python, typing, protocol, abc, interfaces, design]
source: Track A · postqueue · Lesson 3 (the Storage checklist)
updated: 2026-08-17
---
# Protocol vs ABC — writing an "interface" in Python

> Both are ways to say *"anything used here must be able to do X, Y, Z."* The difference is **how a class conforms** and **whether the contract can hand out shared code.**

Two plain pictures:
- **Protocol = a checklist of abilities.** You qualify by *being able to do the tasks*. Nobody checks your family tree.
- **ABC = an official sign-up form + a starter kit.** You must *formally join* (inherit it), and in return you can get some *ready-made code* for free.

---

## Why you'd want an "interface" at all

So your code depends on a **capability**, not a specific class. Example: `postqueue` needs *something that can save/get/list/delete posts*. Today that's a JSON file; later a database. If your commands depend on "a Storage" (the checklist) instead of "JsonStore" specifically, you swap the implementation and **change one line**, nothing else. → program to an interface, not an implementation.

---

## Protocol — structural ("duck typing")

```python
from typing import Protocol
from models import Post

class Storage(Protocol):
    def save(self, post: Post) -> None: ...
    def get(self, id: int) -> Post | None: ...
    def list(self) -> list[Post]: ...
    def delete(self, id: int) -> None: ...

class JsonStore:                       # NOTE: no (Storage) base class
    def save(self, post: Post) -> None: ...
    def get(self, id: int) -> Post | None: ...
    def list(self) -> list[Post]: ...
    def delete(self, id: int) -> None: ...

def add_post(store: Storage, post: Post) -> None:
    store.save(post)

add_post(JsonStore(), some_post)       # ✓ accepted purely because it has the 4 methods
```

- Conform by **just having the methods** — no subclassing, no importing the Protocol.
- The implementer (`JsonStore`) **doesn't even need to know `Storage` exists** → the classes stay independent (looser coupling).
- Bodies are `...` — a Protocol declares shape, it never implements.
- "If it walks like a duck and quacks like a duck, it's a duck." The fancy name is **structural subtyping** (PEP 544).

---

## ABC — nominal (explicit inheritance + shared code)

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, post: Post) -> None: ...

	# SHARED concrete code — the ABC superpower
    def describe(self) -> str: 
        return f"{type(self).__name__} store"

class JsonStore(Storage):                 # MUST subclass
    def save(self, post: Post) -> None: ...
```

- Conform by **subclassing** — explicit, checked at runtime (can't instantiate if an `@abstractmethod` is unfilled).
- Can provide **shared concrete methods** every subclass inherits — the reason to pick ABC.
- The implementer **depends on** the ABC (imports + inherits it).

---

## The difference, side by side

| | **Protocol** (structural) | **ABC** (nominal) |
|---|---|---|
| How you conform | just have the methods | must `class X(TheABC)` |
| Does the class know the contract? | no — stays independent | yes — imports + inherits it |
| Can share ready-made code? | ❌ checklist only | ✅ concrete methods inherited |
| Checked | by the type checker, by shape | at runtime, by inheritance |
| Works on code you don't own | ✅ any class that fits, retroactively | ❌ can't add a base to a stdlib/3rd-party class |
| Coupling | looser | tighter |

---

## When to consider each

**Reach for a Protocol (the usual default) when:**
- You only need a **checklist of abilities** and want implementers to stay simple/separate.
- You want a class you **don't own** (stdlib, 3rd-party) to satisfy the contract.
- You're matching Python's natural duck typing.

**Reach for an ABC when:**
- You want to **share implementation** — give every subclass ready-made helper methods.
- You want to **force an explicit "I am a Storage" declaration** (subclassing as documentation/intent).
- You want a hard runtime guarantee that missing methods block instantiation.

**One-line rule:** *Just a shape?* → Protocol. *Shape + shared code (or forced sign-up)?* → ABC.

---

## The safety net in action (structural check)

```python
class BadStore:                 # missing delete()
    def save(self, post: Post) -> None: ...
    def get(self, id: int) -> Post | None: ...
    def list(self) -> list[Post]: ...

bad: Storage = BadStore()
# mypy error:
#   "BadStore" is missing following "Storage" protocol member:  delete
```

mypy names the exact missing method — **before it ever runs**, with no inheritance anywhere. That's a Protocol earning its keep.

---

## Extras (optional)

- **Generic Protocol** — one checklist for any type:
  ```python
  from typing import Protocol, TypeVar
  T = TypeVar("T")
  class Storage(Protocol[T]):
      def save(self, item: T) -> None: ...
  x: Storage[Post]                    # "a Storage of Posts"
  # Python 3.12+ shorthand:  class Storage[T](Protocol): ...
  ```
- **`@runtime_checkable`** — lets you use `isinstance(x, Storage)` at runtime, but it only checks **method names exist**, not their signatures/types.

---

## Quick reference

```
interface = "must be able to do X,Y,Z" ; program to it, not to a concrete class
Protocol : just have the methods ; no base class ; implementer stays independent ; NO shared code
ABC      : must subclass ; implementer depends on it ; CAN share concrete methods
default  : Protocol (shape only). ABC when you need shared code or forced sign-up.
check    : Protocol -> mypy, structural (by shape) | ABC -> runtime, by inheritance
generic  : class Storage(Protocol[T]) + TypeVar   (== TS <T>)
```

**Track B bridge:** a Python `Protocol` ≈ a TypeScript `interface`; `TypeVar`/`Generic[T]` ≈ TS `<T>`. Shutterabia's `SocialProvider` is this exact pattern in TS.

**Sources:** [PEP 544 / typing spec — Protocols](https://typing.python.org/en/latest/spec/protocol.html) · [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) · [`abc`](https://docs.python.org/3/library/abc.html) · Lesson: `D:\me\teach\lessons\0005-storage-protocol.html`
