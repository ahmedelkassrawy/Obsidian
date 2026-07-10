## Introduction to Deep Learning
### Core Definitions

- Deep learning is a subset of machine learning that utilizes multilayered neural networks to simulate the complex decision-making power of the human brain.
    
- It currently powers the majority of artificial intelligence applications in our daily lives.
    
- The underlying layers of neural networks learn from vast amounts of data.
## Neurons and Perceptrons

### The Artificial Neuron

- Modeled after biological neurons, an artificial neuron is a mathematical function that processes input data to produce an output.
    
- **Inputs (Features):** The data points provided to the neuron, often represented as numbers.
    
- **Weights:** Each input is assigned a positive or negative weight that determines its importance and amplifies or diminishes its effect on the output.
    
- **Bias:** An additional constant term added to the weighted sum to shift the activation function and help the model fit the data better.
    
- **Weighted Sum:** The neuron multiplies each input by its weight and adds them all together.
    
- Mathematically, the weighted sum is expressed as:
    $$z=w_{1}\cdot x_{1}+w_{2}\cdot x_{2}+...+w_{n}\cdot x_{n}+b$$

### The Perceptron
- The perceptron is a single-layer neural network and the simplest form of a neural network.
    
- It utilizes a step function as its activation function to make binary decisions.
    
- The step function outputs 1 if the weighted sum is greater than 0, and 0 otherwise.
    
- **Limitations:** The perceptron can only classify linearly separable data using a straight line or plane. It can handle simple logic like AND/OR gates but fails on more complex problems like XOR. It also lacks hidden layers, limiting its ability to learn abstract patterns.
    
### Evolving into Neural Networks
- Stacking perceptrons creates multi-layer neural networks (Multi-Layer Perceptrons or MLPs) that can learn complex patterns.
    
- Modern networks replace the simple step function with non-linear activation functions.
    
- Introducing non-linearity allows the network to model complex relationships and solve problems that perceptrons cannot, such as XOR.
    
### Common Activation Functions

- **Sigmoid:** Outputs values between 0 and 1, often used in the output layer for binary classification.
    $$\sigma(z)=\frac{1}{1+e^{-z}}$$
- **ReLU (Rectified Linear Unit):** Outputs 0 if the input is negative, and returns the raw input value if positive. It is highly popular for hidden layers.
    $$ReLU(z)=max(0,z)$$
- **Tanh:** Outputs values between -1 and 1, frequently used in hidden layers.
    $$tanh(z)=\frac{e^{z}-e^{-z}}{e^{z}+e^{-z}}$$
---
## Feedforward Neural Networks (FNNs)

### Core Architecture
- Feedforward Neural Networks are the foundation of deep learning models.
    
- Information moves strictly in one direction from the input layer to the output layer, with no loops or feedback connections.
    
- **Input Layer:** Receives the initial feature data.
    
- **Hidden Layers:** Process the data using learned weights; this is where the network learns patterns.
    
- **Output Layer:** Delivers the final prediction or classification.

### Fully Connected Neurons
- In a fully connected layer, every neuron receives input from all neurons in the previous layer and sends its output to every neuron in the subsequent layer.
    
- This design ensures the network utilizes all available information from previous layers for its computations.
### Neuron Operations inside FNNs
- The neuron calculates the weighted sum of its inputs and adds the bias term.
    
- An activation function (like ReLU or Sigmoid) is applied to this result to introduce non-linearity.
    
- The final activated result is passed forward as an input to the neurons in the next sequential layer.

---
## Backpropagation and Gradient Descent

### Overview
- Together, these two techniques allow a neural network to learn from data by minimizing errors and improving predictions over time.
### Backpropagation
- Backpropagation calculates the gradient (partial derivative) of the loss function with respect to every weight in the network.
    
- It uses the chain rule of calculus to propagate the error backward through the network, determining how much each individual weight contributed to the final error.
### Gradient Descent
- Gradient Descent is the optimization algorithm utilized to minimize the loss function.
    
- It updates the weights and biases in the specific direction that will reduce the overall error.
    
- The mathematical rule for updating weights is:
$$w_{new}=w_{old}-\eta\cdot\frac{\partial L}{\partial w}$$

- In this formula, $\eta$ represents the learning rate, which is a small positive number that controls the adjustment step size.
    

### The Complete Training Loop

1. **Forward Pass:** The network uses current weights to make a prediction.
    
2. **Compute Loss:** A loss function (like Mean Squared Error or Cross-Entropy) calculates the error by comparing the prediction to the actual target.
    
3. **Backward Pass (Backpropagation):** The error is pushed backward to calculate the gradients for each weight and bias.
    
4. **Weight Update (Gradient Descent):** The model adjusts its weights based on the calculated gradients to push the loss down.
    
5. **Repeat:** This entire cycle loops for many iterations (epochs) until the loss function reaches a minimum and the model converges.