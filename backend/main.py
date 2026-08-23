from urllib import response

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Base, engine, SessionLocal
import models
from pwdlib import PasswordHash 
import os
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

password_hash = PasswordHash.recommended()
security = HTTPBearer()


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

class UserLogin(BaseModel):
    username: str
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

def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload.get("sub"))

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    db.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.post("/projects")
def create_project(
    project: ProjectCreate,
    current_user = Depends(get_current_user)
):
    db = SessionLocal()

    new_project = models.Project(
        name=project.name,
        user_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    db.close()

    return new_project



@app.get("/projects")
def get_projects(
    current_user = Depends(get_current_user)
):
    db = SessionLocal()

    projects = db.query(models.Project).filter(
        models.Project.user_id == current_user.id
    ).all()

    db.close()

    return projects

@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    current_user = Depends(get_current_user)
):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()

    db.close()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@app.put("/projects/{project_id}")
def update_project(
    project_id: int,
    updated_project: ProjectUpdate,
    current_user = Depends(get_current_user)
):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
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
def delete_project(
    project_id: int,
    current_user = Depends(get_current_user)
):
    db = SessionLocal()

    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
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

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload.get("sub"))

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    db.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

@app.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }


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

@app.post("/login")
def login_user(credentials: UserLogin):
    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == credentials.username
    ).first()

    if not user:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_is_valid = password_hash.verify(
        credentials.password,
        user.hashed_password
    )

    if not password_is_valid:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(user.id)

    response = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

    db.close()
    return response
