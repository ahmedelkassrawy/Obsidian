---
description: "Ch6 notes comparing request/response, short polling, long polling, Server-Sent Events and WebSockets for streaming model output."
domain: ai-eng
type: book
status: digested
tags:
  - domain/ai-eng
  - type/book
  - status/digested
  - topic/fastapi
  - topic/http-and-networking
aliases:
  - "streaming"
  - "SSE"
  - "websockets"
hubs:
  - "[[FastAPI]]"
  - "[[HTTP & Networking]]"
---

## What this chapter covers

- When real-time communication is worth it in AI apps, and when it's overkill.
- The five web communication mechanisms: HTTP request-response, short polling, long polling, Server-Sent Events (SSE), and WebSocket (WS).
- Streaming LLM output to a browser with SSE (GET and POST) and with WebSocket.
- Handling errors and closing streaming connections cleanly.
- One API design rule that keeps streaming endpoints simple.

The goal: send the model's tokens to the user **as they're generated**, instead of making them wait for the full answer.

> [!note] Code in this note
> The book targets 2024-era libraries. I checked every snippet against the current docs (October 2026) and marked each change with a `# ⚠️` comment. Details are in the Verification note at the end.

---

## Why real-time streaming matters in AI

Plain HTTP is **stateless**: the server treats every request on its own, unrelated to the others. Normally it replies only once the whole request has been processed.

That's a problem for AI. On top of normal I/O latency, you now have **model inference latency**, which can be large. If you wait for the full completion:

- Users wait a long time.
- Then they get hit with a huge block of text all at once.
- Engagement drops.

If you send the data while it's being generated, users get it in small, readable chunks and stay engaged.

> [!warning] Streaming isn't free
> Sometimes it's overkill. Some models and APIs can't stream at all, and streaming adds work on both server and client:
> - Exceptions need different handling, and concurrent connections must be managed to avoid memory leaks.
> - If the client disconnects mid-stream, you can lose data or end up with server and client out of sync, so you may need reconnection and state logic.
> - Many open connections load your servers and raise hosting costs.
>
> Also weigh scalability, your latency needs, and browser support for the protocol you pick.

---

## Web communication mechanisms

### 1. HTTP request-response (traditional)

The client sends a request, the server processes it, and sends one response back.

- Stateless, simple, and supported by every client and server.
- No real-time updates: the full response has to be ready before anything is sent.

**Best for:** standard REST APIs and work that doesn't need real-time updates.

### 2. Short (regular) polling

> [!definition] Short polling
> The client sends HTTP requests at fixed intervals to ask "anything new?". Shorter intervals feel closer to real time but create more traffic.

The flow for a batch job (for example, generating images in bulk):

1. The client starts a job.
2. The server returns a unique job ID.
3. The client checks back periodically. The server replies with new data, or an empty response (maybe with a status) if it's not ready yet.

| Pros | Cons |
|---|---|
| Simple, works everywhere | Lots of requests even when nothing changed |
| | Overwhelms the server with many users, so it scales poorly |

You can soften the load with cached responses and rate limiting (Chapters 9 and 10).

**Best for:** checking the status of batch or inference jobs, infrequent updates.

### 3. Long polling

> [!definition] Long polling
> An improved short polling. The server keeps each request open ("hanging") until it has data to send. After the response, the connection closes and the client immediately opens a new one.

Both client and server are configured to avoid timeouts, so neither side gives up on the long request. That suits an LLM with unpredictable processing times, and it lets you skip building a batch job manager.

Each request-response cycle carries **one message**. The client gets many messages over time by reconnecting again and again.

| Pros | Cons |
|---|---|
| Fewer requests than short polling | The server still holds open requests, which costs resources |
| Near real time | Multiple open requests from one client can arrive **out of order** |
| | Not truly persistent |

**Best for:** notifications, and near-real-time features where persistent connections aren't available.

---

## Server-Sent Events (SSE)

> [!definition] Server-Sent Events (SSE)
> An HTTP-based way to open a **persistent, one-way** connection from server to client. While it's open, the server keeps pushing updates as data becomes available.

