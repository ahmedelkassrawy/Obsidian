Create a pytorch dataset:
	__init__ -> as most python classes
	__getitem__ -> called every iteration
	__len__ -> return length of the dataset

```python
class SineDataset:
  def __init__(self):
    pass

  def __getitem__(self,index):
    return self.x_data[index], self.y_data[index]

  def __len__(self):
    pass
```

__init__
```python
def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
    self.img_labels = pd.read_csv(annotations_file)
    self.img_dir = img_dir
    self.transform = transform
    self.target_transform = target_transform
```

__len__
```python
def __len__(self):
    return len(self.img_labels)
```

__getitem__
```python
def __getitem__(self, idx):
    img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
    image = decode_image(img_path)
    label = self.img_labels.iloc[idx, 1]
    if self.transform:
        image = self.transform(image)
    if self.target_transform:
        label = self.target_transform(label)
    return image, label
```

```python
import torch
from torch.utils.data import DataLoader
from SineDataset import SineDataset

# Parameters
n_x_train = 30000  # Number of training datapoints
n_x_test = 8000    # Number of testing datapoints
batch_size = 16

# Create instances of SineDataset
dataset_train = SineDataset(num_datapoints = n_x_train)
dataset_test = SineDataset(num_datapoints = n_x_test)

# Create DataLoader instances
data_loader_train = DataLoader(dataset=dataset_train, 
								batch_size=batch_size, 
								shuffle=True)
data_loader_test = DataLoader(dataset=dataset_test, 
								batch_size=batch_size, 
								shuffle=False)
```

Iterate through a Dataloader
```python
# Display image and label.
train_features, train_labels = next(iter(train_dataloader))
print(f"Feature batch shape: {train_features.size()}")
print(f"Labels batch shape: {train_labels.size()}")

img = train_features[0].squeeze()
label = train_labels[0]

plt.imshow(img, cmap="gray")
plt.show()

print(f"Label: {label}")

>> #Feature batch shape: torch.Size([64, 1, 28, 28])
>> #Labels batch shape: torch.Size([64])
>> #Label: 7
```

```python
import torch
import torch.nn as nn

class SineANN(nn.Module):
    def __init__(self, hidden_size=64):
        super(SineANN, self).__init__()
        # Define layers
        self.layer1 = nn.Linear(1, hidden_size)  # Input layer: 1 input -> hidden_size
        self.relu = nn.ReLU()                    # Non-linear activation
        self.layer2 = nn.Linear(hidden_size, hidden_size)  # Hidden layer
        self.layer3 = nn.Linear(hidden_size, 1)  # Output layer: hidden_size -> 1 output

    def forward(self, x):
        # Define forward pass
        x = self.layer1(x)  # Input to first hidden layer
        x = self.relu(x)    # Apply ReLU activation
        x = self.layer2(x)  # First hidden layer to second hidden layer
        x = self.relu(x)    # Apply ReLU activation
        x = self.layer3(x)  # Second hidden layer to output
        return x
```

- Batch size (which has already been defined)
- Learning rate
- Number of training epochs
- Optimizer
- Loss function

```python
# Define the hyperparameters
learning_rate = # TO DO
epochs = # TO DO

# Create model
model = # TO DO

# Initialize the optimizer with above parameters
optimizer = # TO DO

# Define the loss function
loss_fn = # TO DO mean squared error
```

```python
# Loss loggers
training_loss_logger = []
testing_loss_logger = []

# Training and testing loop
for epoch in range(epochs):
    # Training Loop
    model.train()
    train_loss_accum = 0
    for x, y in tqdm(data_loader_train):
        # Run forward calculation
        y_pred = model(x)
        
        # Compute loss
        loss = loss_fn(y_pred, y)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Backward pass: compute gradient of the loss
        loss.backward()
        
        # Update parameters
        optimizer.step()
        
        # Log the loss
        train_loss_accum += loss.item()
    
    # Average training loss for the epoch
    avg_train_loss = train_loss_accum / len(data_loader_train)
    training_loss_logger.append(avg_train_loss)
    
    # Testing Loop
    with torch.no_grad():
        model.eval()
        test_loss_accum = 0
        for i, (x, y) in enumerate(tqdm(data_loader_test)):
            # Run forward calculation
            y_pred = model(x)
            
            # Compute loss
            loss = loss_fn(y_pred, y)
            
            # Log the loss
            test_loss_accum += loss.item()
        
        # Average test loss
        test_loss_accum /= (i + 1)
        testing_loss_logger.append(test_loss_accum)
    
    # Print average test loss for the epoch
    print("Epoch [%d/%d], Average Test Loss %.4f" % (epoch + 1, nepochs, test_loss_accum))
```

