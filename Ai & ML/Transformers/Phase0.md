a transformer takes a sequence of words and for each position it predicts what comes next by letting every word look at every other word and mix in the relevant information

That "look at each other" step is **attention**

Let's build the pipeline in order.
#### 1. Text → tokens

A model can't read letters. 
First the text is chopped into **tokens** — chunks that are usually a word or word-piece.

```
"I love RAG"  →  ["I", " love", " R", "AG"]  →  [40, 1842, 431, 6438]
```

[!definition] Token  
- The smallest unit of text the model reads.
- Each maps to an integer ID from a fixed vocabulary (e.g. ~50k–100k entries). 
- Not always a whole word — "RAG" might split into "R"+"AG".

2. Token → embedding (a vector)
- Each token ID is looked up in a big table and turned into a vector
- a list of numbers (say 1536 of them) that represents the token's _meaning_ as a point in space.

```
40  →  [0.2, -1.1, 0.7, ...]   (1536 numbers)
```

[!definition] Embedding  
- A vector that encodes a token's meaning.
- Similar meanings sit near each other in this space ("king" near "queen").
- The model _learns_ these numbers during training. 
- `d_model` = the length of this vector (1536 here).

So your sentence is now a **matrix**:
`[sequence_length × d_model]` — one row per token, 
- each row a meaning-vector.

3. The problem embeddings alone can't solve
The embedding for " love" is the **same vector** no matter where it appears or what surrounds it.

But meaning depends on context:
- "river **bank**" vs "money **bank**" — same token, different meaning.
- The model needs each word's vector to _absorb_ meaning from its neighbors.

**That's what attention does:** it rewrites each token's vector by pulling in information from the other tokens that matter.

After attention, the "bank" vector in "river bank" has soaked up "river" and now means the right thing.

- so now text -> tokens -> embeddings
- after this step your sentence is a **matrix of numbers** — a grid
- If the sentence is 4 tokens and each embedding is 1536 long, you have a `4 × 1536` grid. 
- 4 rows (one per token), 1536 columns (the meaning-numbers).

[ + position info ]
The problem:
	attention (next box) looks at all tokens _at once_, with no built-in sense of order.
	
"dog bites man" and "man bites dog" look identical — same tokens, same vectors. But order changes meaning completely.

**The fix:** add **position information** to each embedding so the model knows _where_ each token sits.

```
embedding of "dog" at position 0 = meaning("dog") + position(0)

embedding of "dog" at position 5 = meaning("dog") + position(5) ← now distinguishable
```

[!definition] Positional encoding  
Extra numbers added to each token's vector that encode its position in the sequence.
Without it, a transformer is "order-blind."

#### `ATTENTION (mix across tokens)` — the core

This is the "let words look at each other" step. 
Each token's vector gets **rewritten** by pulling in information from other tokens.

what happens for one word:

1. The word asks a question: _"which other words are relevant to me?"_
2. It compares itself against every other word to get a **relevance score** for each.
3. It builds its new vector as a **weighted blend** of the other words' info — more from the relevant ones, less from the rest.

So "bank" in "river bank" scores "river" as highly relevant, blends it in, and its vector shifts toward the water meaning.

**That's the whole point of the model** — the Q/K/V math in Step 1 is just _how_ those relevance scores and blending are computed.

[!definition] Attention  
The step where each token updates its own vector by mixing in information from other tokens, weighted by how relevant each other token is to it.

#### `feed-forward (think per-token)`

After attention, each token has gathered context from its neighbors. Now the **feed-forward** network processes **each token on its own** — no more looking around — to "digest" what it just gathered.

- **Attention = tokens talk to each other** (mixing across positions).
- **Feed-forward = each token thinks alone** (a small neural net applied to each row independently).

[!definition] Feed-forward network (FFN)  
- A small 2-layer neural net applied to each token's vector separately. 
- It's where a lot of the model's learned "knowledge" is stored. 
- Attention _moves_ information between tokens; 
- the FFN _transforms_ it within each token.

Think of one layer as: **gather (attention) → digest (feed-forward).**

#### `repeat N times (N layers)`

One round of "gather → digest" is **one layer**. A real model stacks many (GPT-3 = 96 layers).

