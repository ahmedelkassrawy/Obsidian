There are two kinds of features unique to time series: time-step features and lag features.
Time-step features are features we can derive directly from the time index. The most basic time-step feature is the **time dummy**, which counts off time steps in the series from beginning to end.

![[Pasted image 20240918144229.png]]

```python
df = tunnel.copy()

df['Time'] = np.arange(len(tunnel.index))

df.head()
```
### Lag features

To make a **lag feature** we shift the observations of the target series so that they appear to have occured later in time. Here we've created a 1-step lag feature, though shifting by multiple steps is possible too.

![[Pasted image 20240918144155.png]]

```python
df['Lag_1'] = df['NumVehicles'].shift(1)
df.head()
```

- `X = df.loc[:, ['time']]`: This returns a DataFrame because `['time']` is a list (even if it contains only one element). In machine learning, features (or inputs) are typically expected to be in the form of a 2D array (i.e., a DataFrame or a 2D NumPy array), where rows are the samples, and columns are the features. Even if you have just one feature (`'time'`), you still need it in a 2D format because that's how the `LinearRegression` model expects the input.
    
- `y = df.loc[:, 'sales']`: This returns a **Series** because you're selecting a single column without brackets. The target (`y`) is expected to be a 1D array (a vector) representing the output values, which can be a pandas Series.
    

In summary, the brackets for `X` ensure that the feature matrix is 2D, while `y` remains 1D, which matches the expected input shapes for scikit-learn models.

```python
# Predict using the trained model
y_pred = model.predict(X)  # This returns an array, no index

# Convert predictions into a Series and retain the original index
y_pred = pd.Series(y_pred, index=X.index)

```

# What is Trend?

The **trend** component of a time series represents a persistent, long-term change in the mean of the series.
- slowest moving part of series representing the largest time scale of importance
- we use Moving Average plots --> each point on the graph represents the average of all the values in the series that fall within the window on either side.
![[EZOXiPs.gif]]

```python
moving_average = df.rolling(window = 365, #365 day window
							center = True, #puts the average at the center
							min_periods = 183, #choose about the half the window size
						   ).mean() # compute the mean (could also do median, std, min, max, ...)

ax = df.plot()
moving_average.plot(ax=ax,title="Tunnel Traffic - 365-Day Moving Average")
```
![[__results___4_0.png]]

time dummy in Pandas directly. From now on, however, we'll use a function from the `statsmodels` library called `DeterministicProcess`

```python
from statsmodels.tsa.deterministic import DeterministicProcess

dp = DeterministicProcess(
    index=tunnel.index,  # dates from the training data
    constant=True,       # dummy feature for the bias (y_intercept)
    order=1,             # the time dummy (trend)
    drop=True,           # drop terms if necessary to avoid collinearity
)
# `in_sample` creates features for the dates given in the `index` argument
X = dp.in_sample()

X.head()
```

To make a forecast, we apply our model to "out of sample" features. "Out of sample" refers to times outside of the observation period of the training data. Here's how we could make a 30-day forecast:

```python
X = dp.out_of_sample(steps=30)

y_fore = pd.Series(model.predict(X), index=X.index)

y_fore.head()
```

# What is Seasonality?
whenever there is a regular, periodic change in the mean of the series
Seasonal changes generally follow the clock and calendar -- repetitions over a day, a week, or a year are common.
- Indicators --> weekly season of daily observations
- Fourier Features --> season with many observations like an annual season of daily observations

```python
y = average_sales.copy()

# YOUR CODE HERE
fourier = CalendarFourier(freq="M",order=4) #new code , order = no. of months we want
dp = DeterministicProcess(
    index=y.index,
    constant=True,
    order=1,
    # YOUR CODE HERE
    seasonal=True, #new code
    additional_terms=[fourier], #new code
    drop=True,
)

X = dp.in_sample()
```
```python
# Scikit-learn solution
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse=False)

X_holidays = pd.DataFrame(
    ohe.fit_transform(holidays),
    index=holidays.index,
    columns=holidays.description.unique(),
)


# Pandas solution
X_holidays = pd.get_dummies(holidays)

```