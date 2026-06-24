**In deep learning, we often use the terms _embedding vectors_, _representations_, and _latent space_. What do these concepts have in common, and how do they differ?**
- Embedding vectors are representations of input data where similar items are close to each other.
- Latent vectors are intermediate representations of input data.
- Representations are encoded versions of the original input.

Embeddings
Embedding vectors, or _embeddings_ for short, encode relatively high-dimensional data into relatively low-dimensional vectors.

### Latent Space
_Latent space_ is typically used synonymously with _embedding space_, the space into which embedding vectors are mapped.

Similar items can appear close in the latent space; however, this is not a strict requirement. More loosely, we can think of the latent space as any feature space that contains features, often compressed versions of the original input features. These latent space features can be learned by a neural network, such as an autoencoder that reconstructs input images

### Representation
A _representation_ is an encoded, typically intermediate form of an input. For instance, an embedding vector or vector in the latent space is a representation of the input, as previously discussed. However, representations can also be produced by simpler procedures. For example, one-hot encoded vectors are considered representations of an input.

The key idea is that the representation captures some essential features or characteristics of the original data to make it useful for further analysis or processing.