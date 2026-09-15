---
description: "Hub: every note about Clustering & Dimensionality Reduction"
type: hub
domain: ml
tags:
  - type/hub
  - topic/clustering-and-dimensionality-reduction
---
# Clustering & Dimensionality Reduction

> [!info] KMeans, DBSCAN/HDBSCAN, Gaussian mixtures, PCA and t-SNE. Missing hierarchical clustering and UMAP.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/clustering-and-dimensionality-reduction`.

## Concepts
- [[Anomaly Detection]] — Covers anomaly detection approaches (statistical, distance, density, tree-based), when to remove vs keep outliers, and how to feed an anomaly score back in as a feature.
- [[Autoencoders, GANs, and Diffusion Models]] — Explains autoencoders as learned compression (undercomplete, denoising, variational) and how GANs and diffusion models differ as generative approaches.
- [[DBSCAN , HDBSCAN]] — Explains density-based clustering: DBSCAN's eps/minPts and noise points, how HDBSCAN removes the eps guess, and code on non-spherical data.
- [[Dimensionality Reduction]] — Explains PCA as projection onto the maximum-variance hyperplane with scikit-learn code and explained-variance selection, then contrasts it with t-SNE, LLE and other reducers.
- [[Gaussian Mixtures]] — Explains Gaussian Mixture Models as soft, ellipse-shaped clustering, how they beat k-means on non-spherical data, and their use for anomaly detection.
- [[KMeans]] — Explains k-means intuitively - assign, recompute centroid, repeat - with scikit-learn code and its main strengths and weaknesses.
- [[Unsupervised Tasks]] — Surveys what unsupervised learning is used for - clustering, anomaly detection, dimensionality reduction, semi-supervised labelling - with k-means and DBSCAN as the worked examples.

## How-tos & recipes
- [[Clustering]] `raw` — Code snippets for k-means: sweeping k to build an elbow plot from inertia, and plotting centroid movement across iterations.

## Book notes
- [[Unsupervised Learning - AI Book]] — Book-chapter notes on unsupervised learning: what clustering is for, how k-means iterates centroids, and how to pick the number of clusters.

## Course notes
- [[Curse Of Dimensionality And PCA]] — ML lecture 6: the curse of dimensionality and data sparsity, then PCA step by step - standardize, fit, and visualize the 2D projection.
- [[KMeans And DBSCAN]] — ML lecture 8: distance metrics and centroids, the k-means loop and how to choose k, then DBSCAN's core, border and noise points and its advantages.

## Related hubs
[[Feature Engineering & Pipelines]], [[PyTorch]], [[CNN]], [[Matplotlib]], [[Statistics]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
