from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()


@app.get("/")
def home():
    return {"message": "DevBoard backend is running"}

projects = [
    {"id": 1, "name": "DevBoard"},
    {"id": 2, "name": "Test Project"}
]

class ProjectCreate(BaseModel):
    name: str


@app.get("/projects")
def get_projects():
    return projects

@app.post("/projects")
def create_project(project: ProjectCreate):
    new_project = {
        "id": len(projects) + 1,
        "name": project.name
    }

    projects.append(new_project)

    return new_project