- Early layers catch simple patterns (grammar, which word refers to which).
- Later layers build abstract meaning (tone, logic, facts).
- Each layer's output feeds the next, so understanding gets deeper with depth.

[!definition] Layer / depth  
- One attention + feed-forward block. 
- "N layers" = stacking N of them. 
- More layers = more capacity to build abstract understanding, but more compute.

#### `predict the next token`

After the last layer, each position's final vector is turned back into a **probability over the whole vocabulary** — "what word comes next?"

"I love" →  next-token probabilities:  " you" 12%, " it" 9%, " RAG" 3%, ...

The model picks from that distribution → that's the generated word.
Then it appends that word and runs the whole pipeline again for the next one.

(This repeat-with-each-new-word is exactly what makes generation slow — and why the **KV cache**, Step 5, exists.)

[!tip] The rhythm of the whole thing  
**embeddings** (meaning) **+ position** (order) → then per layer: **attention** (tokens share info) → **feed-forward** (each token digests) → stack that N times → **predict next word** → append it → do it all again.

![[Pasted image 20260917204215.png]]

![[Pasted image 20260917204710.png]]

Query (Q)
What do I look for?

Key (K)
what do I offer?

Value (V)
what I pass on

each = input × a learned weight matrix (Wq, Wk, Wv)

Why three copies (Q, K, V)? Why not compare embeddings directly?
**The naive idea:** just dot each token's embedding with every other token's embedding to get similarity. Skip Q/K/V.

Why that fails
a token needs to play **three different roles** at once, and one vector can't do all three:
- When it's the one **asking** ("what am I looking for?") — that's a different question than
- when it's being **searched** ("do I match what you're looking for?") — which is different again from
- **what it actually contributes** once matched ("here's my information")

**The fix:** multiply the embedding by three separate **learned** matrices to get three specialized views:

```
Q = embedding × Wq   ("what I'm looking for")
K = embedding × Wk   ("what I offer to matchers")
V = embedding × Wv   ("what I pass on if matched")
```

[!definition] Q, K, V  
Three learned projections of the same token vector. 
- **Query** = the search request. 
- **Key** = the searchable label. 
- **Value** = the payload delivered. 

- Attention matches Q against K to decide how much of each V to take.

**The library analogy:** 
- you have a **search request** (Q). 
- Every book has a **spine label** (K). 
- You match your request against the labels, and from the best matches you take the **book's actual contents** (V).

Because Wq, Wk, Wv are _learned_, the model figures out on its own what makes a good question, a good label, and a good payload.

### 2. Why ÷√d?

### 2. Why ÷√d?

**What the dot product gives you:** `Q · K` sums up `d` multiplied pairs (d = the vector length per head, e.g. 128). Add up 128 random-ish products and the total **grows with d** — more terms, bigger sum. The bigger d is, the larger the raw scores get.

**Why big scores are a problem:** those scores go straight into **softmax**. Softmax turns numbers into probabilities, but it's _sharp_ — if one input is much bigger than the others, softmax pushes almost all the weight onto that one and ~0 on the rest.

softmax([2, 1, 0])      → [0.67, 0.24, 0.09]   (soft, spread)
softmax([20, 10, 0])    → [~1.0, ~0.00, ~0.00] (spiky, winner-take-all)

So if d is large, raw scores blow up → softmax goes spiky → each token attends to **exactly one** other token and ignores everything else. That kills the "blend from several tokens" behavior, and during training it makes gradients tiny (the flat regions of softmax) → the model barely learns.

**The fix — scale the scores back down:** divide by √d.

scores = (Q · Kᵀ) / √d

> [!definition] The √d scaling  
> As vectors get longer (d), dot-product scores grow proportionally to d, and their spread (standard deviation) grows like √d. Dividing by √d cancels that growth, keeping scores in a sane range so softmax stays soft and gradients stay healthy — no matter how big d is.

**Why √d and not d?** Because the _spread_ of the sum grows like **√d**, not d. (Variance adds up linearly across the d terms → variance ∝ d → standard deviation ∝ √d.) You divide by the standard deviation to normalize, so you divide by √d. Dividing by d would over-shrink and flatten the scores too much. **This is the "why √d not d" gate in your roadmap** — the answer is "variance is proportional to d, so std-dev is √d."

