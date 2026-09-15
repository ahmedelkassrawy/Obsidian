---
description: "Hub: every note about Voice Agents"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/voice-agents
---
# Voice Agents

> [!info] The STT-LLM-TTS sandwich, latency, LiveKit and a LangChain voice agent. Missing: anything you shipped.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/voice-agents`.

## Concepts
- [[Pipecat]] — Why real-time voice is hard and what Pipecat gives you: low latency, a modular pipeline, and the transport options (P2P WebRTC, Daily rooms, telephony).
- [[Pipecat.Pipeline & Frame Processing]] — How Pipecat's pipeline moves data: system frames processed immediately vs data and control frames that queue in order, chaining processors, and running the pipeline.
- [[Pipecat.Speech Input & Turn Detection]] — How Pipecat decides the user has finished speaking: VAD parameters, smart turn detection, handling interruptions, and the performance cost of each setting.
- [[Voice Agent]] — The vocabulary and the core problem of voice agents: VAD, end-of-turn detection, the STT-LLM-TTS chain, and how latency is fought with infrastructure and optimization.
- [[Pipecat.Transports]] `stub` — Short note on Pipecat transports as the media layer between users and the bot, carrying audio, video and data.

## How-tos & recipes
- [[Langchain Voice Agent]] — Building a voice agent as an STT-agent-TTS sandwich: synchronizing the async pieces, reading the stream, routing parsed output, error handling, and the WebSocket endpoint.
- [[Livekit]] — LiveKit agents end to end: the component table, server pre-warming, the connection entrypoint, assembling the AgentSession pipeline, usage metrics and starting the session.
- [[Pipecat Pipeline Termination]] — How to shut a Pipecat pipeline down cleanly: graceful termination with EndFrame vs immediate with CancelFrame, from inside or outside the pipeline, plus troubleshooting.
- [[Pipecat.Context Management]] — What context means in Pipecat, how it updates during a conversation, and how to set up the context aggregator with initial messages and a tools schema.
- [[Pipecat.Function Calling]] — Function calling in a Pipecat voice pipeline: defining functions with the standard schema or as direct functions, building the tools schema, and registering the handler.
- [[Pipecat.LLM Inference]] — How the LLM service sits in a Pipecat pipeline: where to place it, the base class config, and how it streams tokens out as LLMTextFrames.
- [[Pipecat.Speech to text]] — Configuring speech-to-text in Pipecat: LiveOptions for full control, wiring STT into the context aggregator, and tuning transcription latency.
- [[Pipecat.TTS]] — Text-to-speech in Pipecat: the frame flow into the TTS service, pipeline-level audio config, and using a pattern aggregator so the bot never reads JSON out loud.
- [[Pipecat.Example]] `raw` — A complete pasted Pipecat bot script: imports, Silero VAD, the pipeline, and the runner.

## Related hubs
[[Pipecat]], [[LangChain]], [[Context Engineering]], [[Tool Use & Function Calling]]

## Notes to self (from the audit)
- [[Pipecat Pipeline Termination]]: Old filename misspelled 'Termination'.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