The client opens the connection once and doesn't need to keep re-establishing it, unlike long polling.

The handshake:

- The client sends a normal HTTP GET with `Accept: text/event-stream`.
- The server answers `200` with `Content-Type: text/event-stream`.
- After that, the server sends events over the same connection.

> [!definition] EventSource
> The browser's built-in interface for SSE. It opens the connection, and if the connection breaks it **reconnects automatically** after a short delay (a few seconds by default). The server can suggest the delay with a `retry:` field, in milliseconds.

### Why SSE fits LLM streaming

- It's plain HTTP, not a new protocol.
- Simple to implement, and simpler than WebSocket.
- Automatic reconnection and **event IDs** to resume interrupted streams, which long polling lacks.
- Native browser support through EventSource.

The catch: it's **one-way**. You send a normal HTTP request and get the answer back via SSE. So it fits apps that don't need to send data to the server mid-stream: news feeds, notifications, live dashboards, and LLM chat. ChatGPT uses SSE under the hood.

> [!tip]
> SSE should be your first choice for real-time features. Fall back to long polling only when updates are rare or your environment can't keep persistent connections.

---

## WebSocket (WS)

> [!definition] WebSocket
> A protocol for a **persistent, bidirectional (full-duplex)** connection. Both sides can send and receive data in any order while the connection is open.

- After the opening handshake it no longer speaks HTTP. RFC 6455 defines two-way messaging over a **single TCP connection**.
- Less protocol overhead than HTTP, so it's faster for data transfer.
- Runs over standard HTTP ports, so it works with existing security setups.

**Best for:** multiplayer games, collaborative tools, multimedia chat, speech-to-text, voice-to-voice, and other duplex AI apps.

> [!warning] WebSocket makes servers stateful
> A socket stays open on both sides for the whole connection. That makes scaling harder. Your service should also handle many concurrent handshakes and **authenticate them before opening** a connection, since each one uses server resources.

> [!note] Webhook ≠ WebSocket
> A **webhook** is server-to-server: one server tells another "send data to this endpoint when an event happens". There's no handshake and no open connection. It's real-time but one-way and non-persistent.

### Example 6-1: the opening handshake

The client sends an HTTP **upgrade** request. The connection starts in the **CONNECTING** state.

```http
GET ws://localhost:8000/generate/text/stream HTTP/1.1
Origin: http://localhost:3000
Connection: Upgrade
Host: http://localhost:8000
Upgrade: websocket
Sec-WebSocket-Key: 8WnhvZTK66EVvhDG++RD0w==
Sec-WebSocket-Protocol: html-chat, text-chat
Sec-WebSocket-Version: 13
```

- WebSocket URLs start with `ws://` instead of `http://`.
- `Connection: Upgrade` + `Upgrade: websocket` ask the server to switch protocols.
- `Sec-WebSocket-Key` is a random 16-byte Base64 string that confirms the server speaks WebSocket.
- `Sec-WebSocket-Protocol` lists subprotocols in order of preference. They define what data will be exchanged.

> [!warning] Use `wss://` in production
> `ws://` isn't encrypted, so any intermediary can read it, and old proxies may see the "strange" headers and drop the connection. `wss://` runs over TLS (like `https://`), so proxies just pass the encrypted packets through.

### Frames and the connection lifecycle

Once the handshake succeeds, the connection is **OPEN** and text or binary data flows both ways as **message frames**.

A frame has:

| Part | What it does |
|---|---|
| Fixed header | Basic info about the message |
| Extended payload length (optional) | The real length when the payload is over 125 bytes |
| Masking key | Masks client-to-server payloads, to block cache poisoning and cross-protocol attacks |
| Payload | The actual message |

Frame types are **text** (UTF-8), **binary**, and **fragmentation** (one message split into several frames and reassembled). **Control frames** manage the connection: **ping/pong** checks it's alive, and **close** ends it gracefully.

To close, either side sends a close frame, optionally with a status code and reason. The connection is then **CLOSING**, and becomes **CLOSED** when the other side answers with its own close frame.

---

## Comparing the mechanisms

