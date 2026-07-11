## 1. Prefill VS Decode
For an LLM to write a sentence for you, it does two completely different things:

### Prefill: The Comprehension Phase
This is the phase where the model reads the **entire prompt** at once and understands it.

**Example:**
It's like an oral exam where the professor asks you a question, and you read the whole question carefully and focus on it before you start answering.

**Technically speaking:**
- The **KV Cache** is computed completely during this phase.
- Processing is **parallel** — the GPU works at full power.
- Prefill is very fast, and we prepare all the information the model will need later.

---
### Decode: The Generation (Writing) Phase
This is the phase where the model starts generating the answer **Token by Token**.

**How does it work?**
- It relies on the **KV Cache** that was built during Prefill.
- Processing is **sequential** — each time it generates only **one token**.
- The GPU does **not** utilize its full power because it is working on something very small (just one token).

**The Problem:**
As a result, this phase is **much slower** and is the reason why the response appears gradually (word by word).

> **Important:** The real bottleneck in LLMs is **Decode**, not Prefill.

---
## 2. KV Cache
In short, it is the secret that makes the LLM respond quickly, instead of rethinking your question from scratch every time you ask for a new word.

### Scenario: How KV Cache Works
Imagine you are reading a book and someone asks you: *"Who killed Joseph?"*

**Without KV Cache:**
You would close the book and go back to read from the first page again, gathering information in your head to answer "Who killed Joseph?" And if they asked for another word, you would close the book again and reread the whole thing from the beginning.

**This is called: Recomputation**
Unfortunately, this is exactly what happens with standard Transformers if you run them naively.

---
### What Changes With KV Cache?
While reading the book, you were taking notes on a separate piece of paper. That paper is the **Cache**.

**What do these notes contain?**
- **Keys:** Character names and their locations (the context).
- **Values:** Important events that happened (the meaning).

When you reach the last page, instead of rereading the book from the beginning, you look at your notes (Cache) and start answering immediately.

### How Does the LLM Do This?
We all know that the model converts text into numbers (Vectors). As soon as a word enters, it produces two things:

- **`K (Key)`**: The context of the word itself.
- **`V (Value)`**: The meaning it carries.

Instead of recalculating K and V for previous words every time new text comes in, the **KV Cache** stores them in the GPU's **VRAM**. When a new word arrives, we only calculate its own K and V and append them to the Cache.

---
## 3. Batching: Processing Multiple Requests
If 10 people came and asked you questions at the same time, what would you do?

Let's imagine a scenario:
### 1. Static Batching
A restaurant takes 10 orders and puts them all in the oven together. If one order takes a minute and the other 9 take a second, then **everyone** is forced to wait the full minute — the time of the slowest order.

### 2. Continuous Batching
Here is the difference: the order that takes a minute goes into the oven, and as soon as the other 9 finish, they are **removed immediately** from the oven, and new orders are placed in the empty spots. In short, in this case, the oven is running at maximum capacity and is not waiting for anything.

> **In summary:** This scenario helps us understand how batching works and why they preferred the second method over the first. The second method is the genius approach.