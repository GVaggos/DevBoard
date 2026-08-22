from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Base, engine, SessionLocal
import models
from pwdlib import PasswordHash 

Base.metadata.create_all(bind=engine)

app = FastAPI()

password_hash = PasswordHash.recommended()


# --------------------





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

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


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
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = updated_project.name

    db.commit()
    db.refresh(project)

    db.close()

    return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    db.close()

    return {"message": "Project deleted successfully"}

@app.post("/tasks")
def create_task(task: TaskCreate):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = models.Task(
        title=task.title,
        project_id=task.project_id,
        status=task.status,
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    db.close()

    return new_task


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    db = SessionLocal()

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    db.close()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.get("/projects/{project_id}/tasks")
def get_project_tasks(project_id: int):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    project_tasks = db.query(models.Task).filter(
        models.Task.project_id == project_id
    ).all()

    db.close()

    return project_tasks


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    db = SessionLocal()

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.status = updated_task.status
    task.priority = updated_task.priority

    db.commit()
    db.refresh(task)

    db.close()

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    db.close()

    return {"message": "Task deleted successfully"}


@app.post("/register")
def register_user(user: UserCreate):
    db = SessionLocal()

    existing_username = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_username:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_email:
        db.close()
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = password_hash.hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }