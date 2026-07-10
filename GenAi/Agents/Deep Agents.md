Most agents today are shallow.
They easily break down on long, multi-step problems (e.g., deep research or agentic coding).

We’re entering the era of "Deep Agents", systems that strategically plan, remember, and delegate intelligently for solving very complex problems.

![[Pasted image 20260502142040.png]]

## Planning
- Instead of reasoning ad-hoc inside a single context window, Deep Agents maintain structured task plans they can update, retry, and recover from.
- Think of it as a living to-do list that guides the agent toward its long-term goal.
- Planning will also be critical for long-horizon problems (think agents for scientific discovery, which comes next).

## Orchestrator & Sub-agent Architecture
![[Pasted image 20260502142335.png]]

- One big agent (typically with a very long context) is no longer enough.
- An orchestrator manages specialized sub-agents such as search agents, coders, KB retrievers, analysts, verifiers, and writers, each with its own clean context and domain focus.
- The orchestrator delegates intelligently, and subagents execute efficiently
---
## Context Retrieval and Agentic Search
![[Pasted image 20260502151253.png]]

High-quality structured memory is a thing of beauty.
Building with the orchestrator-subagents architecture means that you can also leverage hybrid memory techniques (e.g., agentic search + semantic search), and you can let the agent decide what strategy to use.

---
## Verification
![[Pasted image 20260502151440.png]]

Next to context engineering, verification is one of the most important components of an agentic system
Verification helps with making your agents more reliable and more production-ready.