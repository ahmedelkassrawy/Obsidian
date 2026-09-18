---
tags: [ai-ml, transformers, attention, llm, foundations]
domain: ai-ml
type: lesson-note
status: digested
source: Transformers lesson (session 2026-09-18) + "Attention is all you need" walkthrough
---
# Transformers — Phase 0 (foundations)

> The internals (÷√d, GQA/MQA, RoPE, KV cache, memory-bound decode) live in [[Phase1 — Internals]].

> One line: a transformer turns words into meaning-vectors, lets them **look at each other** (attention) so each becomes context-aware, then predicts the next word — and repeats.

The whole pipeline at a glance:
```text
text → tokens → embeddings → [+ position]
     → ATTENTION (tokens mix) → ADD&NORM → FEED-FORWARD → ADD&NORM   ┐
                                                                     │ ×N blocks
     ← output of one block feeds the next ─────────────────────────┘
     → final linear + softmax → next token → append → repeat
```
Each stage below ends with a **Checkpoint**: what we have, what we still need, and why the next layer exists. The "what's still missing" is what forces the next piece.

## Why transformers exist (what RNN/LSTM couldn't do)
Before transformers, sequences were read one word at a time. Three problems killed that approach:

- **No parallelism.** An RNN reads word 2 only after word 1, word 3 only after word 2. A GPU has thousands of cores meant to work at once — sequential reading wastes almost all of them, so training is slow.
- **Long-range memory fades.** Information from an early word has to survive being passed through every step to reach a late word. Over long sentences it decays (the vanishing-gradient problem). LSTMs helped but still struggle when sequences get long.
- **Information bottleneck.** The old encoder–decoder squeezed the *entire* input into one fixed-size vector. The longer the input, the more gets lost through that one narrow pipe.

```text
RNN (sequential):   w1 → w2 → w3 → w4     each waits for the previous
Transformer:        w1 ─┐
                    w2 ─┼─ all attend to all, in ONE parallel step
                    w3 ─┤
                    w4 ─┘
```

> [!abstract] Checkpoint
> - **Have:** the task — read a sequence, predict the next token.
> - **Need:** something parallel, that links far-apart words directly, with no single bottleneck.
> - **Why the next parts exist:** attention gives all three — every word reaches every other in one parallel step.

## 1. Text → tokens
A model can't read letters, only numbers. So text is first **tokenized** — chopped into small pieces (a word or word-piece), each mapped to an integer ID from a fixed vocabulary. One token is not always a full word; rare words split into pieces.

```text
"I love RAG"
   │  tokenizer splits into pieces
   ▼
["I"] [" love"] [" R"] ["AG"]
   │  each piece → its vocab ID
   ▼
[ 40 ] [ 1842 ] [ 431 ] [ 6438 ]
```

> [!definition] Token
> The smallest unit of text the model reads — an integer ID from the vocab (~50k–100k entries). "RAG" here splits into "R" + "AG".

> [!abstract] Checkpoint
> - **Have:** the sentence as a list of integer IDs.
> - **Need:** numbers that carry *meaning* — an ID like `431` is just a name, it says nothing about what the word means.
> - **Why the next layer exists:** embeddings turn each ID into a meaning-vector.

## 2. Token → embedding (a vector)
Each ID is looked up in a big learned table and replaced by a **vector** — a list of numbers (say 1536) that places the word's *meaning* as a point in space. Words with similar meaning end up near each other. The model **learns** these numbers during training; nobody sets them by hand.

```text
ID 40   →  [ 0.2, -1.1,  0.7,  0.9, ... ]   1536 numbers
ID 1842 →  [-0.4,  0.8,  0.1, -0.2, ... ]
ID 431  →  [ 0.6,  0.3, -0.9,  0.5, ... ]
ID 6438 →  [ 0.1, -0.7,  0.4,  0.8, ... ]

stacked = the sentence as a grid:

              1536 columns (meaning)
            ┌───────────────────────────┐
     I      │ 0.2  -1.1  0.7  0.9  ...   │
     love   │-0.4   0.8  0.1 -0.2  ...   │  4 rows
     R      │ 0.6   0.3 -0.9  0.5  ...   │  (one per token)
     AG     │ 0.1  -0.7  0.4  0.8  ...   │
            └───────────────────────────┘
```

