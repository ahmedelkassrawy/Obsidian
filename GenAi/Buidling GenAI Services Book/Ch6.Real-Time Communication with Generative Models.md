# Chapter 6 — Real-Time Communication with Generative Models

This chapter explores real-time communication techniques for streaming AI model outputs. It focuses on:

* HTTP request-response
* Short polling
* Long polling
* Server-Sent Events (SSE)
* WebSocket (WS)

The main goal is to stream LLM outputs in real time instead of waiting for full responses.

---
# Why Real-Time Streaming Matters in AI

AI inference introduces additional latency beyond traditional I/O latency. If you wait for full model completion before responding:
* Users experience long delays
* Responses appear as overwhelming text blocks
* Engagement drops

Streaming improves:
* Perceived responsiveness
* User engagement
* Progressive rendering of responses

However, streaming adds:
* Connection management complexity
* Reconnection logic
* Memory and concurrency overhead
* Scaling challenges

---
# Web Communication Mechanisms

## 1. HTTP Request–Response (Traditional)

**Characteristics:**

* Stateless
* One request → one response
* Widely supported
* Simple to implement

**Limitations:**
* No real-time updates
* Entire response must complete before sending

Best for:
* Standard REST APIs
* Non-real-time workloads

---
## 2. Short (Regular) Polling

Client repeatedly checks server for updates.
### Flow:
1. Client starts a job.
2. Server returns job ID.
3. Client periodically checks status.
### Pros:
* Simple
* Works everywhere
### Cons:
* Many unnecessary requests
* Poor scalability
* High server overhead

Best for:
* Batch jobs
* Infrequent updates
---
## 3. Long Polling
Improved version of short polling.
### Flow:
* Client sends request.
* Server keeps request open until data is available.
* After response, client reconnects.
### Pros:
* Fewer requests than short polling
* Near real-time
### Cons:
* Still resource-heavy
* Message ordering complexity
* Not truly persistent

Best for:
* Notifications
* Near real-time systems without persistent connections
---
# Server-Sent Events (SSE)

## What is SSE?

SSE creates a **persistent, unidirectional** HTTP connection:
Server → Client only
Client sends:

```
Accept: text/event-stream
```

Server responds with:

```
Content-Type: text/event-stream
```

Then continuously pushes events.

---

## Why SSE is Ideal for LLM Streaming

* Built on HTTP
* Simple to implement
* Auto-reconnect support
* Event IDs supported
* Native browser support (EventSource)

Best for:

* Chatbot streaming
* Live feeds
* Dashboards
* LLM token streaming

---

## SSE Streaming Example (Azure OpenAI)

### Async Chat Stream Generator

```python
# stream.py
import asyncio
import os
from typing import AsyncGenerator
from openai import AsyncAzureOpenAI

class AzureOpenAIChatClient:
    def __init__(self):
        self.aclient = AsyncAzureOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["OPENAI_API_ENDPOINT"],
            azure_deployment=os.environ["OPENAI_API_DEPLOYMENT"],
        )

    async def chat_stream(
        self, prompt: str, model: str = "gpt-3.5-turbo"
    ) -> AsyncGenerator[str, None]:

        stream = await self.aclient.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            stream=True,
        )

        async for chunk in stream:
            yield f"data: {chunk.choices[0].delta.content or ''}\n\n"

        await asyncio.sleep(0.05)
        yield f"data: [DONE]\n\n"
```

Key points:

* `stream=True` enables token streaming
* Prefix each chunk with `data:`
* End stream with `[DONE]`
* Small delay reduces client back pressure

---

## SSE Endpoint in FastAPI

```python
# main.py
from fastapi.responses import StreamingResponse
from stream import azure_chat_client

@app.get("/generate/text/stream")
async def serve_text_to_text_stream_controller(prompt: str):
    return StreamingResponse(
        azure_chat_client.chat_stream(prompt),
        media_type="text/event-stream"
    )
```

---

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Production note:
Restrict origins instead of using `"*"`.

---

## SSE with POST

GET has limitations:

* No request body
* URL length limits
* Less secure

POST workaround:

```python
@app.post("/generate/text/stream")
async def serve_text_to_text_stream_controller(prompt: str):
    return StreamingResponse(
        azure_chat_client.chat_stream(prompt),
        media_type="text/event-stream"
    )
```

