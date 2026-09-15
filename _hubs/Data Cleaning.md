---
description: "Hub: every note about Data Cleaning"
type: hub
domain: ml
tags:
  - type/hub
  - topic/data-cleaning
---
# Data Cleaning

> [!info] Missing values, dtype fixes, scaling vs normalization, date parsing and fuzzy-matching inconsistent text. Solid coverage; no note on outlier policy.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/data-cleaning`.

## Concepts
- [[Data Leakage]] — Explains data leakage: the common causes (future information, preprocessing before the split, duplicate rows), the damage it does, and how to prevent it.
- [[Data Cleaning - Scaling And Normalization]] `stub` — Explains the difference between scaling (changing the range) and normalization (changing the shape of the distribution), with min-max and Box-Cox as the examples.

## How-tos & recipes
- [[Data Cleaning - Inconsistent Text Entries]] — Fixing inconsistent text entries: inspecting unique values, normalizing case and whitespace, and using fuzzy matching to collapse near-duplicate strings.
- [[Data Cleaning - Dates And Times]] `stub` — Parsing date columns in pandas: the strftime format codes, pd.to_datetime, and pulling day-of-month out of a parsed date.
- [[Data Cleaning - Missing Values And Dtypes]] `raw` — Kaggle data-cleaning exercise code: converting dtypes, clipping out-of-range values, capping future dates, and counting missing values.
- [[EDA Notes]] `raw` — Copy-ready EDA snippets: describe/groupby summaries, feature binning, boxplots, KDE plots and a correlation heatmap, using the Titanic dataset.

## References & cheat sheets
- [[LSTMS Adhocs]] `stub` — Scratch notes on picking LSTM hidden-unit counts (64/128/256), what the timestep dimension of input_shape means, and how to handle NAs in text fields.

## Book notes
- [[Designing ML Systems Ch3 - Data Engineering]] — Chapter 3 notes on data engineering for ML: data sources, formats and serialization, row vs column storage, OLTP vs OLAP, and the ETL pipeline.
- [[Designing ML Systems Ch4 - Training Data]] — Chapter 4 notes on training data: probability vs nonprobability sampling, labeling strategies and weak supervision, handling missing labels, and dealing with class imbalance.

## Course notes
- [[Categorical Encoding And Feature Scaling]] — ML lecture 2: encoding categorical data (one-hot vs label encoding and their dimensionality trade-off), then min-max normalization vs z-score standardization.

## Related hubs
[[Feature Engineering & Pipelines]], [[Pandas]], [[ML System Design]], [[Matplotlib]], [[RNN & LSTM]], [[TensorFlow & Keras]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
