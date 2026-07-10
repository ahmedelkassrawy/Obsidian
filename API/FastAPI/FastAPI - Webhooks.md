# FastAPI Webhooks Implementation Guide

## 📚 What Are Webhooks?

Webhooks are automated HTTP callbacks that allow your application to send real-time data to other services when specific events occur. Instead of constantly polling your API for updates, external services can register a URL (webhook endpoint) to receive instant notifications.

**Think of it like this:**
- **Polling (Old Way):** "Are you done yet? Are you done yet? Are you done yet?"
- **Webhooks (Modern Way):** "I'll call you when I'm done!"

---
## 🏗️ Your Current Webhook Implementation

Your FastAPI application has **TWO webhook components**:

### 1. Webhook Sender (Outgoing Webhooks)
Sends notifications to external services when events happen in your app.

**Location:** `/create-subscription` endpoint

### 2. Webhook Receiver (Incoming Webhooks)
Receives notifications from external services.

**Location:** `/webhook` endpoint

---

## 📦 Required Code Components

### 1. Dependencies (`main.py`)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import httpx  # For sending webhooks asynchronously
```

**Install dependencies:**
```bash
pip install fastapi uvicorn httpx
```

### 2. Configuration File (`webhook_config.py`)

```python
# Webhook Configuration
WEBHOOK_URLS = [
    # Add external service URLs here
    "https://your-service.com/webhook",
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
]

WEBHOOK_TIMEOUT = 5.0  # seconds
WEBHOOK_RETRY = False  # Enable if you want retry logic
```

### 3. Import Configuration in `main.py`

```python
try:
    from webhook_config import WEBHOOK_URLS, WEBHOOK_TIMEOUT
except ImportError:
    # Fallback values if config file doesn't exist
    WEBHOOK_URLS = []
    WEBHOOK_TIMEOUT = 5.0
```

---

## 🔧 How to Implement Webhook Sender

### Step 1: Create the Sending Logic

```python
@app.post("/create-subscription")
async def create_sub(sub: Subscription):
    # 1. Process your main business logic first
    response = {
        "message": "Subscription created successfully",
        "username": sub.username,
        "monthly_fee": sub.monthly_fee,
        "start_date": sub.start_date.isoformat()
    }
    # 2. Prepare webhook data
    webhook_data = {
        "username": sub.username,
        "monthly_fee": sub.monthly_fee,
        "start_date": sub.start_date.isoformat(),
        "event": "subscription_created"  # Optional: event type
    }
    # 3. Send webhooks to all configured URLs
    async with httpx.AsyncClient() as client:
        for webhook_url in WEBHOOK_URLS:
            try:
                webhook_response = await client.post(
                    webhook_url,
                    json=webhook_data,
                    timeout=WEBHOOK_TIMEOUT
                )
                print(f"✓ Webhook sent to {webhook_url}: {webhook_response.status_code}")
            except Exception as e:
                print(f"✗ Failed to send webhook to {webhook_url}: {e}")
                # Don't fail the main operation if webhook fails
    return JSONResponse(status_code=201, content=response)
```

### Step 2: Key Principles

> [!tip]
> - ✅ **Always use `async with httpx.AsyncClient()`** - Don't block your API  
> - ✅ **Handle errors gracefully** - Webhook failures shouldn't crash your API  
> - ✅ **Use try-except blocks** - Catch connection errors  
> - ✅ **Log everything** - Track successful and failed webhook deliveries  
> - ✅ **Set timeouts** - Don't wait forever for slow services  

---

## 📥 How to Implement Webhook Receiver

### Step 1: Create the Receiving Endpoint

```python
@app.post("/webhook")
async def receive_webhook(request: Request):
    # 1. Parse incoming JSON data
    data = await request.json()
    
    # 2. Log the received data
    print("Received webhook data:", data)
    
    # 3. Process the webhook (your custom logic)
    # Example: Save to database, trigger actions, etc.
    
    # 4. Return acknowledgment
    return {"status": "Webhook received"}
