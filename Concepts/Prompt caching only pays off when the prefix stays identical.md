---
description: "LLM providers can reuse the processed prefix of a prompt, but only an exact match counts, so stable content must go first and changing content last."
type: zettel
status: digested
tags:
  - type/zettel
  - status/digested
  - topic/caching
  - topic/context-engineering
hubs:
  - "[[Caching]]"
  - "[[Context Engineering]]"
created: 2026-10-01
---
# Prompt caching only pays off when the prefix stays identical

## The idea
Before a model writes anything, it has to process the whole prompt (the prefill step). In an agent loop the prompt grows every turn: same system prompt, same tool definitions, same history, plus a bit more. Prompt caching lets the provider save the processed prefix and reuse it, which makes those tokens much cheaper and faster.

The rule is strict: the cache matches from the start of the prompt, and the first changed token breaks everything after it. So the order of the prompt matters. Things that never change go first (system prompt, tools), then things that grow (history), then things that change every call (the new message).

## Example
Putting the current timestamp at the top of the system prompt looks harmless, but it changes on every call, so the cache never hits. Moving it to the end of the prompt brings the cache back.

## Connects to
- [[Caching trades freshness for speed]] — same reuse-what-you-computed idea. Here staleness can't happen, because any change misses the cache.
- [[The context window is a budget, not a bucket]] — caching makes a long context cheaper, but trimming it still matters for quality and limits.

## Sources
- [[AI Agent Prompt Caching and Context Management]]
- [[LiteLLM Prompt Caching]]

## 30-second answer
> Prompt caching reuses the already-processed prefix of a prompt. It only matches exactly from the start, so you put stable content (system prompt, tools) first and changing content last. In agent loops that cuts cost and latency a lot, because most of each turn's prompt is a repeat.
