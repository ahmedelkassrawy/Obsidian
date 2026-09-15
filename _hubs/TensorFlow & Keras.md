---
description: "Hub: every note about TensorFlow & Keras"
type: hub
domain: ml
tags:
  - type/hub
  - topic/tensorflow-and-keras
---
# TensorFlow & Keras

> [!info] Sequential models, tokenizer pipelines and transfer learning. Thinner than the PyTorch side and mostly pasted code.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/tensorflow-and-keras`.

## Concepts
- [[CNN]] — Explains the CNN building blocks with concrete tensor shapes: Conv2D filters, pooling layers, and how a typical CNN stack is assembled in Keras.
- [[Recurrent Neural Networks (RNNs) and LSTMs]] — Explains what RNNs are for and how their memory works, then the Keras text pipeline (tokenize, pad, embed) and the exact input and output shapes an LSTM layer expects.

## How-tos & recipes
- [[Final Transfer Learning]] — Hands-on transfer learning in both Keras and PyTorch: load a pretrained backbone, freeze layers, add augmentation, and fine-tune for a custom image dataset.
- [[NLP - AI BOOK]] — Shows the Keras text pipeline end to end: Tokenizer to sequences, stop-word removal, padding, an Embedding layer, and a TextVectorization-based classification model.
- [[POS Tagging]] — Builds an RNN part-of-speech tagger in Keras on NLTK corpora: data prep, splits, tokenization, padding, one-hot labels, model, training and inference.
- [[RNN Implementation Guide]] — Explains every parameter choice in a small LSTM text classifier - vocab size, embedding dim, LSTM units, dense layer, optimizer, epochs - and when to add more layers.
- [[Keras Build Fit Evaluate]] `raw` — Pasted Keras code for the build, fit and evaluate cycle on a regression model and a small CNN.
- [[LSTMS Forecasting]] `raw` — Walks through an LSTM stock-price forecast on TSLA data: scaling, building 60-step lookback windows, training, and inverse-transforming predictions.
- [[MLP Code]] `raw` — Pasted Keras code for building, compiling and training MLPs for image classification and regression, with brief notes on activations and output layers.

## References & cheat sheets
- [[MLP (Multilayer Perceptrons)]] — A decision guide for feed-forward networks: which loss to use per task type, what each optimizer family does, and rules of thumb for picking layer and neuron counts.
- [[LSTMS Adhocs]] `stub` — Scratch notes on picking LSTM hidden-unit counts (64/128/256), what the timestep dimension of input_shape means, and how to handle NAs in text fields.

## Related hubs
[[RNN & LSTM]], [[NLP Preprocessing]], [[CNN]], [[Optimizers & Training]], [[PyTorch]], [[Embeddings & Semantic Search]]

## Notes to self (from the audit)
- [[LSTMS Forecasting]]: BUG: the MinMaxScaler is fit on the whole series before the train/test split, which leaks test statistics into training - fit the scaler on the training slice only.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
