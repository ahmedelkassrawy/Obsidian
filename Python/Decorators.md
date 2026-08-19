---
tags: [python, decorators, functools, contextmanager, design]
source: Track A · postqueue · Lessons 5–7 (Day 3)
updated: 2026-08-17
---

# Decorators

> The one idea: **`@deco` on top of `def f` means exactly `f = deco(f)`.** A decorator is a function that takes a function and returns a (usually new) function. Everything else is what the wrapper chooses to do.

Prereq that must click first: **a function is just a value** — you can point a name at it (`g = f`, no parens), pass it around, and return it from another function.

```python
def shout(t): return t.upper()
yell = shout        # no () -> the function itself
yell("hi")          # "HI"   (shout("hi") runs it)
```

---

## 1. Basic decorator (2 layers) + `@wraps`

```python
import time
from functools import wraps

def timed(func):                        # takes the function
    @wraps(func)                        # keep func's name/docstring
    def wrapper(*args, **kwargs):       # a stand-in accepting ANY args
        start = time.perf_counter()
        result = func(*args, **kwargs)  # run the real function
        print(f"{func.__name__} took {time.perf_counter()-start:.4f}s")
        return result                   # hand its answer back
    return wrapper                      # return the wrapper

@timed
def add(a, b):
    "Add two numbers."
    return a + b
```

- `@timed` == `add = timed(add)`. After that line, `add` **is** the wrapper; the real `add` is tucked inside.
- `*args, **kwargs` = "forward whatever arguments came in" (works for any function).
- **Must `return result`** or the wrapped function silently returns `None`.
- **`@wraps(func)` preserves the wrapped function's identity** (`__name__`, `__doc__`, …). Without it, `add.__name__` becomes `"wrapper"` and the docstring is `None` — breaks debuggers/docs. Always include it.

`time.perf_counter()` > `time.time()` for measuring durations (higher precision, doesn't jump if the clock changes).

---

## 2. Decorator WITH an argument (3 layers) — `@retry(n)`

Parentheses mean the decorator is **configured first**. `retry(3)` runs, and whatever it **returns** is used as the decorator. So it needs one extra outer layer to catch the argument.

```python
from functools import wraps

def retry(times):                          # LAYER 1: catches the argument (3)
    def decorator(func):                   # LAYER 2: the normal decorator
        @wraps(func)
        def wrapper(*args, **kwargs):      # LAYER 3: does the work
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)   # success -> return now
                except Exception as e:
                    last_error = e
                    print(f"attempt {attempt} failed: {e}")
            raise last_error               # all tries used -> give up
        return wrapper
    return decorator
```

**The two-call truth:**
```python
@retry(3)
def fetch(): ...
# is exactly:
fetch = retry(3)(fetch)
#        └────┘ first call:  retry(3) RETURNS a decorator
#        └──────────┘ second call: decorator(fetch) returns the wrapper
```

`retry(3)` by itself is a **decorator factory** — it returns a decorator, not the final wrapper. The `()()` double-call is the visible sign of a decorator-with-an-argument. (Same shape as `@lru_cache(maxsize=100)`, `@app.route("/path")`.)

Test pattern — a counter that lives OUTSIDE the function (so it survives across retry calls):
```python
attempts = {"n": 0}

@retry(3)
def flaky():
    attempts["n"] += 1               # local `n = 0` would reset every call -> keep it outside
    if attempts["n"] < 3:
        raise Exception("not yet")
    return "ok on try 3"
```

---

## 3. A decorator that only REGISTERS — `@command`

A decorator doesn't have to *replace* your function. This one takes an argument, stores the function in a table, and returns it **unchanged** — its only job is the side effect of registering.

```python
COMMANDS = {}                      # name -> function

def command(name):
    def decorator(func):
        COMMANDS[name] = func       # store it
        return func                 # return UNCHANGED — no wrapper
    return decorator

@command("add")
def add_cmd(a, b): return a + b

@command("cancel")
def cancel_cmd(job_id): print(f"cancel {job_id}")

COMMANDS["add"](2, 3)      # 5    -- look up by name and call
COMMANDS.keys()           # dict_keys(['add', 'cancel'])
```

Replaces a growing `if word == "add": ... elif ...` with a **self-filling table**: add a command = write a function with `@command("name")`. This is the pattern behind CLI commands, plugin systems, event handlers, and **Shutterabia's provider registry**.

---

## 4. `@contextmanager` — build your own `with` block

A `with` block is "setup → your code → cleanup (guaranteed)". `open()` is one Python gives you. Build your own with one function split by `yield`:

```python
from contextlib import contextmanager

@contextmanager
def section(name):
    print(f"start {name}")     # SETUP: before the with-body
    yield                      # <-- the with-body runs HERE (the pause point)
    print(f"end {name}")       # CLEANUP: after the with-body

with section("saving"):
    print("doing the work")
# start saving / doing the work / end saving
```

- **`yield` is the pause point.** Before it = setup (runs when `with` starts); after it = cleanup (runs when the body finishes).
- **Give a value to `as x`** by yielding it:
  ```python
  @contextmanager
  def open_store(path):
      posts = load(path)     # setup
      yield posts            # -> `with open_store(p) as posts`
      save(path, posts)      # cleanup: write back on the way out
  ```
- **For real code:** wrap `yield` in `try/finally` so cleanup runs even if the body crashes (`finally` always runs).

Use it for any "always do X first, always do Y after" pair: open/close, load/save, start/stop timer, begin/commit transaction.

---

## Gotchas

- **Forgot `@`** → `retry(3)` runs and the result is thrown away; the function is NOT decorated. Tell-tale: none of the wrapper's behaviour happens.
- **Forgot `@wraps`** → wrapped function's `__name__` becomes `"wrapper"`, docstring gone.
- **Forgot `return result`** in the wrapper → wrapped function returns `None`.
- **State that must persist across calls** (a retry counter) must live OUTSIDE the function; a local resets every call.
- **`func` vs `func()`** → a decorator gets the function itself (`func`); you call it (`func(...)`) inside the wrapper.

---

## Quick reference

```
@deco            ==  name = deco(name)              (1 call)
@deco(arg)       ==  name = deco(arg)(name)         (2 calls: factory then wrap)
2-layer  timed(func) -> wrapper                       plain decorator
3-layer  retry(n) -> decorator(func) -> wrapper       decorator with an argument
register command(name) -> decorator(func){store; return func}   side-effect only, no wrapper
context  @contextmanager + yield : before=setup, after=cleanup, `yield x` -> `as x`
always   @wraps(func) on the wrapper ; return the result
```

**Where they show up:** `@app.get(...)` (FastAPI), `@pytest.fixture`, `@lru_cache(...)`, retries/backoff, login checks, plugin/provider registries — all this same idea.

**Sources:** [Real Python — Decorators primer](https://realpython.com/primer-on-python-decorators/) · [`functools.wraps`](https://docs.python.org/3/library/functools.html#functools.wraps) · [`contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) · Lessons: `D:\me\teach\lessons\0007–0009*.html` · Code: `D:\me\teach\postqueue\deco.py`
