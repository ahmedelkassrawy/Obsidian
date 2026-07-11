# 📚 AI Prompt Engineering Study Guide

> **Tags**: #AI #PromptEngineering #LLM #LangChain #APICalls  

---

## 🧠 Key Parameters for LLMs

> [!info] Overview
> Parameters control LLM output behavior, balancing creativity, determinism, and length.

| Parameter | Description | Range | Effect |
|-----------|-------------|-------|--------|
| **Temperature** | Controls randomness | 0 to 2 | - **Low (0–0.3)**: Focused, deterministic<br>- **Medium (0.4–0.7)**: Balances creativity<br>- **High (0.8–2)**: More creative outputs |
| **Top_p** | Considers only top p probability tokens | 0 to 1 | Lower values restrict to more probable tokens |
| **Max Tokens** | Max number of tokens in generated output | Default: 4096 | Limits response length |

> [!example] API Call Example
> ```python:disable-run
> response = openai.ChatCompletion.create(
>     model="gpt-3.5-turbo",
>     messages=[{"role": "user", "content": "Tell me a story."}],
>     max_tokens=150,
>     top_p=0.9,
>     temp=1.2
> )
> ```

> [!tip] Study Tip
> Experiment with these in [[LLM_Parameters]]. Link results back here!

---

## 🤖 Roles in API Calls

> [!info] Overview
> Roles define context in API conversations.

| Role | Description |
|------|-------------|
| **System** | Provides high-level instructions to guide the model |
| **User** | Represents human input |
| **Assistant** | Model's response based on user input and system instructions |

> [!example] Messages Example
> ```python
> messages = [
>     {"role": "system", 
>         "content": "You are a helpful assistant."},
>     {"role": "user", 
>         "content": "What can you do?"}
> ]
> ```

> [!tip] Study Tip
> Test role variations in [[Code_Examples]] to see how they shape responses.

---

## 🚀 Basic Prompt Engineering Techniques

> [!info] Overview
> Techniques for crafting effective prompts, from simple to structured.

### 1. Zero-Shot Prompting
> Simplest form: Ask directly without examples.

> [!example]
> ```
> ❌ Complex: Please tell me, if you would be so kind, what the capital of France might be?
> ✅ Simple: What is the capital of France?
> ```

### 2. One-Shot Prompting
> Provide one example + new request for format/style guidance.

> [!example]
> ```
> Product Description Example:
> "The Classic White Mug - A timeless 12oz ceramic mug perfect for your morning coffee. Microwave-safe and dishwasher-friendly."
> 
> Please write a similar description for: Gaming Mechanical Keyboard
> ```

### 3. Few-Shot Prompting
> Multiple examples for patterns in complex tasks.

> [!example]
> ```
> Convert these sentences to past tense:
> Input: "I eat an apple"
> Output: "I ate an apple"
> 
> Input: "She runs fast"
> Output: "She ran fast"
> 
> Now convert: "They sing well"
> ```

### 4. Role-Based Prompting
> Assign roles to shape perspective, tone, and expertise.

> [!example]
> ```
> Act as a cybersecurity expert and explain how password hashing works to a beginner.
> ```

> [!tip] Study Tip
> Practice these in [[Prompt_Techniques]]. Use #ZeroShot, #FewShot tags.

---

## 🧩 Advanced Prompt Engineering Techniques

### Chain of Thought (CoT)
> Breaks down complex problems into steps for better reasoning.

> [!example]
> ```
> Problem: A store has a 30% discount on all items. If Sarah buys a shirt
> originally priced at $40 and pants originally priced at $60, how much
> does she save in total?
> 
> Chain of Thought:
> 1. Calculate original total:
>    Shirt ($40) + Pants ($60) = $100
> 
> 2. Calculate discount percentage:
>    30% of $100 = $100 × 0.30 = $30
> 
> Therefore, Sarah saves $30 in total.
> ```

### ReAct
> Dynamic planning with Thought, Action, Observation for problem-solving.

> [!example]
> ```
> Task: Find out who directed the highest-grossing film of 2009
> 
> 1. Thought: I need to identify the highest-grossing film of 2009 first
> 2. Action: Search for "highest-grossing film 2009"
> 3. Observation: Avatar was the highest-grossing film of 2009
> 
> 4. Thought: Now I need to find out who directed Avatar
> 5. Action: Search for "Avatar 2009 director"
> 6. Observation: James Cameron directed Avatar
> 
> 7. Thought: I have all the necessary information
> 8. Answer: James Cameron directed Avatar, the highest-grossing film of 2009
> ```

> [!tip] Study Tip
> Apply CoT/ReAct to problems in [[ReAct_Examples]].

---

## 🛠️ LangChain Script Summary (`untitled145.py`)

> [!info] Overview
> Demonstrates prompt engineering types: Structured prompts, CoT, rule-based generation, safety filtering, A/B testing, multilingual tasks, input validation.

