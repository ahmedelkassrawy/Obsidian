---
description: "How attention actually computes, and the four tricks that make real LLMs run: √d scaling, GQA/MQA, RoPE, KV cache — plus why decode is memory-bound."
type: note
domain: ml
tags:
  - topic/transformers
  - topic/llm-internals
  - type/lesson
grok_scope: M
grok_status: captured
rebuild_solo: 0%
---
# Transformer Internals

> [!info] What this note is
> The **implementation layer** under the concepts you already have in [[Transformers]] and [[Self-Attention vs Cross-Attention]]. Goal: understand these well enough to **write them from an empty file**. Every section ends with a *defend-solo* check. Part of [[LLM Internals]].

> [!note] Where you're starting (2026-09-15)
> You already own the *what* and *why*: Q/K/V, self vs cross attention, multi-head, positional encoding, encoder vs decoder. This note fills the five gaps that separate "I can explain a transformer" from "I can build one that runs fast": **√d scaling, MHA→GQA/MQA, RoPE, KV cache, memory-bound decode.**

---

## 1. Attention math — the one equation

Self-attention turns a sequence of token vectors into a new sequence where each token has "looked at" every other token and pulled in what's relevant.

Three learned projections turn each token vector `x` into:
- **Query (Q)** — "what am I looking for?"
- **Key (K)** — "what do I offer as a match target?"
- **Value (V)** — "what do I actually hand over if matched?"

The whole operation:

$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Read it left to right:

1. `Q @ Kᵀ` → a `(seq × seq)` **score matrix**. Entry `(i,j)` = how much token `i`'s query matches token `j`'s key (a dot product).
2. Divide by `√d_k` → the scaling fix (Section 2).
3. `softmax` over each row → each row becomes weights that sum to 1: "how much of my attention goes to each other token."
4. `@ V` → each token's output is a weighted average of all the value vectors.

From-scratch (teaching sketch, PyTorch):

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q, k, v, mask=None):
    # q, k, v: (batch, heads, seq, d_head)
    d_head = q.size(-1)
    scores = (q @ k.transpose(-2, -1)) / (d_head ** 0.5)   # (b, h, sq, sk)
    if mask is not None:                                   # causal or padding mask
        scores = scores.masked_fill(mask, float("-inf"))
    attn = scores.softmax(dim=-1)                          # weights sum to 1 per row
    return attn @ v                                        # (b, h, sq, d_head)
```

The **causal mask** (for a decoder) sets scores above the diagonal to `-inf` so a token can't attend to future tokens — after softmax those become 0.

> [!question] Defend solo
> Without looking: write the attention equation, and say in one sentence what each of the three matmuls (`QKᵀ`, `softmax`, `·V`) produces and its shape.

---

## 2. Why divide by √d_k

**Fact.** Suppose each component of `q` and `k` is independent with mean 0 and variance 1. Their dot product `q·k = Σᵢ qᵢkᵢ` is a sum of `d_k` independent terms, each with mean 0 and variance 1. So:

- `mean(q·k) = 0`
- `Var(q·k) = d_k`  →  **standard deviation = √d_k**

So as the head dimension `d_k` grows, the raw scores spread out over a range that grows like `√d_k`.

**Why that's bad.** Feed large-magnitude numbers into softmax and it **saturates**: one entry goes to ≈1, the rest to ≈0 (nearly one-hot). In that saturated region the softmax gradient is almost zero → **vanishing gradients**, the model can't learn.

**The fix.** Divide scores by `√d_k`. That rescales the variance back to ≈1 regardless of `d_k`, keeping softmax in its responsive range.

```python
# d_k = 64  → raw scores have std ~8   → softmax too peaky
# after /√64 = /8 → std ~1             → healthy softmax
```

> [!tip] The intuition in one line
> `√d_k` cancels the standard deviation that the dot-product picks up from summing `d_k` terms, so softmax sees numbers of a sane size no matter how wide the head is.

> [!question] Defend solo
> Why `√d_k` and not `d_k` or `d_k²`? (Answer: you're normalizing the *standard deviation*, which scales as √d_k, not the variance.)

---

## 3. Multi-head → GQA → MQA

### Multi-Head Attention (MHA)
Instead of one big attention over `d_model` dims, split into `h` **heads** each of size `d_head = d_model / h`. Run attention independently per head, concatenate, then one output projection `W_O`.

Why: each head can specialize — one tracks syntax, another tracks a subject–verb link, etc. Cheap because total work is the same (`h × d_head = d_model`).

```python
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.wq = nn.Linear(d_model, d_model, bias=False)
        self.wk = nn.Linear(d_model, d_model, bias=False)
        self.wv = nn.Linear(d_model, d_model, bias=False)
        self.wo = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, mask=None):
        b, t, _ = x.shape
        # (b, t, d_model) -> (b, n_heads, t, d_head)
        q = self.wq(x).view(b, t, self.n_heads, self.d_head).transpose(1, 2)
        k = self.wk(x).view(b, t, self.n_heads, self.d_head).transpose(1, 2)
        v = self.wv(x).view(b, t, self.n_heads, self.d_head).transpose(1, 2)
        out = scaled_dot_product_attention(q, k, v, mask)   # (b, h, t, d_head)
        out = out.transpose(1, 2).reshape(b, t, -1)         # concat heads
        return self.wo(out)
