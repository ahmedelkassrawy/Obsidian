---
tags: [software-design, data-modeling, types, python, pydantic]
source: Track A · postqueue · Lesson 2
updated: 2026-08-17
---

# Data Modeling — Why a Class? Why an Enum?

> The whole strategy in one line: **make illegal states unrepresentable.** Every type choice shrinks the set of values a slot can hold — aim so only legal values remain, and a wrong one *can't be built*.

Companion to [[Pydantic]] (the *how*). This note is the *why/when* — the instinct behind reaching for a `class` or `Enum` in the first place.

---

## 1. The north star

When you design data you're secretly answering one question:

> **"What are all the values this thing could hold — and how many of them are wrong?"**

Good modeling drives the count of *wrong* values toward zero. Enums, classes, validators are all just tactics for that one strategy: **leave fewer ways to be wrong.**

Two named ideas underneath:
- **Make illegal states unrepresentable** (Scott Wlaschin, *Domain Modeling Made Functional*).
- **Parse, don't validate** (Alexis King) — turn raw input into a valid type at the boundary, so nothing downstream re-checks.

---

## 2. A type is a *set of allowed values*

Stop reading a type as "what kind of thing." Read it as **the set of values allowed in this slot.**

| Type for `platform` | Values it permits | How many are meaningful |
|---|---|---|
| `str` | infinite — `""`, `"instgram"`, `"MySpace"`, `"42"`… | 3 |
| `Platform` (Enum) | exactly 3 | 3 |

`str` = a slot permitting infinitely many values, almost all bugs. The `Enum` = a slot where *every* value it can hold is correct. Picking the type **is** shrinking the wrongness.

A `str` standing in for a concept with a fixed set of values is a smell with a name: **primitive obsession** / "stringly typed."

---

## 3. Enum = a dropdown, not a text box

> **If a UI designer would draw the field as a *dropdown*, it's an `Enum`. If a *free-text box*, it's a `str`.**

Condition for an enum: a **known, closed, finite** list of choices that rarely changes. Ask: *"Can I write every legal value on my fingers, and will the list rarely change?"* → yes = enum.

An enum buys three things a `str` can't:
- **Wrong values become impossible** — `"tiktok"` can't be assigned; rejected at the gate.
- **Right values become discoverable** — editor autocompletes `Platform.` — you never guess spelling.
- **One source of truth** — the set lives in one place; add once, everywhere sees it.

**Examples:** order status (`new/paid/shipped`), currency (`USD/EUR/GBP`), user role, HTTP method, log level. Not: email, username, comment, search query (open text → `str`).

---

## 4. Class = a noun that carries its own rules

An enum narrows **one** field. A class earns its place for a different reason: **several values that mean nothing apart and must obey rules together.**

A caption alone isn't schedulable. A time alone isn't. But *caption + platform + time + status* bundled **is** a `Post` — a noun in your domain. Two signals a class is being born:

- **Data clump** — the same 2–3 variables keep travelling together, arg after arg, function after function. That clump is begging for a name.
- **Homeless invariant** — a rule spanning fields ("caption length depends on platform", "a cancelled post can't have a future send time") with nowhere to live. A rule needs a home; that home is a model.

**The tell:** if you write `def schedule(caption, platform, when, status)` and then the same four params in `edit(...)` and `preview(...)` — stop. Those four are a `Post`. Name it once. Without the class, the "postness" (which fields belong together + what makes them valid) lives only in your head and gets re-checked or forgotten everywhere.

---

## 5. The payoff — validate once, trust everywhere ("parse, don't validate")

Two ways to handle risky input:

| | **Validate** (junior habit) | **Parse into a type** (senior habit) |
|---|---|---|
| What you do | `is_valid(data)` → `True/False`, carry raw data on | turn raw data into a `Post` at the boundary; if not a `Post`, it never gets in |
| Downstream code | must re-check or blindly trust — the boolean was forgotten | receives a `Post` and *knows* it's valid; the type is the proof |
| Where bugs surface | deep in business logic, hard to trace | at the front door, cheap |

A [[Pydantic]] model **is** a parser: `Post.model_validate(raw)` hands you something provably valid or raises at the gate. That's why a good model makes the rest of the code simple — every function after the gate gets to be dumb and trusting.

---

## 6. The reusable thinking tool — 4 questions

Run these in order on *any* new data (config, API payload, domain object):

| # | Ask | If yes |
|---|---|---|
| 1 | Several values travel together / a rule spans them? | make a **class** (name the noun) |
| 2 | A field's legal values = small fixed closed list? | make it an **Enum** |
| 2b | Open value but constrained (range, non-empty, format)? | primitive **+ validator** |
| 2c | Field is itself a compound thing? | **nest another model** |
| 3 | What must always be true once built? (invariants) | enforce at the **boundary** |
| 4 | **Can I still construct an *illegal* version?** | if yes → **tighten** until you can't |

**Question 4 is the senior move most people skip.** After drafting a model, actively try to build a nonsense instance. Every hole you find is a validator or tighter type you're missing.

---

## 7. Pick-the-type quick table

| The field is… | Use | Litmus |
|---|---|---|
| one of a known closed set | **Enum** | designer draws a *dropdown* |
| open-ended text/number, no rule | **str / int** | designer draws a *text box* |
| open but bounded/formatted | primitive **+ validator** | "any number, but 0–10" |
| a bundle of fields with rules | **class / model** | the parts mean nothing apart |
| a field that is itself a bundle | **nested model** | a `Post` holding an `Author` |

---

## 8. Three smells that say "model me"
- **Stringly typed / primitive obsession** — `str`/`int` standing in for a concept with a fixed value set → Enum or a small type.
- **Data clump** — same 2–3 variables passed together again and again → a class.
- **Homeless invariant** — a rule re-checked in many places or written only in comments → put it in one model's validator.

---

## 9. When NOT to model (restraint is senior too)

Modeling has a cost — every class/enum is a thing to read and maintain. Don't reach for one when none of the triggers is present:
- A **single** value, used once, **no rule**, **no fixed set** → a plain variable. A class here is ceremony.
- A truly open value (comment, search query) → leave it `str`. Forcing an enum on open text is the opposite mistake.

**Balance test, one line:** *Is there a rule, a fixed set, or a clump?* None of the three → don't model. Any → do.

---

## Quick reference

```
Strategy: make illegal states unrepresentable. A type = the set of values allowed in a slot.
Enum   -> field is one of a small fixed closed set          (dropdown, not text box)
str/int-> open-ended value, no rule                          (text box)
+valid.-> open but constrained (range / non-empty / format)
class  -> 2+ fields travel together AND/OR a rule spans them (a named noun)
nested -> a field that is itself a compound thing

Parse, don't validate: turn raw input into a valid type at the boundary; trust it after.
4 questions: clump/rule? -> closed set? -> constrained/compound? -> invariants? -> can I build an illegal one?
Don't model when: no rule, no fixed set, no clump.
```

**Sources:** [Parse, don't validate — King](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) · [Python translation](https://www.bitecode.dev/p/what-parse-dont-validate-means-in) · [Make illegal states unrepresentable — Stemmler](https://khalilstemmler.com/articles/typescript-domain-driven-design/make-illegal-states-unrepresentable/) · [Domain Modeling Made Functional — Wlaschin](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/) · [Primitive Obsession](https://refactoring.guru/smells/primitive-obsession) · Lesson HTML: `D:\me\teach\lessons\0004-modeling-illegal-states.html`
