- SGD, Momentum
- Adam / AdamW
- Learning rate scheduling (concept)
## 1️⃣ SGD (Stochastic Gradient Descent)

### 🔹 Concept (idea)

- Update weights using the **current batch gradient**
- Simple rule:  
    _“Move parameters in the direction that reduces loss.”_
- Very **noisy** updates → can jump around the minimum
    

### 🔹 Why use it?
- Noise helps **generalization**
- Very **stable & predictable**
- Less chance of weird training behavior

### 🔹 Use cases

- Classic **CNNs** (ResNet, VGG)
- Large datasets
- When you care about **final generalization**, not speed

### 🔹 When to use SGD

✅ When:
- Dataset is large
- You want best test accuracy
- You have time to tune learning rate


❌ Avoid when:

- Training is unstable
- You need fast convergence

---
## 2️⃣ Momentum (SGD + Momentum)

### 🔹 Concept

Adds **velocity** to SGD:

- Keeps moving in the same direction if gradients agree
- Reduces zig-zag motion

Think of a **ball rolling downhill** 🏀

### 🔹 Why use it?
- Faster than vanilla SGD
- Smoother convergence
- Escapes shallow local minima

### 🔹 Use cases
- Almost **always better than plain SGD**
- CNNs, vision models
### 🔹 When to use
✅ Use when:
- Using SGD
- Loss curve oscillates
- Training is slow

👉 **Rule of thumb**:

> If you use SGD → use Momentum

---
## 3️⃣ Adam

### 🔹 Concept

Adam =
- Momentum (1st moment)
- Adaptive learning rates (2nd moment)

Each parameter gets its **own learning rate**
### 🔹 Why people love it
- Works **out of the box**
- Fast convergence
- Minimal tuning
### 🔹 Use cases
- NLP 
- Transformers
- Small datasets
- Prototyping
### 🔹 When to use Adam
✅ Use when:
- Training Transformers / LLMs
- Dataset is small or noisy
- You want fast results

❌ Be careful:
- Can **overfit**
- Sometimes worse final accuracy than SGD
---
## 4️⃣ AdamW (Adam + correct weight decay)

### 🔹 Concept

Fixes a **flaw in Adam**:
- Separates weight decay from gradient update

This makes regularization **actually work**
### 🔹 Why it’s preferred
- Better generalization than Adam
- Stable training
- Industry standard
### 🔹 Use cases

- Transformers
- Vision Transformers (ViT)
- Modern deep learning
### 🔹 When to use AdamW

✅ Use when:
- Using Adam-like optimizers
- You care about generalization
- Training modern architectures

👉 **Today’s default choice**

---
## 5️⃣ Learning Rate Scheduling (CONCEPT)

### 🔹 Core idea
> Learning rate should **change over time**

Why?
- Large LR → explore
- Small LR → fine-tune
### 🔹 Common schedules (conceptual)
- **Step decay** → reduce at milestones
- **Cosine decay** → smooth annealing
- **Warmup** → start small, then increase
### 🔹 Why it matters
- Prevents divergence
- Improves final accuracy
- Especially important for **SGD & Transformers**

---
## 6️⃣ What to use — quick decision table

| Situation           | Best Choice                      |
| ------------------- | -------------------------------- |
| CNN, large dataset  | **SGD + Momentum + LR schedule** |
| Transformer / NLP   | **AdamW + Warmup + Cosine**      |
| Fast prototyping    | **Adam**                         |
| Best final accuracy | **SGD + Momentum**               |
| Unstable training   | **AdamW**                        |

---
## 🧠 Mental model (remember this)

- **SGD** → slow but strong
- **Momentum** → faster SGD
- **Adam** → fast & easy
- **AdamW** → fast + correct regularization
- **LR schedule** → polish & stability
---