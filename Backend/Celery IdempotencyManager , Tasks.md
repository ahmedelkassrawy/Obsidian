```python
import hashlib
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from database.models import CeleryTaskExecution
from backend.database.db import async_session_maker

db = async_session_maker()

class IdempotencyManager:
    def __init__(self):
        self.db = db

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

### 1. The "Race Condition" Flaw

Your current `should_execute_task` logic follows a **Check-then-Act** pattern:
1. Query the DB (Check).
2. If `True`, proceed to create a record or run the task (Act).

In a distributed system, two workers can pick up the same task at the exact same millisecond. Both will see `existing_task = None`, and both will proceed to execute the task.

**The Fix:** Use a **Unique Constraint** on `task_args_hash` (and potentially `celery_task_id`) in your database schema. Use an "Upsert" or a `try-except` on the initial insert to guarantee that only one worker can ever claim the "Running" state for a specific hash.

### 2. Dependency on `celery_task_id`

In `get_existing_task`, you filter by `CeleryTaskExecution.celery_task_id == celery_task_id`.

- **The Problem:** If a task is retried by Celery (due to `autoretry_for`), the `celery_task_id` **remains the same**.
    
- **The Problem:** If a user submits the same file twice (creating two different requests), they will have **different** `celery_task_ids`.
    
- **The Result:** Your idempotency check will fail to catch a user double-clicking "Upload" because the IDs don't match, even though the `task_args_hash` is identical.

**The Fix:** Rely primarily on the `task_args_hash`. The `celery_task_id` should be metadata, not a primary lookup key for idempotency.

### 3. Sync vs. Async Mismatch

You are using `async_session_maker` and `await session.close()`.
- **The Context:** Celery workers are synchronous by default (Prefork pool).
    
- **The Risk:** If you run this inside a standard `@app.task`, you will get `Coroutine was never awaited` errors or `Greenlet` errors unless you carefully wrap everything in `asyncio.run()` or use `asgiref.sync.async_to_sync`.

### Summary of Corrections Needed:
1. **Unique Constraint:** Add `unique=True` to `task_args_hash` in your model.
2. **Remove `celery_task_id` from Lookup:** Look up by the hash of the arguments only.
3. **Atomic "Claim":** The moment you check if a task should run, you should mark it as `STARTED` in the same transaction to prevent other workers from grabbing it.

4. **Timeouts:** Your logic for "stuck" tasks is good—just ensure the `started_at` is updated if a task is "re-claimed."
----
Currently, your unique index includes `celery_task_id`. As we discussed, if a user sends the same file twice (creating two different `celery_task_id`s), the unique constraint won't trigger, and you'll process the same data twice.
```python
class CeleryTaskExecution(Base):
    __tablename__ = "celery_task_executions"

    execution_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=False)
    
    # This is your "Idempotency Key"
    task_args_hash = Column(String(64), nullable=False) 
    
    celery_task_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String(20), nullable=False, default='PENDING')
    
    task_args = Column(JSONB, nullable=True)
    result = Column(JSONB, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __table_args__ = (
        # CRITICAL: Unique constraint on name + hash only.
        # This prevents the same logical work from being done twice, 
        # even if it has a different Celery Task ID.
        Index('uix_task_name_args_hash', task_name, task_args_hash, unique=True),
        
        Index('ix_task_execution_status', status),
        Index('ix_celery_task_id', celery_task_id),
    )
```
---
```python
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.celery_app import celery_app
from config import get_settings
import logging
import asyncio
import gc
import base64
from celery.exceptions import SoftTimeLimitExceeded
from backend.ai.ingestion import process_documents_langchain, invalidate_user_bm25
from backend.database.db import get_task_session
from backend.idempotency_manager import IdempotencyManager
from backend.database.models import Document, CeleryTaskExecution
from sqlalchemy import select
import uuid
import nest_asyncio
nest_asyncio.apply()  # ✅ Allows nested event loops

settings = get_settings()

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="tasks.upload_service.upload_file_task",
                acks_late = True, #ensure task isnt lost if worker dies
                autoretry_for=(Exception,),
                dont_autoretry_for=(SoftTimeLimitExceeded,),
                max_retries=3, default_retry_delay=30)
