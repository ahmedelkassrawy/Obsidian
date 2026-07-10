```python
df = pd.read_csv("/content/TSLA.csv", parse_dates=True, index_col="Date")
```

- `parse_dates=True`: Ensures the "Date" column is treated as dates.
- 
```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(np.array(data).reshape(-1, 1))
```

Since the min, max scaler needs rescaled size

```python
train_data = scaled_data[:train_size, 0:1]
test_data = scaled_data[train_size - 60:, 0:1]
```


In the scaled data: 
	each row represent a time step 
	each col represent a feature

So scaled_data[ :train_size , 0:1]
where selecting rows until train_size 
The 0:1 is to select the cols for the features

test_data = scaled_data[train_size-60:, 0:1]
-60 in the code snippet is used an additional 60 rows of data ensures the data includes 60+ rows , often done in the time series forecasting to provide context or lookback for the model when making the predictions. LSTM often require a sequence of past data points to make predictions.
It ensures a smooth transition between the training and test datasets, which is critical for time series analysis.

```python
model.compile(optimizer='adam', loss='mse', metrics = ['mean_absolute_error']) 
```

The **Mean Absolute Error (MAE)** is a commonly used metric to evaluate the performance of regression models, including LSTM models for time series forecasting.

```python
predict = model.predict(X_test)

#Inverse the predictions scaling
pred = scaler.inverse_transform(predict)
pred.shape
```

#### **What’s Happening?**

- `scaler.inverse_transform(predict)`: The `MinMaxScaler` object (`scaler`) is used to reverse the scaling applied to the predictions.
    
- During preprocessing, the data was scaled to a range of `[0, 1]` using `MinMaxScaler`. Now, we need to convert the predictions back to their original scale (e.g., actual stock prices in dollars).
    
- `pred`: The output of this step is a NumPy array containing the **denormalized predictions** in the original scale.
```python
def insert_end(X_in, new_input):
    timestep = 60

    for i in range(timestep - 1):
        X_in[:, i, :] = X_in[:, i+1, :]

    X_in[: ,timestep - 1, :] = new_input

    return X_in
```

so in the for loop we are shifting the seq left and moved one position to the left , the new prediction is added to the end of seq.

```python
future = 30
forecast = []
X_in = X_test[-1:, :, :]
time = []
```

- `future = 30`: Number of days to forecast (30 days).
-  forecast = []`: List to store the forecasted values.
Initializes the input sequence with the last sequence from the test data (`X_test`).
- `time = []`: List to store the corresponding dates for the forecasts.

```python
for i in range(future):
    out = model.predict(X_in, batch_size=5)
    forecast.append(out[0, 0]) 
    
    print(forecast)
    
    X_in = insert_end(X_in, out[0, 0])
    time.append(pd.to_datetime(df.index[-1]) + timedelta(days = i))
```

**Update the Input Sequence**:

- `X_in = insert_end(X_in, out[0, 0])`: Updates the input sequence by shifting it left and appending the new prediction

 **Generate the Corresponding Date**:
    
`time.append(pd.to_datetime(df.index[-1]) + timedelta(days=i))`: Generates the date for the forecasted value by adding `i` days to the last date in the dataset.

```python
forcasted_output = np.asanyarray(forecast)
forcasted_output = forcasted_output.reshape(-1, 1)
forcasted_output = scaler.inverse_transform(forcasted_output)

forcasted_output = pd.DataFrame(forcasted_output)
date = pd.DataFrame(time)

df_result = pd.concat([date, forcasted_output], axis=1)
df_result.columns = ["Date", "Forecasted"]
```

convert to numpy array
reshape for inverse scaling to reshape 2D required for inverse
Converts the scaled predictions back to the original scale (e.g., actual stock prices in dollars).

- `forcasted_output = pd.DataFrame(forcasted_output)`: Converts the denormalized predictions to a DataFrame.
- `date = pd.DataFrame(time)`: Converts the `time` list to a DataFrame.
- `df_result = pd.concat([date, forcasted_output], axis=1)`: Combines the dates and forecasted values into a single DataFrame.
    
- `df_result.columns = ["Date", "Forecasted"]`: Renames the columns for clarity.