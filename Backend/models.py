from sqlalchemy import Column,Date, Integer, String,ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime



class User(Base):
  '''
  Represents a user in the system.

  Attributes:
    id (int): Unique identifier for the user.
    username (str): Name of the user.
    email (str): Email address of the user (unique).
    hashed_password (str): Password stored in a hashed format.
    role (str): Role of the user (e.g., admin, manager, member).
    comments (relationship): List of comments made by the user.
  '''
  __tablename__ = "users"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  username =  Column(String,nullable=False)
  email  = Column(String,unique=True,nullable=False,index=True,)
  hashed_password = Column(String,nullable=False)
  role = Column(String,default="member")
  comments = relationship("Comment", back_populates="user", cascade="all,delete")
  
  



class Project(Base):
  '''
  Represents a project entity.

  Attributes:
    id (int): Unique identifier for the project.
    title (str): Title of the project.
    description (str): Description of the project.
    tasks (relationship): List of tasks under the project.
    tools (relationship): List of toold under the project.
  '''
  __tablename__= "projects"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  title = Column(String,index=True)
  description = Column(String,nullable=False)
  tasks = relationship("Task", back_populates="project", cascade="all,delete")
  tools = relationship("Tool",back_populates="project", cascade="all,delete")

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

class Tool(Base):
  """
  Represent all the tools available in a task
  
  Attributes:
  id (int): Unique identifier for the tool.
  name (string): Name of the tool.
  project_id (int): The ID of the project where the tool is added.
  project (relationship): A relation between tool and project.
  tasks (relationship): A relation between tool and tasks.
  """
  __tablename__ = 'tools'
  id = Column(Integer,primary_key=True,index=True)
  name = Column(String,nullable=False)
  project_id = Column(Integer,ForeignKey('projects.id'))
  project = relationship("Project", back_populates="tools")
  tasks = relationship("Task", back_populates="tool",cascade="all,delete")
  
  