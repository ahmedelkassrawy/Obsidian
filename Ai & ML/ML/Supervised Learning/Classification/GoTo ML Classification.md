## 🔹 1. Understand the Problem
- Target variable is **categorical** (e.g. churn: Yes/No, disease: Positive/Negative).
- Business goal: accuracy vs recall vs precision vs F1 depends on the context.
- Data distribution: is it **balanced** or **imbalanced**

👉 Example: predicting whether a customer churns.

---

## 🔹 2. Workflow for Tackling a Classification Problem

### **EDA**

- Check class balance.
- Explore correlations between features and target.
- Visualize class separation (scatter plots, histograms).

---

### **Preprocessing**

- **Missing values**:
    - Numeric → median/mean (same as regression).
    - Categorical → mode or “missing” category.
    - Flag columns can still help.
- **Scaling/Normalization**:
    - Needed for distance-based methods (KNN, SVM, Logistic Regression, Neural Nets).
    - Not needed for tree-based methods.
- **Encoding Categorical Variables**:
    - OneHot, Target Encoding, or let CatBoost handle them natively.
---

### **Baseline**

- Start with a **dummy classifier** (predict most frequent class) to have a benchmark.
---

## 🔹 3. Models & When to Use Them

### **Linear Models**

- **Logistic Regression** → baseline, interpretable.
- Works well if features and target are linearly separable.
- Add **regularization** (L1 = feature selection, L2 = shrink coefficients).
---

### **Tree-based Models**
- **Decision Trees**: interpretable but can overfit.
- **Random Forests**: good general baseline.
- **Gradient Boosting (XGBoost, LightGBM, CatBoost)**: usually **SOTA for tabular classification**.
    - Handles mixed features, missing values, and non-linear interactions.
---
### **Distance-based**
- **KNN Classifier**: works with small datasets, but sensitive to scaling and high dimensions.
---
### **Support Vector Machines (SVM)**
- Strong for medium-sized datasets with clear boundaries.
- Needs scaling.
- Kernel trick makes it powerful for non-linear separation.
---
### **Neural Networks**
- Use only if you have **lots of data** or text/images.
- On small/medium tabular data, boosting usually beats them.
---
## 🔹 4. Evaluation Metrics

This is a big difference from regression:
- **Accuracy**: overall correctness.
- **Precision**: of predicted positives, how many are correct?
- **Recall**: of actual positives, how many did we catch?
- **F1 Score**: harmonic mean of precision & recall.
- **ROC-AUC**: how well model ranks classes.
- **PR-AUC**: for imbalanced datasets.
👉 Choice depends on problem. (Example: disease detection → recall is key; spam detection → precision matters).

---

## 🔹 5. Handling Imbalanced Data
- **Resampling**: SMOTE (oversample minority), undersample majority.
- **Class weights**: make errors on minority class more costly.
- **Specialized metrics**: use F1, ROC-AUC, PR-AUC instead of accuracy.
---
## 🔹 Rules of Thumb

- **Small dataset, interpretable needed** → Logistic Regression or Decision Tree.
- **Medium dataset, tabular** → Random Forest or Gradient Boosting.
- **Imbalanced data** → use class weights or resampling.
- **Large dataset, high-dimensional or unstructured** → Neural Nets.

```python
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
```