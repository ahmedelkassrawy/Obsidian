#### Tabular Classification
#### Dataset Class
```python
class RiceDataset(Dataset):
  def __init__(self,X,y):
    self.X = torch.tensor(X.values,dtype = torch.float32).to(device)
    self.y = torch.tensor(y.values,dtype = torch.float32).to(device)

  def __len__(self):
    return len(self.X)

  def __getitem__(self,idx):
    return self.X[idx],self.y[idx]

train_dataset = RiceDataset(X_train,y_train)
test_dataset = RiceDataset(X_test,y_test)
```

```python
class Model(nn.Module):
  def __init__(self):
    super().__init__()

    self.l1 = nn.Linear(X.shape[1],10)
    self.l2 = nn.Linear(10,1)
    self.sigmoid = nn.Sigmoid()

  def forward(self,x):
    return self.sigmoid(self.l2(self.l1(x)))

model = Model().to(device)
summary(model,(X.shape[1],))
```

```python
import torch

total_loss_train_plot = []
total_loss_test_plot = []
total_acc_train_plot = []
total_acc_test_plot = []

for epoch in range(EPOCHS):
  model.train()
  
  total_acc_train = 0
  total_loss_train = 0
  total_acc_test = 0
  total_loss_test = 0

  for inputs,labels in train_dataloader:
    optimizer.zero_grad()

    outputs = model(inputs).squeeze(1)
    loss = loss_fn(outputs,labels)

    loss.backward()
    optimizer.step()

    total_loss_train += loss.item()
    acc = ((outputs).round() == labels).sum().item()
    total_acc_train += acc
  
  with torch.no_grad():
    model.eval()

    for inputs,labels in test_dataloader:
      outputs = model(inputs).squeeze(1)
      loss = loss_fn(outputs,labels)

      total_loss_test += loss.item()
      acc = ((outputs).round() == labels).sum().item()
      total_acc_test += acc

  total_loss_train_plot.append(round(total_loss_train/len(train_dataloader),4))
  total_loss_test_plot.append(round(total_loss_test/len(test_dataloader),4))
  total_acc_train_plot.append(round(total_acc_train/len(train_dataloader.dataset),4))
  total_acc_test_plot.append(round(total_acc_test/len(test_dataloader.dataset),4))

  print(f"Epoch no. {epoch + 1} Train Loss: {round(total_loss_train/len(train_dataloader),4)} Train Acc: {round(total_acc_train/len(train_dataloader.dataset),4)} Test Loss: {round(total_loss_test/len(test_dataloader),4)} Test Acc: {round(total_acc_test/len(test_dataloader.dataset),4)}")
  print("="*50)
```

```python
with torch.no_grad():
  total_loss_test = 0
  total_acc_test = 0

  for inputs,labels in test_dataloader:
    outputs = model(inputs).squeeze(1)

    test_loss = loss_fn(outputs,labels)
    total_loss_test += test_loss.item()

    acc = ((outputs).round() == labels).sum().item()
    total_acc_test += acc

print(f"Accuracy Score is: {round((total_acc_test/X_test.shape[0])*100, 2)}%")
```

```python

```

----
##### CNN 
```python
import torch # Main PyTorch Library
from torch import nn # Used for creating the layers and loss function
from torch.optim import Adam # Adam Optimizer
import torchvision.transforms as transforms # Transform function used to modify and preprocess all the images
from torch.utils.data import Dataset, DataLoader # Dataset class and DataLoader for creating the objects
from sklearn.preprocessing import LabelEncoder # Label Encoder to encode the classes from strings to numbers
import matplotlib.pyplot as plt # Used for visualizing the images and plotting the training progress
from PIL import Image # Used to read the images from the directory
import pandas as pd # Used to read/create dataframes (csv) and process tabular data
import numpy as np # preprocessing and numerical/mathematical operations
import os # Used to read the images path from the directory

device = "cuda" if torch.cuda.is_available() else "cpu" # detect the GPU if any, if not use CPU, change cuda to mps if you have a mac
print("Device available: ", device)
```

