Parameter-Efficient Fine-Tuning (PEFT)
PEFT methods are techniques used to adapt a massive pre-trained model to a specific task without retraining all billions of its parameters.
### **LoRA (Low-Rank Adaptation)**
- **What it is:** Instead of changing the original weights ($W$) of the model, LoRA adds two tiny, high-speed "sidecar" matrices ($A$ and $B$). The original model is frozen (locked), and only these tiny matrices are trained.
    
- **Usage:** Used when you want "full fine-tuning" performance but only have a single GPU or a small budget

- **Example:** You have a 70B parameter model. Instead of updating 70 billion numbers, you only update about 100 million in the LoRA matrices. It's like adding a small "legal expert" module to a general-purpose AI.
### **QLoRA (Quantized LoRA)**
- **What it is:** An even more efficient version of LoRA. It "compresses" the base model into 4-bit precision (making it much smaller) before adding the LoRA matrices.
    
- **Usage:** The gold standard for "budget" AI training. It allows you to fine-tune massive models on consumer-grade gaming GPUs.
    
- **Example:** Running the fine-tuning of a massive model like Llama-3 70B on a single NVIDIA RTX 3090/4090.
### **Adapters**
- **What it is:** Small new layers inserted _between_ the existing layers of the model. Like LoRA, the original model stays frozen, and only these new "adapter" layers are trained.
    
    +1
    
- **Usage:** Great for multi-tasking. You can have one base model and 10 different small adapter files for 10 different tasks (translation, coding, poetry, etc.).
    
- **Example:** A translation service that uses one base model but swaps in a "French Adapter" or "Japanese Adapter" depending on the user's request.

## Instruction / Supervised Fine-Tuning (SFT)
- **What it is:** This is the process of taking a "Base Model" (which just predicts the next word) and turning it into an "Assistant." You feed it a dataset of **(Prompt, Response)** pairs so it learns how to follow instructions.
    
- **Usage:** To change the _behavior_ or _format_ of a model.
    
- **Example:**
    - **Base Model:** If you type "What is the capital of France?", it might respond with "...and what is the capital of Germany?" because it thinks it's looking at a quiz.
        
    - **After SFT:** It learns that when asked a question, it should provide the answer: "The capital of France is Paris."

## 3. KV Cache (Key-Value Cache)
- **What it is:** A memory optimization trick used during **inference** (when the model is generating text).
    
- **How it works:** When an LLM generates the 10th word in a sentence, it normally has to re-calculate everything about the previous 9 words. The KV Cache "saves" the mathematical representations (Keys and Values) of those 9 words so the model can just look them up instantly.
    
- **Usage:** Essential for speed. Without KV Caching, LLMs would get slower and slower for every word they type.
    
- **Example:** If you ask an LLM to write a long story, KV Caching is what allows it to keep a steady "typing speed." Without it, the first paragraph would be fast, but the tenth paragraph would take minutes per word.