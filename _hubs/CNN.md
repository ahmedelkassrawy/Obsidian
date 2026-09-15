---
description: "Hub: every note about CNN"
type: hub
domain: ml
tags:
  - type/hub
  - topic/cnn
---
# CNN

> [!info] Conv and pool mechanics, hyperparameters, a reusable trainer class and transfer learning. Missing object detection and segmentation entirely.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/cnn`.

## Concepts
- [[Autoencoders, GANs, and Diffusion Models]] — Explains autoencoders as learned compression (undercomplete, denoising, variational) and how GANs and diffusion models differ as generative approaches.
- [[BatchNorm]] — Compares batch normalization (per feature across the mini-batch) with layer normalization (per sample across features), why each helps training, and where to place them in PyTorch.
- [[CNN]] — Explains the CNN building blocks with concrete tensor shapes: Conv2D filters, pooling layers, and how a typical CNN stack is assembled in Keras.

## How-tos & recipes
- [[Final Transfer Learning]] — Hands-on transfer learning in both Keras and PyTorch: load a pretrained backbone, freeze layers, add augmentation, and fine-tune for a custom image dataset.
- [[CNN Trainer]] `raw` — A reusable PyTorch ModelTrainer class that wraps the train/validate loop, checkpoint saving and loading, and tqdm progress for CNN training.
- [[CNN.Pytorch]] `raw` — Snippets for image work in PyTorch: ImageFolder datasets, torchvision transform pipelines, data augmentation and evaluation.
- [[Keras Build Fit Evaluate]] `raw` — Pasted Keras code for the build, fit and evaluate cycle on a regression model and a small CNN.
- [[Pytorch NN]] `raw` — A long pasted PyTorch notebook covering a custom Dataset class, dataloaders, tabular classification, and the training and evaluation loops.

## References & cheat sheets
- [[CNN HyperParameters]] `stub` — Short crib sheet on what padding, kernel size, stride and pooling each do to a CNN's activation maps.

## Course notes
- [[Introduction To Deep Learning]] — Deep learning lecture 1: neurons and perceptrons, common activation functions, feedforward network architecture, and backpropagation with gradient descent.
- [[Sequence Modeling With RNNs]] — NLP lecture 3: the sequence-modelling task types (one-to-many, many-to-one, many-to-many), a comparison of ANN vs CNN vs RNN, and an RNN deep dive.
- [[Transfer Learning And Training Callbacks]] — Deep learning lecture 3: reusing pretrained models by freezing early layers and fine-tuning the last ones, hyperparameter tuning, early stopping and model checkpointing.

## Related hubs
[[PyTorch]], [[Optimizers & Training]], [[TensorFlow & Keras]], [[Transfer Learning]], [[Clustering & Dimensionality Reduction]], [[Classification]]

## Notes to self (from the audit)
- [[CNN HyperParameters]]: Under 120 words - expand with a worked output-size calculation.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
