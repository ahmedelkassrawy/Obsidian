```python
import torch
import torch.nn as nn
import torch.optim as optim

# Create a model with one input (distance) and one output (time)
model = nn.Sequential(nn.Linear(1, 1))
```
###### Training
Loss function -> measure how wrong your predictions are.  ex: nn.MSELoss
Optimizer -> adjusts model weight and biases and params based on the errors
```python
loss_function = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)
```

During each epoch, these steps occur:
- optimizer.zero_grad( ): Clears gradients from the previous round. Without this, PyTorch would accumulate adjustments, which could break the learning process.
- outputs = model(input) : Performs the forward pass
- loss = loss_fn(outputs,predictions) : calculates how wrong the predicited is
- loss.backward( ) -> the backward pass , which caluclates exactly how to adjust the weight and bias to reduce the error
- optimizer.step( ) -> updates the model parameters using those calculated adjustments. 

```python
for epoch in range(500):
	optimizer.zero_grad()
	
	outputs = model(input)
	
	loss = loss_fn(outputs,predictions)
	
	loss.backward()
	optimizer.step()
	
	if(epoch + 1) % 50 == 0:
		 print(f"Epoch {epoch + 1}: Loss = {loss.item()}")
```

For predictions:
```python
with torch.no_grad():
    # Convert the Python variable into a 2D PyTorch tensor that the model expects
    new_distance = torch.tensor([[distance_to_predict]], dtype=torch.float32)
    
    predicted_time = model(new_distance)
    
    # Use .item() to extract the scalar value from the tensor for printing
    print(f"Prediction for a {distance_to_predict}-mile delivery: {predicted_time.item():.1f} minutes")

    # Use the scalar value in a conditional statement to make the final decision
    if predicted_time.item() > 30:
        print("\nDecision: Do NOT take the job. You will likely be late.")
    else:
        print("\nDecision: Take the job. You can make it!")
```

----
##### Non linear patterns with Activation functions
```python
model = nn.Sequential(
			nn.Linear(1,3),
			nn.ReLU(),
			nn.Linear(3,1)
		)
```