Note:
EventSource officially supports GET only. POST requires custom client handling.

---
# Streaming Hugging Face Models

## Run vLLM Inference Server

```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=<secret>" \
    -p 8080:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model mistralai/Mistral-7B-v0.1
```

---
## Async Hugging Face Stream Client

```python
import asyncio
from typing import AsyncGenerator
from huggingface_hub import AsyncInferenceClient

client = AsyncInferenceClient("http://localhost:8080")

async def chat_stream(prompt: str) -> AsyncGenerator[str, None]:
    stream = await client.text_generation(prompt, stream=True)
    async for token in stream:
        yield token
    await asyncio.sleep(0.05)
```

---
# WebSocket (WS)

## What is WebSocket?

* Persistent
* Full-duplex (bidirectional)
* Runs over TCP
* Lower overhead than HTTP after handshake

Best for:

* Multiplayer apps
* Collaborative tools
* Speech-to-text
* Voice applications
* Real-time duplex AI systems

---
## WebSocket Opening Handshake

Example:

```
GET ws://localhost:8000/generate/text/stream HTTP/1.1
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Key: ...
Sec-WebSocket-Version: 13
```

Production use:

```
wss://
```

(encrypted via TLS)

---
# WebSocket Connection Manager

```python
# stream.py
from fastapi.websockets import WebSocket
from typing import List

class WSConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()

    @staticmethod
    async def receive(websocket: WebSocket):
        return await websocket.receive_text()

    @staticmethod
    async def send(message, websocket: WebSocket):
        if isinstance(message, str):
            await websocket.send_text(message)
        elif isinstance(message, bytes):
            await websocket.send_bytes(message)
        else:
            await websocket.send_json(message)
```

---
## Broadcast Support

```python
async def broadcast(self, message):
    for connection in self.active_connections:
        await self.send(message, connection)
```

---
## Unified Streaming Method (SSE + WS)

```python
async def chat_stream(
    self, prompt: str, mode: str = "sse", model: str = "gpt-4o"
):
    stream = ...
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield (
                f"data: {chunk.choices[0].delta.content}\n\n"
                if mode == "sse"
                else chunk.choices[0].delta.content
            )

    await asyncio.sleep(0.05)

    if mode == "sse":
        yield f"data: [DONE]\n\n"
```

---
## WebSocket Endpoint in FastAPI

```python
# main.py
from fastapi.websockets import WebSocket, WebSocketDisconnect
from stream import ws_manager, azure_chat_client
import asyncio

@app.websocket("/generate/text/stream")
async def websocket_endpoint(websocket: WebSocket):

    await ws_manager.connect(websocket)

    try:
        while True:
            prompt = await ws_manager.receive(websocket)

            async for chunk in azure_chat_client.chat_stream(prompt, "ws"):
                await ws_manager.send(chunk, websocket)

            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        pass
    finally:
        await ws_manager.disconnect(websocket)
```

---
# SSE vs WebSocket Comparison

| Feature        | HTTP             | Short Polling | Long Polling  | SSE             | WebSocket             |
| -------------- | ---------------- | ------------- | ------------- | --------------- | --------------------- |
| Persistent     | No               | No            | Partial       | Yes             | Yes                   |
| Direction      | Request/Response | Client-driven | Client-driven | Server → Client | Bidirectional         |
| Complexity     | Low              | Low           | Medium        | Low             | High                  |
| Auto Reconnect | No               | No            | No            | Yes             | Manual                |
| Binary Support | Yes              | Yes           | Yes           | No              | Yes                   |
| Best For       | REST APIs        | Batch jobs    | Notifications | LLM streaming   | Real-time duplex apps |

---
# Key Takeaways

* Use HTTP for non-real-time APIs.
* Use short polling for batch jobs.
* Use long polling for near-real-time updates.
* Use SSE for streaming LLM outputs (recommended default).
* Use WebSocket when you need full-duplex communication.
* SSE is simpler and sufficient for most GenAI chat applications.
* WebSocket introduces statefulness and scaling complexity.
* Always manage concurrency, reconnection, and resource cleanup carefully.

---