Why not the simple approach (**one-hot**: a 1 at the word's index, 0 everywhere else)? Two killers: it's huge and mostly zeros (a 50k-long vector per word), and every word is *equally far* from every other — "king" is as unrelated to "queen" as to "cat". Embeddings are dense and actually encode relationships.

> [!definition] Embedding
> A learned vector encoding a token's meaning. `d_model` = its length (1536 here). After this step the sentence is a **matrix**: `[tokens × d_model]`.

> [!abstract] Checkpoint
> - **Have:** each token as a meaning-vector; a `4 × 1536` grid.
> - **Need:** the vector to change with *context* — "bank" is one fixed vector today, but means different things in "river bank" vs "money bank" (a **static** embedding).
> - **Why the next layer exists:** attention makes the vector context-aware — but first it needs to know word order.

## 3. `+` position info
Attention (next) looks at all tokens **at the same time**, so on its own it has no idea of order — "dog bites man" and "man bites dog" would look identical. Fix: add **position information** to each token's vector so order is baked in before attention runs.

```text
                meaning            position          goes into attention
     dog  →  [meaning of dog]  +  [pos 0]  =  [dog-here-at-0]
     bites →  [meaning ...   ]  +  [pos 1]  =  [bites-at-1]
     man  →  [meaning ...   ]  +  [pos 2]  =  [man-at-2]

same word, different slot → different final vector → order is preserved
```

> [!definition] Positional encoding
> Extra numbers added to each token's vector encoding *where* it sits. Without it a transformer is order-blind. (The modern version is RoPE — see the internals below.)

> [!abstract] Checkpoint
> - **Have:** meaning + order in every vector; still a `4 × 1536` grid.
> - **Need:** tokens to actually **share** information with each other.
> - **Why the next layer exists:** that sharing is attention.

## 4. Attention — the core
This is the whole invention. Each token's vector is **rewritten** by pulling in information from the tokens that matter to it. For one word:

1. it asks *"which other words are relevant to me?"*
2. it scores every other word for relevance,
3. it rebuilds itself as a **weighted blend** — more from relevant words, less from the rest.

```text
"river bank" — rebuilding the "bank" vector:

   bank looks at →  river   the   bank
   relevance     →   0.7    0.1   0.2
                      │      │     │
   new bank = 0.7·river + 0.1·the + 0.2·bank
            → shifts toward the WATER meaning
```

![[Pasted image 20260917204215.png]]

![[Pasted image 20260917204710.png]]

**Q, K, V — why three copies.** A single token has to play three different jobs at once, and one vector can't do all three well. So we multiply its embedding by three **learned** matrices (Wq, Wk, Wv) to get three specialized views:

```text
                   ┌── × Wq → Q  "what am I looking for?"   (the question)
 token vector ─────┼── × Wk → K  "what do I offer?"         (the label)
                   └── × Wv → V  "what do I pass on?"       (the payload)
```

Library analogy: you have a **search request** (Q). Every book has a **spine label** (K). You match your request against the labels, and from the best matches you take the **book's contents** (V). You'd never make the request and the contents the same object — that's why Q, K, V are separate.

How they combine into the blend:
```text
Q · Kᵀ           → scores  (how much each token matches each other)
  │ ÷ √d, softmax → weights (each row sums to 1)
  ▼
weights × V      → new context-mixed vectors (same 4 × 1536 shape)
```

> [!definition] Q, K, V
> Three learned projections of the same token vector — request, label, payload. Attention matches Q against K to decide how much of each V to take. Because Wq/Wk/Wv are learned, the model discovers what makes a good question, label, and payload.

> [!note] The scores get scaled
> Before softmax, scores are divided by √d to stop them blowing up as vectors get long — otherwise attention collapses onto a single word instead of blending. (The full reason is in the internals below.)

> [!abstract] Checkpoint
> - **Have:** context-aware vectors — each token has absorbed the ones it attended to. Still `4 × 1536`.
> - **Need:** to catch **several kinds** of relationship at once (grammar, reference, nearby words) — one attention pattern is a blur.
> - **Why the next layer exists:** multi-head runs attention many times in parallel.

## 5. Multi-head — and what a "head" is
One attention pass can only learn **one** kind of relevance. Language has many at once ("who does this pronoun refer to?", "what's the subject?", "which words modify me?"). So we run several attention passes in parallel — each is a **head**.

```text
       token vector (1536)
   ┌────────┬────────┬─────── … ──────┐   split into H slices
 slice1   slice2   slice3          sliceH   (e.g. 12 × 128)
   │        │        │                │
 head1    head2    head3    …       headH    each does FULL attention
   │        │        │                │      on its own slice, own Q/K/V
   └────────┴────────┴─────── … ──────┘
                   │  concat back to 1536
                   ▼
              × Wo (mix)  →  output (4 × 1536)
```

> [!definition] Head
> One complete attention computation with its **own** Q/K/V, running on a **slice** of each token's vector.

Why slice instead of 12 full copies:
- **Cost stays flat** — 12 heads × 128 = 1536, the same total work as one big head. Twelve specialists for the price of one generalist.
- **Specialization** — one head tracks grammar, another tracks pronoun reference, etc. The model decides what each learns.

> [!abstract] Checkpoint
> - **Have:** rich context from many relationship types, back to a `4 × 1536` grid.
> - **Need:** to keep training stable across a deep stack, and to *transform* (not just move) the gathered info.
> - **Why the next parts exist:** Add & Norm stabilize; feed-forward digests.

## 6. The block — 4 steps, repeated ×N
Every transformer block runs the same four steps in order:

```text
        input (4 × 1536)
          │
   ┌──────▼──────────────┐
   │ 1. Multi-head attn  │  tokens SHARE context
   └──────┬──────────────┘
   ┌──────▼──────────────┐
   │ 2. Add & Norm       │  + input (residual), then normalize
   └──────┬──────────────┘
   ┌──────▼──────────────┐
   │ 3. Feed-forward     │  each token DIGESTS alone
   └──────┬──────────────┘
   ┌──────▼──────────────┐
   │ 4. Add & Norm       │  + input again, normalize
   └──────┬──────────────┘
          ▼  output → becomes the next block's input   (×N)
```

- **Step 1 — Multi-head attention:** tokens talk to each other (share context). Everything above happens here.
- **Step 2 — Add & Norm:** *Add (residual)* = add the block's input back to its output, so nothing important is lost and gradients flow through deep stacks. *Norm* = rescale each vector to a healthy range.
- **Step 3 — Feed-forward:** each token is processed **alone** (a small 2-layer net per row). Attention *moves* info between tokens; the feed-forward *transforms* it inside each token. A lot of the model's learned facts live here.
- **Step 4 — Add & Norm again:** same residual + normalize around the feed-forward.

The block repeats **×N** (the original paper used 6; GPT-3 used 96). Early layers catch simple patterns; later layers build abstract meaning.

> [!definition] Residual + LayerNorm
> **Residual** = output + input (protects the signal, lets gradients flow through deep networks). **LayerNorm** = normalize each vector to a stable range. Together = what makes stacking N layers trainable.

> [!abstract] Checkpoint
> - **Have:** after N blocks, deeply context-aware vectors.
> - **Need:** turn the final vector into an actual next-word choice.
> - **Why the next layer exists:** the final linear + softmax does that.

## 7. Predict the next token
The last block's vector for the final position is turned into a **probability over the whole vocabulary**.

```text
final vector ── linear + softmax ──▶  " you" 12%
                                       " it"   9%
                                       " RAG"  3%
                                        ...
                          pick one → append → run the whole pipeline again
```

This one-word-at-a-time loop is **autoregressive generation** — and it's why generation is slower than training (the KV cache in the internals exists to speed this up).

## 8. Encoder / decoder (the original architecture)
The original transformer had two halves. Modern LLMs (GPT, Llama) are usually **decoder-only**, but both are worth knowing.

```text
   INPUT ─▶ ENCODER (reads all at once) ─┐
                                         │ K,V
   OUTPUT so far ─▶ DECODER ─────────────┘
        (masked self-attn → cross-attn → FFN) ─▶ next token
```

- **Encoder** — reads the whole input in parallel; every token attends to every other.
- **Decoder** — generates output one token at a time, with two twists:
  - **Masked attention** — a token may only attend to tokens **before** it, never the future (during generation the future doesn't exist yet). Done by setting future scores to −∞ so softmax makes them 0.
  - **Cross-attention** — the decoder's Q looks at the encoder's K and V, so the output can attend to the input (e.g. translation).

> [!tip] Training vs inference
> **Training:** both halves run fully in parallel (the target is known; masking enforces left-to-right learning). **Inference:** the encoder still runs in parallel, but the decoder generates **one token at a time**, feeding each new token back in. Sequential at the token level, parallel inside each step.

> [!tip] The whole model in one breath
> Words → meaning vectors + position → then, N times: **attention (tokens share context) → add & norm → feed-forward (each token digests) → add & norm** → final softmax → next word → append and repeat.

## What's next
The five internals — **÷√d · GQA/MQA · RoPE · KV cache · memory-bound decode** — are in [[Phase1 — Internals]], plus **KV cache vs GQA/MQA**.
