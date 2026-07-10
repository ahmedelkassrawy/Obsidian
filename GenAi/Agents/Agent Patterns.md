## . Reactive Agents
**Concept:** These agents follow a direct mapping from states to actions. They do not maintain an internal "memory" or "world model"; they simply respond to the current input or environment immediately.

- **Example:** A simple thermostat. If temperature $< 20°C$, then turn on heater.
    
- **When to use:** Use for low-latency tasks where the environment is predictable and historical context doesn't change the immediate decision.
## 2. Deliberative Agents
**Concept:** These agents possess an internal model of the world and use **planning** to achieve goals. They think through the consequences of their actions before taking them.

- **Example:** A chess AI. It doesn't just react to your move; it simulates thousands of potential future board states to find the one that leads to a win.
    
- **When to use:** Use for complex, goal-oriented tasks where multiple steps are required and the "best" move isn't immediately obvious from the current state.
## 3. Hybrid Agents
**Concept:** These combine the speed of reactive agents with the foresight of deliberative agents. They usually have a "layered" architecture: a fast layer for emergencies and a slow layer for long-term planning.
- **Example:** A self-driving car. It has a **reactive** layer to slam the brakes if a pedestrian jumps out, and a **deliberative** layer to plan the route from New York to DC.
    
- **When to use:** Use for real-world robotics or autonomous systems that must balance safety (immediate) with efficiency (planned).
---
## 4. ReAct (Reason + Act)

**Concept:** ReAct combines **Chain-of-Thought reasoning** with **Action execution**. The agent writes down its "Thought," decides on an "Action" (like a Google search), observes the "Result," and repeats until the task is done.
- **RAG (ReAct Based):** The agent doesn't just guess; it "thinks" it needs more info, "acts" by querying a database, and then uses that data to answer.
    
- **Example:** "I need to find the current price of Apple stock. _Action: Search Finance API._ _Observation: $180._ _Thought: Now I can calculate the total value..._"
    
- **When to use:** Use for LLM-based assistants that need to interact with external tools (APIs, Browsers, Databases) to reduce hallucinations.
## 5. Plan-and-Execute
**Concept:** This pattern separates the "Brain" from the "Hands." One agent creates a comprehensive multi-step plan, and a second agent (or loop) executes each step sequentially without re-planning every time.
- **Example:** A "Research Agent." Step 1: Find 5 papers. Step 2: Summarize each. Step 3: Write a synthesis.
    
- **When to use:** Use for long-running tasks where the steps are relatively stable, saving "tokens" and time by not re-reasoning at every single sub-action.
## 6. Tree/Graph of Thoughts (ToT / GoT)
**Concept:** Traditional LLMs think linearly. ToT allows the agent to branch out into multiple potential solutions (the Tree), evaluate which one looks promising, and even backtrack if a "branch" hits a dead end. **Graph of Thoughts** takes this further by allowing ideas to merge or loop.

- **Example:** Solving a complex math problem or a crossword puzzle where an early mistake ruins the whole result. The agent tries three different formulas, realizes two fail, and returns to the successful one.
    
- **When to use:** Use for high-stakes reasoning, creative writing, or complex coding where the first "thought" might be wrong and self-correction is vital.
---
### Comparison Summary

|**Pattern**|**Primary Strength**|**Weakness**|
|---|---|---|
|**Reactive**|Speed / Simplicity|No long-term memory|
|**Deliberative**|Goal-oriented|High compute / Slow|
|**ReAct**|Tool use / Fact-checking|Can get stuck in infinite loops|
|**Plan-Execute**|Efficiency in long tasks|Brittle if the plan fails midway|
|**Tree of Thoughts**|Deep problem solving|Very high token cost|