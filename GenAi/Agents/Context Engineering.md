## What is Context Engineering?

Context engineering is the process of designing, testing, and iterating on the contextual information provided to AI agents to shape their behavior and improve task performance. Unlike simple prompt engineering for single LLM calls, context engineering for agents involves (but not limited to):

- **System prompts** that define agent behavior and capabilities
- **Task constraints** that guide decision-making
- **Tool descriptions** that clarify when and how to use available functions/tools
- **Memory management** for tracking state across multiple steps
- **Error handling** patterns for robust execution

## Building a Deep Research Agent: A Case Study

Let's explore context engineering principles through an example: a minimal deep research agent that performs web searches and generates reports.

![Agent Workflow](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsimple-dr-agent.46d70e98.png&w=3840&q=75)

### The Context Engineering Challenge

When building the first version of this agent system, the initial implementation revealed several behavioral issues that required careful context engineering:

#### Issue 1: Incomplete Task Execution

**Problem**: When running the agentic workflow, the orchestrator agent often creates three search tasks but only executes searches for two of them, skipping the third task without explicit justification.

**Root Cause**: The agent's system prompt lacked explicit constraints about task completion requirements. The agent made assumptions about which searches were necessary, leading to inconsistent behavior.

**Solution**: Two approaches are possible:
1. **Flexible Approach** (current): Allow the agent to decide which searches are necessary, but require explicit reasoning for skipped tasks
2. **Strict Approach**: Add explicit constraints requiring search execution for all planned tasks

Example system prompt enhancement:

```
You are a deep research agent responsible for executing comprehensive research tasks.TASK EXECUTION RULES:- For each search task you create, you MUST either:  1. Execute a web search and document findings, OR  2. Explicitly state why the search is unnecessary and mark it as completed with justification- Do NOT skip tasks silently or make assumptions about task redundancy- If you determine tasks overlap, consolidate them BEFORE execution- Update task status in the spreadsheet after each action
```

#### Issue 2: Lack of Debugging Visibility

**Problem**: Without proper logging and state tracking, it was difficult to understand why the agent made certain decisions.

**Solution**: For this example, it helps to implement a task management system using a spreadsheet or text file (for simplicity) with the following fields:

- Task ID
- Search query
- Status (todo, in_progress, completed)
- Results summary
- Timestamp

This visibility enables:

- Real-time debugging of agent decisions
- Understanding of task execution flow
- Identification of behavioral patterns
- Data for iterative improvements

### Context Engineering Best Practices
Based on this case study, here are key principles for effective context engineering:

#### 1. Eliminate Prompt Ambiguity

**Bad Example:**

```
Perform research on the given topic.
```

**Good Example:**

```
Perform research on the given topic by:1. Breaking down the query into 3-5 specific search subtasks2. Executing a web search for EACH subtask using the search_tool3. Documenting findings for each search in the task tracker4. Synthesizing all findings into a comprehensive report
```

#### 2. Make Expectations Explicit
Don't assume the agent knows what you want. Be explicit about:

- Required vs. optional actions
- Quality standards
- Output formats
- Decision-making criteria

#### 3. Implement Observability
Build debugging mechanisms into your agentic system:

- Log all agent decisions and reasoning
- Track state changes in external storage
- Record tool calls and their outcomes
- Capture errors and edge cases

Pay close attention to every run of your agentic system. Strange behaviors and edge cases are opportunities to improve your context engineering efforts.

#### 4. Iterate Based on Behavior
Context engineering is an iterative process:

1. **Deploy** the agent with initial context
2. **Observe** actual behavior in production
3. **Identify** deviations from expected behavior
4. **Refine** system prompts and constraints
5. **Test** and validate improvements
6. **Repeat**

#### 5. Balance Flexibility and Constraints

Consider the tradeoff between:

- **Strict constraints**: More predictable but less adaptable
- **Flexible guidelines**: More adaptable but potentially inconsistent

Choose based on your use case requirements.

## Advanced Context Engineering Techniques

