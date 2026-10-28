---
tags: [genai, llm, transformers, attention, kv-cache, moe, deepseek]
---

## How self-attention works

Self-attention lets the model look at **previous tokens** to enrich the representation of the token it's currently processing.

It takes the current token's vector (pink in the figure) together with the vectors of the tokens before it. The output is an enriched vector for the current position that carries context from the rest of the sequence.

![[Pasted image 20261028181400.png]]

The attention calculation takes in a set of vectors:

- The vector for the **current** position
- The vectors for the **previous** positions

### Queries, keys, and values

A trained model knows what to attend to because of three **projection matrices** it learned during training.

> [!definition] Queries, keys, and values (Q, K, V)
> The three matrices you get by multiplying the input vectors by each of the three learned projection matrices.

![[Pasted image 20261028181620.png]]

### Combining the relevant information

Once the relevance scores are known, self-attention combines information from the previous tokens, **weighted by how relevant each one is**, and merges it into the vector of the current token.

![[Pasted image 20261028182521.png]]

That merged vector is the output of the self-attention layer.

> [!abstract] The full calculation
> 1. Project the current and previous tokens into queries, keys, and values.
> 2. Multiply the query by the keys, scale by √dₖ, and pass the result through a softmax. This gives the **relevance scores**.
> 3. Multiply the relevance scores by the values. This gives the **attention output** for the current position.

![[Pasted image 20261028182602.png]]

## KV caching

Applied naively to text generation, this early form of self-attention does a lot of **redundant work**.

At every generation step, attention is recalculated for the whole sequence, even though the K and V vectors of the earlier tokens were already computed in previous steps.

For example, say the model is processing the attention scores for the tokens "My" and "name." Regular attention would recompute their K and V vectors at every later step, even though it already computed them once.

![[Pasted image 20261028182849.png]]

> [!definition] KV cache
> Storing the K and V vectors of tokens already processed so they can be reused in later decoding steps instead of recomputed. This cuts redundant computation and makes inference much faster.

The query (Q) vectors don't need to be cached, because old queries aren't used again in later steps.

> [!tip] Only one query is needed
> To compute self-attention for the next token, you need only the **query vector of the latest token**, plus the cached keys and values.

![[Pasted image 20261028183059.png]]

> [!warning] The memory trade-off
> A KV cache makes inference much faster, but caching every K and V value takes significantly more memory.

## More efficient self-attention

DeepSeek recently introduced two attention mechanisms that greatly improved the efficiency of attention:

- **Multi-head Latent Attention (MLA)**
- **DeepSeek Sparse Attention (DSA)**

### Multi-head Latent Attention (MLA)

MLA is a major step toward making the KV cache use less memory.

> [!definition] Multi-head Attention (MHA)
> Attention that keeps separate Q, K, and V projection matrices for each **attention head**, so each head produces its own Q, K, and V.

MLA is a variant of Multi-head Attention. It uses **low-rank joint compression** of the keys and values to shrink the KV cache during inference.

At its core, MLA compresses the keys and values into a smaller **latent representation**, and caches that instead of the full K and V.

> [!definition] Quantization
> Reducing the numerical precision of stored values. In practice, MLA's compressed cache is often combined with quantization to save even more memory.

How MLA works, step by step:

1. **Compress.** The input embeddings are compressed into smaller representations called the **latent Q** and **latent KV**. These are much smaller than the full Q and KV, so we cache the latent KV instead of the full K and V.
2. **Add position.** Positional information comes from **Rotary Position Embedding (RoPE)**. It's applied to a separate (decoupled) part of the latent Q, since the latent Q is recomputed at every step anyway.
3. **Split into heads.** The Q, K, and V representations are split across multiple attention heads, just like standard Multi-head Attention.
4. **Attend.** The content and positional parts are concatenated and passed through standard Multi-head Attention.

> [!warning] Why RoPE isn't applied to the latent K
> If RoPE were applied to the cached latent K, that cached K would have to be recomputed at every step, which defeats the point of caching. So positional information is carried by a separate small key instead.

![[Pasted image 20261028184006.png]]

In short, MLA is Multi-head Attention with a **compressed KV cache** that holds the latent KV.

This compression shrinks the KV cache a lot and allows much faster inference. It's also more efficient than earlier methods such as Grouped-Query Attention.

> [!note] GQA and MQA
> **Grouped-Query Attention (GQA)** and **Multi-Query Attention (MQA)** save KV-cache memory by sharing K and V across query heads, but they tend to be less accurate.

![[Pasted image 20261028190004.png]]

---

### DeepSeek Sparse Attention (DSA)

