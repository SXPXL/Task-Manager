# routers/summary_routes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from common.utils import get_current_user
from database.database import get_db
from common.permissions import manager_required
from services import summary_service

router = APIRouter()

@router.get("/user-summary")
def user_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return summary_service.get_user_summary(db, user)

@router.get("/project-summary")
def project_summary(db: Session = Depends(get_db), user=Depends(manager_required)):
    return summary_service.get_project_summary(db)

@router.get("/tasks/{status}")
def tasks_by_status(
    status: str, 
    user_id: int = Query(None), 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    return summary_service.get_tasks_by_status(db, user, status, user_id)
