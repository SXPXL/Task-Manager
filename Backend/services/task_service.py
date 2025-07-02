"""
Task Service Module
------------------
Provides business logic and helper functions for task management.

Features:
- Create, update, and delete tasks with validation (dates, project existence, etc.)
- Attachments and relationships with projects and users
- Handles error responses for invalid operations
- Used by API routes to interact with the database

Functions:
- create_task: Validates and creates a new task
- update_task: Updates an existing task
- delete_task: Removes a task from the database
- Additional helpers for task operations
"""

from fastapi import HTTPException
from datetime import date
from sqlalchemy.orm import Session
from models.task_model import Task
from models.project_model import Project
from models.attachment_model import Attachment
from schemas.task_schemas import TaskCreate, TaskUpdate
from schemas.project_schemas import ProjectCreate
from fastapi.responses import StreamingResponse
from io import BytesIO
from typing import Tuple, Optional

def create_task(db: Session, task: TaskCreate) -> Tuple[Optional[Task], Optional[str]]:
    """
    Validates and creates a new task for a project, ensuring dates are within project bounds.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        task (TaskCreate): Schema containing task details.
    
    Variables:
        project: The Project object found by task.project_id.
    Returns:
        Tuple of (created Task object or None, error message or None).
    Raises:
        HTTPException: If task dates are invalid.
    """
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        return None, "Project not found"
    if task.start_date < project.start_date or task.start_date > project.due_date:
        raise HTTPException(
            status_code=400, 
            detail="Task start date must be within the project's start and due dates."
        )
    if task.due_date < project.start_date or task.due_date > project.due_date:
        raise HTTPException(
            status_code=400, 
            detail="Task due date must be within the project's start and due dates."
        )
    if task.due_date < task.start_date:
        raise HTTPException(
            status_code=400, 
            detail="Task due date cannot be before start date."
        )
    task = Task(**task.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task, None

def get_tasks_by_project(db: Session, project_id: int):
    """
    Retrieves all tasks for a specific project.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        project_id (int): ID of the project.
    Returns:
        List of Task objects for the project.
    """
    return db.query(Task).filter(Task.project_id == project_id).all()

def update_task(db: Session, task_id: int, task_in: TaskUpdate):
    """
    Updates an existing task with new details.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        task_id (int): ID of the task to update.
        task_in (TaskUpdate): Schema containing updated task details.
    
    Variables:
        task: The Task object found by task_id.
    Returns:
        Tuple of (updated Task object or None, error message or None).
    Raises:
        HTTPException: If the task is not found or dates are invalid.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None, "Task not found"
    old_due_date = task.due_date
    new_due_date = task_in.due_date if "due_date" in task_in.dict(exclude_unset=True) else old_due_date
    if old_due_date != new_due_date:
        task.due_date_edited = True
        task.due_date_change_reason = task_in.due_date_change_reason
    for key, value in task_in.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task, None

def delete_task(db: Session, task_id: int):
    """
    Removes a task from the database.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        task_id (int): ID of the task to delete.
    Returns:
        Tuple of (deleted Task object or None, error message or None).
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None, "Task not found"
    db.delete(task)
    db.commit()
    return task, None

async def upload_attachment(db: Session, task_id: int, file) -> Tuple[Optional[dict], Optional[str]]:
    """
    Uploads an attachment (EML or PDF file) to a task.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        task_id (int): ID of the task to attach the file to.
        file: The file object uploaded by the user.
    
    Returns:
        Tuple of (attachment info dictionary or None, error message or None).
    """
    filename = file.filename.lower()
    if not (filename.endswith(".eml") or filename.endswith(".pdf")):
        return None, "Only .eml or .pdf files are allowed"
    content = await file.read()
    attachment = Attachment(
        filename=file.filename,
        content_type=file.content_type,
        file_data=content,
        task_id=task_id,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return {"filename": attachment.filename, "id": attachment.id}, None

def get_attachments_by_task(task_id: int, db: Session,):
    """
    Retrieves all attachments for a specific task, ordered by creation date.
    
    Args:
        task_id (int): ID of the task.
        db (Session): SQLAlchemy database session for DB operations.
    Returns:
        List of Attachment objects for the task.
    """
    return db.query(Attachment).filter(Attachment.task_id == task_id).order_by(Attachment.created_at.desc()).all()

def download_attachment(attachment_id: int, db: Session):
    """
    Downloads an attachment by its ID.
    
    Args:
        attachment_id (int): ID of the attachment to download.
        db (Session): SQLAlchemy database session for DB operations.
    Returns:
        StreamingResponse for the attachment file.
    Raises:
        HTTPException: If the attachment is not found.
    """
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return StreamingResponse(
        BytesIO(attachment.file_data),
        media_type="message/rfc822",
        headers={"Content-Disposition": f"attachment; filename={attachment.filename}"},
    )

def create_project(db: Session, project_in: ProjectCreate):
    """
    Creates a new project with validated start and due dates.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        project_in (ProjectCreate): Schema containing project details.
    
    Returns:
        The created Project object.
    Raises:
        HTTPException: If project dates are invalid.
    """
    project = Project(**project_in.dict())
    today = date.today()
    if project.start_date < today:
        raise HTTPException(status_code=400, detail="Project start date cannot be in the past.")
    if project.due_date < today:
        raise HTTPException(status_code=400, detail="Project due date cannot be in the past.")
    if project.due_date < project.start_date:
        raise HTTPException(status_code=400, detail="Project due date cannot be before start date.")
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_all_projects(db: Session):
    """
    Retrieves all projects from the database.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
    Returns:
        List of all Project objects.
    """
    return db.query(Project).all()

def delete_project(db: Session, project_id: int):
    """
    Removes a project and its associated tasks and attachments from the database.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        project_id (int): ID of the project to delete.
    Returns:
        Tuple of (deleted Project object or None, error message or None).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None, "Project not found"
    db.delete(project)
    db.commit()
    return project, None

