---
description: "Hub: every note about Feature Engineering & Pipelines"
type: hub
domain: ml
tags:
  - type/hub
  - topic/feature-engineering-and-pipelines
---
# Feature Engineering & Pipelines

> [!info] sklearn Pipelines, imputers, encoding and scaling decisions. Missing ColumnTransformer and custom transformers.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/feature-engineering-and-pipelines`.

## Concepts
- [[Anomaly Detection]] — Covers anomaly detection approaches (statistical, distance, density, tree-based), when to remove vs keep outliers, and how to feed an anomaly score back in as a feature.
- [[Data Leakage]] — Explains data leakage: the common causes (future information, preprocessing before the split, duplicate rows), the damage it does, and how to prevent it.
- [[Dimensionality Reduction]] — Explains PCA as projection onto the maximum-variance hyperplane with scikit-learn code and explained-variance selection, then contrasts it with t-SNE, LLE and other reducers.
- [[Random Forest]] — Explains Random Forest as bagged trees with random feature subsets, its key hyperparameters, Extra-Trees, and how to read feature importances.
- [[Data Cleaning - Scaling And Normalization]] `stub` — Explains the difference between scaling (changing the range) and normalization (changing the shape of the distribution), with min-max and Box-Cox as the examples.

## How-tos & recipes
- [[Time Series Kaggle]] — Kaggle's time series course notes: time-step and lag features, fitting trend with a DeterministicProcess, and modelling seasonality with Fourier terms.
- [[Pipelines]] `raw` — A worked scikit-learn Pipeline that chains an imputer with logistic regression, fitted and scored on a small synthetic dataset.

## References & cheat sheets
- [[GoTo ML Classification]] — A go-to playbook for classification problems: the EDA-to-baseline workflow, which model family fits which situation, and which metric to optimise.
- [[GoTo ML Regression]] — A go-to playbook for regression problems: the EDA-to-baseline workflow, which model to pick when, and which algorithms actually need feature scaling.
- [[ML Project Checklist]] — The eight-step checklist for running an ML project end to end, from framing the problem through data prep, model shortlisting, fine-tuning and presenting the solution.
- [[Hyperparameter Tuning]] `stub` — Two snippets for hyperparameter search: GridSearchCV and RandomizedSearchCV over a Ridge model with KFold cross-validation.

## Book notes
- [[Designing ML Systems Ch3 - Data Engineering]] — Chapter 3 notes on data engineering for ML: data sources, formats and serialization, row vs column storage, OLTP vs OLAP, and the ETL pipeline.
- [[Designing ML Systems Ch4 - Training Data]] — Chapter 4 notes on training data: probability vs nonprobability sampling, labeling strategies and weak supervision, handling missing labels, and dealing with class imbalance.

## Course notes
- [[Categorical Encoding And Feature Scaling]] — ML lecture 2: encoding categorical data (one-hot vs label encoding and their dimensionality trade-off), then min-max normalization vs z-score standardization.
- [[Curse Of Dimensionality And PCA]] — ML lecture 6: the curse of dimensionality and data sparsity, then PCA step by step - standardize, fit, and visualize the 2D projection.

## Related hubs
[[Data Cleaning]], [[ML System Design]], [[Clustering & Dimensionality Reduction]], [[Evaluation Metrics]], [[Classification]], [[MLOps]]

## Notes to self (from the audit)
- [[Hyperparameter Tuning]]: Code only - no guidance on picking the search space.
- [[GoTo ML Regression]]: Old filename had a stray apostrophe that breaks wikilinks.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
