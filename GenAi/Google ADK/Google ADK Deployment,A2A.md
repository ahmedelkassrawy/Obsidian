Now we'll use ADK's `to_a2a()` function to make our Product Catalog Agent accessible to other agents.

### What `to_a2a()` does:
- 🔧 Wraps your agent in an A2A-compatible server (FastAPI/Starlette)
- 📋 Auto-generates an **agent card** that includes:
    - Agent name, description, and version
    - Skills (your tools/functions become "skills" in A2A)
    - Protocol version and endpoints
    - Input/output modes
- 🌐 Serves the agent card at `/.well-known/agent-card.json` (standard A2A path)
- ✨ Handles all A2A protocol details (request/response formatting, task endpoints)

This is the **easiest way** to expose an ADK agent via A2A!
**💡 Key Concept: Agent Cards**
An **agent card** is a JSON document that serves as a "business card" for your agent. It describes:

- What the agent does (name, description, version)
- What capabilities it has (skills, tools, functions)
- How to communicate with it (URL, protocol version, endpoints)

Every A2A agent must publish its agent card at the standard path: `/.well-known/agent-card.json`

```python
# Convert the product catalog agent to an A2A-compatible application
# This creates a FastAPI/Starlette app that:
#   1. Serves the agent at the A2A protocol endpoints
#   2. Provides an auto-generated agent card
#   3. Handles A2A communication protocol

product_catalog_a2a_app = to_a2a(
    product_catalog_agent, 
    port=8001  # Port where this agent will be served
)

print("✅ Product Catalog Agent is now A2A-compatible!")
print("   Agent will be served at: http://localhost:8001")
print("   Agent card will be at: http://localhost:8001/.well-known/agent-card.json")
print("   Ready to start the server...")
```

#### Start the Product Catalog Agent Server
We'll start the Product Catalog Agent server in the **background** using `uvicorn`, so it can serve requests from other agents.
#### Why run in background?
- The server needs to keep running while we create and test the Customer Support Agent
- This simulates a real-world scenario where different agents run as separate services
- In production, the vendor would host this on their infrastructure
```python
# First, let's save the product catalog agent to a file that uvicorn can import
product_catalog_agent_code = '''
import os
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

def get_product_info(product_name: str) -> str:
    """Get product information for a given product."""
    product_catalog = {
        "iphone 15 pro": "iPhone 15 Pro, $999, Low Stock (8 units), 128GB, Titanium finish",
        "samsung galaxy s24": "Samsung Galaxy S24, $799, In Stock (31 units), 256GB, Phantom Black",
        "dell xps 15": "Dell XPS 15, $1,299, In Stock (45 units), 15.6\\" display, 16GB RAM, 512GB SSD",
        "macbook pro 14": "MacBook Pro 14\\", $1,999, In Stock (22 units), M3 Pro chip, 18GB RAM, 512GB SSD",
        "sony wh-1000xm5": "Sony WH-1000XM5 Headphones, $399, In Stock (67 units), Noise-canceling, 30hr battery",
        "ipad air": "iPad Air, $599, In Stock (28 units), 10.9\\" display, 64GB",
        "lg ultrawide 34": "LG UltraWide 34\\" Monitor, $499, Out of Stock, Expected: Next week",
    }
    
 product_lower = product_name.lower().strip()
    
    if product_lower in product_catalog:
        return f"Product: {product_catalog[product_lower]}"
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return f"Sorry, I don't have information for {product_name}. Available products: {available}"

product_catalog_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="product_catalog_agent",
    description="External vendor's product catalog agent that provides product information and availability.",
    instruction="""
    You are a product catalog specialist from an external vendor.
    When asked about products, use the get_product_info tool to fetch data from the catalog.
    Provide clear, accurate product information including price, availability, and specs.
    If asked about multiple products, look up each one.
    Be professional and helpful.
    """,
    tools=[get_product_info]
)

# Create the A2A app
app = to_a2a(product_catalog_agent, port=8001)
'''

# Write the product catalog agent to a temporary file
with open("/tmp/product_catalog_server.py", "w") as f:
    f.write(product_catalog_agent_code)

print("📝 Product Catalog agent code saved to /tmp/product_catalog_server.py")

# Start uvicorn server in background
# Note: We redirect output to avoid cluttering the notebook
server_process = subprocess.Popen(
    [
        "uvicorn",
        "product_catalog_server:app",  # Module:app format
        "--host",
        "localhost",
        "--port",
        "8001",
    ],
    cwd="/tmp",  # Run from /tmp where the file is
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env={**os.environ},  # Pass environment variables (including GOOGLE_API_KEY)
)

print("🚀 Starting Product Catalog Agent server...")
print("   Waiting for server to be ready...")

# Wait for server to start (poll until it responds)
max_attempts = 30
for attempt in range(max_attempts):
    try:
        response = requests.get(
            "http://localhost:8001/.well-known/agent-card.json", timeout=1
        )
        if response.status_code == 200:
            print(f"\n✅ Product Catalog Agent server is running!")
            print(f"   Server URL: http://localhost:8001")
            print(f"   Agent card: http://localhost:8001/.well-known/agent-card.json")
            break
    except requests.exceptions.RequestException:
        time.sleep(5)
        print(".", end="", flush=True)
else:
    print("\n⚠️  Server may not be ready yet. Check manually if needed.")

# Store the process so we can stop it later
globals()["product_catalog_server_process"] = server_process
```
#####  View the Auto-Generated Agent Card
The `to_a2a()` function automatically created an **agent card** that describes the Product Catalog Agent's capabilities. Let's take a look!
```python
try:
    response = requests.get(
        "http://localhost:8001/.well-known/agent-card.json", timeout=5
    )

    if response.status_code == 200:
        agent_card = response.json()
        print("📋 Product Catalog Agent Card:")
        print(json.dumps(agent_card, indent=2))

        print("\n✨ Key Information:")
        print(f"   Name: {agent_card.get('name')}")
        print(f"   Description: {agent_card.get('description')}")
        print(f"   URL: {agent_card.get('url')}")
        print(f"   Skills: {len(agent_card.get('skills', []))} capabilities exposed")
    else:
        print(f"❌ Failed to fetch agent card: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching agent card: {e}")
    print("   Make sure the Product Catalog Agent server is running (previous cell)")
```

