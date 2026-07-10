## DSPy Optimization Workflow — Key Points

### **1. Build proper datasets**
* Expand from a dev set to **train**, **validation**, and **test** sets.
* Training set can start small (~30 examples), but aim for **300+ examples** for better results.
* Different optimizers require:

  * **trainset only**, or
  * **trainset + valset**.

### **2. Recommended dataset splits**
* For most **prompt-based optimizers**:

  * **20% train**, **80% validation** ← unusual but preferred to prevent overfitting.
* For **dspy.GEPA optimizer**:

  * Use a **large training set** and a **small validation set**, like standard ML practice.

### **3. After initial optimization runs**

* If you're unhappy with the outcome, revisit key design decisions:

  * **Is the task defined correctly?**
  * **Do you need more or better data?**
  * **Should you update the evaluation metric?**
  * **Should you use a more advanced optimizer?**
  * **Should you incorporate DSPy Assertions?**
  * **Does your DSPy program need additional steps or complexity?**
  * **Would running multiple optimizers sequentially help?**
---
### DSPy Optimizers
A **DSPy optimizer** is an algorithm that can tune the parameters of a DSPy program (i.e., the prompts and/or the LM weights) to maximize the metrics you specify, like accuracy.

A typical DSPy optimizer takes three things:

- Your **DSPy program**. This may be a single module (e.g., `dspy.Predict`) or a complex multi-module program.
    
- Your **metric**. This is a function that evaluates the output of your program, and assigns it a score (higher is better).
    
- A few **training inputs**. This may be very small (i.e., only 5 or 10 examples) and incomplete (only inputs to your program, without any labels).
---
## What does a DSPy Optimizer tune? How does it tune them?

Different optimizers in DSPy will tune your program's quality by **synthesizing good few-shot examples** for every module, like `dspy.BootstrapRS`  **proposing and intelligently exploring better natural-language instructions** for every prompt, like `dspy.MIPROv2` and `dspy.GEPA`, and **building datasets for your modules and using them to finetune the LM weights** in your system, like `dspy.BootstrapFinetune`.

Here is a **clear explanation** of DSPy optimizers and how **dspy.MIPROv2** works, broken down into simple concepts.

---
### **What is a DSPy Optimizer?**

A **DSPy optimizer** is a tool that automatically improves your DSPy program by tuning:

* Prompt instructions
* Module inputs/outputs
* Internal weights (if using parametric models)
* Program structure (in some advanced optimizers)

DSPy optimizers search for better *instructions* or *configurations* that maximize **your evaluation metric** on a train/val dataset.

They're like AutoML—but for prompt pipelines and program-level LLM systems.

---
### **Example Optimizer: `dspy.MIPROv2`**

MIPROv2 is one of the most powerful DSPy prompt optimizers.
It works in **three major stages**:

---
## **1️⃣ Bootstrapping Stage — Collect good traces**

What it does:

* Runs your DSPy program many times across diverse training inputs.
* Collects **execution traces** for each module (intermediate inputs/outputs).
* Scores each trajectory using your metric.
* Keeps only the **high-scoring traces**.

Purpose:

* To understand *how* your current program behaves.
* To identify examples of good reasoning and useful module sequences.

Think of it as gathering "demonstration data" automatically from the program itself.

---

## **2️⃣ Grounded Proposal Stage — Generate better instructions**

What it does:
* Looks at:

  * Your DSPy program code
  * Your dataset
  * The high-quality traces from step 1
* Generates **many possible candidate instructions** for each module’s prompt.

Purpose:
* To propose improved prompt templates that better guide the LLM.
* These proposals are "grounded" in real data and real executions.

The optimizer is literally rewriting prompts based on how the program behaves.

---

## **3️⃣ Discrete Search Stage — Test and refine**

What it does:
* Samples mini-batches from the training set.
* For each candidate instruction set:

  * Builds a fully updated DSPy program.
  * Runs it on the mini-batch.
  * Scores the results.
* Updates a **surrogate model** that learns which proposals are promising.

Purpose:
* To search the combinatorial space of prompts efficiently.
* To find the best-performing program configuration.

This stage iteratively improves instruction proposals based on performance.

---
### **Why DSPy optimizers are powerful**

DSPy optimizers can be **composed** like Lego pieces.
### ✔ Run MIPRO twice

You can run:

```
MIPROv2 → optimized program → MIPROv2 again
```

to refine prompts further — because each run produces better traces and proposals.

### ✔ Combine different optimizers
Example:

```
MIPROv2 → BootstrapFinetune
```

