---
description: "Hub: every note about Pandas"
type: hub
domain: ml
tags:
  - type/hub
  - topic/pandas
---
# Pandas

> [!info] Everyday dataframe work: selection, apply and map, groupby, datetime handling. Three overlapping cheat-sheet notes that should be merged into one.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/pandas`.

## Concepts
- [[Time Series Basics And Naive Forecasting]] `stub` — Explains univariate vs multivariate time series, weekly seasonality, and why naive forecasting (copy last week's value) is a strong baseline.

## How-tos & recipes
- [[Data Cleaning - Inconsistent Text Entries]] — Fixing inconsistent text entries: inspecting unique values, normalizing case and whitespace, and using fuzzy matching to collapse near-duplicate strings.
- [[Time Series Kaggle]] — Kaggle's time series course notes: time-step and lag features, fitting trend with a DeterministicProcess, and modelling seasonality with Fourier terms.
- [[2.Bar Charts and Analyzing Data from CSVs]] `raw` — Bar charts in matplotlib: grouped bars with numpy index offsets, horizontal bars, and counting survey responses from a CSV.
- [[7.Scatterplots]] `raw` — Scatter plots in matplotlib: mapping a third variable to color with a colormap, sizing points, log axes and a colorbar, on YouTube trending data.
- [[8.Plotting Time Series Data]] `raw` — Plotting dates in matplotlib: plot_date, sorting by date, rotating labels with autofmt_xdate and formatting the axis with DateFormatter.
- [[Data Cleaning - Dates And Times]] `stub` — Parsing date columns in pandas: the strftime format codes, pd.to_datetime, and pulling day-of-month out of a parsed date.
- [[Data Cleaning - Missing Values And Dtypes]] `raw` — Kaggle data-cleaning exercise code: converting dtypes, clipping out-of-range values, capping future dates, and counting missing values.
- [[Data Visualization]] `raw` — A run of plotting snippets - line, scatter, histogram, heatmap, pairplot - using matplotlib and seaborn on sample and California housing data.
- [[EDA Notes]] `raw` — Copy-ready EDA snippets: describe/groupby summaries, feature binning, boxplots, KDE plots and a correlation heatmap, using the Titanic dataset.

## References & cheat sheets
- [[Pandas Basics Cheat Sheet]] — Cheat sheet for the basics: Series vs DataFrame, creating each, the quick inspection methods, and selecting columns.
- [[Panda Freq Code]] `raw` — Frequently used pandas one-liners: info and describe, sorting, apply and map, boolean filtering and groupby aggregation.
- [[Pandas Cheatsheet]] `raw` — A numbered list of basic pandas exploration calls (columns, dtypes, isnull().sum(), describe) repeated across the DonorsChoose dataset tables.
- [[Pandas Notes]] `raw` — Pandas working notes: series vs dataframe indexing, iterating with iterrows, assigning with .loc, and numpy array iteration.
- [[Pandas Time Series Cookbook]] `raw` — Pandas datetime cookbook: date_range, day attributes, to_datetime, setting a DatetimeIndex, partial string indexing and resampling.

## Course notes
- [[Pandas - Selecting Filtering And Indexing]] — Reading a CSV and getting around a DataFrame: shape/info/head, selecting columns, loc vs iloc, set_index and reset_index, and boolean filtering.
- [[Pandas - Adding And Removing Columns]] `raw` — Code-only notes on adding a combined column, dropping columns, and splitting one column into two with str.split.
- [[Pandas - Aggregation And Grouping]] `raw` — Code-only notes on aggregation: median and describe on the frame, value_counts, and grouping before aggregating.
- [[Pandas - Dates And Times]] `raw` — Code-only notes on parsing date columns with pd.to_datetime and a format string so timestamps are recognised.
- [[Pandas - Handling Missing Data]] `raw` — Code-only notes on missing data: the NaN/None/'NA' mess in a frame, and cleaning it with dropna and fillna.
- [[Pandas - Modifying Rows And Columns]] `raw` — Code-only notes on renaming columns in bulk (list assignment, comprehension, str.replace, rename) and updating row values.
- [[Pandas - Sorting Values]] `raw` — Code-only notes on sort_values: one column, descending, and multiple columns as tie-breakers.
- [[Pandas.7 Sorting]] `empty` — Two lines of sort_values - a truncated first copy of the sorting note.

## Related hubs
[[Matplotlib]], [[Time Series]], [[Data Cleaning]], [[Numpy]], [[Feature Engineering & Pipelines]]

## Notes to self (from the audit)
- [[Pandas.7 Sorting]]: Duplicate-of 'Pandas.7 Sorting 1' (which has the full version). 15 words, 109 bytes.
- [[Panda Freq Code]]: Overlaps heavily with 'Pandas Cheatsheet.md' (being inboxed) - merge the useful lines in here.
- [[Pandas Cheatsheet]]: Near-duplicate of 'Panda Freq Code.md' and hard-coded to one Kaggle dataset - merge the useful lines into that note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