| Feature | HTTP | Short polling | Long polling | SSE | WebSocket |
|---|---|---|---|---|---|
| Persistent | No | No | Partly | Yes | Yes |
| Direction | Request/response | Client-driven | Client-driven | Server → client | Bidirectional |
| Complexity | Low | Low | Medium | Low | High |
| Auto reconnect | No | No | No | Yes | Manual |
| Binary support | Yes | Yes | Yes | No | Yes |
| Best for | REST APIs | Batch jobs, simple dashboards | Notifications | LLM streaming, live feeds | Real-time duplex apps |

With SSE and WebSocket getting more popular, short and long polling are becoming less common.

---

## Implementing SSE endpoints

LLMs are **autoregressive**: each output token is appended to the input and fed back in until a stop token appears (Chapter 3). Instead of waiting for that loop to finish, you can forward each token to the user as it comes out.

Providers usually expose this as `stream=True`. You then get a data generator instead of the final output, and you can pass it straight to FastAPI.

### Example 6-2: async Azure OpenAI chat client

You need an Azure OpenAI resource with a model deployment. Note the endpoint, key, and deployment name. (The book used API version `2023-05-15`; see the warning below.)

```python
# stream.py
import asyncio
import os
from typing import AsyncGenerator

from openai import AsyncAzureOpenAI


class AzureOpenAIChatClient:
    def __init__(self):
        self.aclient = AsyncAzureOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],          # ⚠️ the SDK's own default env var is AZURE_OPENAI_API_KEY; the book's names work because they're passed explicitly
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["OPENAI_API_ENDPOINT"],  # ⚠️ SDK default: AZURE_OPENAI_ENDPOINT
            azure_deployment=os.environ["OPENAI_API_DEPLOYMENT"],
        )

    async def chat_stream(
        self, prompt: str, model: str = "gpt-4.1-nano"  # ⚠️ book had "gpt-3.5-turbo" (retired); on Azure this is your deployment name
    ) -> AsyncGenerator[str, None]:
        stream = await self.aclient.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            stream=True,
        )
        async for chunk in stream:
            if not chunk.choices:  # ⚠️ added: Azure's first chunk can carry only content-filter results with empty choices, so choices[0] would raise IndexError
                continue
            yield f"data: {chunk.choices[0].delta.content or ''}\n\n"
            await asyncio.sleep(0.05)  # ⚠️ my old note had this after the loop; the book sleeps between chunks
        yield "data: [DONE]\n\n"


azure_chat_client = AzureOpenAIChatClient()
```

- `AsyncAzureOpenAI` talks to models in your private Azure environment, asynchronously.
- `stream=True` makes the API return a stream of chunks instead of the full response.
- Each token gets the `data: ` prefix and a blank line (`\n\n`). That's the SSE format, so browsers can parse it with EventSource.
- `or ''` covers chunks where `delta.content` is `None`.
- `[DONE]` tells the client the stream is finished.
- The short sleep slows the stream down to reduce back pressure on clients.

> [!definition] Back pressure
> What happens when you send data faster than the client can consume it. The book's fix is to throttle the stream rate. Tune it by testing with different clients on different devices.

> [!warning] Azure API versions have moved on
> `AsyncAzureOpenAI` still exists in the current SDK and still needs `api_version`. But Microsoft now recommends the **v1 API**: use the plain `OpenAI` / `AsyncOpenAI` client with `base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"`, and no dated `api-version`. If you stay on `AsyncAzureOpenAI`, pick a current version from Azure's API lifecycle page rather than `2023-05-15`.

### Example 6-3: SSE endpoint with GET

```python
# main.py
from fastapi.responses import StreamingResponse
from stream import azure_chat_client

...

@app.get("/generate/text/stream")
async def serve_text_to_text_stream_controller(
    prompt: str,
) -> StreamingResponse:
    return StreamingResponse(
        azure_chat_client.chat_stream(prompt), media_type="text/event-stream"
    )
```

- It's a GET endpoint so the browser's EventSource can use it.
- `StreamingResponse` forwards the generator's output as it's produced.
- `media_type="text/event-stream"` is required by the SSE spec so browsers handle the response correctly.

