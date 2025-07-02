"""
Comment Schemas
---------------
Defines Pydantic schemas for comment creation, base, and output/response.

Classes:
- CommentBase: Base schema for comment data
- CommentCreate: For creating a new comment
- CommentOut: For sending comment details in API responses
"""

from pydantic import BaseModel
from datetime import datetime
from schemas.user_schemas import UserOut

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