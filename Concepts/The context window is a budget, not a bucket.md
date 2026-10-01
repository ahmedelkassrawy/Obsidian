---
description: "Everything you put in an LLM's context costs money, latency and attention, so context engineering is choosing what goes in, not stuffing in everything that fits."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/context-engineering
  - topic/agents
hubs:
  - "[[Context Engineering]]"
  - "[[Agents]]"
created: 2026-10-01
---
# The context window is a budget, not a bucket

## The idea
It's tempting to treat a big context window like a bucket: everything fits, so throw it all in. But every token costs money and latency, and models get worse at using information buried in a long, noisy context. Long agent sessions also hit the hard limit eventually.

So treat context as a budget. Spend it on what this step actually needs. Tools: summarize or compact old turns, load instructions only when needed (the Skills pattern, progressive disclosure), retrieve instead of pasting whole documents, and split work across sub-agents so each one has a small, clean context.

## Example
An agent that pastes every tool result into history slows down and gets confused by turn 30. Keeping only a summary of old tool outputs, and the full text of recent ones, keeps it sharp and cheaper.

## Connects to
- [[Prompt caching only pays off when the prefix stays identical]] — caching lowers the cost of a long context but not the quality cost, so you need both.
- [[A RAG answer is only as good as its retrieval]] — RAG is context budgeting: fetch a few right chunks, not the whole knowledge base.
- [[Attention lets every token decide what to look at]] — the quadratic cost is why the budget exists at all.

## Sources
- [[Context Engineering]]
- [[Context-Compression Best Practices]]
- [[AI Agent Prompt Caching and Context Management]]
- [[Deep Agents Best Practice]]
- [[Langchain.Multi Agent - Skills Implementation]]

## 30-second answer
> Context is a budget: every token costs money and latency, and too much noise hurts accuracy. Context engineering means choosing what goes in for each step, using compaction, on-demand loading, retrieval and sub-agents instead of dumping everything into the window.
