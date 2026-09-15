---
description: "Map of Content for the Machine Learning domain"
type: moc
domain: ml
tags:
  - type/moc
  - domain/ml
---
# MOC - Machine Learning

This is the classical ML, deep learning, NLP and data analysis half of the vault: 146 notes from the Hands-On ML and Designing ML Systems books, the DEPI bootcamp lectures, Kaggle courses and a lot of PyTorch practice.
The strongest areas are supervised learning (regression, trees and boosting, clustering) and NLP - both have several digested notes plus working code.
MLOps and recommender systems read well but nothing here is wired to a pipeline that actually runs; MLflow and DVC are covered as commands only.
The biggest gaps are statistics (one note), evaluation metrics (mostly bare snippets with no interpretation), and time series (four overlapping notes, one with a real data-leakage bug).
About a third of the notes are raw pastes with no explanation - they carry status/raw so they are easy to find and rewrite. See 'Knowledge Gaps Audit 2026-09-15' for the full list.

**148 notes** — digested 103, raw 36, stub 8, stale 0, empty 1. Search tip: tag `#domain/ml`.

## Hubs
- [[Statistics]] (5) — Population vs sample, descriptive measures, the central limit theorem and hypothesis testing. Only one note - missing confidence intervals, p-value pitfalls and A/B test design.
- [[Pandas]] (23) — Everyday dataframe work: selection, apply and map, groupby, datetime handling. Three overlapping cheat-sheet notes that should be merged into one.
- [[Matplotlib]] (13) — A complete ten-part plotting series from line charts to live animations. All raw code - none of it explains when to pick which chart.
- [[Data Cleaning]] (10) — Missing values, dtype fixes, scaling vs normalization, date parsing and fuzzy-matching inconsistent text. Solid coverage; no note on outlier policy.
- [[Feature Engineering & Pipelines]] (15) — sklearn Pipelines, imputers, encoding and scaling decisions. Missing ColumnTransformer and custom transformers.
- [[Regression]] (14) — Linear, polynomial, Ridge, Lasso and Elastic Net with intuition and code. Well covered.
- [[Classification]] (20) — Logistic regression, KNN, SVM, Naive Bayes plus a go-to workflow playbook. Strong area.
- [[Trees & Boosting]] (11) — Decision trees, bagging and pasting, random forest, OOB, AdaBoost and gradient boosting. The deepest part of the ML side.
- [[Clustering & Dimensionality Reduction]] (11) — KMeans, DBSCAN/HDBSCAN, Gaussian mixtures, PCA and t-SNE. Missing hierarchical clustering and UMAP.
- [[Regularization & Overfitting]] (6) — New hub. Pulls together learning curves, L1/L2 penalties, dropout and early stopping, which currently sit in three different folders.
- [[Evaluation Metrics]] (21) — Confusion matrix, ROC and AUC, loss function tables and NLP metrics. Several notes are bare code with no interpretation - the weakest hub relative to how often it matters.
- [[Optimizers & Training]] (15) — SGD, momentum, Adam, learning-rate schedules, batch and layer norm, vanishing gradients. Good conceptual coverage.
- [[PyTorch]] (19) — Tensors, the standard workflow, Dataset and DataLoader, classification, CNN and RNN builds. The most hands-on cluster in the vault.
- [[TensorFlow & Keras]] (11) — Sequential models, tokenizer pipelines and transfer learning. Thinner than the PyTorch side and mostly pasted code.
- [[CNN]] (12) — Conv and pool mechanics, hyperparameters, a reusable trainer class and transfer learning. Missing object detection and segmentation entirely.
- [[RNN & LSTM]] (13) — RNN, GRU and LSTM theory, tensor shapes, PyTorch and Keras builds, POS tagging and forecasting. Well covered but spread over four folders.
- [[Transformers]] (22) — Attention, self vs cross attention, the full architecture walkthrough and BERT internals. Strong; the 13k-word CS224n note needs splitting.
- [[Transfer Learning]] (2) — New hub. Freezing backbones, fine-tuning heads, SetFit and MLM pretraining - currently split between the CNN, DEPI and NLP folders.
- [[NLP Preprocessing]] (17) — Tokenization (word, character, subword), stop words, stemming, lemmatization, padding and modern BERT tokenizers. Strong.
- [[Embeddings & Semantic Search]] (24) — BoW, TF-IDF, Word2Vec, sentence transformers, semantic search and ANN libraries. Bridges into the ai-eng RAG notes.
- [[Time Series]] (8) — Decomposition, stationarity, lag features, seasonality and LSTM forecasting. Four notes overlap heavily and one has a data-leakage bug - needs a cleanup pass.
- [[Recommender Systems]] (8) — Content-based filtering, collaborative filtering, two-tower retrieval with FAISS and the 3-stage pipeline. Surprisingly complete for a side topic.
- [[ML System Design]] (13) — Designing ML Systems chapters 1-4 and 8 plus an Instagram feed-ranking interview. Missing chapters 5-7 (feature engineering, model development, deployment).
- [[MLOps]] (22) — Maturity levels, CI/CD, serving a model as an API, ONNX, monitoring and LLMOps. Read, not practised.
- [[MLflow & DVC]] (6) — Experiment tracking, autolog, model registry, evaluation and DVC data versioning. Command-level coverage only.

Gaps: [[Knowledge Gaps Audit 2026-09-15]]. Back to [[00 Home]].
