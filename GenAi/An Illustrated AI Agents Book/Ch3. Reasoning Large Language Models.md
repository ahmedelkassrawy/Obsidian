Reasoning in LLMs attempts to mimic human thinking by generating thoughts through tokens before giving a final answer.

Reasoning steps or thought processes

![[Pasted image 20261102191133.png]]

Nonreasoning LLMs operate much like System 1 thinking and generate responses quickly based on patterns they learned during training. They produce immediate answers without step-by-step (explicit) thinking

Reasoning LLMs operate much like System 2 thinking and generate more deliberate step-by-step analyses before reaching conclusions. They explicitly work through problems and catch errors that a nonreasoning LLM might miss.

Reasoning is critical in AI agents because it allows them to plan out behavior, decide which actions to take, and reflect on the actions they have taken

AI agents need reasoning to devise a plan, decide on the actions they take, and reflect on the results. This is especially true for planning out actions and reflecting on them.

we uncover the history of reasoning LLMs through an important paradigm shift from training to inference and explore various methods for creating reasoning LLMs.

### The paradigm shift from TrainTime Compute to TestTime Compute
we changed our focus from scaling traintime compute to testtime compute

To improve the performance of LLMs during pre-training, developers used to focus on three main factors:
- Inc model size (num of params)
- Inc dataset size (num of tokens)
- Inc compute (num of floating point operations per second --- FLOPS)

This combination of factors called -> traintime compute
basic principle is that more pre training resources lead to a better , more powerful model

- You can see how both data and compute can also be increased to improve its performance. 
- When you fine-tune a model, you can often decide how many of its parameters you would like to update. 
- In a way, even during post-training, you can increase the “model size.

TrainTime compute means a focus on inc pre-training and post-training resources and little attention is spent on inference, especially non reasoning LLMs

![[Pasted image 20261102232037.png]]

- In contrast, testtime compute focuses more on scaling inference instead of pre-training and post-training. 
- Scaling inference generally applies to reasoning LLMs and allows them to “think longer” during inference.

![[Pasted image 20261102232234.png]]

- The underlying idea is that the more tokens you generate, the better the resulting performance will be. 
- However, you cannot just produce many random tokens to get a better output. 
- Instead, tokens need to be generated that, for instance, contain additional relationships and new thoughts about the original problem.

![[Pasted image 20261102232939.png]]

To sum up
- traintime compute focuses on scaling resources (e.g., data and compute) spent during pre-training and post-training,
- while testtime compute focuses on scaling resources (e.g., compute) spent during inference

![[Pasted image 20261102233025.png]]

Why has there been a paradigm shift from scaling traintime compute to testtime compute?

Scaling Laws
the relationshhs between the model scale and performance follow the scalling lows and power laws 
power laws say that each doubling of soemthing gives smaller gain than the previous doubling

Jared Kaplan found that a model’s performance improves predictably as you increase compute, dataset size, and parameters, but with diminishing returns. It follows the same powerlaw form just described.

For a fixed compute budget, the best strategy was to keep increasing the model size and train on as much data as possible without overfitting.

they showed that models were often undertrained and that for a fixed compute budget, it’s better to use a smaller model and train it on much more data

Performance of models can be improved with things other than compute, data, and model sizes

![[Pasted image 20261102234848.png]]

testtime compute turned out to be a prime candidate to continue scaling LLMs. Although scaling laws for testtime compute are relatively unexplored, there are several interesting sources comparing scaling traintime compute with testtime compute

First, a post by OpenAI detailed that increasing testtime compute might affect performance the same as increasing traintime compute. 
- They defined the traintime compute as more reinforcement learning (RL)
- the testtime compute as more time spent thinking

Likewise, for the best performance, both forms of compute should be increased together

That made the paradigm shift that happend in 2024/25 all point that the signifcant beneift of scaling testtime compute, instead of focusing purely on traintime compute (pre-training and fine tuning), these reasoning models intead balance training with inference''

more test-time compute -> less train-time compute needed

Testtime compute doesn’t necessarily mean scaling-only thinking; it refers to scaling time and compute spent on inference. Instead of thinking longer, we could also generate many different answers and vote on the best one. By creating more answers, we could likewise scale time to run inference, and stabilize and improve on the output.