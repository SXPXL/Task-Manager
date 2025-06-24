"""
API routes for managing tools in a project: create, fetch, delete, and list related tasks.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.tool_schemas import ToolCreate, ToolOut
from schemas.task_schemas import TaskOut
from database.database import get_db
from common.utils import get_current_user
from models.user_model import User
from services import tool_service

router = APIRouter()

@router.post("/{project_id}/tools", response_model=ToolOut)
def create_tool(
    project_id: int,
    tool: ToolCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return tool_service.create_tool_for_project(db, project_id, tool, current_user)


@router.get("/{project_id}/tools", response_model=List[ToolOut])
def get_tools(
    project_id: int,
    db: Session = Depends(get_db)
):
    return tool_service.get_tools_by_project(db, project_id)


@router.delete("/tools/{tool_id}")
def delete_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tool_service.delete_tool_by_id(db, tool_id, current_user)
    return {"detail": "Tool deleted successfully"}


@router.get("/{project_id}/tools/{tool_id}/tasks", response_model=List[TaskOut])
def get_tasks_by_tool(
    project_id: int,
    tool_id: int,
    db: Session = Depends(get_db)
):
    return tool_service.get_tasks_by_tool(db, project_id, tool_id)
