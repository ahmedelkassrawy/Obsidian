---
description: "How LLM inference actually runs: the prefill vs decode phases, the KV cache that stops recomputation, paged attention that stops memory waste, static vs continuous batching, and the vLLM knobs you tune for throughput."
domain: ai-eng
type: concept
status: digested
tags:
  - domain/ai-eng
  - type/concept
  - status/digested
  - topic/llm
  - topic/llm-internals
  - topic/llm-serving-and-vllm
aliases:
  - "prefill vs decode"
  - "KV cache"
  - "paged attention"
  - "continuous batching"
  - "vLLM tuning"
hubs:
  - "[[LLM Internals]]"
  - "[[LLM Serving & vLLM]]"
---
# LLM Inference Internals

A model that feels lightning-fast for one user slows to a crawl for a hundred, and the GPU memory maxes out. The model isn't broken — the slowdown is about **how inference manages compute and memory** while generating tokens. Here's the whole chain, from the two phases up to the serving knobs.

---

## 1. Prefill vs Decode — the two phases

An LLM does two completely different things to write a sentence:

### Prefill — the comprehension phase
The model reads the **entire prompt at once** to understand it. Like an oral exam where you read the whole question carefully before you start answering.
- The **KV cache** is computed completely during this phase.
- Processing is **parallel** — the GPU works at full power.
- It needs a lot of **compute**, but it's fast. The slight delay before the first token appears is prefill happening.

### Decode — the generation phase
The model generates the answer **one token at a time**. Each new token has to reach back into context.
- It relies on the **KV cache** built during prefill.
- Processing is **sequential** — one token per step.
- The GPU does **not** use its full power (it's working on just one token), so it's dependent on **memory speed and space**.

> **The real bottleneck is Decode, not Prefill.** Decode is why the response appears gradually, word by word.

---

## 2. KV cache — stop redoing the attention maths

Every time the model generates a token, it computes a **Query** (what it's looking for), a **Key** (what context is available), and a **Value** (the meaning). Doing that maths from scratch for *every past token* every step is far too slow — that's **recomputation**, and it's what naive Transformers do.

### The book analogy
Imagine reading a book and being asked "Who killed Joseph?"
- **Without a cache:** you close the book and reread from page one every time you need the next word.
- **With a cache:** while reading, you take notes on a separate page. When you reach the end you answer from your notes instead of rereading.

Those notes are the cache:
- **Keys** = the context (character names, locations).
- **Values** = the meaning (important events).

### How the LLM does it
As each word enters, the model produces its `K` (context of the word) and `V` (meaning it carries). Instead of recalculating K and V for all previous words each step, the **KV cache stores them in GPU VRAM**. When a new token arrives, only its own K and V are computed and appended to the cache.

- **The catch:** this trades compute for memory. A 13B model takes ~65% of a standard GPU's memory just for its weights ("brain"), leaving only ~35% for the KV cache across all active users.

---

## 3. Paged attention — stop wasting GPU memory

Traditional systems waste much of that precious 35%. They reserve one **giant, continuous block** of memory per user, sized for the *maximum possible* answer length. If the answer is short, the rest sits empty and unusable by anyone else.

**Paged attention** (built into vLLM) copies how a normal OS manages RAM:
- The KV cache is broken into small **pages** (usually 16 tokens each).
- Pages don't have to sit next to each other — they're mapped and grabbed on demand.
- **Result:** almost no wasted space, so far more users fit on the same GPU.

---

## 4. Batching — serving many requests at once

If 10 people ask questions at the same moment, how do you run them together?

### Static batching
A restaurant puts all 10 orders in the oven together. If one order takes a minute and the other nine take a second, **everyone** waits the full minute — the time of the slowest request in the batch.

### Continuous batching
The slow order stays in; as soon as each of the other nine finishes, it's **removed immediately** and a new request drops into the empty slot. The oven runs at maximum capacity and never waits. This is the genius approach and why vLLM-style servers prefer it over static batching.

---

## 5. vLLM tuning knobs

Four settings (plus one bonus) to squeeze the most out of the hardware:

1. **GPU memory utilization** — how much leftover memory goes to the KV cache. Default ~90% (`0.9`). Stable workload → push to `0.95` for more users. Crashing on memory spikes → pull back to `0.80`.
2. **Prefix caching** — if many users send the same system prompt, save its maths **once** and let everyone point at it instead of recomputing it 100 times. Big win for chatbots and coding assistants.
3. **Chunked prefill** — normally a huge new prompt pauses everyone's decoding (prefill takes priority). Chunked prefill splits that prompt into smaller bites and mixes them into ongoing decode work, so no one stutters.
4. **Speculative decoding (bonus)** — run a tiny fast "draft" model alongside the main model. The draft rapidly guesses the next few tokens while the main model rests between memory reads; the main model then verifies the guesses in one quick sweep.
