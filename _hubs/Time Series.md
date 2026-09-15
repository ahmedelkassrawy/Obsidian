---
description: "Hub: every note about Time Series"
type: hub
domain: ml
tags:
  - type/hub
  - topic/time-series
---
# Time Series

> [!info] Decomposition, stationarity, lag features, seasonality and LSTM forecasting. Four notes overlap heavily and one has a data-leakage bug - needs a cleanup pass.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/time-series`.

## Concepts
- [[Pandas Time Series Cookbook]] — Explains what a time series is from the statistics and dynamic-system points of view, and walks through additive/multiplicative decomposition, stationarity and classical forecasting.
- [[Pandas Time Series Cookbook]] — Explains time series from the statistics and dynamic-system views, then covers decomposition models, stationarity, autocorrelation and classical forecasting.
- [[Time Series Basics And Naive Forecasting]] `stub` — Explains univariate vs multivariate time series, weekly seasonality, and why naive forecasting (copy last week's value) is a strong baseline.

## How-tos & recipes
- [[Time Series Kaggle]] — Kaggle's time series course notes: time-step and lag features, fitting trend with a DeterministicProcess, and modelling seasonality with Fourier terms.
- [[8.Plotting Time Series Data]] `raw` — Plotting dates in matplotlib: plot_date, sorting by date, rotating labels with autofmt_xdate and formatting the axis with DateFormatter.
- [[Data Cleaning - Dates And Times]] `stub` — Parsing date columns in pandas: the strftime format codes, pd.to_datetime, and pulling day-of-month out of a parsed date.
- [[LSTMS Forecasting]] `raw` — Walks through an LSTM stock-price forecast on TSLA data: scaling, building 60-step lookback windows, training, and inverse-transforming predictions.

## References & cheat sheets
- [[Pandas Time Series Cookbook]] `raw` — Pandas datetime cookbook: date_range, day attributes, to_datetime, setting a DatetimeIndex, partial string indexing and resampling.

## Related hubs
[[Pandas]], [[Statistics]], [[RNN & LSTM]], [[TensorFlow & Keras]], [[Data Cleaning]], [[Matplotlib]]

## Notes to self (from the audit)
- [[Pandas Time Series Cookbook]]: Byte-identical duplicate of 'Ai & ML/ML/Time Series.md' (only line endings differ) - keep the ML/ copy.
- [[LSTMS Forecasting]]: BUG: the MinMaxScaler is fit on the whole series before the train/test split, which leaks test statistics into training - fit the scaler on the training slice only.
- [[Pandas Time Series Cookbook]]: A byte-identical copy sat at 'Ai & ML/Time Series.md'; that one is being inboxed and this is the keeper.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