```

### The problem MHA creates at inference
Each of the `h` heads has its **own** K and V. During generation you cache all past K and V (Section 5). With MHA that cache is `h` copies wide — huge memory and bandwidth cost.

### GQA and MQA — shrink the K/V side
Keep `h` **query** heads, but use **fewer K/V heads**:

| Variant | Query heads | K/V heads | KV cache size | Used by |
|---|---|---|---|---|
| **MHA** (Multi-Head) | h | h | 1× (biggest) | original Transformer, GPT-2, BERT |
| **GQA** (Grouped-Query) | h | g (1 < g < h) | h/g smaller | Llama 2 70B, Llama 3, Mistral |
| **MQA** (Multi-Query) | h | 1 | h× smaller | PaLM, Falcon |

- **MQA**: all query heads share **one** K and **one** V. Smallest cache, fastest decode, some quality loss.
- **GQA**: the middle ground. Split `h` query heads into `g` groups; each group shares one K/V head. `g = h` is plain MHA, `g = 1` is MQA. This is the modern default.

Implementation is MHA with narrower K/V projections, then repeat each K/V head across its group:

```python
# n_heads=32, n_kv_heads=8  -> GQA with 4 query heads per K/V head
self.wk = nn.Linear(d_model, n_kv_heads * self.d_head, bias=False)
self.wv = nn.Linear(d_model, n_kv_heads * self.d_head, bias=False)
...
rep = self.n_heads // self.n_kv_heads
k = k.repeat_interleave(rep, dim=1)   # (b, n_kv_heads, t, d) -> (b, n_heads, t, d)
v = v.repeat_interleave(rep, dim=1)
# now shapes match the query heads; run attention as normal
```

> [!important] Why this matters (ties to Section 6)
> GQA/MQA exist almost entirely to shrink the **KV cache**, because decode speed is limited by memory bandwidth, not compute. Fewer K/V heads = fewer bytes to read per generated token = faster generation.

> [!question] Defend solo
> A 32-query-head model uses GQA with 8 K/V heads. By what factor is its KV cache smaller than the MHA version? (Answer: 32/8 = 4×.)

---

## 4. RoPE — Rotary Position Embedding

The problem: attention as written is **order-blind** — shuffle the tokens and the math gives the same answer. You must inject position. Older models *added* a positional vector to the embedding. Modern models (Llama, Mistral, Qwen) use **RoPE**, which *rotates* Q and K instead.

### The idea
Chop each head's vector into 2D pairs `(x₀,x₁), (x₂,x₃), …`. For a token at position `m`, rotate pair `i` by angle `m · θᵢ`:

$$\begin{bmatrix} x'_{2i} \\ x'_{2i+1} \end{bmatrix} = \begin{bmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{bmatrix}\begin{bmatrix} x_{2i} \\ x_{2i+1} \end{bmatrix}, \qquad \theta_i = \text{base}^{-2i/d}$$

`base` is usually 10000. Low-`i` pairs rotate fast (fine position), high-`i` pairs rotate slowly (coarse position) — like the hands of many clocks at different speeds.

### The property that makes it work
After rotating query at position `m` and key at position `n`, their dot product depends **only on the relative distance `m − n`**, never the absolute positions:

$$\langle R_m q,\; R_n k\rangle = \langle q,\; R_{n-m}\, k\rangle$$

So RoPE gives you **relative** position information (what actually matters for language) while being applied with each token's **absolute** position. No learned parameters, and it extends to longer contexts (linear/NTK scaling).

Applied to **Q and K only**, before the score matmul. **Not to V** — V carries content, not position.

```python
def build_rope(seq_len, d_head, base=10000.0):
    theta = base ** (-torch.arange(0, d_head, 2).float() / d_head)  # (d_head/2,)
    pos = torch.arange(seq_len).float()                             # (seq,)
    angles = torch.outer(pos, theta)                                # (seq, d_head/2)
    return angles.cos(), angles.sin()

def apply_rope(x, cos, sin):
    # x: (b, heads, seq, d_head)
    x1, x2 = x[..., 0::2], x[..., 1::2]          # even / odd dims
    cos, sin = cos[None, None], sin[None, None]  # broadcast over batch & heads
    out = torch.empty_like(x)
    out[..., 0::2] = x1 * cos - x2 * sin
    out[..., 1::2] = x1 * sin + x2 * cos
    return out