## Create the Customer Support Agent (Consumer)
Now we'll create a **Customer Support Agent** that consumes the Product Catalog Agent using A2A.
#### How it works:
1. We use `RemoteA2aAgent` to create a **client-side proxy** for the Product Catalog Agent
2. The Customer Support Agent can use the Product Catalog Agent like any other tool
3. ADK handles all the A2A protocol communication behind the scenes
This demonstrates the power of A2A: **agents can collaborate as if they were local!**
**How RemoteA2aAgent works:**
- It's a **client-side proxy** that reads the remote agent's card
- Translates sub-agent calls into A2A protocol requests (HTTP POST to `/tasks`)
- Handles all the protocol details so you just use it like a regular sub-agent

```python
# Create a RemoteA2aAgent that connects to our Product Catalog Agent
# This acts as a client-side proxy - the Customer Support Agent can use it like a local agent
remote_product_catalog_agent = RemoteA2aAgent(
    name="product_catalog_agent",
    description="Remote product catalog agent from external vendor that provides product information.",
    # Point to the agent card URL - this is where the A2A protocol metadata lives
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

print("✅ Remote Product Catalog Agent proxy created!")
print(f"   Connected to: http://localhost:8001")
print(f"   Agent card: http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}")
print("   The Customer Support Agent can now use this like a local sub-agent!")
```

```python
# Now create the Customer Support Agent that uses the remote Product Catalog Agent
customer_support_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="customer_support_agent",
    description="A customer support assistant that helps customers with product inquiries and information.",
    instruction="""
    You are a friendly and professional customer support agent.
    
    When customers ask about products:
    1. Use the product_catalog_agent sub-agent to look up product information
    2. Provide clear answers about pricing, availability, and specifications
    3. If a product is out of stock, mention the expected availability
    4. Be helpful and professional!
    
    Always get product information from the product_catalog_agent before answering customer questions.
    """,
    sub_agents=[remote_product_catalog_agent],  # Add the remote agent as a sub-agent!
)

print("✅ Customer Support Agent created!")
print("   Model: gemini-2.5-flash-lite")
print("   Sub-agents: 1 (remote Product Catalog Agent via A2A)")
print("   Ready to help customers!")
```

