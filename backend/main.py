from fastapi import FastAPI, HTTPException
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

class ProjectUpdate(BaseModel):
    name: str

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            projects.remove(project)
            return {"message": "Project deleted successfully"}

    raise HTTPException(status_code=404, detail="Project not found")

@app.put("/projects/{project_id}")
def update_project(project_id: int, updated_project: ProjectUpdate):
    for project in projects:
        if project["id"] == project_id:
            project["name"] = updated_project.name
            return project

    raise HTTPException(status_code=404, detail="Project not found")