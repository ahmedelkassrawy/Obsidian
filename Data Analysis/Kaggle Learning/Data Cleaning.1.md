```python
# Convert tire_sizes to integer
ride_sharing['tire_sizes'] = ride_sharing['tire_sizes'].astype('int')
  
# Set all values above 27 to 27
ride_sharing.loc[ride_sharing['tire_sizes'] > 27, 'tire_sizes'] = 27  

# Reconvert tire_sizes back to categorical
ride_sharing['tire_sizes'] = ride_sharing['tire_sizes'].astype('category')

# Print tire size description
print(ride_sharing['tire_sizes'].describe())
```

```python
# Convert ride_date to date
ride_sharing['ride_dt'] = pd.to_datetime(ride_sharing['ride_date']).dt.date
  
# Save today's date
today = dt.date.today()

# Set all in the future to today's date
ride_sharing.loc[ride_sharing['ride_dt'] > today, 'ride_dt'] = today
  
# Print maximum of ride_dt column
print(ride_sharing['ride_dt'].max())
```


## Handling Missing Values
1. Take a first look at the data
2. # How many missing data points do we have?
```python
import pandas as pd
import numpy as np

df_sum = df.isnull().sum() #returns the total of number of nulls in the data frame
all_cells = np.prod(sf_permits.shape) #takes the shape of the data frame and return the prod of it 
missing_cells = df_sum.sum() #returns the sum of the cells
percent_missing = (missing_cells / all_cells) * 100 
print(percent_missing) 
# Check your answer
q2.check()
```
3. # Figure out why the data is missing
4. #  Drop missing values: rows or columns
```python
# TODO: Your code here!
trial = df.dropna(axis = 0) #dropping rows 
#trial = -----(axis = 1) dropping columns
trial.head()

print(trial.shape)
```
5. # Fill in missing values automatically
```python
sf_permits.fillna(0) #filling all Nans with zeros but it will be float sine the Nan values are floats in the first place

sf_permits_with_na_imputed = sf_permits.fillna(method='bfill', axis=0).fillna(0)
#method backward fill in the rows using filling NaN values
```