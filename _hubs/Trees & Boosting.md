---
description: "Hub: every note about Trees & Boosting"
type: hub
domain: ml
tags:
  - type/hub
  - topic/trees-and-boosting
---
# Trees & Boosting

> [!info] Decision trees, bagging and pasting, random forest, OOB, AdaBoost and gradient boosting. The deepest part of the ML side.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/trees-and-boosting`.

## Concepts
- [[Bagging & Pasting]] — Explains bagging vs pasting (sampling with or without replacement), how bagging underpins Random Forest, and how that contrasts with XGBoost's sequential boosting.
- [[Boosting Methods]] — Deep dive on boosting: AdaBoost's reweighting, gradient boosting's residual fitting, and the practical differences between XGBoost, LightGBM and CatBoost.
- [[Decision Trees]] — Explains how a decision tree splits, when to stop growing it, and which regularization hyperparameters (depth, min samples, leaf nodes) control overfitting.
- [[Ensemble Learning]] — Explains why ensembles beat single models and demonstrates hard vs soft voting classifiers in scikit-learn.
- [[Out-of-Bag (OOB) Evaluation]] — Explains out-of-bag evaluation: the samples a bootstrap draw leaves out act as a free validation set, and how the OOB score compares to a held-out test score.
- [[Random Forest]] — Explains Random Forest as bagged trees with random feature subsets, its key hyperparameters, Extra-Trees, and how to read feature importances.
- [[Regression Trees]] — Explains how regression trees predict continuous values, the variance/MSE splitting criterion, and how they differ from classification trees, with scikit-learn code.

## Book notes
- [[Supervised.Regression - AI Book]] — Book-chapter notes on supervised regression: OLS linear regression, outlier handling, regression variants, parametric vs nonparametric algorithms, and decision trees for regression.

## Course notes
- [[Bagging And Boosting]] — ML lecture 7: ensemble methods split into bagging and boosting, with scikit-learn BaggingClassifier examples over trees and KNN plus feature importance.
- [[Decision Trees And Naive Bayes]] — ML lecture 4: how decision trees split using Gini impurity and entropy/information gain with worked calculations, then Gaussian Naive Bayes.

## Interviews
- [[ML Multiple Choice Questions]] — A set of multiple-choice ML questions with worked explanations - picking the right model for a scenario, metric choice, and common pitfalls.

## Related hubs
[[Evaluation Metrics]], [[Regression]], [[Classification]], [[Optimizers & Training]], [[Regularization & Overfitting]], [[Feature Engineering & Pipelines]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