### 🧱 3. Structured Prompting with `PromptTemplate`

> [!example] Code
> ```python
> structured_prompt = PromptTemplate(
>     template="Provide a definition of {topic}, explain its importance and list three key benefits.",
>     input_variables=["topic"]
> )
> 
> chain = structured_prompt | llm
> result = chain.invoke({"topic": "prompt engineering"})
> print(result.content)
> ```

> [!note] Concept
> Reusable, parameterized prompts for automation.

### 🧮 4. Fact-Checking and Problem Solving

> [!example] Code
> ```python
> fact_check_prompt = PromptTemplate(
>     template="""Evaluate the following statement for factual accuracy:
>     Statement: {statement}
>     Evaluation:""",
>     input_variables=["statement"]
> )
> ```

> [!example] Use
> Input: “The capital of France is London.” → Output: “Incorrect. The capital of France is Paris.”

### 🗣️ 5. Conversational Memory

> [!example] Code
> ```python
> from langchain.chains import ConversationChain
> from langchain.memory import ConversationBufferMemory
> 
> conversation = ConversationChain(
>     llm=llm,
>     memory=ConversationBufferMemory(),
>     verbose=True
> )
> 
> conversation.predict(input="Hi, I'm learning about space.")
> conversation.predict(input="What's the largest planet?")
> ```

> [!note] Concept
> Maintains context with `ConversationBufferMemory`.

### 🧠 6. Chain-of-Thought (CoT) Reasoning

> [!example] Code
> ```python
> cot_prompt = PromptTemplate(
>     template="Answer the following question step by step: {question}",
>     input_variables=["question"]
> )
> 
> cot_chain = cot_prompt | llm
> result = cot_chain.invoke({"question": "If a train travels 120 km in 2 hours, what is its speed?"})
> print(result.content)
> ```

> [!note] Concept
> Step-by-step reasoning for accuracy.

### 🏗️ 7. Rule-Based Generation

> [!example] Code
> ```python
> job_posting_prompt = PromptTemplate(
>     input_variables=["job_title", "company", "location", "experience"],
>     template="""Create a job posting for a {job_title} position at {company} in {location}.
>     The candidate should have {experience} years of experience.
>     Follow these rules:
>     - Start with a brief company description
>     - List 5 key responsibilities
>     - List 5 qualifications
>     - End with an equal opportunity statement
>     """
> )
> ```

> [!note] Used For
> Structured documents like job listings.

### 🧩 8. Decomposition & Subtasks

> [!example] Code
> ```python
> decomposition_prompt = PromptTemplate(
>     template="Break down the following task into 3 subtasks:\nTask: {task}\nSubtasks:",
>     input_variables=["task"]
> )
> ```

> [!note] Idea
> Breaks tasks for agents/workflows.

### 📊 9. A/B Prompt Testing

> [!example] Code
> ```python
> prompt_a = PromptTemplate(template="Explain {topic} in simple terms.", input_variables=["topic"])
> prompt_b = PromptTemplate(template="Explain {topic} with an example.", input_variables=["topic"])
> ```

> [!note] Concept
> Compare prompts on metrics like clarity.

### 🌍 10. Multilingual Prompts & Translation

> [!example] Code
> ```python
> translation_prompt = PromptTemplate(
>     input_variables=["source_lang", "target_lang", "text"],
>     template="""Translate from {source_lang} to {target_lang}:
>     {text}"""
> )
> ```

> [!note] Concept
> Language adaptation.

### 🧰 11. Input Validation & Security

> [!example] Code
> ```python
> import re
> 
> def validate_and_sanitize_input(user_input: str) -> str:
>     allowed_pattern = r'^[a-zA-Z0-9\s.,!?()-]+$'
>     if not re.match(allowed_pattern, user_input):
>         raise ValueError("Disallowed characters")
>     if "ignore previous instructions" in user_input.lower():
>         raise ValueError("Prompt injection detected")
>     return user_input.strip()
> ```

> [!note] Purpose
> Prevents prompt injection.

### 🛡️ 12. Role-Based and Content Filtering

> [!example] Code
> ```python
> content_filter_prompt = PromptTemplate(
>     input_variables=["content"],
>     template="""Analyze the following for unsafe material:
>     Content: {content}
>     Respond with SAFE or UNSAFE."""
> )
> ```

> [!note] Concept
> Ethical safety filters.

### 🧑‍💻 13. Code Generation Example

> [!example] Code
> ```python
> code_gen_template = PromptTemplate(
>     input_variables=["language", "task"],
>     template="Generate {language} code for: {task}"
> )
> 
> generated_code = code_gen_template | llm
> ```

> [!note] Use
> Auto-generate functions.

### 🎨 14. Creative Writing & Story Generation

> [!example] Code
> ```python
> creative_writing_template = PromptTemplate(
>     input_variables=["genre", "setting", "theme"],
>     template="Write a {genre} story set in {setting} exploring {theme}."
> )
> ```

