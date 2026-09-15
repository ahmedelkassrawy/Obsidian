---
description: "A three-line snippet adding APScheduler BackgroundScheduler interval jobs inside a FastAPI app file."
domain: backend
type: howto
status: stub
tags:
  - domain/backend
  - type/howto
  - status/stub
  - topic/fastapi
  - topic/celery-and-message-queues
aliases:
  - "BackgroundScheduler"
  - "APScheduler"
hubs:
  - "[[FastAPI]]"
  - "[[Celery & Message Queues]]"
---
In the api py file.
```python
scheduler = BackgroundScheduler()
scheduler.add_job(run_eval,"interval",minutes = 60)
scheduler.add_job(dashboard.change_data,"interval",days = 60)
scheduler.start()
```