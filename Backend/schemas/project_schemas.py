"""
Project Schemas
---------------
Defines Pydantic schemas for project creation and output/response.

Classes:
- ProjectCreate: For creating a new project
- ProjectOut: For sending project details in API responses
"""

from pydantic import BaseModel
from datetime import date

class ProjectCreate(BaseModel):
  """
    Schema for creating a new project.

    Attributes:
        title (str): The title of the project.
        description (str): Detailed description of the project.
    """
  title: str
  description: str
  start_date: date
  due_date: date

class ProjectOut(BaseModel):
  """
    Schema for sending project details in responses.

    Attributes:
        id (int): The unique identifier for the project.
        title (str): The title of the project.
        description (str): Description of the project.
    """
  id: int
  title: str
  description: str
  start_date: date
  due_date: date
  
  class Config:
    orm_mode = True