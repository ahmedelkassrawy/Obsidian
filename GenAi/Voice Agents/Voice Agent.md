- Voice Activity Detection (VAD) -> detecting presence/abscence of human speech
- End of Turn / Utternace Detection (EOU) -> detecting whether a speaker has finished their speech or not
- STT
- LLM
- TTS

## The Latency Challenge
Timing is the biggest hurdle in voice applications. If the system lags, the interaction quickly feels unnatural.

| **Metric**                                 | **Latency / Time**               |
| ------------------------------------------ | -------------------------------- |
| **Human Expectation (Average)**            | 236 milliseconds                 |
| **Human Expectation (Standard Deviation)** | ~520 milliseconds                |
| **Pipeline Best-Case Scenario**            | ~540 milliseconds                |
| **Pipeline Worst-Case Scenario**           | 1.5+ seconds (highly noticeable) |

_Note: Expectations vary heavily depending on the language spoken._
### Mitigating Latency with Infrastructure

To approach the lower bounds of latency, developers use real-time **peer-to-peer (P2P) communication**, bypassing traditional intermediary servers.

This is typically achieved using:
- **WebRTC:** An open-source project providing standardized APIs for real-time web/mobile communication.
    
- **WebSockets:** Used to establish the initial client-server handshake and session management.
    
- **LiveKit:** A globally distributed mesh network that abstracts the complex P2P infrastructure, managing input/output streams and streaming APIs asynchronously.
---
## Implementation & Optimization
### Building the Backend
Using platforms like LiveKit, setting up the backend requires focusing on three main code components:
1. **The Agent:** Defining the agent's core instructions and prompts.
    
2. **The Session:** Linking your chosen STT, LLM, and TTS providers into a functional pipeline.
    
3. **The Entrypoint Function:** The main function executed for each new peer-to-peer connection.
### Practical Challenges & Optimizations
- **Speech Disfluencies:** Filler words ("um") or long pauses can confuse the transcription and end-of-turn detection, reducing the LLM's output quality. VAD helps handle interruptions cleanly.
    
- **Multilingual Limitations:** Multilingual ASR models generally underperform compared to their English-only counterparts.
    
- **Optimizing the LLM:** The LLM is usually the main bottleneck. To speed it up, use smaller/quantized models, utilize fast inference APIs, and prompt the LLM to provide shorter or staged replies.
---
