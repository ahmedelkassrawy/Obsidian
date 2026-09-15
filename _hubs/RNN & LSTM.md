---
description: "Hub: every note about RNN & LSTM"
type: hub
domain: ml
tags:
  - type/hub
  - topic/rnn-and-lstm
---
# RNN & LSTM

> [!info] RNN, GRU and LSTM theory, tensor shapes, PyTorch and Keras builds, POS tagging and forecasting. Well covered but spread over four folders.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/rnn-and-lstm`.

## Concepts
- [[Recurrent Neural Networks (RNNs) and LSTMs]] — Explains what RNNs are for and how their memory works, then the Keras text pipeline (tokenize, pad, embed) and the exact input and output shapes an LSTM layer expects.
- [[Seq2Seq]] — Explains the encoder-decoder Seq2Seq architecture, the fixed-vector bottleneck problem, how attention fixes it, and how Seq2Seq compares to transformers.
- [[Stanford CS224n]] — A very long single-file NLP walkthrough from Bag of Words and TF-IDF through embeddings, RNNs and attention to BERT's encoder internals, with formulas and mermaid diagrams.
- [[Transformers]] — A synthesis note that stitches the transformer story together: why RNNs fell short, how attention fixed it, then embeddings, positional encoding, multi-head attention and the full stack.

## How-tos & recipes
- [[POS Tagging]] — Builds an RNN part-of-speech tagger in Keras on NLTK corpora: data prep, splits, tokenization, padding, one-hot labels, model, training and inference.
- [[RNN]] — Builds a character and token-level GRU language model from scratch: encoding text to ids, sliding-window datasets, dataloaders, embeddings, and predicting the next character.
- [[RNN Implementation Guide]] — Explains every parameter choice in a small LSTM text classifier - vocab size, embedding dim, LSTM units, dense layer, optimizer, epochs - and when to add more layers.
- [[RNN and LSTM]] — NLP in PyTorch with RNNs and LSTMs: preprocessing, spaCy tokenization, vocabulary building and numericalization, then an RNN question-answering model and an LSTM next-word predictor.
- [[LSTMS Forecasting]] `raw` — Walks through an LSTM stock-price forecast on TSLA data: scaling, building 60-step lookback windows, training, and inverse-transforming predictions.

## References & cheat sheets
- [[LSTM PyTorch]] `empty` — One-line reminder that BCELoss needs .squeeze() on the output while CrossEntropyLoss does not.
- [[LSTMS Adhocs]] `stub` — Scratch notes on picking LSTM hidden-unit counts (64/128/256), what the timestep dimension of input_shape means, and how to handle NAs in text fields.

## Course notes
- [[Seq2Seq And Neural Machine Translation]] — NLP lecture 4: how an RNN language model is trained layer by layer, RNN pros and cons, and the seq2seq encoder-decoder for neural machine translation.
- [[Sequence Modeling With RNNs]] — NLP lecture 3: the sequence-modelling task types (one-to-many, many-to-one, many-to-many), a comparison of ANN vs CNN vs RNN, and an RNN deep dive.

## Related hubs
[[TensorFlow & Keras]], [[NLP Preprocessing]], [[Transformers]], [[PyTorch]], [[Embeddings & Semantic Search]], [[Time Series]]

## Notes to self (from the audit)
- [[LSTMS Forecasting]]: BUG: the MinMaxScaler is fit on the whole series before the train/test split, which leaks test statistics into training - fit the scaler on the training slice only.
- [[Stanford CS224n]]: Not a raw lecture transcript despite the name - it is a 13.5k-word structured guide with 200+ headings and no CS224n lecture content. Too big for one note: split it per topic and rename.
- [[LSTM PyTorch]]: Only 11 words - fold this line into the PyTorch RNN/LSTM note instead of keeping a separate file.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
