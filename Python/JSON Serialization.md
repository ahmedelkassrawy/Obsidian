---
tags: [python, json, serialization, pydantic, files]
source: Track A · postqueue · Lesson 4 (saving & loading)
updated: 2026-08-17
---

# JSON & Serialization — object ⇄ text

> The one thing to hold: **a file can only hold text.** Your objects live in memory. So **saving = object → text**, **loading = text → object**. Everything below is just the tools for those two arrows.

Companion to [[Pydantic]] (the model whose `.model_dump` / `.model_validate` do the object↔dict half).

The fancy words: object → text is **serialize**; text → object is **deserialize**.

---

## The round trip

A `Post` doesn't go straight to text — it passes through a plain **dict** in the middle:

```
SAVE :  Post object  ->  dict  ->  JSON text  ->  file
LOAD :  Post object  <-  dict  <-  JSON text  <-  file
```

| Arrow                   | Tool                                | From          |
| ----------------------- | ----------------------------------- | ------------- |
| Post → dict             | `post.model_dump(mode="json")`      | Pydantic      |
| dict → JSON text → file | `json.dump(x, f)`                   | `json` module |
| file → JSON text → dict | `json.loads(text)` / `json.load(f)` | `json` module |
| dict → Post             | `Post.model_validate(d)`            | Pydantic      |

---

## What the transformation looks like (real output)

```python
p = Post(id=1, platform=Platform.x, caption="hi", scheduled_at=datetime(2027,1,1,10,0))

p.model_dump()
# {'id': 1, 'platform': <Platform.x: 'X'>, 'scheduled_at': datetime.datetime(2027,1,1,10,0), ...}
#  ^ a dict, but scheduled_at is STILL a datetime object -> json can't write that

p.model_dump(mode="json")
# {'id': 1, 'platform': 'X', 'scheduled_at': '2027-01-01T10:00:00', 'status': 'pending'}
#  ^ JSON-friendly values: datetime is now a STRING

json.dumps([p.model_dump(mode="json")])
# '[{"id": 1, "platform": "X", "scheduled_at": "2027-01-01T10:00:00", ...}]'
#  ^ one big TEXT string, ready for a file
```

**Why `mode="json"`?** Plain `model_dump()` leaves values as real Python objects (a `datetime`, an `Enum`). `json` only understands text-friendly values (str/int/float/bool/list/dict/None). `mode="json"` converts them — `datetime` → ISO string — so `json.dump` can handle it.

---

## `dump` vs `dumps` (and `load` vs `loads`)

The **`s` = string**.

| Call | Direction | Talks to |
|---|---|---|
| `json.dump(x, f)` | object → text | a **file** `f` |
| `json.dumps(x)` | object → text | returns a **string** |
| `json.load(f)` | text → object | a **file** `f` |
| `json.loads(text)` | text → object | a **string** |

`json.dumps`/`loads` (string) are handy for APIs and quick tests; `json.dump`/`load` (file) for writing/reading files directly.

---

## The file bits

```python
if not self.path.exists():          # first run: no file yet -> reading would crash
    return []

with self.path.open("w", encoding="utf-8") as f:   # 'w' = write (replaces file)
    json.dump(posts, f)
# the `with` AUTO-CLOSES the file when the block ends, even on error
```

- `path.exists()` — guard before reading a file that may not be there yet.
- `with open(...) as f:` — opens **and** guarantees close. Forgetting to close is a classic bug; `with` removes it.
- `'w'` write (replaces whole file) · `'r'` read · `'a'` append.
- `path.read_text()` / `path.write_text(s)` — open+read/write+close in one call (even less to get wrong).
- Pass `encoding="utf-8"` so non-ASCII (emojis, Arabic) round-trips correctly.

---

## List comprehension — `[f(x) for x in things]`

A short way to build a new list by doing something to each item. These are identical:

```python
# long
out = []
for p in posts:
    out.append(p.model_dump(mode="json"))

# short
out = [p.model_dump(mode="json") for p in posts]
```

Read left-to-right: *"a list of `p.model_dump(...)` for each `p` in `posts`."* Same for loading: `[Post.model_validate(d) for d in raw]`.

---

## GOTCHA: object vs dict — dots vs brackets

Once `_read` rebuilds real `Post`s (via `model_validate`), treat items as **objects**:

```python
post.id          # ✓ object -> dot
post["id"]       # ✗ that's dict syntax; mypy: "Post is not indexable"
```

Keep the **text↔object boundary in ONE place**: turn dicts into Posts inside `_read`, turn Posts into dicts inside `_write`. Then every other method only ever handles real `Post`s (dots, never brackets), and never has to re-validate.

---

## Worked example — the JsonStore round trip

```python
import json
from pathlib import Path
from models import Post

class JsonStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _read(self) -> list[Post]:                 # text -> objects (one place)
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text())
        return [Post.model_validate(d) for d in raw]

    def _write(self, posts: list[Post]) -> None:   # objects -> text (one place)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([p.model_dump(mode="json") for p in posts], f)

    def save(self, post: Post) -> None:
        posts = self._read()
        posts.append(post)
        self._write(posts)

    def get(self, id: int) -> Post | None:
        for post in self._read():
            if post.id == id:                      # dot, not post["id"]
                return post
        return None

    def list(self) -> list[Post]:
        return self._read()

    def delete(self, id: int) -> None:
        self._write([p for p in self._read() if p.id != id])
```

---

## Quick reference

```
file holds only TEXT -> save = object->text, load = text->object
Post <-> dict   :  model_dump(mode="json")  /  model_validate(d)
dict <-> text   :  json.dump(x,f)/json.dumps(x)  /  json.load(f)/json.loads(s)
s = string      :  dumps/loads use strings; dump/load use files
files           :  with open(...,'w',encoding='utf-8') as f  (auto-closes) ; check .exists() first
comprehension   :  [f(x) for x in things]  == a for-loop that appends
gotcha          :  real Post -> use post.id (dot), not post["id"] (bracket)
boundary        :  serialize in _write, deserialize in _read — one place each
```

**Track B bridge:** JavaScript does the same two steps — `JSON.stringify(x)` (object→text) and `JSON.parse(text)` (text→object). Same idea, different names.

**Sources:** [Python `json`](https://docs.python.org/3/library/json.html) · [Pydantic serialization](https://docs.pydantic.dev/latest/concepts/serialization/) · Lesson: `D:\me\teach\lessons\0006-json-save-load.html` · Code: `D:\me\teach\postqueue\storage.py`
