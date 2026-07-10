# Celery Overview

## What is Celery?

Celery is a **distributed task queue** that enables running **time-consuming or scheduled tasks in the background**, separate from your main web application (e.g., FastAPI, Django, Flask).

## When to Use Celery?

Use Celery when you need to:
- **Send emails** after user actions (e.g., signup confirmation).
- **Process large datasets** (e.g., training ML models, generating reports).
- **Queue tasks** (e.g., resizing uploaded images).
- **Schedule tasks** (e.g., nightly database cleanup, periodic retraining).

### Why Use Celery?

Running heavy tasks within an API request causes delays for users. Celery **delegates** these tasks to run asynchronously, allowing the API to respond instantly.

## How Celery Works (High-Level)

1. **FastAPI App**: Initiates a task by telling Celery to run it.
2. **Message Broker** (e.g., Redis, RabbitMQ): Stores tasks in a queue.
3. **Celery Worker(s)**: Pick up tasks from the queue and execute them in the background.
4. **Result Backend** (optional): Stores task results for later retrieval.

**Key Idea**: Celery acts as a **background worker system** for:
- Long-running tasks
- Asynchronous tasks
- Tasks that should not block user requests

## Celery Terminology
- **Task**: A Python function you want to run later.
- **Producer**: Code (often your web app) that queues tasks.
- **Broker**: Message queue system (e.g., Redis, RabbitMQ) that holds tasks.
- **Worker**: A process that pulls tasks from the broker and executes them.
- **Result Backend**: Optional storage for task return values or tracebacks.
- **Beat**: Celery’s built-in scheduler for periodic tasks.

## Choosing a Message Broker

### Redis
- **Characteristics**:
    - Pure in-memory, single-digit millisecond latency, handles 100K+ messages/second without tuning.
    - Ideal for **chat-like, fire-and-forget tasks**.
- **When to Choose**:
    - Already using Redis for caching/sessions (reduces service overhead).
    - Tasks are small and quick (e.g., emails, thumbnails).
    - Occasional duplicate or lost tasks are tolerable, or your code is idempotent.

### RabbitMQ

- **Characteristics**:
    - Adds protocol overhead but handles tens of thousands of messages/second.
    - Streams large payloads to disk (better than Redis’ RAM buffering for big messages).
- **When to Choose**:
    - **Exactly-once** or **at-least-once** delivery (no duplicates) is critical.
    - Need complex routing, priorities, or delayed tasks.
    - Queues may grow large or carry big messages.
    - You’re okay managing an additional service (or using managed RabbitMQ).

late acknowledge -> means that the worker may be working on it already but appearing to be free!!!

```env
#===========================Celery Task Queue Config========================
CELERY_BROKER_URL = "amqp://minirag_user:admin@localhost:5672/minirag_vhost"
CELERY_RESULT_BACKEND = "redis://:minirag_redis@localhost:6379/0"
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 600
CELERY_TASK_ACKS_LATE = false #after task is executed , acknowledge it late
CELERY_WORKER_CONCURRENCY=2
```

/celery
```python
from celery import Celery

#Create Celery Application Instance
celery_app = Celery(
    "minirag",
    broker = settings.CELERY_BROKER_URL,
    backend = settings.CELERY_RESULT_BACKEND,
    include = [
        "tasks.file_processing",
        "tasks.mail_service"
    ]
)
celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=[
        settings.CELERY_TASK_SERIALIZER
    ],

    # Task safety - Late acknowledgment prevents task loss on worker crash
    task_acks_late=settings.CELERY_TASK_ACKS_LATE,

    # Time limits - Prevent hanging tasks
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,

    # Result backend - Store results for status tracking
    task_ignore_result=False,
    result_expires=3600,

    # Worker settings
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,

    # Connection settings for better reliability
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    worker_cancel_long_running_tasks_on_connection_loss=True,

    task_routes={
        "tasks.file_processing.process_project_files": {"queue": "file_processing"},
        "tasks.mail_service.send_email_reports": {"queue": "default"}
    }
)

celery_app.conf.task_default_queue = "default"
```

