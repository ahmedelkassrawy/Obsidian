---
description: "A model that fits training data too closely memorizes noise; regularization deliberately makes it fit a bit worse so it does better on data it hasn't seen."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/regularization
  - topic/ml
hubs:
  - "[[Regularization & Overfitting]]"
created: 2026-10-01
---
# Regularization trades training fit for generalization

## The idea
Overfitting is when a model learns the noise in its training data along with the real pattern. Training error looks great and validation error is bad. Learning curves show it as a gap between the two lines.

Regularization adds pressure toward simpler models. L2 (Ridge) shrinks all weights a bit. L1 (Lasso) pushes some to exactly zero, which also picks features. Elastic Net mixes the two. Trees get limits on depth and leaf size. Neural nets use dropout, weight decay and early stopping. In every case you accept a slightly worse training score for a better score on new data.

## Example
A depth-30 decision tree hits 100% training accuracy and 70% on validation. Capping depth at 6 drops training accuracy to 88% and lifts validation to 85%. That's the trade working.

## Connects to
- [[Caching trades freshness for speed]] — a different field, but the same habit of asking what you give up to get what you want. Most good engineering answers sound like this.
- [[Exact nearest-neighbour search doesn't scale, so vector databases approximate]] — another case of accepting a slightly worse score on one measure for a big gain where it matters.

## Sources
- [[Learning Curves And Regularization]]
- [[Ridge Regression]]
- [[Lasso Regression]]
- [[Elastic Net Regression]]
- [[Decision Trees]]

## 30-second answer
> Regularization makes a model fit training data a bit less closely so it generalizes better. I spot overfitting from the train-validation gap in learning curves, then use L1/L2 penalties, tree depth limits, or dropout and early stopping, tuned on validation data.