#### Dataframe
```python
image_paths = []
labels = []

for i in os.listdir("/content/afhq"):
  for label in os.listdir(f"/content/afhq/{i}"):
    for image in os.listdir(f"/content/afhq/{i}/{label}"):
      labels.append(label)
      image_paths.append(f"/content/afhq/{i}/{label}/{image}")

df = pd.DataFrame(zip(image_paths,labels), columns = ["image_path", "label"])
df.head()
```

#### Data Split
```python
train = df.sample(frac=0.7,random_state=7) # Create training of 70% of the data
test = df.drop(train.index) # Create testing by removing the 70% of the train data which will result in 30%
```

#### Image Transformation
```python
le = LabelEncoder()
le.fit(df["label"])

transform = transforms.Compose(
    [
        transforms.Resize((128,128)),
        transforms.ToTensor(),
        transforms.ConvertImageDtype(torch.float)
    ]
)
```

#### Dataset
```python
class ImageDataset(Dataset):
  def __init__(self,df,transform = None):
    self.df = df
    self.transform = transform
    self.labels = torch.tensor(le.transform(df["label"])).to(device)

  def __len__(self):
    return self.df.shape[0]

  def __getitem__(self,idx):
    img_path = self.df.iloc[idx,0]
    label = self.labels[idx]

    image = Image.open(img_path).convert("RGB")
    if self.transform:
      image = self.transform(image).to(device)

    return image,label
    
train_dataset = ImageDataset(train,transform = transform)
test_dataset = ImageDataset(test,transform = transform)
```

#### Visualize Images
```python
n_rows = 3
n_cols = 3
f, axarr = plt.subplots(n_rows, n_cols)
for row in range(n_rows):
    for col in range(n_cols):
        image = train_dataset[np.random.randint(0,train_dataset.__len__())][0].cpu()
        axarr[row, col].imshow((image*255).squeeze().permute(1,2,0))
        axarr[row, col].axis('off')

plt.tight_layout()
plt.show()
```

#### Dataloader
```python
train_loader = DataLoader(train_dataset,batch_size = BATCH_SIZE,shuffle = True)
test_loader = DataLoader(test_dataset,batch_size = BATCH_SIZE,shuffle = False)
```

#### Network 
```python
class Neural(nn.Module):
  def __init__(self):
    super().__init__()

    self.conv1 = nn.Conv2d(in_channels=3,out_channels = 32,kernel_size = 3,padding = 1)
    self.conv2 = nn.Conv2d(in_channels = 32,out_channels = 64,kernel_size = 3, padding = 1)
    self.conv3 = nn.Conv2d(in_channels = 64,out_channels = 128,kernel_size = 3, padding = 1)
    self.pooling = nn.MaxPool2d(2,2)
    self.relu = nn.ReLU()

    self.flatten = nn.Flatten()
    self.l1 = nn.Linear(in_features =  (128 * 16 * 16),out_features = 128)
    self.output = nn.Linear(in_features = 128, out_features = len(df["label"].unique()))

  def forward(self,x):
    x = self.conv1(x)
    x = self.pooling(x)
    x = self.relu(x)

    x = self.conv2(x)
    x = self.pooling(x)
    x = self.relu(x)

    x = self.conv3(x)
    x = self.pooling(x)
    x = self.relu(x)

    x = self.flatten(x)
    x = self.l1(x)
    x = self.output(x)

    return x 
```

#### Model Summary
```python
from torchsummary import summary

model = Neural().to(device)
summary(model,input_size = (3,128,128))
```

#### Loss and Optimizer
```python
loss_fn = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(),lr = LR)
```