#### Making small task
Task:
/tasks
each task in a python file
```python
from celery_app import celery_app
from helpers.config import get_settings,Settings
import logging
from time import sleep
from datetime import datetime
import asyncio

logger = logging.getLogger("celery.task")

@celery_app.task(bind = True,name = "tasks.mail_service.send_email_reports")
def send_email_reports(self,mail_wait_seconds:int):
    return asyncio.run(_send_email_reports(self,mail_wait_seconds))

async def _send_email_reports(task_instance,mail_wait_seconds:int):
    started_at = str(datetime.now())

    task_instance.update_state(
        state = "PROGRESS",
        meta = {
            "started_at": started_at,
        }
    )

    for ix in range(15):
        logger.info(f"Send email to user:{ix}")
        await asyncio.sleep(mail_wait_seconds)

    return {
        "no_emails":15,
        "end_at" : str(datetime.now()),
    }
```

#### FASTAPI Route:
```python
@base_router.get("/send_reports")
async def send_reports(app_settings:Settings = Depends(get_settings)):
    task = send_email_reports.delay(mail_wait_seconds = 5)

    return {
        "success":True,
        "task_id": task.id
    }
```

- Any exceptions please use try and except and finally (also raise exceptions)
- Have to close the db engine after closes
#### Exceptions:
```python
task_instance.update_state(
                    state = "FAILURE",
                    meta = { "signal":ResponseSignal.NO_FILES_ERROR.value,
	}
)

raise Exception(f"No assets for file: {file_id}")
```
#### Closing tasks:
```python
except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise
finally:
	try:
		if db_engine:
			await db_engine.dispose()
		if vectordb_client:
			await vectordb_client.disconnect()
	except Exception as e:
		logger.error(f"Task failed while cleaning: {str(e)}")
```

#### Flower : Monitoring Celery
```python
pip install flower

#in terminal
python -m celery -A celery_app flower --port=5555
```

can make a config for flower
```python
from dotenv import dotenv_values
config = dotenv_values(".env")

#flower config
port = 5555
max_tasks = 10000
auto_refresh = True
#db = "flower.db" #sqlite db for persistent storage

basic_auth = [f"admin:{config['CELERY_FLOWER_PASSWORD']}"]
```

```terminal
python -m celery -A celery_app flower --conf=flowerconfig.py
```

#### Workflow 
We want to make a workflow containing more than one task each one after the other in correct order
```python
@celery_app.task(
                 bind=True, name="tasks.process_workflow.process_and_push_workflow",
                 autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 3, 'countdown': 60}
                )
def process_and_push_workflow(  self, project_id: int, 
                                file_id: int, chunk_size: int,
                                overlap_size: int, do_reset: int):

    workflow = chain(
        process_project_files.s(project_id, file_id, chunk_size, overlap_size, do_reset),
        push_after_process_task.s()
    )

    result = workflow.apply_async()

    return {
        "signal": "WORKFLOW_STARTED",
        "workflow_id": result.id,
        "tasks": ["tasks.file_processing.process_project_files", 
                  "tasks.data_indexing.index_data_content"]
    }
```
we use chain instead of task here, the first task takes the same input , the next task takes the result from the task but the input of the task has to be in the result of the previous task 

```python
@celery_app.task(
                 bind=True, name="tasks.process_workflow.push_after_process_task",
                 autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 3, 'countdown': 60}
                )
def push_after_process_task(self, prev_task_result):

    project_id = prev_task_result.get("project_id")
    do_reset = prev_task_result.get("do_reset")

    task_results = asyncio.run(
        _index_data_content(self, project_id, do_reset)
    )

    return {
        "project_id": project_id,
        "do_reset": do_reset,
        "task_results": task_results
    }
```

#### Idempotency Manager
Scheme:
```python
from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Index
import uuid

class CeleryTaskExecution(SQLAlchemyBase):

    __tablename__ = "celery_task_executions"

    execution_id = Column(Integer, primary_key=True, autoincrement=True)

    task_name = Column(String(255), nullable=False)
    task_args_hash = Column(String(64), nullable=False)  # SHA-256 hash of task arguments
    celery_task_id = Column(UUID(as_uuid=True), nullable=True)

    status = Column(String(20), nullable=False, default='PENDING')

    task_args = Column(JSONB, nullable=True)
    result = Column(JSONB, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __table_args__ = (
        Index('ixz_task_name_args_celery_hash', task_name, task_args_hash, celery_task_id, unique=True),
        Index('ixz_task_execution_status', status),
        Index('ixz_task_execution_created_at', created_at),
        Index('ixz_celery_task_id', celery_task_id),
    )
```

