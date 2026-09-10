The problem is not with prompt engineering. It’s a real and useful skill to have. The problem is when prompt engineering is the only thing people know

This chapter covers both how to write effective prompts and how to defend your applications against prompt attacks.

A prompt generally consists of one or more of the following parts: 
- Task description 
What you want the model to do, including the role you want the model to play and the output format. 

- Example(s) of how to do this task 
For example, if you want the model to detect toxicity in text, you might provide a few examples of what toxicity and non-toxicity look like. 

- The task 
The concrete task you want the model to do, such as the question to answer or the book to summarize

Today, in-context learning is taken for granted. A foundation model learns from a massive amount of data and should be able to do a lot of things.

System Prompt and User Prompt
You can think of the system prompt as the task description and the user prompt as the task.

System prompt: 
You’re an experienced real estate agent. Your job is to read each disclosure carefully, fairly assess the condition of the property based on this disclosure, and help your buyer understand the risks and opportunities of each property. For each question, answer succinctly and professionally. 

User prompt: 
	Context: [disclosure.pdf] 
	Question: Summarize the noise complaints, if any, about this property. 
	
Answer:

---
Context Length and Context Efficiency 
How much information can be included in a prompt depends on the model’s context length limit.

Research has shown that a model is much better at understanding instructions given at the beginning and the end of a prompt than in the middle

Ask the model to adopt a persona A persona can help the model to understand the perspective it’s supposed to use to generate responses.

Explain, without ambiguity, what you want the model to do

Write Clear and Explicit Instructions

Specify the output format If you want the model to be concise, tell it so. Long outputs are not only costly (model APIs charge per token) but they also increase latency. 

Provide Sufficient Context 
Just as reference texts can help students do better on an exam, sufficient context can help models perform better. If you want the model to answer questions about a paper, including that paper in the context will likely improve the model’s responses

Break Complex Tasks into Simpler Subtasks

If used correctly, prompt engineering tools can greatly improve your system’s performance. However, it’s important to be aware of how they work under the hood to avoid unnecessary costs and headaches

Defensive Prompt Engineering
- Prompt extraction
Extracting the application’s prompt, including the system prompt, either to replicate or exploit the application

- Jailbreaking and prompt injection
Getting the model to do bad things

- Information Extraction
Getting the model to reveal its training data or information used in its context

Reverse prompt engineering is the process of deducing the system prompt used for a certain application.

Reverse prompt engineering is typically done by analyzing the application outputs or by tricking the model into repeating its entire prompt, which includes the system prompt.