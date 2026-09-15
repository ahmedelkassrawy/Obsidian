---
description: "Hub: every note about Regularization & Overfitting"
type: hub
domain: ml
tags:
  - type/hub
  - topic/regularization-and-overfitting
---
# Regularization & Overfitting

> [!info] New hub. Pulls together learning curves, L1/L2 penalties, dropout and early stopping, which currently sit in three different folders.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/regularization-and-overfitting`.

## Concepts
- [[Decision Trees]] — Explains how a decision tree splits, when to stop growing it, and which regularization hyperparameters (depth, min samples, leaf nodes) control overfitting.
- [[Elastic Net Regression]] — Explains Elastic Net as the Lasso/Ridge blend: the combined penalty, when to use it, scikit-learn code, and its pros and cons.
- [[Lasso Regression]] — Explains Lasso regression: how the L1 penalty shrinks some coefficients to exactly zero, giving regularization and feature selection at once, with scikit-learn code.
- [[Learning Curves And Regularization]] — Reads learning curves to tell underfitting from overfitting, then explains L1/L2/elastic-net regularization and how to choose between them.
- [[Ridge Regression]] — Explains Ridge regression: the L2 penalty shrinks coefficients without zeroing them, how it differs from Lasso, and scikit-learn code.

## Course notes
- [[Deep Network Training - Vanishing Gradients And Optimizers]] — Deep learning lecture 2: how data flows through a deep network, the vanishing gradient problem, regularization against overfitting, and gradient descent variants and advanced optimizers.

## Related hubs
[[Regression]], [[Evaluation Metrics]], [[Trees & Boosting]], [[Optimizers & Training]]

## Notes to self (from the audit)
- [[Learning Curves And Regularization]]: Old name suggested evaluation metrics, but the note is about learning curves and regularization.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
