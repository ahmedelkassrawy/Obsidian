Learn about the different ways users can connect to your Pipecat voice AI bot

- **Transports** are the communication layer between users and your Pipecat bot. 
- They handle receiving and sending audio, video, and data, serving as the media interface that enables real-time interaction.

Pipeline Integration:
provide two key components for your pipeline: input( ) and output( ) methods

```python
pipeline = Pipeline([
    transport.input(),              # Receives user audio/video
    stt,
    context_aggregator.user(),
    llm,
    tts,
    transport.output(),             # Sends bot audio/video
    context_aggregator.assistant(), # Processes after output
])
```

**Key points about transport placement:**
- **`transport.input()`** typically goes first in the pipeline to receive user input
- **`transport.output()`** doesn’t always go last - you may want processors after it
- **Post-output processing** enables synchronized actions like:
    - Recording with word-level accuracy
    - Displaying subtitles synchronized to audio
    - Capturing context information precisely timed to output

Transport Configurations
```python
from pipecat.transports.base_transport import TransportParams

params = TransportParams(
    # Audio settings
    audio_in_enabled=True,
    audio_out_enabled=True,

    # Video settings
    video_in_enabled=False,
    video_out_enabled=False,

    # Video stream configuration
    video_out_width=1024,
    video_out_height=576,
    video_out_bitrate=800000,
    video_out_framerate=30,
)
```

Telephony integration 

## Key Takeaways
- **Transports are modular** - swap them without changing bot logic
- **Choose based on use case** - WebRTC for clients, WebSocket for telephony
- **Configuration is standardized** - TransportParams work across transport types
- **Pipeline placement matters** - consider what processing happens after output
- **Development runner helps** - provides patterns for multi-transport bots