> [!tip] Newer option: FastAPI's built-in SSE (0.135.0+)
> FastAPI now ships `fastapi.sse`. With `response_class=EventSourceResponse` you just `yield` events and FastAPI does the formatting. It also sends keep-alive pings every 15 seconds and sets `Cache-Control: no-cache` and `X-Accel-Buffering: no` for you. The book's `StreamingResponse` version still works.
>
> ```python
> # main.py (modern alternative)
> from collections.abc import AsyncIterable
> from fastapi.sse import EventSourceResponse, ServerSentEvent
>
> @app.get("/generate/text/stream", response_class=EventSourceResponse)
> async def serve_text_to_text_stream_controller(
>     prompt: str,
> ) -> AsyncIterable[ServerSentEvent]:
>     async for token in azure_chat_client.chat_stream(prompt, mode="ws"):  # raw tokens, no "data:" prefix (Example 6-14)
>         yield ServerSentEvent(raw_data=token)
>     yield ServerSentEvent(raw_data="[DONE]")
> ```
>
> Use `raw_data` for plain text. With `data=`, FastAPI JSON-encodes the value, so `"hello"` arrives with quotes.

### Example 6-4: SSE client with EventSource

A plain HTML page, no frameworks (libraries exist for React, Vue, SvelteKit, etc.). The key part is the script:

```html
<!-- pages/client-sse.html -->
<button id="streambtn">Start Streaming</button>
<label for="messageInput">Enter your prompt:</label>
<input type="text" id="messageInput" placeholder="Enter your prompt">
<div style="padding-top: 10px" id="container"></div>  <!-- ⚠️ book used id="responseContainer" but the script looks up 'container' -->

<script>
    let source;
    const button = document.getElementById('streambtn');
    const container = document.getElementById('container');
    const input = document.getElementById('messageInput');

    function resetForm() {
        input.value = '';
        container.textContent = '';
    }

    function handleOpen() {
        console.log('Connection was opened');
    }

    function handleMessage(e) {
        if (e.data === '[DONE]') {
            source.close();
            console.log('Connection was closed');
            return;
        }
        container.textContent += e.data;
    }

    function handleClose(e) {
        console.error(e);
        source.close();
    }

    button.addEventListener('click', function () {
        const message = input.value;
        const url = 'http://localhost:8000/generate/text/stream?prompt=' +
            encodeURIComponent(message);
        resetForm();

        source = new EventSource(url);
        source.addEventListener('open', handleOpen, false);
        source.addEventListener('message', handleMessage, false);
        source.addEventListener('error', handleClose, false);
    });
</script>
```

- Clicking the button opens a new `EventSource` on the GET endpoint, with the prompt URL-encoded.
- Each `message` event appends the token to the container until `[DONE]` arrives, then the connection is closed.
- On any error, it logs to the console and closes the connection.

### Example 6-5: serve the page from FastAPI

```python
# main.py
from fastapi.staticfiles import StaticFiles

app.mount("/pages", StaticFiles(directory="pages"), name="pages")
```

- Put the HTML in a `pages` folder. Each file is then at `<origin>/pages/<filename>`, e.g. `http://localhost:8000/pages/client-sse.html`.
- Serving the page from the **same origin** as the API avoids CORS blocking.

### Example 6-6: CORS

> [!definition] CORS (cross-origin resource sharing)
> A browser security check on requests sent to a different origin (domain) than the page came from. If your page is on `https://example.com` and calls `https://api.example.com`, the browser blocks it unless the API enables CORS. It only applies to requests sent from the browser, not server to server.

If you open the HTML file directly and click the button, nothing happens: the browser's preflight CORS check failed. For development, a CORS middleware lets everything through:

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # ⚠️ book had True; FastAPI docs: "*" origins/methods/headers can't be combined with allow_credentials=True
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- This allows any origin, method, and header.
- Streamlit doesn't hit CORS because it sends requests from its own server. FastAPI's `/docs` page doesn't either, since it's on the same origin.

