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

## Multi-head Attention (MHA), from A to Z

> [!info] Added notes, not from the book
> This section is an explainer added on top of the chapter. Paper names, years, and model details are from memory and weren't re-checked against sources.

MHA runs several small attention calculations side by side. Each one learns to look for a different kind of relationship between tokens. It was introduced in the 2017 Transformer paper, *Attention Is All You Need*.

### The problem before it

Before 2017, language models were mostly **RNNs** (recurrent neural networks, including LSTMs). They read a sentence one word at a time and carried a running memory forward. That caused two problems:

- **Slow.** Word 50 can't be processed until word 49 is done, so the work can't be spread across a GPU's cores.
- **Forgetful.** Everything has to squeeze through one running memory, so the start of a long sentence fades by the end.

In 2014–2015, Bahdanau and then Luong added **attention** on top of RNNs. When producing each output word, the model could look back at every input word and weight the useful ones. That fixed much of the forgetting, but the RNN underneath was still slow.

### The first fix: attention alone

The 2017 paper dropped the RNN and kept only attention: the self-attention above, where every token makes a Q, K, and V and you compute softmax(QKᵀ / √dₖ) · V.

Every token can look at every other token directly, and all positions are processed at once. That solves both problems: the work runs in parallel, and there's no memory bottleneck.

### Why one head wasn't enough

A single attention calculation gives each token **one** set of weights, which means one blended average of the other tokens. But language has several relationships at once.

Take "The animal didn't cross the street because **it** was tired." To understand *it*, the model wants to know:

- what *it* refers to (animal),
- which verb goes with it (was),
- what's nearby in position.

One softmax has to squash all of that into one average, so the signals blur together.

### How MHA fixed it

Instead of one big attention, run **h small ones in parallel**, each with its own learned projection matrices:

```text
input x (512 dims)
   │
   ├─ head 1: W_Q1, W_K1, W_V1 → 64-dim Q,K,V → attention → 64-dim output
   ├─ head 2: W_Q2, W_K2, W_V2 → 64-dim Q,K,V → attention → 64-dim output
   ├─ ...
   └─ head 8: W_Q8, W_K8, W_V8 → 64-dim Q,K,V → attention → 64-dim output
                                                     │
                       concat (8 × 64 = 512) → W_O → output (512 dims)
```

1. **Each head has its own Q, K, and V.** So one head can track "which noun does this pronoun mean" while another tracks "the previous word."
2. **The heads are smaller.** The original split 512 dimensions into 8 heads of 64, so total compute is about the same as one full-size head.
3. **The output matrix W_O mixes them back together**, so the next layer gets one vector that combines every head's findings.

Nobody tells a head what to specialize in; it falls out of training. Researchers have found heads that follow grammar, resolve pronouns, look at the previous token, and copy earlier patterns ("induction heads").

> [!note] Three places MHA shows up
> - **Self-attention** (encoder): every word looks at every other word.
> - **Masked self-attention** (decoder): each word looks only at earlier words. This is the GPT style.
> - **Cross-attention**: the decoder looks at the encoder's output, as in translation.

### Pros and cons

**Pros**

- **Parallel.** The whole sequence is processed at once during training, which made huge models practical.
- **Direct long-range links.** Word 1 and word 1,000 are one step apart.
- **Several relationships at once**, at about the cost of one head.
- **General.** It works on text, images, audio, and proteins with almost no changes.

**Cons**

- **Cost grows with the square of the sequence length.** Every token scores every other token, so twice the context means four times the attention work.
- **Big KV cache.** Every head in every layer caches its own K and V for every token.
- **Redundant heads.** Studies in 2019 (Michel et al., Voita et al.) found many heads can be pruned with little loss.

> [!example] How big the KV cache gets
> A Llama-2-7B-sized model: 32 layers × 32 heads × 128 dims per head × 2 (K and V) × 2 bytes (16-bit) ≈ **0.5 MB per token**. A 4,096-token conversation needs about **2 GB** of cache. Generation ends up limited by memory speed, not compute.

### What came next

Each step down this line attacks the KV-cache cost:

| Version | Idea | Cache vs MHA | Used in |
| --- | --- | --- | --- |
| **MQA** (Shazeer, 2019) | All query heads share **one** K and V | ÷ number of heads | PaLM, Falcon |
| **GQA** (Ainslie et al., 2023) | Query heads share K/V **in groups** | ÷ group size | Llama 2 70B, Llama 3, Mistral |
| **MLA** (DeepSeek-V2, 2024) | Compress K/V into a small **latent** vector and cache that | smaller still, quality close to MHA | DeepSeek V2/V3/R1 |

