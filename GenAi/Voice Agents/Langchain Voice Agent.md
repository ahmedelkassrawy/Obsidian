1. STT > Agent > TTS architecture (The “Sandwich”)
2. Sppech to Speech 

#### Sandwich 
The Sandwich architecture composes three distinct components: speech-to-text (STT), a text-based LangChain agent, and text-to-speech (TTS).

![[Pasted image 20260219161744.png]]

Pros:
- Full control
- transparent behaviour with clear boundaries between components

Cons:
- requires orchestrating 
- additional complexity in managing the pipeline

#### Speech to Speech Arch
Speech-to-speech uses a multimodal model that processes audio input and generates audio output natively.

![[Pasted image 20260219161922.png]]

Pros:
- Simpler arch
- lower latency
- direct audio processing capture tone

Cons:
- limited model options
- less transpatrency in how audio is processed
- reduce controllability
---
### Architecture
Client (Browser)
- captures microphone audio and encode it as PCM (is the "rawest" form of digital audio.)
- Establishes WebSocket connection to the backend server
- Streams audio chunks to the server in real-time
- Receives and plays back synthesized speech audio

Server (Python)
- Accepts websocket connections from clients

The pipeline uses async generators to enable streaming at each stage. 
This allows downstream components to begin processing before upstream stages complete, minimizing end-to-end latency.

---
#### 1. Speech to text
- The STT stage transforms an incoming audio stream into text transcripts.
- Producer - Consumer Pattern : Audio chunks are sent to the STT  service concurrently with receiving transcript events.
- This allows transcription to begin before all audio has arrived

**Event Types**:
- `stt_chunk`: Partial transcripts provided as the STT service processes audio
- `stt_output`: Final, formatted transcripts that trigger agent processing

