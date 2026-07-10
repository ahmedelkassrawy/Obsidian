# Agents, Planning, Tools, and Memory


## II. Agent Overview

### A. Definition and Characteristics

An **agent** is defined as anything that can perceive its **environment** and act upon that environment.

An agent is characterized by two elements:

1. **The environment** it operates in.
2. **The set of actions** it can perform.

### B. Environment and Actions

The environment of an agent is defined by its use case:

- **Examples of Environments:**
    - If an agent plays a game (e.g., _Minecraft_ or _Go Data_), the game is its environment.
    - If the agent scrapes documents from the internet, the internet is the environment.
    - A self-driving car's environment is the road system and adjacent areas.

The success of an agent depends heavily on the tool inventory it has access to and the strength of its AI planner. The environment determines what tools an agent can potentially utilize.

### C. Agent Goals and Process

An AI agent is intended to accomplish tasks provided by users. The AI agent functions as the **brain** that processes information received from the inputs and feedback from the environment. It then determines a sequence of actions necessary to achieve the task and verify its accomplishment.

## III. Tools: Augmenting Agent Capabilities

The ability to use tools is a core characteristic of the agentic pattern, as it enables models to handle more complex queries and generate higher-quality responses.

A Large Language Model (LLM) alone can typically only perform one action (e.g., generate text or images). Tools enable an agent to perceive the environment (**read-only actions**) and act upon it (**write actions**).

The **tool inventory** is the set of tools an agent has access to, and this inventory determines what an agent is capable of doing.

### A. Categories of Tools

Depending on the agent's environment, tools generally fall into three categories:

1. **Knowledge Augmentation (Context Construction):** Tools that retrieve data to help the agent respond with higher quality or more relevant information.
    
    - **Examples:** text retriever, image retriever, SQL executor/retriever, internal tools (people search, inventory API, Slack retrieval), email readers.
    - **Web Browsing:** Considered one of the most anticipated capabilities. It prevents models from growing stale and helps reduce hallucinations by providing up-to-date information (e.g., weather, news, flight status). Web browsing is often used as an umbrella term for all tools accessing the internet.
2. **Capability Extension:** Tools designed to address inherent limitations in AI models, such as poor mathematical accuracy.
    
    - **Examples:** calculator, calendar, timezone converter, unit converter (e.g., converting lbs to kg), and translator.
    - **Code Interpreters:** More complex and powerful tools. Instead of training the model in a specific skill (like arithmetic), a code interpreter allows the agent to execute a piece of code, return results, or analyze failures. They are often used for data analysts and research assistants.
3. **Tools Enabling Agent Action (Write Actions):** Tools that allow the agent to perform data writes, modify settings, or delete data.
    
    - **Examples:** A SQL executor can perform `read` (data retrieval) actions but also `write` (data update) actions or `delete` actions.
    - **Workflow Automation:** Write actions enable complex automation, such as researching potential customers, sending emails, extracting orders, or updating databases with new orders.
    - **Security Concerns:** Because agents can potentially execute impactful tasks like initiating bank transfers or deleting production data, proper security measures are crucial.

### B. Function Calling / Tool Invocation

Many model providers implement tool usage by integrating **function calling**.

**The Tool Invocation Process:**

1. **Create a tool inventory:** All tools the model might need must be declared, including the execution entry point, function name, parameters, and documentation.
2. **Specify tool usage:** The agent specifies how tools should be used per query (`required`, `none`, or `auto`).

When given a query, the agent should automatically determine which tool to use and the parameters required. Users should inspect the parameter values used for each function call to ensure they are correct.

## IV. Planning

**Planning** is central to a foundation model agent, as it is the component responsible for solving a task defined by a goal and constraints.

### A. The Planning Challenge

For complex tasks, planning is necessary to create a **roadmap outlining the steps needed to accomplish the task**. Effective planning requires the model to understand the task, consider various options, and choose the most promising one.

Planning is a **search problem** at its core, requiring the agent to search among different paths to the goal.

### B. Planning vs. Execution

The planning process can be executed in two ways:

1. **Coupled Planning and Execution:** The agent plans and executes step by step (e.g., using a chain-of-thought prompt). This may fail if a step doesn't accomplish the goal, resulting in wasted time and API calls.
2. **Decoupled Planning and Execution:** The agent first generates a complete plan, which is then validated before execution. This ensures only valid plans are executed and is often performed in a multi-agent system.

A decoupled system may involve three components for planning and execution:

- One component to **generate** plans.
- One component to **validate** plans (an evaluator).
- One component to **execute** plans.

### C. Foundation Models as Planners

LLMs are often categorized as **poor planners** because they may lack the fundamental ability to plan, search, and perform **backtracking**.

- Since autoregressive models typically only generate forward actions, backtracking (revising a previous step that led to a dead end) is difficult.
- LLMs must be given the necessary toolings, the potential outcome of each action, and state tracking to be effective planners.

**Foundation Model (FM) vs. Reinforcement Learning (RL) Planners:**

|Planner Type|Method|Characteristics|
|:--|:--|:--|
|**RL Planners**|Trained via an RL algorithm|Requires significant time and resources for training|
|**FM Planners**|Uses prompt engineering|Can be prompted or finetuned; requires less time and resources|
|**Similarity**|Both seek to maximize cumulative reward in a dynamic environment.|

### D. Planning Granularity and Control Flow

**Planning Granularity** refers to the level of detail in a plan, which can range from a 1-year plan to a week-to-week plan. There is a planning/execution trade-off:

- **Detailed Plans:** Harder to generate but easier to execute.
- **High-level Plans:** Easier to generate but harder to execute.

