"""
This module provides API routes for task and project summaries.

Imports:
- fastapi.APIRouter: Used to create a router for grouping related API routes.
- fastapi.Depends: Allows dependency injection for getting DB sessions and user info.
- fastapi.HTTPException: Used to raise HTTP errors like 400 Bad Request.
- sqlalchemy.orm.Session: SQLAlchemy session class for DB operations.
- datetime, timedelta: For working with timestamps and filtering tasks by due dates.
- models: Contains ORM models for Task, Project, User, etc.
- auth.get_current_user: Dependency to get the currently authenticated user from JWT.
- database.get_db: Dependency to get a database session.
- permissions.manager_required: Dependency to enforce manager-level permissions on endpoints.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
from auth import get_current_user
from database import get_db
from permissions import manager_required


router = APIRouter()


@router.get("/user-summary")
def user_summary(db: Session = Depends(get_db),user=Depends(get_current_user)):
  """
    Returns a summary of tasks for the authenticated user.

    Counts the number of:
    - Assigned tasks
    - Completed tasks
    - Overdue tasks (due date passed, not completed)
    - Soon due tasks (due within next 2 days, not completed)

    Args:
        db (Session): Database session, injected via Depends.
        user (User): Current authenticated user, injected via Depends.

    Returns:
        dict: Summary counts keyed by task status.
  """

  now = datetime.utcnow()
  soon = now + timedelta(days=2)

  assigned = db.query(models.Task).filter(
  models.Task.assigned_to == user.id).count()

  completed = db.query(models.Task).filter(
  models.Task.assigned_to == user.id,
  models.Task.status == "completed").count()

  overdue = db.query(models.Task).filter(
  models.Task.assigned_to == user.id,
  models.Task.due_date < now,
  models.Task.status != "completed").count()

  soon_due = db.query(models.Task).filter(
  models.Task.assigned_to == user.id,
  models.Task.due_date >= now,
  models.Task.due_date <= soon,
  models.Task.status != "completed").count()


  return {
    "username": user.id,
    "assigned_tasks": assigned,
    "completed_tasks": completed,
    "overdue_tasks": overdue,
    "soon_due_tasks": soon_due
  }



@router.get("/project-summary")
def project_summary(
  db: Session = Depends(get_db),
  user = Depends(manager_required)):
  """
    Returns a summary of all projects with counts of total, completed, and pending tasks.

    Access restricted to users with manager or higher roles.

    Args:
        db (Session): Database session.
        user (User): Current user with manager permissions.

    Returns:
        list: Each element is a dict with project name and task counts.
    """

  projects = db.query(models.Project).all()
  result = []
  for project in projects:
    tasks = db.query(models.Task).filter(models.Task.project_id == project.id)
    result.append({
      "project_name": project.title,
      "total_tasks": tasks.count(),
      "completed_tasks": tasks.filter(models.Task.status == "completed").count(),
      "pending_tasks": tasks.filter(models.Task.status != "completed").count(),
    })
  return result
  

  

@router.get("/tasks/{status}")
def tasks_by_status(
    status: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Returns a list of tasks assigned to the current user filtered by task status.

    Supported statuses:
    - assigned_tasks: all assigned tasks
    - completed_tasks: tasks with status "completed"
    - overdue_tasks: tasks overdue and not completed
    - due_soon: tasks due within next 2 days and not completed

    Args:
        status (str): Status filter string.
        db (Session): Database session.
        user (User): Current authenticated user.

    Raises:
        HTTPException: 400 Bad Request for invalid status filter.

    Returns:
        list: Tasks matching the filter.
    """
    
    now = datetime.utcnow()
    soon = now + timedelta(days=2)

    query = db.query(models.Task).filter(models.Task.assigned_to == user.id)

    if status == "assigned_tasks":
        pass
    elif status == "completed_tasks":
        query = query.filter(models.Task.status == "completed")
    elif status == "overdue_tasks":
        query = query.filter(
            models.Task.due_date < now,
            models.Task.status != "completed"
        )
    elif status == "due_soon":
        query = query.filter(
            models.Task.due_date >= now,
            models.Task.due_date <= soon,
            models.Task.status != "completed"
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid status filter")

    return query.all()