### Layered Context Architecture

Context engineering applies to all stages of the AI agent build process. Depending on the AI Agent, it's sometimes helpful to think of context as a hierarchical structure. For our basic agentic system, we can organize context into hierarchical layers:

1. **System Layer**: Core agent identity and capabilities
2. **Task Layer**: Specific instructions for the current task
3. **Tool Layer**: Descriptions and usage guidelines for each tool
4. **Memory Layer**: Relevant historical context and learnings

### Dynamic Context Adjustment[](https://www.promptingguide.ai/agents/context-engineering#dynamic-context-adjustment)

Another approach is to dynamically adjust context based on the task complexity, available resources, previous execution history, and error patterns. Based on our example, we can adjust context based on:

- Task complexity
- Available resources
- Previous execution history
- Error patterns

### Context Validation
Evaluation is key to ensuring context engineering techniques are working as they should for your AI agents. Before deployment, validate your context design:

- **Completeness**: Does it cover all important scenarios?
- **Clarity**: Is it unambiguous?
- **Consistency**: Do different parts align?
- **Testability**: Can you verify the behavior?

## Common Context Engineering Pitfalls
Below are a few common context engineering pitfalls to avoid when building AI agents:

### 1. Over-Constraint

**Problem**: Too many rules make the agent inflexible and unable to handle edge cases.

**Example**:

```
NEVER skip a search task.ALWAYS perform exactly 3 searches.NEVER combine similar queries.
```

**Better Approach**:

```
Aim to perform searches for all planned tasks. If you determine that tasks are redundant, consolidate them before execution and document your reasoning.
```

### 2. Under-Specification

**Problem**: Vague instructions lead to unpredictable behavior.

**Example**:

```
Do some research and create a report.
```

**Better Approach**:

```
Execute research by:1. Analyzing the user query to identify key information needs2. Creating 3-5 specific search tasks covering different aspects3. Executing searches using the search_tool for each task4. Synthesizing findings into a structured report with sections for:   - Executive summary   - Key findings per search task   - Conclusions and insights
```

### 3. Ignoring Error Cases

**Problem**: Context doesn't specify behavior when things go wrong.

**Solution**: In some cases, it helps to add error handling instructions to your AI Agents:

```
ERROR HANDLING:- If a search fails, retry once with a rephrased query- If retry fails, document the failure and continue with remaining tasks- If more than 50% of searches fail, alert the user and request guidance- Never stop execution completely without user notification
```

## Measuring Context Engineering Success
Track these metrics to evaluate context engineering effectiveness:

1. **Task Completion Rate**: Percentage of tasks completed successfully
2. **Behavioral Consistency**: Similarity of agent behavior across similar inputs
3. **Error Rate**: Frequency of failures and unexpected behaviors
4. **User Satisfaction**: Quality and usefulness of outputs
5. **Debugging Time**: Time required to identify and fix issues

It's important to not treat context engineering as a one-time activity but an ongoing practice that requires:

- **Systematic observation** of agent behavior
- **Careful analysis** of failures and edge cases
- **Iterative refinement** of instructions and constraints
- **Rigorous testing** of changes
---
Spend hours of iterating on:
- System prompt design and refinement
- Tool definitions and usage instructions
- Agent architecture and communication patterns
- Input/output specifications between agents

## The Reality of Context Engineering

Building effective AI agents requires substantial tuning of system prompts and tool definitions. The process involves spending hours iterating on:

- System prompt design and refinement
- Tool definitions and usage instructions
- Agent architecture and communication patterns
- Input/output specifications between agents

Don't underestimate the effort required for context engineering. It's not a one-time task but an iterative process that significantly impacts agent reliability and performance.

## Agent Architecture Design

### The Original Design Problem

![deep-research-agent](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsimple-dr-agent.46d70e98.png&w=3840&q=75)

Let's look at a basic deep research agent architecture. The initial architecture connects the web search tool directly to the deep research agent. This design places too much burden on a single agent responsible for:

- Managing tasks (creating, updating, deleting)
- Saving information to memory
- Executing web searches
- Generating final reports

**Consequences of this design:**

- Context grew too long
- Agent forgot to execute web searches
- Task completion updates were missed
- Unreliable behavior across different queries

### The Improved Multi-Agent Architecture

The solution involved separating concerns by introducing a dedicated search worker agent:

**Benefits of the multi-agent design:**

1. **Separation of Concerns**: The parent agent (Deep Research Agent) handles planning and orchestration, while the search worker agent focuses exclusively on executing web searches
2. **Improved Reliability**: Each agent has a clear, focused responsibility, reducing the likelihood of missed tasks or forgotten operations
3. **Model Selection Flexibility**: Different agents can use different language models optimized for their specific tasks
    - Deep Research Agent: Uses Gemini 2.5 Pro for complex planning and reasoning
    - Search Worker Agent: Uses Gemini 2.5 Flash for faster, more cost-effective search execution

If you are using models from other providers like OpenAI, you can leverage GPT-5 (for planning and reasoning) and GPT-5-mini (for search execution) for similar performance.

**Design Principle**: Separating agent responsibilities improves reliability and enables cost-effective model selection for different subtasks.

## System Prompt Engineering

Here is the full system prompt for the deep research agent we built in n8n:

```
You are a deep research agent who will help with planning and executing search tasks to generate a deep research report. ## GENERAL INSTRUCTIONS The user will provide a query, and you will convert that query into a search plan with multiple search tasks (3 web searches). You will execute each search task and maintain the status of those searches in a spreadsheet. You will then generate a final deep research report for the user. For context, today's date is: {{ $now.format('yyyy-MM-dd') }} ## TOOL DESCRIPTIONS Below are some useful instructions for how to use the available tools.  Deleting tasks: Use the delete_task tool to clear up all the tasks before starting the search plan.  Planning tasks: You will create a plan with the search tasks (3 web searches) and add them to the Google Sheet using the append_update_task tool. Make sure to keep the status of each task updated after completing each search. Each task begins with a todo status and will be updated to a "done" status once the search worker returns information regarding the search task. Executing tasks: Use the Search Worker Agent tool to execute the search plan. The input to the agent are the actual search queries, word for word.  Use the tools in the order that makes the most sense to you but be efficient. 
```

Let's break it down into parts and discuss why each section is important:

### High-Level Agent Definition

The system prompt begins with a clear definition of the agent's role:

```
You are a deep research agent who will help with planning and executing search tasks to generate a deep research report.
```

### General Instructions

Provide explicit instructions about the agent's workflow:

```
## GENERAL INSTRUCTIONS The user will provide a query, and you will convert that query into a search plan with multiple search tasks (3 web searches). You will execute each search task and maintain the status of those searches in a spreadsheet. You will then generate a final deep research report for the user.
```

### Providing Essential Context

**Current Date Information:**

Including the current date is crucial for research agents to get up-to-date information:

```
For context, today's date is: {{ $now.format('yyyy-MM-dd') }}
```

**Why this matters:**

- LLMs typically have knowledge cutoffs months or years behind the current date
- Without current date context, agents often search for outdated information
- This ensures agents understand temporal context for queries like "latest news" or "recent developments"

In n8n, you can dynamically inject the current date using built-in functions with customizable formats (date only, date with time, specific timezones, etc.).

## Tool Definitions and Usage Instructions

### The Importance of Detailed Tool Descriptions

Tool definitions typically appear in two places:

1. **In the system prompt**: Detailed explanations of what tools do and when to use them
2. **In the actual tool implementation**: Technical specifications and parameters

**Key Insight**: The biggest performance improvements often come from clearly explaining tool usage in the system prompt, not just defining tool parameters.

### Example Tool Instructions

The system prompt also includes detailed instructions for using the available tools:

