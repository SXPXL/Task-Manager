"""
Summary API Routes
------------------
Defines endpoints for retrieving user and project summaries, and tasks by status.

Routes:
- /user-summary: Get summary for the current user
- /project-summary: Get summary for all projects (manager only)
- /tasks/{status}: Get tasks filtered by status and optionally by user

Each route delegates business logic to the summary_service module.
"""

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
    """
    Retrieves a summary for the current user.
    
    Args:
        db: Database session.
        user: The current authenticated user.
    Returns:
        User summary data.
    """
    return summary_service.get_user_summary(db, user)

@router.get("/project-summary")
def project_summary(db: Session = Depends(get_db), user=Depends(manager_required)):
    """
    Retrieves a summary for all projects (manager access required).
    
    Args:
        db: Database session.
        user: The current manager user.
    Returns:
        Project summary data.
    """
    return summary_service.get_project_summary(db)

@router.get("/tasks/{status}")
def tasks_by_status(
    status: str, 
    user_id: int = Query(None), 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    """
    Retrieves tasks filtered by status and optionally by user.
    
    Args:
        status: Status to filter tasks by.
        user_id: (Optional) User ID to filter tasks for a specific user.
        db: Database session.
        user: The current authenticated user.
    Returns:
        List of tasks matching the criteria.
    """
    return summary_service.get_tasks_by_status(db, user, status, user_id)
