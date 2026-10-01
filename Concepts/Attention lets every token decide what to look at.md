---
description: "Self-attention lets each token weigh every other token when building its meaning, which fixed the RNN bottleneck but costs compute that grows with the square of sequence length."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/transformers
  - topic/llm-internals
hubs:
  - "[[Transformers]]"
  - "[[LLM Internals]]"
created: 2026-10-01
---
# Attention lets every token decide what to look at

## The idea
RNNs read text one token at a time and squeeze everything so far into one hidden state. Long-range information fades, and you can't parallelize. Seq2seq models made it worse by forcing the whole input through one fixed vector.

Attention fixes this. Each token makes a query ("what am I looking for?"), and every token offers a key ("what do I contain?") and a value ("what I'll pass on"). Compare the query to all keys, softmax the scores into weights, and take a weighted mix of the values. Every token can look directly at every other token, and it all runs in parallel.

The price: every token attends to every token, so compute and memory grow with the square of the sequence length. That's a big reason context windows have limits and why long prompts are slow and expensive.

## Example
In "The animal didn't cross the street because it was too tired", attention lets "it" put most of its weight on "animal", so its vector carries the right meaning.

## Connects to
- [[Embeddings turn meaning into distance]] — attention is what turns static word vectors into contextual ones.
- [[The context window is a budget, not a bucket]] — the quadratic cost is the hardware reason behind that budget.

## Sources
- [[Transformers]]
- [[Self-Attention vs Cross-Attention]]
- [[Seq2Seq]]
- [[Clipping - Self-Attention Explained (Article)]]

## 30-second answer
> Self-attention lets each token compute a weighted mix of all other tokens, using query-key similarity to set the weights and mixing the values. It replaced RNNs because it handles long-range links and parallelizes well. The cost is quadratic in sequence length.