> [!warning] Production
> Allow only the few origins, methods, and headers you actually need. If you need cookies (`allow_credentials=True`), list origins explicitly.

With async streaming, tokens can arrive so fast that the text appears as one block, even though it really is being streamed.

### Streaming Hugging Face models

The `transformers` library has a `TextStreamer`, but the easiest route is to run a separate inference server. The book uses vLLM in Docker.

#### Example 6-7: run vLLM

```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_TOKEN=<secret>" \
    -p 8080:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model mistralai/Mistral-7B-v0.1
# ⚠️ book used HUGGING_FACE_HUB_TOKEN; current vLLM docs pass HF_TOKEN
```

- Pulls and runs the `vllm/vllm-openai` image on all NVIDIA GPUs.
- The volume shares your Hugging Face cache, so weights aren't downloaded on every run.
- The token is needed for **gated** models like Mistral-7B.
- Host port 8080 maps to the container's port 8000.
- `--ipc=host` lets the container use the host's shared memory.
- vLLM serves an **OpenAI-compatible API**.

#### Example 6-8: consume the stream

The book's client:

```python
import asyncio
from typing import AsyncGenerator

from huggingface_hub import AsyncInferenceClient

client = AsyncInferenceClient("http://localhost:8080")


async def chat_stream(prompt: str) -> AsyncGenerator[str, None]:
    stream = await client.text_generation(prompt, stream=True)
    async for token in stream:
        yield token
        await asyncio.sleep(0.05)  # ⚠️ my old note had this after the loop; the book sleeps per token
```

> [!warning] The book mixes two servers here
> The text calls it "HF Inference Server", but Example 6-7 runs **vLLM's OpenAI-compatible server**. `text_generation` sends a TGI-style request (`POST /` with `{"inputs": ...}`), and that isn't one of the OpenAI-style routes vLLM serves. So the pairing likely won't work as printed.
>
> To talk to the vLLM server from Example 6-7, use an OpenAI-style client on `/v1`. Mistral-7B-v0.1 is a base model, so the plain completions route fits:
>
> ```python
> from openai import AsyncOpenAI
>
> client = AsyncOpenAI(base_url="http://localhost:8080/v1", api_key="EMPTY")
>
> async def chat_stream(prompt: str) -> AsyncGenerator[str, None]:
>     stream = await client.completions.create(
>         model="mistralai/Mistral-7B-v0.1", prompt=prompt, stream=True
>     )
>     async for chunk in stream:
>         if chunk.choices:
>             yield chunk.choices[0].text
>             await asyncio.sleep(0.05)
> ```
>
> `AsyncInferenceClient(base_url="http://localhost:8080/v1").chat_completion(..., stream=True)` also targets `/v1/chat/completions`, but that needs a model with a chat template.

### Example 6-9: SSE with POST

GET has limits:

