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