events.py
```python
import base64
import time
from dataclasses import dataclass
from typing import Literal, Union

def _now_ms() -> int:
    """Return current Unix timestamp in milliseconds."""
    return int(time.time() * 1000)

@dataclass
class UserInputEvent:
	"""Event emitted when raw audio is recieved from the user.
	This is the entry point of the voice agent pipeline."""
	
	type: Literal["user_input"]
	audio: bytes #raw PCM audio bytes
	ts: int #unix timestamp
	
	@classmethod
	def create(cls,audio:bytes) -> "UserInputEvent":
		"""Factory method to create a USerInputEvent event with current timestamp"""
		return cls(type = "user_input",
			audio = audio,
			ts = _now_ms()
		)
		
@dataclass
class STTChunkEvent:
	"""Event emitted during speech-to-text processing for partial transcription results.
	Theese chunks allow for real-time display of transcription progess to the user"""
	
	type:Literal["stt_chunk"]
	transcript: str
	ts:int 
	
	@classmethod
	def create(cls,transcript:str) -> "STTChunkEvent":
		"""Factory method to create STTChunkEvent"""
		return cls(type = "stt_chunk",
			transcript = transcript,
			ts = _now_ms()
		)
		
@dataclass
class STTOutputEvent:
	"""Event emitted when speech-to-text processing completes for a turn
	This represents the final , formatted transcription of the user's speech"""
	
	type: Literal["stt_output"]
	transcript: str
	ts:int
	
	@classmethod
	def create(cls,trasncript) -> "STTOutputEvent":
	 """Factory method to create an STTOutputEvent event with current timestamp."""
        return cls(type="stt_output", 
	        transcript=transcript, 
	        ts=_now_ms()
        )
        
STTEvent = Union[STTChunkEvent,STTOutputEvent]

@datalcass
class AgentChunkEvent:
	"""Event emiited during agent response generation for streaming text chunks
	As the llm generates its response,it streams tokens incrementally"""
	type:Literal["agent_chunk"]
	text:str
	ts:int 
	
	@classmethod
	def create(cls,text) -> "AgenthunkEvent":
		return cls(type = "agent_chunk"
			text = text,
			ts = _now_ms()
		)	
		
@dataclass
class AgentEndEvent:
	"""Event emitted when the agent has finished generating its response for a turn"""
	type:Literal["agent_end"]
	ts:int
	
	@classmethod
	def create(cls) -> "AgentEndEvent":
		return cls(type = "agent_end",ts: _now_ms())
		
@dataclass
class ToolCallEvent:
	"""Event emitted when the agent invokes a tool"""
	type:Literal["tool_call"]
	id:str #tool call id
	name:str
	args:dict
	ts:int
	
	@classmethod
	def create(cls,id:str,name:str,args:dict) -> "ToolCallEvent":
		return cls(type="tool_call", 
			id=id, 
			name=name, 
			args=args, 
			ts=_now_ms()
		)
		
@dataclass
class ToolResultEvent:
    """Event emitted when a tool completes execution and returns a result."""
    type:Literal["tool_result"]
    tool_call_id:str
    name:str
    result:str
    ts:int
    
    @classmethod
    def create(cls,tool_call_id:str,name:str,result:str) -> "ToolResultEvent":
	    return cls(type = "tool_result",
		    tool_call_id = tool_call_id,
		    name = name,
		    result = result,
		    ts = _now_ms(),
	    )
	    
AgentEvent = Union[AgentChunkEvent,AgendEndEvent,ToolCallEvent,ToolResultEvent]

@dataclass 
class TTSChunkEvent:
	"""Event emitted during text-to-speech synthesis for streaming audio chunks"""
	type:Literal["tts_chunk"]
	audio:bytes
	ts:int
	
	@classmethod
	def create(cls,audio:bytes):
		return cls(type = "tts_chunk", 
			audio=audio, 
			ts=_now_ms()
		)
		
VoiceAgentEvent = Union[UserInputEvent, STTEvent, AgentEvent, TTSChunkEvent]

def event_to_dict(event: VoiceAgentEvent) -> dict:
    """Convert a VoiceAgentEvent to a JSON-serializable dictionary."""
    if isinstance(event, UserInputEvent):
        return {
	        "type": event.type, 
	        "ts": event.ts
		}
    elif isinstance(event, STTChunkEvent):
        return {
	        "type": event.type, 
	        "transcript": event.transcript, 
	        "ts": event.ts
		}
    elif isinstance(event, STTOutputEvent):
        return {
	        "type": event.type, 
	        "transcript": event.transcript, 
	        "ts": event.ts
		}
    elif isinstance(event, AgentChunkEvent):
        return {
	        "type": event.type, 
	        "text": event.text, 
	        "ts": event.ts
		}
    elif isinstance(event, AgentEndEvent):
        return {
	        "type": event.type, 
			"ts": event.ts
		}
    elif isinstance(event, ToolCallEvent):
        return {
            "type": event.type,
            "id": event.id,
            "name": event.name,
            "args": event.args,
            "ts": event.ts,
        }
    elif isinstance(event, ToolResultEvent):
        return {
            "type": event.type,
            "toolCallId": event.tool_call_id,
            "name": event.name,
            "result": event.result,
            "ts": event.ts,
        }
    elif isinstance(event, TTSChunkEvent):
        return {
            "type": event.type,
            "audio": base64.b64encode(event.audio).decode("ascii"),
            "ts": event.ts,
        }
    else:
        raise ValueError(f"Unknown event type: {type(event)}")
```

assemblyai_stt.py

