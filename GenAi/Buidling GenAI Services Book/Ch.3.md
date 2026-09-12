In this chapter, you will learn the mechanisms of various GenAI models and how to serve them in a FastAPI application

how to preload models for efficiency, and how to use FastAPI features for service monitoring.

we will progressively build a FastAPI service using open source GenAI models that generate text, images, audio, and 3D geometries, all from scratch.

will show you how to serve models across a variety of modalities including:
- Language models based on the transformer neural network architecture
- Audio models in text-to-speech and text-to-audio services based on the aggressive transformer architecture
- Vision models for text-to-image and text-to-video services based on the Stable Diffusion and vision transformer architectures
- 3D models for text-to-3D services based on the conditional implicit function encoder and diffusion decoder architecture
---
### Language Models
we talk about langauge models including transformers and RNNs

Transformers VS RNNs
![[Pasted image 20260911184358.png]]

RNN models historically was used to learn patterns in sequential data such as "free text"
To process text, models chunk text into small pieces as a word or char called token that can be sequentially processed

RNNs maintain a memory store called a "state vector", which carries info from one token to the next throughout the full text sequence until the end.This means that by the time you go to the end of the text sequence , the impact fo early tokens on the state verctor is lot smaller compared to the most recent tokens

Ideally, every token should be as important as the other tokens in any text. However, as RNNs can only predict the next item in a sequence by looking at the items that came before, they struggle with this ideal in capturing long-range dependencies and modeling patterns in large chunks of texts. As a result, they effectively fail to remember or comprehend essential information or context in large documents. With the invention of transformers, recurrent or convolutional modeling could now be replaced with a more efficient approach. Since transformers don’t maintain a hidden state memory and leverage a new capability termed self-attention, they’re capable of modeling relationships between words, no matter how far apart they appeared in a sentence. This self-attention component allows the model to “place attention” on contextually relevant words within a sentence. While RNNs model relationships between neighboring words in a sentence, transformers map pairwise relationships between every word in the text.

![[Pasted image 20260911184841.png]]

What powers the self-attention system are specialized blocks called attention heads that capture pairwise patterns between words as attention maps

- A transformer model contains several attention heads distributed across its neural network layers.
- Each head computes its own attention map independently to capture relationships between words focusing on certain patterns in the inputs.
- Using multiple attention heads, the model can simultaneously analyze the inputs from various angles and contexts to understand complex patterns and dependencies within the data.

![[Pasted image 20260911185532.png]]

- RNNs also required extensive compute power to train, as the training process couldn’t be parallelized on multiple GPU due to the sequential nature of their training algorithms.

- Transformers, on the other hand, process words non-sequentially, so they can run attention mechanisms in parallel on GPUs.

The efficiency of the transformer architecture means that these models are more scalable as long as there is more data, compute power, and memory.

Serving LLMs still remains a challenge due to high memory requirements with requirements doubling if you need to train and fine-tune them on your own dataset. This is because the training process will require caching and reusing model parameters across training batches.

Processing Data:
Tokenization and embedding
Neural networks can’t process words directly as they’re big statistical models that function on numbers. To bridge that gap between language and numbers, you need to use tokenization. With tokenization, you break down text into smaller pieces that a model can process

Any piece of text must be first sliced into a list of tokens that represent words, syllables, symbols, and punctuations. These tokens are then mapped to unique numbers so that patterns can be numerically modeled. 

By providing a vector of input tokens to a trained transformer, the network can then predict the next best token to generate text, one word at a time

So what can you do after you tokenize some text? These tokens need to be processed further before a language model can process them

After tokenization, you need to use an embedder to convert these tokens into dense vectors of real numbers called embeddings, capturing semantic information (i.e., meaning of each token) in a continuous vector space.

![[Pasted image 20260911190145.png]]

![[Pasted image 20260911190215.png]]

After the embedding process, each token is assigned an embedding vector filled with n numbers. Each number in the embedding vector focuses on a dimension that represents a specific aspect of the token’s meaning

Training transformers Once you have a set of embedding vectors, you can train a model on your documents to update the values inside each embedding. During model training, the training algorithm updates the parameters of the embedding layers so that the embedding vectors describe the meaning of each token as close as possible within the input text.

Understanding how embedding vectors work can be challenging, so let’s try a visualization approach. Imagine you used a two-dimensional embedding vectors, meaning the vectors contained only two numbers. Then, if you plot these vectors, before and after model training, you will observe plots similar to Figure 3-7. The embedding vectors of tokens, or words, with similar meanings will be closer to each other

![[Pasted image 20260911190439.png]]

To determine the similarity between two words, you can compute the angle between vectors using a calculation known as cosine similarity.

Smaller angles imply higher similarity, representing similar context and meaning.

After training, the cosine similarity calculation of two embedding vectors with similar meanings will validate that those vectors are close to each other

![[Pasted image 20260911190538.png]]

Once you have a trained embedding layer, you can now use it to embed any new input text to the transformer model

Positional encoding A final step before forwarding the embedding vectors to the attention layers in the transformer network is to implement positional encoding. The positional encoding process produces the positional embedding vectors that then are summed with the token embedding vectors.

Since transformers process words simultaneously rather than sequentially, positional embeddings are needed to record the word order and context within the sequential data, like sentences. The resultant embedding vectors capture both meaning and positional information of words in the sentences before they’re passed to the attention mechanisms of the transformer. This process ensures attention heads have all the information they need to learn patterns effectively.

![[Pasted image 20260911191105.png]]

Autoregressive prediction
The transformer is an autoregressive (i.e., sequential) model as future predictions are based on the past values

![[Pasted image 20260911191249.png]]

The model receives input tokens that are then embedded and passed through the network to make the next best token prediction. This process repeats until a "<stop>" or end of sentence <eos> is generated

However there is a limit tot the number fo tokens that the mdoel can storre in the memory to generate the next token , this token limit is referred to as the model context window which is important factor during the model selection

If the context window limit is reached, the model simply discards the least recently used tokens. This means it can forget the least recently used sentences in documents or messages in a conversation

Short windows will lead to loss of information, difficulty maintaining conversations, and reduced coherence with the user query. 
On the other hand, long context windows have larger memory requirements and can lead to performance issues or slow services when scaling to thousands of concurrent users who are using your service.

In addition, you will need to consider the costs of relying on models with larger context windows as they tend to be more expensive due to increased compute and memory requirements. The correct choice will depend on your budget and user needs in your use case