## Test A2A Communication
Let's test the agent-to-agent communication! We'll ask the Customer Support Agent about products, and it will communicate with the Product Catalog Agent via A2A.
#### What happens behind the scenes:
1. Customer asks Support Agent a question about a product
2. Support Agent realizes it needs product info
3. Support Agent calls the `remote_product_catalog_agent` (RemoteA2aAgent)
4. ADK sends an A2A protocol request to `http://localhost:8001`
5. Product Catalog Agent processes the request and responds
6. Support Agent receives the response and continues
7. Customer gets the final answer
All of this happens **transparently** - the Support Agent doesn't need to know it's talking to a remote agent!
![[Pasted image 20251124004049.png]]

**What happened:**
1. **Customer** asked about the iPhone 15 Pro
2. **Customer Support Agent** (LlmAgent) received the question and decided it needs product information
3. **Support Agent** delegated to the `product_catalog_agent` sub-agent
4. **RemoteA2aAgent** (client-side proxy) translated this into an A2A protocol request
5. The A2A request was sent over HTTP to `http://localhost:8001` (highlighted in yellow)
6. **Product Catalog Agent** (server) received the request and called `get_product_info("iPhone 15 Pro")`
7. **Product Catalog Agent** returned the product information via A2A response
8. **RemoteA2aAgent** received the response and passed it back to the Support Agent
9. **Support Agent** formulated a final answer with the product details
10. **Customer** received the complete, helpful response

### Key Benefits Demonstrated[](https://www.kaggle.com/code/kaggle5daysofai/day-5a-agent2agent-communication#Key-Benefits-Demonstrated)

1. **Transparency**: Support Agent doesn't "know" Product Catalog Agent is remote
2. **Standard Protocol**: Uses A2A standard - any A2A-compatible agent works
3. **Easy Integration**: Just one line: `sub_agents=[remote_product_catalog_agent]`
4. **Separation of Concerns**: Product data lives in Catalog Agent (vendor), support logic in Support Agent (your company)
### Real-World Applications
This pattern enables:
- **Microservices**: Each agent is an independent service
- **Third-party Integration**: Consume agents from external vendors (e.g., product catalogs, payment processors)
- **Cross-language**: Product Catalog Agent could be Java, Support Agent Python
- **Specialized Teams**: Vendor maintains catalog, your team maintains support agent
- **Cross-Organization**: Vendor hosts catalog on their infrastructure, you integrate via A2A
---
### Deployment
at requirements.txt
```python
%%writefile sample_agent/requirements.txt

google-adk
opentelemetry-instrumentation-google-genai
```

at .env
```python
%%writefile sample_agent/.env

# https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#global-endpoint
GOOGLE_CLOUD_LOCATION="global"

# Set to 1 to use Vertex AI, or 0 to use Google AI Studio
GOOGLE_GENAI_USE_VERTEXAI=1
```
**Configuration explained:**
- `GOOGLE_CLOUD_LOCATION="global"` - Uses the `global` endpoint for Gemini API calls
- `GOOGLE_GENAI_USE_VERTEXAI=1` - Configures ADK to use Vertex AI instead of Google AI Studio
##### Create deployment config
The `.agent_engine_config.json` file controls the deployment settings.

```python
%%writefile sample_agent/.agent_engine_config.json
{
    "min_instances": 0,
    "max_instances": 1,
    "resource_limits": {"cpu": "1", "memory": "1Gi"}
}
```

**Configuration explained:**
- `"min_instances": 0` - Scales down to zero when not in use (saves costs)
- `"max_instances": 1` - Maximum of 1 instance running (sufficient for this demo)
- `"cpu": "1"` - 1 CPU core per instance
- `"memory": "1Gi"` - 1 GB of memory per instance
These settings keep costs minimal while providing adequate resources for our weather agent.
#### Select deployment region
Agent Engine is available in specific regions. We'll randomly select one for this demo.
```python
regions_list = ["europe-west1", "europe-west4", "us-east4", "us-west1"]
deployed_region = random.choice(regions_list)

print(f"✅ Selected deployment region: {deployed_region}")
```

