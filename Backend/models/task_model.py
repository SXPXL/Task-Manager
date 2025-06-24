from sqlalchemy import Column,Date, Integer, String,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database.database import Base


class Task(Base):
  '''
  Represents a task under a project.

  Attributes:
    id (int): Unique identifier for the task.
    title (str): Title of the task.
    description (str): Detailed description of the task.
    status (str): Current status of the task (e.g., pending, completed).
    start_date (date): Start date of the task.
    due_date (date): Due date for the task.
    assigned_to (int): User ID of the assignee.
    project_id (int): Project ID to which this task belongs.
    tool_id (int): tool ID to which this task belongs.
    project (relationship): Associated project object.
    assigned_user (relationship): Assigned user object.
    comments (relationship): Comments associated with the task.
    attachments (relationship): Attachments uploaded to the task.
    tools (relationship): Tool used in the task.

  '''
  __tablename__= "tasks"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  title = Column(String,nullable=False)
  description = Column(String,nullable=False)
  status = Column(String,default="pending")
  due_date = Column(Date,nullable=False)
  start_date = Column(Date,nullable=False)
  assigned_to = Column(Integer,ForeignKey("users.id"),nullable=True)
  project_id = Column(Integer,ForeignKey("projects.id"))
  project = relationship("Project", back_populates="tasks")
  assigned_user = relationship("User")
  comments = relationship("Comment", back_populates="task", cascade="all,delete")
  attachments = relationship("Attachment", back_populates="task", cascade="all, delete")
  tool_id = Column(Integer, ForeignKey('tools.id'), nullable=True)
  tool = relationship("Tool", back_populates="tasks")
  due_date_edited= Column(Boolean,default=False)
  due_date_change_reason = Column(String, nullable=True)