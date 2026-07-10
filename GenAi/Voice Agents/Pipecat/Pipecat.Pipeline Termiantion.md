Learn how to properly terminate Pipecat pipelines for clean shutdown and resource management

- **Pipeline termination** ensures your voice AI applications shut down cleanly without resource leaks or hanging processes. 
- Understanding the different termination methods helps you handle various scenarios from natural conversation endings to unexpected disconnections.

```python
pipeline = Pipeline([
    transport.input(),
    stt,
    context_aggregator.user(),
    llm,
    tts,
    transport.output(),
    context_aggregator.assistant(),
])
# EndFrame or CancelFrame flows through entire pipeline for shutdown
```

**Termination frames:**
- **`EndFrame`**: A queued ControlFrame that triggers graceful shutdown after processing pending frames
- **`CancelFrame`**: A SystemFrame that triggers immediate shutdown, discarding pending frames

Both frames flow downstream through the pipeline, allowing each processor to clean up resources appropriately.
###  1. Graceful Termination
Graceful termination allows the bot to complete its current processing before shutting down. This is ideal when you want the bot to properly end a conversation. For example, after completing a specific task or reaching a natural conclusion.**When to use:**

- Natural conversation endings
- Task completion scenarios
- When the bot should say goodbye

**Implementation options:**Push an `EndFrame` from outside your pipeline:

```python
# From outside the pipeline
from pipecat.frames.frames import EndFrame, TTSSpeakFrame

await task.queue_frame(EndFrame())
```

Push an `EndTaskFrame` upstream from inside your pipeline:

```python
# From inside a function call
from pipecat.frames.frames import EndTaskFrame, TTSSpeakFrame
from pipecat.processors.frame_processor import FrameDirection

async def end_conversation(params: FunctionCallParams):
    await params.llm.push_frame(TTSSpeakFrame("Have a nice day!"))

    # Signal that the task should end after processing this frame
    await params.llm.push_frame(EndTaskFrame(), FrameDirection.UPSTREAM)
```

**How graceful termination works:**
1. `EndFrame` is queued and processes after any pending frames (like goodbye messages)
2. All processors shutdown when they receive the `EndFrame`
3. Once the `EndFrame` reaches the end of the pipeline, shutdown is complete
4. Resources are cleaned up and the process terminates

Graceful termination allows your bot to say goodbye and complete any final actions before terminating.

### 2. Immediate Termination
Immediate termination cancels the pipeline without waiting for pending frames to complete. This is appropriate when the user is no longer active in the conversation.**When to use:**

- User disconnections (browser closed, call ended)
- Error conditions requiring immediate shutdown
- When completing the conversation is no longer necessary

**Implementation:**Use event handlers to detect disconnections and trigger cancellation:

```python
@transport.event_handler("on_client_disconnected")
async def on_client_disconnected(transport, client):
    logger.info("Client disconnected - terminating pipeline")
    await task.cancel()
```

**How immediate termination works:**
1. An event triggers the cancellation (like client disconnection)
2. `task.cancel()` pushes a `CancelFrame` downstream from the PipelineTask
3. `CancelFrame`s are `SystemFrame`s and bypass queues for immediate processing
4. Processors handle the `CancelFrame` and shut down immediately
5. Any pending frames are discarded during shutdown

>[!warning]
Immediate termination will discard any pending frames in the pipeline. Use this approach when completing the conversation is no longer necessary.

## Automatic Termination
Pipeline Idle Detection

Pipecat includes automatic idle detection to prevent hanging pipelines. This feature monitors activity and can automatically cancel tasks when no meaningful bot interactions occur for an extended period.

**How it works:**
- Monitors pipeline activity for meaningful bot interactions
- Automatically triggers termination after configured idle timeout
- Serves as a safety net for anomalous behavior or forgotten sessions

**Configuration:**
```python
task = PipelineTask(
    pipeline,
    # Configure idle detection timeout
    cancel_on_idle_timeout=True, # Default is True
    idle_timeout_seconds=600,  # Default is 300 seconds
    idle_timeout_frames=(BotSpeakingFrame,), # Default is (BotSpeakingFrame, LLMFullResponseEndFrame)
)
```

>[!tip]
>Pipeline Idle Detection is enabled by default and helps prevent resources from being wasted on inactive conversations.

## Implementation Patterns
Event-Driven Termination
Connect termination to transport events for automatic cleanup:

```python
@transport.event_handler("on_client_connected")
async def on_client_connected(transport, client):
    logger.info("Client connected - starting conversation")
    await task.queue_frames([LLMRunFrame()])

@transport.event_handler("on_client_disconnected")
async def on_client_disconnected(transport, client):
    logger.info("Client disconnected - immediate termination")
    await task.cancel()

# Run the pipeline
runner = PipelineRunner(handle_sigint=False)
await runner.run(task)
```

### Conditional Termination
Use function calling or other logic to determine when conversations should end:

```python
async def check_conversation_complete(params: FunctionCallParams):
    # Your logic to determine if conversation should end
    conversation_complete = await evaluate_completion_criteria()

    if conversation_complete:
        await params.llm.push_frame(TTSSpeakFrame("Thank you for using our service!"))
        await params.llm.push_frame(EndTaskFrame(), FrameDirection.UPSTREAM)

    await params.result_callback({"status": "complete" if conversation_complete else "continuing"})
```

### Error Handling
Ensure pipelines can terminate properly even when exceptions occur:

```python
try:
    runner = PipelineRunner(handle_sigint=False)
    await runner.run(task)
except Exception as e:
    logger.error(f"Pipeline error: {e}")
    # Ensure cleanup happens even on errors
    await task.cancel()
```

## Troubleshooting
If your pipeline isn’t shutting down properly, check these common issues:
### Custom Processors Not Propagating Frames
**Problem:** Custom processors that don’t call `push_frame()` can block termination frames from reaching the end of the pipeline.

**Solution:** Ensure your custom processors propagate all frames downstream, including `EndFrame` and `CancelFrame`:

```python
async def process_frame(self, frame: Frame, direction: FrameDirection):
    await super().process_frame(frame, direction)

    # Your custom processing logic here

    # Always push frames downstream (including termination frames)
    await self.push_frame(frame, direction)
```

### Incorrect Termination Frame Direction
**Problem:** Pushing `EndFrame` or `CancelFrame` from the middle of the pipeline may not reach the pipeline source properly.
**Solution:** Use the appropriate frame type and direction:

```python
# From inside the pipeline, push upstream to reach the source
await self.push_frame(EndTaskFrame(), FrameDirection.UPSTREAM)
await self.push_frame(CancelTaskFrame(), FrameDirection.UPSTREAM)

# The pipeline source will then convert these to proper termination frames
# and push them downstream through the entire pipeline
```

The pipeline source automatically converts `EndTaskFrame` to `EndFrame` and `CancelTaskFrame` to `CancelFrame` when pushing downstream, ensuring proper termination handling throughout the pipeline.
## Key Takeaways
- **Frame-based termination** - shutdown uses the same frame system as processing
- **Choose the right method** - graceful for natural endings, immediate for disconnections
- **Event handlers enable automatic termination** - respond to user disconnections cleanly
- **Idle detection provides safety net** - prevents hanging processes and resource waste
- **SystemFrames bypass queues** - CancelFrames process immediately for fast shutdown
- **Resource cleanup is automatic** - proper termination ensures clean resource disposal