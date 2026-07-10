---
title: Celery - Complete Guide
tags:
  - celery
  - distributed-tasks
  - rabbitmq
  - redis
  - task-queue
  - backend
aliases:
  - Celery Documentation
  - Task Queue Guide
date: 2026-03-26
status: refined
---

# Celery - Complete Guide

A practical, step-by-step guide to implementing Celery in production. Each section explains **what** it is, **why** you need it, **when** to use it, and **how** to implement it.

---

## Table of Contents

1. [[#Quick Decision Guide]]
2. [[#Core Concepts]]
3. [[#Setup & Configuration]]
4. [[#Creating Tasks]]
5. [[#Idempotency & Deduplication]]
6. [[#Task Workflows]]
7. [[#Periodic Tasks]]
8. [[#Monitoring & Operations]]
9. [[#Troubleshooting]]

---

## Quick Decision Guide

### Do I Need Celery?

| Scenario | Use Celery? | Why |
|----------|-------------|-----|
| API response takes > 2 seconds | ✅ Yes | Users get instant response, work happens in background |
| Sending emails/notifications | ✅ Yes | Non-blocking, can retry on failure |
| Processing uploaded files | ✅ Yes | Heavy I/O shouldn't block requests |
| Simple database CRUD | ❌ No | Fast enough to run synchronously |
| Real-time websocket updates | ❌ No | Use websockets/SSE instead |
| Tasks that must run at exact times | ⚠️ Maybe | Use Celery Beat, but consider cron for simplicity |

### Broker Selection Cheat Sheet

| Choose **Redis** when... | Choose **RabbitMQ** when... |
|--------------------------|----------------------------|
| Already using Redis for caching | Need guaranteed delivery |
| Tasks are small & quick (<1min) | Tasks carry large payloads |
| Occasional lost tasks are OK | Complex routing/priorities needed |
| Want minimal infrastructure | Need message acknowledgments |
| **Fire-and-forget** patterns | **At-least-once** delivery required |

---

## Core Concepts

### What is Celery?

**Celery** = A distributed task queue that runs Python functions in background worker processes.

### The 4 Components

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Your App  │───▶│   Broker    │───▶│   Worker    │───▶│  Backend    │
│  (Producer) │    │(Redis/RMQ)  │    │ (Executor)  │    │ (Results)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     sends              queues           executes          stores
     task               message          function          result
```

| Component | What It Does | Required? |
|-----------|--------------|-----------|
| **Producer** | Your FastAPI/Django app that calls `.delay()` | ✅ Yes |
| **Broker** | Message queue (Redis/RabbitMQ) that holds tasks | ✅ Yes |
| **Worker** | Process that executes tasks | ✅ Yes |
| **Backend** | Stores task results for retrieval | ❌ Optional |

### Terminology Quick Reference

| Term | Definition | Example |
|------|------------|---------|
| `Task` | Decorated Python function | `@app.task def process_video()` |
| `delay()` | Sends task to queue immediately | `process_video.delay("video.mp4")` |
| `apply_async()` | Sends task with options (countdown, ETA) | `task.apply_async(countdown=60)` |
| `bind=True` | Gives task access to `self` for retries | `@app.task(bind=True)` |
| `acks_late` | Acknowledge after execution (safer) | Prevents loss on crash |
| `Beat` | Scheduler for periodic tasks | Runs tasks on cron-like schedule |

---

## Setup & Configuration

### Step 1: Installation

```bash
# Core Celery
pip install celery

# Choose your broker
pip install redis        # For Redis broker
# OR
pip install amqp         # For RabbitMQ broker (included by default)

# Optional monitoring
pip install flower
```

### Step 2: Choose Your Broker

#### Option A: Redis Setup

**When:** Simple setup, already using Redis, fire-and-forget tasks OK.

```bash
# Docker
docker run -d --name redis -p 6379:6379 redis:alpine

# Connection string
CELERY_BROKER_URL=redis://localhost:6379/0
```

#### Option B: RabbitMQ Setup

**When:** Need guaranteed delivery, complex routing, large payloads.

```bash
# Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

# Connection string
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
```

> [!warning] Late Acknowledge Gotcha
> With `acks_late=True`, a worker appears "free" while still processing. The broker might send the same task to another worker if the first is slow. Use idempotency to handle this.

### Step 3: Minimal Working Example

**File structure:**
```
my_project/
├── celery_app.py      # Celery configuration
├── tasks/
│   ├── __init__.py
│   └── email.py       # Task definitions
└── main.py            # Your FastAPI/Flask app
```

**`celery_app.py`** - Celery Configuration:
```python
from celery import Celery

app = Celery(
    'my_project',
    broker='redis://localhost:6379/0',        # Message queue
    backend='redis://localhost:6379/1',       # Result storage
    include=['tasks.email']                   # Auto-discover tasks
)

# Recommended defaults
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    task_track_started=True,
)
```

**`tasks/email.py`** - Define a Task:
```python
from celery_app import app

@app.task
def send_welcome_email(user_email: str):
    """Send welcome email to new user."""
    # Your email sending logic here
    print(f"Sending welcome email to {user_email}")
    return {"status": "sent", "to": user_email}
```

**`main.py`** - Dispatch the Task:
```python
from tasks.email import send_welcome_email

# Fire and forget - returns immediately
result = send_welcome_email.delay("user@example.com")
print(f"Task queued with ID: {result.id}")
```

### Step 4: Run the System

```bash
# Terminal 1: Start the worker
celery -A celery_app worker --loglevel=info

# Terminal 2: Run your application
python main.py
```

### Step 5: Production Configuration

```python
# celery_app.py - Production-ready configuration
from celery import Celery
from config import settings

celery_app = Celery(
    "production_app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "tasks.file_processing",
        "tasks.email_service",
        "tasks.maintenance"
    ]
)

celery_app.conf.update(
    # Serialization - JSON is safest
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    
    # Safety - Acknowledge AFTER execution (prevents loss on crash)
    task_acks_late=True,
    
    # Time limits - Kill stuck tasks
    task_time_limit=600,           # Hard kill after 10 mins
    task_soft_time_limit=540,      # Warn at 9 mins
    
    # Results - Store for status tracking
    task_ignore_result=False,
    result_expires=3600,           # Clean up after 1 hour
    
    # Workers
    worker_concurrency=4,          # Parallel task execution
    worker_prefetch_multiplier=1,  # Fetch 1 task at a time (fairer)
    
    # Connection resilience
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    
    # Route tasks to specific queues
    task_routes={
        "tasks.file_processing.*": {"queue": "files"},
        "tasks.email_service.*": {"queue": "email"},
        "*": {"queue": "default"}
    }
)

celery_app.conf.task_default_queue = "default"
```

**Environment Variables (`.env`):**
```env
CELERY_BROKER_URL=amqp://user:password@rabbitmq:5672/vhost
CELERY_RESULT_BACKEND=redis://:password@redis:6379/0
CELERY_WORKER_CONCURRENCY=4
CELERY_TASK_TIME_LIMIT=600
```

### Configuration Options Reference

| Option | Purpose | Recommended Value |
|--------|---------|-------------------|
| `task_acks_late` | Acknowledge after completion | `True` (safer) |
| `task_time_limit` | Hard timeout (kills task) | 600 seconds |
| `task_soft_time_limit` | Soft timeout (raises exception) | 540 seconds |
| `worker_concurrency` | Parallel workers | CPU cores or I/O bound * 2 |
| `worker_prefetch_multiplier` | Tasks to prefetch | 1 (fair scheduling) |
| `result_expires` | Auto-delete results after | 3600 seconds |
| `task_serializer` | Message format | `json` (safest) |

---

## Creating Tasks

### Task Patterns Overview

| Pattern | When to Use | Decorator |
|---------|-------------|-----------|
| **Simple Task** | Quick, stateless operations | `@app.task` |
| **Bound Task** | Need retries, task ID access | `@app.task(bind=True)` |
| **Async Task** | Database/I/O with async code | `@app.task(bind=True)` + `asyncio.run()` |
| **Retry Task** | External APIs, network calls | `autoretry_for=(Exception,)` |

### Pattern 1: Simple Task

**When:** Quick operations, no error handling needed.

```python
from celery_app import app

@app.task
def send_notification(user_id: int, message: str):
    """Simple fire-and-forget notification."""
    # Send notification logic
    return {"user_id": user_id, "sent": True}

# Usage
send_notification.delay(123, "Welcome!")
```

### Pattern 2: Bound Task with Retries

**When:** External API calls, network operations that may fail.

```python
from celery_app import app
from celery.exceptions import SoftTimeLimitExceeded
import httpx

@app.task(
    bind=True,                              # Access self.request, self.retry()
    autoretry_for=(httpx.RequestError,),    # Auto-retry on these exceptions
    dont_autoretry_for=(SoftTimeLimitExceeded,),  # Don't retry timeouts
    max_retries=3,                          # Maximum retry attempts
    default_retry_delay=30,                 # Wait 30s between retries
    acks_late=True                          # Acknowledge after completion
)
def call_external_api(self, endpoint: str, payload: dict):
    """Call external API with automatic retries."""
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        # Log and let autoretry handle it
        print(f"Attempt {self.request.retries + 1} failed: {exc}")
        raise

# Usage
call_external_api.delay("https://api.example.com/webhook", {"event": "signup"})
```

### Pattern 3: Async-Aware Task (FastAPI/SQLAlchemy)

**When:** Your business logic uses `async`/`await` (database, async HTTP).

**Why:** Celery workers are synchronous. You must bridge with `asyncio.run()`.

```python
import asyncio
import nest_asyncio
from celery_app import celery_app
from database import get_async_session_maker

nest_asyncio.apply()  # Allow nested event loops

@celery_app.task(
    bind=True,
    name="tasks.user_service.sync_user_data",
    acks_late=True,
    max_retries=3,
    default_retry_delay=60
)
def sync_user_data(self, user_id: int):
    """Synchronous Celery wrapper for async logic."""
    return asyncio.run(_sync_user_data_async(self, user_id))

async def _sync_user_data_async(task_instance, user_id: int):
    """The actual async business logic."""
    session_maker = get_async_session_maker()
    
    async with session_maker() as session:
        # Your async database operations
        user = await session.get(User, user_id)
        
        # Process user data
        result = await process_user(user)
        
        return {"user_id": user_id, "processed": True}
```

### Pattern 4: Task with Manual State Updates

**When:** Long-running tasks where you want to track progress.

```python
@celery_app.task(bind=True, name="tasks.processing.batch_process")
def batch_process(self, items: list):
    """Process items with progress tracking."""
    total = len(items)
    processed = 0
    
    for item in items:
        # Update state for monitoring
        self.update_state(
            state='PROGRESS',
            meta={'current': processed, 'total': total}
        )
        
        # Process item
        process_item(item)
        processed += 1
    
    return {'processed': processed, 'total': total}

# Check progress from client
result = batch_process.delay([1, 2, 3, 4, 5])
print(result.info)  # {'current': 2, 'total': 5} while running
```

### Dispatching Tasks from FastAPI

```python
from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from tasks.file_processing import process_file_task
import base64

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    """Upload and process file asynchronously."""
    
    # Validate
    allowed_types = ["application/pdf", "text/csv", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"Unsupported type: {file.content_type}")
    
    # Read file content
    content = await file.read()
    
    # ⚠️ IMPORTANT: Don't pass large files directly!
    # Option 1: Save to S3/disk, pass path
    # Option 2: For small files (<1MB), base64 encode
    
    if len(content) > 1_000_000:  # 1MB
        raise HTTPException(413, "File too large. Use presigned URL upload.")
    
    file_b64 = base64.b64encode(content).decode('utf-8')
    
    # Queue task
    task = process_file_task.delay(
        file_b64=file_b64,
        file_name=file.filename,
        file_type=file.content_type
    )
    
    return {
        "message": "Processing started",
        "task_id": task.id,
        "status_url": f"/tasks/{task.id}/status"
    }

@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """Check task status and result."""
    from celery.result import AsyncResult
    
    result = AsyncResult(task_id)
    
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
        "error": str(result.result) if result.failed() else None
    }
```

> [!warning] Anti-Pattern: Large Payloads
> **Never** pass files >1MB directly to Celery tasks. The broker (Redis/RabbitMQ) isn't designed for large messages.
> 
> **Do this instead:**
> 1. Upload file to S3/MinIO/disk
> 2. Pass the file path/URL to the task
> 3. Task downloads and processes the file

---

## Idempotency & Deduplication

### The Problem

In distributed systems, tasks can be executed multiple times due to:

| Scenario | What Happens |
|----------|--------------|
| User double-clicks submit | Two identical tasks queued |
| Worker crashes mid-execution | Task redelivered to another worker |
| Network timeout + retry | Duplicate task sent |
| `acks_late=True` + slow task | Broker redelivers "stuck" task |

**Without idempotency:** Files processed twice, emails sent twice, charges made twice.

### The Solution: IdempotencyManager

Create a database record with a **unique hash of task arguments**. The database enforces uniqueness—second attempts fail with a constraint violation.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Idempotency Flow                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Task arrives → Hash(task_name + args) → "abc123"            │
│  2. Check DB: Does record with hash "abc123" exist?             │
│     ├─ No  → Create record (PENDING) → Execute → Update result  │
│     └─ Yes → Return existing result (skip execution)            │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Database Schema

```python
from sqlalchemy import Column, Integer, DateTime, func, String, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base

class CeleryTaskExecution(Base):
    """Track task executions for idempotency."""
    __tablename__ = "celery_task_executions"

    execution_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=False)
    
    # CRITICAL: This is the idempotency key
    task_args_hash = Column(String(64), nullable=False)
    
    # Track which Celery task ID is handling this
    celery_task_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Status: PENDING → IN_PROGRESS → SUCCESS/FAILURE
    status = Column(String(20), nullable=False, default='PENDING')
    
    # Store arguments and results
    task_args = Column(JSONB, nullable=True)
    result = Column(JSONB, nullable=True)

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        # UNIQUE on (task_name, task_args_hash) - NOT celery_task_id!
        # This ensures same args can only have ONE execution record
        Index('uix_task_name_args_hash', task_name, task_args_hash, unique=True),
        Index('ix_task_execution_status', status),
        Index('ix_celery_task_id', celery_task_id),
    )
```

> [!important] Why Exclude `celery_task_id` from Unique Index?
> If two different Celery task IDs try to process the same file, you want the database to **block the second one**. Including `celery_task_id` would allow both to proceed.

### Step 2: IdempotencyManager Implementation

```python
import hashlib
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

class IdempotencyManager:
    """
    Ensures tasks with identical arguments execute only once.
    
    Usage:
        manager = IdempotencyManager(session_maker)
        should_run, existing = await manager.should_execute_task(name, args, task_id)
        if not should_run:
            return existing.result  # Skip, return cached result
    """
    
    def __init__(self, session_maker):
        self.session_maker = session_maker

    def create_args_hash(self, task_name: str, task_args: dict) -> str:
        """Create deterministic hash from task name + arguments."""
        combined = {"task_name": task_name, **task_args}
        json_str = json.dumps(combined, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    async def should_execute_task(
        self, 
        task_name: str, 
        task_args: dict,
        celery_task_id: str, 
        task_time_limit: int = 600
    ) -> tuple[bool, "CeleryTaskExecution | None"]:
        """
        Determine if task should execute or return cached result.
        
        Returns:
            (True, None) - Execute task, no existing record
            (True, record) - Execute task, previous failed/timed out
            (False, record) - Skip, return existing result
        """
        args_hash = self.create_args_hash(task_name, task_args)
        
        async with self.session_maker() as session:
            stmt = select(CeleryTaskExecution).where(
                CeleryTaskExecution.task_name == task_name,
                CeleryTaskExecution.task_args_hash == args_hash
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
        
        if not existing:
            return True, None
            
        # Already succeeded - return cached result
        if existing.status == 'SUCCESS':
            return False, existing
        
        # Check if task is stuck (exceeded time limit + grace period)
        if existing.status in ['PENDING', 'IN_PROGRESS']:
            if existing.started_at:
                elapsed = (datetime.utcnow() - existing.started_at).total_seconds()
                grace_period = 60  # Extra buffer
                if elapsed > (task_time_limit + grace_period):
                    return True, existing  # Stuck, allow re-execution
            return False, existing  # Still running, wait
        
        # Failed previously - allow retry
        if existing.status == 'FAILURE':
            return True, existing
            
        return False, existing
    
    async def create_task_record(
        self, 
        task_name: str, 
        task_args: dict, 
        celery_task_id: str
    ) -> CeleryTaskExecution:
        """
        Create execution record. Uses UNIQUE constraint for race condition safety.
        
        Raises IntegrityError if duplicate - caller should handle gracefully.
        """
        args_hash = self.create_args_hash(task_name, task_args)
        
        record = CeleryTaskExecution(
            task_name=task_name,
            task_args_hash=args_hash,
            task_args=task_args,
            celery_task_id=celery_task_id,
            status='PENDING',
            started_at=datetime.utcnow()
        )
        
        async with self.session_maker() as session:
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record

    async def update_task_status(
        self, 
        execution_id: int, 
        status: str, 
        result: dict = None
    ):
        """Update task status and optionally store result."""
        async with self.session_maker() as session:
            record = await session.get(CeleryTaskExecution, execution_id)
            if record:
                record.status = status
                if result:
                    record.result = result
                if status in ['SUCCESS', 'FAILURE']:
                    record.completed_at = datetime.utcnow()
                await session.commit()

    async def cleanup_old_tasks(self, retention_seconds: int = 86400) -> int:
        """Delete records older than retention period. Returns count deleted."""
        cutoff = datetime.now(timezone.utc) - timedelta(seconds=retention_seconds)
        
        async with self.session_maker() as session:
            stmt = delete(CeleryTaskExecution).where(
                CeleryTaskExecution.created_at < cutoff
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount
```

### Step 3: Using IdempotencyManager in Tasks

```python
import asyncio
from celery_app import celery_app
from idempotency import IdempotencyManager
from database import get_async_session_maker
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="tasks.files.process_upload", acks_late=True)
def process_upload(self, file_path: str, user_id: int):
    """Idempotent file processing task."""
    return asyncio.run(_process_upload_async(self, file_path, user_id))

async def _process_upload_async(task_instance, file_path: str, user_id: int):
    session_maker = get_async_session_maker()
    manager = IdempotencyManager(session_maker)
    
    task_name = task_instance.name
    task_args = {"file_path": file_path, "user_id": user_id}
    celery_task_id = task_instance.request.id
    
    # Step 1: Check if we should execute
    should_run, existing = await manager.should_execute_task(
        task_name, task_args, celery_task_id
    )
    
    if not should_run and existing:
        logger.info(f"Skipping duplicate task, returning cached result")
        return existing.result
    
    # Step 2: Create or reuse record
    try:
        if existing:
            record = existing
        else:
            record = await manager.create_task_record(
                task_name, task_args, celery_task_id
            )
    except IntegrityError:
        # Race condition: another worker got there first
        logger.info("Another worker claimed this task, exiting")
        return {"status": "skipped", "reason": "claimed_by_other_worker"}
    
    # Step 3: Execute with status tracking
    await manager.update_task_status(record.execution_id, "IN_PROGRESS")
    
    try:
        # ============ YOUR BUSINESS LOGIC HERE ============
        result = await do_actual_processing(file_path, user_id)
        # ==================================================
        
        await manager.update_task_status(
            record.execution_id, "SUCCESS", result=result
        )
        return result
        
    except Exception as e:
        await manager.update_task_status(
            record.execution_id, "FAILURE", result={"error": str(e)}
        )
        raise
```

### Idempotency Decision Matrix

| Existing Status | Started > Time Limit? | Action |
|-----------------|----------------------|--------|
| No record | - | ✅ Execute, create record |
| PENDING | No | ⏳ Skip, wait for completion |
| PENDING | Yes | ✅ Execute, task is stuck |
| IN_PROGRESS | No | ⏳ Skip, wait for completion |
| IN_PROGRESS | Yes | ✅ Execute, task is stuck |
| SUCCESS | - | ✅ Skip, return cached result |
| FAILURE | - | ✅ Execute, retry allowed |

---

## Task Workflows

### When to Use Workflows

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Chain** | Sequential steps, each needs previous result | Process file → Index → Notify |
| **Group** | Parallel independent tasks | Send email to 100 users |
| **Chord** | Parallel tasks + callback when all complete | Process 10 images → Create gallery |

### Pattern 1: Chain (Sequential Pipeline)

**When:** Steps must run in order, each step needs the previous result.

```python
from celery import chain
from celery_app import celery_app

@celery_app.task(name="tasks.pipeline.extract")
def extract_data(file_path: str) -> dict:
    """Step 1: Extract data from file."""
    data = read_file(file_path)
    return {"file_path": file_path, "records": len(data), "data": data}

@celery_app.task(name="tasks.pipeline.transform")  
def transform_data(prev_result: dict) -> dict:
    """Step 2: Transform extracted data. Receives result from extract."""
    data = prev_result["data"]
    transformed = [process(item) for item in data]
    return {**prev_result, "transformed": transformed}

@celery_app.task(name="tasks.pipeline.load")
def load_data(prev_result: dict) -> dict:
    """Step 3: Load transformed data. Receives result from transform."""
    save_to_database(prev_result["transformed"])
    return {"status": "complete", "records": prev_result["records"]}

# Execute the chain
pipeline = chain(
    extract_data.s("data.csv"),    # .s() = signature (partial function)
    transform_data.s(),             # Receives extract result automatically
    load_data.s()                   # Receives transform result automatically
)
result = pipeline.apply_async()
print(f"Pipeline ID: {result.id}")
```

> [!info] How Chain Passes Data
> - First task receives explicit arguments: `extract_data.s("data.csv")`
> - Subsequent tasks receive the **return value** of the previous task as their **first argument**
> - Your function signature must accept this: `def transform_data(prev_result: dict)`

### Pattern 2: Group (Parallel Execution)

**When:** Many independent tasks that can run simultaneously.

```python
from celery import group

@celery_app.task(name="tasks.email.send_to_user")
def send_email_to_user(user_id: int, template: str):
    """Send email to a single user."""
    user = get_user(user_id)
    send_email(user.email, template)
    return {"user_id": user_id, "sent": True}

# Send to 100 users in parallel
user_ids = list(range(1, 101))
job = group(
    send_email_to_user.s(uid, "welcome") for uid in user_ids
)
result = job.apply_async()

# Check progress
print(f"Completed: {result.completed_count()} / 100")
```

### Pattern 3: Chord (Parallel + Callback)

**When:** Run tasks in parallel, then do something when ALL complete.

```python
from celery import chord

@celery_app.task(name="tasks.images.resize")
def resize_image(image_path: str) -> str:
    """Resize single image, return path to resized version."""
    resized_path = do_resize(image_path)
    return resized_path

@celery_app.task(name="tasks.images.create_gallery")
def create_gallery(resized_paths: list) -> dict:
    """Called when ALL resize tasks complete. Receives list of all results."""
    gallery_url = build_gallery(resized_paths)
    return {"gallery_url": gallery_url, "image_count": len(resized_paths)}

# Process 10 images, then create gallery
images = ["img1.jpg", "img2.jpg", ..., "img10.jpg"]
workflow = chord(
    [resize_image.s(img) for img in images],  # Header: parallel tasks
    create_gallery.s()                         # Callback: runs when all complete
)
result = workflow.apply_async()
```

### Real-World Example: File Processing Pipeline

```python
from celery import chain
from celery_app import celery_app
import asyncio

@celery_app.task(
    bind=True, 
    name="tasks.workflow.process_and_index",
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60}
)
def process_and_index_workflow(self, project_id: int, file_id: int):
    """Orchestrate file processing pipeline."""
    
    workflow = chain(
        process_file.s(project_id, file_id),    # Step 1: Process
        index_content.s(),                       # Step 2: Index (receives process result)
        notify_completion.s()                    # Step 3: Notify (receives index result)
    )
    
    result = workflow.apply_async()
    
    return {
        "workflow_id": result.id,
        "status": "STARTED",
        "steps": ["process_file", "index_content", "notify_completion"]
    }

@celery_app.task(bind=True, name="tasks.workflow.process_file")
def process_file(self, project_id: int, file_id: int):
    """Extract and parse file content."""
    content = extract_content(file_id)
    return {
        "project_id": project_id,
        "file_id": file_id,
        "content": content,
        "chunks": len(content.split('\n\n'))
    }

@celery_app.task(bind=True, name="tasks.workflow.index_content")
def index_content(self, prev_result: dict):
    """Index processed content in vector database."""
    vectors = create_embeddings(prev_result["content"])
    store_vectors(vectors, prev_result["project_id"])
    return {
        **prev_result,
        "indexed": True,
        "vector_count": len(vectors)
    }

@celery_app.task(bind=True, name="tasks.workflow.notify_completion")
def notify_completion(self, prev_result: dict):
    """Send notification when pipeline completes."""
    send_notification(
        project_id=prev_result["project_id"],
        message=f"File {prev_result['file_id']} processed: {prev_result['vector_count']} vectors"
    )
    return {"status": "complete", **prev_result}
```

---

## Periodic Tasks

### When to Use Celery Beat

| Use Celery Beat | Use Cron |
|-----------------|----------|
| Task needs Celery features (retries, results) | Simple script, no dependencies |
| Dynamic scheduling from app | Static schedule |
| Need monitoring with Flower | Log files sufficient |
| Task is part of Celery ecosystem | Standalone script |

### Step 1: Define Periodic Tasks

```python
# tasks/maintenance.py
from celery_app import celery_app
import asyncio
import logging

logger = logging.getLogger(__name__)

@celery_app.task(
    bind=True, 
    name="tasks.maintenance.cleanup_old_records",
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60}
)
def cleanup_old_records(self):
    """Clean up records older than 24 hours."""
    return asyncio.run(_cleanup_async())

async def _cleanup_async():
    from database import get_async_session_maker
    from idempotency import IdempotencyManager
    
    session_maker = get_async_session_maker()
    manager = IdempotencyManager(session_maker)
    
    deleted = await manager.cleanup_old_tasks(retention_seconds=86400)
    logger.info(f"Cleaned up {deleted} old task records")
    
    return {"deleted": deleted, "status": "complete"}

@celery_app.task(name="tasks.maintenance.health_check")
def health_check():
    """Simple health check task for monitoring."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

### Step 2: Configure Beat Schedule

```python
# celery_app.py - Add to your Celery configuration
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    # Run every hour
    "cleanup-hourly": {
        "task": "tasks.maintenance.cleanup_old_records",
        "schedule": 3600,  # Every 3600 seconds (1 hour)
        "args": ()
    },
    
    # Run every 5 minutes
    "health-check": {
        "task": "tasks.maintenance.health_check", 
        "schedule": 300,  # Every 5 minutes
    },
    
    # Run at specific time (cron-style)
    "daily-report": {
        "task": "tasks.reports.generate_daily_report",
        "schedule": crontab(hour=0, minute=0),  # Midnight UTC
    },
    
    # Run every Monday at 9am
    "weekly-digest": {
        "task": "tasks.email.send_weekly_digest",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),
    }
}

celery_app.conf.timezone = 'UTC'
```

### Schedule Reference

| Schedule | Syntax | Example |
|----------|--------|---------|
| Every N seconds | `N` | `60` (every minute) |
| Cron-style | `crontab(...)` | `crontab(hour=0)` (midnight) |
| Every N minutes | `crontab(minute='*/N')` | `crontab(minute='*/15')` |
| Specific days | `crontab(day_of_week='mon-fri')` | Weekdays only |

### Step 3: Run Celery Beat

```bash
# Terminal 1: Worker (executes tasks)
celery -A celery_app worker --loglevel=info

# Terminal 2: Beat scheduler (triggers tasks)
celery -A celery_app beat --loglevel=info

# Combined (development only - not recommended for production)
celery -A celery_app worker --beat --loglevel=info
```

### Production Deployment

```yaml
# docker-compose.yml
services:
  celery_worker:
    build: .
    command: celery -A celery_app worker -l info -c 4
    depends_on:
      - rabbitmq
      - redis
    restart: always
    
  celery_beat:
    build: .
    command: celery -A celery_app beat -l info
    depends_on:
      - rabbitmq
      - redis
    restart: always
    # IMPORTANT: Only run ONE beat instance!
```

> [!warning] Beat Singleton
> **Never run multiple Beat instances!** They will schedule duplicate tasks. In production, ensure only one Beat process runs (use a distributed lock or single container).

---

## Monitoring & Operations

### Flower Dashboard

**What:** Real-time web UI for monitoring Celery workers and tasks.

**When:** Production deployments, debugging task issues, monitoring queue health.

#### Installation & Setup

```bash
pip install flower
```

#### Running Flower

```bash
# Basic
celery -A celery_app flower --port=5555

# With authentication
celery -A celery_app flower --port=5555 --basic_auth=admin:secretpassword

# With config file
celery -A celery_app flower --conf=flowerconfig.py
```

#### Flower Configuration

```python
# flowerconfig.py
from dotenv import load_dotenv
import os

load_dotenv()

port = 5555
max_tasks = 10000
auto_refresh = True

# Authentication
basic_auth = [f"admin:{os.getenv('FLOWER_PASSWORD')}"]

# Persistent storage (optional)
# db = "flower.db"
```

#### What You Can Monitor

| Metric | Where | Why |
|--------|-------|-----|
| Active workers | Dashboard | Ensure workers are running |
| Queue lengths | Queues tab | Detect backlog |
| Task success/failure rates | Tasks tab | Spot problems |
| Worker memory/CPU | Workers tab | Resource issues |
| Task execution time | Task details | Performance tuning |

### Checking Task Status Programmatically

```python
from celery.result import AsyncResult

def get_task_status(task_id: str) -> dict:
    """Check status of a Celery task."""
    result = AsyncResult(task_id)
    
    return {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready(),
        "successful": result.successful() if result.ready() else None,
        "result": result.result if result.ready() else None,
        "traceback": result.traceback if result.failed() else None
    }

# Task states
# PENDING - Task not yet received by worker
# STARTED - Task started (requires task_track_started=True)
# RETRY   - Task is being retried
# FAILURE - Task raised exception
# SUCCESS - Task completed successfully
```

### HTTP Calls from Tasks

```python
import httpx
from celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(
    bind=True,
    name="tasks.api.call_external_service",
    autoretry_for=(httpx.RequestError, httpx.TimeoutException),
    max_retries=3,
    default_retry_delay=30
)
def call_external_service(self, endpoint: str, payload: dict):
    """Make HTTP call with automatic retries."""
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(endpoint, json=payload)
            response.raise_for_status()
            
            logger.info(f"API call successful: {endpoint}")
            return response.json()
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP {e.response.status_code}: {e}")
        if e.response.status_code >= 500:
            raise  # Retry on server errors
        return {"error": str(e), "status_code": e.response.status_code}
        
    except httpx.RequestError as e:
        logger.error(f"Request failed: {e}")
        raise  # Will trigger autoretry
```

### Using Results in Application Code

```python
# Synchronous wait (blocks)
result = my_task.delay(args)
data = result.get(timeout=30)  # Wait up to 30 seconds

# Async check (non-blocking)
result = my_task.delay(args)
if result.ready():
    data = result.result
else:
    print("Still processing...")

# In FastAPI endpoint
from celery.result import AsyncResult

@app.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    
    if not result.ready():
        return {"status": result.status, "message": "Still processing"}
    
    if result.failed():
        return {"status": "failed", "error": str(result.result)}
    
    return {"status": "success", "result": result.result}
```

---

## Troubleshooting

### Common Issues & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| Tasks stuck in PENDING | Worker not running | Start worker: `celery -A app worker` |
| Tasks executed twice | No idempotency | Implement IdempotencyManager |
| Worker crashes on async code | No event loop bridge | Use `asyncio.run()` + `nest_asyncio` |
| Results not stored | No backend configured | Add `backend=` to Celery config |
| Task timeout | `task_time_limit` too low | Increase limit or optimize task |
| Memory leak in workers | Resources not cleaned | Use `finally` blocks, call `gc.collect()` |

### Exception Handling Best Practices

```python
@celery_app.task(bind=True, name="tasks.example.robust_task")
def robust_task(self, data):
    """Template for robust task with proper error handling."""
    
    resources = None
    
    try:
        # Initialize resources
        resources = acquire_resources()
        
        # Do work
        result = process(data)
        
        return {"status": "success", "result": result}
        
    except SoftTimeLimitExceeded:
        # Task took too long - don't retry
        self.update_state(
            state="FAILURE",
            meta={"error": "Task exceeded time limit"}
        )
        raise
        
    except RecoverableError as e:
        # Transient error - retry makes sense
        logger.warning(f"Recoverable error, will retry: {e}")
        raise  # Let autoretry handle it
        
    except PermanentError as e:
        # Won't recover by retrying
        self.update_state(
            state="FAILURE",
            meta={"error": str(e), "type": "permanent"}
        )
        return {"status": "failed", "error": str(e)}
        
    except Exception as e:
        # Unexpected error
        logger.exception(f"Unexpected error in task: {e}")
        raise
        
    finally:
        # ALWAYS clean up resources
        if resources:
            try:
                release_resources(resources)
            except Exception as cleanup_error:
                logger.error(f"Cleanup failed: {cleanup_error}")
```

### Debugging Tips

```bash
# Run worker with verbose logging
celery -A celery_app worker --loglevel=debug

# Inspect active tasks
celery -A celery_app inspect active

# Inspect reserved tasks (prefetched)
celery -A celery_app inspect reserved

# Inspect registered tasks
celery -A celery_app inspect registered

# Purge all pending tasks (DANGEROUS)
celery -A celery_app purge

# Check broker connection
celery -A celery_app inspect ping
```

---

## Quick Reference

### Commands Cheat Sheet

```bash
# Start worker
celery -A celery_app worker --loglevel=info

# Start beat scheduler
celery -A celery_app beat --loglevel=info

# Start Flower monitoring
celery -A celery_app flower --port=5555

# Inspect workers
celery -A celery_app inspect active
celery -A celery_app inspect stats

# Control workers
celery -A celery_app control shutdown  # Graceful shutdown
```

### Task Dispatch Methods

```python
# Fire and forget
task.delay(arg1, arg2)

# With options
task.apply_async(
    args=[arg1, arg2],
    kwargs={"key": "value"},
    countdown=60,          # Delay execution by 60 seconds
    eta=datetime(2024, 1, 1, 12, 0),  # Run at specific time
    expires=3600,          # Expire if not executed within 1 hour
    queue="high_priority"  # Send to specific queue
)

# Get result
result = task.delay(args)
result.get(timeout=30)     # Wait for result (blocking)
result.ready()             # Check if done (non-blocking)
result.status              # Current status
result.result              # Result value (if ready)
```

### Best Practices Summary

1. **Always use `acks_late=True`** for important tasks
2. **Implement idempotency** for tasks that modify data
3. **Set time limits** to prevent stuck tasks
4. **Use `bind=True`** for access to retries and task ID
5. **Never pass large payloads** - use file paths/URLs
6. **Clean up resources** in `finally` blocks
7. **Log task progress** for debugging
8. **Monitor with Flower** in production
9. **Run only ONE Beat instance**
10. **Use queues** to separate different task types

---

## See Also

- [[RabbitMQ Configuration]]
- [[Redis Configuration]]
- [[FastAPI Integration]]
- [[Database Models]]
- [[Async Programming]]

---

*Last updated: 2026-03-26*
