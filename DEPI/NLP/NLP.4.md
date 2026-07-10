[machine-translation-using-seq2seq-model (1).ipynb - Colab](https://colab.research.google.com/drive/1md2gXefVArfOWNWAyRa0Q8wKOyGl9v-6?usp=sharing#scrollTo=noDNi_wWIG8D)
# Sequence to Sequence Models for Machine Translation

> The seq2seq architecture can be broken down into 2 sub models - the encoder and the decoder. The encoder takes in the input sequence and processes it whereas the decoder takes the output of the encoder and uses this to output a new sequence.

> [!info] RNN Variants
> The RNN cells can be either plain, GRU or LSTM as this doesn't change the architecture

![[Pasted image 20260503172042.png]]

Observe how the intermediate outputs of the encoder are not used at all in this setup. The only thing that gets passed to the decoder is the **final hidden state**, which can be thought of as an embedding of the input sequence.

The first step of the decoder takes in the encoder embedding and a beginning of sentence token. It uses this to generate an output that is passed through a softmax function to produce a probability distribution over the target language vocabulary. The most probable word is selected as the prediction, which is then fed in as the input for the next time step of the decoder and the process repeats.

> [!note] Conditional Language Model
> Because the decoder makes predictions based on the encoder output, this is considered a **conditional language model**. This is trained using a self-supervised **teacher forcing** approach. That is, we get it to predict the next word in the sequence given the correct previous words in the translation. Backpropagation is used to update the weights of the encoder and decoder simultaneously, i.e. it is treated as a single system.

![[Pasted image 20260503172256.png]]

## RNN Advantages and Disadvantages

### Advantages
- **Flexible Input Length:** They can process inputs of any length
- **Constant Model Size:** The size of the model does not increase as the input length increases
- **Long-term Theoretical Memory:** In theory, computation for step $t$ can utilize information from many preceding steps
- **Shared Parameters:** Weights and representations are shared across all timesteps

### Disadvantages
- **Slow Speed:** Recurrent computation is slow
- **Practical Memory Limitations:** In practice, it is difficult for the model to access information from many steps back

![[Pasted image 20260503172504.png]]

## How an RNN Language Model is Trained

The primary goal of a language model is to predict the next word in a sequence given the preceding words.

### 1. The Input Layer (Bottom)
- **Corpus ($c_1, c_2, c_3, c_4$):** The process starts with a sequence of words from your training data (e.g., "the", "students", "opened", "their")
- **Embeddings ($W_e$):** Each word is transformed into a continuous vector representation by being multiplied by an embedding weight matrix $W_e$

### 2. The Recurrent Hidden State (Middle)
This is the core "memory" of the RNN.

- **Hidden State ($h^{(t)}$):** At each time step $t$, the network computes a hidden state
- To compute $h^{(1)}$, the network takes the embedded input for "the" and combines it with an initial (usually zero) hidden state $h^{(0)}$
- To compute $h^{(2)}$, it takes the input for "students" and combines it with $h^{(1)}$
- **Shared Weights ($W_h$):** The same $W_h$ (and $W_e$) is used at every time step

### 3. The Output Layer (Top)
- **Predictions ($\hat{y}^{(t)}$):** At every time step, $h^{(t)}$ is multiplied by output weight matrix $W_2$ to produce $\hat{y}^{(t)}$
- $\hat{y}^{(t)}$ represents the predicted probability distribution over the entire vocabulary for the *next* word

### 4. Loss Calculation (Topmost)
- **Loss ($J^{(1)}(\theta)$):** The model calculates an error by comparing $\hat{y}^{(1)}$ to the actual target word ("students")
- $J^{(1)}(\theta)$ is the **"negative log prob of 'students'"** (Cross-Entropy Loss)

### Training Loop Summary
The model processes the sequence, generates predictions at each step, and calculates the loss $J^{(t)}(\theta)$ for each prediction. The total loss for the sequence is typically the sum or average of these individual step losses. Once calculated, the network uses **Backpropagation Through Time** to adjust all the shared weights ($W_e, W_h, W_2$).

---

## Machine Translation Challenges

Machine Translation is a very challenging problem because different languages can express the same concept in different ways:

- **Word alignment** - a word in one language may be expressed as 2 words in another language and vice versa
- **Word order structure** - English is SVO whereas Japanese is SOV. So "Joe ate cake" becomes "Joe cake ate"
- **Adequacy vs fluency** - many ways to express the same information, but some sound more natural
- **Bias** - very large sets of diverse training data are needed to train accurate and unbiased models

## Neural Machine Translation (NMT)

> [!def] NMT
> Neural Machine Translation is a way to do Machine Translation with a single neural network. The neural network architecture is called **sequence-to-sequence** (aka seq2seq)

![[Pasted image 20260503172706.png]]
![[Pasted image 20260503183901.png]]

### NMT Architecture & Test Time

- **The Encoder RNN:** Reads the source sentence one word at a time, updating its internal hidden state. The final hidden state acts as a compressed "encoding" of the entire source sentence
- **The Decoder RNN:** A language model conditioned on the Encoder. Takes the compressed encoding as its starting point
- **Test Time Behavior:** Given a `<START>` token, outputs a probability distribution and picks the most likely word using `argmax`
- **The Feedback Loop:** The predicted word is fed back as input for the next step (autoregressive loop) until an `<END>` token is produced

### Training the NMT System

- **Different Inputs:** During training, we feed the *actual* correct target words into the decoder at each step (teacher forcing)
- **Calculating Loss:** At each step $t$, we calculate loss $J_t$ by looking at the negative log probability of the *correct* word
- **Total Loss:** $J = \frac{1}{T} \sum_{t=1}^{T} J_t$
- **End-to-End Backpropagation:** Error signals flow backward through both Decoder and Encoder - they are optimized together as a **single system**

---

## Beam Search

> [!warning] Greedy Decoding Limitations
> Greedy decoding (choosing the most probable word at each time step) doesn't necessarily produce the best translations. The second most probable word at the first time step might lead to a better scoring sentence overall.

![[Pasted image 20260503184533.png]]
![[Pasted image 20260503184908.png]]

### Key Parameters

- **Beam Size ($k = 2$):** At every time step, keep only the top $k$ most probable partial sequences (hypotheses)
- **Score:** Cumulative log probability: $\sum_{i=1}^t \log P_{LM}(y_i | y_1, ..., y_{i-1}, x)$

### Step-by-Step Execution

1. **Step 1:** From `<START>`, keep top two: "I" (-0.9) and "he" (-0.7)
2. **Step 2:** Top two cumulative scores: "I was" (-1.6) and "he hit" (-1.7)
3. **Step 3:** Top two: "he hit me" (-2.5) and "he hit a" (-2.8)
   - "I was hit" (-2.9) is pruned
4. **Step 4:** Top two: "he hit me with" (-3.3) and "he hit a pie" (-3.4)
5. **Step 5:** Top two: "he hit me with a" (-3.7) and "he hit me with one" (-4.3)
6. **Step 6:** Final expansions yield highest score for sequence ending in "pie" (-4.3)

> [!tip] Backtracking
> The final step is to **backtrack** from the highest-scoring end node to assemble the complete sentence.

---

## The Bottleneck Problem

When seq2seq models were first experimented with, they performed well for short sequences but struggled with long sentences.

> [!danger] Information Bottleneck
> All information from the input sequence must be compressed into a **single fixed-length vector**. As the input sequence gets longer, there's less space to carry all the complex language information needed for accurate translation.

![[Pasted image 20260503191646.png]]

## Attention Mechanism

Attention provides a solution to the bottleneck problem:

- Allows decoder to look directly at source; bypass bottleneck
- Provides shortcut to faraway states (helps with vanishing gradient problem)
- Significantly improves NMT performance

### Attention Equations

- Encoder hidden states: $h_1, \ldots, h_N \in \mathbb{R}^h$
- On timestep $t$, decoder hidden state: $s_t \in \mathbb{R}^h$

1. **Attention scores** for this step:
   $$e^t = [s_t^T h_1, \ldots, s_t^T h_N] \in \mathbb{R}^N$$

2. **Attention distribution** (softmax, sums to 1):
   $$\alpha^t = \text{softmax}(e^t) \in \mathbb{R}^N$$

3. **Attention output** (weighted sum of encoder hidden states):
   $$a_t = \sum_{i=1}^N \alpha_i^t h_i \in \mathbb{R}^h$$

4. **Concatenate** attention output with decoder hidden state:
   $$[a_t; s_t] \in \mathbb{R}^{2h}$$