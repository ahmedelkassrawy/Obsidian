Here is a clean, structured Markdown guide that you can save and reference whenever you need to create a new Celery task using your asynchronous idempotency setup.

---

# Creating Async-Aware Celery Tasks with Idempotency

When building a system with FastAPI (which is natively asynchronous) and Celery (which relies on synchronous worker processes), you need a bridge between the two. This is especially true when your database operations and tools, like `IdempotencyManager`, rely on `async`/`await`.

This guide outlines the standard pattern for executing async logic safely within a synchronous Celery task while ensuring no duplicate work is performed.

---

## 1. The Celery Task Implementation

Create your task definition in your designated tasks file (e.g., `backend/tasks/data_uploading.py`).

Because Celery workers execute functions synchronously, you must use `asyncio.run()` to execute your asynchronous core logic.

Python

```
import asyncio
from celery import shared_task

# Import your session maker and idempotency manager
from database.database import get_async_session_maker
from idempotency_manager import IdempotencyManager

# Initialize dependencies globally for the worker process
session_maker = get_async_session_maker()
idempotency_manager = IdempotencyManager(session_maker)


async def async_upload_file_logic(file_name: str, filetype: str, celery_task_id: str):
    """The asynchronous core logic for the task."""
    task_name = "upload_file_task"
    task_args = {"file_name": file_name, "filetype": filetype} # The unique arguments used for hashing

    # 1. Check Execution Status
    should_execute, existing_task = await idempotency_manager.should_execute_task(
        task_name=task_name,
        task_args=task_args,
        celery_task_id=celery_task_id
    )

    if not should_execute:
        # Task was already completed successfully or is currently running
        return existing_task.result if existing_task else {"status": "skipped"}

    # 2. Claim the Execution (Handles race conditions)
    if not existing_task:
        task_record = await idempotency_manager.create_task_record(
            task_name=task_name, 
            task_args=task_args, 
            celery_task_id=celery_task_id
        )
    else:
        task_record = existing_task

    # 3. Update Status to IN_PROGRESS
    await idempotency_manager.update_task_status(task_record.id, "IN_PROGRESS")

    try:
        # -----------------------------------------
        # EXECTUTE LONG-RUNNING WORK HERE
        # e.g., parsing the file and saving to DB
        await asyncio.sleep(5)  # Simulated work
        # -----------------------------------------
        
        result_data = {"status": "success", "processed_file": file_name}
        
        # 4. Mark as SUCCESS
        await idempotency_manager.update_task_status(
            task_record.id, 
            "SUCCESS", 
            result=result_data
        )
        return result_data

    except Exception as e:
        # 5. Mark as FAILURE on crash
        await idempotency_manager.update_task_status(
            task_record.id, 
            "FAILURE", 
            result={"error": str(e)}
        )
        raise


# The actual Celery task definition (Synchronous wrapper)
@shared_task(bind=True, name="tasks.upload_service.upload_file_task")
def upload_file_task(self, file_name: str, filetype: str):
    """
    Synchronous entry point for Celery. 
    Passes the unique request ID and runs the async event loop.
    """
    celery_task_id = self.request.id 
    return asyncio.run(async_upload_file_logic(file_name, filetype, celery_task_id))
```

---

## 2. Dispatching the Task from the API

In your API routes (e.g., `api.py`), you can dispatch the task to Celery. Because the idempotency logic handles deduplication on the worker side, your API simply needs to queue the task and return a response to the user.

Python

```
from fastapi import APIRouter, UploadFile, HTTPException
from backend.tasks.data_uploading import upload_file_task

app = APIRouter()

@app.post("/upload")
async def upload_file(file: UploadFile):
    valid_types = [
        "application/pdf", 
        "text/csv", 
        "text/plain", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    if file.content_type not in valid_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_name = file.filename.lower()
    filetype = file.content_type.split("/")[-1]

    # BEST PRACTICE NOTE: 
    # Save the file contents to S3, a temporary folder, or pass a pre-signed URL 
    # to the Celery task. Passing large byte streams directly as Celery task arguments 
    # is an anti-pattern and can crash your message broker (e.g., Redis/RabbitMQ).
    
    # Fire and forget the task
    task = upload_file_task.delay(file_name, filetype)
    
    return {"message": "Upload queued successfully", "task_id": task.id}
```

---

## 3. Key Takeaways & Design Patterns

- **The Async Wrapper:** Because the database session (`get_async_session_maker`) and `IdempotencyManager` use `async`/`await`, you must encapsulate your actual logic in an `async def` function and run it inside the Celery `@shared_task` using `asyncio.run()`.
    
- **Early Deduplication:** Always call `should_execute_task` first. It hashes the `task_args` to ensure that if a user double-clicks an upload button, the second worker immediately skips the duplicate work.
    
- **Graceful State Management:** Always wrap your actual heavy lifting in a `try...except` block. This ensures that if the process fails, the database record is cleanly updated to `FAILURE`, allowing for future retries without leaving the task perpetually stuck in `IN_PROGRESS`.
    

---

Would you like me to show you how to write a mock test for this task to verify that the idempotency logic correctly catches duplicate submissions?