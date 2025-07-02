"""
Task and Project API Routes
--------------------------
Defines endpoints for creating, retrieving, updating, and deleting tasks and projects.

Routes:
- /create-tasks: Create a new task (manager only)
- /{project_id}/tasks: Get all tasks for a project
- /update-task/{task_id}: Update a task
- /delete-task/{task_id}: Delete a task (manager only)
- /create-projects: Create a new project (manager only)

Each route delegates business logic to the task_service module.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from schemas.task_schemas import TaskCreate, TaskUpdate, TaskOut
from schemas.project_schemas import ProjectCreate, ProjectOut
from schemas.attachment_schemas import AttachmentOut
from database.database import get_db
from services import task_service
from common.permissions import manager_required

router = APIRouter()

@router.post("/create-tasks", dependencies=[Depends(manager_required)], response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Creates a new task for a project (manager only).
    
    Args:
        task: TaskCreate schema with task details.
        db: Database session.
    Returns:
        The created TaskOut schema or error message.
    """
    result, error = task_service.create_task(db, task)
    if error:
        raise HTTPException(status_code=400 if "Due date" in error else 404, detail=error)
    return result

@router.get("/{project_id}/tasks", response_model=List[TaskOut])
def get_tasks(project_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all tasks for a specific project.
    
    Args:
        project_id: ID of the project.
        db: Database session.
    Returns:
        List of TaskOut schemas.
    """
    return task_service.get_tasks_by_project(db, project_id)

@router.put("/update-task/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing task.
    
    Args:
        task_id: ID of the task to update.
        task: TaskUpdate schema with updated details.
        db: Database session.
    Returns:
        The updated TaskOut schema or error message.
    """
    updated, error = task_service.update_task(db, task_id, task)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return updated

@router.delete("/delete-task/{task_id}", dependencies=[Depends(manager_required)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Deletes a task by its ID (manager only).
    
    Args:
        task_id: ID of the task to delete.
        db: Database session.
    Returns:
        Success message or error message.
    """
    deleted, error = task_service.delete_task(db, task_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"message": "Task deleted successfully"}

@router.post("/create-projects", dependencies=[Depends(manager_required)], response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Creates a new project (manager only).
    
    Args:
        project: ProjectCreate schema with project details.
        db: Database session.
    Returns:
        The created ProjectOut schema.
    """
    return task_service.create_project(db, project)

@router.get("/get-projects", response_model=List[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    """
    Retrieves all projects.
    
    Args:
        db: Database session.
    Returns:
        List of ProjectOut schemas.
    """
    return task_service.get_all_projects(db)

@router.delete("/delete-project/{project_id}", dependencies=[Depends(manager_required)])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Deletes a project by its ID (manager only).
    
    Args:
        project_id: ID of the project to delete.
        db: Database session.
    Returns:
        Success message or error message.
    """
    deleted, error = task_service.delete_project(db, project_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"message": "Project has been deleted successfully"}

@router.post("/tasks/{task_id}/attachments/")
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads an attachment for a task.
    
    Args:
        task_id: ID of the task.
        file: The file to upload.
        db: Database session.
    Returns:
        The result of the upload operation.
    """
    return await task_service.upload_attachment(db,task_id, file)


@router.get("/tasks/{task_id}/attachments/", response_model=List[AttachmentOut])
def get_attachments(task_id:int, db: Session = Depends(get_db)):
    """
    Retrieves all attachments for a task.
    
    Args:
        task_id: ID of the task.
        db: Database session.
    Returns:
        List of AttachmentOut schemas.
    """
    return task_service.get_attachments_by_task(task_id, db)


@router.get("/attachments/download/{attachment_id}")
def download_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """
    Downloads an attachment by its ID.
    
    Args:
        attachment_id: ID of the attachment.
        db: Database session.
    Returns:
        The attachment file or error message.
    """
    return task_service.download_attachment(attachment_id, db)