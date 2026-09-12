---
title: Transformers — the big picture
type: synthesis
tags: [nlp, transformers, attention, deep-learning, synthesis]
created: 2026-09-12
---

# Transformers — the big picture

> [!abstract] What this note is
> A single walkthrough that stitches together the transformer story from my scattered notes: why RNNs weren't enough, how attention fixed it, and how a full transformer is built piece by piece. Each section points to the deeper note it came from — see [[#Resources]] at the bottom.

---

## 1. The road here: why transformers exist

Transformers didn't appear from nowhere. They solved specific pain points in the models that came before.

### RNNs and their limit

An **RNN** reads text one token at a time and keeps a running memory (a *hidden state*) that it passes forward. The problem: by the end of a long sequence, the earliest tokens barely affect that memory. RNNs struggle with **long-range dependencies** — they forget context in long text.

> [!definition] Long-range dependency
> A relationship between two words that sit far apart in the text (e.g. a pronoun and the noun it refers to, ten words earlier). RNNs handle these poorly; attention handles them directly.

RNNs are also **slow to train** — each step depends on the previous one, so the work can't be split across GPUs. → deeper: [[RNN]], [[Recurrent Neural Networks (RNNs) and LSTMs]]

### Seq2Seq and the bottleneck

**Seq2Seq** (encoder + decoder, usually built from LSTMs) transforms one sequence into another — translation, summarization, chatbots. The encoder squeezes the whole input into a single fixed-length **context vector**, and the decoder generates the output from it.

The flaw: one fixed vector can't hold everything about a long sentence — the **information bottleneck**. The fix was to let the decoder *attend* to different parts of the input at each step instead of relying on one summary. That idea grew into full self-attention — and transformers. → deeper: [[Seq2Seq]]

---

## 2. The core idea: attention

> [!definition] Attention
> A mechanism that lets every token **look at every other token** and decide: *"how much should I care about each of them to understand myself?"* It learns relationships between words directly, regardless of distance.

Unlike an RNN (which only relates neighboring words through its memory), attention maps relationships between **every pair of words at once** — and it runs in **parallel** on GPUs, which is why transformers scale.

### Query, Key, Value

Attention works through three vectors per token. The "library" analogy makes it click:

| Vector | Question it answers | Library analogy |
|---|---|---|
| **Query (Q)** | What am I looking for right now? | Your search request |
| **Key (K)** | What do I offer / what am I about? | The label on each book |
| **Value (V)** | My actual content | What's inside the book |

You match your Query against every Key to get relevance scores, then use those scores to pull a weighted blend of the Values. → deeper: [[Self-Attention vs Cross-Attention]], [[Self Attention]]

### Self-attention vs cross-attention

Same math, different sources for Q/K/V:

- **Self-attention** — Q, K, V all come from the **same** sequence. Used to understand context *within* one input. Example: linking "it" → "animal" in *"The animal didn't cross because it was tired."*
- **Cross-attention** — Q comes from the sequence being generated (the decoder/"writer"), while K and V come from the input (the encoder/"reference"). Used to **align two sequences** — e.g. French ↔ English in translation.

> [!important] The rule
> In cross-attention, the **Query** always comes from the side producing output; the **Key/Value** come from the input being referenced.

### Multi-head attention

One attention mechanism can only learn **one type** of relationship. Language has many at once (grammar, meaning, reference), so we run several attention mechanisms in parallel — **heads**.

- Each head gets its own Q, K, V and learns to focus on a different pattern.
- Outputs of all heads are concatenated, then passed through a final projection (`W_o`).
- Practical rule: **`num_heads` must divide `d_model` evenly**. Pick the count like a learning rate — not too small, not too large.

---

## 3. Building a full transformer, step by step

The full flow before any attention happens: turn words into vectors, then add position.

### Step 1 — Token embeddings

> [!definition] Embedding
> A dense vector of real numbers that captures a token's **meaning**. Similar words end up with similar vectors (close together by cosine similarity).