- GET is usually less secure and more exposed to **XSS** (attackers injecting scripts that run in other users' browsers).
- No request body, so everything goes in query parameters. URLs have a length limit and need careful encoding.
- So you can't send the whole conversation history. The server has to track it.

The usual workaround is a POST SSE endpoint, even though the SSE spec doesn't cover it:

```python
# main.py
from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.responses import StreamingResponse
from stream import azure_chat_client


@app.post("/generate/text/stream")
async def serve_text_to_text_stream_controller(
    prompt: Annotated[str, Body(embed=True)],  # ⚠️ book had Body() with no embed; then FastAPI expects a bare JSON string and the client's {"prompt": ...} gets a 422
) -> StreamingResponse:
    return StreamingResponse(
        azure_chat_client.chat_stream(prompt), media_type="text/event-stream"
    )
```

- `Body(embed=True)` reads `prompt` from a JSON body shaped like `{"prompt": "..."}`.
- The new `fastapi.sse` works with POST too, if you prefer it.

**The client side (Example 6-10)** can't use EventSource, which only does GET. You process the stream by hand with `fetch`:

- Send a POST with `Content-Type: application/json`, `Accept: text/event-stream`, and the prompt as JSON.
- Get a reader with `response.body.getReader()` and a `TextDecoder`.
- Loop on `reader.read()`: stop when `done` is true, otherwise decode the chunk and append it to the page.

That's noticeably more complex than EventSource.

> [!tip] Alternatives to POST SSE
> - Send the large payload first with a normal POST. The server stores it, then uses it when the GET SSE connection opens.
> - SSE supports cookies, so you can carry larger data that way.

**Retries (Example 6-11).** In production, the client should also retry, handle errors, and be able to abort. The book wraps the connection in a loop: up to `maxRetries` attempts, a `try/catch` around connecting, `sleep(delay)` between attempts, and `delay *= backoffFactor` each time. That's **exponential backoff**, which also lowers the chance of hitting rate limits. After the last attempt it rethrows the error.

---

## Implementing WebSocket endpoints

FastAPI supports WebSocket through Starlette's `WebSocket` class. Connections need managing, so start with a connection manager.

### Example 6-12: connection manager

```python
# stream.py
from fastapi import WebSocket
from fastapi.websockets import WebSocketState


class WSConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)
        # ⚠️ book always called websocket.close(). If the client already left, that raises
        # (tested: RuntimeError on uvicorn's websockets backend, WebSocketDisconnect on wsproto).
        # FastAPI's docs example doesn't close here at all; this guard closes only if both sides are still open.
        if (
            websocket.application_state == WebSocketState.CONNECTED
            and websocket.client_state == WebSocketState.CONNECTED
        ):
            await websocket.close()

    @staticmethod
    async def receive(websocket: WebSocket) -> str:
        return await websocket.receive_text()

    @staticmethod
    async def send(
        message: str | bytes | list | dict, websocket: WebSocket
    ) -> None:
        if isinstance(message, str):
            await websocket.send_text(message)
        elif isinstance(message, bytes):
            await websocket.send_bytes(message)
        else:
            await websocket.send_json(message)


ws_manager = WSConnectionManager()
```

- `connect` accepts the handshake and stores the connection.
- `disconnect` removes it from the list and closes it if it's still open.
- `receive` reads incoming text. `send` picks the right method for text, bytes, or JSON.
- One shared `ws_manager` instance is reused across the app.

### Example 6-13: broadcast

Because the manager keeps every client in `active_connections`, it can message all of them. That's useful for system alerts, group chats, or collaborative editing.

```python
# stream.py
class WSConnectionManager:
    ...

    async def broadcast(self, message: str | bytes | list | dict) -> None:
        for connection in self.active_connections:
            await self.send(message, connection)
```

### Example 6-14: one chat stream for SSE and WS

WebSocket doesn't need the `data:` prefix or the `[DONE]` marker, so the stream method takes a `mode`:

```python
# stream.py
import asyncio
from typing import AsyncGenerator


class AzureOpenAIChatClient:
    def __init__(self):
        self.aclient = ...

    async def chat_stream(
        self, prompt: str, mode: str = "sse", model: str = "gpt-4o"  # on Azure, use your deployment name
    ) -> AsyncGenerator[str, None]:
        stream = ...  # OpenAI chat completion stream, as in Example 6-2
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:  # ⚠️ added the empty-choices guard (Azure content-filter chunk)
                yield (
                    f"data: {chunk.choices[0].delta.content}\n\n"
                    if mode == "sse"
                    else chunk.choices[0].delta.content
                )
                await asyncio.sleep(0.05)  # ⚠️ my old note had this after the loop; the book sleeps per chunk
        if mode == "sse":
            yield "data: [DONE]\n\n"
```

- Only non-empty content is sent.
- SSE mode wraps each token in `data: ...\n\n`. WS mode sends the raw token.
- `[DONE]` is sent only in SSE mode.

### Example 6-15: the WebSocket endpoint

```python
# main.py
import asyncio

from fastapi import WebSocket, WebSocketDisconnect  # ⚠️ book imported from fastapi.websockets; the FastAPI docs import from fastapi (both work)
from loguru import logger
from stream import azure_chat_client, ws_manager


@app.websocket("/generate/text/stream")  # the book prints "/streams" here but "/stream" elsewhere
async def websocket_endpoint(websocket: WebSocket) -> None:
    logger.info("Connecting to client....")
    await ws_manager.connect(websocket)
    try:
        while True:
            prompt = await ws_manager.receive(websocket)
            async for chunk in azure_chat_client.chat_stream(prompt, "ws"):
                await ws_manager.send(chunk, websocket)
                await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error with the WebSocket connection: {e}")
        await ws_manager.send("An internal server error has occurred", websocket)  # ⚠️ book left out the websocket argument (TypeError)
    finally:
        await ws_manager.disconnect(websocket)
```

- `@app.websocket` registers the route, reachable at `ws://localhost:8000/generate/text/stream`.
- The `while True` loop keeps the connection open: each message received is a prompt, and the chat stream's chunks are sent back one by one.
- The short sleep gives the client time to process the stream and reduces race conditions.
- `WebSocketDisconnect` is raised when the **client** closes the connection.
- Any other error is logged and reported to the client as a message.
- `finally` always cleans up: it removes the connection and closes it if it's still open.

> [!note] My old note vs the book
> My earlier version dropped the logging and the generic `except Exception` branch. Both are back.

**The client (Example 6-16)** uses the browser's `WebSocket`:

- `connectWebSocket()` opens `new WebSocket("ws://localhost:8000/generate/text/stream")` and wires up `onopen`, `onmessage`, `onclose`, `onerror`.
- `onmessage` appends `event.data` to the page.
- `onerror` sets an `isError` flag and closes the socket. `onclose` then reconnects with exponential backoff (`2^retryCount` seconds), up to `maxRetries = 5`.
- The Stream button sends the prompt with `ws.send(prompt)` only if `ws.readyState === WebSocket.OPEN`. The Close button clears `isError` first, so a manual close doesn't trigger a retry.

Test it at `http://localhost:8000/pages/client-ws.html`.

### SSE or WebSocket?

It depends on your app:

- **SSE** is simple, native to HTTP, and supported by most clients. If you only need one-way streaming to the client, the book recommends SSE for LLM output.
- **WebSocket** gives you more control and duplex communication on one connection: multi-user chat with an LLM, speech-to-text, text-to-speech, speech-to-speech. But it needs a protocol upgrade that older clients may not support, and exceptions are handled differently.

---

## Handling WebSocket exceptions

Once a WebSocket connection is accepted, you're no longer returning HTTP responses. There are no `4xx`/`5xx` status codes and no `HTTPException`.

So when something goes wrong:

1. **Send the client a WebSocket message** describing the issue.
2. Then **close the connection**, optionally with a WebSocket close code that explains why.

Clients and servers can use these codes to build custom closing behavior.

| Code | Meaning |
|---|---|
| 1000 | Normal closure |
| 1001 | Client navigated away, or server went down |
| 1002 | Protocol violation (e.g., unmasked packets, invalid payload length) |
| 1003 | Unsupported data (e.g., expected text, got binary) |
| 1007 | Inconsistently encoded data (e.g., non-UTF-8 in a text message) |
| 1008 | Policy violation; can hide closure details for security reasons |
| 1011 | Internal server error |

The full list is in RFC 6455, Section 7.4.

---

## Designing APIs for streaming

> [!warning] Don't expose a pile of streaming endpoints
> A common mistake is one streaming endpoint per step of a conversation. The client then has to switch endpoints and pass state each time, and both frontend and backend must manage conversation state while avoiding race conditions and network issues.

Better: give the client **one entry point** for streaming. Use headers, the request body, or query parameters to trigger the right logic on the backend.

- The backend has the databases, other services, and custom prompts, so it handles routing, CRUD operations, and switching prompts or models.
- The frontend stays simple, because it doesn't manage that state.

---

## Summary

- **HTTP request-response** for normal APIs that don't need real-time updates.
- **Short polling** for checking batch job status. Simple, but wasteful at scale.
- **Long polling** for near-real-time updates like notifications. Fewer requests, but the server holds open connections.
- **SSE** is the default for streaming LLM output: plain HTTP, one-way, auto-reconnect, EventSource in the browser. Use POST plus `fetch` when you need a request body.
- **WebSocket** when you need full duplex: voice, transcription, collaboration. It makes servers stateful and harder to scale.
- With WebSocket, report errors as messages, close with a close code, and always clean up connections.
- Prefer a single streaming entry point and keep routing logic on the backend.

**Next chapter:** integrating databases into AI services: schemas, SQLAlchemy, migrations, and saving data while streaming model output.

---

## Verification note

Checked on 2026-10-04 against:

- FastAPI SSE: https://fastapi.tiangolo.com/tutorial/server-sent-events/ (and `fastapi.sse` source in FastAPI 0.139.0)
- FastAPI WebSockets: https://fastapi.tiangolo.com/advanced/websockets/
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- Starlette `websockets.py`: https://github.com/encode/starlette/blob/master/starlette/websockets.py
- openai-python README: https://github.com/openai/openai-python, and the installed SDK (openai 3.7.0) source for `AsyncAzureOpenAI` and `ChatCompletionChunk`
- Azure OpenAI v1 API: https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle
- Azure content streaming: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-streaming (search summary only)
- vLLM Docker: https://docs.vllm.ai/en/stable/deployment/docker/ (search summary only; the page itself was blocked)
- huggingface_hub `AsyncInferenceClient` docstrings in the installed package (huggingface_hub 1.4.1)

Tested locally (FastAPI 0.139.0, Starlette 1.3.1, uvicorn 0.41.0): the WebSocket close-after-disconnect error, the guarded `disconnect`, `Body()` vs `Body(embed=True)`, both SSE endpoints with a fake token stream including an empty-`choices` chunk, and which URL `text_generation` posts to.

Changes marked ⚠️:

- Example 6-2: model default `gpt-3.5-turbo` → `gpt-4.1-nano` (the deployment-name example on Microsoft's page). On Azure it's really your deployment name.
- Example 6-2: noted the SDK's default env var names (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `OPENAI_API_VERSION`). Code unchanged.
- Examples 6-2 and 6-14: added a guard for empty `chunk.choices` (Azure content-filter chunk; the SDK type also says `choices` can be empty).
- Examples 6-2, 6-8, 6-14: moved `asyncio.sleep(0.05)` back inside the loop, matching the book (my old note had it after the loop).
- Azure `2023-05-15` API version: flagged; Microsoft now recommends the v1 API with the `OpenAI` client and `base_url`.
- Example 6-3: added FastAPI's built-in `fastapi.sse` (`EventSourceResponse`, `ServerSentEvent`, since 0.135.0) as a modern option. Book version kept.
- Example 6-4: fixed the container `id` mismatch in the book's HTML.
- Example 6-6: `allow_credentials=True` → `False` with wildcards, per the FastAPI CORS docs.
- Example 6-7: `HUGGING_FACE_HUB_TOKEN` → `HF_TOKEN`.
- Example 6-8: flagged that `text_generation` (TGI-style `POST /`) doesn't match vLLM's OpenAI-compatible server; added an `AsyncOpenAI` completions alternative.
- Example 6-9: `Body()` → `Body(embed=True)` so the client's `{"prompt": ...}` body is accepted.
- Example 6-12: `disconnect` closes only if both sides are still connected.
- Example 6-15: imports from `fastapi`; added the missing `websocket` argument in the error branch; restored logging.

Not verified:

- No live calls to Azure OpenAI or a running vLLM server. The vLLM route mismatch comes from the request `text_generation` sends plus vLLM serving OpenAI-style routes, not from a live run.
- The client-side JavaScript (Examples 6-4, 6-10, 6-11, 6-16) wasn't run in a browser.
- The book names the SSE page `sse-client.html` in one place and `client-sse.html` in another; I used `client-sse.html`.

%% related:start (auto-generated, regenerate with related_links.py) %%
## Related
- [[Streaming And Structured Outputs]]
- [[Pipecat]]
- [[Ch2. Selecting Your API Architecture]]
- [[Phase5 — Asynchronism & Communication]]
- [[gRPC and Protocol Buffers]]
%% related:end %%
