Guardrails
- I/O guardrails are designed to verify data entering a GenAI model and outputs sent to the downstream systems or users
- Such guardrails can flag inappropriate user queries and validate output content against toxicity, hallucinations, or banned topics

![[Pasted image 20260226035550.png]]

API Rate Limiting and Throttling
- consider service exhaustion and model overloading issues in production. 
- Best practice is to implement rate limiting and potentially throttling into your services

- Rate limiting controls the amount of incoming and outgoing traffic to and from a network to prevent abuse, ensure fair usage, and avoid overloading the server.
- throttling controls the API throughput by temporarily slowing down the rate of request processing to stabilize the server.

Both techniques can help you:
- Prevent abuse by blocking malicious users or bots from overwhelming your services from data scraping and brute-force attacks that involve too many requests or large payloads.
- Enforce fair usage policies so that capacity is shared among multiple users and a handful of users are prevented from monopolizing server resources
- Maintain server stability by regulating incoming traffic to maintain consistent performance and prevent crashes during peak periods.

##### Strategies:
## 1. Token Bucket

Imagine a bucket that slowly fills with "permission slips" (tokens). Every time an AI agent wants to perform a task, it must grab a token.

- **The "Burst" Factor:** If the agent hasn't been busy, the bucket fills up. This allows the agent to suddenly handle a **burst** of 10 tasks in a row. Once the bucket is empty, it has to wait for new tokens to drip in.
    
- **Best For:** **Event-driven agents**. If your agent sits idle for an hour and then suddenly needs to process 5 emails at once, Token Bucket allows that flexibility.
---
## 2. Leaky Bucket

Imagine a bucket with a small hole at the bottom. No matter how much water (requests) you pour in at once, it only leaks out (processes) at one constant speed. If you pour too fast, the bucket overflows and those requests are dropped.

- **The "Smooth" Factor:** This is great for **GPU inference**. AI models can only process so much at once. The Leaky Bucket ensures the model gets a steady, predictable stream of work rather than being slammed by 100 requests at the exact same millisecond.
    
- **Best For:** **Stable API services** where you want to guarantee a consistent response time.
---
## 3. Fixed Window
This is the simplest version. You get $X$ requests per minute. At 12:01:00, the counter resets.

- **The "Edge Case":** The danger here is the "boundary spike." If a user sends 100 requests at 12:00:59 and another 100 at 12:01:01, your system just took 200 requests in 2 seconds, even though the limit was "100 per minute."
    
- **Best For:** **Free tiers or credit limits**. "You get 50 messages per day." It’s easy for the user to understand and easy for you to code.
---
## 4. Sliding Window
This is the "smarter" version of the Fixed Window. Instead of resetting at the top of the minute, it looks back at the _last 60 seconds_ from this exact moment.

- **The "Fairness" Factor:** It smooths out the boundary spikes found in the Fixed Window. It is more expensive to calculate (requires more memory to track timestamps), but it feels much "fairer" to the user.
    
- **Best For:** **Premium AI subscriptions**. If a user is paying for high-frequency access, you don't want them getting blocked just because they hit a specific "window" boundary.
---
### Summary Comparison for AI Agents

|**Strategy**|**Logic**|**Vibe**|**Best Agent Use Case**|
|---|---|---|---|
|**Token Bucket**|"Save up for a rainy day."|Flexible|Agents that react to irregular user pings.|
|**Leaky Bucket**|"One at a time, please."|Disciplined|Protecting your local LLM from crashing.|
|**Fixed Window**|"You have a daily allowance."|Strict|Managing API costs for free users.|
|**Sliding Window**|"What have you done lately?"|Precise|Real-time conversational assistants.|

To implement rate limiting, you will need to monitor incoming requests within a time period and use a queue to balance the load

```python
pip install slowapi
```

```python
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

...
limiter = Limiter(
	key_func = get_remote_address, 
	default_limits=["200 per day", "60 per hour", "2/5seconds"]
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request,exc):
	retry_after = int(exc.description.split(" ")[-1])
	
	response_body = {
		"detail": "Rate limit exceeded. Please try again later",
		"retyr_after_seconds": retry_after,
	}
	
	return JSONResponse(
		status_code  = 429,
		content = response_body,
		headers = {"Retry-After: str(retry_after)},
	)
	
app.add_middleware(SlowAPIMiddleware)
```

