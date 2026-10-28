How Self-Attention Works
self-attention allows the model to attend to previous tokens, thus enriching the representation of the token we’re currently processing

Self-attention takes the current token’s vector (pink) along with those of preceding tokens and produces an enriched output vector for the current position that incorporates context from the rest of the sequence

![[Pasted image 20261028181400.png]]

Going into the attention calculation are a collection of vectors
- Vector for the curr position 
- Vector for the prev position

A trained model is able to attend properly by utilizing three projection matrices that resulted from the training process

We multiply the input vectors by each of these projection matrices, resulting in matrices we call the queries, keys, and values matrices

![[Pasted image 20261028181620.png]]

After deciding the relevance values, self-attention then proceeds to combine information from these tokens, weighted by how relevant they are, and merge them into the vector of the current token we’re processing.

![[Pasted image 20261028182521.png]]

This vector becomes the output of the self-attention layer.

The current and previous tokens are projected into queries, keys, and values; the query-key product (scaled by √dk and passed through softmax) produces the relevance scores, which are then multiplied by the values to produce the attention output for the current position.

![[Pasted image 20261028182602.png]]


KV Caching
This early form of self attention , does a lot of redundant calculations of the K and V weights for each generated attention score if we apply it natively to text geenration

Specifically, at each step, attention is recalculated for the entire sequence despite having calculated the K and V vectors of the previously seen tokens before.

Imagine that a model is processing the attention scores for the tokens “My” and “name.”

regular attention would recalculate the K and V vectors at each subsequent step despite having calculated them before.

![[Pasted image 20261028182849.png]]

This is where the KV cache comes in. 
- Instead of having to recalculate those vectors, we can simply cache and reuse them for subsequent decoding steps.
- This makes inference much faster by reducing the redundant computation

A basic KV cache demonstrates how the K and V vectors are reused from previous steps instead. note that the query (Q) vectors do not need to be cached because they become unnecessary in subsequent iterations.

**Specifically, we need only the query vector of the latest token to compute the self-attention

![[Pasted image 20261028183059.png]]

KV cache can make inference much faster, it does require significantly more memory if all KV values are cached.

More Efficient Self-Attention
More recently, however, DeepSeek introduced two attention mechanisms that showed tremendous improvements in the efficiency of attention calculations, namely Multi-head Latent Attention (MLA) and DeepSeek Sparse Attention (DSA).

Multi-head Latent Attention 
A major step in making the KVcache more memory efficient is through MLA,

MLA is a variant of Multi-head Attention, which maintains separate Q, K, and V projection matrices for each attention head, producing a different Q, K, and V matrix per head.

MLA uses lowrank joint compression of the keys and values to reduce the KV cache during inference.

At its core, it compresses the keys and values into a smaller latent representation that is cached in place of the full K and V. In practice, this compressed cache is often combined with quantization (reducing the numerical precision of stored values) for additional memory savings

MLA first compresses the input embeddings into lower-dimensional representations called the latent Q and latent KV

These representations are significantly smaller than the full Q and KV, which allows us to cache the latent KV instead of the full K and V

Positional information via Rotary Position Embedding (RoPE) is applied to a decoupled component of the latent Q, since the latent Q is recomputed at every step. RoPE is not applied to the latent K itself, because the cached K would then need to be recomputed at every step, breaking the benefit of caching. Therefore, positional information is carried by a separate small key instead

Note that at this step, the Q, K, and V representations are split across multiple attention heads, much like standard Multi-head Attention. Finally, the content and positional components are concatenated and passed through standard Multi-head Attention.

![[Pasted image 20261028184006.png]]

MLA is essentially Multi-head Attention but with a compressed KV cache containing the previously mentioned Latent KV representation.

This compression reduces the KV cache quite a bit and allows for much faster inference. It’s also more efficient than previous methods, such as Grouped-Query Attention.