```

### Step 2: Add Validation (Recommended)

```python
from typing import Optional

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
        
        # Validate webhook data
        if not data:
            raise HTTPException(status_code=400, detail="Empty payload")
            
        print("Received webhook data:", data)
        
        # Your custom processing logic here
        # e.g., update database, send emails, etc.
        
        return {"status": "success", "message": "Webhook processed"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
```

---

## 🚀 Usage Guide

### Starting Your Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload

# Server runs at: http://localhost:8000
```

### Testing Webhook Sender

**Method 1: Create a subscription (triggers webhook)**

```bash
curl -X POST http://localhost:8000/create-subscription \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","monthly_fee":29.99,"start_date":"2025-10-29T10:00:00"}'
```

**What happens:**
1. Subscription is created
2. Webhook is sent to allraising all URLs in `WEBHOOK_URLS`
3. Check your console for webhook delivery logs

### Testing Webhook Receiver

**Method 1: Using curl**

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event":"test","data":"Hello from external service"}'
```

**Method 2: Using Python**

```python
import requests

response = requests.post(
    "http://localhost:8000/webhook",
    json={"event": "payment_received", "amount": 100}
)
print(response.json())
```

**Method 3: Using Postman/Insomnia**
- Method: POST
- URL: `http://localhost:8000/webhook`
- Headers: `Content-Type: application/json`
- Body: Any JSON data

---

## 🔐 Security Best Practices

### 1. Verify Webhook Signatures

```python
import hmac
import hashlib

def verify_webhook_signature(signature: str, payload: bytes, secret: str) -> bool:
    """Verify that webhook came from trusted source"""
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@app.post("/webhook")
async def receive_webhook(request: Request):
    # Get signature from headers
    signature = request.headers.get("X-Webhook-Signature")
    # Get raw body
    body = await request.body()
    # Verify signature
    if not verify_webhook_signature(signature, body, "your-secret-key"):
        raise HTTPException(status_code=401, detail="Invalid signature")
    # Process webhook...
```

### 2. Use HTTPS in Production

```python
# webhook_config.py (Production)
WEBHOOK_URLS = [
    "https://your-service.com/webhook",  # ✓ HTTPS
    # "http://insecure.com/webhook",     # ✗ Avoid HTTP
]
```

### 3. Rate Limiting

```python
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/webhook")
@limiter.limit("10/minute")  # Max 10 webhooks per minute
async def receive_webhook(request: Request):
    # Process webhook...
    pass
```

### 4. Authentication Headers

```python
# When sending webhooks, include authentication
async with httpx.AsyncClient() as client:
    webhook_response = await client.post(
        webhook_url,
        json=webhook_data,
        headers={
            "Authorization": "Bearer YOUR_API_KEY",
            "X-Webhook-Signature": generate_signature(webhook_data)
        },
        timeout=WEBHOOK_TIMEOUT
    )
```

---

## 🎯 Real-World Use Cases

### 1. Notify Slack When Subscription Created

```python
# webhook_config.py
WEBHOOK_URLS = [
    "https://hooks.slack.com/services/T00/B00/XXX"
]

# Format data for Slack
webhook_data = {
    "text": f"🎉 New subscription from {sub.username}",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*New Subscription*\n• User: {sub.username}\n• Fee: ${sub.monthly_fee}"
            }
        }
    ]
}
```

### 2. Send to Discord

```python
# webhook_config.py
WEBHOOK_URLS = [
    "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/TOKEN"
]

# Format data for Discord
webhook_data = {
    "content": f"New subscription from {sub.username}",
    "embeds": [{
        "title": "Subscription Created",
        "description": f"Monthly Fee: ${sub.monthly_fee}",
        "color": 5814783
    }]
}
```

### 3. Trigger External Processing

```python
# webhook_config.py
WEBHOOK_URLS = [
    "https://your-analytics-service.com/webhook",
    "https://your-crm.com/api/webhooks/new-customer",
    "https://your-email-service.com/send-welcome"
]
```

---

## 🛠️ Advanced: Webhook Retry Logic

```python
async def send_webhook_with_retry(webhook_url: str, data: dict, max_retries: int = 3):
    """Send webhook with exponential backoff retry"""
    import asyncio
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                response = await client.post(
                    webhook_url,
                    json=data,
                    timeout=WEBHOOK_TIMEOUT
                )
                if response.status_code < 500:  # Success or client error
                    return response
                # Server error - retry
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    print(f"Failed after {max_retries} attempts: {e}")
                    raise
```

---

## 📊 Monitoring Webhooks

### Add Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    logger.info(f"Webhook received from {request.client.host}: {data}")
    # Process webhook...
    logger.info("Webhook processed successfully")
    return {"status": "success"}
```

### Track Webhook Metrics

```python
from collections import defaultdict

webhook_stats = defaultdict(int)

async def send_webhook(url: str, data: dict):
    try:
        # Send webhook...
        webhook_stats[f"{url}_success"] += 1
    except Exception:
        webhook_stats[f"{url}_failed"] += 1

@app.get("/webhook-stats")
async def get_webhook_stats():
    return webhook_stats
```

---
## 🎓 Quick Reference

| Action             | Endpoint                    | Method |
|--------------------|-----------------------------|--------|
| Send webhook       | Triggered by `/create-subscription` | Automatic |
| Receive webhook    | `/webhook`                  | POST   |
| View API docs      | `/docs`                     | GET    |

**Configuration File:** `webhook_config.py`  
**Dependencies:** `fastapi`, `uvicorn`, `httpx`  
**Start Server:** `uvicorn main:app --reload`

---

## ❓ Troubleshooting

> [!warning] Webhooks not being sent?
> - Check `webhook_config.py` for valid URLs
> - Verify `httpx` is installed: `pip install httpx`
> - Check console logs for error messages
> - Ensure URLs are reachable (try curl)

> [!warning] Webhooks not being received?
> - Verify server is running on correct port
> - Check firewall settings
> - Ensure Content-Type is `application/json`
> - Check server logs for errors

> [!warning] Connection timeout errors?
> - Increase `WEBHOOK_TIMEOUT` value
> - Check if target service is online
> - Verify network connectivity

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HTTPX Documentation](https://www.python-httpx.org/)
- [Webhook Best Practices](https://webhooks.dev/)

---

> [!note] Need help?
> Check the FastAPI docs at `http://localhost:8000/docs` when your server is running!
