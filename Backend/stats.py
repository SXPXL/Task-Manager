from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
from auth import get_current_user
from database import get_db
from permissions import manager_required,admin_required,member_required

router = APIRouter()

now = datetime.utcnow()
soon = now + timedelta(days=2)

#user summary

@router.get("/user-summary")
def user_summary(db: Session = Depends(get_db),user=Depends(get_current_user)):

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

# project summary

@router.get("/project-summary")
def project_summary(
  db: Session = Depends(get_db),
  user = Depends(manager_required)):
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
  

  #listing tasks by status

@router.get("/tasks/{status}")
def tasks_by_status(
    status: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    query = db.query(models.Task).filter(models.Task.assigned_to == user.id)

    if status == "assigned_tasks":
        # No extra filter — show all assigned tasks
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