Each token id is mapped to a vector of size `d_model` via an embedding layer (`nn.Embedding(vocab_size, d_model)`). The embeddings are then **scaled by √d_model** — without scaling, the positional encoding (next step) would dominate the small random embedding values and the model gets harder to train.

- Input shape: `(batch, seq_len)` → after embedding: `(batch, seq_len, d_model)`

### Step 2 — Positional encoding

A transformer has **no recurrence and no convolution**, so on its own it has no idea what order the words came in. Positional encoding injects that order.

> [!definition] Positional encoding
> A precomputed vector added to each token's embedding that encodes *where* the token sits in the sequence. After adding it, each token vector carries **meaning + position**.

- `PE` shape `(1, seq_len, d_model)` is added to `x` `(batch, seq_len, d_model)`.

### Step 3 — Multi-head attention

The Q/K/V, heads, and `W_o` projection described in [Section 2](#2-the-core-idea-attention). This is where tokens actually exchange information.

### Step 4 — Feed-forward network (FFN)

After attention, each position passes through the same small 2-layer MLP, independently:

```
d_model (512) → d_ff (2048) → ReLU → d_model (512)
```

Why expand then shrink? Expanding to `d_ff` lets the layer learn **rich, nonlinear feature combinations**; shrinking back keeps the model size manageable. Think of it as a per-token "mini brain" inside every transformer layer. (Paper defaults: `d_model=512`, `d_ff=2048`.)

### Step 5 — Encoder vs decoder blocks

- **Encoder block** — self-attention only. Purpose: build a rich representation of the input. No mask (it should see the whole sentence).
- **Decoder block** — two attention layers:
  1. **Masked self-attention** — looks only at tokens already generated (see masking below).
  2. **Cross-attention** — looks at the encoder's output to pull in the source content.

Decoder flow: `[previous outputs] → masked self-attention → cross-attention (with encoder output) → next-word prediction`

### Step 6 — Masking (so the model can't cheat)

> [!definition] Causal (look-ahead) mask
> A lower-triangular mask that stops a token from attending to future tokens. Word *t* may see words *1…t* but not *t+1*. Future positions are set to −∞ before the softmax so they get zero weight.

Where it applies:

| Layer | Mask? |
|---|---|
| Encoder self-attention | No — see the whole input |
| Decoder cross-attention | No — see the whole source |
| **Decoder self-attention** | **Yes — causal mask** (generation is sequential) |

---

## 4. Autoregressive generation

A decoder-style transformer is **autoregressive**: it predicts the next token from all previous ones, appends it, and repeats until a stop token (`<eos>`) appears. The number of tokens it can hold while doing this is its **context window** — bigger window = more it can "remember," but more memory and cost. → deeper: [[Ch.3]] (GenAI Services book — transformer + serving view)

---

## 5. The three transformer families

Each specializes by which blocks it keeps:

| Variant | Keeps | Good at |
|---|---|---|
| **Encoder-only** (e.g. BERT) | Encoder | Understanding: classification, sentiment, entity extraction |
| **Decoder-only** (e.g. GPT) | Decoder | Generation: text, chat, language modeling |
| **Encoder–decoder** (e.g. T5) | Both | Sequence-to-sequence: translation, summarization, Q&A |

---

## Resources

Notes this was synthesized from (each goes deeper on its piece):

- [[RNN]] — recurrent networks and their memory limits
- [[Recurrent Neural Networks (RNNs) and LSTMs]] — RNN/LSTM mechanics
- [[Seq2Seq]] — encoder/decoder, the context-vector bottleneck, attention's origin
- [[Attention is all you need]] — embeddings, scaling, positional encoding, FFN, multi-head attention (implementation-level)
- [[Self-Attention vs Cross-Attention]] — Q/K/V sources, decoder layers, masking, PyTorch patterns
- [[Self Attention]] — self-attention clipping
- [[Ch.3]] — transformers in the context of serving GenAI models (Building GenAI Services book)

### Related architectures
- [[LSTM PyTorch]] · [[LSTMS Adhocs]] · [[RNN and LSTM]] · [[RNN Implementation Guide]]
