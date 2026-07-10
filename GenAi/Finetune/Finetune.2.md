Think of fine-tuning as creating a specialized expert out of a generalist model. Some debate whether to use Retrieval-Augmented Generation (RAG) instead of fine-tuning, but fine-tuning can incorporate knowledge and behaviors directly into the model in ways RAG cannot. In practice, combining both approaches yields the best results - leading to greater accuracy, better usability, and fewer hallucinations.

### Real-World Applications of Fine-Tuning
Fine-tuning can be applied across various domains and needs. Here are a few practical examples of how it makes a difference:
- **Sentiment Analysis for Finance** – Train an LLM to determine if a news headline impacts a company positively or negatively, tailoring its understanding to financial context.
- **Customer Support Chatbots** – Fine-tune on past customer interactions to provide more accurate and personalized responses in a company’s style and terminology.
- **Legal Document Assistance** – Fine-tune on legal texts (contracts, case law, regulations) for tasks like contract analysis, case law research, or compliance support, ensuring the model uses precise legal language.

Fine-tuning deeply integrates domain knowledge into the model. This makes it highly effective at handling structured, repetitive, or nuanced queries, scenarios where RAG-alone systems often struggle. In other words, a fine-tuned model becomes a specialist in the tasks or content it was trained on.

- Task Specific Mastery
- Independence from Retrieval
- Faster Responses
- Custom Behavior and Tone
- Reliable Performance

### Does Fine-Tuning Add New Knowledge to a Model?
**Yes - it absolutely can.** A common myth suggests that fine-tuning doesn’t introduce new knowledge, but in reality it does. If your fine-tuning dataset contains new domain-specific information, the model will learn that content during training and incorporate it into its responses.

### Is RAG Always Better Than Fine-Tuning?
**Not necessarily.** Many assume RAG will consistently outperform a fine-tuned model, but that’s not the case when fine-tuning is done properly. In fact, a well-tuned model often matches or even surpasses RAG-based systems on specialized tasks.

Instruct Models
Instruct models are pre-trained with built-in instructions, making them ready to use without any fine-tuning.

Base models, on the other hand, are the original pre-trained versions without instruction fine-tuning. These are specifically designed for customization through fine-tuning, allowing you to adapt them to your unique needs.

- Large dataset -> Base Model
- small datasets -> Instruct Model

Fine-tuning the instruct model enables it to align with specific needs while preserving its built-in instructional capabilities. This ensures it can follow general instructions without additional input unless you intend to significantly alter its functionality.

### Fine-tuning Hyperparamters
Learning rate
Defines how much the model’s weights are adjusted during each training step.
- **Higher Learning Rates**: Lead to faster initial convergence but can cause training to become unstable or fail to find an optimal minimum if set too high.
- **Lower Learning Rates**: Result in more stable and precise training but may require more epochs to converge, increasing overall training time. While low learning rates are often thought to cause underfitting, they actually can lead to **overfitting** or even prevent the model from learning.
- **Typical Range**: `2e-4` (0.0002) to `5e-6` (0.000005). 🟩 _**For normal LoRA/QLoRA Fine-tuning**_, _we recommend_ `**2e-4**` _as a starting point._ 🟦 _**For Reinforcement Learning**_ _(DPO, GRPO etc.), we recommend_ `**5e-6**` **.** ⬜ _**For Full Fine-tuning,**_ _lower learning rates are generally more appropriate._

Epochs 
More epochs -> Can help the model learn better but the model can memorize the training data
Fewer epochs -> reduces training time and can prevent overfiiting
Recommended -> 1-3 epochs.

LoRA vs QLoRA
LoRA uses 16-bit precision, while QLoRA is a 4-bit fine-tuning method.
- **LoRA:** 16-bit fine-tuning. It's slightly faster and slightly more accurate, but consumes significantly more VRAM (4× more than QLoRA). Recommended for 16-bit environments and scenarios where maximum accuracy is required.
- **QLoRA:** 4-bit fine-tuning. Slightly slower and marginally less accurate, but uses much less VRAM (4× less).

### 

Hyperparameters & Recommendations:

Hyperparameter

Function

Recommended Settings

**LoRA Rank** (`r`)

Controls the number of trainable parameters in the LoRA adapter matrices. A higher rank increases model capacity but also memory usage.

8, 16, 32, 64, 128 Choose 16 or 32

