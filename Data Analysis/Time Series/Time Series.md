to create range of dates
```python
pd.date_range(start=" ",periods = num of days you want to have)
```

day attributes 
```python
day.dayofweek
day.day_name() 
```

converting strings into datetime series
```python
google.date = pd.to_datetime(google.date)
```

setting date as index
```python
google.set_index("date",inplace=True)
```

partial string indexing
```python
google["2015"].info || ["2015-3":"2016-2"] || google.loc["2016-3","price"]
```

Setting frequency
```python
google.asfreq("D") #Daily #"B" --> Buisness Days
```

Upsampling --> Higher frequency implies new dates --> more missing data

Parsing and indexing all in one in importing the csv file
```python
csv_reader = pd.read_csv("google.csv",parse_dates=["Dates"],index_col="Dates")
```

Moving data or Shifting them Forward or Backwards
```python
google["Shifted"] = google.price.shift(#periods = 1 by defualt)
google["Lagged"] = google.price.shift(periods = -1)
```

Calc of one periods percent change Xt/Xt-1
```python
google["change"] = google.price.div(google.shiffted) #dividing the prices by the shifted column
```

Calc diff in values Xt - Xt-1
```python
google["Diff"] = google.price.diff()
```

Calc Percent Change
```python
google["pct_change"] = google.price.pct_change().mul(100)
```

Subtract column from another
```python
yahoo.price.sub(yahoo.shifted_30)
```

```python
for year in ["2013", "2014", "2015"]: 
price_per_year = yahoo.loc[year, ["price"]].reset_index(drop=True)
price_per_year.rename(columns={"price": year}, inplace=True) 
prices = pd.concat([prices, price_per_year], axis=1)
```

- `yahoo.loc[year, ["price"]]` selects the "price" column from the `yahoo` DataFrame for the current year. The `.loc` accessor is used to select rows based on the label (in this case, `year`).
- `.reset_index(drop=True)` resets the index of the selected rows, which is useful to prevent the year from remaining part of the index.
- `price_per_year.rename(columns={"price": year}, inplace=True)` renames the "price" column to the corresponding year (e.g., "2013"). This way, each year's data will be stored in a separate column.
- `prices = pd.concat([prices, price_per_year], axis=1)` concatenates the current `price_per_year` data for the current year into the `prices` DataFrame along the columns (using `axis=1`).