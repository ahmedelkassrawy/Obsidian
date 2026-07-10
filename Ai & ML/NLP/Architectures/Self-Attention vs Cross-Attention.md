---
## 1. Core Concepts & Differences
Both mechanisms calculate relevance (weights) between tokens, but they differ in **where** the information comes from.

| Feature | Self-Attention (Intra-Attention) | Cross-Attention (Encoder-Decoder) |
| :--- | :--- | :--- |
| **Definition** | The model looks at other words within the **same** sequence to understand context. | The model looks at a **different** sequence to gather information. |
| **Goal** | Contextual understanding & relationship extraction within one input. | Alignment & mapping between two different modalities (e.g., Translation, Image Captioning). |
| **Example** | Linking "it" to "animal" in: *"The animal didn't cross because **it** was tired."* | Linking "Chat" (French) to "Cat" (English) during translation. |
| **Analogy** | Reading a sentence and re-reading parts of it to understand the grammar. | Writing a summary (Decoder) while looking back at the original book (Encoder). |
---
## 2. The Mechanics: Query, Key, Value ($Q, K, V$)

Attention is calculated using three vectors. The source of these vectors defines the type of attention.

### The "Library" Analogy
* **Query ($Q$):** What I am looking for *right now*.
* **Key ($K$):** The label/identifier of the data.
* **Value ($V$):** The actual content/information.

### Vector Sources

#### A. Self-Attention
All three vectors come from the **same** source sequence.
* $Q$: Source Sequence
* $K$: Source Sequence
* $V$: Source Sequence

#### B. Cross-Attention
Vectors come from **two different** sequences (typically Decoder and Encoder).
* $Q$: **Target Sequence (Decoder)** $\rightarrow$ "What do I need to write next?"
* $K$: **Source Sequence (Encoder)** $\rightarrow$ "Here is the reference index."
* $V$: **Source Sequence (Encoder)** $\rightarrow$ "Here is the reference content."

> [!IMPORTANT] Important Rule
> In Cross-Attention, the **Query** always comes from the part of the model attempting to generate output (the Writer), while the **Key/Value** come from the input data (the Reference).

---
## 3. Architecture & Use Cases

### Standard Transformer Location
In a standard Transformer (e.g., "Attention Is All You Need"), these layers are stacked in specific orders.

1.  **Encoder Block:**
    * Contains only **Self-Attention**.
    * *Purpose:* Build a rich representation of the input.

2.  **Decoder Block:**
    * Contains **both**.
    * **Layer 1: Masked Self-Attention:** Look at previous generated tokens (Context).
    * **Layer 2: Cross-Attention:** Look at the Encoder output (Content).

### Visual Flow in Decoder
`[Previous Outputs]` $\to$ **Masked Self-Attention** $\to$ `[Context Vector]` $\to$ **Cross-Attention** (with Encoder Output) $\to$ `[Next Word Prediction]`

---
## 4. PyTorch Implementation

The class `torch.nn.MultiheadAttention` handles both types. The difference is purely in how you pass the arguments to `.forward()`.

**Variables:**
* `src`: The Source Sequence (e.g., English Input).
* `tgt`: The Target Sequence (e.g., French Output so far).
### Code Patterns
#### 1. Self-Attention (Encoder)
```python
# Looking at itself
attn_output, _ = attention_layer(
    query=src, 
    key=src, 
    value=src
)
```

**2.Cross-Attention(Decoder)**
```python
# Decoder (tgt) looking at Encoder (src)
attn_output, _ = attention_layer(
    query=tgt,  # The 'Writer' asking questions
    key=src,    # The 'Reference' providing keys
    value=src   # The 'Reference' providing values
)
```
## 5. Masking (Critical Detail)
Masking is used to prevent the model from "cheating" (seeing the future).
### Where is it used?
- **Encoder Self-Attention:** No mask (usually). We want to see the whole sentence.
- **Decoder Cross-Attention:** No mask. We want to see the whole Source sentence.
- **Decoder Self-Attention:** **YES. Requires Causal Mask.**
### Causal Mask (Look-ahead Mask)
Since the Decoder generates text sequentially, word $t$ cannot attend to word $t+1$. We use a **Lower Triangular Matrix** (top-right is masked with $-\infty$).

```python
# Simplified concept of Causal Masking in PyTorch
# 0 = allow, -inf = block

mask = [
  [0,    -inf, -inf],  # Word 1 sees only Word 1
  [0,    0,    -inf],  # Word 2 sees Word 1 & 2
  [0,    0,    0   ]   # Word 3 sees Word 1, 2, & 3
]

# Implementation in Decoder Self-Attention
output, _ = self_attn_layer(
    query=tgt, 
    key=tgt, 
    value=tgt, 
    attn_mask=mask  # <--- Prevents peeking at future words
)
```