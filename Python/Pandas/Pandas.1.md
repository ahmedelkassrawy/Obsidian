```python 
df = pd.read_csv('data/survey_results_public.csv') 
df

df.shape #gives a tuple with the no.of columns,rows
df.info() #shows the type and kind of data type in each column

df.head() #outputs the first 5 data entries of the data frame
df.head(10) #first 10

df.tail() #output the last 5
df.tail(10) #output last 10
```

```python
import pandas as pd

people = {"first":["Corey","JAne","Joe"],
		 "last": ["Schafer","Doe","Doe"],
		 "email": ["CoreyMSchafer@gmail.com","JaneDoe@email.com","JohnDoe@email.com"]}


df = pd.DataFrame(people) #DataFrame built from a dict

df['email'] #ouputs the key email with the rows and columns indexed
df.email #same thing

type(df['email']) #pandas.core.series.series
```
A Series is basically a single column of rows other than that its called a Dataframe.

---

```python
df.iloc[row,column] #default

df.iloc[0] #fisrt row with all the columns
df.iloc[0,1] #row 0 but specify the column 1 values

df.iloc[[0,1]] #row 0,1 with all the columns

df.iloc[[0,1] , 2] #row 0,1 with the specified values of col 1

df.iloc[0:-1] #row starting from 0 to the before last row
```
`iloc`  is searching by integer location

---
`loc` searching by labels
### 1. Basic Selection
```python
df.loc[row label , column label]
```

| **Selection Type** | **Syntax**                        | **Result Type**                     |
| ------------------ | --------------------------------- | ----------------------------------- |
| **Single Label**   | `df.loc['viper']`                 | Returns a **Series**                |
| **List of Labels** | `df.loc[['viper', 'sidewinder']]` | Returns a **DataFrame**             |
| **Row & Column**   | `df.loc['cobra', 'shield']`       | Returns a **Scalar** (single value) |

---
### 2. Slicing and Filtering

Unlike standard Python slices, `.loc` is **inclusive** of both the start and the stop labels.

- **Label Slicing**
    Selects a range of rows for a specific column.
    ```python
    >>> df.loc['cobra':'viper', 'max_speed']
    cobra    1
    viper    4
    ```
    
- **Boolean Indexing**
    Filter rows based on a condition.
    ```python
    >>> df.loc[df['shield'] > 6]
                max_speed  shield
    sidewinder          7       8
    ```
    
- **Filtered Column Selection**
    Combine a condition with specific column labels to narrow your results.
    ```python
    >>> df.loc[df['shield'] > 6, ['max_speed']]
                max_speed
    sidewinder          7
    ```

---
### 3. Data Modification
You can use `.loc` to find and update values in a single step.

- **Mass Update via Condition**
    ```python
    # Set all values to 0 where shield strength exceeds 35
    >>> df.loc[df['shield'] > 35] = 0
    ```

> **Pro Tip:** If you need to select by integer position rather than labels, use `.iloc` instead.

```python
df.loc[df["first"].apply(len) > 4,:]
==
df[df["first"].apply(len) > 4]
```

```python
df.loc[df["first"].apply(len) > 4, "first"] = "Too Long"
==
df[df["first"].apply(len) > 4]["first"] = "Too Long"
```

---
## `set_index("email")`
This command moves a column into the **index position** (the far-left bolded column).

- **Why do it?** It makes lookups much faster. Instead of searching the whole table, Pandas can find a row by its "address" (the email) instantly.
    
- **The "Copy" vs. "Inplace" factor:**
    - `new_df = df.set_index("email")`: This keeps your original `df` the same and creates a brand-new version with the new index. This is generally preferred in modern Python to avoid "side effects."
        
    - `df.set_index("email", inplace=True)`: This modifies your existing `df` directly.
---
## 2. `reset_index()`

This is the "undo" button for `set_index`. It moves the index back into a regular column and replaces it with the default integers ($0, 1, 2, ...$).

- **Why do it?** You often reset the index after filtering or sorting data to make the row numbers clean again, or when you need to perform an operation that requires the index to be a normal column.
    
- **The `drop` parameter:** A common trick is `df.reset_index(drop=True)`. If you don't use `drop=True`, the old index becomes a new column. If you do use it, the old index is simply deleted.
---
### Filtering 
## 1. Basic Boolean Filtering

A "filter" in Pandas is a Series of `True` and `False` values. When you pass this to `df.loc[]`, it only keeps the `True` rows.

```python
# 1. Define the mask (Boolean Series)
filt = (df['last'] == 'Doe')

# 2. Apply the mask to the entire DataFrame
df[filt] 

# 3. Apply the mask and select specific columns
df.loc[filt, 'email']
```

---
## 2. Logical Operators (Multiple Conditions)

When combining filters, you must wrap each condition in **parentheses** `()` and use bitwise operators:
- `&` for **AND**
- `|` for **OR**
- `~` for **NOT** (The "opposite" of a filter)
```python
# AND condition
filt_and = (df['last'] == 'Doe') & (df['first'] == 'John')

# OR condition
filt_or = (df['last'] == 'Doe') | (df['first'] == 'John')

# NOT condition (Everything EXCEPT Doe/John)
df.loc[~filt_and, 'email']
```

---
## 3. Advanced Filtering Methods
For more complex data, Pandas provides built-in methods like `.isin()` and `.str.contains()`.

### The `.isin()` Method
Instead of writing multiple `|` (OR) conditions, use a list.

```python
countries = ['United States', 'India', 'United Kingdom', 'Germany', 'Canada']
filt = df['Country'].isin(countries)

df.loc[filt, 'Country']
```

### String Methods (`.str`)
When a column contains long strings or lists separated by characters (like `Python;Java;C++`), use `.str.contains()`.

```python
# na=False ensures that rows with missing data (NaN) don't break the filter
filt = df['LanguageWorkedWith'].str.contains('Python', na=False)

df.loc[filt, 'LanguageWorkedWith']
```

---
## 4. Practical Example: High Salary Search
You can combine filtering and column selection to create custom reports:

```python
# Define high salary threshold
high_salary = (df['ConvertedComp'] > 70000)

# Select specific columns for those high earners
df.loc[high_salary, ['Country', 'LanguageWorkedWith', 'ConvertedComp']]
```

### Quick Reference Table

|**Operator/Method**|**Description**|**Usage**|
|---|---|---|
|`&`|Both must be True|`(cond1) & (cond2)`|
|`\|`|Either can be True|`(cond1) \| (cond2)`|
|`~`|Invert the filter|`df.loc[~filt]`|
|`.isin(list)`|Match any item in a list|`df['col'].isin(['A', 'B'])`|
|`.str.contains()`|Find a substring|`df['col'].str.contains('text')`|
