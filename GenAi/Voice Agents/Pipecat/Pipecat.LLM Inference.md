Learn how to configure language models to generate intelligent responses in your voice AI pipeline
- **LLM services** are responsible for chat completions and tool calling based on the provided context (conversation history). 
- The LLM responds by streaming tokens via `LLMTextFrame`s, which are used by subsequent processors to create audio output for the bot.

## Pipeline Placement
The LLM instance should be placed after the user context aggregator and before any downstream services that depend on the LLM’s output stream:

**Frame flow:**
- **Input**: Receives `LLMContextFrame` containing conversation history
- **Processing**:
    - Analyzes context and generates streaming response
    - Handles function calls if tools are available
    - Tracks token usage for metrics
- **Output**:
    - Denotes the start of the streaming response by pushing an `LLMFullResponseStartFrame`
    - Streams `LLMTextFrame`s containing response tokens to downstream processors (enables real-time TTS processing)
    - Ends with an `LLMFullResponseEndFrame` to mark the completion of the response
    - Output frames can be configured to [skip TTS](https://docs.pipecat.ai/guides/learn/text-to-speech#skipping-tts-output) via `LLMConfigureOutputFrame(skip_tts=True)`, allowing text to flow through the pipeline without being spoken
- **Function calls:**
    - `FunctionCallsStartedFrame`: Indicates function execution beginning
    - `FunctionCallInProgressFrame`: Indicates a function is currently executing
    - `FunctionCallResultFrame`: Contains results from executed functions

### Base Class Config
All LLM services inherit from the `LLMService` base class with shared configuration options:
```python
llm = YourLLMService(
    # Service-specific options...
    run_in_parallel=True,  # Whether function calls run in parallel (default: True)
)
```

**Key options:**
- **`run_in_parallel`**: Controls whether function calls execute simultaneously or sequentially
    - `True` (default): Faster execution when multiple functions are called
    - `False`: Sequential execution for dependent function calls

#### Event Handlers
LLM services provide event handlers for monitoring completion lifecycle:
```python
@llm.event_handler("on_completion_timeout")
async def on_completion_timeout(service):
    logger.warning("LLM completion timed out")
    # Handle timeout (retry, fallback, etc.)

@llm.event_handler("on_function_calls_started")
async def on_function_calls_started(service, function_calls):
    logger.info(f"Starting {len(function_calls)} function calls")
    # Optionally notify user that bot is "thinking"
    await tts.queue_frame(TTSSpeakFrame("Let me check on that."))
```

**Available events:**
- **`on_completion_timeout`**: Triggered when LLM requests timeout
- **`on_function_calls_started`**: Triggered when function calls are initiated

These handlers enable you to provide user feedback and implement error recovery strategies.
## Key Takeaways
- **Pipeline placement matters** - LLM goes after user context, before TTS
- **Token streaming enables real-time responses** - no waiting for complete generation
- **OpenAI compatibility** enables easy provider switching
- **Function calling extends capabilities** beyond training data
- **Configuration affects behavior** - tune temperature, penalties, and limits
- **Services are modular** - swap providers without changing pipeline code
