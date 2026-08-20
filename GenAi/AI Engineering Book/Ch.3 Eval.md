While I discuss evaluation in its own chapters, evaluation has to be considered in the context of a whole system, not in isolation.

Evalutation comes to aim to migtate risks and uncover oppurtunites
we first have to identify the places where the system is likely to fail and design the eval around them which my aoften require the redesigning of the system to enhance the visibility.

Evaluating foundation models is especially challenging because they are open-ended, and I’ll cover best practices for how to tackle these

First, the more intelligent AI models become, the harder it is to evaluate them. Most people can tell if a first grader’s math solution is wrong. Few can do the same for a PhD-level math solution. It’s easy to tell if a book summary is bad if it’s gibberish, but a lot harder if the summary is coherent. To validate the quality of a summary, you might need to read the book first.

Second the open edned nature of the  models make it more diffuclt than the ML models where you had to just check the ouput of the ML based on the output expected if its from a certain category or not

third is that most foundational models are treated as black boxes , we can only evaluate the model based on the input and output , we cant see the reasoning

Entropy
- how much information on average a token carries 
- the higher the entropy the more info each token carries, the more bits are needed to represent the token
- entropy measures how difficult it is to predict what comes next in a language

Cross Entropy 
- same as entropy but it measures the difficulty of the model to predict what comes next in this dataset.
model's cross entropy depends on two qualities:
1. training data predictability
2. how the distribution captured by the LLM diverges from the true distribution of the training data

Bits-per-Character and Bits-per-Byte
If the cross entropy of a language model is 6 bits, this language model needs 6 bits to represent each token.

Perplexity
- perplexity measures the amount of uncertainty it has when predicting the next token.
- Higher uncertainty means there are more possible options for the next token

More structured data gives lower expected perplexity -> since it is more predictable
The bigger the vocabulary, the higher the perplexity -> because more possible tokens
The longer the context length, the lower the perplexity -> the possible tokens possibility lowers

- perplexity of a model with respect to text measures how difficult it was for the model to predict the text
- perplexity is the lowest for texts that model has seen and memorized during training
- perplexity can be used to detect whether a text was in a model’s training data.

Exact Evaluation 
When evaluating models’ performance, it’s important to differentiate between exact and subjective evaluation. Exact evaluation produces judgment without ambiguity.

Functional Correctness
Functional correctness evaluation means evaluating a system based on whether it performs the intended functionality


1. Asking an evaluator to make the judgment whether two texts are the same
2. Exact match: whether the generated response matches one of the reference responses exactly 
3. Lexical similarity: how similar the generated response looks to the reference responses 
4. Semantic similarity: how close the generated response is to the reference responses in meaning (semantics)