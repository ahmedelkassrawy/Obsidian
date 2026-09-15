---
description: "A single snippet showing how to wrap a compiled LangGraph with langgraphics' watch() to visualize a run."
domain: ai-eng
type: howto
status: stub
tags:
  - domain/ai-eng
  - type/howto
  - status/stub
  - topic/langgraph
  - topic/observability
aliases:
  - "Langgraphics - Langgraph"
  - "graph visualization"
hubs:
  - "[[LangGraph]]"
  - "[[Observability]]"
---
```python
from langgraph.graph import StateGraph, MessagesState
from langgraphics import watch

workflow = StateGraph(MessagesState)
workflow.add_node(...)
workflow.add_edge(...)

graph = watch(workflow.compile())

await graph.ainvoke({"messages": [...]})
```