#### Training and eval loop
```python
total_loss_train_plot = []
total_loss_test_plot = []
total_acc_train_plot = []
total_acc_test_plot = []

for epoch in range(EPOCHS):
  total_train_loss = 0
  total_train_acc = 0
  total_test_loss = 0
  total_test_acc = 0

  model.train()
  for inputs,labels in train_loader:
    optimizer.zero_grad()

    outputs = model(inputs)
    loss = loss_fn(outputs,labels)
    loss.backward()
    optimizer.step()

    total_train_loss += loss.item()
    total_train_acc += (torch.argmax(outputs,axis = 1) == labels).sum().item()

  model.eval()
  with torch.no_grad():
    for inputs,labels in test_loader:
      outputs = model(inputs)
      val_loss = loss_fn(outputs,labels)

      total_test_loss += val_loss.item()
      total_test_acc += (torch.argmax(outputs,axis = 1) == labels).sum().item()

  total_loss_train_plot.append(round(total_train_loss/1000, 4))
  total_loss_test_plot.append(round(total_test_loss/1000, 4))
  total_acc_train_plot.append(round(total_train_acc/(train_dataset.__len__())*100, 4))
  total_acc_test_plot.append(round(total_test_acc/(test_dataset.__len__())*100, 4))
  print(f'''Epoch {epoch+1}/{EPOCHS}, Train Loss: {round(total_train_loss/100, 4)} Train Accuracy {round((total_train_acc)/train_dataset.__len__() * 100, 4)}
              Validation Loss: {round(total_test_loss/100, 4)} Validation Accuracy: {round((total_test_acc)/test_dataset.__len__() * 100, 4)}''')
  print("="*25)
```

#### Plot
```python
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

axs[0].plot(total_loss_train_plot, label='Training Loss')
axs[0].plot(total_loss_test_plot, label='Validation Loss')
axs[0].set_title('Training and Validation Loss over Epochs')
axs[0].set_xlabel('Epochs')
axs[0].set_ylabel('Loss')
axs[0].legend()

axs[1].plot(total_acc_train_plot, label='Training Accuracy')
axs[1].plot(total_acc_test_plot, label='Validation Accuracy')
axs[1].set_title('Training and Validation Accuracy over Epochs')
axs[1].set_xlabel('Epochs')
axs[1].set_ylabel('Accuracy')
axs[1].legend()

plt.tight_layout()

plt.show()
```

#### Inference
1. Read image
2. Transform using transform object
3. Predict through model
4. Inverse transform by label encoder
```python
def predict(image_path:str):
  image = Image.open(image_path).convert("RGB")
  image = transform(image).to(device)

  output = model(image.unsqueeze(0))
  output = torch.argmax(output,axis = 1).item()
  return le.inverse_transform([output])
```
---
#### Transfer Learning(Pretrained)
```python
googlenet_model = models.googlenet(weights='DEFAULT')

for param in googlenet_model.parameters():
  param.requires_grad = True
```

```python
googlenet_model.fc
```

```python
num_classes = len(df["category"].unique())

googlenet_model.fc = torch.nn.Linear(googlenet_model.fc.in_features, num_classes)
googlenet_model.to(device)
```

```python
loss_fn = nn.CrossEntropyLoss()
optimizer = Adam(googlenet_model.parameters(),lr = LR)
```

----
##### Text
```python
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert_model = AutoModel.from_pretrained("bert-base-uncased")
```

```python
class TextDataset(Dataset):
  def __init__(self,X,y):
    self.X = [tokenizer(x,
                        max_length = 100,
                        truncation = True,
                        padding = "max_length",
                        return_tensors = "pt").to(device)
              for x in X]

    self.y = torch.tensor(y,dtype = torch.float32).to(device)

  def __len__(self):
    return len(self.X)
  
  def __getitem__(self,idx):
    return self.X[idx],self.y[idx]
```

```python
train_dataset = TextDataset(X_train,y_train)
test_dataset = TextDataset(X_test,y_test)
```

```python
class MyModel(nn.Module):
    def __init__(self, bert):
        super(MyModel, self).__init__()

        self.bert = bert
        self.dropout = nn.Dropout(0.25)
        self.linear1 = nn.Linear(768, 384)
        self.linear2 = nn.Linear(384, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids, attention_mask):
        pooled_output = self.bert(input_ids, attention_mask, return_dict = False)[0][:,0]
        output = self.linear1(pooled_output)
        output = self.dropout(output)
        output = self.linear2(output)
        output = self.sigmoid(output)
        return output
```

