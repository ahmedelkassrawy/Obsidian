|Component|Description|Use cases|
|---|---|---|
|**Agent sessions**|Orchestrate input collection, pipeline management, and output delivery. The main orchestrator for your voice AI app.|Single-agent apps, session lifecycle management, and room I/O configuration.|
|**Tasks & task groups**|Create focused, reusable units that perform specific objectives and return typed results. Tasks run inside agents and take temporary control until completion.|Consent collection, structured data capture, and multi-step processes with task groups.|
|**Workflows**|Model repeatable patterns with agents, handoffs, and tasks for complex voice AI systems.|Multi-persona systems, conversation phase management, and specialized agent routing.|
|**Tool definition & use**|Extend agent capabilities with custom functions callable by the LLM for external actions and data access.|API integrations, frontend RPC calls, and triggering agent handoffs.|
|**Pipeline nodes & hooks**|Customize agent behavior at pipeline processing points with custom STT, LLM, TTS, and lifecycle hooks. Override nodes to modify input, output, or add custom logic.|Custom providers, output modification, and pronunciation control.|
|**Turn detection & interruptions**|Manage conversation flow with turn detection, interruption handling, and manual turn control.|Natural conversation timing, interruption management, and push-to-talk interfaces.|
|**Agents & handoffs**|Define distinct reasoning behaviors and transfer control between agents when different capabilities are needed.|Role-based agents, model specialization, and permission management.|
|**External data & RAG**|Connect agents to external data sources, databases, and APIs for RAG and data operations. Load initial context, perform RAG lookups, and integrate with external services.|Knowledge base search, user profile loading, and database operations.|

---
#### Agent Session
The main orchestrator, The session is responsible for:
- collecting user input
- managing the voice pipeline
- invoking the LLM
- sending the output back to the user
- emits events for observability and control 

Each session requires at least one `Agent` to orchestrate.
```python
from livekit.agents import AgentSession, Agent, inference, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

session = AgentSession(
    stt="assemblyai/universal-streaming:en",
    llm="openai/gpt-4.1-mini",
    tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    vad=silero.VAD.load(),
    turn_detection=MultilingualModel(),
)

await session.start(
    room=ctx.room,
    agent=Agent(instructions="You are a helpful voice AI assistant."),
    room_options=room_io.RoomOptions(
        audio_input=room_io.AudioInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    ),
)
```

Lifecycle:
- Intializing -> session setting up, no audio or video processing occurs yet
- Starting -> session is started using the start( ), I/O connections, agents transition to the listening state
- Running -> The session is actively processing user input and generating agent responses.
	- In this phase, the agent transitions between `listening`, `thinking`, and `speaking` states.
- Closing -> When a session is closed , the cleanup process includes waiting for any queued operations to complete, committing any remaining user transcripts, and closing all I/O connections
	- The session emits a `close` event and resets internal state.

![[Pasted image 20260220010804.png]]

Events
`AgentSession` emits events throughout its lifecycle to provide visibility into the conversation flow.

