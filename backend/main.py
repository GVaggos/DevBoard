from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Base, engine, SessionLocal
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


# --------------------
# DATA
# --------------------

projects = [
    {"id": 1, "name": "DevBoard"},
    {"id": 2, "name": "Test Project"}
]

tasks = []


# --------------------
# MODELS
# --------------------

class ProjectCreate(BaseModel):
    name: str


class ProjectUpdate(BaseModel):
    name: str


class TaskCreate(BaseModel):
    title: str
    project_id: int
    status: str = "todo"
    priority: str = "medium"

class TaskUpdate(BaseModel):
    title: str
    status: str
    priority: str


# --------------------
# HOME
# --------------------

@app.get("/")
def home():
    return {"message": "DevBoard backend is running"}


# --------------------
# PROJECTS
# --------------------

@app.get("/projects")
def get_projects():
    db = SessionLocal()

    projects = db.query(models.Project).all()

    db.close()

    return projects

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    db.close()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@app.post("/projects")
def create_project(project: ProjectCreate):
    db = SessionLocal()

    new_project = models.Project(name=project.name)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    db.close()

    return new_project


@app.put("/projects/{project_id}")
def update_project(project_id: int, updated_project: ProjectUpdate):
    for project in projects:
        if project["id"] == project_id:
            project["name"] = updated_project.name
            return project

    raise HTTPException(status_code=404, detail="Project not found")


@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            projects.remove(project)
            return {"message": "Project deleted successfully"}

    raise HTTPException(status_code=404, detail="Project not found")

@app.post("/tasks")
def create_task(task: TaskCreate):
    project_exists = any(
        project["id"] == task.project_id
        for project in projects
    )

    if not project_exists:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "project_id": task.project_id,
        "status": task.status,
        "priority": task.priority
    }

    tasks.append(new_task)

    return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/projects/{project_id}/tasks")
def get_project_tasks(project_id: int):
    project_exists = any(
        project["id"] == project_id
        for project in projects
    )

    if not project_exists:
        raise HTTPException(status_code=404, detail="Project not found")

    project_tasks = [
        task for task in tasks
        if task["project_id"] == project_id
    ]

    return project_tasks


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["status"] = updated_task.status
            task["priority"] = updated_task.priority

            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")