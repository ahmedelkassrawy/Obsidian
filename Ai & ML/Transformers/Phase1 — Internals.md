---
tags: [ai-ml, transformers, attention, llm, kv-cache, rope, gqa, inference]
domain: ai-ml
type: lesson-note
status: digested
source: Transformers lesson (session 2026-09-18)
---
# Transformers — Phase 1 (the internals)

> Builds on [[Phase0]]. Five fixes, each for a specific problem the base architecture leaves open. Concepts only — no math.

## 1. Why ÷√d (scale the scores)
**Problem:** the wider each head is, the **bigger** the raw attention scores get. Big scores make softmax **spiky** — it dumps almost all the weight on a single token and ignores the rest. That kills the "blend from several tokens" behavior, and training barely moves.

**Fix:** shrink the scores before softmax by dividing them by a set factor (√d, the head width). That keeps the scores in a sane range no matter how wide the head is, so softmax stays **soft** and the token blends from several others.

```text
too-big scores → softmax picks ONE winner, ignores the rest   (bad)
scaled scores  → softmax spreads weight across several tokens  (good)
```

> [!tip] One line
> ÷√d keeps softmax soft as heads get wide, so attention blends instead of picking one winner.

## 2. GQA / MQA — fewer K/V heads to save memory
**Setup:** in normal multi-head attention (MHA), every head has its **own** Q, K, and V. Fine for compute — but the **K and V** of every past token must be **stored** during generation (the KV cache, below). With many heads, that storage explodes.

**The insight:** you need many *different questions* (Q heads) to catch different relationships — but you don't need as many *different answer-sources* (K/V heads). So keep all the Q heads, and **share** the K/V heads.

```text
MHA  (one K/V per Q):        GQA  (K/V shared per group):      MQA (one K/V for all):
 Q1 Q2 Q3 Q4                  Q1 Q2   Q3 Q4                     Q1 Q2 Q3 Q4
 │  │  │  │                    \ /     \ /                       \  \ /  /
 K1 K2 K3 K4                   K/V-a   K/V-b                      K/V (single)
 V1 V2 V3 V4                  (2 groups share)                  (all share one)
 4 Q, 4 KV sets               4 Q, 2 KV sets                    4 Q, 1 KV set
```

> [!definition] MHA / GQA / MQA
> **MHA** = one K/V per head (best quality, biggest cache). **MQA** = all Q heads share **one** K/V (tiny cache, small quality drop). **GQA** = the middle — Q heads split into groups, each group shares one K/V. Modern models (Llama, Mistral) use **GQA** — most of the memory savings, almost none of the quality loss.

**Why it matters:** the KV cache is the #1 memory hog at inference. GQA shrinks it several times over → longer context, bigger batches, cheaper serving. (Exactly the memory pressure you hit in your raaaaag/vLLM work.)

> [!tip] One line
> GQA = keep all the questions, share the answer-sources → smaller cache.

## 3. RoPE — how position is *really* injected
**Recap the naive approach:** in Phase 0, position was *added* to the embedding. That works but is weak — added position numbers can dominate, and the model only learns *absolute* positions ("slot 5"), not *relative* ones ("3 words apart"), which is what actually matters for language.

**The fix (RoPE = Rotary Position Embedding):** instead of *adding* position, **rotate** each token's Q and K vector by an amount set by its position.

```text
token at position 0 → no rotation
token at position 1 → rotate a little
token at position 2 → rotate twice as much
token at position 5 → rotate five times as much
```

**Why rotation is clever:** when attention compares two tokens, the result depends only on the **difference** in their rotations — i.e. **how far apart they are**, not their absolute slots. So relative position falls out *for free*.

```text
compare pos 2 vs pos 5    →  gap = 3  →  "3 apart"
compare pos 10 vs pos 13  →  gap = 3  →  ALSO "3 apart" (same relationship)
```

> [!definition] RoPE
> Encode position by **rotating** Q and K by an amount set by the token's position. Because the comparison then depends on the *rotation difference*, the model sees **relative** distance automatically. Applied only to Q and K (not V), and it handles long contexts better than added encodings — which is why nearly all modern LLMs use it.

