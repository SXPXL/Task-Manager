"""
Summary Service
---------------
Provides business logic for generating user and project summaries, and filtering tasks by status.

Functions:
- get_user_summary: Returns summary stats for a user
- get_project_summary: Returns summary stats for all projects
- get_tasks_by_status: Returns tasks filtered by status and user
"""

# services/summary_service.py
from datetime import datetime, timedelta
from models import task_model as models
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Query

def get_user_summary(db: Session, user):
    """
    Returns summary statistics for a user, including assigned, completed, overdue, and soon-due tasks.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        user: The user object for whom to generate the summary.
    
    Variables:
        now: Current UTC datetime.
        soon: Datetime two days from now.
        assigned: Count of tasks assigned to the user.
        completed: Count of completed tasks.
        overdue: Count of overdue tasks.
        soon_due: Count of tasks due soon.
    Returns:
        Dictionary with summary statistics for the user.
    """
    now = datetime.utcnow()
    soon = now + timedelta(days=2)

    assigned = db.query(models.Task).filter(models.Task.assigned_to == user.id).count()
    completed = db.query(models.Task).filter(models.Task.assigned_to == user.id, models.Task.status == "completed").count()
    overdue = db.query(models.Task).filter(models.Task.assigned_to == user.id, models.Task.due_date < now, models.Task.status != "completed").count()
    soon_due = db.query(models.Task).filter(models.Task.assigned_to == user.id, models.Task.due_date >= now, models.Task.due_date <= soon, models.Task.status != "completed").count()

    return {
        "username": user.id,
        "assigned_tasks": assigned,
        "completed_tasks": completed,
        "overdue_tasks": overdue,
        "soon_due_tasks": soon_due
    }

def get_project_summary(db: Session):
    """
    Returns summary statistics for all projects, including total, completed, and pending tasks per project.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
    
    Variables:
        projects: List of all Project objects.
        result: List of summary dictionaries for each project.
        tasks: Query for tasks in each project.
    Returns:
        List of dictionaries with project summary statistics.
    """
    projects = db.query(models.Project).all()
    result = []
    for project in projects:
        tasks = db.query(models.Task).filter(models.Task.project_id == project.id)
        result.append({
            "project_name": project.title,
            "total_tasks": tasks.count(),
            "completed_tasks": tasks.filter(models.Task.status == "completed").count(),
            "pending_tasks": tasks.filter(models.Task.status != "completed").count()
        })
    return result

def get_tasks_by_status(db: Session, user, status: str, user_id: int = Query(None)):
    """
    Returns tasks filtered by status and optionally by user.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        user: The user requesting the data.
        status (str): Status to filter tasks by.
        user_id (int, optional): User ID to filter tasks for a specific user.
    
    Variables:
        now: Current UTC datetime.
        soon: Datetime two days from now.
        target_user_id: The user ID to filter tasks for.
        query: SQLAlchemy query for tasks.
    Returns:
        List of Task objects matching the criteria.
    Raises:
        HTTPException: If not authorized.
    """
    now = datetime.utcnow()
    soon = now + timedelta(days=2)
    if user_id is not None:
        if user.role != "admin":
            raise HTTPException(status_code=403, details="Not authorized")
        
        target_user_id =user_id
    else:
        target_user_id = user.id
    query = db.query(models.Task).filter(models.Task.assigned_to == target_user_id)

    if status == "assigned_tasks":
        pass
    elif status == "completed_tasks":
        query = query.filter(models.Task.status == "completed")
    elif status == "overdue_tasks":
        query = query.filter(models.Task.due_date < now, models.Task.status != "completed")
    elif status == "due_soon":
        query = query.filter(models.Task.due_date >= now, models.Task.due_date <= soon, models.Task.status != "completed")
    else:
        raise HTTPException(status_code=400, detail="Invalid status filter")

    return query.all()