### 3. Multi-head — why run it several times in parallel

**The limit of one attention grid:** a single Q/K/V set can only learn **one kind** of "what's relevant." But relevance has many flavors at once:

- one pattern = "which word does this pronoun refer to?"
- another = "what's the grammatical subject?"
- another = "which nearby words modify me?"

One head must average all these into a single attention pattern — a blur.

**The fix:** run several attention operations **in parallel**, each with its _own_ Wq/Wk/Wv. Each is a **head**, and each learns a different relevance pattern.

[!definition] Multi-head attention (MHA)  
The attention computation run H times in parallel, each head on a `d_model/H`-sized slice, each with its own learned Q/K/V matrices. The heads' outputs are concatenated back to `d_model` and mixed by one more matrix. Different heads specialize in different kinds of relationships.

**Key mechanics:**

- The vector is _split_ across heads (1536 → 12 × 128), so multi-head costs about the **same** as single-head — you're not doing 12× the work, you're slicing the same budget 12 ways.
- Each head produces its own `4×128` output; you **concatenate** them back to `4×1536`, then apply a final "mixing" matrix (Wo) so the heads can combine.

[!tip] The three answers in one line each  
**Q/K/V** = one token plays 3 jobs (ask / advertise / deliver), so it needs 3 learned views. **÷√d** = keeps scores from blowing up as d grows (spread ∝ √d), so softmax stays soft. **Multi-head** = run attention many times in parallel so each head learns a different kind of relevance, at the same total cost.

### What is a "head"?

> [!definition] Head  
> One complete attention computation — its **own** Q, K, and V matrices — running on a **slice** of each token's vector. A model runs many heads side by side (H of them); each learns to look for a _different kind_ of relationship.

The plain picture: take each token's 1536-number vector and **cut it into H slices** (say 12 slices of 128 each). Give each slice to its own head. Each head does the _full_ attention dance you saw (Q·Kᵀ → ÷√d → softmax → ×V) but only on its 128-wide slice. Then you **glue the slices back together** into 1536 and mix them with one final matrix (Wo).

**Why slice instead of just running 12 full copies?**

- **Cost stays flat.** 12 heads × 128 dims = 1536 — the same total work as one 1536-wide head. You get 12 specialists for the price of one generalist.
- **Specialization.** One big head must blur all relationship types into a single attention pattern. Twelve small heads each get to specialize — head 2 tracks grammar, head 5 tracks which noun a pronoun refers to, etc. The model decides what each head learns.

**The one-line version:** a head is a mini-attention with its own Q/K/V on a slice of the vector; multi-head = many of them in parallel, each catching a different pattern, glued back together.

### The 4 steps inside every block (what the diagram shows)

**Step 1 — Multi-head attention.** Tokens _talk to each other_. Each head compares queries to keys, blends values, and the token vectors absorb context. (Everything in the previous two visuals happens here, ×H heads.)

**Step 2 — Add & Norm.** Two safety mechanisms bolted on:

- **Add (residual):** take attention's output and _add back the original input_ (`output + input`). This lets information skip the layer if it wants — critical for training deep stacks (96 layers) without the signal getting lost or scrambled.
- **Norm (layer normalization):** rescale each vector to a stable range so numbers don't blow up or vanish as they pass through many layers.

> [!definition] Residual + LayerNorm  
> **Residual** = add the block's input to its output, so nothing important gets destroyed and gradients flow cleanly through deep networks. **LayerNorm** = normalize each token vector to keep its numbers in a healthy range. Together they're what make stacking N layers actually trainable.

**Step 3 — Feed-forward.** Now each token is processed **alone** — a small 2-layer network applied to each row. Attention _moved_ information between tokens; the feed-forward _transforms_ it inside each token. This is where a lot of the model's learned facts live.

**Step 4 — Add & Norm again.** Same residual + normalize, this time around the feed-forward.

Then the block's output becomes the next block's input — **×N times**. After the last block, the **final linear + softmax** turns each vector into next-token probabilities.

> [!tip] The whole model in one breath  
> Words → meaning vectors + position → then, N times: **heads let tokens share context (attention) → add & norm → each token digests alone (feed-forward) → add & norm** → final softmax → next word → append and repeat.