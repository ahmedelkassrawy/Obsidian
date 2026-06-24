```python
from torchvision.datasets import ImageFolder
from torchvision import transforms

train_transforms = transforms.Compose([
	tranforms.ToTensor(),
	transforms.Resize((128,128)),
])

df_train = ImageFolder(
	"data/clouds_train",
	transform = train_transforms,
)

#Display image
dataloader_train = DataLoader(
	dataset_train,
	shuffle = True,
	batch_size = 1
)

img,label = next(iter(dataloader_train))
print(img.shape)

img = img.squeeze().permute(1,2,0)
print(img.shape)

import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()
```

### Data Augmentation
```python
train_transforms = transforms.Compose([
	transforms.RandomHorizantalFlip(),
	transforms.RandomRotation(45),
	tranforms.ToTensor(),
	transforms.Resize((128,128)),
])
```

#### Convolutional layer
- Slide filter of parameters over the input
- at each position perform convolution
- feature map:
	- preserves spatial patterns from the input
	- uses fewer parameters than linear layer
- One filter = one feature map
- apply activations to feature maps
- all feature maps combined from the output 
- nn.Conv2d(3,32,kernel_size = 3,padding = 1)
- zero padding -> maintain spatial dimensions

Max pooling 
- slide non overlapping window over the input
- at each position retain only the max value
- used after the convolutional layers to reduce the spatial dimensions
- nn.MaxPool2d(kernel_size = 2)
![[Pasted image 20250722152944.png]]![[Pasted image 20250722153022.png]]
No data augmentation in the test time
except the totensor and resize

### Evaluation
```python
from torchmetrics import Recall

recall_per_class = Recall(task = "multiclass",num_classes = 7,average = None)
recall_micro = Recall(task = "multiclass",num_classes = 7,average = "micro")
recall_macro = Recall(task = "multiclass",num_classes = 7,average = "macro")
recall_weighted = Recall(task = "multiclass",num_classes = 7,average = "weighted")
```

micro -> imbalanced datasets
mcro -> care about the performance on small classes 
weighted -> consider errors in larger classes as more important
![[Pasted image 20250722155328.png]]![[Pasted image 20250722155443.png]]![[Pasted image 20250722155450.png]]

