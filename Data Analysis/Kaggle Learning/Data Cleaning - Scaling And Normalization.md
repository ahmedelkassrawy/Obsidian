---
description: "Explains the difference between scaling (changing the range) and normalization (changing the shape of the distribution), with min-max and Box-Cox as the examples."
domain: ml
type: concept
status: stub
tags:
  - domain/ml
  - type/concept
  - status/stub
  - topic/data-cleaning
  - topic/feature-engineering-and-pipelines
aliases:
  - "Data Cleaning.2 Scaling and Normalization"
  - "Data Cleaning.2"
  - "scaling vs normalization"
  - "min-max Box-Cox"
hubs:
  - "[[Data Cleaning]]"
  - "[[Feature Engineering & Pipelines]]"
---
- in **scaling**, you're changing the _range_ of your data, while
- in **normalization**, you're changing the _shape of the distribution_ of your data.

# Scaling

This means that you're transforming your data so that it fits within a specific scale, like 0-100 or 0-1.For example, you might be looking at the prices of some products in both Yen and US Dollars. One US Dollar is worth about 100 Yen, but if you don't scale your prices, methods like SVM or KNN will consider a difference in price of 1 Yen as important as a difference of 1 US Dollar!