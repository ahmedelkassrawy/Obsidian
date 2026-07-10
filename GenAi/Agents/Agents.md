| Agency Level | Description                                              | What that’s called | Example pattern                                    |
| ------------ | -------------------------------------------------------- | ------------------ | -------------------------------------------------- |
| ☆☆☆          | Agent output has no impact on program flow               | Simple processor   | `process_llm_output(llm_response)`                 |
| ★☆☆          | Agent output determines basic control flow               | Router             | `if llm_decision(): path_a() else: path_b()`       |
| ★★☆          | Agent output determines function execution               | Tool caller        | `run_function(llm_chosen_tool, llm_chosen_args)`   |
| ★★★          | Agent output controls iteration and program continuation | Multi-step Agent   | `while llm_should_continue(): execute_next_step()` |
| ★★★          | One agentic workflow can start another agentic workflow  | Multi-Agent        | `if llm_trigger(): execute_agent()`                |
Agents work in a continuous cycle of: **thinking (Thought) → acting (Act) and observing (Observe)**.

Let’s break down these actions together:
1. **Thought**: The LLM part of the Agent decides what the next step should be.
2. **Action:** The agent takes an action, by calling the tools with the associated arguments.
3. **Observation:** The model reflects on the response from the tool.

**ReAct approach**, which is the concatenation of “Reasoning” (Think) with “Acting” (Act).
Simple prompting technique that appends “Let’s think step by step” before letting the LLM decode the next tokens.

## Types of Agent Actions

There are multiple types of Agents that take actions differently:

|Type of Agent|Description|
|---|---|
|JSON Agent|The Action to take is specified in JSON format.|
|Code Agent|The Agent writes a code block that is interpreted externally.|
|Function-calling Agent|It is a subcategory of the JSON Agent which has been fine-tuned to generate a new message for each action.|

## Agentic Patterns
### 1.Reflection Pattern
The **Reflection Pattern** in agentic AI is a design approach where an AI system iteratively improves its output by generating content, critiquing it, and refining it based on the critique. The process involves three key steps: (1) **Generation**, where the AI produces an initial output (e.g., code, text); (2) **Reflection**, where the AI evaluates the output for errors, inefficiencies, or improvements; and (3) **Refinement**, where the AI revises the output based on the critique. This cycle repeats for a fixed number of iterations or until a stopping condition (e.g., "no further improvements") is met. The pattern enhances output quality by mimicking human-like self-assessment and iterative problem-solving, making it ideal for tasks like code generation, writing, or complex reasoning.