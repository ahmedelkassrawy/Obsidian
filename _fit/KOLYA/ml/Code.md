# 📋 Presenter Summary — `streamlit_app.py`

---

## 🔍 What This App Does (One Sentence)

> A Streamlit web app that loads pre-trained LDA models and lets users input feature values manually to get a predicted class + class probabilities — for either the Iris or Breast Cancer dataset.

---

## 🏗️ App Architecture — 4 Layers

```
User picks dataset
      ↓
Load model (.joblib) + rebuild StandardScaler from training data
      ↓
User fills in feature values (sliders/inputs)
      ↓
Scale input → Predict → Show class + probabilities
```

---

## 📦 Key Components to Know

### 1. `DATASET_CONFIG` — the config dictionary

```python
DATASET_CONFIG = {
    "Iris":          { model_path: ..., loader: load_iris },
    "Breast Cancer": { model_path: ..., loader: load_breast_cancer },
}
```

- Centralizes everything per dataset in one place
- Adding a new dataset = just add a new entry here
- Models are expected as `.joblib` files **in the same folder as the script**

---

### 2. `load_model_and_scaler()` — the critical function

```python
@st.cache_resource   ← loads once, stays in memory across reruns
```

**What it does step by step:**

1. Finds the `.joblib` model file — raises a clear error if missing
2. Reloads the **same dataset** used during training
3. Performs the **exact same train/test split** (`random_state=42, stratify=y`)
4. Fits a `StandardScaler` on the training portion only ← _important detail_
5. Loads and returns: `model`, `scaler`, `dataset`

> **Why rebuild the scaler here instead of saving it?** Because it must match exactly what was used in the notebook. The same seed + same split = same scaler every time.

---

### 3. `predict_single()` — prediction pipeline

```python
row_scaled = scaler.transform(row.reshape(1, -1))
prediction = model.predict(row_scaled)[0]
probabilities = model.predict_proba(row_scaled)[0]
```

- Reshapes single input row to `(1, n_features)` before scaling
- Returns: dataset bundle, predicted class index, probability array

---

### 4. `main()` — the UI

|UI Element|What it does|
|---|---|
|`st.selectbox`|Switches between Iris / Breast Cancer|
|`st.columns(2)`|Splits feature inputs into 2 columns|
|`st.number_input`|One input per feature, pre-filled with the **dataset mean**|
|`st.button("Predict")`|Triggers prediction|
|`st.success`|Shows predicted class name|
|`st.dataframe`|Shows all class probabilities as a table|

---

## ⚠️ Important Details to Mention

|Detail|Why it matters|
|---|---|
|`@st.cache_resource`|Model loads **once** — fast on reruns|
|`stratify=y` in the split|Keeps class proportions equal — must match the training notebook exactly|
|Default values = dataset means|User sees realistic starting values, not zeros|
|`key=f"{dataset_name}_{feature_name}"`|Prevents input state collision when switching datasets|
|`model_path.exists()` check|Gives a clean error instead of a cryptic crash if `.joblib` is missing|

---

## 🔗 Dependencies

```
streamlit       — web UI
scikit-learn    — LDA model, StandardScaler, datasets, train_test_split
joblib          — loading the saved .joblib model files
numpy           — array reshaping for prediction input
pathlib         — cross-platform file path handling
```

---

## 📁 Required Files at Runtime

```
📂 same folder as streamlit_app.py
├── streamlit_app.py
├── iris_lda_model.joblib           ← must exist
└── breast_cancer_lda_model.joblib  ← must exist
```

If either `.joblib` file is missing, the app shows `st.error()` and halts gracefully with `st.stop()`.

---

## 🗣️ What to Say When Presenting

1. **Start with the purpose** — _"This app exposes two pre-trained LDA classifiers through a simple UI. The user doesn't need to know any ML — they just enter values and get a prediction."_
    
2. **Highlight the scaler decision** — _"Instead of saving the scaler separately, we rebuild it deterministically from the same split. Same seed, same data, same scaler — guaranteed."_
    
3. **Point out the caching** — _"`@st.cache_resource` means the model and scaler are loaded once per session, not on every click — keeping the app fast."_
    
4. **Walk the prediction flow** — _"Input → reshape → scale → predict → display class + probabilities. Five steps, all in `predict_single()`."_
    
5. **Mention extensibility** — _"Adding a third dataset is a one-entry change to `DATASET_CONFIG`. The rest of the app adapts automatically."_
    

---

## ✅ Quick Pre-Demo Checklist

- [ ] Both `.joblib` files are in the same directory as the script
- [ ] `streamlit`, `scikit-learn`, `joblib` are installed
- [ ] Run with: `streamlit run streamlit_app.py`
- [ ] Test switching between Iris and Breast Cancer — inputs should reset cleanly
- [ ] Test the Predict button with default values — should return a valid class