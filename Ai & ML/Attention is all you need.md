sentence -> tokenized to tokens(numbeers) known as token id and the seq len is the length of the sentence
vocab_size is the size of the list of words learned by the tokenzer while toknizing

inside input_embeddings, the module maps each word(represented as token id) to a dense vector of size d_model
self.embedding = nn.Embedding(vocab_size, d_model)

what happens at the forward function is that the input (vocab_size , d_model) is passed to the embedding model and then multiplied with the square root of the dimensions to scale the embeddings 
if the embeddings are not scalled 
- positional encoding will dominate beacuase the nn.Embeddings is just normal small random values
- model becomes harder to train

the x shape is (batch_size,seq_len)
the ouput of word embeddings is (batch_size,seq_len,d_model)

the positional encoding comes here since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.

so the positonal encoding precomputes 
PE shape = (1,max_seq_len,d_model)

at the forward function what we do is like the arch we just add the input which here is the (batch_size,seq_len,d_model) to be added to the pe of the same shape and seq_len (1,seq_len (of length same as input x),d_model)
x: (batch, seq_len, d_model)
pe: (1, seq_len, d_model)

Now each token vector contains:
semantic meaning (embedding) + information about its position (PE)

#### Feed forward
Each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically. This consists of two linear transformations with a ReLU activation in between.
**2-layer MLP** with a ReLU
Where:
- First linear layer **expands** dimension from `d_model` → `d_ff`
- Second linear layer **reduces** dimension from `d_ff` → `d_model`
Default values from original paper:
- d_model = 512
- d_ff = 2048
The feed forward network = 512 → 2048 → 512

Why expand then shrink dimensions?
Because:
- expanding to 2048 allows the model to learn **rich, nonlinear combinations** of features
- collapsing back to 512 keeps the model size manageable
- this acts like a per-token “neural network brain” inside each Transformer layer

#### Multi Head Attention
What is Attention?
- Attention is a mechanism that lets every word **look at (attend to)** every other word in the sentence and decide:
> “How much should I care about each other token when understanding this token?”

- It learns **relationships and dependencies** between words.

1. We create Query,Key,Values
	- Query : What am _I_ looking for?
	- Key: What do _I_ offer? What am I about?
	- Value My actual info/content
2. Splits into heads
	- Think of attention as a tool that helps each word look at the other words.
	- Having one attention mechanism means it can only learn ONE TYPE of relationship
	- Since language relationships are multi-dimensional 
	- we give the model multiple parallel attention mechanisms called **heads**
	- Each head gets its own Q,K,V therefore it learns to focus on diff patterns.
	- How are number of heads chosen? like the learning rate not too small or too large
	- Most important thinks is that num_heads divides d_model evenly
3. Computes attention 
4. Concatenates Heads
5. Applies w_o projection