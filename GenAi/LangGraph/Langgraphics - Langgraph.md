```python
from langgraph.graph import StateGraph, MessagesState
from langgraphics import watch

workflow = StateGraph(MessagesState)
workflow.add_node(...)
workflow.add_edge(...)

graph = watch(workflow.compile())

await graph.ainvoke({"messages": [...]})
```