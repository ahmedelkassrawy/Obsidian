# 🧠 Logistic Regression Notes

## 📘 Overview

In logistic regression, predictions are made by applying a **threshold** (commonly `0.5`) to the predicted probability.

> ⚖️ **Threshold Tuning**  
> Adjusting this threshold controls the trade-off between **false positives** and **false negatives**.

- **High false positives** (e.g., misclassifying low-risk patients as high-risk):  
  🔺 **Increase the threshold** to require stronger evidence for positive classification.
- **Impact**:  
  ✅ Reduces false positives  
  ⚠️ May increase false negatives

---

## ⚙️ Key Concepts

### 🔁 Sigmoid Function
The logistic regression model uses the **sigmoid function** to map the output to a probability between 0 and 1.

---

## 🧪 Threshold Adjustment

- **Default threshold**: `0.5`
- **To reduce false positives**:  
  Increase the threshold (e.g., to `0.6`), requiring higher confidence before classifying as positive.
- **Trade-off**:  
  May lead to more false negatives (fewer true positives classified correctly).

---

## 🧱 Implementation (Scikit-learn)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Example
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict probabilities
y_proba = model.predict_proba(X_test)[:, 1]

# Apply custom threshold
import numpy as np
threshold = 0.6
y_pred = (y_proba >= threshold).astype(int)

# Evaluation
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))