- this class is designed to handle a continuous stream of audio over a **WebSocket** using **asynchronous programming** (`asyncio`).
- **`format_turns = True`:** This is likely an AssemblyAI-specific setting that tells the engine to automatically add punctuation and capitalization to the transcribed text as people take turns speaking.
```python
import asyncio
import contextlib
import json
import os
from typing import AsyncIterator, Optional
from urllib.parse import urlencode
import websockets
from websockets.client import WebSocketClientProtocol
from events import STTChunkEvent, STTEvent, STTOutputEvent

class AssemblyAISTT:
    def __init__(
        self,api_key: Optional[str] = None,
        sample_rate: int = 16000,
        format_turns: bool = True,
    ):
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("AssemblyAI API key is required")

        self.sample_rate = sample_rate
        self.format_turns = format_turns
        
        self._ws: Optional[WebSocketClientProtocol] = None
        self._connection_signal = asyncio.Event()
        self._close_signal = asyncio.Event()

    async def receive_events(self) -> AsyncIterator[STTEvent]:
        while not self._close_signal.is_set():
            _, pending = await asyncio.wait(
                [
                    asyncio.create_task(self._close_signal.wait()),
                    asyncio.create_task(self._connection_signal.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            with contextlib.suppress(asyncio.CancelledError):
                for task in pending:
                    task.cancel()

            if self._close_signal.is_set():
                break

            if self._ws and self._ws.close_code is None:
                self._connection_signal.clear()
                try:
                    async for raw_message in self._ws:
                        try:
                            message = json.loads(raw_message)
                            message_type = message.get("type")

                            if message_type == "Begin":
                                pass
                            elif message_type == "Turn":
                                transcript = message.get("transcript", "")
                                turn_is_formatted = message.get(
                                    "turn_is_formatted", False
                                )

                                if turn_is_formatted:
                                    if transcript:
                                        yield STTOutputEvent.create(transcript)
                                else:
                                    yield STTChunkEvent.create(transcript)

                            elif message_type == "Termination":
                                # no-op
                                pass
                            else:
                                if "error" in message:
                                    print(f"AssemblyAISTT error: {message['error']}")
                                    break
                        except json.JSONDecodeError as e:
                            print(f"[DEBUG] AssemblyAISTT JSON decode error: {e}")
                            continue
                except websockets.exceptions.ConnectionClosed:
                    print("AssemblyAISTT: WebSocket connection closed")

    async def send_audio(self, audio_chunk: bytes) -> None:
        ws = await self._ensure_connection()
        await ws.send(audio_chunk)

    async def close(self) -> None:
        if self._ws and self._ws.close_code is None:
            await self._ws.close()
        self._ws = None
        self._close_signal.set()

    async def _ensure_connection(self) -> WebSocketClientProtocol:
        if self._close_signal.is_set():
            raise RuntimeError(
                "AssemblyAISTT tried establishing a connection after it was closed"
            )
        if self._ws and self._ws.close_code is None:
            return self._ws

        params = urlencode(
            {
                "sample_rate": self.sample_rate,
                "format_turns": str(self.format_turns).lower(),
            }
        )
        url = f"wss://streaming.assemblyai.com/v3/ws?{params}"
        self._ws = await websockets.connect(
            url, additional_headers={"Authorization": self.api_key}
        )

        self._connection_signal.set()
        return self._ws
```

```python
self._ws: Optional[WebSocketClientProtocol] = None
```
- As we discussed earlier, WebSockets keep a two-way connection open. This variable will eventually hold the active connection to AssemblyAI's servers.
- It starts as `None` because the connection hasn't been established yet (that usually happens in a separate `connect()` method).
- The underscore (`_ws`) is a Python convention signaling that this is a "private" variable meant only for internal use by the class, not to be messed with from the outside.
### The Asynchronous "Traffic Lights"
```python
self._connection_signal = asyncio.Event()
self._close_signal = asyncio.Event()
```

