Regression Model
```python
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Input

def reg_model():
	model = Sequential()
	model.add(Input(8,1))
	model.add(Dense(50,activation = "relu"))
	model.add(Dense(50,activation = "relu"))
	model.add(Dense(1))

	model.compile(optimizer = "adam",loss = "mean_squared_error")
	return model

model = reg_model()

hist = model.fit(X,y,validation_split = 0.3,epochs = 100)
test_loss = hist.history["val_loss"][-1]:.4f
```

Classification model
```python
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Input
from keras.utils import to_categorical
from keras.datasets import mnist

X_train.shape
>>> (60000, 28, 28)

plt.imshow(X_train[0])
```

```python
num_pixel = X_train.shape[1] * X_train.shape[2]

X_train = X_train.reshape(X_train.shape[0],num_pixel).astype("float32")
X_test = X_test.reshape(X_test.shape[0],num_pixel).astype('float32')

X_train.shape
>>> (60000, 784)
```

Pixel values can range from 0 to 255
let the range be 0 to 1
```python
y_train = to_categorical(y_train)

y_train.shape
>>> (60000,10)

num_classes = y_test.shape[1]
>>> 10
```

```python
def classification_model():
  model = Sequential()

  model.add(Input(shape = (784,)))
  model.add(Dense(100,activation = "relu"))
  model.add(Dense(num_classes,activation = "softmax"))

  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
  return model
```

```python
# build the model
model = classification_model()

# fit the model
hist = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, verbose=2)

# evaluate the model
scores = model.evaluate(X_test, y_test, verbose=0)
```

#### Saving the model
```python
model.save('classification_model.keras')
```

```python
pretrained_model = keras.saving.load_model('classification_model.keras')
```

#### Plot Loss
```python
#plot the loss
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()
```

### CNN
```python
def convolutional_model():
    
    # create model
    model = Sequential()
    model.add(Input(shape=(28, 28, 1)))
    model.add(Conv2D(16, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    
    model.add(Conv2D(8, (2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    
    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy',  metrics=['accuracy'])
    return model
```