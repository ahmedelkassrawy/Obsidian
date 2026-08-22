Learn how to configure speech recognition to convert user audio into text in your Pipecat pipeline

**Speech to Text (STT)** services are responsible for converting user audio into text transcriptions. 
- They receive audio input from users and provide real-time transcriptions that your bot can process and respond to.

Pipeline Placement
STT processors must be positioned correctly in your pipeline to receive and process audio frames:
```python
pipeline = Pipeline([
    transport.input(),             # Creates InputAudioRawFrames
    stt,                           # Processes audio → creates TranscriptionFrames
    context_aggregator.user(),     # Uses transcriptions for context
    llm,
    tts,
    transport.output(),
])
```

**Placement requirements:**
- **After `transport.input()`**: STT needs `InputAudioRawFrame`s from the transport
- **Before context processing**: Transcriptions must be available for context aggregation
- **Before LLM processing**: Text must be ready for language model input

STT Service Types:
how they process audio:
1. STTService (Streaming)
	How it works
		- Establishes a WebSocket connection to the STT provider
		- Continuously streams audio for real-time transcription
		- Lower latency due to persistent connection
2. SegmentedSTTService (HTTP-based)
	How it works
		- Uses local VAD (Voice Activity Detection) to chunk speech
		- Sends audio segments to STT service as wav files
		- Higher latency due to segmentation and HTTP POST requests

STT Configuration
For example, let’s look at configuring the **DeepgramSTTService** using the `LiveOptions` class:
```python
from deepgram import LiveOptions
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.transcriptions.language import Language

# Configure using LiveOptions for full control
live_options = LiveOptions(
    model="nova-2",
    language=Language.EN_US,
    interim_results=True,        # Enable interim transcripts
    punctuate=True,              # Add punctuation
    profanity_filter=True,       # Filter profanity
    vad_events=False,            # Use pipeline VAD instead
)

stt = DeepgramSTTService(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    live_options=live_options,
)
```

STTService Base Class Configuration
All STT services inherit from the STTService base class. The base class has base configuration options which are set with smart defaults:
```python
stt = YourSTTService(
    # Service-specific options...
    audio_passthrough=True,      # Pass audio frames downstream (recommended)
    sample_rate=16000,           # Audio sample rate (better set in PipelineParams)
)
```
- **`audio_passthrough=True`**: Allows audio frames to continue downstream to other processors (like audio recording)
- **`sample_rate`**: Audio sampling rate - best practice is to **set the `audio_in_sample_rate` in `PipelineParams` for consistency**

Pipeline-Level Audio Configuration
Instead of setting sample rates on individual services, configure them pipeline-wide:
```python
task = PipelineTask(
    pipeline,
    params=PipelineParams(
        audio_in_sample_rate=16000,   # All input processors use this rate
        audio_out_sample_rate=24000,  # All output processors use this rate
    ),
)
```

This ensures all audio processors use consistent sample rates without manual configuration.

>[!tip]
>This ensures all audio processors use consistent sample rates without manual configuration.

Best Practices

- Enable Interim Results
When available, enable interim transcripts for better user experience:
```python
stt = DeepgramSTTService(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    live_options=LiveOptions(
      interim_results=True,
    )
)
```

**Benefits:**
- Notifies context aggregation that more text is coming
- Prevents premature LLM completions
- Enables interruption detection
- Improves conversation flow

- Enable Punctuation and Formatting
Use punctuation when available for better LLM comprehension:
```python
stt = DeepgramSTTService(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    live_options=LiveOptions(
        punctuate=True,        # Adds punctuation
        profanity_filter=True, # Optional content filtering
    )
)
```

**Benefits:**
- Professional-looking transcripts
- Better LLM comprehension
- Eliminates post-processing needs
- Improved context understanding

- Use Local VAD
While many STT services provide Voice Activity Detection, use Pipecat’s local Silero VAD for better performance:
```python
from pipecat.audio.vad.silero import SileroVADAnalyzer

# Configure in context aggregator
user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
    context,
    user_params=LLMUserAggregatorParams(
        vad_analyzer=SileroVADAnalyzer(),
    ),
)
```

**Advantages:**
- **150-200ms faster** speech detection (no network round trip)
- More responsive conversation flow
- Better interruption handling
- Reduced latency overall

### Tune STT Latency
- Each STT service has a measured P99 latency for delivering final transcripts after the user stops speaking. 
- This value is used by turn stop strategies to decide how long to wait before ending the user’s turn. 
- If you notice the bot responding too early (cutting off the user) or too late (long pauses), tuning this value can help.

Key Takeaways
- **Pipeline placement matters** - STT must come after transport input, before context processing
- **Service types differ** - streaming services have lower latency than segmented
- **Services are modular** - easily swap providers without code changes
- **Best practices improve performance** - use interim results, formatting, and local VAD
- **Configuration affects quality** - proper setup significantly impacts transcription accuracy