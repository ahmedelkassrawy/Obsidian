Challenging Voice Ai
- **Speech recognition** must transcribe audio as users speak
- **Language models** need to process context and generate responses
- **Speech synthesis** has to convert text back to natural audio
- **Network transports** must handle streaming audio with minimal delay
## Ultra-Low Latency
Typical voice interactions complete in 500-800ms for natural conversations
## Modular Design
Swap AI providers, add features, or customize behavior without rewriting code
## Real-time Processing
Stream processing eliminates waiting for complete responses at each step
## Production Ready
Built-in error handling, logging, and scaling considerations

----
#### Core Concepts
Frames: 
Think of frames as **data packages** moving through your application. Each frame contains a specific type of information:
- Audio data from a microphone
- Transcribed text from speech recognition
- Generated responses from an LLM
- Synthesized audio for playback

Frame Processors 
Frame processors are **specialized workers** that handle specific tasks:
- A speech-to-text processor converts audio frames into text frames
- An LLM processor takes text frames and produces response frames
- A text-to-speech processor converts response frames into audio frames

Pipelines
Pipelines **connect processors together**, creating a path for frames to flow through your application. They handle the orchestration automatically.

1 Audio Input
User speaks → Transport receives streaming audio → Creates audio frames

2 Speech Recognition
STT processor receives audio frames → Transcribes speech in real-time → Outputs text frames

3 Context Management
Context processor aggregates text frames with conversation history → Creates formatted input for LLM

4 Language Processing
LLM processor receives context → Generates streaming response → Outputs text frames

5 Speech Synthesis
TTS processor receives text frames → Converts to speech → Outputs audio frames

6 Audio Output
Transport receives audio frames → Streams to user’s device → User hears response

![[Pasted image 20260223230320.png]]

Each processor in the pipeline:
1. Receives specific frame types as input
2. Performs its specialized task (transcription, language processing, etc.)
3. Outputs new frames for the next processor
4. Passes through frames it doesn’t handle
---
#### Session Initialization
- How to set up connections between users and your Pipecat voice AI bot
- This process is called **session initialization** - it’s how users and bots find each other and establish a communication channel for real-time audio exchange.
##### Architecture:
- Runner -> A fastapi server that handles incoming connection requests and manages session setup
- Pipecat Bot -> Your voice ai app running as a seperate server side service
- Client Application -> the user facing a web browser,mobile app,etc

The runner acts as the coordinator, setting up the necessary resources and starting bot instances
While the Pipecat bot handles the actual voice AI processing.

---
#### Development Runner
 - Pipecat provides a **development runner** that handles all the session initialization complexity for you.
 -  Instead of building FastAPI servers and managing WebRTC connections yourself, you focus on your bot logic while the runner handles the infrastructure.

Usage
Your bot needs a single entry point function that the runner will call:
```python
from pipecat.runner.types import RunnerArguments

async def bot(runner_args: RunnerArguments):
	"""Main bot entry point called by the development runner"""
	#create your transport based on the runner arguments
	transport = SmallWebRTCTransport(
		params = TransportParams(
			audio_in_enabled = True,
			audio_out_enbaled = True,
		),
		webrtc_connection = runner_args.webrtc_connection,
	)
	
	await rub_bot(transport)
	
if __name__ == "__main__": 
	from pipecat.runner.run import main 
	main()
```

```python
# P2P WebRTC (opens browser interface)
python bot.py -t webrtc

# Daily room-based WebRTC
python bot.py -t daily

# Telephony (requires ngrok or similar)
python bot.py -t twilio -x your_domain.ngrok.io
```

The development runner automatically:
- Creates the FastAPI server
- Sets up the appropriate endpoints
- Handles connection management
- Starts your bot instances
- Provides a web interface (for WebRTC)
----
#### Connections Typed Under The hood
While the development runner handles the complexity, understanding the three connection patterns helps you choose the right approach and debug issues:

1. P2P WebRTC Connections
2. Room-Based WebRTC (Daily)
3. WebSocket Connections(Telephony)

P2P WebRTC Connections
What happens:
- Runner serves a web interface at `http://localhost:7860/client`
- When you open the page and connect
- browser creates a WebRTC offer
- Runner recieves the offer, establishes connection and start your bot
- Browser and bot communicate directly via WebRTC

**When to use:** Direct client connections, embedded applications, local development

Room-Based WebRTC (Daily)
What happens:
- Room Request: User visits the client application and clicks to start a session
- Room Creation: Runner calls Daily's API to create a room and tokens using `pipecat.runner.daily.configure( )`
- Parallel Join: Both user's browser and your bot join the same Daily room
- Media Handshake: Once media streams are established, browser sends `client_ready` message
- Bot Activation: Your bot receives the event and starts the conversation
**When to use:** Video calls, group sessions, production deployments

WebSocket Connections(Telephony)
What happens: 
- Telephony provider (Twilio,etc..) recieves a phone call
- Provider connects to your runner's webhook endpoint
- Runner receives the WebSocket connection and parses the telephony specific messages
- Your bot starts immediately with the parsed connection data
**When to use:** Phone bots, telephony integrations
---
#### Starting Conversations
How and when your bot begins talking depends on the connection type:

- Immediate Start(P2P WebRTC, WebSocket)
These connections are ready immediately, so you can start talking right after connection:
```python
@transport.event_handler("on_client_connected")
async def on_client_connected(transport,client):
	logger.info("Client connected - starting conversation")
	
	messages.append(
		{
			"role":"system",
			"content": "Say hello and introduce yourself"
		}
	)
	await task.queue_frames([LLMRunFrame()])
```

- Handshake Required (Client/Server Room-based WebRTC)
for client/server apps using room-based WebRTC, a handshake ensures both sides are ready and the client wont miss the opening message:
```python
@rtvi.event_handler("on_client_ready")
async def on_client_ready(rtvi):
	await rtvi.set_bot_ready() #confirm the readiness to client
	#start convo
	await task.queue_frames([LLMRunFrame()])
```

>[!warning]
>For client/server room-based connections, waiting for `on_client_ready` is crucial - starting too early can cause the client to miss part of the initial message.

---
Process Isolation 
Each session run its own dedicated bot instance for:
- **Resource Management**: Dedicated CPU and memory per session
- **Error Isolation**: One session crash doesn’t affect others
- **Clean Cleanup**: Resources automatically freed when sessions end

The development runner handles this process management automatically.

Daily Integration
```python
from pipecat.runner.daily import configure

@app.post("/start")
async def start_bot(background_tasks: BackgroundTasks):
    async with aiohttp.ClientSession() as session:
        room_url, token = await configure(session)

        # Start bot instance
        background_tasks.add_task(run_bot, room_url, token)

        return {"room_url": room_url, "token": token}
```

WebSocket Telephony
```python
from pipecat.runner.utils import parse_telephony_websocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Parse provider-specific messages
    transport_type, call_data = await parse_telephony_websocket(websocket)

    # Start bot with parsed data
    await run_telephony_bot(websocket, transport_type, call_data)
```