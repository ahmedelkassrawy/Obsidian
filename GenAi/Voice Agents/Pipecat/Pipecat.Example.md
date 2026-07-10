```python
import os
from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.services.google import GoogleLLMService
from pipecat.runner.run import main

load_dotenv(override=True)

os.environ["GOOGLE_API_KEY"] = "AIzaSyCtrxoL_PmeHsS1YzzWYbhxVUsqiufPFL8"
os.environ["CARTESIA_API_KEY"] = "sk_car_UGfrVJ3jnoguu66PmCQz2p"
os.environ["DEEPGRAM_API_KEY"] = "441fda4be7980b278400b4afefb5553d74e90f25"
os.environ["DAILY_API_KEY"] = "ed95e39a64e083d2c210c95d1d2f35e3e153fe2052d9e1b0fa14928755fb85f7"

print("Starting Pipecat bot...")

async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    logger.info(f"Starting bot")

    stt = DeepgramSTTService(api_key = os.getenv("DEEPGRAM_API_KEY"))
    tts = CartesiaTTSService(api_key = os.getenv("CARTESIA_API_KEY"),
                             voice_id = "71a7ad14-091c-4e8e-a314-022ece01c121")
    
    llm = GoogleLLMService(api_key=os.getenv("GOOGLE_API_KEY"),
                        model="gemini-2.5-flash",
                        kwargs = {
                                    "max_tokens": 500,
                                }   
                            )

    messages = [
        {
            "role":"system",
            "content": "You are friendly AI Asisstant. Respond naturally and keep your answers conversational."
        }
    ]

    context = LLMContext(messages)
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params = LLMUserAggregatorParams(vad_analyzer = SileroVADAnalyzer()),
    )
 
    pipeline = Pipeline(
        [
            transport.input(),  # Transport user input
            stt,
            user_aggregator,  # User responses
            llm,  # LLM
            tts,  # TTS
            transport.output(),  # Transport bot output
            assistant_aggregator,  # Assistant spoken responses
        ]
    )

    task = PipelineTask(
        pipeline,
        params = PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info(f"Client connected")
        messages.append(
            {
                "role": "system", 
                "content": "Say hello and briefly introduce yourself."
            }
        )
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info(f"Client disconnected")
        await task.cancel()

    runner = PipelineRunner(handle_sigint = runner_args.handle_sigint)
    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    """Main bot entry point"""
    transport_params = {
        "webrtc": lambda: TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
        ),
    }

    transport = await create_transport(runner_args, transport_params)
    await run_bot(transport, runner_args)

if __name__ == "__main__":
    main()
```
---
#### To Add a wakeup filter
```python
hey_robot_filter = WakeCheckFilter(
        [
            "hey robot",
            "ok robot"
        ]
    )

    context = LLMContext(messages)
    user_aggregator,assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params = LLMUserAggregatorParams(vad_analyzer = vad),
    )

    task = PipelineTask(
        Pipeline(
            [
                transport.input(),  # Transport user input
                stt,  # STT
                hey_robot_filter,  # Filter out speech not directed at the robot
                user_aggregator,  # User responses
                llm,  # LLM
                tts,  # TTS
                transport.output(),  # Transport bot output
                assistant_aggregator,  # Assistant spoken responses
            ]
        ),
        idle_timeout_secs = runner_args.pipeline_idle_timeout_secs,
        params = PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport,client):
        await task.queue_frames(
            [
                TTSSpeakFrame("Hi! If you want to talk to me, just say 'Hey Robot'"),
            ]
        )
```
---
#### Adding IdleTimeout
```python
context = LLMContext(messages)
    user_aggregator,assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params = LLMUserAggregatorParams(vad_analyzer = vad,user_idle_timeout=0),
    )

    task = PipelineTask(
        Pipeline(
            [
                transport.input(),  # Transport user input
                stt,  # STT
                user_aggregator,  # User responses
                llm,  # LLM
                tts,  # TTS
                transport.output(),  # Transport bot output
                assistant_aggregator,  # Assistant spoken responses
            ]
        ),
        idle_timeout_secs = runner_args.pipeline_idle_timeout_secs,
        cancel_on_idle_timeout=True,
        idle_timeout_frames=(BotSpeakingFrame),
        params = PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
    )
```
---
Function Calling
```python
from pipecat.adapters.schemas.function_schema import FunctionSchema
from pipecat.services.llm_service import FunctionCallParams
from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.services.llm_service import FunctionCallParams

async def get_weather(params: FunctionCallParams,location:str):
    weather_data = {
        "conditions": "sunny",
        "temperature": "25C",
    }
    await params.result_callback(weather_data)
    
async def run_bot(transport: BaseTransport,
                  runner_args: RunnerArguments):
    ...
    tools = ToolsSchema(standard_tools = [get_weather])
    llm.register_direct_function(
        get_weather,
        cancel_on_interruption=False,)
        
	context = LLMContext(messages,tools = tools)
```
---
RAG
```python
print("Starting Pipecat bot...")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

async def query_knowledge_base(params: FunctionCallParams,query:str):
    FULL_PROMPT = f"""You are a helpful assistant with access to a knowledge base. The user will ask you questions, and you will query the knowledge base to find the answer. The knowledge base is accessed through the `query'"""
    
    response = client.models.generate_content(
        model="gemini-3-flash",
        contents = [
            {
                "role": "user",
                "parts": [
                    {
                        "text": FULL_PROMPT + query
                    }
                ]
            }
        ]
    )
    await params.result_callback(response.text)

```