#### Manager:
We want to make a db table to store which worker is working on which task so that if some worker has a certain task other workers cant interfer with that worker's work so we use md5 hash so that not everytime we have a new task I have to compare the parameters one by one.
The md5 hash gives u the ability to compare the parameters easily.
```python
import hashlib
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from models.db_schemas.minirag.schemes.celery_task_execution import CeleryTaskExecution

class IdempotencyManager:
    def __init__(self, db_client, db_engine):
        self.db_client = db_client
        self.db_engine = db_engine

    def create_args_hash(self, task_name: str, task_args: dict):
        combined_data = {
            **task_args,
            "task_name": task_name
        }
        json_string = json.dumps(combined_data, sort_keys=True, default=str)
        return hashlib.sha256(json_string.encode()).hexdigest()
    
    async def create_task_record(self, task_name: str, task_args: dict, celery_task_id: str = None) -> CeleryTaskExecution:
        """Create new task execution record."""
        args_hash = self.create_args_hash(task_name, task_args)
        
        task_record = CeleryTaskExecution(
            task_name=task_name,
            task_args_hash=args_hash,
            task_args=task_args,
            celery_task_id=celery_task_id,
            status='PENDING',
            started_at=datetime.utcnow()
        )
        
        session = self.db_client()
        try:
            session.add(task_record)
            await session.commit()
            await session.refresh(task_record)
            return task_record
        finally:
            await session.close()

    async def update_task_status(self, execution_id: int, status: str, result: dict = None):
        """Update task status and result."""
        session = self.db_client()
        try:
            task_record = await session.get(CeleryTaskExecution, execution_id)
            if task_record:
                task_record.status = status
                if result:
                    task_record.result = result
                if status in ['SUCCESS', 'FAILURE']:
                    task_record.completed_at = datetime.utcnow()
                await session.commit()
        finally:
            await session.close()

    async def get_existing_task(self, task_name: str, 
                                task_args: dict, celery_task_id: str) -> CeleryTaskExecution:
        """Check if task with same name and args already exists."""
        args_hash = self.create_args_hash(task_name, task_args)
        
        session = self.db_client()
        try:
            stmt = select(CeleryTaskExecution).where(
                CeleryTaskExecution.celery_task_id == celery_task_id,
                CeleryTaskExecution.task_name == task_name,
                CeleryTaskExecution.task_args_hash == args_hash
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        finally:
            await session.close()

    async def should_execute_task(self, task_name: str, task_args: dict,
                                  celery_task_id: str, 
                                  task_time_limit: int = 600) -> tuple[bool, CeleryTaskExecution]:
        """
        Check if task should be executed or return existing result.
        Args:
            task_time_limit: Time limit in seconds after which a stuck task can be re-executed
        Returns (should_execute, existing_task_or_none)
        """
        existing_task = await self.get_existing_task(task_name, task_args, celery_task_id)
        
        if not existing_task:
            return True, None
            
        # Don't execute if task is already completed successfully
        if existing_task.status == 'SUCCESS':
            return False, existing_task
            
        # Check if task is stuck (running longer than time limit + 60 seconds)
        if existing_task.status in ['PENDING', 'STARTED', 'RETRY']:
            if existing_task.started_at:
                time_elapsed = (datetime.utcnow() - existing_task.started_at).total_seconds()
                time_gap = 60  # 60 seconds grace period
                if time_elapsed > (task_time_limit + time_gap):
                    return True, existing_task  # Task is stuck, allow re-execution
            return False, existing_task  # Task is still running within time limit
            
        # Re-execute if previous task failed
        return True, existing_task
    
    async def cleanup_old_tasks(self, time_retention: int = 86400) -> int:
        """
        Delete old task records older than time_retention seconds.
        Args:
            time_retention: Time in seconds to retain tasks (default: 86400 = 24 hours)
        Returns:
            Number of deleted records
        """
        cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=time_retention)
        
        session = self.db_client()
        try:
            stmt = delete(CeleryTaskExecution).where(
                CeleryTaskExecution.created_at < cutoff_time
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount
        finally:
            await session.close()
```

