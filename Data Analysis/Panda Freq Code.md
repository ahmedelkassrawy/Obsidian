```python
df.info()
```

```python
df.describe()
df.describe(include=["object", "bool"])
```

Sorting
```python
df.sort_values(by="column", ascending=False).head()
df.sort_values(by=["col1", "col2"], ascending=[True, False]).head()
```

```python
df.apply(np.max)
```

if we need to select all states starting with ‘W’
```python
df[df["State"].apply(lambda state: state[0] == "W")].head()
```

The `map` method can be used to **replace values in a column** by passing a dictionary of the form `{old_value: new_value}` as its argument:
```python
d = {"No": False, "Yes": True}
df["col"] = df["col"].map(d)
df.head()
```

```python
df = df.replace({"Voice mail plan": d})
df.head()
```

```python
df.groupby(by=grouping_columns)[columns_to_show].function()

columns_to_show = ["Total day minutes", "Total eve minutes", "Total night minutes"]
df.groupby(["Churn"])[columns_to_show].describe(percentiles=[])

columns_to_show = ["Total day minutes", "Total eve minutes", "Total night minutes"]
df.groupby(["Churn"])[columns_to_show].agg(["mean", "std", "min", "max"])
```