DSA is built on top of MLA. It's an extra module that selects **which tokens to attend to** more efficiently.

It has two main components:

- A **lightning indexer**
- A **Top-K selector**

> [!definition] Lightning indexer
> Scores how relevant each preceding token is to the current query. It uses Q and K values that both have RoPE applied, plus a scalar weight parameter *w* that helps it decide which tokens to pass to full attention.

> [!definition] Top-K selector
> Takes the lightning indexer's scores and retrieves only the KV entries for the top-K scoring tokens.

The result: the attention output is computed from the query token and only a **subset** of KV entries.

![[Pasted image 20261028190333.png]]

Together, the lightning indexer and Top-K selector cut the number of tokens to attend to down to K. That drastically reduces the computation attention needs.

> [!note] MLA inside DSA uses MQA
> Because DSA sits on MLA, it already gets a large memory saving from the compressed KV cache. In DeepSeek's version of MLA here, the core attention mechanism is **MQA instead of MHA**. The authors said they optimized for computational efficiency, which fits MQA, since it uses fewer keys and values than MHA.

## Mixture of Experts (MoE)

MoE is an increasingly mainstream technique for building more efficient LLMs. It uses several sub-models, called **experts**, to improve both quality and efficiency.

The two main components of MoE:

| Component | What it does |
| --- | --- |
| Experts | Each feed-forward neural network in the LLM is replaced by a set of experts |
| Router (gate network) | Decides which tokens are sent to which experts |

### Experts

A typical Transformer-based LLM uses self-attention followed by a feed-forward neural network (FFNN).

> [!definition] Dense model
> A model where everything is activated for every token. In a dense Transformer block, the FFNN is active for every single token that passes through.

![[Pasted image 20261028190719.png]]

> [!definition] Sparse model
> A model that uses several feed-forward networks instead of one. Each is typically smaller than a regular FFNN, but together they tend to be bigger.

Each of these networks is called an **expert**, because during training each one learns different information and may specialize in processing certain tokens.

For instance, one expert might handle numbers while another handles verbs. It's still not entirely clear what experts learn. Some research suggests they specialize in fine-grained information (like verbs vs. numbers) rather than each learning a whole different domain.

### The router

If every expert is used for every token, there's no efficiency gain. To pick a subset of experts during inference, we use the **router**.

> [!definition] Router (gate network)
> A small feed-forward neural network trained to choose an expert for a given token. The router plus the experts make up the **MoE layer**.

The router is arguably the most important part, since the experts themselves are just small feed-forward networks.

![[Pasted image 20261028192633.png]]

![[Pasted image 20261028192644.png]]

How the router chooses an expert:

1. The router has its own weight matrix, which it multiplies by the input token embeddings.
2. A softmax over the output gives a **probability distribution over the experts**.
3. Each probability is the likelihood that an expert is chosen for that token.

![[Pasted image 20261028192740.png]]

### Load balancing

Any number of experts can be selected, but usually a fixed number is used for training and inference.

> [!warning] Undertrained experts
> If the same experts are always chosen during training and inference, all the other experts end up undertrained.

> [!definition] Load balancing
> The router dynamically balancing which experts it chooses and when, so training is spread across all experts.

Two main techniques keep one expert from dominating training: **expert capacity** and **auxiliary loss**.

#### Expert capacity

> [!definition] Expert capacity
> A limit on how many tokens each expert in the MoE layer can process.

- Instead of one expert doing all the work, tokens are spread more evenly.
- Once an expert hits its capacity, any further token routed to it goes to the **next-highest-scoring** expert.

![[Pasted image 20261028192952.png]]

#### Adjusting the router

Instead of limiting the experts, you can adjust the router to account for the imbalance.

A simple technique is to add **Gaussian noise** just before the router produces its probabilities. The noise shifts the distribution slightly, so by chance the router sometimes picks different experts.

#### Auxiliary loss

> [!definition] Auxiliary loss
> Extra loss functions added to the router that reward it for spreading tokens evenly across experts during training, or penalize it when the same expert keeps getting chosen.

### Why MoE is efficient

MoE's main benefit is lower compute. It doesn't make the model smaller, but it runs much faster because only a few experts are active at any moment.

> [!definition] Sparse vs. active parameters
> - **Sparse parameters:** all of an MoE model's parameters. They all have to be loaded into memory.
> - **Active parameters:** the ones actually activated during inference.

![[Pasted image 20261028193141.png]]

### Shared expert (DeepSeek R1)

DeepSeek R1 also has a **shared expert** that bypasses the router and is always chosen. This often lets the model route general knowledge to the shared expert and specialized knowledge to the others.

![[Pasted image 20261028193227.png]]
