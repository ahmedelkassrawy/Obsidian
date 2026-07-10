#### Classification
Normalization of images : / 255.

```python
model = tf.keras.Sequential(
    [
        tf.keras.layers.Flatten(input_shape = [28,28]),
        tf.keras.layers.Dense(300, activation = "relu"),
        tf.keras.layers.Dense(100, activation = "relu"),
        tf.keras.layers.Dense(10, activation = "softmax")
    ]
)
```

We use the activation = "relu" in all the Dense layer, until the last layer we use the num of classes -> if more than 2 categories -> activation = "softmax"
-> if only 2 categories -> activation = "sigmoid"

```python
model.compile(loss = "sparse_categorical_crossentropy",
              optimizer = "sgd",
              metrics = ["accuracy"])
              
history = model.fit(X_train,
                    y_train,
                    epochs = 30,
                    validation_data = (X_valid,y_valid))

model.evaluate(X_test, y_test)			   
```

If you only care about the class with the highest estimated probability (even if
that probability is quite low), then you can use the argmax() method to get the
highest probability class index for each instance:
```python
X_new = X_test[:3]

y_proba = model.predict(X_new)
y_proba.round(2)

y_pred = y_proba.argmax(axis=-1)
np.array(class_names)[y_pred]
```

#### Plotting
```python
import matplotlib.pyplot as plt
import pandas as pd

pd.DataFrame(history.history).plot(
 figsize=(8, 5), 
 xlim=[0, 29], 
 ylim=[0, 1], 
 grid=True, 
 xlabel="Epoch",
 style=["r--", "r--.", "b-", "b-*"])

plt.show()
```

#### Regression
Moreover, in this example we don’t need a Flatten layer, and instead we’re using a Normalization layer as the first layer: it does the same thing as Scikit Learn’s StandardScaler, but it must be fitted to the training data using its adapt() method before you call the model’s fit() method.
Use 1 only in Dense since its Regression.
```python
norm_layer = tf.keras.layer.Normalization(input_shape = X_train.shape[1:])

model = tf.keras.Sequential(
    [
        norm_layer,
        tf.keras.layers.Dense(50,activation="relu"),
        tf.keras.layers.Dense(50,activation="relu"),
        tf.keras.layers.Dense(50,activation="relu"),
        tf.keras.layers.Dense(1)
    ]
)
```

The Normalization layer learns the feature means and standard deviations in the training data when you call the adapt() method. Yet when you display the model’s summary, these statistics are listed as non-trainable. This is because these parameters are not affected by gradient descent

```python
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3) model.compile(loss="mse", optimizer=optimizer, metrics=["RootMeanSquaredError"]) 
norm_layer.adapt(X_train)
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_valid, y_valid))
```

#### Save and Restore a Model
If you set save_format="h5" or use a filename that ends with .h5, .hdf5, or .keras, then Keras will save the model to a single file using a Keras-specific format based on the HDF5 format. However, most TensorFlow deployment tools require the SavedModel format instead.
```python
model.save("my_keras_model", save_format="tf")

model = tf.keras.models.load_model("my_keras_model")
```