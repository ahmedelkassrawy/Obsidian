---
description: "Hub: every note about Prompting"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/prompting
---
# Prompting

> [!info] Prompt techniques from zero-shot to ReAct, plus prompt-injection defence. The main note's code half is pre-1.0 LangChain.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/prompting`.

## Concepts
- [[Context Engineering]] — What context engineering is and how to do it: a deep-research-agent case study, layered context architecture, dynamic adjustment, and validation techniques.
- [[DSPy Optimization]] — The DSPy optimization workflow: how to build and split datasets, what an optimizer actually tunes, and a step-by-step walk through MIPROv2's bootstrapping and proposal stages.

## How-tos & recipes
- [[Anthropic Messages API Basics]] `raw` — Short pasted Anthropic SDK code: a single messages.create call and a helper pattern for multi-turn conversations that keeps history in a message list.
- [[LangChain Prompt Templates And LLMChain]] `stale` — Early LangChain notes on prompt templates feeding an LLMChain, with a football Q&A example.

## References & cheat sheets
- [[ALX Resources - Remote Job Boards and Career Prompts]] `raw` — A list of remote job boards (FlexJobs, WeWorkRemotely, Upwork, Remotive and others) followed by copy-paste ChatGPT prompts for LinkedIn profile review and career coaching.
- [[ALX Week 2 - Prompt Engineering Basics]] `raw` — ALX week 2 notes on how an LLM is trained (pretraining then RLHF) and the six building blocks of a good prompt.
- [[ALX Week 3 - Job Search Prompt Pack]] `raw` — ALX week 3 prompt templates for the job hunt: analysing a job description, writing a cover letter hook, and tailoring an application to a role.
- [[DSPy Programming]] `raw` — Large pasted code reference for programming in DSPy: calling the LM directly, modules, custom types, usage tracking and caching, and where adapters fit.

## Book notes
- [[Ch5. Prompt Engineering]] — Chip Huyen Ch5 notes: what makes a prompt effective, and how to defend an application against prompt injection and other prompt attacks.

## Course notes
- [[Prompt Engineering]] `stale` — Study guide on prompting: the sampling parameters, API roles, zero/one/few-shot and role prompting, then chain of thought and ReAct, with a LangChain script at the end.

## Related hubs
[[DSPy]], [[LangChain]], [[Resume & Job Search]], [[Context Engineering]], [[Agents]], [[AI Security]]

## Notes to self (from the audit)
- [[LangChain Prompt Templates And LLMChain]]: Uses pre-1.0 LLMChain and a hardcoded API key - port to LCEL/create_agent and rotate the key.
- [[Prompt Engineering]]: The LangChain section uses pre-1.0 ConversationChain and ConversationBufferMemory - the prompting content itself is still fine.
- [[ALX Resources - Remote Job Boards and Career Prompts]]: Owner-authored prompt dump - kept in place, not inboxed. Worth splitting the job boards from the prompts.
- [[ALX Week 2 - Prompt Engineering Basics]]: Lecture-numbered filename renamed. Content is close to a real concept note - a short rewrite would move it to digested.
- [[ALX Week 3 - Job Search Prompt Pack]]: Owner-authored prompt dump - kept in place, not inboxed.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
