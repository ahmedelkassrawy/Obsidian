Data leakage in machine learning occurs when information from outside the training dataset, which should not be available during model training, inadvertently influences the model. This leads to overly optimistic performance estimates during training or evaluation, but poor generalization to new, unseen data.

## Common Causes of Data Leakage

1. **Including Future Information**: Using data that would not be available at prediction time (e.g., including a target variable or future timestamps in features).
2. **Improper Data Splitting**: Allowing overlap between training, validation, and test sets, such as including the same or highly correlated samples across splits.
3. **Feature Engineering with Test Data**: Calculating features (e.g., normalization, scaling, or imputations) using the entire dataset, including test or validation data, before splitting.
4. **Target Leakage**: Including features that are derived from the target variable or are proxies for it, which would not be available in real-world predictions.
5. **Data Preprocessing Issues**: Applying transformations (e.g., encoding categorical variables) before splitting data, causing information from the test set to influence the training process.

## Examples

- **Credit Risk Model**: Including a feature like "loan default status" as a predictor, which directly reveals the target variable (whether the loan was defaulted).
- **Time-Series Forecasting**: Using future data points to predict past or current values, such as including next month's sales to predict this month's.
- **Image Classification**: Normalizing pixel values across the entire dataset (including test images) before splitting, allowing test data statistics to influence training.

## Consequences

- **Overfitting** to the training data.
- Inflated performance metrics (e.g., high accuracy or low error during evaluation) that don't hold in production.
- Models that fail to generalize to real-world scenarios.

## How to Prevent Data Leakage

1. **Proper Data Splitting**: Ensure training, validation, and test sets are mutually exclusive and mimic real-world conditions.
2. **Time-Aware Processing**: For time-series data, respect temporal order and avoid using future data in training.
3. **Pipeline Discipline**: Apply preprocessing (e.g., scaling, encoding) only on the training set and then transform the test set separately.
4. **Feature Selection**: Exclude features that contain or are derived from the target variable or are unavailable at prediction time.
5. **Cross-Validation**: Use proper cross-validation techniques, ensuring no data leakage occurs across folds.
6. **Simulate Real-World Conditions**: Design the training process to reflect how the model will be used in production.

By carefully structuring the data pipeline and ensuring that only relevant, realistic information is used during training, data leakage can be minimized, leading to more robust and reliable machine learning models.