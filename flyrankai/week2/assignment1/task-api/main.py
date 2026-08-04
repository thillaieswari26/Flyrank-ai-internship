from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0"
)

# In-memory task list
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push to GitHub",
        "done": True
    }
]
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool
# Root endpoint
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Get a single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)
    return new_task
# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if not updated_task.title.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Title cannot be empty"
                )

            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Delete a task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )