"""
Service layer for managing tools and related tasks under projects.
Handles validation, permission checks, and database operations.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.tool_model import Tool
from models.project_model import Project 
from models.task_model import Task 
from models.user_model import User
from schemas.tool_schemas import ToolCreate
from typing import List


def create_tool_for_project(db: Session, project_id: int, tool_in: ToolCreate, current_user: User) -> Tool:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="You don't have permission")

    new_tool = Tool(name=tool_in.name, project_id=project_id)
    db.add(new_tool)
    db.commit()
    db.refresh(new_tool)
    return new_tool


def get_tools_by_project(db: Session, project_id: int) -> List[Tool]:
    return db.query(Tool).filter(Tool.project_id == project_id).all()


def delete_tool_by_id(db: Session, tool_id: int, current_user: User) -> None:
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    project = db.query(Project).filter(Project.id == tool.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="You cannot delete this")

    db.delete(tool)
    db.commit()


def get_tasks_by_tool(db: Session, project_id: int, tool_id: int) -> List[Task]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tool = db.query(Tool).filter(Tool.id == tool_id, Tool.project_id == project_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    return db.query(Task).filter(Task.project_id == project_id, Task.tool_id == tool_id).all()