The order in which actions are executed is known as **control flow**. While the sequential form is the simplest, complex plans can involve other types of control flows:

|Control Flow Type|Description|Example (from source)|
|:--|:--|:--|
|**Sequential**|Task B executes only after Task A is completed.|Task A: Translate query into SQL query; Task B: Execute SQL query.|
|**Parallel**|Tasks A and B execute at the same time.|Task A: Find best-selling products; Task B/C/etc.: Retrieve price for each product. **Parallel execution can significantly reduce latency**.|
|**If statement**|Execution is conditional on the output of the previous step.|Task A: Analyze earnings report; Task B: Buy shares (if positive); Task C: Sell shares (if negative).|
|**For loop**|Repeat Task A until a specific condition is met.|Keep generating random numbers until a prime number is reached.|

## V. Reflection and Error Correction

Reflection is critical for ensuring plans are constantly evaluated and adjusted to maximize success.

Reflection is typically performed in multiple stages during a task:

- After receiving a user query (to evaluate feasibility).
- After initial plan generation (to ensure the plan makes sense).
- After each execution step (to evaluate progress).
- After the whole plan is executed (to determine if the task is accomplished).

### A. The ReAct Framework

Reflection and error correction are two different mechanisms that help uncover and correct errors.

The **ReAct** (Reasoning + Action) framework interweaves reasoning and action. In ReAct, the agent is prompted to:

1. Explain its thinking (planning/Reasoning).
2. Take actions (Act).
3. Analyze observations (reflection).

### B. Reflection Agents

Reflection can be implemented with a separate component, such as a specialized scorer, or using the same agent via self-critique prompts.

In the approach by Shinn et al. (2023), the framework separates reflection into two modules: an **evaluator** that determines what went wrong, and a **self-reflection module** that analyzes these errors. This framework proposes a new **trajectory** (plan) at each step after evaluation and self-reflection.

## VI. Agent Failure Modes and Evaluation

To evaluate an agent, one must identify the failure modes and measure their frequency. Agents exhibit unique failure types related to planning, tool execution, and efficiency.

### A. Planning Failures

The most common failure mode in planning is **tool use failure**. Errors include:

1. **Invalid tool:** The agent generates a plan using a tool that is not present in its tool inventory (e.g., trying to use `bing_search` when it is not available).
2. **Valid tool, invalid parameters:** The agent calls a tool with the wrong number of parameters (e.g., calling a function that requires two parameters with only one).
3. **Valid tool, incorrect parameter values:** The agent calls the correct tool with the correct structure, but the parameter value is wrong (e.g., using `lbs=120` when it should be `lbs=40`).
4. **Goal failure:** The plan fails to achieve the goal or violates initial constraints (e.g., a planned trip overshoots the budget).
5. **Errors due to reflection:** Poor planning reflection can cause the agent to incorrectly assume a task is finished.

### B. Tool and Efficiency Failures

- **Tool Failures:** Occur when the correct tool is used, but the tool output is wrong (e.g., an image captioner returns a wrong description, or an SQL query generator returns a wrong SQL query). Tool failures are tool-dependent and should be tested independently.
- **Compound Mistakes:** Since agents often perform multi-step tasks, overall accuracy degrades quickly. For example, a model with 95% accuracy per step drops to 60% accuracy over 10 steps.
- **Efficiency Metrics:** Used to evaluate an agent's performance relative to a baseline (e.g., a human operator). Metrics include:
    - The number of steps needed to complete a task.
    - The cost associated with completing a task.
    - The time/resource consumption of the actions.

## VII. Memory

**Memory** refers to the mechanisms that allow a model to retain and utilize information. It is essential for knowledge augmentation (RAG) and multi-step applications. An agentic system's memory is used to store context, instructions, examples, plans, tool outputs, and reflections.

AI models typically have three primary memory mechanisms:

|Mechanism|Description|Use Case|
|:--|:--|:--|
|**Internal Knowledge**|Knowledge retained from the model's training data. It does not change unless the model itself is updated.|Accessing knowledge that all queries rely on.|
|**Short-term memory (Context)**|The model's context window. Stores previous messages in a conversation and is critical for the _current_ task. Capacity is limited and this memory typically fades across tasks.|Immediate context relevant to the ongoing conversation.|
|**Long-term memory (External Data)**|External data sources accessed via retrieval, such as RAG systems. This knowledge persists across tasks and can be updated or deleted.|Retrieving information essential for all tasks (e.g., training/finetuning data).|

### A. Memory System Functions and Management

A memory system for AI models has two key functions:

1. **Memory management:** Managing what information should be stored in the short-term and long-term memory.
2. **Memory retrieval:** Retrieving information relevant to the task from long-term memory.

**Overflow Management:** Long-term memory is used to store the overflow from short-term memory. If the model's short-term context limit is reached (e.g., 70% of the context limit is reserved), the overflow is moved to long-term memory.

**Data Integrity:** Storing structured data (like an Excel sheet) in the memory system's context, where it is often treated as unstructured text, can compromise its structural integrity.

### B. Maintaining Consistency and Reducing Redundancy

- **Consistency:** Memory allows an AI model to reference its previous answers to ensure future responses are consistent.
- **Redundancy Reduction:** FIFO (First In, First Out) is the simplest strategy for memory management, where the oldest messages are moved first to the external storage.
- More sophisticated strategies for removing redundancy involve using a summary of the conversation or using a reflection approach. Reflection can be used to determine if new information should be merged with existing memory, replace outdated information, or contradict existing information.