from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    return projects


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            return project

    raise HTTPException(status_code=404, detail="Project not found")


@app.post("/projects")
def create_project(project: ProjectCreate):
    new_project = {
        "id": len(projects) + 1,
        "name": project.name
    }

    projects.append(new_project)

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