> [!note] Used For
> Fiction and content creation.

---

## 🧩 Key Concepts Recap

| Concept               | Description                        | LangChain Tool             |
| --------------------- | ---------------------------------- | -------------------------- |
| Prompt Template       | Structured prompt with variables   | `PromptTemplate`           |
| Chain                 | Sequential LLM + prompt connection | `                          |
| Memory                | Retains chat history               | `ConversationBufferMemory` |
| Chain-of-Thought      | Step-by-step reasoning             | Prompt pattern             |
| Rule-based generation | Formatted output                   | Templates with constraints |
| Input validation      | Security against injection         | Regex + logic              |
| A/B testing           | Comparing prompts                  | Manual/evaluation chain    |
| Translation           | Language conversion                | Parameterized prompt       |
| Content filter        | Safety system                      | Filtering prompt           |

----
### ELement of prompt
**Instruction** - a specific task or instruction you want the model to perform

**Context** - external information or additional context that can steer the model to better responses

**Input Data** - the input or question that we are interested to find a response for

**Output Indicator** - the type or format of the output.

### The Instruction

You can design effective prompts for various simple tasks by using commands to instruct the model what you want to achieve, such as "Write", "Classify", "Summarize", "Translate", "Order", etc.

Keep in mind that you also need to experiment a lot to see what works best. Try different instructions with different keywords, contexts, and data and see what works best for your particular use case and task. Usually, the more specific and relevant the context is to the task you are trying to perform, the better. We will touch on the importance of sampling and adding more context in the upcoming guides.

Others recommend that you place instructions at the beginning of the prompt. Another recommendation is to use some clear separator like "###" to separate the instruction and context.

### Specificity

Be very specific about the instruction and task you want the model to perform. The more descriptive and detailed the prompt is, the better the results. This is particularly important when you have a desired outcome or style of generation you are seeking. There aren't specific tokens or keywords that lead to better results. It's more important to have a good format and descriptive prompt. In fact, providing examples in the prompt is very effective to get desired output in specific formats.

When designing prompts, you should also keep in mind the length of the prompt as there are limitations regarding how long the prompt can be. Thinking about how specific and detailed you should be. Including too many unnecessary details is not necessarily a good approach. The details should be relevant and contribute to the task at hand. This is something you will need to experiment with a lot. We encourage a lot of experimentation and iteration to optimize prompts for your applications.

As an example, let's try a simple prompt to extract specific information from a piece of text.

_Prompt:_

```
Extract the name of places in the following text. Desired format:Place: <comma_separated_list_of_places>Input: "Although these developments are encouraging to researchers, much is still a mystery. “We often have a black box between the brain and the effect we see in the periphery,” says Henrique Veiga-Fernandes, a neuroimmunologist at the Champalimaud Centre for the Unknown in Lisbon. “If we want to use it in the therapeutic context, we actually need to understand the mechanism.“"
```

_Output:_

```
Place: Champalimaud Centre for the Unknown, Lisbon
```

### Avoid Impreciseness

Given the tips above about being detailed and improving format, it's easy to fall into the trap of wanting to be too clever about prompts and potentially creating imprecise descriptions. It's often better to be specific and direct. The analogy here is very similar to effective communication -- the more direct, the more effective the message gets across.

For example, you might be interested in learning the concept of prompt engineering. You might try something like:

```
Explain the concept prompt engineering. Keep the explanation short, only a few sentences, and don't be too descriptive.
```

It's not clear from the prompt above how many sentences to use and what style. You might still somewhat get good responses with the above prompts but the better prompt would be one that is very specific, concise, and to the point. Something like:

```
Use 2-3 sentences to explain the concept of prompt engineering to a high school student.
```

### To do or not to do?

Another common tip when designing prompts is to avoid saying what not to do but say what to do instead. This encourages more specificity and focuses on the details that lead to good responses from the model.

Here is an example of a movie recommendation chatbot failing at exactly what I don't want it to do because of how I wrote the instruction -- focusing on what not to do.

_Prompt:_

```
The following is an agent that recommends movies to a customer. DO NOT ASK FOR INTERESTS. DO NOT ASK FOR PERSONAL INFORMATION.Customer: Please recommend a movie based on my interests.Agent: 
```

_Output:_

```
Sure, I can recommend a movie based on your interests. What kind of movie would you like to watch? Do you prefer action, comedy, romance, or something else?
```

Here is a better prompt:

_Prompt:_

```
The following is an agent that recommends movies to a customer. The agent is responsible to recommend a movie from the top global trending movies. It should refrain from asking users for their preferences and avoid asking for personal information. If the agent doesn't have a movie to recommend, it should respond "Sorry, couldn't find a movie to recommend today.".Customer: Please recommend a movie based on my interests.Agent:
```

_Output:_

```
Sorry, I don't have any information about your interests. However, here's a list of the top global trending movies right now: [list of movies]. I hope you find something you like!
```