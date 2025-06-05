"""
This module defines API routes for managing tools associated with projects,
including creation, retrieval, deletion, and task filtering by tool.

Imports:
- FastAPI modules for API routing, dependency injection, and exception handling.
- SQLAlchemy Session for database interaction.
- Pydantic schemas for input/output validation.
- ORM models for Project, Task, Tool, and User.
- Dependency functions for DB session and user authentication.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Project, Task, Tool, User
from schemas import ToolCreate,ToolOut, TaskOut
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/{project_id}/tools",response_model=ToolOut)
def create_tool(
  project_id: int,
  tool: ToolCreate, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
  """
    Create a new tool for a specific project. Only admins and managers are allowed.

    Args:
        project_id (int): ID of the project to associate the tool with.
        tool (ToolCreate): Payload containing the tool's details.
        db (Session): SQLAlchemy DB session.
        current_user (User): Authenticated user.

    Returns:
        ToolOut: The newly created tool.
    """

  project = db.query(Project).filter(Project.id == project_id).first()
  if not project:
    raise HTTPException(status_code=404,detail="Project not found")
  if current_user.role not in ['admin','manager']:
    raise HTTPException(status_code=403, detail="You dont have the permission to add a tool")
                               
  new_tool = Tool(name = tool.name, project_id = project_id)
  db.add(new_tool)
  db.commit()
  db.refresh(new_tool)
  return new_tool

@router.get("/{project_id}/tools", response_model=List[ToolOut])
def get_tools(
  project_id: int,
  db:Session=Depends(get_db)
  ):
  """
    Retrieve all tools associated with a specific project.

    Args:
        project_id (int): ID of the project.
        db (Session): DB session.

    Returns:
        List[ToolOut]: List of tools.
    """

  tools = db.query(Tool).filter(Tool.project_id == project_id).all()
  return tools

@router.delete("/tools/{tool_id}")
def delete_tool(
  tool_id: int, 
  db:Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):

  """
    Delete a tool by its ID. Only accessible to admins and managers.

    Args:
        tool_id (int): ID of the tool to delete.
        db (Session): DB session.
        current_user (User): Authenticated user.

    Returns:
        dict: Success message on deletion.
    """
  tool =db.query(Tool).filter(Tool.id == tool_id).first()
  if not tool:
    raise HTTPException(status_code=404,detail="Tool not found")
  if current_user.role not in ['admin','manager']:
    raise HTTPException(status_code=403,detail="You cannot delete this.")
  db.delete(tool)
  db.commit()
  return {"details": "Tool deleted successfully"}

@router.get("/{project_id}/tools/{tool_id}/tasks",response_model=List[TaskOut])
def get_tasks_by_tool(
  project_id:int,
  tool_id: int,
  db: Session = Depends(get_db),
  ):
  """
    Retrieve all tasks associated with a specific tool under a given project.

    Args:
        project_id (int): ID of the project.
        tool_id (int): ID of the tool.
        db (Session): DB session.

    Returns:
        List[TaskOut]: List of tasks linked to the tool.
    """
  
  project =db.query(Project).filter(Project.id == project_id).first()
  if not project:
    raise HTTPException(status_code=404,details="Project not found")
  
  tool =db.query(Tool).filter(Tool.id == tool_id, Tool.project_id == project_id).first()
  if not tool:
    raise HTTPException(status_code=404,detail="Tool not found")
  
  tasks = db.query(Task).filter(Task.project_id == project_id, Task.tool_id == tool_id).all()
  return tasks