```
## TOOL DESCRIPTIONS Below are some useful instructions for how to use the available tools.  Deleting tasks: Use the delete_task tool to clear up all the tasks before starting the search plan.  Planning tasks: You will create a plan with the search tasks (3 web searches) and add them to the Google Sheet using the append_update_task tool. Make sure to keep the status of each task updated after completing each search. Each task begins with a todo status and will be updated to a "done" status once the search worker returns information regarding the search task. Executing tasks: Use the Search Worker Agent tool to execute the search plan. The input to the agent are the actual search queries, word for word.  Use the tools in the order that makes the most sense to you but be efficient. 
```

Initially, without explicit status definitions, the agent would use different status values across runs:

- Sometimes "pending", sometimes "to-do"
- Sometimes "completed", sometimes "done", sometimes "finished"

Be explicit about allowed values. This eliminates ambiguity and ensures consistent behavior.

Note that the system prompt also includes this instruction:

```
Use the tools in the order that makes most sense to you, but be efficient.
```

What's the reasoning behind this decision?

This provides flexibility for the agent to optimize its execution strategy. During testing, the agent might:

- Execute only 2 searches instead of 3 if it determines that's sufficient
- Combine redundant search queries
- Skip searches that overlap significantly

Here is a specific instruction you can use, if you require all search tasks to be executed:

```
You MUST execute a web search for each and every search task you create.Do NOT skip any tasks, even if they seem redundant.
```

**When to use flexible vs. rigid approaches:**

- **Flexible**: During development and testing to observe agent decision-making patterns
- **Rigid**: In production when consistency and completeness are critical

## Context Engineering Iteration Process

### The Iterative Nature of Improving Context

Context engineering is not a one-time effort. The development process involves:

1. **Initial implementation** with basic system prompts
2. **Testing** with diverse queries
3. **Identifying issues** (missed tasks, wrong status values, incomplete searches)
4. **Adding specific instructions** to address each issue
5. **Re-testing** to validate improvements
6. **Repeating** the cycle

### What's Still Missing

Even after multiple iterations, there are opportunities for further improvement:

**Search Task Metadata:**

- Augmenting search queries
- Search type (web search, news search, academic search, PDF search)
- Time period filters (today, last week, past month, past year, all time)
- Domain focus (technology, science, health, etc.)
- Priority levels for task execution order

**Enhanced Search Planning:**

- More detailed instructions on how to generate search tasks
- Preferred formats for search queries
- Guidelines for breaking down complex queries
- Examples of good vs. bad search task decomposition

**Date Range Specification:**

- Start date and end date for time-bounded searches
- Format specifications for date parameters
- Logic for inferring date ranges from time period keywords

Based on the recommended improvements, it's easy to appreciate that web search for AI agents is a challenging effort that requires a lot of context engineering.

## Advanced Considerations

### Sub-Agent Communication

When designing multi-agent systems, carefully consider:

**What information does the sub-agent need?**

- For the search worker: Just the search query text
- Not the full context or task metadata
- Keep sub-agent inputs minimal and focused

**What information should the sub-agent return?**

- Search results and relevant findings
- Error states or failure conditions
- Metadata about the search execution

### Context Length Management

As agents execute multiple tasks, context grows:

- Task history accumulates
- Search results add tokens
- Conversation history expands

**Strategies to manage context length:**

- Use separate agents to isolate context
- Implement memory management tools
- Summarize long outputs before adding to context
- Clear task lists between research queries

### Error Handling in System Prompts

Include instructions for failure scenarios:

```
ERROR HANDLING:- If search_worker fails, retry once with rephrased query- If task cannot be completed, mark status as "failed" with reason- If critical errors occur, notify user and request guidance- Never proceed silently when operations fail
```

## Conclusion

Context engineering is a critical practice for building reliable AI agents that requires:

- **Significant iteration time** spent tuning prompts and tool definitions
- **Careful architectural decisions** about agent separation and communication
- **Explicit instructions** that eliminate assumptions
- **Continuous refinement** based on observed behavior
- **Balance between flexibility and control**