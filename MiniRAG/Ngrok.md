---
description: "A snippet that starts an ngrok tunnel in front of a local FastAPI app to get a public URL."
domain: ai-eng
type: howto
status: stub
tags:
  - domain/ai-eng
  - type/howto
  - status/stub
  - topic/http-and-networking
  - topic/fastapi
aliases:
  - "public URL"
  - "tunnel"
hubs:
  - "[[HTTP & Networking]]"
  - "[[FastAPI]]"
---
Masking a Public Url
```python
import ngrok
import uvicorn
from fastapi import FastAPI
from loguru import logger
from config import get_settings

settings = get_settings()

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Hello via ngrok!"}

if __name__ == "__main__":
    # Start ngrok tunnel
    listener = ngrok.forward(8000, authtoken=NGROK_AUTH_TOKEN)
    print(f"ngrok tunnel established at: {listener.url()}")
    logger.info(f"Public URL: {listener.url()}")

    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
```