# in forward(): q = apply_rope(q, cos, sin); k = apply_rope(k, cos, sin)
```

> [!question] Defend solo
> Two questions: (1) Why rotate Q and K but not V? (2) What single property makes RoPE behave as a *relative* position encoding even though you feed it *absolute* positions?

---

## 5. KV cache — why generation isn't O(n²) per step

**The setup.** A decoder generates one token at a time. To produce token `t`, its query must attend to the keys and values of **all** tokens `0..t`. Naively you'd recompute K and V for the entire sequence every single step — pure waste, since the past tokens' K and V never change.

**The fix.** Cache K and V for every past token. Each step you:
1. Compute K, V for **only the new token**.
2. Append them to the cache.
3. Let the new query attend to the whole cached K/V.

```python
# decode loop (one layer, sketch)
k_cache, v_cache = [], []
for token in generated_stream:
    q = wq(token)                       # (b, h, 1, d_head)  -- just this token
    k = wk(token); v = wv(token)
    k_cache.append(k); v_cache.append(v)
    K = torch.cat(k_cache, dim=2)       # all keys so far  (b, h, t, d_head)
    V = torch.cat(v_cache, dim=2)
    out = scaled_dot_product_attention(q, K, V)   # 1 query vs t keys
```

This turns per-step cost from recomputing everything into **one matrix–vector step** plus a growing read of the cache.

**The cost.** Cache size grows linearly with sequence length:

```
kv_bytes = 2 * n_layers * n_kv_heads * d_head * seq_len * batch * bytes_per_elem
           ^K and V
```

For a long context this is gigabytes — and it must be read from GPU memory on **every** token. That's the direct link to GQA/MQA (fewer `n_kv_heads`) and to the next section.

> [!question] Defend solo
> Why is the KV cache only for K and V, not Q? (Answer: a past token's Q is never needed again — only the *current* token queries. But past K/V are matched against every future query, so they're reused.)

---

## 6. Why decode is memory-bound

The single most important performance fact about serving LLMs.

**Two phases:**

| Phase | What happens | Shape of the matmuls | Bottleneck |
|---|---|---|---|
| **Prefill** | Process the whole prompt at once | matrix × matrix (many tokens) | **Compute-bound** (FLOPs) |
| **Decode** | Generate one token per step | matrix × **vector** (1 token) | **Memory-bound** (bandwidth) |

**The mechanism.** Every decode step, to produce **one** token, the GPU must read the **entire model's weights** (plus the whole KV cache) from HBM (high-bandwidth memory) into the compute cores — then does only a tiny amount of arithmetic on them (one token's worth). The ratio

$$\text{arithmetic intensity} = \frac{\text{FLOPs done}}{\text{bytes read}}$$

is **low** during decode. When intensity is low you sit on the memory-bound side of the *roofline*: the compute units are starving, waiting on memory. So generation speed is set by **how fast you can stream weights + KV from memory**, not by how many FLOPs the GPU can do.

**What follows from this (and why it's worth knowing):**
- **Batching** helps a lot — read the weights once, reuse them across many sequences' tokens. Raises intensity, raises throughput.
- **KV cache size directly costs speed** — every step re-reads it. → GQA/MQA (Section 3) shrink it.
- **Quantizing weights** (fewer bytes each) speeds decode because there's less to read.
- Prefill is different — it's compute-bound, so the same tricks don't move it much.

> [!question] Defend solo
> Explain in plain words why generating token #500 reads the whole model from memory to compute just one token — and why batching many requests together fixes the waste.

---

## Excel Gate — grokked when…

**Open a blank file and, with no AI, write a runnable single-head → multi-head → GQA attention block with RoPE and a KV-cache decode loop — then explain out loud, for each of the five topics, the *why* (not just the code):**

1. Where `√d_k` comes from and what breaks without it.
2. How GQA differs from MHA and MQA, and the exact cache-shrink factor for given head counts.
3. The one property that makes RoPE a *relative* encoding, and why V is untouched.
4. Why the KV cache stores K/V but never Q.
5. Why decode is memory-bound and prefill isn't — in terms of arithmetic intensity.

Pass = all five explained cold + the code runs on a toy input. That's `rebuild_solo: 100%`.

---

## Next layer (the L-domain tail)
When this note is grokked, promote toward "full transformer from scratch": FFN/SwiGLU, residual stream + RMSNorm, the full decoder block, tokenizer → embedding → logits, sampling, then training loop. Ties to [[Transformers]], [[Stanford CS224n]], and your [[LLM Internals]] hub.

## Progress log
- 2026-09-15 — captured. Note written covering all five Week-1 topics with math + from-scratch code + defend-solo checks. `rebuild_solo: 0%` (parked behind System Design per WIP cap).