| **Event**                                                                                            | **Description**                                                                                     |
| ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [`agent_state_changed`](https://docs.livekit.io/reference/other/events/#agent_state_changed)         | Emitted when the agent's state changes (for example, from `listening` to `thinking` or `speaking`). |
| [`user_state_changed`](https://docs.livekit.io/reference/other/events/#user_state_changed)           | Emitted when the user's state changes (for example, from `listening` to `speaking`).                |
| [`user_input_transcribed`](https://docs.livekit.io/reference/other/events/#user_input_transcribed)   | Emitted when user speech is transcribed to text.                                                    |
| [`conversation_item_added`](https://docs.livekit.io/reference/other/events/#conversation_item_added) | Emitted when a message is added to the conversation history.                                        |
| [`close`](https://docs.livekit.io/reference/other/events/#close)                                     | Emitted when the session closes, either gracefully or due to an error.                              |

[[Turn Detection]]
[[tools]]

### User interaction
Configure user state and timing:
- `user_away_timeout`: Time in seconds of silence before setting user state to `away`. Set to `None` to turn off. Default: `15.0` seconds.
    
- `min_consecutive_speech_delay`: Minimum delay in seconds between consecutive agent utterances. Default: `0.0` seconds.
### Text processing
Control how text is processed:
- `tts_text_transforms`: Transforms to apply to TTS input text. Built-in transforms include `"filter_markdown"` and `"filter_emoji"`. Set to `None` to turn off. When not given, all filters are applied by default.
    
- `use_tts_aligned_transcript`: Whether to use TTS-aligned transcript as input for the transcription node. Only applies if the TTS supports aligned transcripts. Default: turned off.

### Performance optimization
Optimize response latency:

[`preemptive_generation`](https://docs.livekit.io/agents/build/audio/#preemptive-generation): Whether to speculatively begin LLM and TTS requests before an end-of-turn is detected. When `True`, the agent sends inference calls as soon as a user transcript is received. This can reduce response latency but can incur extra compute costs if the user interrupts. Default: `False`.

---
```python
import logging
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RunContext,
    cli,
    inference,
    metrics,
    room_io,
)
from livekit.agents.llm import function_tool
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import noise_cancellation
from livekit.plugins import silero
from livekit.plugins import groq
import os

class MyAgent(Agent):
    def __init__(self) -> None:
      super().__init__(
          instructions="Your name is Kelly. You would interact with users via voice."
          "with that in mind keep your responses concise and to the point."
          "do not use emojis, asterisks, markdown, or other special characters in your responses."
          "You are curious and friendly, and have a sense of humor."
          "you will speak english to the user",
      )

    async def on_enter(self):
      #when the agent is added to the session,it will generate a reply according to its instructions
      self.session.generate_reply(allow_interruptions=True)

    @function_tool
    async def lookup_weather(self,context:RunContext,
                            location:str,latitude:str,longitude:str):
      """Called when the user asks for weather related information.
      Ensure the user's location (city or region) is provided.
      When given a location, please estimate the latitude and longitude of the location and
      do not ask the user for them."""
      
      logger.info(f"Looking up for weather for location: {location}")
      return "Sunny with a temperature of 7o degrees"
```

This snippet is the "engine room" of your LiveKit application. It handles how the server starts up, how the AI models are loaded into memory, and exactly what happens the moment a user connects to a voice room.

### 1. Server Setup and "Pre-warming"
```python
server = AgentServer()

def prewarm(proc: JobProcess):
  proc.userdata["vad"] = silero.VAD.load()

server.setup_fnc = prewarm
```

- **The Problem:** Machine learning models (like Voice Activity Detection) take time to load from your hard drive into memory. If you wait to load the model until the user calls, there will be a noticeable, awkward delay.
    
- **The Solution:** The `prewarm` function loads the Silero VAD model into memory (`proc.userdata`) _before_ anyone connects. When a user finally joins, the model is already hot and ready to process audio instantly.

### 2. The Connection Entrypoint
```python
@server.rtc_session()
async def entrypoint(ctx:JobContext):
  ctx.log_context_fields = { "room": ctx.room.name }
```

- The `@server.rtc_session()` decorator tells LiveKit: _"Run this function every time a new room is created."_ * `ctx` (JobContext) holds all the information about that specific call. The code adds the `room.name` to the logs so that if you are debugging later, you can trace exactly which user/room caused an error.
### 3.Assembling the AI Pipeline (`AgentSession`)
This is where you wire up the "brain" and "senses" of the agent for this specific call:
- **`stt`, `llm`, `tts`:** You are plugging in Groq for transcription (Whisper), Groq for the brain (a 20B parameter model), and Cartesia for the voice.
    
- **`vad=ctx.proc.userdata["vad"]`:** Here, you are grabbing that pre-warmed VAD model we set up earlier.
    
- **`preemptive_generation=True`:** This is a massive speed boost. It allows the LLM to start drafting its response while the user is _still finishing their sentence_.
    
- **Interruption Handling:** * `resume_false_interruption=True` and `false_interruption_timeout=1.0` handle a common voice AI issue. If the user coughs or says "uh-huh," the agent might stop speaking, thinking it was interrupted. This logic tells the agent: _"If the user makes a noise but doesn't actually say words, wait 1 second and then resume your sentence."_
```python
session = AgentSession(
      stt = groq.STT(model="whisper-large-v3-turbo"),
      llm = groq.LLM(model="openai/gpt-oss-20b"),
      tts = inference.TTS("cartesia/sonic-3", voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"),
      turn_detection=MultilingualModel(),
      vad=ctx.proc.userdata["vad"],
      preemptive_generation=True,
      resume_false_interruption=True,
      false_interruption_timeout=1.0,
  )
```

### 4. Tracking Usage & Metrics
```python
  usage_collector = metrics.UsageCollector()
  # ... (metrics collection event handler) ...
  ctx.add_shutdown_callback(log_usage)
```
- Because AI models charge by the token or by the second of audio, this section quietly collects usage data in the background.
    
- `ctx.add_shutdown_callback(log_usage)` ensures that the moment the user hangs up (the session shuts down), it prints a total summary of the tokens and audio seconds used during that call.
### 5. Starting the Session
```python
  await session.start(
      agent=MyAgent(),
      room=ctx.room,
      room_options=room_io.RoomOptions(
          audio_input=room_io.AudioInputOptions(
              noise_cancellation=noise_cancellation.BVC(),
          ),
      ),
  )
```

- Finally, `session.start()` brings Kelly to life. It connects your `MyAgent` class to the LiveKit `room`.
    
- It also wraps the incoming audio in a Noise Cancellation filter (`BVC`) to scrub out background noise like typing, dogs barking, or fans before the audio reaches the transcription engine.