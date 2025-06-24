from sqlalchemy import Column, Integer, String,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime
class Comment(Base):
  '''
Represents a comment made by a user on a task.

  Attributes:
    id (int): Unique identifier for the comment.
    content (str): Content of the comment.
    created_at (datetime): Timestamp when the comment was created.
    user_id (int): ID of the user who made the comment.
    task_id (int): ID of the task the comment is associated with.
    user (relationship): User object who made the comment.
    task (relationship): Task object the comment is linked to.
  '''
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True)
  content = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer, ForeignKey("users.id"))
  task_id = Column(Integer, ForeignKey("tasks.id"))
  user = relationship("User", back_populates="comments")
  task = relationship("Task", back_populates="comments")