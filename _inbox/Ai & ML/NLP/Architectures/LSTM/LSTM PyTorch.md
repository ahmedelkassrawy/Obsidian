---
description: "One-line reminder that BCELoss needs .squeeze() on the output while CrossEntropyLoss does not."
domain: ml
type: reference
status: empty
tags:
  - domain/ml
  - type/reference
  - status/empty
  - topic/rnn-and-lstm
  - topic/pytorch
aliases:
  - "squeeze BCELoss"
hubs:
  - "[[RNN & LSTM]]"
  - "[[PyTorch]]"
---
- **Binary Classification (`BCELoss`)** → ✅ Use ' .squeeze( ) '
- **Multi-Class Classification (`CrossEntropyLoss`)** → ❌ No `.squeeze()`
