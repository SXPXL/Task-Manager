"""
Tool API Routes
---------------
Defines endpoints for creating, retrieving, and deleting tools for a project, and listing related tasks.

Routes:
- /{project_id}/tools (POST): Create a tool for a project
- /{project_id}/tools (GET): Get all tools for a project
- /tools/{tool_id} (DELETE): Delete a tool by ID

Each route delegates business logic to the tool_service module.
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
    """
    Creates a new tool for a specific project.
    
    Args:
        project_id: ID of the project to add the tool to.
        tool: ToolCreate schema with tool details.
        db: Database session.
        current_user: User creating the tool.
    Returns:
        The created ToolOut schema.
    """
    return tool_service.create_tool_for_project(db, project_id, tool, current_user)


@router.get("/{project_id}/tools", response_model=List[ToolOut])
def get_tools(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves all tools for a specific project.
    
    Args:
        project_id: ID of the project.
        db: Database session.
    Returns:
        List of ToolOut schemas.
    """
    return tool_service.get_tools_by_project(db, project_id)


@router.delete("/tools/{tool_id}")
def delete_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes a tool by its ID.
    
    Args:
        tool_id: ID of the tool to delete.
        db: Database session.
        current_user: User performing the deletion.
    Returns:
        Result of the deletion operation.
    """
    tool_service.delete_tool_by_id(db, tool_id, current_user)
    return {"detail": "Tool deleted successfully"}


@router.get("/{project_id}/tools/{tool_id}/tasks", response_model=List[TaskOut])
def get_tasks_by_tool(
    project_id: int,
    tool_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves all tasks associated with a specific tool in a project.
    
    Args:
        project_id: ID of the project.
        tool_id: ID of the tool.
        db: Database session.
    Returns:
        List of TaskOut schemas related to the tool.
    """
    return tool_service.get_tasks_by_tool(db, project_id, tool_id)
