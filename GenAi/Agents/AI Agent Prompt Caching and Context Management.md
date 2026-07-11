# AI Agent Optimization: Prompt Caching & Context Management

If you are building an AI Agent, the biggest challenge you will face is **Cost** and **Latency**, both of which increase with every Turn. In this video, I explained in detail how to properly utilize Prompt Caching to save over 80% of your costs.

## Topics Discussed
- **Mechanistic Breakdown:** The difference between Prefill and Decode, and how we skip the O(n²) computations.
- **KV Tensors Caching:** The concept of storing Key-Value pairs for the Static Prefix and dealing with O(1) Memory Read.
- **Prompt Architecture:** Why the order of Tools and system instructions is important so the Cache doesn't break.
- **Context Compaction:** The correct strategy for dealing with the Context Window when it fills up without losing the logic.
- **Efficiency Metrics:** How to calculate the Cache Hit Rate from the API Response and know exactly how much you are saving.

This video contains the technical essence that will transform your Agent from mere experiments into a Product ready for Scaling.

---
## The Problem: The Accumulating Cost of Chat History

**Three Consecutive Turns Sent to LLM:**

- **Turn 1:** Context Window contains System Prompt, Tool Definitions, and User Message 1. *Result:* New task. Full computation. Paid at base rate.
- **Turn 2:** Context Window adds Assistant Response 1 and User Message 2. Historical data is redundantly processed. *Result:* Prefix is fully re-sent. Paying again for historical data.
- **Turn 3:** Context Window grows further with Tool Calls, Results, Assistant Response 2, and User Message 3. *Result:* Compounding cost. Same prefix, billed full price every turn.

> **Key Insight:** You are paying for the whole conversation again every turn. This leads to increasing cumulative costs and frustrated users.

---

## The Solution: LLM Prompt Caching & Context Management

### Cache Architecture

| Component | Behavior | Cost |
| :--- | :--- | :--- |
| **Static Prefix (Locked)** <br>*(System Instructions, Tool Definitions, Project Context, Behavioral Guidelines)* | Identical across every turn. Computed once, cached. | **0.1x** (cached read) <br> *90% savings* |
| **Dynamic Suffix (Repeating)** <br>*(User Messages, Assistant Responses, Tool Calls)* | Grows with every turn. Unique to each request. Always billed as new computation. | **1.0x** (full price) |

### Visualizing Multiple Turns
- **Turn 1:** Static Prefix + Turn 1 Suffix (Full compute)
- **Turn 2:** Cached Static Prefix + Cached Turn 1 Suffix + **New** Turn 2 Suffix (Partial compute)

---

## Mechanistic Breakdown: Standard vs. Cached Prefill

### Turn 1 (Initial Context Setup)
- **Full Prefill** of all initial tokens (System + Tools + User Msg 1)
- Creates Q, K, V matrices
- Full KV Cache is saved
- **Price:** 1.0x (Full Compute)

### Turn 2+ (Optimized Subsequent Turn)
1. **Static Prefix:** Load KV from Cache (O(1) Memory Read)
2. **Dynamic Suffix:** Partial Prefill required (O(suffix length²))
3. **Result:** Static KV Cache loaded from storage, New Suffix KV computed

### Comparison
- **(A) Standard Prefill (No Cache):** Reads all tokens → Parallel Processing → O(n²) compute across ALL tokens
- **(B) Cached Prefill (Subsequent Turn):** Reads new query tokens, skips prefill for locked tokens. KV Cache Reader does O(1) Memory Read. Parallel processing only on new suffix tokens.
- **(C) Decode Phase:** Combined cache handed off to compute Q, attend, and generate tokens. Memory-bound O(n) per token.

---

## System Prompt Layering (Optimal Architecture)

*Recommended order for maximum cache hits:*

| Layer | Content | Cache Behavior |
| :--- | :--- | :--- |
| **Green (Stable/Top)** | Base System Instructions, Tools (Read, Write, Bash, Grep, Glob, etc.) | Globally cached |
| **White** | CLAUDE.md & Memory | Cached per project |
| **Orange** | Session State (env, MCP, output style) | Cached per session |
| **Red (Dynamic/Bottom)** | Messages (user messages, tool results, etc.) | Grows each turn, not cached |

> **Note:** System prompts are layered — stable instructions sit at the top, dynamic messages accumulate at the bottom.

---

## The Lifecycle: Context Caching & Compaction

### Standard Updates (Turns 1–10)
- Each turn reuses cached context
- Appends new actions/observations
- Window slides forward
- Cache breakpoint moves down over time (growing reusable context)

### Compaction Point (Turn 10)
When the full conversation buffer is nearly full:

1. **Forked Compaction Call** is made
2. Copy of all conversation messages sent with prompt: `+ SUMMARIZE THIS CONVERSATION`
3. This is a **Cache Hit** processed at 1/10 the price (~20k tokens max)
4. Creates a **Fresh Context Rebuild (Turn 11)**

> **Summary:** An AI agent's context is built by standard turns appending new actions and observations to a growing, dynamically-cached buffer. When the context window reaches capacity, a background summarization call is forked (at 1/10 cost), which efficiently condenses the history into a summary and re-attaches it. This creates a fresh, short context with significant room for new interactions while preserving essential history.

---

## Efficiency Metrics

**Formula for calculating cache efficiency:**

$$ \text{Efficiency} = \frac{\text{Cache Read}}{\text{Cache Read} + \text{Cache Creation}} $$

---

## Discussion & Community Insights

**Original Question:** Do you think Context Compaction is better done through LLM Summarization, or are there other methods like Vector DB Retrieval that might be more efficient in certain cases?

**Youssef Bastawisy:**
> In my opinion, it depends on the business case. If you have important steps whose details need to be known, you can use context offload to a file system. If the overall meaning is what matters most, there are many ways for compaction like summarization, or doing HeadTailCompaction where a percentage is tuned via traces. Great effort, Youssef 🫡

**Mohamed Sheded:**
> Thank you, Mohamed. I agree with you 100% that the Business Case is what dictates. I really loved the idea of Context Offload as an alternative if we need the Agent to retain hard details (we can consider it its functional memory) instead of them getting lost in the semantic space of the Vector DB.

---

## Practical Note for LangChain & CrewAI Users

> **Quick Point:** Caching doesn't just save money, it significantly reduces the **TTFT (Time To First Token)** because the model doesn't re-process the System Prompt every time. If your Agent is slow, try **Caching first** before you think about changing the model.

![[Pasted image 20260503141725.png]]
![[Pasted image 20260503141745.png]]![[Pasted image 20260503141836.png]]
![[Pasted image 20260503141859.png]]![[Pasted image 20260503142013.png]]
![[Pasted image 20260503142025.png]]