#### Maintenance
```python
from celery_app import celery_app, get_setup_utils
from helpers.config import get_settings
import asyncio
from utils.idempotency_manager import IdempotencyManager

import logging
logger = logging.getLogger(__name__)

@celery_app.task(
                 bind=True, name="tasks.maintenance.clean_celery_executions_table",
                 autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 3, 'countdown': 60}
                )
def clean_celery_executions_table(self):

    return asyncio.run(
        _clean_celery_executions_table(self)
    )

async def _clean_celery_executions_table(task_instance):

    db_engine, vectordb_client = None, None
    
    try:

        (db_engine, db_client, llm_provider_factory, 
        vectordb_provider_factory,
        generation_client, embedding_client,
        vectordb_client, template_parser) = await get_setup_utils()

        # Create idempotency manager
        idempotency_manager = IdempotencyManager(db_client, db_engine)

        logger.warning(f"cleaning !!!")
        _ = await idempotency_manager.cleanup_old_tasks(5)

        return True

    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise
    finally:
        try:
            if db_engine:
                await db_engine.dispose()
            
            if vectordb_client:
                await vectordb_client.disconnect()
        except Exception as e:
            logger.error(f"Task failed while cleaning: {str(e)}")
```
add the beat schedule in the celery_app (where schedule here is in seconds)
```python
beat_schedule = {
        "cleanup-old-task-records":{
            "task":"tasks.maintenance.clean_celery_executions_table",
            "schedule":10,
            "args":()
        }
    },

    timezone='UTC',
```
----
#### API Endpoints in Celery
```python
@celery_app.task(bind = True, name = "tasks.check_complaint_by_id")
def check_complaint_by_id(self,complaint_id:str):
    return asyncio.run(_check_complaint_by_id(self,complaint_id))

async def _check_complaint_by_id(self,complaint_id:str):
    url = f"{settings.API_BASE_URL}/complaints/check_by_id/{complaint_id}"
    max_retries = settings.CELERY_MAX_RETRIES
    retry_delay = settings.CELERY_RETRY_DELAY

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout = 10.0)
                response.raise_for_status()

                data = response.json()
                logger.info(f"Successfully checked complaint ID {complaint_id}: {data}")
                return data
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.error(f"Attempt {attempt + 1} failed for complaint ID {complaint_id}: {exc}")
            if attempt < max_retries - 1:
                sleep(retry_delay)
            else:
                logger.error(f"All {max_retries} attempts failed for complaint ID {complaint_id}.")
                raise
```

##### How to use the task:
```python
@tool
@traceable
def check_complaint_status(runtime: ToolRuntime[Context]) -> str:
    """Check the status of an existing complaint."""
    ctx = runtime.context
    if not ctx.complaint_id:
        ctx.complaint_id = input("Enter your Complaint ID: ").strip() or "CMP123"

    if CELERY_AVAILABLE:
        try:
            result = check_complaint_by_id.delay(ctx.complaint_id)
            data = result.get(timeout=10)
            
            if data.get("exists"):
                return f"📝 **Complaint Details:**\n" \
                       f"Complaint ID: {data['complaint_id']}\n" \
                       f"Issue: {data['issue']}\n" \
                       f"Escalation Status: {data['escalation_status']}"
            else:
                return f"❌ Complaint {ctx.complaint_id} not found in the system."
        except Exception as e:
            return f"⚠️ Error checking complaint via Celery: {e}"
    else:
        # Fallback to direct API call
        try:
            url = f"{API_BASE_URL}/complaints/check_by_id/{ctx.complaint_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return f"📝 Complaint Details: {response.json()}"
            return f"Complaint not found (Status: {response.status_code})"
        except Exception as e:
            return f"Error connecting to complaint system: {e}"
```
###### Here
```python
result = check_complaint_by_id.delay(ctx.complaint_id)
data = result.get(timeout=10)
```