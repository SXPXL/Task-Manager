# services/summary_service.py
from datetime import datetime, timedelta
from models import task_model as models
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Query

def get_user_summary(db: Session, user):
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

def get_tasks_by_status(db: Session, user, status: str,user_id:int = Query(None)):
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
