---
description: "Hub: every note about Classification"
type: hub
domain: ml
tags:
  - type/hub
  - topic/classification
---
# Classification

> [!info] Logistic regression, KNN, SVM, Naive Bayes plus a go-to workflow playbook. Strong area.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/classification`.

## Concepts
- [[K Nearest Neighbor Algo]] — Grokking-style intro to K-nearest-neighbours: picking good features, classification vs regression, and the spam-filter example.
- [[KNN Algo]] — Explains K-Nearest Neighbours from intuition to mechanics, with scikit-learn code, an accuracy-vs-k curve, and the trade-offs of the algorithm.
- [[Logistic Regression]] — Explains logistic regression's sigmoid output and, in particular, how moving the decision threshold trades false positives against false negatives.
- [[SVM]] — Full walkthrough of SVMs: maximum-margin intuition, linear and kernel SVMs, the soft-margin C parameter, SVR for regression, and OneClassSVM for outliers, with scikit-learn code.

## How-tos & recipes
- [[02. PyTorch Classification]] — PyTorch classification workflow: device-agnostic code, building the model, choosing loss and optimizer, turning logits into predictions, and improving the model.
- [[Fine-Tuning Tutorial]] — A full fine-tuning tutorial on Rotten Tomatoes sentiment: loading data, BERT setup, freezing layers to save compute, few-shot SetFit, and masked-language-model pretraining.
- [[NLP]] — An end-to-end NLP guide with code: lowercasing, stop words, tokenization, stemming vs lemmatization, n-grams, feature extraction, model training and saving.
- [[PyTorch Linear, Logistic]] — Trains linear and logistic models in PyTorch by hand: define nn.Linear, MSE loss, an SGD optimizer, and step through the training loop.
- [[Text Classification]] — Four ways to classify text: sentence-transformer embeddings plus logistic regression, zero-shot cosine similarity against label embeddings, and a T5 generative classifier.
- [[Pipelines]] `raw` — A worked scikit-learn Pipeline that chains an imputer with logistic regression, fitted and scored on a small synthetic dataset.
- [[Pytorch NN]] `raw` — A long pasted PyTorch notebook covering a custom Dataset class, dataloaders, tabular classification, and the training and evaluation loops.

## References & cheat sheets
- [[GoTo ML Classification]] — A go-to playbook for classification problems: the EDA-to-baseline workflow, which model family fits which situation, and which metric to optimise.
- [[Confusion Matrix]] `stub` — Minimal snippet showing how to print a confusion matrix and classification report for a fitted scikit-learn classifier.
- [[ROC And AUC]] `raw` — Snippets for producing predicted probabilities, plotting a ROC curve and computing AUC with scikit-learn.

## Book notes
- [[Text Classification - AI Book]] — Book-chapter notes on text classification: turning a corpus into vectors with CountVectorizer and TfidfVectorizer, then training and scoring a classifier on that matrix.

## Course notes
- [[Decision Trees And Naive Bayes]] — ML lecture 4: how decision trees split using Gini impurity and entropy/information gain with worked calculations, then Gaussian Naive Bayes.
- [[KNN And SVM]] — ML lecture 5: KNN as a non-parametric lazy learner and the steps it takes to classify, then the SVM maximum-margin idea.
- [[Logistic Regression And Classification Basics]] — ML lecture 3: logistic regression as a classifier - the sigmoid mapping to probabilities, the decision boundary, and how it reuses the linear hypothesis.
- [[Text Representation - BoW TF-IDF And N-Grams]] — NLP lecture 2: turning text into numbers with Bag of Words, N-grams, TF-IDF and one-hot encoding, worked by hand and then with sklearn vectorizers into a classifier.

## Interviews
- [[ML Multiple Choice Questions]] — A set of multiple-choice ML questions with worked explanations - picking the right model for a scenario, metric choice, and common pitfalls.

## Related hubs
[[Evaluation Metrics]], [[Embeddings & Semantic Search]], [[NLP Preprocessing]], [[Regression]], [[PyTorch]], [[Feature Engineering & Pipelines]]

## Notes to self (from the audit)
- [[K Nearest Neighbor Algo]]: Sits in DSA/ but this is a machine-learning note, not a data-structures one - domain set to ml. Consider moving it next to the ML notes.
- [[Confusion Matrix]]: Code only, and nothing explains what the four cells mean - worth filling in. Old name also had a typo.
- [[Logistic Regression]]: Filed under the Regression folder but it is a classification note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
