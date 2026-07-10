# Pandas Basics Cheat Sheet

Pandas has **two primary data structures**:
- **Series** → 1-dimensional (like a column / labeled array)
- **DataFrame** → 2-dimensional (table with rows & columns)

## 1. Creating a Series

```python
import pandas as pd

# From a list
series = pd.Series([10, 20, 30, 40, 50])
print(series)
```

```
0    10
1    20
2    30
3    40
4    50
dtype: int64
```

## 2. Creating a DataFrame

### From a dictionary

```python
data = {
    "Name": ["Alice", "Bob"],
    "Age": [25, 30],
    "City": ["New York", "Los Angeles"]
}

df = pd.DataFrame(data)
print(df)
```

```
    Name  Age         City
0  Alice   25     New York
1    Bob   30  Los Angeles
```

## 3. Quick Inspection Methods

```python
df.head()       # First 5 rows (or n rows: df.head(10))
df.info()       # Column names, types, non-null counts, memory
df.describe()   # Statistical summary (count, mean, std, min, max, quartiles)
numerical_cols = df.select_dtypes("number").columns
```

## 4. Selecting Columns

```python
df["Name"]          # → returns a Series
df[["Name", "Age"]] # → returns a DataFrame with selected columns
```

## 5. Filtering Rows (Boolean Indexing)

```python
# Rows where Age > 28
filtered_df = df[df["Age"] > 28]
print(filtered_df)
```

## 6. Label-based Selection with `.loc[]`

```python
# Rows 0–1, only Name and City columns
selected = df.loc[0:1, ["Name", "City"]]
```

> **Tip**: `.loc[]` uses **labels** (names/indices), `.iloc[]` uses **integer positions**

## 7. Adding / Modifying Columns

```python
# Add new column
df["Salary"] = [80000, 95000]

# Update existing column (vectorized)
df["Age"] = df["Age"] + 1

# Using apply() with custom function
def double_salary(x):
    return x * 2

df["Double Salary"] = df["Salary"].apply(double_salary)
```

## 8. Dropping Columns or Rows

```python
# Drop column
df = df.drop("City", axis=1)          # axis=1 → columns

# Drop row (by index)
df = df.drop(0, axis=0)               # axis=0 → rows
```

## 9. Handling Missing Values

```python
df_with_nan = pd.DataFrame({
    'A': [1, 2, None],
    'B': [4, None, 6]
})

df_with_nan.isnull()      # → boolean mask
df_with_nan.isna().sum()  # → count missing per column

# Fill missing values
df.fillna(0)
df.fillna({"A": -1, "B": 999})

# Drop rows with any missing value
df.dropna()
df.dropna(subset=["A"])   # only consider column A
```

## 10. Grouping & Aggregation

```python
df = pd.DataFrame({
    'Department': ['HR', 'IT', 'HR', 'IT'],
    'Salary': [50000, 60000, 45000, 80000]
})

# Group and calculate mean
df.groupby('Department')['Salary'].mean()

# Multiple aggregations
df.groupby('Department').agg({
    'Salary': ['mean', 'sum', 'count', 'max']
})
```

## 11. Sorting

```python
# Sort by one column
df.sort_values("Salary", ascending=False)

# Sort by multiple columns
df.sort_values(["Department", "Salary"], ascending=[True, False])
```

## 12. Adding Calculated Columns

```python
# 5% raise
df["Salary_After_Raise"] = df["Salary"] * 1.05

# Using numpy where (conditional column)
import numpy as np
df["Category"] = np.where(df["Salary"] >= 60000, "High", "Standard")
```

## 13. Working with Dates

```python
# Convert string to datetime
df["Joining_Date"] = pd.to_datetime(df["Joining_Date"])

# Filter by date
recent = df[df["Joining_Date"] > "2020-01-01"]

# Extract parts
df["Year"]  = df["Joining_Date"].dt.year
df["Month"] = df["Joining_Date"].dt.month
```

## 14. Exporting Data

```python
df.to_csv("employees_clean.csv", index=False)
df.to_excel("employees.xlsx", index=False, sheet_name="Staff")
```

> **Quick Reminder – Most Common Axis Values**
> - `axis=0` → **rows** (default for many operations)
> - `axis=1` → **columns**

