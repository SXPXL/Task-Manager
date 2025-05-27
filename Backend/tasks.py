"""
This module defines API routes for managing projects, tasks, and attachments.

Imports:
- FastAPI modules for API routing, dependencies, exception handling, file upload, and file streaming.
- SQLAlchemy Session for DB interaction.
- Response models from `schemas` for validation and structure.
- ORM models for Project, Task, and Attachment from `models`.
- Dependencies for DB session and permission checks.
- BytesIO for streaming file content.
"""


from fastapi import APIRouter, Depends, HTTPException,File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from models import Project, Task, Attachment
from schemas import TaskCreate, TaskUpdate, TaskOut, ProjectCreate, ProjectOut, AttachmentOut
from database import get_db
from typing import List
from permissions import manager_required
from io import BytesIO

router = APIRouter()

@router.post("/create-projects",dependencies=[Depends(manager_required)])
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project. Only accessible to managers.

    Args:
        project (ProjectCreate): Project creation payload.
        db (Session): SQLAlchemy DB session.

    Returns:
        Project: Newly created project.
    """
    
    new_project = Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/get-projects", response_model=List[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    """
    Get all projects in the system.

    Args:
        db (Session): DB session.

    Returns:
        List[ProjectOut]: List of all projects.
    """

    projects = db.query(Project).all()
    return projects

@router.post("/create-tasks", dependencies=[Depends(manager_required)])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
   """
    Create a new task under a specific project.

    Validates:
    - Project must exist.
    - Due date should be after start date.

    Args:
        task (TaskCreate): Task creation payload.
        db (Session): DB session.

    Returns:
        Task: Created task.
    """
   
   project = db.query(Project).filter(Project.id==task.project_id).first()
   if not project:
        raise HTTPException(status_code=404, detail="Project not found")
   if task.due_date < task.start_date:
        raise HTTPException(status_code=400, detail="Due date cannot be before start date")
   new_task = Task(**task.dict())
   db.add(new_task)
   db.commit()
   db.refresh(new_task)
   return new_task

@router.get("/{project_id}/tasks", response_model=List[TaskOut])
def get_tasks(project_id: int,db:Session = Depends(get_db)):
    """
    Get all tasks under a specific project.

    Args:
        project_id (int): Project ID.
        db (Session): DB session.

    Returns:
        List[TaskOut]: List of tasks.
    """

    tasks = db.query(Task).filter(Task.project_id==project_id).all()  
    return tasks

@router.delete("/delete-task/{task_id}",dependencies=[Depends(manager_required)])
def delete_task(task_id:int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID. Only for managers.

    Args:
        task_id (int): Task ID.
        db (Session): DB session.

    Returns:
        dict: Success message.
    """
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.delete("/delete-project/{project_id}",dependencies=[Depends(manager_required)])
def delete_project(project_id:int, db: Session = Depends(get_db)):
    """
    Delete a project by ID. Only for managers.

    Args:
        project_id (int): Project ID.
        db (Session): DB session.

    Returns:
        dict: Success message.
    """
    
    project = db.query(Project).filter(Project.id==project_id).first()
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message":"Project has bee deleted successfully"}
  

@router.put("/update-task/{task_id}", response_model=TaskOut)
def update_task(task_id:int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task's details.

    Args:
        task_id (int): Task ID to update.
        task (TaskUpdate): Fields to update.
        db (Session): DB session.

    Returns:
        TaskOut: Updated task.
    """
    
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.post("/tasks/{task_id}/attachments/")
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a .eml email file as an attachment to a task.

    Args:
        task_id (int): Task to attach the file to.
        file (UploadFile): .eml file upload.
        db (Session): DB session.

    Returns:
        dict: Uploaded file info (filename and ID).
    """

    if not file.filename.lower().endswith('.eml'):
        raise HTTPException(status_code=400, detail='Only .eml files are allowed')
       
    content = await file.read()

    attachment = Attachment(
        filename=file.filename,
        content_type=file.content_type,
        file_data=content,
        task_id=task_id
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return {"filename": attachment.filename, "id": attachment.id}


@router.get("/tasks/{task_id}/attachments/",response_model=List[AttachmentOut])
def get_attachments(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all email attachments for a task, sorted by newest first.

    Args:
        task_id (int): Task ID.
        db (Session): DB session.

    Returns:
        List[AttachmentOut]: List of email attachments.
    """
    
    emails = db.query(Attachment).filter(Attachment.task_id == task_id).order_by(Attachment.created_at.desc()).all()
    return emails
    

@router.get("/attachments/download/{attachment_id}")
def download_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """
    Download a .eml email attachment by ID.

    Args:
        attachment_id (int): Attachment ID.
        db (Session): DB session.

    Returns:
        StreamingResponse: Streamed .eml file for download.
    """
    
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    return StreamingResponse(
        BytesIO(attachment.file_data),
        media_type="message/rfc822",  
        headers={"Content-Disposition": f"attachment; filename={attachment.filename}"}
    )
