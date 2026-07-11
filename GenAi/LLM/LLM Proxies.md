Link: [LLM-Proxy-Course.ipynb - Colab](https://colab.research.google.com/drive/169AKoMXcT460hiqmtrP4Y_sxWVOLnlQ3?usp=sharing#scrollTo=GiaAQkVggT3B)
# LLM Proxy Course

This document outlines the setup and usage of a proxy server for Large Language Models (LLMs) using LiteLLM, including logging, load balancing, fallbacks, and observation with Langfuse. It also integrates with LangChain for processing web documents.

## Concept Definitions

- **Observation**: Monitoring and tracking the performance and behavior of LLM requests, typically using tools like Langfuse to log successes, failures, and other metrics for analysis and debugging.
    
- **Fallbacks**: A mechanism to redirect LLM requests to an alternative model or provider if the primary model fails or is unavailable, ensuring system reliability and continuity.
    
- **Load Balancer**: A system that distributes incoming LLM requests across multiple models or providers based on a defined strategy (e.g., simple shuffle or least busy) to optimize performance and resource utilization.
    

## Setup

### Install Dependencies

Install the required packages for LiteLLM and Langfuse.

```bash
pip install 'litellm==1.44.9' 'litellm[proxy]==1.44.9' openai==1.42.0 langfuse==2.52.2
pip install -qU langchain-openai langchain langchain_community
```

### Environment Variables

Set up environment variables for API keys. Ensure you have the necessary API keys stored securely.

```python
import os
from google.colab import userdata

os.environ["OPENAI_API_KEY"] = userdata.get('openai-colab')
os.environ["COHERE_API_KEY"] = userdata.get('cohere')
os.environ["GROQ_API_KEY"] = userdata.get('GROQ_API_KEY')

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-27f7fa53-b370-46d2-82f0-6f32851dfc92"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-c3571355-5d0c-48bb-ac92-c3dfaecea1c2"
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"
```

## Basic Completion

Use LiteLLM to send a completion request to a model.

```python
from litellm import completion
from pprint import pprint

messages = [
    {"role": "user", "content": "لماذا تبدو السماء زرقاء بالنهار؟"}
]

response = completion(
    model="cohere/command-r-plus-08-2024",
    messages=messages,
    temperature=0.5,
    max_tokens=200
)

pprint(response.choices[0].message.content)
```

## SDK Logging

Log successful and failed LLM requests to JSONL files for debugging and analysis.

```python
import litellm
import os
import json

logs_dir = "./llm-logs"
os.makedirs(logs_dir, exist_ok=True)

def log_success(kwargs, completion_obj, start_time, end_time):
    with open(f"{logs_dir}/success-logs.jsonl", "a") as dest:
        dest.write(
            json.dumps({
                "kwargs": kwargs,
                "completion_obj": completion_obj,
                "start_time": start_time,
                "end_time": end_time,
            }, ensure_ascii=False, default=str) + "\n"
        )

def log_failure(kwargs, completion_obj, start_time, end_time):
    with open(f"{logs_dir}/failure-logs.jsonl", "a") as dest:
        dest.write(
            json.dumps({
                "kwargs": kwargs,
                "completion_obj": completion_obj,
                "start_time": start_time,
                "end_time": end_time,
            }, ensure_ascii=False, default=str) + "\n"
        )

litellm.success_callback = [log_success]
litellm.failure_callback = [log_failure]

response = completion(
    model="openai/gpt-4o-mini",
    messages=messages,
    temperature=0.5,
    max_tokens=200
)
```

## Proxy Server

Configure a LiteLLM proxy server to route requests to different models.

### Configuration File (llm.yaml)

```yaml
model_list:
  - model_name: "groq-gemma9b"
    litellm_params:
      model: "groq/gemma2-9b-it"
      api_key: "os.environ/GROQ_API_KEY"
  - model_name: "groq-mixtral"
    litellm_params:
      model: "groq/mixtral-8x7b-32768"
      api_key: "os.environ/GROQ_API_KEY"
  - model_name: "openai-gpt4o-mini"
    litellm_params:
      model: "openai/gpt-4o-mini"
      api_key: "os.environ/OPENAI_API_KEY"
```

### Start Proxy Server

```bash
nohup litellm --port 4000 --config llm.yaml &
sleep 10 && tail nohup.out
```

### Send Request via OpenAI Client

```python
import openai
from pprint import pprint

client = openai.OpenAI(
    api_key="any key",
    base_url="http://0.0.0.0:4000"
)

messages = [
    {"role": "user", "content": "لماذا تبدو السماء زرقاء بالنهار؟"}
]

response = client.chat.completions.create(
    model="groq-mixtral",
    messages=messages,
)

pprint(response.choices[0].message.content)
```

## Load Balancer

Distribute requests across multiple models using a load balancer.

### Configuration File (llm-lb.yaml)

```yaml
model_list:
  - model_name: "global-llm"
    litellm_params:
      model: "groq/gemma2-9b-it"
      api_key: "os.environ/GROQ_API_KEY"
      rpm: 20
  - model_name: "global-llm"
    litellm_params:
      model: "groq/mixtral-8x7b-32768"
      api_key: "os.environ/GROQ_API_KEY"
      rpm: 20
  - model_name: "global-llm"
    litellm_params:
      model: "openai/gpt-4o-mini"
      api_key: "os.environ/OPENAI_API_KEY"
      rpm: 10
routing_strategy: simple-shuffle
```

### Start Load Balancer

```bash
nohup litellm --port 4000 --config llm-lb.yaml &
sleep 10 && tail nohup.out
```

### Send Request via OpenAI Client

```python
client = openai.OpenAI(
    api_key="any key",
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="global-llm",
    messages=messages,
)

pprint(response.choices[0].message.content)
```

## Fallbacks

Configure fallbacks to switch to alternative models if the primary model fails.

### Configuration File (llm-fallback.yaml)

```yaml
router_settings:
  enable_pre_call_checks: true
model_list:
  - model_name: "groq-gemma9b"
    litellm_params:
      model: "groq/gemma2-9b-it"
      api_key: "os.environ/GROQ_API_KEY"
  - model_name: "groq-mixtral"
    litellm_params:
      model: "groq/mixtral-8x7b-32768"
      api_key: "os.environ/GROQ_API_KEY"
  - model_name: "openai-gpt4o-mini"
    litellm_params:
      model: "openai/gpt-4o-mini"
      api_key: "os.environ/OPENAI_API_KEY"
      rpm: 20
litellm_settings:
  num_retries: 3
  fallbacks: [{"openai-gpt4o-mini": "groq-mixtral"}]
  request_timeout: 10
  allowed_fails: 3
  cooldown_time: 30
```

### Start Fallback Server

```bash
nohup litellm --port 4000 --config llm-fallback.yaml &
sleep 10 && tail nohup.out
```

## Observation with Langfuse

Integrate Langfuse for observability of LLM requests.

### Configuration File (llm-langfuse.yaml)

```yaml
model_list:
  - model_name: "groq-gemma9b"
    litellm_params:
      model: "groq/gemma2-9b-it"
      api_key: "os.environ/GROQ_API_KEY"
  - model_name: "groq-mixtral"
    litellm_params:
      model: "groq/mixtral-8x7b-32768"
      api_key: "os.environ/GROQ_API_KEY"
  - model_name: "openai-gpt4o-mini"
    litellm_params:
      model: "openai/gpt-4o-mini"
      api_key: "os.environ/OPENAI_API_KEY"
litellm_settings:
  drop_params: True
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]
  redact_user_api_key_info: true
```

### Start Observation Server

```bash
nohup litellm --port 4000 --config llm-langfuse.yaml &
sleep 10 && tail nohup.out
```

### Send Request with Observation

```python
client = openai.OpenAI(
    api_key="any key",
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="openai-gpt4o-mini",
    messages=messages,
)

pprint(response.choices[0].message.content)
```

## LiteLLM + LangChain

Use LangChain to process web documents and generate summaries with LiteLLM.

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

loader = WebBaseLoader([
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-02-05-human-data-quality/",
])
docs = loader.load()

llm = ChatOpenAI(
    openai_api_base="http://0.0.0.0:4000",
    model="openai-gpt4o-mini",
    temperature=0.1
)

map_prompt = ChatPromptTemplate.from_messages(
    [("system", "Write a concise summary of the following:\\n\\n{context}")]
)

map_chain = map_prompt | llm | StrOutputParser()

result = map_chain.invoke({"context": docs})
print(result)
```