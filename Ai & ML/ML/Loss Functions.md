---
description: "A lookup table of common loss functions saying which are for classification, which for regression, and when to prefer each."
domain: ml
type: reference
status: digested
tags:
  - domain/ml
  - type/reference
  - status/digested
  - topic/evaluation-metrics
  - topic/optimizers-and-training
aliases:
  - "loss function table"
  - "MSE MAE"
  - "cross entropy"
hubs:
  - "[[Evaluation Metrics]]"
  - "[[Optimizers & Training]]"
---
This table outlines the applicability of common loss functions to classification and regression problems.

| **Loss Function**                          | **Classification** | **Regression** |
|--------------------------------------------|---------------------|----------------|
| **Mean Square Error (MSE) / L2 Loss**      | ❌                  | ✔️             |
| **Mean Absolute Error (MAE) / L1 Loss**    | ❌                  | ✔️             |
| **Binary Cross-Entropy Loss / Log Loss**   | ✔️                  | ❌             |
| **Categorical Cross-Entropy Loss**         | ✔️                  | ❌             |
| **Hinge Loss**                              | ✔️                  | ❌             |
| **Huber Loss / Smooth MAE**                | ❌                  | ✔️             |
| **Log Loss**                                | ✔️                  | ❌             |

---

## 🔍 Notes

- **MSE and MAE** are best for regression tasks where outputs are continuous values.
- **Cross-Entropy** and **Log Loss** are standard for classification problems.
- **Hinge Loss** is used for "maximum-margin" classifiers like SVM.
- **Huber Loss** is robust for regression with outliers — a combination of MSE and MAE.

---

## 📌 Tips

- For binary classification, use **Binary Cross-Entropy**.
- For multi-class classification, use **Categorical Cross-Entropy**.
- For regression with outliers, **Huber Loss** can be more stable than MSE.



![[Pasted image 20250710152947.png]]

|                           |                                 |                             |                         |
| ------------------------- | ------------------------------- | --------------------------- | ----------------------- |
| Loss Function             | Applicability to Classification | Applicability to Regression | Sensitivity to Outliers |
| Mean Squared Error (MSE)  | ✖️                              | ✔️                          | High                    |
| Mean Absolute Error (MAE) | ✖️                              | ✔️                          | Low                     |
| Cross-Entropy             | ✔️                              | ✖️                          | Medium                  |
| Hinge Loss                | ✔️                              | ✖️                          | Low                     |
| Huber Loss                | ✖️                              | ✔️                          | Medium                  |
| Log Loss                  | ✔️                              | ✖️                          | Medium                  |
loss function -> CrossEntropyLoss
```python
_,predicted = torch.max(outputs.data,1)

n_samples += label.size(0)
n_correct += (predicted == labels).sum().item()

acc = 100 * n_correct / n_samples
```