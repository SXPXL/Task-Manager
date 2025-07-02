"""
Attachment Schemas
------------------
Defines Pydantic schemas for attachment output/response.

Classes:
- AttachmentOut: For sending attachment details in API responses
"""

from pydantic import BaseModel
from datetime import datetime


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

