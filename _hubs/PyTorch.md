---
description: "Hub: every note about PyTorch"
type: hub
domain: ml
tags:
  - type/hub
  - topic/pytorch
---
# PyTorch

> [!info] Tensors, the standard workflow, Dataset and DataLoader, classification, CNN and RNN builds. The most hands-on cluster in the vault.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/pytorch`.

## Concepts
- [[Autoencoders, GANs, and Diffusion Models]] — Explains autoencoders as learned compression (undercomplete, denoising, variational) and how GANs and diffusion models differ as generative approaches.
- [[BatchNorm]] — Compares batch normalization (per feature across the mini-batch) with layer normalization (per sample across features), why each helps training, and where to place them in PyTorch.
- [[Self-Attention vs Cross-Attention]] — Explains Q/K/V with a library analogy, where self-attention and cross-attention each sit in a transformer, the PyTorch call patterns, and how masking differs between them.
- [[Attention is all you need]] `raw` — Running commentary on implementing the Transformer paper: token ids, nn.Embedding to d_model vectors, positional encoding and what each forward pass does.

## How-tos & recipes
- [[00. PyTorch Tensor Fundamentals]] — Beginner PyTorch tensor walkthrough: scalars, vectors, matrices, ndim and shape, random tensors, and basic tensor operations.
- [[01. PyTorch Workflow Fundamentals]] — The standard PyTorch workflow end to end: prepare and split data, build an nn.Module, train with a loss and optimizer, evaluate, then save and load the model.
- [[02. PyTorch Classification]] — PyTorch classification workflow: device-agnostic code, building the model, choosing loss and optimizer, turning logits into predictions, and improving the model.
- [[Building a Two-Tower Retrieval System with PyTorch and FAISS]] — Builds a two-tower retrieval model on MovieLens 1M in PyTorch: feature encoding, contrastive training with in-batch negatives, then serving the item tower through FAISS.
- [[Final Transfer Learning]] — Hands-on transfer learning in both Keras and PyTorch: load a pretrained backbone, freeze layers, add augmentation, and fine-tune for a custom image dataset.
- [[PyTorch Dataset , Dataloaders]] — Explains the three methods a PyTorch Dataset needs, how DataLoader batches and shuffles, and wires them into a training and testing loop.
- [[PyTorch Linear, Logistic]] — Trains linear and logistic models in PyTorch by hand: define nn.Linear, MSE loss, an SGD optimizer, and step through the training loop.
- [[RNN]] — Builds a character and token-level GRU language model from scratch: encoding text to ids, sliding-window datasets, dataloaders, embeddings, and predicting the next character.
- [[RNN and LSTM]] — NLP in PyTorch with RNNs and LSTMs: preprocessing, spaCy tokenization, vocabulary building and numericalization, then an RNN question-answering model and an LSTM next-word predictor.
- [[CNN Trainer]] `raw` — A reusable PyTorch ModelTrainer class that wraps the train/validate loop, checkpoint saving and loading, and tqdm progress for CNN training.
- [[CNN.Pytorch]] `raw` — Snippets for image work in PyTorch: ImageFolder datasets, torchvision transform pipelines, data augmentation and evaluation.
- [[Pytorch Basic Training]] `raw` — A short, runnable PyTorch training loop on a one-input regression model, with notes on what the loss function and optimizer each do.
- [[Pytorch NN]] `raw` — A long pasted PyTorch notebook covering a custom Dataset class, dataloaders, tabular classification, and the training and evaluation loops.

## References & cheat sheets
- [[MLP (Multilayer Perceptrons)]] — A decision guide for feed-forward networks: which loss to use per task type, what each optimizer family does, and rules of thumb for picking layer and neuron counts.
- [[LSTM PyTorch]] `empty` — One-line reminder that BCELoss needs .squeeze() on the output while CrossEntropyLoss does not.

## Related hubs
[[CNN]], [[Optimizers & Training]], [[RNN & LSTM]], [[Classification]], [[TensorFlow & Keras]], [[Transformers]]

## Notes to self (from the audit)
- [[Attention is all you need]]: Unformatted stream of notes with no headings - worth rewriting as prose with real code blocks.
- [[LSTM PyTorch]]: Only 11 words - fold this line into the PyTorch RNN/LSTM note instead of keeping a separate file.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
