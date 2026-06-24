Anomaly detection (Outlier detection) is the process of identifying data points, events, or observations that deviate significantly from the majority of the data

These “anomalies” often signal **rare but important** occurrences — like fraud, sensor failure, or system intrusion.
## ⚙️ 2. Main Approaches in Anomaly Detection

| Approach                            | Description                                                                                           | Example Algorithms                                            |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Statistical methods**             | Model normal data distribution and detect deviations.                                                 | Z-score, Gaussian models, Mahalanobis distance                |
| **Machine learning (unsupervised)** | Learn the structure of “normal” data, flag anything far from it.                                      | Isolation Forest, One-Class SVM, Autoencoders                 |
| **Supervised learning**             | Use labeled normal vs. anomalous data to train a classifier.                                          | Random Forest, XGBoost (if labeled anomalies exist)           |
| **Deep learning**                   | Learn compressed representations to reconstruct normal data; large reconstruction errors → anomalies. | Autoencoders, Variational Autoencoders, LSTMs for time series |
## 💡 3. Common Use Cases

| Domain                  | Use Case               | Anomaly                      |
| ----------------------- | ---------------------- | ---------------------------- |
| **Finance**             | Credit card fraud      | Unusual spending pattern     |
| **Cybersecurity**       | Intrusion detection    | Abnormal network traffic     |
| **Manufacturing / IoT** | Predictive maintenance | Sensor reading deviates      |
| **Healthcare**          | Disease detection      | Abnormal patient data        |
| **Web analytics**       | Server monitoring      | Spike in error rates         |
| **Data quality**        | Cleaning datasets      | Impossible or extreme values |

---
## 4. Key Concepts

- **Distance-based methods:** Compare distance from cluster centers or neighbors.
- **Density-based methods:** Low local density points → anomalies (e.g. DBSCAN, LOF).
- **Reconstruction-based:** If a model can’t reconstruct an input well, it’s likely abnormal (Autoencoders).
- **Isolation-based:** Anomalies are easier to isolate (Isolation Forest).
---
## 🧠 Step 1. Understand the situation

You have:
- A **classification problem** (e.g. predicting labels `0` or `1`),
- But your dataset includes **anomalies/outliers** — samples that don’t fit normal patterns.

👉 These could be:
- **Measurement errors or noise** (bad data you want to remove),
- **Rare but valid cases** (frauds, rare diseases — you want to _detect_, not delete),
- **Distribution shifts or mislabeled examples** (need correction).
So before doing anything, **understand the meaning of anomalies** in your domain.

## ⚙️ Step 2. Detect & analyze anomalies

You can use unsupervised detectors _before training_ your classifier to see which samples are suspicious.

Example using **Isolation Forest**:

`from sklearn.ensemble import IsolationForest import numpy as np  iso = IsolationForest(contamination=0.02, random_state=42) y_outlier = iso.fit_predict(X)   # -1 = anomaly, 1 = normal  mask = y_outlier != -1 X_clean, y_clean = X[mask], y[mask]   # remove anomalies`

Now you can:

- **Inspect** them (plot distributions, boxplots),
    
- **Decide** whether to drop, fix, or keep them.

## 🧹 Step 3. Choose your handling strategy

Let’s compare options.

| Situation                          | What to do                                                 | Why                               |
| ---------------------------------- | ---------------------------------------------------------- | --------------------------------- |
| **Data errors / noise**            | Remove detected outliers before training                   | Prevent model from learning noise |
| **Legit rare events** (e.g. fraud) | Keep them, maybe _oversample_ or _reweight_                | They matter to prediction         |
| **Unknown cause / uncertain**      | Train model with and without outliers, compare performance | Empirical check                   |

We’ll walk through a small, **step-by-step example** where we:
1. Detect anomalies using **IsolationForest**.
2. Add the **anomaly score** as a new feature.
3. Train a **RandomForestClassifier** with and without that feature to compare.

```python
iso = IsolationForest(contamination=0.05, random_state=42)
iso.fit(X_train)

# Add anomaly score (higher = more normal)
X_train_score = iso.decision_function(X_train)
X_test_score = iso.decision_function(X_test)

# Append as a new feature
X_train_aug = np.hstack([X_train, X_train_score.reshape(-1, 1)])
X_test_aug = np.hstack([X_test, X_test_score.reshape(-1, 1)])
```

```python
# Without anomaly feature
rf_plain = RandomForestClassifier(n_estimators=200, random_state=42)
rf_plain.fit(X_train, y_train)
y_pred_plain = rf_plain.predict(X_test)

# With anomaly score feature
rf_aug = RandomForestClassifier(n_estimators=200, random_state=42)
rf_aug.fit(X_train_aug, y_train)
y_pred_aug = rf_aug.predict(X_test_aug)

```

## 🧠 Step 6. Why This Works

The **anomaly score** gives the classifier an extra signal about:
- How _normal_ or _strange_ a sample is compared to the rest.
- Which samples might represent unusual but valid events (like fraud).

Random Forest can then **learn interactions** like:

> “If `amount > 5000` and `anomaly_score` is very low → likely fraud.”

So you’re combining **unsupervised anomaly detection** with **supervised classification**, which makes the model more robust and interpretable.