MQA saves the most memory but loses some quality. GQA is the middle ground most open models chose. MLA is covered below.

A separate line of work makes attention cheaper without changing what it computes. **FlashAttention** gives the exact same result while touching GPU memory far less. **Sparse attention** (sliding windows, DSA below) has each token look at only some of the others.

### Where MHA was used

From about 2017 to 2022 it was the default almost everywhere:

- **Translation:** the original Transformer.
- **Understanding text:** BERT (12 heads in the base model), RoBERTa, T5.
- **Generating text:** GPT-2, GPT-3 (96 heads per layer), Llama 1.
- **Images:** Vision Transformer (ViT), CLIP.
- **Speech:** Whisper.
- **Science:** AlphaFold 2 uses attention variants for protein structure.

Today it's still standard in encoders and smaller models. Large chat models have mostly moved to GQA or MLA, because at long context the KV cache is what costs money.

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

## MoE, dense vs. sparse, explained

> [!info] Added notes, not from the book
> This section is an explainer added on top of the chapter. Model figures are from memory and weren't re-checked against sources.

In one line: a **dense** model runs all its weights on every token. A **sparse** (MoE) model owns many more weights but runs only a small slice of them per token. You get a big model's knowledge for close to a small model's compute.

### Why MoE targets the FFNN

Each Transformer block has two main parts. Attention mixes information *between* tokens. The FFNN then processes each token *on its own*, and it's often described as where much of the model's stored knowledge lives.

The FFNN also holds most of the parameters (roughly two-thirds in a typical model). That's why MoE replaces the FFNN and leaves attention alone.

### Dense: one doctor sees everyone

```text
token → attention → [ one big FFNN ] → next block
                     (all weights used, every token)
```

Think of a clinic with one general doctor who sees every patient. To make the doctor know more, you make them bigger, and every visit costs more. In a dense model, **more knowledge = more compute per token**. GPT-3, Llama 1–3, and BERT are dense.

### Sparse: a receptionist and specialists

```text
                            ┌─ expert 1
                            ├─ expert 2  ◄── chosen (0.6)
token → attention → router ─┼─ expert 3
                            ├─ expert 4
                            ├─ expert 5  ◄── chosen (0.3)
                            └─ ... expert 8
output = 0.6 × expert2(token) + 0.3 × expert5(token)
```

Now the clinic has 8 specialists and a receptionist (the router), and each patient sees only 2 of them. The clinic knows a lot, but each visit costs about two doctors' time. "Sparse" just means most of the model is switched off for any given token.

> [!tip] Routing happens per token, per layer
> In one sentence, "The" might go to experts 2 and 5 in layer 1, then experts 7 and 1 in layer 2. That's why experts don't become clean "math" or "biology" specialists. They pick up finer patterns like punctuation, numbers, or certain verbs.

### Total vs. active parameters

The book calls all the weights "sparse parameters." Most papers and model cards call them **total parameters**.

- **Total parameters:** every expert. All must sit in GPU memory, because any token might need any expert.
- **Active parameters:** what one token actually uses. This sets the compute cost.

> [!example] Mixtral 8x7B
> 8 experts, top-2 routing. About **47B total** parameters but only about **13B active** per token. (Not 56B, because the experts share attention and embeddings.) It runs about as fast as a 13B dense model while knowing closer to what a 47B model knows.

### Pros and cons

**Pros**

- Much more knowledge for the same compute per token.
- Reaches a given quality with less training compute than a dense model.
- Fast inference for its size.

**Cons**

- **Memory doesn't shrink.** All experts must be loaded. MoE saves compute, not memory.
- **Harder to train.** Load balancing, routing instability, and extra loss terms need tuning.
- **Harder to serve.** Experts are spread across GPUs, and moving tokens between them adds overhead.
- **Fine-tuning can be tricky**, and small batches use the hardware less efficiently.

### Real models

| Model | Type | Total | Active per token |
| --- | --- | --- | --- |
| Llama 3 70B | Dense | 70B | 70B |
| Switch Transformer (Google, 2021) | MoE, top-1 | up to 1.6T | a small fraction |
| Mixtral 8x7B (2023) | MoE, 8 experts, top-2 | ~47B | ~13B |
| DeepSeek-V3 / R1 | MoE, 256 routed + 1 shared, top-8 | 671B | ~37B |

The idea dates to 1991. Shazeer's 2017 paper (*Outrageously Large Neural Networks*) brought it into modern deep learning with noisy top-k routing. It went mainstream once Mixtral and DeepSeek showed open MoE models could match much bigger dense ones.
