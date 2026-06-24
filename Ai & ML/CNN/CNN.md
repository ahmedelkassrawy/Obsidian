# Convolutional Neural Networks (CNNs) Concepts
## Image Preprocessing and Convolutional Layers
### Initial Image Dimensions

- Original image size: **427 × 640 pixels**.
- After cropping: **70 × 120 pixels** (height × width).
- Input tensor shape (example with batch size of 2 and 3 color channels):  
    **TensorShape([2, 70, 120, 3])**.

### Convolutional Layer (`Conv2D`)

A `Conv2D` layer applies convolution operations to process 2D inputs (height and width).

#### Example Code

```python
conv_layer = tf.keras.layers.Conv2D(filters=32, kernel_size=7)
```

- **Parameters**:
    - `filters=32`: Produces 32 output feature maps (replacing the 3 input channels).
    - `kernel_size=7`: Uses a 7×7 kernel for convolution.
    - Default `padding="valid"`: No zero padding, causing output size reduction.

#### Output Size with `padding="valid"`

- Input: **TensorShape([2, 70, 120, 3])**.
- Output: **TensorShape([2, 64, 114, 32])**.
    - **Height reduction**: 70 - (7 - 1) = 64 (loses 3 pixels on each side).
    - **Width reduction**: 120 - (7 - 1) = 114 (loses 3 pixels on each side).
    - **Channels**: 3 → 32 (due to 32 filters).

#### Output Size with `padding="same"`

- Example code:
    
    ```python
    conv_layer = tf.keras.layers.Conv2D(filters=32, kernel_size=7, padding="same")
    ```
    
- Input: **TensorShape([2, 70, 120, 3])**.
- Output: **TensorShape([2, 70, 120, 32])**.
    - **Padding**: Adds zeros around the input to maintain the same height and width.
    - **Channels**: 3 → 32 (due to 32 filters).

#### Effect of Stride

- If `stride=2` (with `padding="same"`):
    - Output size is halved in both dimensions.
    - Example: (70, 120) → (35, 60).
    - Output shape: **TensorShape([2, 35, 60, 32])**.
- **Note**: Even with `padding="same"`, a stride > 1 reduces output size.

## Pooling Layers

Pooling layers reduce spatial dimensions (height and width) to:

- Decrease computational load.
- Reduce the number of parameters.
- Limit the risk of overfitting.

### Max Pooling Layer

- Uses a pooling kernel (e.g., 2×2) with an aggregation function (e.g., max).
- **Example**: For inputs [1, 5, 3, 2] in a 2×2 receptive field, only the max value (5) is propagated.
- **Parameters**:
    - Kernel size: 2×2.
    - Stride: 2 (moves 2 pixels at a time).
    - No padding (typically).
- **Effect**:
    - Halves height and width (rounded down).
    - Drops 75% of input values (e.g., 2×2 kernel reduces area by 4x).
- **Output example**: Input (70, 120) → Output (35, 60).

#### Downsides of Max Pooling

- **Destructive**: Discards 75% of input data, potentially losing useful information.
- **Invariance vs. Equivariance**:
    - Max pooling promotes **invariance** (small input changes don’t affect output), which is undesirable for tasks like **semantic segmentation** where **equivariance** (output shifts with input) is needed.

## Typical CNN Architecture

- **Structure**:
    - Stack multiple **convolutional layers** (each followed by a **ReLU** activation).
    - Add a **pooling layer** (e.g., max pooling) to reduce spatial dimensions.
    - Repeat: more convolutional layers (+ReLU), then another pooling layer.
    - Image size shrinks, but depth (number of feature maps) increases due to more filters.
- **Top layers**:
    - A **feedforward neural network** with fully connected layers (+ReLUs).
    - Final layer: Outputs predictions (e.g., **softmax** for class probabilities).

## Summary

- **Convolutional layers**: Apply filters to extract features, with `padding` and `stride` controlling output size.
- **Pooling layers**: Reduce dimensions, but max pooling can be destructive and may not suit tasks requiring equivariance.
- **CNN design**: Alternates convolution and pooling layers, increasing depth while reducing spatial size, culminating in a dense output layer for predictions.