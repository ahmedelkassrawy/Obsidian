---
tags:
  - ai-agents
  - llm
  - chapter-summary
  - foundational
---

# Ch1 — From LLMs to Agents: The Foundational Blueprint

> **Core Idea:** An LLM alone is a static text predictor. Embed it in a loop of **reasoning → acting → observing feedback**, give it **tools**, and it becomes a dynamic, stateful **agent**.

---

## 1. The Human ↔ Agent Parallel

| Human Developer | LLM Agent |
|----------------|-----------|
| Client request (prompt) | User prompt |
| Reasoning (sketch a plan) | LLM reasons about next step |
| Action (search docs, write code, debug) | Tool calls (search, calculator, APIs) |
| Feedback (test fails, code review) | Environment signals (errors, results) |
| Iterative refinement | Loop: reason → act → observe → adapt |

> [!quote] The Defining Trait
> "An LLM agent is a large language model embedded in a loop of reasoning, acting, and feedback, where it can call external tools and adapt its behavior based on results."

---

## 2. Bounded Autonomy

- Neither humans nor agents operate with **unbounded** freedom.
- Structure (coding standards / workflow guards) is what makes both **safe, reliable, and aligned**.
- Agents operate *only* within their provided tools, permissions, and safeguards — this is a **feature**, not a bug.

> [!note] Terminology
> This book uses *AI agent*, *agent*, and *LLM agent* interchangeably. Strictly speaking, an AI agent doesn't need an LLM (e.g. pure RL agents). LLMs add **generalization, reasoning, and natural language** to make agents flexible beyond narrow environments.

---

## 3. State Machines: The Blueprint for Agents

### Finite State Machines (FSMs)

| Term | Meaning | Agent Analogy |
|------|---------|---------------|
| **State** | Snapshot of what the system knows | Message list, routing hints, progress markers |
| **Event** | Something that happened | Tool invoked / tool returned a result |
| **Guard** | Check deciding which transition to take | "Did the last step succeed?" |
| **Action** | Work during a transition | Invoke a tool, append a message, checkpoint |
| **Termination** | End condition | Goal met or max steps reached |

FSMs are ideal when behavior alternates among a **few stable modes** and **recoverability matters** (checkpoint at each state boundary).

### Hierarchical State Machines (HSMs)

| Concept | Meaning |
|---------|---------|
| **Superstate** | Groups child states with shared entry/exit logic & guards |
| **Substate** | Concrete mode inside a superstate; inherits parent guards |
| **History** | "Remember where I was" marker (shallow = last child; deep = inside grandchildren) |
| **Parallel region** | Two+ child regions that advance independently (fan-out tool calls or agent roles) |

> [!tip] Why HSMs Matter
> Attach a **rate limit, safety filter, or circuit breaker** to a `WORKING` superstate so PLAN, ACT, and REFLECT all inherit the same safeguards — define once, reuse everywhere.

### Mapping to LangGraph

| FSM/HSM Concept | LangGraph Equivalent |
|----------------|----------------------|
| State schema | `TypedDict` (shared bus across parent & subgraphs) |
| Superstate | Subgraph |
| Substate | Node inside subgraph |
| Guard / Router | Conditional edge |
| History | `MemorySaver` checkpointing + `thread_id` |
| Parallel region | Fan-out tool calls or parallel subgraphs |

---

## 4. Static LLM vs. Agentic System

| Dimension | Static LLM | Agentic System |
|-----------|-----------|----------------|
| Mode | Single-pass token generator | Iterative reason–act–feedback loop |
| Knowledge | Confined to training data | Can retrieve, verify, update |
| Memory | Stateless | Stateful (short & long-term) |
| Workflow | Linear prompt → response | Iterative, adaptive |
| Tools | None | Search, code, APIs, retrieval |
| Interpretation | Fixed | Can refine/reinterpret goals |
| Validation | None external | Checks, corrects, improves output |

> [!example] Stateless vs. Stateful in Code
> **Stateless:** `llm.invoke("What are AI agents?")` — one call, no memory, no tools.
> **Stateful (LangGraph):** Graph with `AgentState`, `llm_node`, `tool_node`, conditional edges, and `MemorySaver` checkpointing — the agent can call tools, remember results across turns, and branch threads.

---

## 5. Core Agent Architecture (Figure 1-4)

```
User Request
     │
     ▼
┌─────────────────────────────┐
│         Planning             │
│  (CoT, ToT, self-critique)   │
├─────────────────────────────┤
│          Memory              │
│  (short-term / long-term)    │
├─────────────────────────────┤
│         Tools                │
│  (search, code, APIs, RAG)   │
└─────────────────────────────┘
     │
     ▼
  Action → Feedback → Adapt (loop)
```

- **Planning modules:** Chain-of-thought, tree-of-thought, self-critique
- **Memory modules:** Continuity across steps and sessions ([[Ch10 Memory Architectures]])
- **Tools:** Connect agent to environment

Modern LLMs (Kimi K2, Llama 4, Qwen 3.6) are increasingly **trained for agentic tasks** — tool use, coding, API invocation as a core capability.

---

## 6. The Autonomy Spectrum

```
Routers ──► Tool-calling Agents ──► Multi-Agent Systems ──► (Full Self-Direction)
   │               │                       │
   └── Single      └── Multi-step          └── Specialized agents
       decision        reasoning +              under a supervisor
                       reflection
```

**Orchestrated Autonomy** (today's reality):
- Routes between predefined paths ✓
- Selects tools/sub-agents ✓
- Revises prompts within bounds ✓
- ✗ Cannot redesign its own control graph
- ✗ Cannot create new tools autonomously
- ✗ Cannot operate as fully self-directed

> [!example] AI Scientist v2
> - Generates hypotheses, writes & debugs code, runs experiments, drafts papers
> - **Achievement:** First fully AI-generated paper accepted at a workshop (ICLR 2025)
> - **Limitations:** Workshop-level, not main track; two of three submissions rejected; citation errors, shallow analysis, dataset gaps
> - **Takeaway:** Impressive within boundaries, but still needs human oversight

---

## 7. Key Takeaways

1. **LLMs are static predictors** — they need state + control flow + tools to become agents.
2. **State machines (FSM/HSM)** provide the formal foundation for robust, recoverable agent design.
3. **LangGraph** maps directly to FSM/HSM concepts: state, nodes, conditional edges, subgraphs, checkpointing.
4. **Bounded autonomy is a strength** — constraints make agents safe, predictable, and deployable.
5. **Today's agents are orchestrated, not autonomous** — they make choices within fixed frameworks.
6. **The agent loop** (reason → act → observe → adapt) is what separates agents from simple LLM calls.

> [!next] Next: [[Ch2 - Architectures and Patterns]] — planning, reactivity, reflection, and human-agent interaction.

---

*Summary of Chapter 1 — "AI Agent Defentive Guide"* (July 2026)
