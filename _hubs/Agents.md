---
description: "Hub: every note about Agents"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/agents
---
# Agents

> [!info] The largest agent collection in the vault: patterns, agency levels, workflows vs agents, production best practice, two case studies and a system-design note. Well digested.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/agents`.

> [!abstract] Start here: [[Agent Engineering MOC]]
> A guided map of the 13-note agent-engineering cluster (mechanics → state → control → safety → scale → infra → eval), most with runnable code and a suggested learning order.

## Concepts
- [[AI Workflows VS AI Agent]] — Separates fixed-code AI workflows (chaining, routing, parallelization) from autonomous agents, and gives rules for choosing or combining them.
- [[Agent Agency Levels And Reflection Pattern]] — A table of agency levels (from output-only to fully autonomous) plus the types of agent actions and the reflection pattern.
- [[Agent Evaluation]] — Argues that one-run accuracy or LLM-as-judge is not agent evaluation, and lists what a production eval harness must collect across repeated non-deterministic runs.
- [[Agentic System Best Practices]] — The patterns from Claude Code's architecture that transfer to any agentic system, starting with using an async generator as the agent loop instead of callbacks.
- [[Agents Best Practice]] — Production rules for agents treated as execution systems, not chat toys: orchestration, reliability handled by architecture, judgment left to the model.
- [[Claude Code Core Architecture]] — Deep dive into Claude Code's architecture: what separates an agent from a chatbot, the tech stack and scale, the execution flow, core components and the key design patterns.
- [[Context Engineering]] — What context engineering is and how to do it: a deep-research-agent case study, layered context architecture, dynamic adjustment, and validation techniques.
- [[Deep Agents]] — Short explanation of why shallow agents break on long tasks and the four things deep agents add: planning, orchestrator/sub-agents, agentic search, and verification.
- [[Deep Agents Best Practice]] — When to use the deep-agents pattern instead of one big agent, how to manage context and memory across sub-agents, and a tactical checklist of what works and what to avoid.
- [[Function Calling]] — How function calling drives the agent loop - tool definitions, the action/observation cycle, debugging bad tool calls, and rules for writing tool schemas.
- [[System Design for AI Agents (Architecture and the Why)]] — Trains you to defend every agent design decision: start from constraints, place the system on the agency spectrum, split into single-responsibility agents, and route for cost vs quality.
- [[Uber Eats — Designing Agents and Eval Loops (Production Case Study)]] — Production case study of Uber Eats' photo-enhancement agent system, focused on how each stage is wrapped in its own eval loop and how routing controls agency.
- [[Workers Concept]] — How to make scheduled agent work survive crashes on Cloudflare Workers using a sync plus watchdog pattern, state projection, heartbeats and reconciliation.
- [[camelAI - VM-less Agent in a Durable Object]] — Beginner-level walkthrough of how camelAI moved a coding agent off VMs into a Cloudflare Durable Object, explaining each term and comparing it to serverless sandboxes.
- [[Sandbox in Agent]] `stub` — Sketch of a two-layer agent sandbox: a Docker container per deployed agent, and a bubblewrap sandbox per bash tool call.

## How-tos & recipes
- [[03 - MCP host (client side)]] — Building the other end of MCP - a Gemini-backed host that connects to servers, manages connections, keeps a tool registry, and exposes a webhook.
- [[Agent with Tools]] — Tutorial notes on building a secure multi-user agent with Arcade.dev and LangGraph: per-user identity, authorized tool calls, and human-in-the-loop approval.
- [[LangGraph Agents]] — Walks through building a real LangGraph agent by hand: the tool loop, memory across turns, human approval before a tool runs, tool selection with 100 tools, and idempotent retries.
- [[Skill Creation]] — How to write an Agent Skill so it actually triggers: the name/description is the trigger, be precise about goals and loose about steps, and guard against skill rot.
- [[AWS Bedrock Agent Core]] `raw` — Pasted CLI and Python snippets for configuring, launching, and adding memory to an agent on AWS Bedrock AgentCore with LangGraph.
- [[CrewAI Agent Parameters And Context Window]] `raw` — Pasted CrewAI code showing every Agent parameter, attaching tools, how CrewAI manages the context window with RAG and knowledge sources, and calling an agent directly with kickoff().
- [[DeepAgents]] `raw` — Notes and code for the deepagents library: built-in planning with write_todos, streaming, the default StateBackend, and why a checkpointer is required for human-in-the-loop.
- [[Google ADK]] `raw` — Long compiled ADK tutorial: creating and running an agent project, building a multi-tool agent, agent teams, and adding memory.
- [[LlamaIndex Agents And Multi-Agent Workflows]] `raw` — Pasted LlamaIndex agent code: a basic FunctionAgent, running with a Context for state, setting Settings for LLM and embeddings, and defining a multi-agent workflow.
- [[Mem0.Agents Memory]] `raw` — Pasted Mem0 code for giving an agent long-term memory with Gemini models: init, add, search, and use memories in a chat loop.
- [[PydanticAi]] `raw` — Pasted PydanticAI starter code: creating an Agent with a Gemini model, running it, and carrying message history between runs.

## References & cheat sheets
- [[SKILLS Best Practice]] — The full Skills authoring guide: keep it concise, set the right degrees of freedom, skill structure and naming, writing descriptions that get discovered, and testing across models.
- [[Langchain v1]] `raw` — Very large pasted reference for LangChain v1's create_agent: middleware hooks (before and after model), dynamic prompts, runtime and thread_id, and structured response formats.

## Book notes
- [[Agent Orchestration And Tool Selection]] — Ch5 notes on orchestration: the common agent archetypes (reflex, ReAct, planner-executor, query-decomposition, reflection, deep research) and strategies for selecting tools.
- [[Agent UX Design]] — Ch3 notes on user experience for agentic systems: text and terminal interfaces, the discoverability problem, GUIs and generative UIs.
- [[Agents - Ai Engineering Book]] — Chip Huyen chapter notes on agents: what an environment and action set are, tool categories and function calling, planning vs execution, and agent memory.
- [[Building Applications with Agents.Ch1 & 2]] — Ch1-2 notes: build a minimal 'cancel order' agent in a LangGraph StateGraph, why scoping matters, a minimal evaluation, and the core components of an agent system.
- [[Ch1 - From LLMs to Agents - The Foundational Blueprint]] — Book chapter showing how a static LLM becomes an agent through a reason-act-observe loop, modelled as finite and hierarchical state machines and mapped onto LangGraph.
- [[Ch1 — Foundations of Agent Engineering]] — Book chapter defining an AI agent and its cognitive loop (perceive, reason, plan, act, learn) plus agent communication patterns.
- [[RAG And Agents - AI Engineering Book Ch6]] — Chip Huyen Ch6 notes on RAG and agents: why context construction matters, the RAG architecture, term-based vs embedding-based retrieval, and how retrieval feeds agents.

## Project notes
- [[Project Agent Arch]] — Architecture writeup for DataPilot AI, a LangGraph Text-to-SQL agent: the graph nodes from router through schema intelligence, memory, SQL generation, approval gate and retry loop.

## Clippings (raw)
- [[AI Engineering Reading Links]] `raw` — A bare list of URLs to vLLM, eval-harness, BMAD-method and LinkedIn/YouTube posts to read later.
- [[Clipping - Building Reliable Agentic AI Systems (Article)]] `raw` — Clipped case-study article on PRINCE, a production agentic RAG system for preclinical drug research: intent clarification, a planning step, researcher, reflection and writer agents, and how they built trust in it.
- [[Clipping - SMM System Client Meeting (Arabic)]] `raw` — Arabic tl;dv meeting summary for a social-media management product: agreed tasks and deadlines, finished features, platform integrations, access and security, system limits, AI content improvements, design, and the client brands.

## Related hubs
[[System Design]], [[Context Engineering]], [[LangGraph]], [[Agent Memory]], [[Multi-Agent Systems]], [[Claude Code]]

## Notes to self (from the audit)
- [[AWS Bedrock Agent Core]]: Pasted commands with almost no prose - add a short explanation of what each agentcore step does.
- [[Mem0.Agents Memory]]: Code only, no headings or prose - add a paragraph on when Mem0 beats a plain vector store.
- [[PydanticAi]]: Contains a hardcoded GEMINI_API_KEY in plain text - rotate that key and replace it with an env var.
- [[Sandbox in Agent]]: Placeholder - expand into a real note on isolating agent tool execution.
- [[AI Engineering Reading Links]]: Pure link dump with no annotations - note next to each link why it is worth reading.
- [[LlamaIndex Agents And Multi-Agent Workflows]]: Contains a hardcoded Google API key - rotate it.
- [[Clipping - Building Reliable Agentic AI Systems (Article)]]: Digest into AI-Eng/Agents - it is the only production multi-agent case study in the vault.
- [[Clipping - SMM System Client Meeting (Arabic)]]: Work meeting notes, not knowledge - this does not belong in a study vault. Move to the project repo or archive it.
- [[Project Agent Arch]]: Content is GenAI agent engineering - likely belongs in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