**Why only Q and K, not V:** position should affect *who attends to whom* (the scores, which come from comparing Q and K), not *what information is carried* (V is the payload — it shouldn't be twisted by position).

> [!tip] One line
> RoPE rotates Q/K so attention feels the *distance between* words, not just their slot numbers.

## 4. KV cache — don't recompute the past
**Problem:** generation is autoregressive — one token at a time, feeding the output back in. Naively, to generate token 101 you'd re-run attention over all 100 previous tokens; for token 102, all 101; and so on. That re-computes the same K and V for old tokens **over and over** — huge waste.

**The key observation:** the K and V vectors of tokens 1–100 **never change** when you add token 101. So compute them once and **store** them.

```text
without cache (wasteful):
  step 101: recompute K,V for tokens 1..100  + new token   ✗ redo everything
  step 102: recompute K,V for tokens 1..101  + new token   ✗ again

with KV cache:
  step 101: K,V for 1..100 already stored → just compute token 101, append
  step 102: reuse 1..101 → compute only token 102
            ┌─────────── KV cache (grows by one row per step) ───────────┐
            │ K1 K2 K3 ... K100  [+K101]  [+K102] ...                     │
            │ V1 V2 V3 ... V100  [+V101]  [+V102] ...                     │
            └────────────────────────────────────────────────────────────┘
  new token's Q attends over the whole stored cache
```

> [!definition] KV cache
> Store every past token's K and V so each new token only computes its **own** K/V and attends over the stored rest. Turns per-step work from "redo all previous tokens" into "one new token." **Why cache K/V but not Q?** Old tokens' Q is never needed again — only the *current* token asks a question; but every old token is still a potential *answer*, so its K/V must stay.

> [!tip] One line
> KV cache stores past K/V so each new token is cheap — but the cache is what eats memory (hence GQA).

## 5. Memory-bound decode — why generation is slow
**The surprise:** during generation the GPU is mostly **idle** — not because there's too much math, but because it's **waiting on memory**.

**Why:** to generate **one** token, the GPU must read the **entire model's weights** plus the **whole KV cache** from memory — just to do a small amount of work on a single token. Moving all that data takes far longer than the work itself.

```text
per generated token:
  read ALL weights + KV cache from memory   ← slow (lots of bytes moved)
  do the work for ONE token                  ← fast (little compute)
  → bottleneck is MEMORY BANDWIDTH, not compute  ("memory-bound")
```

> [!definition] Memory-bound decode
> Generation is limited by **memory bandwidth** (moving weights + cache), not by compute. The GPU reads a huge model to produce one small token, so its math units sit mostly idle. (Contrast training/prefill, which processes many tokens at once and *is* compute-bound.)

**The fix — batching:** read the weights *once* and process **many** requests' tokens together, so that expensive read is shared across all of them. Same bytes moved, far more tokens produced → throughput jumps.

```text
1 request:   read weights → make 1 token    (the read is wasted on one token)
32 batched:  read weights → make 32 tokens   (same read, 32× the output)
```

This is exactly **continuous batching** in vLLM — the 1378 vs 28 tok/s number from your M2 work came from this.

> [!tip] One line
> Decode is memory-bound; batching shares the weight-read across many tokens → the big throughput win.

## The five internals in one table
| Internal | Problem | Fix |
|---|---|---|
| ÷√d | wide heads → spiky softmax | scale scores down |
| GQA/MQA | KV cache too big | share K/V across Q heads |
| RoPE | want relative position | rotate Q/K by position |
| KV cache | recomputing the past | store past K/V, reuse |
| memory-bound decode | GPU idle on generation | batch → share the weight read |

---

# KV cache vs GQA/MQA
They're related but do **different jobs**, and they work *together* — the pair people most often confuse.

## The one-line difference
- **KV cache** = a runtime **trick**: *store* past tokens' K and V so you don't recompute them. Saves **time**.
- **GQA/MQA** = a model **design**: use *fewer* K/V heads so there's *less to store*. Saves **memory** (shrinks the cache itself).

KV cache decides **whether** you keep past K/V. GQA/MQA decides **how big** each stored entry is.

## How they chain
```text
KV cache says:  "keep every past token's K and V so generation is cheap"
                        │
                        ▼  ← but now memory is the problem
                the cache grows with model depth, number of K/V heads, and tokens
                        │
                        ▼
GQA/MQA says:   "then use fewer K/V heads, so each stored entry is smaller"
```
So KV cache **creates** the memory pressure; GQA/MQA **relieves** it. You use both at once.

GQA/MQA works because, of all the things the cache grows with, the **number of K/V heads** is the one lever the model design can pull — fewer K/V heads, proportionally smaller cache:

```text
MHA:  many KV heads  → full cache     (baseline)
GQA:  few  KV heads  → cache several times smaller  (Llama-style, tiny quality loss)
MQA:  one  KV head   → cache smallest               (max saving, small quality loss)
```

## Side by side
| | KV cache | GQA / MQA |
|---|---|---|
| **What it is** | runtime technique | model architecture choice |
| **Problem it solves** | recomputing past tokens (speed) | cache too big (memory) |
| **When decided** | at inference, automatically | at model design/training time |
| **What it touches** | *whether* K/V are stored | *how many* K/V heads exist |
| **Without it** | generation is slow (redo the past) | cache blows up memory / limits context |

> [!tip] They're a team, not alternatives
> **KV cache** is *what you do* (keep past K/V). **GQA/MQA** is *how you make that affordable* (keep fewer K/V). Every modern LLM uses **both**: KV cache for speed, GQA to keep that cache small enough for long context and big batches.

**Why you can't swap one for the other:**
- KV cache with no GQA → fast, but the cache eats all your memory at long context.
- GQA with no KV cache → small footprint, but you'd still recompute the past every step → slow.
