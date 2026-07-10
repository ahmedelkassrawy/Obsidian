series --> []
dataframe --> [[]]

```python
# Assert that all values in 'drives_right' are True in the 'sel' DataFrame
assert sel["drives_right"].all()
```

dict --> for key,val in my_dict.items()
numpy array --> for val in np.nditer(my_array)

```python
for label , row in cars.iterrows(): 
cars.loc[label,"COUNTRY"] = row["country"].upper()
#Why do i have to put label in the loc argument?
#`cars.iterrows()`**: This method iterates over the DataFrame rows as (index, Series) pairs. 
#Here, `label` represents the index (or label) of the row, and `row` is a Series containing the row's data.

#`cars.loc[label, "COUNTRY"]`**: The `.loc` method is used to access a group of rows and columns by labels or a boolean array. In this context, `label` is used to identify the specific row to be updated. Without the `label`, `.loc` wouldn't know which row you're referring to.
    
#Row Identification**: The `.loc` method requires a row identifier to perform the update operation. Since `label` is the index of the current row in the iteration, it tells `.loc` exactly which row's "COUNTRY" column should be updated with `row["country"].upper()`

#No, you cannot use `row` instead of `label` in the `.loc` method. Here's why:
#`label`**: This represents the index or label of the current row. It's what `.loc` needs to know exactly which row to update in the DataFrame.
    
#`row`**: This is a Series object containing the data of the current row. It does not serve as an identifier for a specific row but rather as the content of the row.
```

```python
print(np.quantile(food_consumption['co2_emission'], np.linspace(0, 1, 11)))

# Calculate total co2_emission per country: emissions_by_country
emissions_by_country = food_consumption.groupby('country')['co2_emission'].sum()
  
# Compute the first and third quantiles and IQR of emissions_by_country
q1 = np.quantile(emissions_by_country, 0.25)
q3 = np.quantile(emissions_by_country, 0.75)
iqr = q3 - q1

  
# Calculate the lower and upper cutoffs for outliers
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
 
# Subset emissions_by_country to find outliers
outliers = emissions_by_country[(emissions_by_country < lower) | (emissions_by_country > upper)]
print(outliers)
```

```python
from scipy.stats import binom 
prob_3 = binom.pmf(3, 3, 0.3) #binom.pmf(no.of success you want,no.of experiments,probability)
print(prob_3)
```
**`binom.cdf(k, n, p)`**: This function computes the cumulative distribution function (CDF) of a binomial distribution. The CDF represents the probability that a binomial random variable will take a value ==less than or equal to a specified value.==
```python
prob_less_than_or_equal_1 = binom.cdf(1, 3, 0.3) #no of success , no.of experiments,probability

# Probability of closing > 1 deal out of 3 deals

prob_greater_than_1 = 1 - binom.cdf(1,3,0.3)
print(prob_greater_than_1)
```

```python
# Display df sorted by cluster label
print(df.sort_values("labels"))
```

```python
cols = ["rating","total_photos","total_ratings","total_tips"]

for col in cols:
  df[col] = df[col].fillna(0) 
  df.loc[df[col] < 0, col] = 0 #df.loc[row_identifier,col_identifier] = value
  
  
  
  
```

أنا مهندس ذكاء اصطناعي متخصص في بناء تطبيقات إدارة التعلم الآلي القابلة للتطوير والجاهزة للإنتاج. أجمع بين خبرتي في ال تعلم العميق و الفهم الاساسي لل باك اند في FastAPI , Docker في عمل تطبيقات امنه و عمل AI Agents ذات اداء عالي و يمكنها حل مشاكل العالم الحقيقي و العمليه في سوق العمل.