def upload_file_task(self, file_b64, file_name, file_type, user_id):
    """Process file upload. file_b64 contains base64-encoded file data."""

    #check/lock task
    async def process():
        file_bytes = base64.b64decode(file_b64)
        logger.info(f"Processing {len(file_bytes)} bytes for file {file_name}")
        
        async with get_task_session() as session_maker:
            manager = IdempotencyManager(session_maker)
            task_args = {
                "file_name": file_name,
                "file_type": file_type,
                "user_id": user_id,
            }

            should_run, task_record = await manager.should_execute_task(
                task_name=self.name,
                task_args=task_args,
                celery_task_id=self.request.id
            )

            if not should_run:
                # Verify the document still exists in the database
                doc_id_str = task_record.result.get('document_id')
                if doc_id_str:
                    async with session_maker() as db:
                        doc_exists = await db.get(Document, uuid.UUID(doc_id_str))
                        if not doc_exists:
                            logger.warning(f"Cached document {doc_id_str} no longer exists. Reprocessing file.")
                            should_run = True
                        else:
                            logger.info(f"Task with same args already executed. Returning existing result for user {user_id} and file {file_name}")
                            return task_record.result
                
                # If no document_id in result, something's wrong - reprocess
                if not doc_id_str:
                    logger.warning(f"Cached result missing document_id. Reprocessing file.")
                    should_run = True

            # Create new task record if it doesn't exist, or update existing if reprocessing
            if task_record is None:
                task_record = await manager.create_task_record(
                    task_name=self.name,
                    task_args=task_args,
                    celery_task_id=self.request.id
                )
            elif should_run:
                # Update existing record with new celery_task_id if reprocessing
                async with session_maker() as db:
                    existing = await db.get(CeleryTaskExecution, task_record.execution_id)
                    if existing:
                        existing.celery_task_id = self.request.id
                        existing.status = 'IN_PROGRESS'
                        await db.commit()
                        await db.refresh(existing)
                        task_record = existing

            # Mark task as in progress (for new tasks only)
            if task_record and task_record.status != 'IN_PROGRESS':
                await manager.update_task_status(task_record.execution_id, "IN_PROGRESS")

            try:
                # Process the document in its own session block
                async with session_maker() as db:
                    new_id = await process_documents_langchain(
                        db=db,
                        file_bytes=file_bytes,
                        file_name=file_name,
                        file_type=file_type,
                        user_id=user_id,
                    )
                
                # Invalidate cache after db session is closed
                await invalidate_user_bm25(user_id)
                
                # Update status after all db operations are done
                await manager.update_task_status(task_record.execution_id, "SUCCESS", 
                                                 result={"document_id": str(new_id)})
                
                return {"document_id": str(new_id), "status": "success"}
            except SoftTimeLimitExceeded:
                logger.error(f"Task timed out processing file {file_name} for user {user_id}")
                await manager.update_task_status(task_record.execution_id, "FAILURE",
                                               result={"error": "Task exceeded soft time limit"})
                raise
            except Exception as e:
                logger.error(f"Error processing file {file_name} for user {user_id}: {str(e)}")
                await manager.update_task_status(task_record.execution_id, "FAILURE", 
                                               result={"error": str(e)})
                raise e
            finally:
                # Trigger garbage collection to clean up memory
                gc.collect()
                logger.debug(f"Memory cleanup completed for task {self.request.id}")

    result = asyncio.run(process())
    return result
```

### Summary of Improvements

1. **Strict Uniqueness:** By removing `celery_task_id` from the unique index, you ensure that if two different requests try to process the same file hash, the database will block the second one.
    
2. **Acks Late + Status:** Because `acks_late=True`, if the worker crashes during `process_documents`, the task remains in the queue. When it restarts, your `IdempotencyManager` will see the status is `STARTED` and use your `task_time_limit` logic to decide whether to resume it.
    
3. **Audit Trail:** The `CeleryTaskExecution` table now serves as a reliable log for your LLM/Document processing pipeline.