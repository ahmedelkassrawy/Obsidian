---
description: "Hub: every note about Optimizers & Training"
type: hub
domain: ml
tags:
  - type/hub
  - topic/optimizers-and-training
---
# Optimizers & Training

> [!info] SGD, momentum, Adam, learning-rate schedules, batch and layer norm, vanishing gradients. Good conceptual coverage.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/optimizers-and-training`.

## Concepts
- [[BatchNorm]] — Compares batch normalization (per feature across the mini-batch) with layer normalization (per sample across features), why each helps training, and where to place them in PyTorch.
- [[Boosting Methods]] — Deep dive on boosting: AdaBoost's reweighting, gradient boosting's residual fitting, and the practical differences between XGBoost, LightGBM and CatBoost.
- [[Optimizers]] — Plain-English comparison of SGD, momentum, Adam/AdamW and friends: what each update rule does, why it helps, and when to reach for it.
- [[Metaheuristics and Optimization Algorithms]] `raw` — Arabic-language lecture notes on metaheuristic search: local search and its traps, and how algorithms with an escape step get out of local optima on routing problems.

## How-tos & recipes
- [[01. PyTorch Workflow Fundamentals]] — The standard PyTorch workflow end to end: prepare and split data, build an nn.Module, train with a loss and optimizer, evaluate, then save and load the model.
- [[PyTorch Linear, Logistic]] — Trains linear and logistic models in PyTorch by hand: define nn.Linear, MSE loss, an SGD optimizer, and step through the training loop.
- [[RNN Implementation Guide]] — Explains every parameter choice in a small LSTM text classifier - vocab size, embedding dim, LSTM units, dense layer, optimizer, epochs - and when to add more layers.
- [[CNN Trainer]] `raw` — A reusable PyTorch ModelTrainer class that wraps the train/validate loop, checkpoint saving and loading, and tqdm progress for CNN training.
- [[MLP Code]] `raw` — Pasted Keras code for building, compiling and training MLPs for image classification and regression, with brief notes on activations and output layers.
- [[Pytorch Basic Training]] `raw` — A short, runnable PyTorch training loop on a one-input regression model, with notes on what the loss function and optimizer each do.

## References & cheat sheets
- [[Loss Functions]] — A lookup table of common loss functions saying which are for classification, which for regression, and when to prefer each.
- [[MLP (Multilayer Perceptrons)]] — A decision guide for feed-forward networks: which loss to use per task type, what each optimizer family does, and rules of thumb for picking layer and neuron counts.

## Course notes
- [[Deep Network Training - Vanishing Gradients And Optimizers]] — Deep learning lecture 2: how data flows through a deep network, the vanishing gradient problem, regularization against overfitting, and gradient descent variants and advanced optimizers.
- [[Introduction To Deep Learning]] — Deep learning lecture 1: neurons and perceptrons, common activation functions, feedforward network architecture, and backpropagation with gradient descent.
- [[Transfer Learning And Training Callbacks]] — Deep learning lecture 3: reusing pretrained models by freezing early layers and fine-tuning the last ones, hyperparameter tuning, early stopping and model checkpointing.

## Related hubs
[[PyTorch]], [[CNN]], [[TensorFlow & Keras]], [[Regression]], [[Evaluation Metrics]], [[Trees & Boosting]]

## Notes to self (from the audit)
- [[Metaheuristics and Optimization Algorithms]]: Mostly Arabic shorthand with slide references and no figures - hard to use without the slides.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