**About regions:**
Agent Engine is available in multiple regions. For production:
- Choose a region close to your users for lower latency
- Consider data residency requirements
### Deploy the agent
This uses the ADK CLI to deploy your agent to Agent Engine.

```python
!adk deploy agent_engine --project=$PROJECT_ID --region=$deployed_region sample_agent --agent_engine_config_file=sample_agent/.agent_engine_config.json
```
**What just happened:**
The `adk deploy agent_engine` command:
1. Packages your agent code (`sample_agent/` directory)
2. Uploads it to Agent Engine
3. Creates a containerized deployment
4. Outputs a resource name like: `projects/PROJECT_NUMBER/locations/REGION/reasoningEngines/ID`

**Note:** Deployment typically takes 2-5 minutes.
##### Retrieve and Test Your Deployed Agent
After deploying with the CLI, we need to retrieve the agent object to interact with it.
```python
# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=deployed_region)

# Get the most recently deployed agent
agents_list = list(agent_engines.list())
if agents_list:
    remote_agent = agents_list[0]  # Get the first (most recent) agent
    client = agent_engines
    print(f"✅ Connected to deployed agent: {remote_agent.resource_name}")
else:
    print("❌ No agents found. Please deploy first.")
```

**What happened:**
This cell retrieves your deployed agent:
1. Initializes the Vertex AI SDK with your project and region
2. Lists all deployed agents in that region
3. Gets the first one (most recently deployed)
4. Stores it as `remote_agent` for testing
##### Test the deployed agent
Now let's send a query to your deployed agent!
```python
async for item in remote_agent.async_stream_query(
    message="What is the weather in Tokyo?",
    user_id="user_42",
):
    print(item)
```

**What happened:**
This cell tests your deployed agent:
1. Sends the query "What is the weather in Tokyo?"
2. Streams the response from the agent

**Understanding the output:**
You'll see multiple items printed:
1. **Function call** - Agent decides to call `get_weather` tool
2. **Function response** - Result from the tool (weather data)
3. **Final response** - Agent's natural language answer
##### Long-Term Memory with Vertex AI Memory Bank
##### What Problem Does Memory Bank Solve?
Your deployed agent has **session memory** - it remembers the conversation while you're chatting. But once the session ends, it forgets everything. Each new conversation starts from scratch.

**The problem:**
- User tells agent "I prefer Celsius" today
- Tomorrow, user asks about weather → Agent gives Fahrenheit (forgot preference)
- User has to repeat preferences every time
### 💡 What is Vertex AI Memory Bank?
Memory Bank gives your agent **long-term memory across sessions**:

|Session Memory|Memory Bank|
|---|---|
|Single conversation|All conversations|
|Forgets when session ends|Remembers permanently|
|"What did I just say?"|"What's my favorite city?"|

**How it works:**
1. **During conversations** - Agent uses memory tools to search past facts
2. **After conversations** - Agent Engine extracts key information ("User prefers Celsius")
3. **Next session** - Agent automatically recalls and uses that information
##### Memory Bank & Your Deployment
Your Agent Engine deployment **provides the infrastructure** for Memory Bank, but it's not enabled by default.

**To use Memory Bank:**
1. Add memory tools to your agent code (`PreloadMemoryTool`)
2. Add a callback to save conversations to Memory Bank
3. Redeploy your agent

Once configured, Memory Bank works automatically - no additional infrastructure needed!
##### Cleanup
 **IMPORTANT: Prevent unexpected charges: Always delete resources when done testing!**
**Cost Reminders**
As a reminder, leaving the agent running can incur costs. Agent Engine offers a monthly free tier, which you can learn more about in the docs.

**Always delete resources when done testing!**
When you're done testing and querying your deployed agent, it's recommended to delete your remote agent to avoid incurring additional costs:
```python
agent_engines.delete(resource_name=remote_agent.resource_name, force=True)

print("✅ Agent successfully deleted")
```

**What happened:**
This cell deletes your deployed agent:
- `resource_name=remote_agent.resource_name` - Identifies which agent to delete
- `force=True` - Forces deletion even if the agent is running