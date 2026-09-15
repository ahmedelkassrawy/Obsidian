---
description: "The .env variables that turn LangSmith tracing on and the two lines of Python that load them."
domain: ai-eng
type: howto
status: stub
tags:
  - domain/ai-eng
  - type/howto
  - status/stub
  - topic/observability
  - topic/langgraph
  - topic/ai-evaluation
aliases:
  - "LangSmith tracing"
  - "LANGSMITH_TRACING"
hubs:
  - "[[Observability]]"
  - "[[LangGraph]]"
  - "[[AI Evaluation]]"
---
```.env
###### LANGSMITH CONFIGURATION ######
# Enable or disable LangSmith tracing (true/false)

LANGSMITH_TRACING= true
LANGSMITH_API_KEY= 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
LANGSMITH_PROJECT= default
```

```python
from dotenv import load_dotenv

load_dotenv()
```

```python
from langsmith.run_helpers import traceable

@tool
@traceable
def rag_process_tool(query: str) -> str:
    """Process queries using RAG to get relevant information from documents."""
    logger.info("rag_process_tool entered")

    result = rag_process(query)

    logger.info("rag_process_tool exited")
    return result
```