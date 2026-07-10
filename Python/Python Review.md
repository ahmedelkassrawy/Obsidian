## 1. Data Containers

### Lists

Lists are the "Swiss Army Knife" of Python. They are versatile and allow for easy modification.
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")         # Adds "orange" to the end
fruits.insert(1, "mango")       # Adds "mango" at index 1 (second position)
fruits.remove("banana")         # Removes the specific item "banana"
fruits.pop(2)                   # Removes the item at index 2
```

**Explanation:** * **Indexing:** Items are accessed via `0` (first) to `n-1`.
- **Mutablity:** Unlike tuples, you can change a list's size and contents after creation.
### Dictionaries

Dictionaries store data in **Key-Value pairs**, making them ideal for structured data like a database record.
```python
student = {"name": "Alice", "age": 20, "courses": ["Math", "Science"]}
student["age"] = 21             # Updates the existing key "age"
student["grade"] = "A"          # Adds a new key-value pair
```

**Explanation:** * **Lookup:** You don't use numbers to find data; you use the **Key** (e.g., `"name"`).
- **Uniqueness:** Keys must be unique, but multiple keys can share the same value.
---

## 2. Control Flow

### If-Else Statements

This is the basic decision-making structure.
```python
age = 17
if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
```

**Explanation:** Python evaluates the `if` condition. If it's `True`, the first block runs. If `False`, the `else` block acts as a "catch-all" and runs instead.

### If-Elif-Else (The Multi-Chain)

Use this when you have more than two possible outcomes.
```python
traffic_light = "yellow"
if traffic_light == "red":
    print("Stop")
elif traffic_light == "yellow":
    print("Slow down")
elif traffic_light == "green":
    print("Go")
else:
    print("Invalid signal")
```

**Explanation:** The program checks conditions from top to bottom. As soon as it finds one that is **True**, it executes that block and **skips the rest** of the chain.

### Nested If Statements

This involves placing one `if` statement inside another to handle multi-layered logic.
```python
has_discount = True
is_member = False

if has_discount:
    if is_member:
        print("You get a 20% discount.")
    else:
        print("You get a 10% discount.")
else:
    print("No discount available.")
```

**Explanation:** The inner `if/else` block only runs if the outer `if has_discount:` condition is met. This allows you to "drill down" into specific scenarios (e.g., checking if someone has a discount, then checking their specific member status).

```python
# This does the exact same thing
users_interactions_count = interactions_df.groupby('personId')['contentId'].nunique()
```

```python
users_with_enough_interactions_df = users_interactions_count_df[users_interactions_count_df >= 5].reset_index()[['personId']]
```

- **Step A:** `[... >= 5]` filters the Series. It keeps `User_A (10)` and `User_C (7)`.
- **Step B:** `.reset_index()` converts the Series into a DataFrame. The index (`personId`) becomes a column.
- **Step C:** `[['personId']]` selects just that column.

- **Result:** A **DataFrame** containing only the IDs: `['User_A', 'User_C']`.

```python
import numpy as np

# 1. Group and Sum
interactions_full_df = interactions_from_selected_users_df \
    .groupby(['personId', 'contentId'])['eventStrength'].sum() \
    .reset_index()

# 2. Apply Log Smoothing (Vectorized)
# np.log2(1 + x) replaces your custom function completely
interactions_full_df['eventStrength'] = np.log2(1 + interactions_full_df['eventStrength'])

# --- Verify ---
print(f"# of unique user/item interactions: {len(interactions_full_df)}")
print(interactions_full_df.head(10))
```

what is straify in train_test_split

`stratify` is a parameter in `train_test_split` that preserves the **proportion** of your target classes in both the training and testing datasets.

Think of it like cutting a Neapolitan ice cream (Chocolate, Vanilla, Strawberry).
- **Without Stratify (Random):** You might accidentally cut a slice that is 100% Chocolate. The person eating it won't know about Vanilla or Strawberry.
- **With Stratify:** You cut across all three flavors, ensuring the slice has the exact same ratio of Chocolate/Vanilla/Strawberry as the whole block.

### Visualizing the Difference

### Why is this critical?
Imagine you are building a fraud detection model:
- **95%** of transactions are Legal (Class 0).
- **5%** are Fraud (Class 1)

If you do a random split (`stratify=None`), you risk ending up with a Test Set that has **0% Fraud cases**. Your model will look perfect (100% accuracy) but will fail in the real world because it was never tested on fraud.

**Using `stratify=y` guarantees that:**
- **Train Set:** 95% Legal, 5% Fraud.
- **Test Set:** 95% Legal, 5% Fraud.