**LoRA Alpha** (`lora_alpha`)

Scales the strength of the fine-tuned adjustments in relation to the rank (`r`).

`r` (standard) or `r * 2` (common heuristic). [More details here](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide#lora-alpha-and-rank-relationship).

**LoRA Dropout**

A regularization technique that randomly sets a fraction of LoRA activations to zero during training to prevent overfitting. **Not that useful**, so we default set it to 0.

0 (default) to 0.1

**Weight Decay**

A regularization term that penalizes large weights to prevent overfitting and improve generalization. Don't use too large numbers!

0.01 (recommended) - 0.1

**Warmup Steps**

Gradually increases the learning rate at the start of training.

5-10% of total steps

**Scheduler Type**

Adjusts the learning rate dynamically during training.

`linear` or `cosine`

**Seed (**`**random_state**`**)**

A fixed number to ensure reproducibility of results.

Any integer (e.g., `42`, `3407`)

**Target Modules**

Specify which parts of the model you want to apply LoRA adapters to — either the attention, the MLP, or both.

Attention: `q_proj, k_proj, v_proj, o_proj` MLP: `gate_proj, up_proj, down_proj`

Recommended to target all major linear layers: `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`.

batch_size (batch_size) -> Recommended : 2
gradient_accumulation_steps -> Recommended : 8
**Effective Batch Size** (Calculated) -> 4 to 16 Recommended: 16 (from 2 * 8)

of the following configurations:
- `batch_size = 32, gradient_accumulation_steps = 1`
- `batch_size = 16, gradient_accumulation_steps = 2`
- `batch_size = 8, gradient_accumulation_steps = 4`
- `batch_size = 4, gradient_accumulation_steps = 8`
- `batch_size = 2, gradient_accumulation_steps = 16`
- `batch_size = 1, gradient_accumulation_steps = 32`

The first configuration (`batch_size = 32`) uses the **most VRAM** and will likely fail on most GPUs. The last configuration (`batch_size = 1`) uses the **least VRAM,** but at the cost of slightly slower training**.**

Overfitting:
**Solution:**
- **Adjust the learning rate:** A high learning rate often leads to overfitting, especially during short training runs. For longer training, a higher learning rate may work better. It’s best to experiment with both to see which performs best.
- **Reduce the number of training epochs**. Stop training after 1, 2, or 3 epochs.
- **Increase** `weight_decay`. A value of `0.01` or `0.1` is a good starting point.
- **Increase** `lora_dropout`. Use a value like `0.1` to add regularization.
- **Increase batch size or gradient accumulation steps**.
- **Dataset expansion** - make your dataset larger by combining or concatenating open source datasets with your dataset. Choose higher quality ones.
- **Evaluation early stopping** - enable evaluation and stop when the evaluation loss increases for a few steps.
- **LoRA Alpha Scaling** - scale the alpha down after training and during inference - this will make the finetune less pronounced.
- **Weight averaging** - literally add the original instruct model and the finetune and divide the weights by 2.

Underfitting:
**Solution:**
- **Adjust the Learning Rate:** If the current rate is too low, increasing it may speed up convergence, especially for short training runs. For longer runs, try lowering the learning rate instead. Test both approaches to see which works best.
- **Increase Training Epochs:** Train for more epochs, but monitor validation loss to avoid overfitting.
- **Increase LoRA Rank** (`r`) and alpha: Rank should at least equal to the alpha number, and rank should be bigger for smaller models/more complex datasets; it usually is between 4 and 64.
- **Use a More Domain-Relevant Dataset**: Ensure the training data is high-quality and directly relevant to the target task.
- **Decrease batch size to 1**. This will cause the model to update more vigorously.
### Training
We generally recommend keeping the default settings unless you need longer training or larger batch sizes.

- `**per_device_train_batch_size = 2**` – Increase for better GPU utilization but beware of slower training due to padding. Instead, increase `gradient_accumulation_steps` for smoother training.
- `**gradient_accumulation_steps = 4**` – Simulates a larger batch size without increasing memory usage.
- `**max_steps = 60**` – Speeds up training. For full runs, replace with `num_train_epochs = 1` (1–3 epochs recommended to avoid overfitting).
- `**learning_rate = 2e-4**` – Lower for slower but more precise fine-tuning. Try values like `1e-4`, `5e-5`, or `2e-5`.