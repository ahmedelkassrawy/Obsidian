---
description: "Hub: every note about Regression"
type: hub
domain: ml
tags:
  - type/hub
  - topic/regression
---
# Regression

> [!info] Linear, polynomial, Ridge, Lasso and Elastic Net with intuition and code. Well covered.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/regression`.

## Concepts
- [[Elastic Net Regression]] — Explains Elastic Net as the Lasso/Ridge blend: the combined penalty, when to use it, scikit-learn code, and its pros and cons.
- [[Lasso Regression]] — Explains Lasso regression: how the L1 penalty shrinks some coefficients to exactly zero, giving regularization and feature selection at once, with scikit-learn code.
- [[Learning Curves And Regularization]] — Reads learning curves to tell underfitting from overfitting, then explains L1/L2/elastic-net regularization and how to choose between them.
- [[Linear Regression]] — Covers simple and multiple linear regression with scikit-learn code, plotting the fit, and the overfitting risk that comes with adding features.
- [[Regression Trees]] — Explains how regression trees predict continuous values, the variance/MSE splitting criterion, and how they differ from classification trees, with scikit-learn code.
- [[Ridge Regression]] — Explains Ridge regression: the L2 penalty shrinks coefficients without zeroing them, how it differs from Lasso, and scikit-learn code.
- [[SVM]] — Full walkthrough of SVMs: maximum-margin intuition, linear and kernel SVMs, the soft-margin C parameter, SVR for regression, and OneClassSVM for outliers, with scikit-learn code.
- [[Polynomial Regression And Error Metrics]] `raw` — Rough lecture dump on polynomial regression being linear in its parameters, the cost function, and the common regression error metrics.

## How-tos & recipes
- [[01. PyTorch Workflow Fundamentals]] — The standard PyTorch workflow end to end: prepare and split data, build an nn.Module, train with a loss and optimizer, evaluate, then save and load the model.
- [[PyTorch Linear, Logistic]] — Trains linear and logistic models in PyTorch by hand: define nn.Linear, MSE loss, an SGD optimizer, and step through the training loop.
- [[Keras Build Fit Evaluate]] `raw` — Pasted Keras code for the build, fit and evaluate cycle on a regression model and a small CNN.

## References & cheat sheets
- [[GoTo ML Regression]] — A go-to playbook for regression problems: the EDA-to-baseline workflow, which model to pick when, and which algorithms actually need feature scaling.

## Book notes
- [[Supervised.Regression - AI Book]] — Book-chapter notes on supervised regression: OLS linear regression, outlier handling, regression variants, parametric vs nonparametric algorithms, and decision trees for regression.

## Course notes
- [[Logistic Regression And Classification Basics]] — ML lecture 3: logistic regression as a classifier - the sigmoid mapping to probabilities, the decision boundary, and how it reuses the linear hypothesis.

## Related hubs
[[Evaluation Metrics]], [[Regularization & Overfitting]], [[Classification]], [[Trees & Boosting]], [[PyTorch]], [[Optimizers & Training]]

## Notes to self (from the audit)
- [[Polynomial Regression And Error Metrics]]: Filename says nothing about the content and the body is an unformatted paste - worth rewriting.
- [[Learning Curves And Regularization]]: Old name suggested evaluation metrics, but the note is about learning curves and regularization.
- [[GoTo ML Regression]]: Old filename had a stray apostrophe that breaks wikilinks.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
