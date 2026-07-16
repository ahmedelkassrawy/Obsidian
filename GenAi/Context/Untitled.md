## Context Window Management[](https://handbook.exemplar.dev/ai_engineer/llms/pitfalls_llm#%EF%B8%8F-context-window-management)

Modern foundation models boast massive context windows (up to 128k to 2M+ tokens). However, filling these windows with raw text introduces latency and leads to information retrieval degradation.

### 1. The “Lost in the Middle” Effect[](https://handbook.exemplar.dev/ai_engineer/llms/pitfalls_llm#1-the-lost-in-the-middle-effect)

Research shows that LLMs are highly sensitive to the layout of information in their context windows. Models recall facts located at the very beginning and very end of their prompts with high accuracy, but their retrieval rate drops significantly for facts located in the middle:

```
[System instructions]     [Irrelevant history/sources]     [Active User Query]   (High Attention) ➔ ➔ ➔      (Low Attention)    ➔ ➔ ➔    (High Attention)   [Start of Prompt]             [Middle]                  [End of Prompt]
```

#### Optimization Guidelines[](https://handbook.exemplar.dev/ai_engineer/llms/pitfalls_llm#optimization-guidelines)

- **Anchor System Prompts:** Place core behavioral rules, rules of engagement, and schema requirements at the very beginning.
- **Place Context in the Center:** Insert retrieved documents, historical logs, or search results in the middle.
- **Position the Query at the End:** Always place the target question or parsing instruction at the very end of the prompt. This forces the model to focus on the active request.

### 2. Context Compression (LLMLingua)[](https://handbook.exemplar.dev/ai_engineer/llms/pitfalls_llm#2-context-compression-llmlingua)

Instead of sending raw source documents to the LLM, compress them first. Frameworks like **LLMLingua** use small language models (like Llama-3-8B) to calculate the perplexity of individual tokens in the prompt.

- Tokens that are highly predictable (low perplexity) are redundant and can be pruned.
- Tokens with high perplexity contain the core information and are kept.
- This approach can reduce prompt sizes by **30% to 50%** without degrading performance, leading to lower API costs and faster Time to First Token (TTFT).

### 3. Summarization Hierarchies for Agent Memory[](https://handbook.exemplar.dev/ai_engineer/llms/pitfalls_llm#3-summarization-hierarchies-for-agent-memory)

For long conversations, appending the complete history to every request will quickly exceed token limits. Instead, implement a **hierarchical summarization** pattern:

```
# System state tracking diagram# Raw Chats (Recent) -> Keep unmodified (e.g., last 5 turns)# Raw Chats (Older)  -> Summarize dynamically (e.g., every 10 turns)# Summary Block      -> Appended as static system state metadata
```

- **Active Window:** Keep the last 5 turns of conversation raw and unmodified.
- **Archived History:** Summarize the conversation’s first `$N$` turns into a structured bullet-point state block (e.g., _“User is querying API specs for project X”_).
- **Injection:** Inject the state block at the top of the prompt, discarding the older raw chat logs.