from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional




class UserCreate(BaseModel):
  """
    Schema for creating a new user during registration.

    Attributes:
        username (str): The user's chosen username.
        email (EmailStr): The user's email address.
        password (str): The user's password in plain text (will be hashed later).
    """
  username: str
  email: EmailStr
  password: str


class UserLogin(BaseModel):
  """
    Schema for user login credentials.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
  email: EmailStr
  password: str



class UserOut(BaseModel):
  """
    Schema for sending user details in responses.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's username.
        email (EmailStr): The user's email.
        role (str): The user's role (e.g., admin, member).
    """
  id: int
  username: str
  email: EmailStr
  role: str

  class Config:
    orm_mode = True

class ProjectCreate(BaseModel):
  """
    Schema for creating a new project.

    Attributes:
        title (str): The title of the project.
        description (str): Detailed description of the project.
    """
  title: str
  description: str

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
    """
  title: str
  description: str
  due_date: date
  start_date: date
  assigned_to: int
  project_id: int
  


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
    """
  id:int
  title:str
  status:str
  due_date:date
  start_date:date
  assigned_to:int
  project_id:int
  description:str

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


class CommentBase(BaseModel):
  """
    Base schema for comment data.

    Attributes:
        content (str): The comment content.
    """
  content: str

class CommentCreate(CommentBase):
  """
    Schema for creating a new comment.
    Inherits content field from CommentBase.
    """
  pass

class CommentOut(CommentBase):
  """
    Schema for sending comment details in responses.

    Attributes:
        id (int): Comment identifier.
        user_id (int): ID of the user who wrote the comment.
        task_id (int): ID of the task the comment belongs to.
        created_at (datetime): Timestamp of comment creation.
        user (UserOut): Nested user info who created the comment.
    """
  id: int
  user_id: int
  task_id: int
  created_at: datetime
  user: UserOut

  class Config:
    orm_mode = True

class AttachmentOut(BaseModel):
  """
    Schema for sending attachment details in responses.

    Attributes:
        id (int): Attachment identifier.
        filename (str): Name of the attached file.
        task_id (int): ID of the related task.
        created_at (datetime): Timestamp when the attachment was added.
    """
  id: int 
  filename: str
  task_id: int
  created_at: datetime

  class Config:
    orm_mode = True

  