```python
for param in bert_model.parameters():
    param.requires_grad = False
model = MyModel(bert_model).to(device)
```

```python
loss_fn = nn.BCELoss()
optimizer = Adam(model.parameters(), lr= LR)
```

```python
total_loss_train_plot = []
total_loss_test_plot = []
total_acc_train_plot = []
total_acc_test_plot = []

for epoch in range(EPOCHS):
  total_train_loss = 0
  total_train_acc = 0
  total_test_loss = 0
  total_test_acc = 0

  for idx,data in enumerate(train_dataloader):
    input,label = data

    input.to(device)
    label.to(device)

    optimizer.zero_grad()
    outputs = model(input["input_ids"].squeeze(1),
                    input["attention_mask"].squeeze(1)).squeeze(1)

    loss = loss_fn(outputs,label)
    loss.backward()
    optimizer.step()

    acc = ((outputs).round() == label).sum().item()
    
    total_train_loss += loss.item()
    total_train_acc += acc

  with torch.no_grad():
    for idx,data in enumerate(test_dataloader):
      input,label = data

      input.to(device)
      label.to(device)

      outputs = model(input["input_ids"].squeeze(1),
                      input["attention_mask"].squeeze(1)).squeeze(1)
      loss = loss_fn(outputs,label)
      total_test_loss += loss.item()

      acc = ((outputs).round() == label).sum().item()
      total_test_acc += acc

  total_loss_train_plot.append(round(total_train_loss/1000, 4))
  total_loss_test_plot.append(round(total_test_loss/1000, 4))
  total_acc_train_plot.append(round(total_train_acc/(train_dataset.__len__())*100, 4))
  total_acc_test_plot.append(round(total_test_acc/(test_dataset.__len__())*100, 4))
  print(f'''Epoch {epoch+1}/{EPOCHS}, Train Loss: {round(total_train_loss/100, 4)} Train Accuracy {round((total_train_acc)/train_dataset.__len__() * 100, 4)}
              Validation Loss: {round(total_test_loss/100, 4)} Validation Accuracy: {round((total_test_acc)/test_dataset.__len__() * 100, 4)}''')
  print("="*25)
  
```

```python
with torch.no_grad():
  total_loss_test = 0
  total_acc_test = 0
  for indx, data in enumerate(testing_dataloader):
    input, label = data
    input.to(device)
    label.to(device)

    prediction = model(input['input_ids'].squeeze(1), input['attention_mask'].squeeze(1)).squeeze(1)

    batch_loss_val = criterion(prediction, label)
    total_loss_test += batch_loss_val.item()
    acc = ((prediction).round() == label).sum().item()
    total_acc_test += acc

print(f"Accuracy Score is: {round((total_acc_test/X_test.shape[0])*100, 2)}%")
```

```python
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

axs[0].plot(total_loss_train_plot, label='Training Loss')
axs[0].plot(total_loss_test_plot, label='Validation Loss')
axs[0].set_title('Training and Validation Loss over Epochs')
axs[0].set_xlabel('Epochs')
axs[0].set_ylabel('Loss')
axs[0].legend()

axs[1].plot(total_acc_train_plot, label='Training Accuracy')
axs[1].plot(total_acc_test_plot, label='Validation Accuracy')
axs[1].set_title('Training and Validation Accuracy over Epochs')
axs[1].set_xlabel('Epochs')
axs[1].set_ylabel('Accuracy')
axs[1].legend()

plt.tight_layout()

plt.show()

```

| Case                                           | What `.squeeze(1)` does                                             | Why it’s useful                     |
| ---------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------- |
| Binary classification                          | Removes the extra dimension `[batch_size, 1] → [batch_size]`        | Matches labels shape `[batch_size]` |
| Multiclass classification (`CrossEntropyLoss`) | Usually **not used**, since outputs are `[batch_size, num_classes]` | —                                   |
