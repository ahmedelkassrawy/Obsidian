
# Fine-tuning Large Language Models: Fundamentals & Axolotl Tutorial

**Source:** AI anytime YouTube Channel
**Tags:** #LLM #FineTuning #LoRA #QLoRA #Axolotl #MachineLearning

## Overview

This note covers the fundamentals of fine-tuning Large Language Models (LLMs), including the differences between pre-training, fine-tuning, and parameter-efficient techniques like LoRA and QLoRA. It also provides a practical tutorial on using the low-code fine-tuning tool **Axolotl** with a RunPod GPU.

## The Three Approaches to Training LLMs

1.  **Pre-training**
2.  **Fine-tuning**
3.  **LoRA & QLoRA**

### 1. Pre-training

- **Data:** Requires a massive text dataset (terabytes, e.g., trillions of tokens).
- **Process:**
    1.  Identify model architecture.
    2.  Train a tokenizer to handle the data (encoding/decoding).
    3.  Pre-process the dataset using the tokenizer's vocabulary (map tokens to IDs, add special tokens/attention masks).
    4.  The model learns to predict the next word or fill in missing words (Causal Language Modeling vs. Masked Language Modeling).
- **Outcome:** The model captures general language knowledge but lacks specific domain or task knowledge.

### 2. Fine-tuning

- **Goal:** Specialize the pre-trained model's capabilities for a specific downstream task (e.g., instruction following).
- **Data:** Requires a task-specific dataset (e.g., instruction-response pairs).
    - *Note:* This dataset is significantly smaller than pre-training data but should be substantial (e.g., 10,000+ pairs, ~10MB file size).
- **Process:**
    1.  Initialize the model with pre-trained parameters.
    2.  Train on the task-specific dataset using a task-specific loss function.
    3.  Adjust the model's parameters using gradient-based optimization algorithms (e.g., SGD, Adam) via backpropagation.
    4.  Use techniques like learning rate scheduling, dropout, or early stopping to prevent overfitting.
- **Outcome:** A model specialized for a specific task, capable of generalizing to unseen data in that domain.
- **Cost:** Fine-tuning is **expensive**, requiring hundreds of GBs of VRAM.

### 3. LoRA & QLoRA (Parameter-Efficient Fine-Tuning)

#### LoRA (Low-Rank Adaptation)
- **Concept:** A training method that introduces pairs of rank-decomposition weight matrices ("update matrices") while keeping the original pre-trained weights frozen.
- **Advantages:**
    - **Preservation of Pre-trained Weights:** Minimizes catastrophic forgetting.
    - **Portability:** Trained LoRA weights have far fewer parameters and are highly portable.
    - **Memory Efficiency:** Reduces GPU memory requirements by ~3x compared to full fine-tuning.
- **LoRA Hyperparameters:**
    - `lora_r` (Rank): Determines the number of rank-decomposition matrices. Paper recommends `r=8`. Higher rank = better results but more compute.
    - `lora_alpha` (Scaling Factor): Adjusts the contribution of the update matrices. Lower value gives more weight to the original data.
    - `lora_target_modules`: Specifies which weights/matrices to train (e.g., `q_proj`, `v_proj`, `k_proj`, `o_proj`, `lm_head`, `embed_tokens`).

#### QLoRA (Quantized LoRA)
- **Concept:** An even more memory-efficient approach that builds on LoRA.
- **Key Features:**
    - Backpropagation of gradients through a **frozen, 4-bit quantized** model.
    - Uses a new data type: `nf4` (4-bit Normal Float).
    - Uses techniques like **paged optimizers** and **double quantization**.
- **Result:** Enables fine-tuning of very large models (e.g., Llama 2 70B) on much less hardware (e.g., 2x RTX 3090s).

## Training Compute & GPU Rental

- **Memory Requirement for 7B models (estimated):** 150-195 GB for full fine-tuning. QLoRA drastically reduces this.
- **Recommended GPU Rental Providers (in order of preference):**
    1.  **RunPod:** Preferred choice. Easy to use and affordable.
    2.  **Vast.ai:** Cheapest option, but security can be a concern.
    3.  **Lambda Labs:** Good, but support can be bad.
    4.  **AWS SageMaker:** Hyperscaler option.
    5.  **Google Colab:** Life-saver for small experiments.

## Practical Tutorial: Fine-tuning with Axolotl on RunPod

**Axolotl** is a low-code, powerful tool for fine-tuning LLMs. It uses a single YAML config file to manage the entire process.

### Steps:

1.  **Deploy a GPU on RunPod:**
    - Go to RunPod -> Secure Cloud.
    - Select a GPU (e.g., A100 80GB for ~$2/hr).
    - Click "Deploy" and wait for it to spin up.
    - Connect via Jupyter Lab.

2.  **Clone Axolotl Repository:**
    ```bash
    git clone https://github.com/OpenAccess-AI-Collective/axolotl
    cd axolotl
    ```

3.  **Install Dependencies:**
    ```bash
    pip install packaging
    pip install -e '.[flash-attn,deepspeed]'
    ```
    *(This installs packages like `torch`, `transformers`, `bitsandbytes`, `accelerate`, `datasets`, `flash-attn`, etc.)*

4.  **Configure the YAML File:**
    - Navigate to `examples/` and choose a model (e.g., `openllama/`, `mistral/`).
    - Edit the `config.yml` (or `lora.yml`/`qlora.yml`).
    - **Key configurations to change:**
        - `dataset`: Path to your Hugging Face dataset or local file.
        - `base_model`: The pre-trained model ID (e.g., `"openlm-research/open_llama_3b_v2"`).
        - `load_in_4bit`: `true` for QLoRA.
        - `num_epochs`: Set to `1` for a test run.
        - `micro_batch_size`: Set to `1`.
        - `gradient_accumulation_steps`: Set to `8`.
        - `lora_r`, `lora_alpha`, `lora_target_modules`: Define your LoRA parameters.
        - `output_dir`: Where to save the LoRA adapter weights (e.g., `./lora-out`).

5.  **Run Fine-tuning:**
    ```bash
    accelerate launch -m axolotl.cli.train examples/openllama/qlora.yml
    ```
    - The script will download the base model and dataset, then start training.
    - Output (LoRA adapter weights and config) will be saved to the specified `output_dir`.

6.  **Run Inference with Gradio (Optional):**
    ```bash
    accelerate launch -m axolotl.cli.inference examples/openllama/qlora.yml --lora_model_dir='./lora-out'
    ```
    - This spins up a Gradio web interface to test the fine-tuned model.

### Understanding Key Hyperparameters

- **`num_epochs`**: Number of complete passes through the entire training dataset.
- **`batch_size`**: Number of training samples processed before the model's parameters are updated. Larger batch size = higher GPU memory usage.
- **`gradient_accumulation_steps`**: Splits a large global batch into smaller "micro-batches" to simulate a larger batch size without increasing memory usage.
    - *Example:* `global_batch_size = micro_batch_size * gradient_accumulation_steps`
- **`learning_rate`**: Controls the step size taken to improve the model during optimization. Too small = slow learning; too large = unstable learning.

## Summary

This note covered the theory and practice of fine-tuning LLMs. You learned:
1.  The differences between pre-training, fine-tuning, and LoRA/QLoRA.
2.  How to select optimal hyperparameters for a fine-tuning task.
3.  How to use **Axolotl**, a low-code tool, to fine-tune an LLM on a GPU provider like RunPod.

The next step is to experiment with your own datasets and model configurations.
