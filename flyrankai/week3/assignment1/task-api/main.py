from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv

from service import TaskService

load_dotenv()

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0"
)

service = TaskService()


# -------------------------
# Request models
# -------------------------

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


# -------------------------
# Root endpoint
# -------------------------

@app.get("/", summary="API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# -------------------------
# Health check
# -------------------------

@app.get("/health", summary="Health check")
def health():
    return {
        "status": "ok"
    }


# -------------------------
# Get all tasks
# -------------------------

@app.get("/tasks", summary="Get all tasks")
def get_tasks():
    return service.get_tasks()


# -------------------------
# Get single task
# -------------------------

@app.get("/tasks/{task_id}", summary="Get task by ID")
def get_task(task_id: int):
    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


# -------------------------
# Create task
# -------------------------

@app.post(
    "/tasks",
    summary="Create a new task",
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    return service.create_task(task.title)


# -------------------------
# Update task
# -------------------------

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, updated_task: TaskUpdate):

    if not updated_task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    task = service.update_task(
        task_id,
        updated_task.title,
        updated_task.done
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


# -------------------------
# Delete task
# -------------------------

@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return