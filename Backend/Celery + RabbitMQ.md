### 1. The Task Definition (`tasks.py`)
This is where you define the work to be done. The `@app.task` decorator tells Celery that this function can be run in the background.

```python
from celery import Celery

# 1. Initialize Celery 
# 'py_app' is the name of the current module
# broker='amqp://guest@localhost//' tells Celery to use RabbitMQ
app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

@app.task
def process_video(video_id):
    print(f"Started processing video: {video_id}")
    # Simulate a heavy task
    import time
    time.sleep(10) 
    return f"Video {video_id} processed successfully!"
```

### 2. The Producer (`app.py`)
This represents your web server (like Django or Flask). Instead of running the function directly, it "delays" it, sending a message to RabbitMQ.

```python
from tasks import process_video

# .delay() sends the task to the RabbitMQ queue immediately
# The web app continues running without waiting for the result
result = process_video.delay("101_tutorial_mp4")

print(f"Task sent to RabbitMQ! Task ID: {result.id}")
```

---
### How the Flow Works
When you run the code above, the communication follows a specific path. RabbitMQ acts as the middleman ensuring the message isn't lost if the worker is busy or offline.
1. **The Producer** calls `.delay()`.
2. **Celery** serializes the function name and arguments into a JSON message.
3. **RabbitMQ** receives the message and puts it into a queue.
4. **The Worker** (running in a separate terminal) sees a new message in the queue.
5. **The Worker** pulls the message, executes the Python function, and (optionally) sends the result back.
---
### 3. How to Run It
To see this in action, you need to open two terminal windows:

**Terminal 1: Start the Worker** This process sits and waits for messages from RabbitMQ.
```
celery -A tasks worker --loglevel=info
```

**Terminal 2: Run the Application** This triggers the task.
```
python app.py
```

---
### Key Configuration Tips
- **The Connection String:** `amqp://guest:guest@localhost:5672//` is the default for a local RabbitMQ install. In production, you would replace `guest` with a secure username and password.
    
- **Result Backend:** By default, Celery is "fire and forget." If you need to know the _result_ of the task later (e.g., "Did the video finish?"), you need to add a `backend` (usually **Redis** or a Database).