MIPRO improves prompts, then BootstrapFinetune fine-tunes a model using them.
This idea is formalized as **dspy.BetterTogether**, which encourages chaining optimizers.
### ✔ Ensemble top programs
Instead of picking one best program, you can:
* Take top-k optimized programs
* Build a `dspy.Ensemble`
* Use more inference compute for higher accuracy
This mirrors ML ensembling techniques (like random forests or top-k checkpoints).
---
#### **In simple terms**
* DSPy optimizers study your program.
* They generate better prompts and instructions.
* They test those candidates automatically.
* They select the best-performing program.
* You can chain optimizers or ensemble programs for even stronger results.
---
## What DSPy Optimizers are currently available?
Optimizers can be accessed via `from dspy.teleprompt import *`.

Here’s a clean bullet-point summary of the **Automatic Few-Shot Learning** optimizers in DSPy:

---
## ** Automatic Few-Shot Learning — Summary**

These optimizers **automatically generate optimized few-shot examples** and insert them into your prompts.

---
## **1. LabeledFewShot**
* Builds few-shot demos **directly from labeled data** (input → output pairs).
* Requires:

  * **k** = number of examples to include in the prompt.
  * **trainset** = pool to randomly draw examples from.
* Very simple: **random k examples → added to prompt**.
---
## **2. BootstrapFewShot**
* Uses a **teacher module** (default = your current program) to generate demonstrations.
* Sources demos from:
	-  **max_labeled_demos** (from trainset)
	- **max_bootstrapped_demos** (generated by the teacher)
  
* Uses your **metric** to keep only high-quality demonstrations.
* Supports using a **different program as the teacher** for harder tasks.
* Produces a “compiled prompt” containing validated examples for every stage.
---
## **3. BootstrapFewShotWithRandomSearch**

* Runs **BootstrapFewShot repeatedly**, but with random variations in the examples.
* Performs **random search** over:

  * Unoptimized program
  * LabeledFewShot program
  * BootstrapFewShot program
  * Additional randomized-demo programs

* Parameter:
  * **num_candidate_programs** = number of demo-set variations to evaluate.
* Selects the **best-performing** program at the end.
---
## **4. KNNFewShot**

* Uses **k-Nearest Neighbors** to select the **closest examples** to each input.
* These nearest examples form the training set for **BootstrapFewShot**.
* Combines retrieval (KNN) + bootstrapped optimization.
---
---
---
# ** Automatic Instruction Optimization — Summary**

These optimizers automatically generate and refine **instructions** for your prompts.
*MIPROv2* additionally optimizes **few-shot demonstrations**.

---
## **1. COPRO**
* Generates and refines new instructions for each module step.
* Uses **coordinate ascent (hill-climbing)** guided by:
  * Your metric
  * Your trainset
  
* Parameter:
  * **depth** → number of iterations of improvement.
---
## **2. MIPROv2**
* Optimizes:
  * **Instructions**
  * **Few-shot demonstrations**

* Data-aware + demo-aware instruction generation.
* Uses **Bayesian Optimization** to efficiently explore the search space.
* One of the most powerful DSPy optimizers.
---
## **3. SIMBA**

* Uses **stochastic mini-batch sampling** to find challenging examples with high variability.

* LLM analyzes failures and produces:
  * Self-reflective improvement rules, or
  * Additional helpful demonstrations.

* Focuses on introspective error-driven refinement.
---
## **4. GEPA**
* LLM reflects on full program trajectories to identify:
  * What worked
  * What failed
  * What needs to be improved
  
* Produces targeted prompt improvements addressing specific gaps.
* Can incorporate **domain-specific textual feedback**.
* DSPy provides detailed tutorials under **dspy.GEPA Tutorials**.
---
### Automatic Finetuning

