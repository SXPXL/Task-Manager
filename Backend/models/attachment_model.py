from sqlalchemy import Column,Date, Integer, String,ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Attachment(Base):
  """
  Represents a file attachment to a task.

  Attributes:
    id (int): Unique identifier for the attachment.
    task_id (int): ID of the task the file is attached to.
    filename (str): Name of the file.
    file_data (bytes): Binary data of the file.
    content_type (str): MIME type of the file.
    created_at (datetime): Timestamp of when the file was uploaded.
    task (relationship): Associated task object.
    """
  __tablename__ = "attachments"
  id = Column(Integer, primary_key=True, index=True)
  task_id = Column(Integer, ForeignKey("tasks.id"))
  filename = Column(String)
  file_data = Column(LargeBinary)  
  content_type = Column(String)
  task = relationship("Task", back_populates="attachments")
  created_at = Column(DateTime,default=datetime.utcnow)