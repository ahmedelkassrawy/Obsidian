---
description: "Hub: every note about Evaluation Metrics"
type: hub
domain: ml
tags:
  - type/hub
  - topic/evaluation-metrics
---
# Evaluation Metrics

> [!info] Confusion matrix, ROC and AUC, loss function tables and NLP metrics. Several notes are bare code with no interpretation - the weakest hub relative to how often it matters.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/evaluation-metrics`.

## Concepts
- [[Data Leakage]] — Explains data leakage: the common causes (future information, preprocessing before the split, duplicate rows), the damage it does, and how to prevent it.
- [[KNN Algo]] — Explains K-Nearest Neighbours from intuition to mechanics, with scikit-learn code, an accuracy-vs-k curve, and the trade-offs of the algorithm.
- [[Learning Curves And Regularization]] — Reads learning curves to tell underfitting from overfitting, then explains L1/L2/elastic-net regularization and how to choose between them.
- [[Logistic Regression]] — Explains logistic regression's sigmoid output and, in particular, how moving the decision threshold trades false positives against false negatives.
- [[NLP Concepts]] — Compares the main text-representation methods (BoW, TF-IDF, Word2Vec), then BERT vs sentence transformers, and BLEU vs ROUGE for evaluation.
- [[Out-of-Bag (OOB) Evaluation]] — Explains out-of-bag evaluation: the samples a bootstrap draw leaves out act as a free validation set, and how the OOB score compares to a held-out test score.
- [[Polynomial Regression And Error Metrics]] `raw` — Rough lecture dump on polynomial regression being linear in its parameters, the cost function, and the common regression error metrics.

## How-tos & recipes
- [[02. PyTorch Classification]] — PyTorch classification workflow: device-agnostic code, building the model, choosing loss and optimizer, turning logits into predictions, and improving the model.
- [[MLflow Evaluation]] — Shows what mlflow.evaluate generates automatically - classification and regression metrics, ROC and residual plots, custom metrics - and how to evaluate a plain prediction function.
- [[NLP Eval Code]] `raw` — Code for computing NLP metrics with the HuggingFace evaluate library: BLEU for translation, ROUGE for summarization and seqeval for NER, wired into a training loop.

## References & cheat sheets
- [[GoTo ML Classification]] — A go-to playbook for classification problems: the EDA-to-baseline workflow, which model family fits which situation, and which metric to optimise.
- [[Loss Functions]] — A lookup table of common loss functions saying which are for classification, which for regression, and when to prefer each.
- [[NLP Evaluation Metrics]] — Explains the evaluation metrics for generative NLP - perplexity, ROUGE variants, BLEU and METEOR - with formulas, examples and when each applies.
- [[Confusion Matrix]] `stub` — Minimal snippet showing how to print a confusion matrix and classification report for a fitted scikit-learn classifier.
- [[Hyperparameter Tuning]] `stub` — Two snippets for hyperparameter search: GridSearchCV and RandomizedSearchCV over a Ridge model with KFold cross-validation.
- [[ROC And AUC]] `raw` — Snippets for producing predicted probabilities, plotting a ROC curve and computing AUC with scikit-learn.

## Book notes
- [[Supervised.Regression - AI Book]] — Book-chapter notes on supervised regression: OLS linear regression, outlier handling, regression variants, parametric vs nonparametric algorithms, and decision trees for regression.

## Course notes
- [[Logistic Regression And Classification Basics]] — ML lecture 3: logistic regression as a classifier - the sigmoid mapping to probabilities, the decision boundary, and how it reuses the linear hypothesis.

## Interviews
- [[Data Drift and Concept Drift]] — The difference between data drift (inputs shift) and concept drift (the input-to-output relationship shifts), how each is detected, and why continuous training is the fix.
- [[Designing Instagram's Feed Ranking Model]] — A mock Meta ML system design interview: framing Instagram feed ranking, the 3-stage retrieval/ranking/re-rank pipeline, features, offline vs online metrics, and the model architecture.
- [[ML Multiple Choice Questions]] — A set of multiple-choice ML questions with worked explanations - picking the right model for a scenario, metric choice, and common pitfalls.

## Related hubs
[[Classification]], [[Regression]], [[Trees & Boosting]], [[Feature Engineering & Pipelines]], [[MLOps]], [[Embeddings & Semantic Search]]

## Notes to self (from the audit)
- [[Polynomial Regression And Error Metrics]]: Filename says nothing about the content and the body is an unformatted paste - worth rewriting.
- [[Learning Curves And Regularization]]: Old name suggested evaluation metrics, but the note is about learning curves and regularization.
- [[Confusion Matrix]]: Code only, and nothing explains what the four cells mean - worth filling in. Old name also had a typo.
- [[Hyperparameter Tuning]]: Code only - no guidance on picking the search space.
- [[Logistic Regression]]: Filed under the Regression folder but it is a classification note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