This optimizer is used to fine-tune the underlying LLM(s).
1. **`BootstrapFinetune`**: Distills a prompt-based DSPy program into weight updates. The output is a DSPy program that has the same steps, but where each step is conducted by a finetuned model instead of a prompted LM. [See the classification fine-tuning tutorial](https://dspy.ai/tutorials/classification_finetuning/) for a complete example.

### Program Transformations
1. **`Ensemble`**: Ensembles a set of DSPy programs and either uses the full set or randomly samples a subset into a single program.
---
#### Which optimizer should I use?

Ultimately, finding the ‘right’ optimizer to use & the best configuration for your task will require experimentation. Success in DSPy is still an iterative process - getting the best performance on your task will require you to explore and iterate.

That being said, here's the general guidance on getting started:

- If you have very few examples (around 10), start with BootstrapFewShot.
- If you have more data (50 examples or more), try BootstrapFewShotWithRandomSearch.
- If you prefer to do instruction optimization only (i.e. you want to keep your prompt 0-shot), use MIPROv2 configured for 0-shot optimization.
- If you’re willing to use more inference calls to perform longer optimization runs (e.g. 40 trials or more), and have enough data (e.g. 200 examples or more to prevent overfitting) then try MIPROv2.
- If you have been able to use one of these with a large LM (e.g., 7B parameters or above) and need avery **efficient program**, finetune a small LM for your task with `BootstrapFinetune`.
---
#### How do I use an Optimizer?
```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

# Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 8-shot examples of your program's steps.
# The optimizer will repeat this 10 times (plus some initial attempts) before selecting its best attempt on the devset.
config = dict(max_bootstrapped_demos=4, max_labeled_demos=4, num_candidate_programs=10, num_threads=4)

teleprompter = BootstrapFewShotWithRandomSearch(metric=YOUR_METRIC_HERE, **config)
optimized_program = teleprompter.compile(YOUR_PROGRAM_HERE, trainset=YOUR_TRAINSET_HERE)
```
---
#### Optimizing prompts for a ReAct Agent
```python
import dspy
from dspy.datasets import HotPotQA

dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

def search(query: str) -> list[str]:
    """Retrieves abstracts from Wikipedia."""
    results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
    return [x['text'] for x in results]

trainset = [x.with_inputs('question') for x in HotPotQA(train_seed=2024, train_size=500).train]
react = dspy.ReAct("question -> answer", tools=[search])

tp = dspy.MIPROv2(metric=dspy.evaluate.answer_exact_match, auto="light", num_threads=24)
optimized_react = tp.compile(react, trainset=trainset)
```
#### Optimizing prompts for RAG
Given a retrieval index to search, your favorite dspy.LM, and a small trainset of questions and ground-truth responses, the following code snippet can optimize your RAG system with long outputs against the built-in dspy.SemanticF1 metric, which is implemented as a DSPy module.
```python
class RAG(dspy.Module):
    def __init__(self, num_docs=5):
        self.num_docs = num_docs
        self.respond = dspy.ChainOfThought('context, question -> response')

    def forward(self, question):
        context = search(question, k=self.num_docs)   # not defined in this snippet, see link above
        return self.respond(context=context, question=question)

tp = dspy.MIPROv2(metric=dspy.SemanticF1(), auto="medium", num_threads=24)
optimized_rag = tp.compile(RAG(), trainset=trainset, max_bootstrapped_demos=2, max_labeled_demos=2)
```

#### Optimizing weights for Classification
Dataset setup code:
```python
import random
from typing import Literal
from datasets import load_dataset
import dspy
from dspy.datasets import DataLoader

# Load the Banking77 dataset.
CLASSES = load_dataset("PolyAI/banking77", split="train", trust_remote_code=True).features["label"].names
kwargs = {"fields": ("text", "label"), "input_keys": ("text",), "split": "train", "trust_remote_code": True}

# Load the first 2000 examples from the dataset, and assign a hint to each *training* example.
trainset = [
    dspy.Example(x, hint=CLASSES[x.label], label=CLASSES[x.label]).with_inputs("text", "hint")
    for x in DataLoader().from_huggingface(dataset_name="PolyAI/banking77", **kwargs)[:2000]
]
random.Random(0).shuffle(trainset)
```

```python
import dspy
lm=dspy.LM('openai/gpt-4o-mini-2024-07-18')

# Define the DSPy module for classification. It will use the hint at training time, if available.
signature = dspy.Signature("text, hint -> label").with_updated_fields('label', type_=Literal[tuple(CLASSES)])
classify = dspy.ChainOfThought(signature)
classify.set_lm(lm)

# Optimize via BootstrapFinetune.
optimizer = dspy.BootstrapFinetune(metric=(lambda x, y, trace=None: x.label == y.label), num_threads=24)
optimized = optimizer.compile(classify, trainset=trainset)

optimized(text="What does a pending cash withdrawal mean?")

# For a complete fine-tuning tutorial, see: https://dspy.ai/tutorials/classification_finetuning/
```

```
Prediction(
    reasoning='A pending cash withdrawal indicates that a request to withdraw cash has been initiated but has not yet been completed or processed. This status means that the transaction is still in progress and the funds have not yet been deducted from the account or made available to the user.',
    label='pending_cash_withdrawal'
)
```
---
#### Saving and loading optimizer output
After running a program through an optimizer, it's useful to also save it. At a later point, a program can be loaded from a file and used for inference. For this, the load and save methods can be used.

```python
optimized_program.save(YOUR_SAVE_PATH)
```

The resulting file is in plain-text JSON format. It contains all the parameters and steps in the source program. You can always read it and see what the optimizer generated.

To load a program from a file, you can instantiate an object from that class and then call the load method on it.

```python
loaded_program = YOUR_PROGRAM_CLASS()
loaded_program.load(path=YOUR_SAVE_PATH)
```