Because real-time audio streams use asynchronous programming (where the code doesn't wait for one thing to finish before doing another), you need a way to synchronize different parts of your application. `asyncio.Event()` acts like a digital traffic light.

- **`_connection_signal`:** When the program attempts to open the WebSocket, it takes a few milliseconds for the server to reply. 
	- If the audio capturer tries to send PCM data _before_ the socket is fully open, the app will crash. 
	- This event starts out as "Red" (cleared). 
	- Once the WebSocket handshake is successful, a different method will set this event to "Green" (`_connection_signal.set()`), signaling to the rest of the program: _"Okay, the connection is live, you can start streaming the raw audio bytes now."_
    
- **`_close_signal`:** Similarly, this is used to safely shut down the pipeline.
	- When the user stops talking or ends the session, this event is triggered so the program knows to stop capturing audio and gracefully close the WebSocket without losing the final few words.

```python
async def receive_events(self) -> AsyncIterator[STTEvent]:
        while not self._close_signal.is_set():
            _, pending = await asyncio.wait(
                [
                    asyncio.create_task(self._close_signal.wait()),
                    asyncio.create_task(self._connection_signal.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            with contextlib.suppress(asyncio.CancelledError):
                for task in pending:
                    task.cancel()

            if self._close_signal.is_set():
                break

            if self._ws and self._ws.close_code is None:
                self._connection_signal.clear()
                try:
                    async for raw_message in self._ws:
                        try:
                            message = json.loads(raw_message)
                            message_type = message.get("type")

                            if message_type == "Begin":
                                pass
                            elif message_type == "Turn":
                                transcript = message.get("transcript", "")
                                turn_is_formatted = message.get(
                                    "turn_is_formatted", False
                                )

                                if turn_is_formatted:
                                    if transcript:
                                        yield STTOutputEvent.create(transcript)
                                else:
                                    yield STTChunkEvent.create(transcript)

                            elif message_type == "Termination":
                                # no-op
                                pass
                            else:
                                if "error" in message:
                                    print(f"AssemblyAISTT error: {message['error']}")
                                    break
                        except json.JSONDecodeError as e:
                            print(f"[DEBUG] AssemblyAISTT JSON decode error: {e}")
                            continue
                except websockets.exceptions.ConnectionClosed:
                    print("AssemblyAISTT: WebSocket connection closed")
```

This method is the "listener" or the "ear" of your Speech-to-Text (STT) pipeline. Because it is an asynchronous generator (indicated by `-> AsyncIterator[STTEvent]`), its job is to continuously listen to the live WebSocket connection from AssemblyAI and `yield` transcription events one by one as they arrive, passing them downstream to your Large Language Model (LLM).

Here is a step-by-step breakdown of how this listening loop operates:
### 1. The Waiting Game (Synchronization)

```python
while not self._close_signal.is_set():
    _, pending = await asyncio.wait(
        [
            asyncio.create_task(self._close_signal.wait()),
            asyncio.create_task(self._connection_signal.wait()),
        ],
        return_when=asyncio.FIRST_COMPLETED,
    )
```

The method enters a continuous loop that runs until the pipeline is told to shut down (`_close_signal`).

Because the application shouldn't freeze while waiting for the connection to open, it uses `asyncio.wait()`. It races two events against each other and proceeds as soon as the **first one completes**:

1. The WebSocket successfully connects (`_connection_signal`).
2. The user or system abruptly stops the session before it even connects (`_close_signal`).

It then cleans up (cancels) the task that didn't trigger so it doesn't leave stray processes running in the background.
### 2. Reading the Stream

```python
if self._ws and self._ws.close_code is None:
    self._connection_signal.clear()
    try:
        async for raw_message in self._ws:
```

Once the green light is given (and assuming the WebSocket `_ws` is open), it clears the connection signal (so it can be reused later if the socket reconnects) and enters a new loop: `async for raw_message in self._ws`.

This acts as a continuous hose, reading every raw text message sent back by AssemblyAI's servers as soon as it arrives.
### 3. Parsing and Routing (The Core Logic)
```python
message = json.loads(raw_message)
message_type = message.get("type")
```

AssemblyAI sends data back as raw stringified JSON. The code parses it into a Python dictionary and checks the `"type"` to decide what to do next.

Here is how it handles the different message types:
- **`"Begin"` & `"Termination"`:** The server uses these to announce the start and end of a session. The code simply ignores them (`pass`) because the pipeline relies on its own internal signals for this.
    
- **`"Turn"`:** This is the actual transcription data. It extracts the `"transcript"` text and checks if `"turn_is_formatted"` is True.
    
    - **Formatted (`STTOutputEvent`):** If the turn is formatted, it means AssemblyAI has determined the user finished a thought. The text includes punctuation and capitalization. It yields a finalized `STTOutputEvent`.
        
    - **Unformatted (`STTChunkEvent`):** If it's not formatted, this is a "partial" transcript. AssemblyAI is sending back real-time, mid-sentence guesses (e.g., "hello", "hello world", "hello world how are..."). It yields an `STTChunkEvent` so your UI can display the text appearing in real-time before the sentence is finished.
        
- **Errors:** If the JSON contains an `"error"` key, it prints it and breaks out of the loop to prevent a crash.
### 4. Safety Nets (Error Handling)
The entire block is wrapped in `try/except` blocks to handle the harsh realities of network communication.
- `except json.JSONDecodeError`: If AssemblyAI sends a corrupted message that isn't valid JSON, the code catches the error, prints a debug message, and uses `continue` to just skip that message and wait for the next one.
    
- `except websockets.exceptions.ConnectionClosed`: If the internet drops or AssemblyAI cuts the connection, it catches it gracefully, prints a warning, and breaks the loop.
---
stt.py
```python
from typing import AsyncIterator
import asyncio
from assemblyai_stt import AssemblyAISTT
from events import VoiceAgentEvent

async def stt_stream(
    audio_stream: AsyncIterator[bytes],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Audio (Bytes) → Voice Events (VoiceAgentEvent)

    Uses a producer-consumer pattern where:
    - Producer: Reads audio chunks and sends them to AssemblyAI
    - Consumer: Receives transcription events from AssemblyAI
    """
    stt = AssemblyAISTT(sample_rate=16000)

    async def send_audio():
        """Background task that pumps audio chunks to AssemblyAI."""
        try:
            async for audio_chunk in audio_stream:
                await stt.send_audio(audio_chunk)
        finally:
            # Signal completion when audio stream ends
            await stt.close()

    # Launch audio sending in background
    send_task = asyncio.create_task(send_audio())

    try:
        # Receive and yield transcription events as they arrive
        async for event in stt.receive_events():
            yield event
    finally:
        # Cleanup
        with contextlib.suppress(asyncio.CancelledError):
            send_task.cancel()
            await send_task
        await stt.close()
```

---
#### Langchain agent
The agent stage processes text transcripts through a LangChain [agent](https://docs.langchain.com/oss/python/langchain/agents) and streams the response tokens. In this case, we stream all [text content blocks](https://docs.langchain.com/oss/python/langchain/messages#textcontentblock) generated by the agent.
### Key concepts
- **Streaming Responses**: The agent uses [`stream_mode="messages"`](https://docs.langchain.com/oss/python/langchain/streaming#llm-tokens) to emit response tokens as they’re generated, rather than waiting for the complete response. This enables the TTS stage to begin synthesis immediately.
- **Conversation Memory**: A [checkpointer](https://docs.langchain.com/oss/python/langchain/short-term-memory) maintains conversation state across turns using a unique thread ID. This allows the agent to reference previous exchanges in the conversation.
```python
from uuid import uuid4
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

def add_to_order(item: str, quantity: int) -> str:
    """Add an item to the customer's sandwich order."""
    return f"Added {quantity} x {item} to the order."

def confirm_order(order_summary: str) -> str:
    """Confirm the final order with the customer."""
    return f"Order confirmed: {order_summary}. Sending to kitchen."

agent = create_agent(
    model="anthropic:claude-haiku-4-5",  # Select your model
    tools=[add_to_order, confirm_order],
    system_prompt="""You are a helpful sandwich shop assistant.
    Your goal is to take the user's order. Be concise and friendly.
    Do NOT use emojis, special characters, or markdown.
    Your responses will be read by a text-to-speech engine.""",
    checkpointer=InMemorySaver(),
)

async def agent_stream(
    event_stream: AsyncIterator[VoiceAgentEvent],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Voice Events → Voice Events (with Agent Responses)

    Passes through all upstream events and adds agent_chunk events
    when processing STT transcripts.
    """
    # Generate unique thread ID for conversation memory
    thread_id = str(uuid4())

    async for event in event_stream:
        # Pass through all upstream events
        yield event

        # Process final transcripts through the agent
        if event.type == "stt_output":
            stream = agent.astream(
                {
	                "messages": [HumanMessage(content=event.transcript)]
				},
                {"configurable": {"thread_id": thread_id}},
                stream_mode="messages",
            )

            # Yield agent response chunks as they arrive
            async for message, _ in stream:
                if message.text:
                    yield AgentChunkEvent.create(message.text)
```
---
#### 3.Text to Speech
The TTS stage synthesizes agent response text into audio and streams it back to the client. 
Like the STT stage, it uses a producer-consumer pattern to handle concurrent text sending and audio reception.
##### Key concepts
**Concurrent Processing**: The implementation merges two async streams:
- **Upstream processing**: Passes through all events and sends agent text chunks to the TTS provider
- **Audio reception**: Receives synthesized audio chunks from the TTS provider

**Streaming TTS**: Some providers (such as [Cartesia](https://cartesia.ai/)) begin synthesizing audio as soon as it receives text, enabling audio playback to start before the agent finishes generating its complete response.
**Event Passthrough**: All upstream events flow through unchanged, allowing the client or other observers to track the full pipeline state.

cartesia_tts.py
```python
import base64
import json
import websockets

class CartesiaTTS:
    def __init__(
        self,
        api_key: Optional[str] = None,
        voice_id: str = "f6ff7c0c-e396-40a9-a70b-f7607edb6937",
        model_id: str = "sonic-3",
        sample_rate: int = 24000,
        encoding: str = "pcm_s16le",
    ):
        self.api_key = api_key or os.getenv("CARTESIA_API_KEY")
        
        self.voice_id = voice_id
        self.model_id = model_id
        
        self.sample_rate = sample_rate
        self.encoding = encoding
        
        self._ws: WebSocketClientProtocol | None = None

    def _generate_context_id(self) -> str:
        """Generate a valid context_id for Cartesia."""
        timestamp = int(time.time() * 1000)
        
        counter = self._context_counter
        self._context_counter += 1
        
        return f"ctx_{timestamp}_{counter}"

    async def send_text(self, text: str | None) -> None:
        """Send text to Cartesia for synthesis."""
        if not text or not text.strip():
            return

        ws = await self._ensure_connection()
        
        payload = {
            "model_id": self.model_id,
            "transcript": text,
            "voice": {
                "mode": "id",
                "id": self.voice_id,
            },
            "output_format": {
                "container": "raw",
                "encoding": self.encoding,
                "sample_rate": self.sample_rate,
            },
            "language": self.language,
            "context_id": self._generate_context_id(),
        }
        await ws.send(json.dumps(payload))

    async def receive_events(self) -> AsyncIterator[TTSChunkEvent]:
        """Yield audio chunks as they arrive from Cartesia."""
        async for raw_message in self._ws:
            message = json.loads(raw_message)

            # Decode and yield audio chunks
            if "data" in message and message["data"]:
                audio_chunk = base64.b64decode(message["data"])
                
                if audio_chunk:
                    yield TTSChunkEvent.create(audio_chunk)

    async def _ensure_connection(self) -> WebSocketClientProtocol:
        """Establish WebSocket connection if not already connected."""
        if self._ws is None:
            url = (
                f"wss://api.cartesia.ai/tts/websocket"
                f"?api_key={self.api_key}&cartesia_version={self.cartesia_version}"
            )
            self._ws = await websockets.connect(url)

        return self._ws
```

tts.py
```python
from cartesia_tts import CartesiaTTS
from utils import merge_async_iters

async def tts_stream(
    event_stream: AsyncIterator[VoiceAgentEvent],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Voice Events → Voice Events (with Audio)

    Merges two concurrent streams:
    1. process_upstream(): passes through events and sends text to Cartesia
    2. tts.receive_events(): yields audio chunks from Cartesia
    """
    tts = CartesiaTTS()

    async def process_upstream() -> AsyncIterator[VoiceAgentEvent]:
        """Process upstream events and send agent text to Cartesia."""
        async for event in event_stream:
            # Pass through all events
            yield event
            
            # Send agent text to Cartesia for synthesis
            if event.type == "agent_chunk":
                await tts.send_text(event.text)

    try:
        # Merge upstream events with TTS audio events
        # Both streams run concurrently
        async for event in merge_async_iters(
            process_upstream(),
            tts.receive_events()
        ):
            yield event
    finally:
        await tts.close()
```
---
#### Putting it all together
```python
from langchain_core.runnables import RunnableGenerator

pipeline = (
    RunnableGenerator(stt_stream)      # Audio → STT events
    | RunnableGenerator(agent_stream)  # STT events → Agent events
    | RunnableGenerator(tts_stream)    # Agent events → TTS audio
)

# Use in WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def websocket_audio_stream():
        """Yield audio bytes from WebSocket."""
        while True:
            data = await websocket.receive_bytes()
            yield data

    # Transform audio through pipeline
    output_stream = pipeline.atransform(websocket_audio_stream())

    # Send TTS audio back to client
    async for event in output_stream:
        if event.type == "tts_chunk":
            await websocket.send_bytes(event.audio)
```

We use [RunnableGenerators](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.base.RunnableGenerator) to compose each step of the pipeline. This is an abstraction LangChain uses internally to manage [streaming across components](https://reference.langchain.com/python/langchain_core/runnables/)

Each stage processes events independently and concurrently: audio transcription begins as soon as audio arrives, the agent starts reasoning as soon as a transcript is available, and speech synthesis begins as soon as agent text is generated. This architecture can achieve sub-700ms latency to support natural conversation.