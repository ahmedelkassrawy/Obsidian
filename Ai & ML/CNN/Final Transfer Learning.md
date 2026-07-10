
---
# 🧠 Transfer Learning in CNNs (TensorFlow + PyTorch)
## 📘 Overview

**Transfer Learning** is a powerful technique that allows you to **leverage pretrained models** trained on massive datasets (like ImageNet) and reuse them for your custom task.  
This helps:
- Train models **faster**
- Avoid **overfitting** (especially on small datasets.
- Achieve **higher accuracy** with less data
---

## ⚙️ 1. Importing Libraries & Dataset Setup (TensorFlow / Keras)

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, TensorBoard, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix
import ipywidgets as widgets
import io
from PIL import Image
from IPython.display import display, clear_output
from warnings import filterwarnings

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
```

---

## 🧩 2. Train and Test Image Loading

You prepare your data by loading images, resizing them, and appending them to arrays.

```python
X_train = []
y_train = []

image_size = 150

for i in labels:
    folder_path = os.path.join("/content/Training", i)
    for j in os.listdir(folder_path):
        img_path = os.path.join(folder_path, j)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (image_size, image_size))
        X_train.append(img)
        y_train.append(i)
```

You can repeat the same for the test folder.

---

## 🧠 3. Label Encoding and One-Hot Encoding

Since this is **multi-class classification**, we must convert labels to **one-hot encoded format** (not just integer labels).

```python
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)

y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)
```

💡 Use **`categorical_crossentropy`** as your loss function for one-hot targets.

---

## ⚙️ 4. Using EfficientNetB0 (Pretrained Model)

```python
efficient = EfficientNetB0(
    weights='imagenet',
    include_top=False,
    input_shape=(image_size, image_size, 3)
)
```

- `include_top=False`: Removes the final dense layers so we can add our own.
    
- We’ll **freeze the convolutional base** to prevent overfitting.
    

---

## 🧩 5. Data Augmentation (To Reduce Overfitting)

Data augmentation artificially expands your dataset with variations.

```python
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

datagen.fit(X_train)
model.fit(datagen.flow(X_train, y_train, batch_size=32), 
          epochs=12, 
          validation_data=(X_test, y_test))
```

### 🧠 Overfitting Solutions

- ✅ Data Augmentation
    
- ✅ L2 Regularization
    
- ✅ Dropout Layers
    
- ✅ Early Stopping
    

---

## 🧱 6. Freezing Layers (Transfer Learning Logic)

```python
efficientnet = EfficientNetB0(weights='imagenet', 
                              include_top=False, 
                              input_shape=(image_size, image_size, 3))
efficientnet.trainable = False  # Freeze all pretrained layers
```

**When to freeze:**

- Small dataset
    
- Similar domain to ImageNet
    
- Early stages of fine-tuning
    

---

## ⚡ 7. Data Split and Augmentation Pipeline

```python
X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator()

history = model.fit(
    train_datagen.flow(X_train_split, y_train_split, batch_size=32),
    validation_data=val_datagen.flow(X_val_split, y_val_split, batch_size=32),
    epochs=12,
    verbose=1,
    callbacks=[tensorboard, checkpoint, reduce_lr]
)
```

---

## 📊 8. Classification Report

```python
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test, axis=1)

print(classification_report(y_test_classes, y_pred_classes, target_names=label_encoder.classes_))
```

---

# 🔥 Transfer Learning in PyTorch (ResNet & AlexNet)

Now let’s look at how this is done using **PyTorch**.

---

## 🧠 1. Data Augmentation and Preprocessing

```python
import torch
from torchvision.transforms import v2

train_transform = v2.Compose([
    v2.ToImage(),
    v2.RandomHorizontalFlip(p=0.5),
    v2.RandomVerticalFlip(p=0.5),
    v2.RandomResizedCrop(size=[227, 227]),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

test_transform = v2.Compose([
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

---

## 📦 2. Custom Dataset Class

```python
import os
from torch.utils.data import Dataset
from PIL import Image

class dataset(Dataset):
    def __init__(self, paths, transform=None, is_train=False):
        self.paths = paths
        self.transform = transform
        self.is_train = is_train
        
    def __getitem__(self, index):
        full_path = os.path.join(train_path, self.paths[index])
        img = Image.open(full_path)
        img = img.resize((227, 227))
        label = self.paths[index][:3]

        if self.transform:
            if self.is_train:
                img = self.transform["train_transform"](img)
            else:
                img = self.transform["test_transform"](img)

        return img, int(1 if label == "cat" else 0)

    def __len__(self):
        return len(self.paths)
```

---

## 🧩 3. Model Architecture (AlexNet)

```python
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 96, 11, 4)
        self.mx1 = nn.MaxPool2d(3, 2)
        self.conv2 = nn.Conv2d(96, 256, 5, padding=2)
        self.mx2 = nn.MaxPool2d(3, 2)
        self.conv3 = nn.Conv2d(256, 384, 3, padding=1)
        self.conv4 = nn.Conv2d(384, 384, 3, padding=1)
        self.conv5 = nn.Conv2d(384, 256, 3, padding=1)
        self.mx3 = nn.MaxPool2d(3, 2)
        self.flatten = nn.Flatten()
        self.linear1 = nn.Linear(9216, 4096)
        self.relu = nn.ReLU(inplace=True)
        self.linear2 = nn.Linear(4096, 4096)
        self.linear3 = nn.Linear(4096, 2)
        
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.mx1(x)
        x = self.relu(self.conv2(x))
        x = self.mx2(x)
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        x = self.relu(self.conv5(x))
        x = self.mx3(x)
        x = self.flatten(x)
        x = self.relu(self.linear1(x))
        x = self.relu(self.linear2(x))
        return self.linear3(x)
```

---

## ⚙️ 4. Using Pretrained ResNet (Transfer Learning)

```python
from torchvision import models
model = models.resnet50(weights="IMAGENET1K_V1")

for parameter in model.parameters():
    parameter.requires_grad = False

model.fc = nn.Linear(model.fc.in_features, 2)
```

✅ Only the **final layer** is trainable.  
✅ Saves computation and avoids overfitting.

---

## 🔁 5. Training Loop (PyTorch)

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.005)

epochs = 1
for epoch in range(epochs):
    model.train(True)
    total_loss = 0
    for i, (image, labels) in enumerate(train_loader):
        image, labels = image.to(device).float(), labels.to(device)
        output = model(image)
        loss = loss_fn(output, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

---

## 🧪 6. Evaluation

```python
model.eval()
with torch.no_grad():
    for image, labels in test_loader:
        image, labels = image.to(device).float(), labels.to(device)
        output = model(image)
        loss = loss_fn(output, labels)
```

---

## 🧭 Summary

|Concept|TensorFlow Implementation|PyTorch Implementation|
|---|---|---|
|Base Model|EfficientNetB0|ResNet50|
|Dataset Augmentation|`ImageDataGenerator`|`torchvision.transforms`|
|Label Encoding|One-hot (categorical)|Integer labels|
|Fine-tuning|Freeze CNN base|Freeze all layers except final FC|
|Loss Function|`categorical_crossentropy`|`CrossEntropyLoss`|
|Optimizer|Adam|SGD|

---

Would you like me to export this merged version as a **final `.md` Obsidian file** so you can store and navigate it directly inside your vault (with collapsible sections, emojis, and task checkboxes)?