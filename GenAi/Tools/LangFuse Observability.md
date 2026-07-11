```python
LANGFUSE_SECRET_KEY=settings.LANGFUSE_SECRET_KEY
LANGFUSE_PUBLIC_KEY=settings.LANGFUSE_PUBLIC_KEY
LANGFUSE_BASE_URL=settings.LANGFUSE_BASE_URL

from langfuse import get_client, observe

@observe()
async def create_task():

```