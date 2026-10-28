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

Note that Grouped-Query Attention and Multi Query Attention share K and V across query heads to reduce the memory necessary for the KV cache but tend to be less accurate.

![[Pasted image 20261028190004.png]]

----
DeepSeek Sparse Attention
instantiated under MLA and is an additional module to more efficiently select the tokens to attend to

It has two main components
- a lightning indexer 
- a Top-K Selector.

The lightning indexer determines how relevant each preceding token is to the current query.
- For that, it uses the Q/K values that both have RoPE applied to them
- Likewise, it takes in a scalar weight parameter w that helps the lightning indexer make better decisions about which tokens to select for the full attention mechanism.
- The output of the lightning indexer is scores fed to the Top-K Selector, which in turn retrieves only the KV entries that correspond to the Top-K index scores
As a result, the attention output is computed through the query token and a subset of KV entries.

![[Pasted image 20261028190333.png]]

Together, the Lightning Indexer and Top-K Selector reduce the number of tokens to attend to K

drastically reduces the computation necessary for the attention computations

Note that since MLA is used, there is already a significant memory benefit due to the compression of the KVcache. In their construction of MLA, instead of using MHA as the core attention mechanism, MQA was used. The authors mentioned optimizing for computational efficiency, which is true for MQA, considering it uses fewer keys and values than MHA

Mixture of Experts
MoE is a technique that is becoming more mainstream to create more efficient LLMs. MoE uses several submodels or “experts” to improve the quality and efficiency of LLMs.

main components of an MoE:
- Experts -> each feed forward neural network in an LLM is replaced by a set of "experts"
- Router or gate network -> determines which tokens are sent to which experts

Let’s first explore experts.
Remember that a typical Transformer based LLM uses self-attention followed by a feed-forward neural network = we call this a dense model because everything is activated

![[Pasted image 20261028190719.png]]

In a dense Transformer block, the feed-forward neural network (FFNN) is active for every single token passing through

A sparse model, in contrast, may deploy several feed-forward neural networks instead.

These are typically smaller than a regular network, but together they tend to be bigger. Each feed-forward neural network in a sparse model is typically referred to as an “expert” because, during training, each “expert” learns different information and may specialize in the processing of certain tokens

For instance, one expert might be used for processing numbers, whereas another processes verbs. It’s still a bit unclear what these experts actually learn, but there has been some research suggesting that they specialize in fine-grained information such as 142 verbs versus numbers rather than each learning an entirely different domain

Note that in this example, all experts are used, which does not allow for any efficiency gains. To choose a subset of experts during inference, we make use of the router (also called a gate network)

This is a small feed-forward neural network that is trained to choose an expert for a given token. The router, together with the experts, makes up the MoE layer

The router is arguably the most important component because the experts are nothing more than just small feed-forward neural networks. So, how exactly does the router then choose which expert to use for each token?

![[Pasted image 20261028192633.png]]

![[Pasted image 20261028192644.png]]

The router, as a neural network, will have its own weight matrix, which is used to multiply the input token embeddings

Applying a softmax on the output will result in a probability distribution per expert. This probability distribution provides the likelihood that an expert will be chosen given an input token.

![[Pasted image 20261028192740.png]]


Note that any number of experts can be selected, but generally a fixed number are selected for training and inference. When selecting multiple experts, there is a need to balance how much each expert is trained. If the same set of experts is always chosen during training and inference, then all other experts are undertrained.

To balance the distribution of training among experts, the router will have to dynamically balance which expert to choose and when. This is referred to as load balancing.

To prevent one expert from dominating the training time, there are two main techniques that are often employed in one way or another:
- namely expert capacity 
- auxiliary loss

Expert capacity gives each expert in the MoE layer a limit to how many tokens it can process.
- Instead of having a single expert do all the work, the tokens are somewhat more equally distributed.
- For instance, by the time an expert has reached capacity, each subsequent token routed to it will be sent to the next-highest scoring expert

![[Pasted image 20261028192952.png]]

In contrast, instead of limiting the experts, the router can also be adjusted to account for this probability imbalance. A straightforward technique is to add Gaussian noise just before the router produces 149 its probabilities. By introducing noise, the distributions will slightly change, and by (slight) chance, sometimes choose different experts to use

A more advanced technique to balance how the router selects experts is called auxiliary loss

These are loss functions that can be added to the router to reward it for equally distributing the experts during training or punish it when the same expert is chosen.

The main benefit of MoE is its computational requirements. Although using MoE does not make the resulting model smaller, it runs much faster because only a few experts are activated at a given time.

all parameters that a MoE model has need to be loaded into memory and are called sparse parameters. The active parameters, in contrast, are those that are activated only during inference

![[Pasted image 20261028193141.png]]

In Deepseek R1 
Note that there is also a shared expert bypassing the router. This expert is always chosen, which often helps the model divert all general knowledge to that expert and more specialized knowledge to all others

![[Pasted image 20261028193227.png]]