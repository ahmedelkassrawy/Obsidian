the choice of numbers of hidden states in lstm layer , more units allow the model to capture more complex patterns
256 is a common starting point beacuse it balances the model capacity and computational efficency ++ numbers like 256 is a power of 2 which will allign well with hardware optimizations 

usaual numbers are 64,128,256,512

talking about dropping NA's
- **or text fields:** Replace NA with `" "`. This maintains data consistency and avoids excessive data loss.
- **For numerical/critical fields (if applicable):** Investigate further before deciding to drop or fill.

```python
model = keras.models.Sequential()
model.add(keras.layers.LSTM(64,return_sequences=True,input_shape = (X_train.shape[1],1)))
model.add(keras.layers.LSTM(64,return_sequences= False))
model.add(keras.layers.Dense(128,activation = "relu"))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1))

model.summary()
model.compile(optimizer = "adam",
              loss = "mae",
              metrics = [keras.metrics.RootMeanSquaredError()])
              
# input_shape = X_train.shape[1],1 
# the shape [1] is because the the time steps are 1 day only could be 2,3,4,5 daysss
# 1 is the number of features you have in your data
```