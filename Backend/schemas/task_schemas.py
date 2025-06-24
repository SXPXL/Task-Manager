from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class TaskCreate(BaseModel):
  """
    Schema for creating a new task.

    Attributes:
        title (str): Title of the task.
        description (str): Description of the task.
        due_date (date): Due date for the task completion.
        start_date (date): Starting date of the task.
        assigned_to (int): User ID the task is  the assigned to.
        project_id (int): Project ID under which the task falls.
        tool_id (int): ID of the tool used in the task.
    """
  title: str
  description: str
  due_date: date
  start_date: date
  assigned_to: int
  project_id: int
  tool_id: int
  


class TaskOut(BaseModel):
  """
    Schema for sending task details in responses.

    Attributes:
        id (int): Unique task identifier.
        title (str): Task title.
        status (str): Current status of the task (e.g., pending, completed).
        due_date (date): Task due date.
        start_date (date): Task start date.
        assigned_to (int): User ID the task is assigned to.
        project_id (int): ID of the related project.
        description (str): Description of the task.
        tool_id (int): Stores the id of the tool used in the task.
    """
  id:int
  title:str
  status:str
  due_date:date
  start_date:date
  assigned_to:Optional[int]
  project_id:int
  description:str
  tool_id: Optional[int]
  due_date_change_reason: Optional[str]
  due_date_edited: bool

  class Config:
    orm_mode = True

class TaskUpdate(BaseModel):
  """
    Schema for updating task fields (partial updates allowed).

    Attributes:
        title (Optional[str]): New title for the task.
        description (Optional[str]): New description.
        status (Optional[str]): New status.
        due_date (Optional[date]): New due date.
        start_date (Optional[date]): New start date.
    """
  title: Optional[str] = None
  description: Optional[str] = None
  status: Optional[str] = None
  due_date: Optional[date] = None
  start_date: Optional[date] = None
  due_date_change_reason: Optional[str] = None
  