1. Create rate limiter that tracks usage across each IP address and rejects requests if they exceed specified limits across the application.
2. Add a custom exception handler for rate-limited requests to compute and provide waiting times before requests are accepted again

using limiter decorator
```python
@app.post("/generate/text")
@limiter.limit("5/minute")
def serve_text_to_text_controller(request: Request, ...): 
	return ...
	
@app.post("/generate/image") 
@limiter.limit("1/minute") 
def serve_text_to_image_controller(request: Request, ...): 
	return ...
	
@app.get("/health") 
@limiter.exempt 
def check_health_controller(request: Request): 
	return {"status": "healthy"}
```

- Specify more granular rate limits at endpoint level using a rate limiting decorator. The limiter decorator must be ordered last. 
- Pass the Request object to each controller so that the slowapi limiter decorator can hook into the incoming request. Otherwise, rate limiting will not function. 
- Exclude the /health endpoint from rate-limiting logic as cloud providers or Docker daemons may ping this endpoint continually to check the status of your application. 
- Avoid rate limiting the /health endpoint as external systems may frequently trigger it to check the current status of your service.

API load testing with Apache Benchmark CLI
```python
$ab -n 100 -p 2 http://localhost:8000
```

#### User-based rate limits
- With an IP rate limit, you’re limiting excess usage based on IP, but users can get around IP rate limiting by using VPNs, proxies, or rotating IP addresses. 
- Instead, you want each user to have a dedicated quota to prevent a single user from consuming all available resources. 
- Adding user-based limits can help you prevent abuse
```python
@app.post("/generate/text")
@limiter.limit("10/minute", key_func=get_current_user)
def serve_text_to_text_controller(request: Request): 
	return {"message": f"Hello User"}
```

you will need a Redis database to store user API usage data:
```python
 pip install coredis 
$ docker pull redis 
$ docker run \--name rate-limit-redis-cache \-d \-p 6379:6379 \
redis
```

Adding a centralized usage memory store (Redis) across multiple instances
```python
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware 

app.state.limiter = Limiter(storage_uri="redis://localhost:6379")
app.add_middleware(SlowAPIMiddleware)
```

You now have a working rate-limited API that functions as intended across multiple
instances.
You can get around this issue by implementing your own limiter supported by the
limits
 package instead. Alternatively, you can apply rate limiting via a load balancer,
a reverse proxy, or an API gateway instead.

#### Limiting WebSocket connections 
Unfortunately the slowapi package also doesn’t support limiting async and WebSocket endpoints at the time of writing. 
Because WebSocket connections are likely to be long-lived, you may want to limit the data transition rate sent over the socket. 
You can rely on external packages such as fastapi-limiter to rate limit WebSocket connections

Rate-limiting WebSocket connections with the fastapi_limiter
```python
from contextlib import asynccontextmanager
import redis
from fastapi import Depends, FastAPI
from fastapi.websockets import WebSocket
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import WebSocketRateLimiter
...

@asynccontextmanager
async def lifespan(_: FastAPI): 
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, user_id: int = Depends(get_current_user) 
):
    ratelimit = WebSocketRateLimiter(times=1, seconds=5)
    await ws_manager.connect(websocket)
    
    try:
        while True:
            prompt = await ws_manager.receive(websocket)
            await ratelimit(websocket, context_key=user_id) 
            
            async for chunk in azure_chat_client.chat_stream(prompt, "ws"):
                await ws_manager.send(chunk, websocket)
    except WebSocketRateLimitException:
        await websocket.send_text(f"Rate limit exceeded. Try again later")
    finally:
        await ws_manager.disconnect(websocket)

```

1.  Configure the FastAPILimiter application lifespan with a Redis storage backend.
2. Configure a WebSocket rate limiter to allow one request per second.
3. Use the user’s ID as the unique identifier for rate limiting.