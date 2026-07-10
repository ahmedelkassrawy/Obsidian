Why multi-agent?
- **Context Management**: 
	- Provide specialized knowledge without overwhelming the model’s context window. 
	- If context were infinite and latency zero, you could dump all knowledge into a single prompt — but since it’s not, you need patterns to selectively surface relevant information.
- **Distributed development**: Allow different teams to develop and maintain capabilities independently, composing them into a larger system with clear boundaries.
-  **Parallelization**: Spawn specialized workers for subtasks and execute them concurrently for faster results.

>[!tip]
>At the center of multi-agent design is **[context engineering](https://docs.langchain.com/oss/python/langchain/context-engineering)**—deciding what information each agent sees. The quality of your system depends on ensuring each agent has access to the right data for its task.

#### Patterns
|Pattern|How it works|
|---|---|
|[**Subagents**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)|A main agent coordinates subagents as tools. All routing passes through the main agent, which decides when and how to invoke each subagent.|
|[**Handoffs**](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)|Behavior changes dynamically based on state. Tool calls update a state variable that triggers routing or configuration changes, switching agents or adjusting the current agent’s tools and prompt.|
|[**Skills**](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)|Specialized prompts and knowledge loaded on-demand. A single agent stays in control while loading context from skills as needed.|
|[**Router**](https://docs.langchain.com/oss/python/langchain/multi-agent/router)|A routing step classifies input and directs it to one or more specialized agents. Results are synthesized into a combined response.|
|[**Custom workflow**](https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow)|Build bespoke execution flows with [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), mixing deterministic logic and agentic behavior. Embed other patterns as nodes in your workflow.|
### Choosing a pattern
Use this table to match your requirements to the right pattern:

|Pattern|Distributed development|Parallelization|Multi-hop|Direct user interaction|
|---|---|---|---|---|
|[**Subagents**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)|⭐⭐⭐⭐⭐|⭐⭐⭐⭐⭐|⭐⭐⭐⭐⭐|⭐|
|[**Handoffs**](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)|—|—|⭐⭐⭐⭐⭐|⭐⭐⭐⭐⭐|
|[**Skills**](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)|⭐⭐⭐⭐⭐|⭐⭐⭐|⭐⭐⭐⭐⭐|⭐⭐⭐⭐⭐|
|[**Router**](https://docs.langchain.com/oss/python/langchain/multi-agent/router)|⭐⭐⭐|⭐⭐⭐⭐⭐|—|⭐⭐⭐|

- **Distributed development**: Can different teams maintain components independently?
- **Parallelization**: Can multiple agents execute concurrently?
- **Multi-hop**: Does the pattern support calling multiple subagents in series?
- **Direct user interaction**: Can subagents converse directly with the user?

Performance Comparison 
	Key metrics:
		- more models calls = higher latency
		- Tokens processed: more tokens = higher processing costs and context limits

#### Subagents
- A main agent coordinates subagents as tools. 
- All routing passes through the main agent.
![[Pasted image 20260217022220.png]]

#### Handoffs
- Agents transfer control to each other via tool calls. 
- Each agent can hand off to others or respond directly to the user.
![[Pasted image 20260217022252.png]]

#### Skills
A single agent loads specialized prompts and knowledge on-demand while staying in control.
![[Pasted image 20260217022309.png]]

#### Router
- A routing step classifies input and directs it to specialized agents. 
- Results are synthesized.
![[Pasted image 20260217022331.png]]

![[Pasted image 20260217022354.png]]
**Key insight:** Handoffs, Skills, and Router are most efficient for single tasks (3 calls each). Subagents adds one extra call because results flow back through the main agent—this overhead provides centralized control.
#### Subagents
![[Pasted image 20260217022426.png]]

#### Handoffs
![[Pasted image 20260217022514.png]]
#### Skills
![[Pasted image 20260217022557.png]]
#### Router
![[Pasted image 20260217022610.png]]

---
![[Pasted image 20260217022649.png]]
Stateful patterns (Handoffs, Skills) save 40-50% of calls on repeat requests. Subagents maintain consistent cost per request—this stateless design provides strong context isolation but at the cost of repeated model calls.
#### Subagents
**4 calls again → 8 total**

- Subagents are **stateless by design**—each invocation follows the same flow
- The main agent maintains conversation context, but subagents start fresh each time
- This provides strong context isolation but repeats the full flow

#### Handoffs
**2 calls → 5 total**

- The coffee agent is **still active** from turn 1 (state persists)
- No handoff needed—agent directly calls `buy_coffee` tool (call 1)
- Agent responds to user (call 2)
- **Saves 1 call by skipping the handoff**

#### Skills
**2 calls → 5 total**

- The skill context is **already loaded** in conversation history
- No need to reload—agent directly calls `buy_coffee` tool (call 1)
- Agent responds to user (call 2)
- **Saves 1 call by reusing loaded skill**

#### Router
**3 calls again → 6 total**

- Routers are **stateless**—each request requires an LLM routing call
- Turn 2: Router LLM call (1) → Milk agent calls buy_coffee (2) → Milk agent responds (3)
- Can be optimized by wrapping as a tool in a stateful agent

---
![[Pasted image 20260217023123.png]]
Each language agent/skill contains ~2000 tokens of documentation. All patterns can make parallel tool calls.

**Key insight:** 
- For multi-domain tasks, patterns with parallel execution (Subagents, Router) are most efficient. 
- Skills has fewer calls but high token usage due to context accumulation. 
- Handoffs is inefficient here—it must execute sequentially and can’t leverage parallel tool calling for consulting multiple domains simultaneously.

#### Subagents
![[Pasted image 20260217023322.png]]
Each subagent works in **isolation** with only its relevant context. Total: **9K tokens**.
#### Handoffs
![[Pasted image 20260217023410.png]]
Handoffs executes **sequentially**—can’t research all three languages in parallel. Growing conversation history adds overhead. Total: **~14K+ tokens**.
#### Skills
![[Pasted image 20260217023449.png]]
After loading, **every subsequent call processes all 6K tokens of skill documentation**. Subagents processes 67% fewer tokens overall due to context isolation. Total: **15K tokens**.

This diagram is likely a warning about **Context Accumulation**. It is showing you that once you load heavy data (6K tokens) into the context window, **you pay that "tax" on every single turn** that follows.

- If the agent had to do 5 more reasoning steps (e.g., "Check Python," then "Check JS," then "Check Rust"), **all 5 calls** would cost **7K tokens each**.
    
- This is why "Call 3" looks like a duplicate—it is carrying the same heavy payload as Call 2 to ensure the LLM has the context needed to write the final answer.

#### Router 
![[Pasted image 20260217024438.png]]
Router uses an **LLM for routing**, then invokes agents in parallel. Similar to Subagents but with explicit routing step. Total: **9K tokens**.

---
### Summary
Here’s how patterns compare across all three scenarios:

| Pattern                                                                                | One-shot | Repeat request | Multi-domain          |
| -------------------------------------------------------------------------------------- | -------- | -------------- | --------------------- |
| [**Subagents**](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents) | 4 calls  | 8 calls (4+4)  | 5 calls, 9K tokens    |
| [**Handoffs**](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)   | 3 calls  | 5 calls (3+2)  | 7+ calls, 14K+ tokens |
| [**Skills**](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)       | 3 calls  | 5 calls (3+2)  | 3 calls, 15K tokens   |
| [**Router**](https://docs.langchain.com/oss/python/langchain/multi-agent/router)       | 3 calls  | 6 calls (3+3)  | 5 calls, 9K tokens    |

**Choosing a pattern:**

| Optimize for          | [Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents) | [Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) | [Skills](https://docs.langchain.com/oss/python/langchain/multi-agent/skills) | [Router](https://docs.langchain.com/oss/python/langchain/multi-agent/router) |
| --------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Single requests       |                                                                                    | ✅                                                                                | ✅                                                                            | ✅                                                                            |
| Repeat requests       |                                                                                    | ✅                                                                                | ✅                                                                            |                                                                              |
| Parallel execution    | ✅                                                                                  |                                                                                  |                                                                              | ✅                                                                            |
| Large-context domains | ✅                                                                                  |                                                                                  |                                                                              | ✅                                                                            |
| Simple, focused tasks |                                                                                    |                                                                                  | ✅                                                                            |                                                                              |