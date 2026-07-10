## How it works
LiteLLM can automatically inject prompt caching checkpoints into your requests to LLM providers. This allows:

- **Cost Reduction**: Long, static parts of your prompts can be cached to avoid repeated processing
- **No need to modify your application code**: You can configure the auto-caching behavior in the LiteLLM UI or in the `litellm config.yaml` file.

## Configuration
You need to specify `cache_control_injection_points` in your model configuration. This tells LiteLLM:

1. Where to add the caching directive (`location`)
2. Which message to target (`role`)

LiteLLM will then automatically add a `cache_control` directive to the specified messages in your requests

## LiteLLM Proxy Usage
You can configure cache control injection in the proxy configuration file.
litellm config.yaml
```yaml
model_list:
  - model_name: anthropic-auto-inject-cache-system-message
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20240620
      api_key: os.environ/ANTHROPIC_API_KEY
      cache_control_injection_points:
        - location: message
          role: system
```