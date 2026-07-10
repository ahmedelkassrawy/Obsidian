# Transfer Learning

**Transfer Learning** is a technique where a model trained on one task is reused for a different, but related task. Instead of training from scratch, we leverage pre-trained models that have learned useful features on large datasets (e.g., ImageNet).

## How Transfer Learning Works

### 1. Use a Pre-trained Model
Models like [[ResNet]], [[VGG]], or [[Inception]] are trained on large datasets. They have already learned to detect general features (e.g., edges, textures).

### 2. Freeze Early Layers
Freeze the earlier layers of the pre-trained model since they contain general features useful for many tasks. This prevents the weights from being updated during initial training.

![[Pasted image 20260424165947.png]]
### 3. Fine-tune the Last Layers
Replace the final layers (classifier layers) with new layers suited for your specific task. Fine-tune these new layers on your specific dataset.

![[Pasted image 20260424170015.png]]

---
# Hyperparameter Tuning

Hyperparameters are settings used to control the learning process. **Hyperparameter Tuning** involves finding the best combination of values to improve model performance.

## Common Hyperparameters to Tune

| Hyperparameter | Description | Effect of High Value | Effect of Low Value |
| :--- | :--- | :--- | :--- |
| **Learning Rate** | Controls the step size during optimization. | Overshoot optimal weights; instability. | Slow convergence; getting stuck. |
| **Batch Size** | Samples processed before a weight update. | More stable gradients, but higher memory use. | Noisier gradients, but sometimes better generalization. |
| **Number of Neurons/Layers** | Complexity of the model architecture. | Captures complex features, but risks **[[Overfitting]]**. | Underfitting; fails to learn data patterns. |
| **Dropout Rate** | % of neurons randomly dropped during training. | Prevents overfitting, but too high leads to underfitting. | Minor regularization effect. |
![[Pasted image 20260424170225.png]]

![[Pasted image 20260424170238.png]]

![[Pasted image 20260424170301.png]]

---
# Early Stopping & Model Checkpointing

## Early Stopping
Early stopping is a regularization technique used to avoid [[Overfitting]]. It monitors a performance metric (e.g., validation loss) and stops training if the metric stops improving after a set number of epochs.

> [!abstract] Key Parameters
> - **Patience:** The number of epochs to wait after the last improvement before stopping.
> - **Restore Best Weights:** Ensures the model's weights are reverted to the epoch with the best validation performance, even if training stopped later due to patience.

## Model Checkpointing
Model checkpointing saves the model's weights after each epoch where the validation performance improves. This guarantees you always have the best model saved, even if training runs for many epochs and overfits later.

> [!check] Benefits
> - **Early Stopping:** Prevents overfitting by avoiding unnecessary epochs; saves time and resources.
> - **Model Checkpointing:** Ensures you always possess the best-performing model state during training, safeguarding against later deterioration.

---
## Key Takeaways

1.  **[[#Transfer Learning]]:** Leverage pre-trained models for faster and more accurate training on specific tasks.
2.  **[[#Hyperparameter Tuning]]:** Optimize model performance by searching for the best hyperparameters using techniques like [[Random Search]] or [[Grid Search]].
3.  **[[#Early Stopping Model Checkpointing|Early Stopping & Checkpointing]]:** Prevent overfitting and save the best model during training for better generalization.
