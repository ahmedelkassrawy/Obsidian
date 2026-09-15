---
description: "Code-only notes on adding a combined column, dropping columns, and splitting one column into two with str.split."
domain: cs
type: course
status: raw
tags:
  - domain/cs
  - type/course
  - status/raw
  - topic/pandas
aliases:
  - "Pandas.6 Adding OR Removing"
hubs:
  - "[[Pandas]]"
---
```python
df["first"] + " " + df["last"]
df["full_name"] = df["first"] + " " + df["last"] #creating a new column containg the full name of a person

df.drop(columns=["first","last"])
df["full_name"].str.split(" ") #getting a list containing the first and second name seperated by a comma
df["full_name"].str.split(" ", expand=True) #rather than giving u a list of the names seperated it gives u it in a table kind of dataframe indexed by 0 1 2 3

df[["fisrt","last"]] = df["full_name"].str.split(" ", expand=True)
#it assigns the table before to what we want

df.append({"first": "Tony"}, ignore_index = True) #it wil append Tony but will leave the other rows or columns with values of NaN
```