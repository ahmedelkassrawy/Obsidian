---
description: "Hub: every note about LangChain"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/langchain
---
# LangChain

> [!info] v1 create_agent and middleware plus the multi-agent pattern series. Two notes still use pre-1.0 APIs.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/langchain`.

## Concepts
- [[Langchain.Multi Agent - Handoffs]] — The handoffs architecture explained: tools update a persisted state variable that decides which behaviour is active next, plus when to use it.
- [[Langchain.Multi Agent - Router]] — The router architecture: a classification step sends each input to the specialist agent for its vertical, and the router itself can be wrapped as a tool.
- [[Langchain.Multi Agent - Skills]] — The skills architecture: packaging prompt-driven specializations as invokable skills the agent calls on demand instead of stuffing them all in the system prompt.
- [[Langchain.Multi Agent - Subagents]] — The supervisor/subagent architecture: wrapping agents as tools, sync vs async execution, and why a single dispatch tool beats one tool per subagent.
- [[Langchain.Multi Agent Intro]] — Why multi-agent exists at all (context management and specialization) and a decision guide for choosing between the router, handoff, skills and subagent patterns.

## How-tos & recipes
- [[Langchain Voice Agent]] — Building a voice agent as an STT-agent-TTS sandwich: synchronizing the async pieces, reading the stream, routing parsed output, error handling, and the WebSocket endpoint.
- [[Langchain.Multi Agent - Handoffs Implementation]] — Implements the handoff/state-machine pattern: tools that set the current step, per-step prompts and tool sets, required state, and a way to go back a step.
- [[Langchain.Multi Agent - Skills Implementation]] — Implements the skills pattern with progressive disclosure - the agent loads only the skill it needs via a tool call - worked through a database schema and business-logic example.
- [[Langchain.Multi Agent Example]] — A worked multi-agent build: HITL middleware on the subgraphs, a checkpointer on the supervisor, and a three-layer tools/subagents/supervisor architecture with controlled information flow.
- [[Advanced RAG]] `stale` — Two advanced retrievers explained with code: the self-querying retriever that turns a question into a metadata filter, and the parent-document retriever.
- [[Hyde RAG]] `stale` — HyDE explained and implemented: have the model write a fake answer first, embed that instead of the question, and retrieve against it.
- [[LangChain Prompt Templates And LLMChain]] `stale` — Early LangChain notes on prompt templates feeding an LLMChain, with a football Q&A example.
- [[Langchain.Structured Output]] `stale` — Chatbot and chain code for getting structured output out of LangChain, including parallel chains and text splitting.
- [[RAG]] `stale` — End-to-end RAG guide: loading and splitting documents, embeddings and a vector store, retrieval, and generation.
- [[Run Agent - Langchain & Langgraph]] `raw` — Two pasted REPL loops - one LangChain, one LangGraph - for chatting with an agent from the terminal with a per-conversation thread_id.
- [[Sentence Window RAG]] `stale` — Sentence-window retrieval: match on single sentences, then expand a window of neighbours around each hit so the model gets continuous context.

## References & cheat sheets
- [[Langchain v1]] `raw` — Very large pasted reference for LangChain v1's create_agent: middleware hooks (before and after model), dynamic prompts, runtime and thread_id, and structured response formats.

## Course notes
- [[Prompt Engineering]] `stale` — Study guide on prompting: the sampling parameters, API roles, zero/one/few-shot and role prompting, then chain of thought and ReAct, with a LangChain script at the end.

## Related hubs
[[Multi-Agent Systems]], [[RAG]], [[Context Engineering]], [[LangGraph]], [[Prompting]], [[Vector Search]]

## Notes to self (from the audit)
- [[Langchain.Structured Output]]: Uses pre-1.0 imports (langchain.schema, langchain.text_splitter) - port to langchain_core before reusing.
- [[Langchain.Multi Agent Example]]: Contains a hardcoded API key - rotate it.
- [[LangChain Prompt Templates And LLMChain]]: Uses pre-1.0 LLMChain and a hardcoded API key - port to LCEL/create_agent and rotate the key.
- [[Prompt Engineering]]: The LangChain section uses pre-1.0 ConversationChain and ConversationBufferMemory - the prompting content itself is still fine.
- [[Advanced RAG]]: Uses pre-1.0 langchain.llms / langchain.vectorstores / langchain.chains imports - port before reusing.
- [[Hyde RAG]]: Implementation uses pre-1.0 RetrievalQA and langchain.vectorstores - the idea still holds, the code does not.
- [[RAG]]: Uses pre-1.0 langchain.embeddings / vectorstores / chains imports and has a hardcoded API key - port the code and rotate the key.
- [[Sentence Window RAG]]: Implementation uses pre-1.0 RetrievalQA and langchain.vectorstores - the technique is fine, the code is not.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
