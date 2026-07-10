#### Observability
```python
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)  # <---- 1. Import the Plugin
from google.genai import types
import asyncio

runner = InMemoryRunner(
    agent=research_agent_with_plugin,
    plugins=[
        LoggingPlugin()
    ],  # <---- 2. Add the plugin. Handles standard Observability logging across ALL agents
)

response = await runner.run_debug("Find recent papers on quantum computing")
```

1. **Development debugging?** → Use `adk web --log_level DEBUG`
2. **Common production observability?** → Use `LoggingPlugin()`
3. **Custom requirements?** → Build Custom Callbacks and Plugins

#### Eval
Agents are different from traditional software:
- They are non-deterministic
- Users give unpredictable, ambiguous commands
- Small prompt changes cause dramatic behavior shifts and different tool calls

To accommodate all these differences, agents need systematic evaluation, not just "happy path" testing. **Which means assessing the agent's entire decision-making process - including the final response and the path it took to get the response (trajectory)!**