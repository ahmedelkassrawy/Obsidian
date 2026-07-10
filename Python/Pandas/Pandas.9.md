```python
people = {
    'first': ['Corey', 'Jane', 'John', 'Chris', np.nan, None, 'NA'], 
    'last': ['Schafer', 'Doe', 'Doe', 'Schafer', np.nan, np.nan, 'Missing'], 
    'email': ['CoreyMSchafer@gmail.com', 'JaneDoe@email.com', 'JohnDoe@email.com', None, np.nan, 'Anonymous@email.com', 'NA'],
    'age': ['33', '55', '63', '36', None, None, 'Missing']
}

df.dropna() #Remove missing values.

df.dropna(axis="index",how="any")
#axis either index or columns
#for how it is chosed any to drop if any value in the row is missing or NaN
#it could be all and then it will check if the whole row is missing values or NaNs

df.dropna(axis="index",how="any",subset=["email"])
#it drops like the others but if the email section in a missing row is filled it will be kept
```
![[Pasted image 20240722193739.png]]

```python
df.isna()
#returns a dataframe showing true and false for na values

df.fillna("MISSING") #does as it spells

df.dtypes #showing the data types of the whole dataframe

df["age"].mean() #since it conatins na values we can't make a mean

type(np.nan) #its float

df["age"] = df["age"].astype(float) #converting datatypes
```

```python
#dealing with csvs
na_vals = ["NA","Missing"] #including the values we want to convert to na values in the csv
df = pd.read_csv('data/survey_results_public.csv', index_col="Respondent",na_values=na_vals) #the imp keyword (na_values=na_vals)

df ["YearsCode"] = df["YearsCode"].astype(float) #it didnt act as expected because of the Less than 1 year or More than 50 Years answers in the survey

df["YearsCode"].unique() #returns an array of the unique values
df["YearsCode"].replace("Less than 1 year",0,inplace=True)
df["YearsCode"].replace("More than 50 years",51,inplace=True)

df ["YearsCode"] = df["YearsCode"].astype(float)#now acts normally
```